// GLASSHOUSE API - every route in one router over the record.
//
// Three tiers of caller:
//   bots    write with  x-glasshouse-key == env.GLASSHOUSE_KEY
//   humans  write with  x-team-pin       == env.TEAM_PIN   (the sender check)
//   anyone  reads       GETs are open, same standing as the old hub (auth off
//                       by Zac's call; PIN guards every write that steers a bot)
//
// Values are ex VAT everywhere. Every write lands an event with an author.

const J = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json", "access-control-allow-origin": "*" },
  });

const now = () => new Date().toISOString().slice(0, 19).replace("T", " ");

// ---------------------------------------------------------------- registry
// Partial upsert by design: one caller setting `stage` must never blank the
// `value` another caller set an hour earlier.
const UPSERTABLE = {
  company: {
    key: "key",
    cols: ["name", "relationship", "lifetime_value", "payment_terms", "position", "meta_json"],
    required: { name: (k) => k },
  },
  lead: {
    key: "key",
    cols: ["company_key", "title", "stage", "owner", "value", "deadline", "award_due",
      "next_action", "next_action_date", "outcome", "outcome_why", "position", "meta_json"],
    required: { title: (k) => k, company_key: () => "unknown" },
  },
  contract: {
    key: "key",
    cols: ["lead_key", "company_key", "title", "po_ref", "value", "site_date",
      "status", "position", "meta_json"],
    required: { title: (k) => k, company_key: () => "unknown" },
  },
};

const STAGES = ["new", "acknowledged", "materials_out", "awaiting_costs", "quote_ready",
  "pre_quote_call", "quote_sent", "follow_up", "final_follow_up", "closed"];
const PERSONAS = ["mary", "jacob", "joseph"];
const POSITION_CAP = 8000; // chars. A memory that cannot bloat.

async function upsert(db, table, key, fields, author, why) {
  const reg = UPSERTABLE[table];
  if (!reg) throw new Error("not upsertable: " + table);
  if (table === "lead" && fields.stage && !STAGES.includes(fields.stage))
    throw new Error("unknown stage " + fields.stage);
  if (fields.position && fields.position.length > POSITION_CAP)
    fields.position = fields.position.slice(0, POSITION_CAP);

  const existing = await db.prepare(`SELECT * FROM ${table} WHERE key = ?`).bind(key).first();
  const clean = {};
  for (const c of reg.cols) if (fields[c] !== undefined && fields[c] !== null) clean[c] = fields[c];

  if (!existing) {
    for (const [col, dflt] of Object.entries(reg.required))
      if (clean[col] === undefined) clean[col] = dflt(key);
    const cols = ["key", ...Object.keys(clean), "updated_by"];
    await db.prepare(
      `INSERT INTO ${table} (${cols.join(",")}) VALUES (${cols.map(() => "?").join(",")})`
    ).bind(key, ...Object.values(clean), author).run();
  } else {
    const changed = Object.keys(clean).filter((c) => String(existing[c] ?? "") !== String(clean[c]));
    if (!changed.length) return { key, changed: [] };
    await db.prepare(
      `UPDATE ${table} SET ${changed.map((c) => c + " = ?").join(",")},
       updated = datetime('now'), updated_by = ? WHERE key = ?`
    ).bind(...changed.map((c) => clean[c]), author, key).run();
    clean._changed = changed;
  }
  const what = existing
    ? (clean._changed || []).map((c) => `${c} -> ${String(clean[c]).slice(0, 60)}`).join("; ")
    : "created";
  await addEvent(db, {
    author, entity_type: table, entity_key: key,
    kind: existing ? "update" : "create",
    body: why ? `${what} (${why})` : what,
  });
  return { key, changed: existing ? clean._changed : ["*"] };
}

async function addEvent(db, e) {
  await db.prepare(
    `INSERT INTO event (author, entity_type, entity_key, kind, body, ref)
     VALUES (?,?,?,?,?,?)`
  ).bind(e.author || "system", e.entity_type || "", e.entity_key || "",
    e.kind || "note", String(e.body || "").slice(0, 4000), e.ref || "").run();
}

// ---------------------------------------------------------------- cards
// The entity card is what a worker session is seeded with. It is a QUERY, so
// it physically cannot bloat the way a hand-maintained memory file could.
async function leadCard(db, key) {
  const lead = await db.prepare("SELECT * FROM lead WHERE key = ?").bind(key).first();
  if (!lead) return null;
  const [company, contacts, quotes, events, tasks, decisions] = await Promise.all([
    db.prepare("SELECT * FROM company WHERE key = ?").bind(lead.company_key).first(),
    db.prepare("SELECT * FROM contact WHERE company_key = ?").bind(lead.company_key).all(),
    db.prepare("SELECT * FROM quote WHERE lead_key = ? ORDER BY revision DESC").bind(key).all(),
    db.prepare(`SELECT ts, author, kind, body FROM event
                WHERE entity_type = 'lead' AND entity_key = ?
                ORDER BY id DESC LIMIT 30`).bind(key).all(),
    db.prepare(`SELECT id, title, status, created_by FROM task
                WHERE entity_key = ? AND status IN ('open','working')`).bind(key).all(),
    db.prepare(`SELECT id, question, status, answer FROM decision
                WHERE entity_key = ? ORDER BY id DESC LIMIT 8`).bind(key).all(),
  ]);
  return {
    lead, company, contacts: contacts.results, quotes: quotes.results,
    recent_events: events.results, open_tasks: tasks.results, decisions: decisions.results,
  };
}

async function companyCard(db, key) {
  const company = await db.prepare("SELECT * FROM company WHERE key = ?").bind(key).first();
  if (!company) return null;
  const [contacts, leads, contracts, events] = await Promise.all([
    db.prepare("SELECT * FROM contact WHERE company_key = ?").bind(key).all(),
    db.prepare("SELECT * FROM lead WHERE company_key = ? ORDER BY updated DESC").bind(key).all(),
    db.prepare("SELECT * FROM contract WHERE company_key = ?").bind(key).all(),
    db.prepare(`SELECT ts, author, kind, body FROM event
                WHERE entity_type = 'company' AND entity_key = ?
                ORDER BY id DESC LIMIT 30`).bind(key).all(),
  ]);
  return { company, contacts: contacts.results, leads: leads.results,
    contracts: contracts.results, recent_events: events.results };
}

async function contractCard(db, key) {
  const contract = await db.prepare("SELECT * FROM contract WHERE key = ?").bind(key).first();
  if (!contract) return null;
  const [company, steps, invoices, events] = await Promise.all([
    db.prepare("SELECT * FROM company WHERE key = ?").bind(contract.company_key).first(),
    db.prepare("SELECT * FROM step WHERE contract_key = ? ORDER BY n").bind(key).all(),
    db.prepare("SELECT * FROM invoice WHERE contract_key = ?").bind(key).all(),
    db.prepare(`SELECT ts, author, kind, body FROM event
                WHERE entity_type = 'contract' AND entity_key = ?
                ORDER BY id DESC LIMIT 30`).bind(key).all(),
  ]);
  return { contract, company, steps: steps.results, invoices: invoices.results,
    recent_events: events.results };
}

// ---------------------------------------------------------------- handlers
async function handle(request, env, path, url) {
  const db = env.DB;
  const method = request.method;
  const seg = path.split("/").filter(Boolean); // after /api/
  const botKey = request.headers.get("x-glasshouse-key");
  const teamPin = request.headers.get("x-team-pin");
  const isBot = env.GLASSHOUSE_KEY && botKey === env.GLASSHOUSE_KEY;
  const isTeam = env.TEAM_PIN && teamPin === env.TEAM_PIN;
  const body = method === "POST" ? await request.json().catch(() => ({})) : {};

  const needBot = () => { if (!isBot) throw { status: 403, msg: "bot key required" }; };
  const needTeam = () => {
    if (!isTeam && !isBot) throw { status: 403, msg: "PIN required" };
  };

  // ------------------------------------------------ writes: the record
  if (method === "POST" && seg[0] === "upsert") {
    needBot();
    return J(await upsert(db, body.type, body.key, body.fields || {},
      body.author || "bot", body.why || ""));
  }

  if (method === "POST" && seg[0] === "quote") {
    needBot();
    const f = body.fields || {};
    await db.prepare(
      `INSERT INTO quote (lead_key, revision, value, status, issued_at, basis, file_path)
       VALUES (?,?,?,?,?,?,?)
       ON CONFLICT(lead_key, revision) DO UPDATE SET
         value = COALESCE(excluded.value, value),
         status = COALESCE(excluded.status, status),
         issued_at = COALESCE(excluded.issued_at, issued_at),
         basis = COALESCE(NULLIF(excluded.basis,''), basis),
         file_path = COALESCE(NULLIF(excluded.file_path,''), file_path)`
    ).bind(body.lead_key, body.revision || 1, f.value ?? null, f.status ?? null,
      f.issued_at ?? null, f.basis ?? "", f.file_path ?? "").run();
    await addEvent(db, { author: body.author || "bot", entity_type: "lead",
      entity_key: body.lead_key, kind: f.status === "issued" ? "quote_issued" : "quote",
      body: `r${body.revision || 1} ${f.status || ""} ${f.value ? "GBP " + f.value : ""} ${body.why || ""}`.trim() });
    // Quote issued -> the handover Fenster never had, now structural.
    if (f.status === "issued") {
      const lead = await db.prepare("SELECT * FROM lead WHERE key = ?").bind(body.lead_key).first();
      if (lead && lead.owner !== "jacob") {
        await upsert(db, "lead", body.lead_key,
          { stage: "quote_sent", owner: "jacob" }, "system", "quote issued -> chase");
        await db.prepare(
          `INSERT INTO task (assignee, entity_type, entity_key, kind, title, body, created_by)
           VALUES ('jacob','lead',?,'handover',?,?,'system')`
        ).bind(body.lead_key, `Chase: ${lead.title}`,
          `Quote r${body.revision || 1} issued at GBP ${f.value || "?"}. Set the chase dates and own it to closed.`).run();
      }
    }
    return J({ ok: true });
  }

  if (method === "POST" && seg[0] === "contact") {
    needBot();
    await db.prepare(
      `INSERT INTO contact (company_key, name, email, phone, role, notes)
       VALUES (?,?,?,?,?,?)
       ON CONFLICT(company_key, email) DO UPDATE SET
         name = COALESCE(NULLIF(excluded.name,''), name),
         phone = COALESCE(NULLIF(excluded.phone,''), phone),
         role = COALESCE(NULLIF(excluded.role,''), role),
         notes = CASE WHEN excluded.notes != '' THEN notes || char(10) || excluded.notes ELSE notes END`
    ).bind(body.company_key, body.name || "", body.email || "", body.phone || "",
      body.role || "", body.notes || "").run();
    return J({ ok: true });
  }

  // ------------------------------------------------ tasks (the work queue)
  if (method === "POST" && seg[0] === "task" && !seg[1]) {
    needBot();
    const r = await db.prepare(
      `INSERT INTO task (assignee, entity_type, entity_key, kind, title, body,
        payload_json, needs, priority, created_by)
       VALUES (?,?,?,?,?,?,?,?,?,?)`
    ).bind(body.assignee, body.entity_type || "", body.entity_key || "",
      body.kind || "email", body.title || "(untitled)", body.body || "",
      JSON.stringify(body.payload || {}), body.needs || "",
      body.priority || 5, body.created_by || "intake").run();
    return J({ ok: true, id: r.meta.last_row_id });
  }

  if (method === "POST" && seg[0] === "task" && seg[1] === "claim") {
    needBot();
    await db.prepare(
      `UPDATE task SET status = 'working' WHERE id = ? AND status = 'open'`
    ).bind(body.id).run();
    return J({ ok: true });
  }

  if (method === "POST" && seg[0] === "task" && seg[1] === "done") {
    needBot();
    await db.prepare(
      `UPDATE task SET status = ?, done_at = datetime('now'), done_by = ?, result = ?
       WHERE id = ?`
    ).bind(body.status || "done", body.by || "bot",
      String(body.result || "").slice(0, 500), body.id).run();
    const t = await db.prepare("SELECT * FROM task WHERE id = ?").bind(body.id).first();
    if (t) await addEvent(db, { author: body.by || "bot", entity_type: t.entity_type,
      entity_key: t.entity_key, kind: "task_done",
      body: `${t.title}: ${body.result || "done"}`, ref: "task:" + body.id });
    return J({ ok: true });
  }

  if (method === "POST" && seg[0] === "task" && seg[1] === "release") {
    needBot(); // a crashed worker's tasks go back in the queue
    await db.prepare(
      `UPDATE task SET status = 'open' WHERE status = 'working' AND assignee = ?`
    ).bind(body.assignee).run();
    return J({ ok: true });
  }

  if (method === "GET" && seg[0] === "tasks") {
    const q = url.searchParams;
    const rows = await db.prepare(
      `SELECT * FROM task WHERE status = ?1 AND (?2 = '' OR assignee = ?2)
       ORDER BY priority, id LIMIT 200`
    ).bind(q.get("status") || "open", q.get("assignee") || "").all();
    return J(rows.results);
  }

  // ------------------------------------------------ events / notes / usage
  if (method === "POST" && seg[0] === "event") {
    needBot();
    await addEvent(db, body);
    return J({ ok: true });
  }
  if (method === "POST" && seg[0] === "events") {
    needBot();
    for (const e of body.events || []) await addEvent(db, e);
    return J({ ok: true, n: (body.events || []).length });
  }
  if (method === "POST" && seg[0] === "usage") {
    needBot();
    await db.prepare(
      `INSERT INTO usage (persona, entity_key, session_id, model, calls,
        context_tokens, output_tokens, seconds) VALUES (?,?,?,?,?,?,?,?)`
    ).bind(body.persona, body.entity_key || "", body.session_id || "",
      body.model || "", body.calls || 0, body.context_tokens || 0,
      body.output_tokens || 0, body.seconds || 0).run();
    return J({ ok: true });
  }
  if (method === "POST" && seg[0] === "noise") {
    needBot();
    await db.prepare("INSERT INTO noise (sender, subject, why) VALUES (?,?,?)")
      .bind(body.sender || "", body.subject || "", body.why || "").run();
    return J({ ok: true });
  }
  if (method === "POST" && seg[0] === "status") {
    needBot();
    await db.prepare(
      `INSERT INTO setting (key, value) VALUES (?1, ?2)
       ON CONFLICT(key) DO UPDATE SET value = ?2`
    ).bind("status:" + body.persona, JSON.stringify({
      state: body.state, detail: body.detail || "", at: now() })).run();
    return J({ ok: true });
  }

  // ------------------------------------------------ steps & invoices
  if (method === "POST" && seg[0] === "step") {
    needBot();
    if (seg[1] === "done") {
      await db.prepare(
        `UPDATE step SET done_at = datetime('now'), done_by = ?
         WHERE contract_key = ? AND n = ? AND done_at IS NULL`
      ).bind(body.by || "bot", body.contract_key, body.n).run();
      await addEvent(db, { author: body.by || "bot", entity_type: "contract",
        entity_key: body.contract_key, kind: "step_done",
        body: `step ${body.n} done${body.why ? ": " + body.why : ""}` });
    } else {
      await db.prepare(
        `INSERT INTO step (contract_key, n, label, detail, due) VALUES (?,?,?,?,?)
         ON CONFLICT(contract_key, n) DO UPDATE SET
           label = excluded.label,
           detail = COALESCE(NULLIF(excluded.detail,''), detail),
           due = COALESCE(excluded.due, due)`
      ).bind(body.contract_key, body.n, body.label, body.detail || "", body.due ?? null).run();
    }
    return J({ ok: true });
  }
  if (method === "POST" && seg[0] === "invoice") {
    needBot();
    await db.prepare(
      `INSERT INTO invoice (contract_key, ref, value, due, status) VALUES (?,?,?,?,?)`
    ).bind(body.contract_key, body.ref || "", body.value ?? null,
      body.due ?? null, body.status || "draft").run();
    return J({ ok: true });
  }

  // ------------------------------------------------ decisions & messages
  if (method === "POST" && seg[0] === "decision" && !seg[1]) {
    needBot();
    const r = await db.prepare(
      `INSERT INTO decision (raised_by, entity_type, entity_key, question, context)
       VALUES (?,?,?,?,?)`
    ).bind(body.raised_by, body.entity_type || "", body.entity_key || "",
      body.question, body.context || "").run();
    return J({ ok: true, id: r.meta.last_row_id });
  }
  if (method === "POST" && seg[0] === "decision" && seg[1] === "answer") {
    needTeam();
    await db.prepare(
      `UPDATE decision SET status = 'answered', answer = ?, answered_by = ?,
       answered_at = datetime('now') WHERE id = ?`
    ).bind(body.answer, body.by || "team", body.id).run();
    const d = await db.prepare("SELECT * FROM decision WHERE id = ?").bind(body.id).first();
    if (d) {
      // The answer becomes a task for whoever asked - nothing sits unseen.
      await db.prepare(
        `INSERT INTO task (assignee, entity_type, entity_key, kind, title, body,
          priority, created_by)
         VALUES (?,?,?,?,?,?,2,?)`
      ).bind(d.raised_by, d.entity_type, d.entity_key, "hub",
        `Answered: ${d.question.slice(0, 120)}`,
        `${body.by || "team"} answered: ${body.answer}`, body.by || "team").run();
      await addEvent(db, { author: body.by || "team", entity_type: d.entity_type,
        entity_key: d.entity_key, kind: "decision",
        body: `Q: ${d.question.slice(0, 150)} -> A: ${String(body.answer).slice(0, 300)}` });
    }
    return J({ ok: true });
  }

  if (method === "POST" && seg[0] === "message") {
    // Bots post replies with the key; humans post instructions with the PIN.
    if (!isBot) needTeam();
    const author = isBot ? (body.author || "bot") : (body.author || "team");
    const r = await db.prepare(
      `INSERT INTO message (author, persona, body, reply_to) VALUES (?,?,?,?)`
    ).bind(author, body.persona, String(body.body || "").slice(0, 8000),
      body.reply_to ?? null).run();
    if (!isBot) {
      // A human instruction becomes an urgent task for that persona.
      await db.prepare(
        `INSERT INTO task (assignee, kind, title, body, priority, created_by, payload_json)
         VALUES (?,?,?,?,1,?,?)`
      ).bind(body.persona, "hub", `${author}: ${String(body.body).slice(0, 100)}`,
        String(body.body).slice(0, 4000), author,
        JSON.stringify({ message_id: r.meta.last_row_id })).run();
    }
    return J({ ok: true, id: r.meta.last_row_id });
  }
  if (method === "POST" && seg[0] === "outcome") {
    needTeam(); // the one-click habit: won or lost, from the hub
    await upsert(db, "lead", body.lead_key,
      { stage: "closed", outcome: body.outcome, outcome_why: body.why || "" },
      body.by || "team", "outcome recorded on the hub");
    return J({ ok: true });
  }

  // ------------------------------------------------ drafts
  // A bot writes one; a human sends it and says so. Until somebody acts, it
  // sits in front of them - which is the whole point.
  if (method === "POST" && seg[0] === "draft" && !seg[1]) {
    needBot();
    const r = await db.prepare(
      `INSERT INTO draft (author, kind, to_whom, subject, body, entity_type, entity_key)
       VALUES (?,?,?,?,?,?,?)`
    ).bind(body.author, body.kind || "email", body.to || "", body.subject || "",
      String(body.body || "").slice(0, 12000), body.entity_type || "",
      body.entity_key || "").run();
    await addEvent(db, { author: body.author, entity_type: body.entity_type,
      entity_key: body.entity_key, kind: "draft",
      body: `drafted for ${body.to || "someone"}: ${(body.subject || "").slice(0, 120)}` });
    return J({ ok: true, id: r.meta.last_row_id });
  }
  if (method === "POST" && seg[0] === "draft" && seg[1] === "status") {
    needTeam();
    await db.prepare(
      `UPDATE draft SET status = ?, acted_at = datetime('now'), acted_by = ? WHERE id = ?`
    ).bind(body.status, body.by || "team", body.id).run();
    const d = await db.prepare("SELECT * FROM draft WHERE id = ?").bind(body.id).first();
    if (d) {
      await addEvent(db, { author: body.by || "team", entity_type: d.entity_type,
        entity_key: d.entity_key, kind: "draft_" + body.status,
        body: `${body.status}: ${(d.subject || d.body).slice(0, 120)}` });
      // The author learns what happened to its recommendation.
      await db.prepare(
        `INSERT INTO task (assignee, entity_type, entity_key, kind, title, body,
          priority, created_by) VALUES (?,?,?,'hub',?,?,4,?)`
      ).bind(d.author, d.entity_type, d.entity_key,
        `Draft ${body.status}: ${(d.subject || "").slice(0, 90)}`,
        `${body.by || "team"} marked your draft ${body.status}.` +
        (body.note ? " Note: " + body.note : ""), body.by || "team").run();
    }
    return J({ ok: true });
  }
  if (method === "GET" && seg[0] === "drafts") {
    const q = url.searchParams;
    const rows = await db.prepare(
      `SELECT * FROM draft WHERE status = ?1 AND (?2 = '' OR author = ?2)
       ORDER BY id DESC LIMIT 50`
    ).bind(q.get("status") || "waiting", q.get("author") || "").all();
    return J(rows.results);
  }

  // ------------------------------------------------ THE DESK
  // One call returns everything a persona's page needs. A page that takes six
  // round trips is a page that renders in pieces.
  if (method === "GET" && seg[0] === "desk" && seg[1]) {
    const who = seg[1];
    if (!PERSONAS.includes(who)) return J({ error: "no such desk" }, 404);
    const today = new Date().toISOString().slice(0, 10);
    const week = new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10);

    const [tasks, decisions, drafts, messages, events, session, costRow, status] =
      await Promise.all([
        db.prepare(`SELECT * FROM task WHERE assignee = ? AND status IN ('open','working')
                    ORDER BY priority, id`).bind(who).all(),
        db.prepare(`SELECT * FROM decision WHERE raised_by = ?
                    ORDER BY status = 'open' DESC, id DESC LIMIT 20`).bind(who).all(),
        db.prepare(`SELECT * FROM draft WHERE author = ? AND status = 'waiting'
                    ORDER BY id DESC`).bind(who).all(),
        db.prepare(`SELECT * FROM message WHERE persona = ? ORDER BY id DESC LIMIT 60`)
          .bind(who).all(),
        db.prepare(`SELECT * FROM event WHERE author = ? ORDER BY id DESC LIMIT 40`)
          .bind(who).all(),
        db.prepare(`SELECT * FROM usage WHERE persona = ? ORDER BY id DESC LIMIT 1`)
          .bind(who).first(),
        db.prepare(`SELECT SUM(context_tokens) c, COUNT(*) n FROM usage
                    WHERE persona = ? AND ts >= ?`).bind(who, today + " 00:00:00").first(),
        db.prepare(`SELECT value FROM setting WHERE key = ?`).bind("status:" + who).first(),
      ]);

    const out = {
      persona: who,
      status: JSON.parse((status || {}).value || "{}"),
      tasks: tasks.results, decisions: decisions.results, drafts: drafts.results,
      messages: messages.results, events: events.results,
      last_session: session || null, cost_today: costRow || {},
    };

    if (who === "mary") {
      // Her board is the estimating half of the pipeline, plus the two things
      // a human has to act on: quotes to check, and errors she has caught.
      const [board, ready, catches] = await Promise.all([
        db.prepare(`SELECT l.*, c.name company_name FROM lead l
                    LEFT JOIN company c ON c.key = l.company_key
                    WHERE l.stage IN ('new','acknowledged','materials_out',
                      'awaiting_costs','quote_ready','pre_quote_call')
                    ORDER BY (l.deadline IS NULL OR l.deadline = ''), l.deadline,
                      l.updated DESC`).all(),
        db.prepare(`SELECT q.*, l.title, l.company_key FROM quote q
                    JOIN lead l ON l.key = q.lead_key
                    WHERE q.status IN ('draft','checked') AND l.stage != 'closed'
                    ORDER BY q.id DESC LIMIT 20`).all(),
        db.prepare(`SELECT * FROM event WHERE kind = 'catch' ORDER BY id DESC LIMIT 15`).all(),
      ]);
      out.board = board.results;
      out.ready_to_check = ready.results;
      out.catches = catches.results;
      out.no_deadline = board.results.filter((l) => !l.deadline).length;
    }

    if (who === "jacob") {
      const [calls, outFor, companies, scoreboard, quiet] = await Promise.all([
        db.prepare(`SELECT l.*, c.name company_name FROM lead l
                    LEFT JOIN company c ON c.key = l.company_key
                    WHERE l.stage != 'closed' AND COALESCE(l.next_action_date,'') != ''
                      AND l.next_action_date <= ? ORDER BY l.next_action_date`)
          .bind(today).all(),
        db.prepare(`SELECT l.*, c.name company_name,
                      (SELECT MAX(issued_at) FROM quote WHERE lead_key = l.key
                        AND status = 'issued') issued_at
                    FROM lead l LEFT JOIN company c ON c.key = l.company_key
                    WHERE l.stage IN ('quote_sent','follow_up','final_follow_up')
                    ORDER BY COALESCE(l.value,0) DESC`).all(),
        db.prepare(`SELECT key, name, relationship, lifetime_value,
                      (SELECT COUNT(*) FROM lead WHERE company_key = company.key
                        AND stage != 'closed') open_leads
                    FROM company ORDER BY COALESCE(lifetime_value,0) DESC`).all(),
        db.prepare(`SELECT outcome, COUNT(*) n, CAST(SUM(COALESCE(value,0)) AS INT) v
                    FROM lead WHERE stage = 'closed' AND COALESCE(outcome,'') != ''
                    GROUP BY outcome`).all(),
        db.prepare(`SELECT l.*, c.name company_name FROM lead l
                    LEFT JOIN company c ON c.key = l.company_key
                    WHERE l.stage != 'closed' AND COALESCE(l.next_action_date,'') = ''
                      AND l.stage IN ('quote_sent','follow_up','final_follow_up')`).all(),
      ]);
      out.calls_today = calls.results;
      out.out_for_decision = outFor.results;
      out.companies = companies.results;
      out.scoreboard = scoreboard.results;
      out.no_chase_date = quiet.results;
    }

    if (who === "joseph") {
      const [contracts, steps, invoices] = await Promise.all([
        db.prepare(`SELECT ct.*, c.name company_name,
                      (SELECT COUNT(*) FROM step WHERE contract_key = ct.key) steps_total,
                      (SELECT COUNT(*) FROM step WHERE contract_key = ct.key
                        AND done_at IS NULL) steps_open
                    FROM contract ct LEFT JOIN company c ON c.key = ct.company_key
                    ORDER BY ct.status = 'live' DESC,
                      (ct.site_date IS NULL OR ct.site_date = ''), ct.site_date`).all(),
        db.prepare(`SELECT s.*, ct.title contract_title FROM step s
                    JOIN contract ct ON ct.key = s.contract_key
                    WHERE s.done_at IS NULL AND ct.status = 'live'
                    ORDER BY (s.due IS NULL OR s.due = ''), s.due LIMIT 30`).all(),
        db.prepare(`SELECT i.*, ct.title contract_title FROM invoice i
                    JOIN contract ct ON ct.key = i.contract_key
                    ORDER BY i.status = 'paid', i.due`).all(),
      ]);
      out.contracts = contracts.results;
      out.steps_due = steps.results;
      out.invoices = invoices.results;
      out.week = week;
    }
    return J(out);
  }

  // ------------------------------------------------ reads
  if (method === "GET" && seg[0] === "card") {
    const card = seg[1] === "lead" ? await leadCard(db, seg[2])
      : seg[1] === "company" ? await companyCard(db, seg[2])
      : seg[1] === "contract" ? await contractCard(db, seg[2]) : null;
    return card ? J(card) : J({ error: "not found" }, 404);
  }

  if (method === "GET" && seg[0] === "today") {
    const today = new Date().toISOString().slice(0, 10);
    const week = new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10);
    const [due, overdue, upcoming, deadlines] = await Promise.all([
      db.prepare(`SELECT * FROM lead WHERE stage != 'closed' AND next_action_date = ?`)
        .bind(today).all(),
      db.prepare(`SELECT * FROM lead WHERE stage != 'closed' AND next_action_date < ?
                  ORDER BY value DESC LIMIT 20`).bind(today).all(),
      db.prepare(`SELECT * FROM lead WHERE stage != 'closed' AND next_action_date > ?1
                  AND next_action_date <= ?2 ORDER BY next_action_date`)
        .bind(today, week).all(),
      db.prepare(`SELECT * FROM lead WHERE stage != 'closed' AND deadline >= ?1
                  AND deadline <= ?2 ORDER BY deadline`).bind(today, week).all(),
    ]);
    return J({ date: today, due: due.results, overdue: overdue.results,
      upcoming: upcoming.results, deadlines: deadlines.results });
  }

  if (method === "GET" && seg[0] === "overview") {
    const today = new Date().toISOString().slice(0, 10);
    const [deskEvents, lastSessions, workingTasks] = await Promise.all([
      db.prepare(`SELECT author, ts, kind, entity_key, body FROM event
                  WHERE author IN ('mary','jacob','joseph')
                  ORDER BY id DESC LIMIT 30`).all(),
      db.prepare(`SELECT * FROM usage WHERE id IN
                  (SELECT MAX(id) FROM usage GROUP BY persona)`).all(),
      db.prepare(`SELECT assignee, title FROM task WHERE status = 'working'`).all(),
    ]);
    const [decisions, tasks, leads, contracts, messages, statuses, cost] = await Promise.all([
      db.prepare(`SELECT * FROM decision WHERE status = 'open' ORDER BY id DESC`).all(),
      db.prepare(`SELECT assignee, status, COUNT(*) n FROM task
                  WHERE status IN ('open','working') GROUP BY assignee, status`).all(),
      db.prepare(`SELECT stage, COUNT(*) n, SUM(COALESCE(value,0)) v FROM lead
                  WHERE stage != 'closed' GROUP BY stage`).all(),
      db.prepare(`SELECT COUNT(*) n FROM contract WHERE status = 'live'`).first(),
      db.prepare(`SELECT * FROM message ORDER BY id DESC LIMIT 12`).all(),
      db.prepare(`SELECT key, value FROM setting WHERE key LIKE 'status:%'`).all(),
      db.prepare(`SELECT SUM(context_tokens) c, COUNT(*) n FROM usage
                  WHERE ts >= ?`).bind(today + " 00:00:00").first(),
    ]);
    return J({
      decisions: decisions.results, task_counts: tasks.results,
      pipeline: leads.results, live_contracts: contracts ? contracts.n : 0,
      messages: messages.results,
      statuses: Object.fromEntries(statuses.results.map((s) =>
        [s.key.slice(7), JSON.parse(s.value || "{}")])),
      cost_today: cost || {},
      desk_events: deskEvents.results,
      last_sessions: lastSessions.results,
      working: workingTasks.results,
    });
  }

  if (method === "GET" && seg[0] === "pipeline") {
    const rows = await db.prepare(
      `SELECT l.*, c.name company_name FROM lead l
       LEFT JOIN company c ON c.key = l.company_key
       WHERE l.stage != 'closed' ORDER BY l.updated DESC`).all();
    const closed = await db.prepare(
      `SELECT l.*, c.name company_name FROM lead l
       LEFT JOIN company c ON c.key = l.company_key
       WHERE l.stage = 'closed' ORDER BY l.updated DESC LIMIT 30`).all();
    return J({ open: rows.results, closed: closed.results, stages: STAGES });
  }

  if (method === "GET" && seg[0] === "companies") {
    const rows = await db.prepare(
      `SELECT c.*,
        (SELECT COUNT(*) FROM lead WHERE company_key = c.key AND stage != 'closed') open_leads
       FROM company c ORDER BY COALESCE(c.lifetime_value,0) DESC, c.name`).all();
    return J(rows.results);
  }

  if (method === "GET" && seg[0] === "contracts") {
    const rows = await db.prepare(
      `SELECT ct.*, c.name company_name,
        (SELECT COUNT(*) FROM step WHERE contract_key = ct.key AND done_at IS NULL) steps_open,
        (SELECT COUNT(*) FROM step WHERE contract_key = ct.key) steps_total
       FROM contract ct LEFT JOIN company c ON c.key = ct.company_key
       ORDER BY ct.status = 'live' DESC, ct.site_date`).all();
    return J(rows.results);
  }

  if (method === "GET" && seg[0] === "feed") {
    const q = url.searchParams;
    const rows = await db.prepare(
      `SELECT * FROM event WHERE (?1 = '' OR entity_key = ?1)
       ORDER BY id DESC LIMIT ?2`
    ).bind(q.get("entity") || "", Number(q.get("limit") || 100)).all();
    return J(rows.results);
  }

  if (method === "GET" && seg[0] === "messages") {
    const q = url.searchParams;
    const rows = await db.prepare(
      `SELECT * FROM message WHERE (?1 = '' OR persona = ?1) ORDER BY id DESC LIMIT 100`
    ).bind(q.get("persona") || "").all();
    return J(rows.results);
  }

  if (method === "GET" && seg[0] === "decisions") {
    const rows = await db.prepare(
      `SELECT * FROM decision ORDER BY status = 'open' DESC, id DESC LIMIT 100`).all();
    return J(rows.results);
  }

  if (method === "GET" && seg[0] === "cost") {
    const rows = await db.prepare(
      `SELECT date(ts) day, persona, SUM(context_tokens) context,
        SUM(output_tokens) output, SUM(calls) calls, COUNT(*) sessions
       FROM usage WHERE ts >= date('now', '-14 days')
       GROUP BY day, persona ORDER BY day DESC`).all();
    const recent = await db.prepare(
      `SELECT * FROM usage ORDER BY id DESC LIMIT 40`).all();
    return J({ days: rows.results, recent: recent.results });
  }

  if (method === "GET" && seg[0] === "noise") {
    const rows = await db.prepare(
      `SELECT * FROM noise ORDER BY id DESC LIMIT 100`).all();
    return J(rows.results);
  }

  return J({ error: "no such route: " + method + " /api/" + seg.join("/") }, 404);
}

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const path = url.pathname.replace(/^\/api\//, "");
  if (request.method === "OPTIONS")
    return new Response(null, { headers: {
      "access-control-allow-origin": "*",
      "access-control-allow-headers": "content-type,x-glasshouse-key,x-team-pin",
      "access-control-allow-methods": "GET,POST,OPTIONS" } });
  try {
    return await handle(request, env, path, url);
  } catch (e) {
    if (e && e.status) return J({ error: e.msg }, e.status);
    return J({ error: String(e && e.message || e).slice(0, 300) }, 500);
  }
}
