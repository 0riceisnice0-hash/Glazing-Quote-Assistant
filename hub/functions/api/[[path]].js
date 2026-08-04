// GLASSHOUSE API - every route in one router over the record.
//
// Three tiers of caller:
//   bots    write with  x-glasshouse-key == env.GLASSHOUSE_KEY
//   humans  write with  x-team-pin       == env.TEAM_PIN   (the sender check)
//   anyone  reads       GETs are open, same standing as the old hub (auth off
//                       by Zac's call; PIN guards every write that steers a bot)
//
// Values are ex VAT everywhere. Every write lands an event with an author.

import { hashPassword, randomSalt, randomCode, same, mintToken, readToken }
  from "../_auth.js";

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
  const isBot = env.GLASSHOUSE_KEY && botKey === env.GLASSHOUSE_KEY;
  const body = method === "POST" ? await request.json().catch(() => ({})) : {};
  const secret = env.SESSION_SECRET || env.GLASSHOUSE_KEY || "unset";

  // Who is asking? A bot with the shared key, or a person with a session.
  const session = isBot ? null
    : await readToken(secret, (request.headers.get("authorization") || "")
        .replace(/^Bearer\s+/i, ""));
  const role = isBot ? "bot" : (session && session.role) || null;
  const meName = isBot ? "bot" : (session && session.name) || null;

  const needBot = () => { if (!isBot) throw { status: 403, msg: "bot key required" }; };
  // An admin session or a bot may steer the bots. Delivery may not.
  const needTeam = () => {
    if (!isBot && role !== "admin") throw { status: 401, msg: "sign in as an admin" };
  };
  const needAnyUser = () => {
    if (!isBot && !role) throw { status: 401, msg: "sign in" };
  };

  // ------------------------------------------------ sign in / accounts
  if (method === "POST" && seg[0] === "login") {
    const u = await db.prepare(
      "SELECT * FROM user WHERE name = ? AND active = 1"
    ).bind(String(body.name || "").toLowerCase().trim()).first();
    // A missing account and a wrong password answer identically, so the form
    // cannot be used to find out who works here.
    if (!u || !u.pass_hash) return J({ error: "wrong name or password" }, 401);
    const h = await hashPassword(String(body.password || ""), u.pass_salt);
    if (!same(h, u.pass_hash)) return J({ error: "wrong name or password" }, 401);
    await db.prepare("UPDATE user SET last_login = datetime('now') WHERE id = ?")
      .bind(u.id).run();
    return J({ token: await mintToken(secret, { name: u.name, role: u.role, display: u.display }),
      name: u.name, display: u.display, role: u.role });
  }

  // First time in: the person enters the one-time code and chooses a password.
  // The server never receives a password anyone else has seen.
  if (method === "POST" && seg[0] === "setup") {
    const u = await db.prepare(
      "SELECT * FROM user WHERE name = ? AND active = 1"
    ).bind(String(body.name || "").toLowerCase().trim()).first();
    if (!u || !u.setup_code || !same(u.setup_code, String(body.code || "")))
      return J({ error: "that setup code is not right" }, 401);
    const pw = String(body.password || "");
    if (pw.length < 8) return J({ error: "choose at least 8 characters" }, 400);
    const salt = randomSalt();
    await db.prepare(
      "UPDATE user SET pass_hash = ?, pass_salt = ?, setup_code = '' WHERE id = ?"
    ).bind(await hashPassword(pw, salt), salt, u.id).run();
    await addEvent(db, { author: u.name, kind: "account",
      body: `${u.display} set their password and can now sign in` });
    return J({ token: await mintToken(secret, { name: u.name, role: u.role, display: u.display }),
      name: u.name, display: u.display, role: u.role });
  }

  if (method === "GET" && seg[0] === "me") {
    if (!role) return J({ error: "not signed in" }, 401);
    return J({ name: meName, role, display: (session && session.display) || "bot" });
  }

  if (method === "POST" && seg[0] === "users" && seg[1] === "add") {
    needTeam();
    const code = randomCode();
    const name = String(body.name || "").toLowerCase().trim();
    if (!name) return J({ error: "a login name is required" }, 400);
    await db.prepare(
      `INSERT INTO user (name, display, role, setup_code) VALUES (?,?,?,?)
       ON CONFLICT(name) DO UPDATE SET display = excluded.display,
         role = excluded.role, setup_code = excluded.setup_code, active = 1`
    ).bind(name, body.display || name, body.role === "admin" ? "admin" : "delivery", code).run();
    // The code is returned ONCE, to the admin who created the account, to hand
    // over however they like. It is not emailed and not stored in plain sight.
    return J({ ok: true, name, setup_code: code });
  }

  if (method === "GET" && seg[0] === "users") {
    needTeam();
    const rows = await db.prepare(
      `SELECT id, name, display, role, active, created, last_login,
        (pass_hash != '') AS ready FROM user ORDER BY role, name`).all();
    return J(rows.results);
  }

  // ------------------------------------------------ THE GATE
  // Past this line you are a bot, an admin, or delivery. Delivery sees its own
  // day and can tick its own steps; it never sees pricing, decisions, drafts,
  // the bots' conversations or the cost meter.
  needAnyUser();
  const DELIVERY_OK = new Set(["delivery", "card", "step", "me"]);
  if (role === "delivery" && !DELIVERY_OK.has(seg[0]))
    throw { status: 403, msg: "not your side of the hub" };

  // ------------------------------------------------ DELIVERY: Paul and Steve
  // "These are your daily tasks. This glass needs to be ordered by this date.
  //  These are your deadlines." - Adam, 03/08. Deadlines at the top, the spec
  //  attached, and nothing to think about.
  if (method === "GET" && seg[0] === "delivery") {
    const today = new Date().toISOString().slice(0, 10);
    const week = new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10);
    const [steps, contracts] = await Promise.all([
      db.prepare(
        `SELECT s.*, ct.title contract_title, ct.site_date, ct.key contract_key,
           c.name company_name
         FROM step s JOIN contract ct ON ct.key = s.contract_key
         LEFT JOIN company c ON c.key = ct.company_key
         WHERE s.done_at IS NULL AND ct.status = 'live'
         ORDER BY (s.due IS NULL OR s.due = ''), s.due, s.n`).all(),
      db.prepare(
        `SELECT ct.*, c.name company_name FROM contract ct
         LEFT JOIN company c ON c.key = ct.company_key
         WHERE ct.status = 'live'
         ORDER BY (ct.site_date IS NULL OR ct.site_date = ''), ct.site_date`).all(),
    ]);
    const all = steps.results;
    return J({
      date: today,
      late: all.filter((s) => s.due && s.due < today),
      todays: all.filter((s) => s.due === today),
      week: all.filter((s) => s.due && s.due > today && s.due <= week),
      undated: all.filter((s) => !s.due),
      contracts: contracts.results,
      site_this_week: contracts.results.filter(
        (c) => c.site_date && c.site_date >= today && c.site_date <= week),
    });
  }

  // ------------------------------------------------ RFQs: who owes us a price
  if (method === "POST" && seg[0] === "rfq") {
    needTeam();
    if (seg[1] === "received") {
      await db.prepare(
        `UPDATE rfq SET received_at = COALESCE(?, datetime('now')), value = ?, notes = ?
         WHERE id = ?`
      ).bind(body.received_at || null, body.value ?? null, body.notes || "", body.id).run();
    } else {
      await db.prepare(
        `INSERT INTO rfq (lead_key, supplier, scope, sent_at, value, notes)
         VALUES (?,?,?,?,?,?)
         ON CONFLICT(lead_key, supplier) DO UPDATE SET
           scope = COALESCE(NULLIF(excluded.scope,''), scope),
           sent_at = COALESCE(excluded.sent_at, sent_at)`
      ).bind(body.lead_key, body.supplier, body.scope || "",
        body.sent_at || new Date().toISOString().slice(0, 10), null, "").run();
    }
    return J({ ok: true });
  }
  if (method === "GET" && seg[0] === "rfqs") {
    const rows = await db.prepare(
      `SELECT r.*, l.title lead_title FROM rfq r JOIN lead l ON l.key = r.lead_key
       WHERE l.stage != 'closed' ORDER BY r.received_at IS NOT NULL, r.sent_at`).all();
    return J(rows.results);
  }

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
    // Ticking a step is the one write a fitter can make, and it is signed with
    // their name - "who said the glass was ordered" has an answer now.
    if (seg[1] !== "done") needBot();
    if (seg[1] === "done") {
      const by = isBot ? (body.by || "bot") : meName;
      await db.prepare(
        `UPDATE step SET done_at = datetime('now'), done_by = ?
         WHERE contract_key = ? AND n = ? AND done_at IS NULL`
      ).bind(by, body.contract_key, body.n).run();
      await addEvent(db, { author: by, entity_type: "contract",
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
  // Money is never autonomous. An invoice is RAISED as a draft, a human checks
  // it, and only then does it go anywhere. Adam: "invoices to check ... is this
  // correct, basically, yes."
  if (method === "POST" && seg[0] === "invoice" && !seg[1]) {
    needBot();
    const ct = await db.prepare("SELECT * FROM contract WHERE key = ?")
      .bind(body.contract_key).first();
    const co = ct ? await db.prepare("SELECT * FROM company WHERE key = ?")
      .bind(ct.company_key).first() : null;
    // Due date from the client's own terms, learned per company. "Immediate"
    // gets 30 days in practice - Adam, 03/08.
    let due = body.due || null;
    if (!due) {
      const terms = String((co && co.payment_terms) || "").toLowerCase();
      const m = terms.match(/(\d+)/);
      const days = m ? parseInt(m[1], 10) : 30;
      const base = new Date();
      let d = new Date(base.getTime() + days * 864e5);
      if (terms.includes("end of month")) d = new Date(d.getFullYear(), d.getMonth() + 1, 0);
      due = d.toISOString().slice(0, 10);
    }
    const r = await db.prepare(
      `INSERT INTO invoice (contract_key, ref, value, due, status) VALUES (?,?,?,?,'draft')`
    ).bind(body.contract_key, body.ref || "", body.value ?? (ct ? ct.value : null), due).run();
    await addEvent(db, { author: body.author || "joseph", entity_type: "contract",
      entity_key: body.contract_key, kind: "invoice_raised",
      body: `invoice raised for checking: ${body.value ?? (ct && ct.value)} due ${due}` });
    await db.prepare(
      `INSERT INTO decision (raised_by, entity_type, entity_key, question, context)
       VALUES (?,?,?,?,?)`
    ).bind(body.author || "joseph", "contract", body.contract_key,
      `Invoice to check: ${ct ? ct.title : body.contract_key}`,
      `${body.value ?? (ct && ct.value) ?? "?"} ex VAT, due ${due}` +
      (co && co.payment_terms ? ` on ${co.payment_terms} terms` : " on default 30-day terms") +
      `. ${body.basis || "Figure taken from the contract value - confirm it against the final account before this goes."}`).run();
    return J({ ok: true, id: r.meta.last_row_id, due });
  }
  if (method === "POST" && seg[0] === "invoice" && seg[1] === "status") {
    needTeam();
    await db.prepare("UPDATE invoice SET status = ?, paid_at = ? WHERE id = ?")
      .bind(body.status, body.status === "paid" ? new Date().toISOString().slice(0, 10) : null,
        body.id).run();
    const inv = await db.prepare("SELECT * FROM invoice WHERE id = ?").bind(body.id).first();
    if (inv) await addEvent(db, { author: meName || "team", entity_type: "contract",
      entity_key: inv.contract_key, kind: "invoice_" + body.status,
      body: `invoice ${inv.ref || inv.id} marked ${body.status}` });
    return J({ ok: true });
  }

  // A new enquiry becomes a lead. Jacob's job - "we effectively need Jacob to
  // be logging it as a lead himself" - and a button for a human until he runs.
  if (method === "POST" && seg[0] === "lead" && seg[1] === "log") {
    needTeam();
    const key = String(body.key || "").toLowerCase().replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "").slice(0, 60);
    if (!key) return J({ error: "a key is required" }, 400);
    await upsert(db, "lead", key, {
      title: body.title || key, company_key: body.company_key || "unknown",
      stage: "new", owner: "mary", value: body.value ?? null,
      deadline: body.deadline || null, next_action: body.next_action || null,
      next_action_date: body.next_action_date || null,
    }, meName || "team", body.why || "logged as a lead from an enquiry");
    if (body.task_id) {
      await db.prepare(
        `UPDATE task SET entity_type = 'lead', entity_key = ? WHERE id = ?`
      ).bind(key, body.task_id).run();
    }
    return J({ ok: true, key });
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
      // "This is when our client is finding out if THEY have won the work.
      //  This will go red when it's time for us to call." - Adam, 03/08
      const award = await db.prepare(
        `SELECT l.*, c.name company_name FROM lead l
         LEFT JOIN company c ON c.key = l.company_key
         WHERE l.stage != 'closed' AND COALESCE(l.award_due,'') != ''
         ORDER BY l.award_due`).all();
      out.award_dates = award.results;
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
