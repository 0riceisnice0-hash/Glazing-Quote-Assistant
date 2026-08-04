/* GLASSHOUSE — the app. Vanilla JS, no build step.

   ARCHITECTURE: one page per DESK, not per entity type. Every question a
   human actually asks here is a question about a person's job -
   "what is Mary doing", "what does Jacob need from me", "is Joseph's job
   going to be late". A Companies tab answers none of those, so companies
   live inside Jacob's page, contracts inside Joseph's, and the pricing
   board inside Mary's, each with the context that makes it useful.

   Reads are open. Every write that steers a bot asks for the team PIN once
   and keeps it locally — that is the sender check. */

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const view = $("#view");

const PEOPLE = {
  mary:   { name: "Mary Grace",   role: "Estimating",          job: "Prices tenders, audits quotes, catches errors" },
  jacob:  { name: "Jacob Wright", role: "Business development", job: "Owns the lead, chases the quote, records the outcome" },
  joseph: { name: "Joseph Scott", role: "Project management",   job: "Runs the won contract from PO to final payment" },
};
const STAGE_LABEL = {
  new: "New", acknowledged: "Acknowledged", materials_out: "Materials out",
  awaiting_costs: "Awaiting costs", quote_ready: "Quote ready",
  pre_quote_call: "Pre-quote call", quote_sent: "Quote sent",
  follow_up: "Follow-up", final_follow_up: "Final follow-up", closed: "Closed",
};

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const gbp = (v) => v == null || v === "" ? "" :
  "£" + Number(v).toLocaleString("en-GB", { maximumFractionDigits: 0 });
const fmtTok = (n) => !n ? "0" : n >= 1e6 ? (n / 1e6).toFixed(1) + "M"
  : n >= 1e3 ? Math.round(n / 1e3) + "k" : String(n);
const today = () => new Date().toISOString().slice(0, 10);
const dayn = (d) => d ? Math.floor((Date.now() - new Date(d + (d.length < 11 ? "T12:00:00Z" : "")).getTime()) / 864e5) : null;
const rel = (ts) => {
  if (!ts) return "";
  const d = (Date.now() - new Date(ts.replace(" ", "T") + "Z").getTime()) / 1000;
  if (d < 90) return "just now";
  if (d < 5400) return Math.round(d / 60) + "m ago";
  if (d < 129600) return Math.round(d / 3600) + "h ago";
  return Math.round(d / 86400) + "d ago";
};

async function api(path) {
  const r = await fetch("/api" + path);
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).error || r.status);
  return r.json();
}
async function post(path, body) {
  const pin = localStorage.pin || await askPin();
  const r = await fetch("/api" + path, {
    method: "POST",
    headers: { "content-type": "application/json", "x-team-pin": pin },
    body: JSON.stringify(body),
  });
  if (r.status === 403) { delete localStorage.pin; toast("Wrong PIN"); throw new Error("pin"); }
  if (!r.ok) { toast("That did not save"); throw new Error(r.status); }
  return r.json();
}
function askPin() {
  return new Promise((res, rej) => {
    const pin = prompt("Team PIN — the sender check, proof the instruction is from you:");
    if (!pin) return rej(new Error("no pin"));
    localStorage.pin = pin.trim();
    res(localStorage.pin);
  });
}
function whoAmI() {
  if (!localStorage.who) {
    const w = (prompt("Who is this? (zac / adam)") || "").trim().toLowerCase();
    if (w === "zac" || w === "adam") localStorage.who = w;
  }
  return localStorage.who || "team";
}
let toastTimer;
function toast(msg) {
  const t = $("#toast");
  t.textContent = msg; t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (t.hidden = true), 2600);
}

/* ---------------------------------------------------------------- shared bits */
const chase = (issued) => {
  const d = dayn(issued);
  if (d === null) return { label: "no issue date on record", cls: "amber" };
  if (d < 7) return { label: `${d}d out — too early to chase`, cls: "" };
  if (d < 21) return { label: `${d}d out — first follow-up`, cls: "blue" };
  if (d < 45) return { label: `${d}d out — final follow-up`, cls: "amber" };
  return { label: `${d}d out — close it or escalate`, cls: "red" };
};

function leadRow(l, dateField) {
  const d = l[dateField] || l.next_action_date || l.deadline || "";
  const late = d && d < today();
  return `<div class="row click" data-lead="${esc(l.key)}">
    <span class="t">${esc(l.title)}</span>
    <span class="m">${esc(l.company_name || l.company_key || "")}</span>
    <span class="pill blue">${esc(STAGE_LABEL[l.stage] || l.stage)}</span>
    <span class="m ${late ? "late" : ""}">${esc(d || "no date")}</span>
    <span class="v">${gbp(l.value)}</span>
  </div>`;
}
const wire = (root = document) => {
  $$("[data-lead]", root).forEach((x) => x.onclick = () => openLead(x.dataset.lead));
  $$("[data-co]", root).forEach((x) => x.onclick = () => openCompany(x.dataset.co));
  $$("[data-ct]", root).forEach((x) => x.onclick = () => openContract(x.dataset.ct));
  $$("[data-goto]", root).forEach((x) => x.onclick = () => show(x.dataset.goto));
  $$("[data-thread]", root).forEach((x) => x.onclick = (e) => {
    e.stopPropagation(); openThread(x.dataset.thread);
  });
};

/* decisions and drafts are the two things a human MUST act on */
function decisionCard(d) {
  return `<div class="glass item decision" data-id="${d.id}">
    <div class="q">${esc(d.question)}</div>
    ${d.context ? `<div class="ctx">${esc(d.context)}</div>` : ""}
    <div class="who">${esc(d.raised_by)} asked · ${rel(d.ts)}${d.entity_key ? " · " + esc(d.entity_key) : ""}</div>
    <div class="acts"><input type="text" placeholder="Your answer — it goes straight into ${esc(d.raised_by)}'s queue">
      <button class="btn small">Answer</button></div>
  </div>`;
}
function draftCard(dr) {
  return `<div class="glass item draft" data-id="${dr.id}">
    <div class="card-head"><div class="q">${esc(dr.subject || "(no subject)")}</div>
      <span class="pill violet">${esc(dr.kind)}</span></div>
    <div class="draft-to">to <b>${esc(dr.to_whom || "—")}</b> · written by ${esc(dr.author)} ${rel(dr.ts)}
      ${dr.entity_key ? " · " + esc(dr.entity_key) : ""}</div>
    <div class="draft-body">${esc(dr.body)}</div>
    <div class="acts">
      <button class="btn small" data-act="copy">Copy</button>
      <button class="btn small" data-act="sent">I have sent it</button>
      <button class="btn small ghost" data-act="discarded">Discard</button>
    </div>
  </div>`;
}
function wireActions(reload) {
  $$(".decision").forEach((el) => {
    const send = async () => {
      const v = $("input", el).value.trim();
      if (!v) return;
      await post("/decision/answer", { id: +el.dataset.id, answer: v, by: whoAmI() });
      toast("Answered — it is in their queue"); reload();
    };
    $(".btn", el).onclick = send;
    $("input", el).onkeydown = (e) => e.key === "Enter" && send();
  });
  $$(".draft").forEach((el) => {
    $$("[data-act]", el).forEach((b) => b.onclick = async () => {
      const act = b.dataset.act;
      if (act === "copy") {
        const body = $(".draft-body", el).textContent;
        navigator.clipboard.writeText(body).then(() => toast("Copied"),
          () => toast("Could not copy — select it manually"));
        return;
      }
      const note = act === "sent" ? "" : (prompt("Why not? (optional — it teaches them)") || "");
      await post("/draft/status", { id: +el.dataset.id, status: act, by: whoAmI(), note });
      toast(act === "sent" ? "Marked sent — they will learn what happened" : "Discarded");
      reload();
    });
  });
}

/* ---------------------------------------------------------------- routing */
const VIEWS = { today: vToday, mary: vDesk, jacob: vDesk, joseph: vDesk,
  activity: vActivity, cost: vCost };
let current = "today";

async function show(name) {
  current = name;
  $$("#rail .nav button").forEach((b) => b.classList.toggle("active", b.dataset.view === name));
  view.innerHTML = `<div class="empty">Loading…</div>`;
  window.scrollTo(0, 0);
  try { await VIEWS[name](name); } catch (e) {
    view.innerHTML = `<div class="glass card">Could not load <b>${esc(name)}</b>: ${esc(e.message)}</div>`;
  }
}

/* ---------------------------------------------------------------- TODAY */
async function vToday() {
  const ov = await api("/overview");
  const decisions = ov.decisions || [];
  const drafts = await api("/drafts?status=waiting");
  const cost = ov.cost_today || {};
  const needs = decisions.length + drafts.length;

  const deskCard = (p) => {
    const st = (ov.statuses || {})[p] || {};
    const n = (ov.task_counts || []).filter((r) => r.assignee === p).reduce((a, r) => a + r.n, 0);
    const working = (ov.working || []).find((w) => w.assignee === p);
    const evs = (ov.desk_events || []).filter((e) => e.author === p).slice(0, 3);
    const sess = (ov.last_sessions || []).find((s) => s.persona === p);
    const myDec = decisions.filter((d) => d.raised_by === p).length;
    const myDraft = drafts.filter((d) => d.author === p).length;
    return `<div class="glass desk-card" data-goto="${p}">
      <div class="card-head">
        <div style="display:flex;gap:11px;align-items:center;min-width:0">
          <div class="avatar ${p}">${p[0].toUpperCase()}</div>
          <div style="min-width:0"><div class="name" style="font-weight:650">${PEOPLE[p].name}</div>
            <div class="role" style="font-size:12px;color:var(--ink-3)">${PEOPLE[p].role}</div></div>
        </div>
        <span class="pill ${st.state === "working" ? "green" : st.state === "idle" ? "blue" : ""}">${st.state || "offline"}</span>
      </div>
      ${working ? `<div class="doing">now: ${esc(working.title.slice(0, 80))}</div>` : ""}
      <div class="needs-strip">
        <span class="pill">${n} in queue</span>
        ${myDec ? `<span class="pill amber">${myDec} question${myDec > 1 ? "s" : ""} for you</span>` : ""}
        ${myDraft ? `<span class="pill violet">${myDraft} draft${myDraft > 1 ? "s" : ""} to send</span>` : ""}
      </div>
      <div class="lately">${evs.map((e) => `<div class="ev tight">
        <span class="ts">${rel(e.ts)}</span>
        <span class="b">${esc(e.kind)}${e.entity_key ? " · " + esc(e.entity_key) : ""} — ${esc(e.body.slice(0, 80))}</span>
      </div>`).join("") || `<div class="empty tightpad">Nothing done yet.</div>`}</div>
      <div style="font-size:11.5px;color:var(--ink-3);border-top:1px solid var(--line);padding-top:8px">
        ${sess ? `last session ${rel(sess.ts)} · ${fmtTok(sess.context_tokens)} · ${sess.calls} calls`
               : "no sessions yet"}</div>
    </div>`;
  };

  const msgs = (ov.messages || []).slice(0, 6);
  view.innerHTML = `
  <h1>Today</h1>
  <div class="sub">${new Date().toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" })}
    — three desks, ${needs ? needs + " thing" + (needs > 1 ? "s" : "") + " waiting on you" : "nothing waiting on you"}.</div>

  <div class="grid cols-3" style="align-items:start">${Object.keys(PEOPLE).map(deskCard).join("")}</div>

  ${needs ? `<h2>Needs you <span class="count">${needs}</span>
      <span class="hint">answers go straight back into their queue</span></h2>
    <div class="grid">${decisions.map(decisionCard).join("")}${drafts.map(draftCard).join("")}</div>` : ""}

  <h2>Messages <span class="hint">click to open the conversation</span></h2>
  <div class="glass">${msgs.map((m) => `
    <div class="row click" data-thread="${esc(m.persona)}">
      <span class="m">${rel(m.ts)}</span>
      <span class="t"><b>${esc(m.author)}</b> → ${esc(m.persona)}: ${esc(m.body.slice(0, 90))}</span>
    </div>`).join("") || `<div class="empty">No conversation yet.</div>`}
    <div class="row" style="gap:8px;border-top:1px solid var(--line)">
      ${Object.keys(PEOPLE).map((p) => `<button class="btn small ghost" data-thread="${p}">Message ${PEOPLE[p].name.split(" ")[0]}</button>`).join("")}
    </div>
  </div>

  <h2>The day</h2>
  <div class="grid cols-4">
    <div class="glass stat ${needs ? "warn" : "good"}"><div class="n">${needs}</div><div class="l">waiting on you</div></div>
    <div class="glass stat"><div class="n">${(ov.task_counts || []).reduce((a, r) => a + r.n, 0)}</div><div class="l">tasks in all queues</div></div>
    <div class="glass stat"><div class="n">${fmtTok(cost.c || 0)}</div><div class="l">context today · ${cost.n || 0} sessions</div></div>
    <div class="glass stat"><div class="n">${(ov.pipeline || []).reduce((a, r) => a + r.n, 0)}</div><div class="l">live jobs on the record</div></div>
  </div>`;
  wire(); wireActions(vToday);
  refreshBadges(ov, decisions, drafts);
}

/* ---------------------------------------------------------------- A DESK */
function deskHeader(d) {
  const p = d.persona, st = d.status || {};
  const working = (d.tasks || []).find((t) => t.status === "working");
  const s = d.last_session, c = d.cost_today || {};
  return `<div class="glass desk-head">
    <div class="avatar ${p}">${p[0].toUpperCase()}</div>
    <div class="desk-id">
      <div class="name">${PEOPLE[p].name}</div>
      <div class="role">${PEOPLE[p].role} — ${PEOPLE[p].job}</div>
      ${working ? `<div class="doing">now: ${esc(working.title.slice(0, 110))}</div>` : ""}
    </div>
    <div class="desk-stats">
      <div><b>${(d.tasks || []).length}</b>in queue</div>
      <div><b>${(d.drafts || []).length}</b>drafts waiting</div>
      <div><b>${(d.decisions || []).filter((x) => x.status === "open").length}</b>questions</div>
      <div><b>${fmtTok(c.c || 0)}</b>context today</div>
      <div><b>${s ? rel(s.ts) : "—"}</b>last session${s ? ` · ${fmtTok(s.context_tokens)}` : ""}</div>
    </div>
    <div style="display:flex;flex-direction:column;gap:8px">
      <span class="pill ${st.state === "working" ? "green" : st.state === "idle" ? "blue" : ""}">${st.state || "offline"}</span>
      <button class="btn small" data-thread="${p}">Message</button>
    </div>
  </div>`;
}

const queueSection = (d) => `
  <h2>Queue <span class="count">${(d.tasks || []).length}</span>
    <span class="hint">what they will pick up next, most urgent first</span></h2>
  <div class="glass">${(d.tasks || []).slice(0, 12).map((t) => `
    <div class="row ${t.entity_key ? "click" : ""}" ${t.entity_key ? `data-lead="${esc(t.entity_key)}"` : ""}>
      <span class="pill ${t.status === "working" ? "green" : ""}">${t.status === "working" ? "working" : "p" + t.priority}</span>
      <span class="t">${esc(t.title)}</span>
      <span class="m">${esc(t.kind)}${t.needs ? " · " + esc(t.needs) : ""}</span>
      <span class="m">${rel(t.created)}</span>
    </div>`).join("") || `<div class="empty">Queue is empty.</div>`}
  </div>`;

const latelySection = (d) => `
  <h2>Lately <span class="hint">everything they have recorded, newest first</span></h2>
  <div class="glass feed">${(d.events || []).slice(0, 14).map((e) => `
    <div class="ev"><span class="ts">${esc(e.ts.slice(5, 16))}</span>
      <span class="k"><span class="pill ${e.kind === "catch" ? "amber" : e.kind.startsWith("mail") ? "blue" : ""}">${esc(e.kind)}</span></span>
      <span class="b">${e.entity_key ? "<b>" + esc(e.entity_key) + "</b> — " : ""}${esc(e.body)}</span>
    </div>`).join("") || `<div class="empty">Nothing recorded yet.</div>`}
  </div>`;

function needsSection(d, extra = "") {
  const open = (d.decisions || []).filter((x) => x.status === "open");
  const n = open.length + (d.drafts || []).length;
  if (!n && !extra) return "";
  return `<h2>Needs you <span class="count">${n}</span></h2>
    ${extra}<div class="grid">${open.map(decisionCard).join("")}${(d.drafts || []).map(draftCard).join("")}</div>`;
}

async function vDesk(p) {
  const d = await api("/desk/" + p);
  const body = p === "mary" ? maryBody(d) : p === "jacob" ? jacobBody(d) : josephBody(d);
  view.innerHTML = `
    <h1>${PEOPLE[p].name}</h1>
    <div class="sub">${PEOPLE[p].job}.</div>
    ${deskHeader(d)}
    ${body}
    ${queueSection(d)}
    ${latelySection(d)}`;
  wire();
  wireActions(() => vDesk(p));
  if (p === "jacob") wireCompanies(d);
}

/* -------- MARY: the estimator. Her clock is the tender deadline. */
function maryBody(d) {
  const board = d.board || [];
  const byStage = {};
  board.forEach((l) => (byStage[l.stage] ||= []).push(l));
  const order = ["pre_quote_call", "quote_ready", "awaiting_costs", "materials_out",
    "acknowledged", "new"];
  const ready = d.ready_to_check || [];
  const readyBlock = ready.length ? `
    <div class="glass" style="margin-bottom:13px">
      <div class="row" style="border:0;font-weight:600">Quotes built and waiting for Adam to check</div>
      ${ready.map((q) => `<div class="row click" data-lead="${esc(q.lead_key)}">
        <span class="t">${esc(q.title)}</span><span class="m">rev ${q.revision} · ${esc(q.status)}</span>
        <span class="v">${gbp(q.value)}</span></div>`).join("")}
    </div>` : "";

  return `
  ${needsSection(d, readyBlock)}

  <h2>On the board <span class="count">${board.length} jobs · ${gbp(board.reduce((a, l) => a + (l.value || 0), 0))}</span>
    <span class="hint">the estimating half of the pipeline</span></h2>
  ${d.no_deadline ? `<div class="glass card" style="margin-bottom:12px;border-color:var(--amber)">
    <b>${d.no_deadline} of these have no tender deadline recorded.</b>
    <div class="sub" style="margin:4px 0 0">A deadline is the only clock estimating runs on, and the
    record cannot sort, warn or chase without one. They live in Mary's job notes but were never
    written to the record — worth telling her to fix on her next run.</div></div>` : ""}
  ${order.filter((s) => byStage[s]).map((s) => `
    <div class="glass" style="margin-bottom:11px">
      <div class="row" style="font-weight:600;border:0">
        <span class="t">${STAGE_LABEL[s]}</span>
        <span class="m">${byStage[s].length} job${byStage[s].length > 1 ? "s" : ""}</span>
        <span class="v">${gbp(byStage[s].reduce((a, l) => a + (l.value || 0), 0))}</span></div>
      ${byStage[s].map((l) => `<div class="row click" data-lead="${esc(l.key)}">
        <span class="t">${esc(l.title)}</span>
        <span class="m">${esc(l.company_name || l.company_key || "")}</span>
        <span class="m ${l.deadline && l.deadline < today() ? "late" : ""}">${l.deadline ? "due " + esc(l.deadline) : "no deadline"}</span>
        <span class="v">${gbp(l.value)}</span></div>`).join("")}
    </div>`).join("") || `<div class="glass"><div class="empty">Nothing in pricing.</div></div>`}

  <h2>Catches <span class="count">${(d.catches || []).length}</span>
    <span class="hint">errors she found that would have gone out — her scoreboard</span></h2>
  <div class="glass feed">${(d.catches || []).map((c) => `
    <div class="ev"><span class="ts">${esc(c.ts.slice(5, 16))}</span>
      <span class="b">${c.entity_key ? "<b>" + esc(c.entity_key) + "</b> — " : ""}${esc(c.body)}</span></div>`).join("")
    || `<div class="empty">No catches recorded yet.</div>`}
  </div>`;
}

/* -------- JACOB: the BDM. His clock is days since the quote went out. */
function jacobBody(d) {
  const calls = d.calls_today || [];
  const out = d.out_for_decision || [];
  const score = d.scoreboard || [];
  const won = score.find((s) => s.outcome === "won") || { n: 0, v: 0 };
  const lost = score.find((s) => s.outcome === "lost") || { n: 0, v: 0 };
  const rate = (won.n + lost.n) ? Math.round(100 * won.n / (won.n + lost.n)) : null;
  const cos = d.companies || [];
  const paid = cos.filter((c) => c.relationship === "won");

  return `
  ${needsSection(d)}

  <h2>Today's calls <span class="count">${calls.length}</span>
    <span class="hint">these are the people to ring today</span></h2>
  <div class="glass">${calls.map((l) => `
    <div class="row click" data-lead="${esc(l.key)}">
      <span class="t">${esc(l.title)}</span>
      <span class="m">${esc(l.company_name || l.company_key || "")}</span>
      <span class="m ${l.next_action_date < today() ? "late" : ""}">${esc(l.next_action_date)}</span>
      <span class="v">${gbp(l.value)}</span></div>
    ${l.next_action ? `<div class="row" style="border:0;padding-top:0"><span class="m" style="white-space:normal">↳ ${esc(l.next_action)}</span></div>` : ""}
    `).join("") || `<div class="empty">No calls fall due today.</div>`}
  </div>

  <h2>Out for decision <span class="count">${out.length} · ${gbp(out.reduce((a, l) => a + (l.value || 0), 0))}</span>
    <span class="hint">quotes issued and not yet answered</span></h2>
  <div class="glass">${out.map((l) => {
    const c = chase(l.issued_at);
    return `<div class="row click" data-lead="${esc(l.key)}">
      <span class="t">${esc(l.title)}</span>
      <span class="m">${esc(l.company_name || l.company_key || "")}</span>
      <span class="pill ${c.cls}">${c.label}</span>
      <span class="v">${gbp(l.value)}</span></div>`; }).join("")
    || `<div class="empty">Nothing is out for decision.</div>`}
  </div>
  ${(d.no_chase_date || []).length ? `<div class="glass card" style="margin-top:11px;border-color:var(--amber)">
    <b>${d.no_chase_date.length} issued quote${d.no_chase_date.length > 1 ? "s have" : " has"} no next chase date.</b>
    <div class="sub" style="margin:4px 0 0">Without one it will never appear on a call list — this is
    exactly how £548k went quiet before. Worth telling Jacob to set them.</div></div>` : ""}

  <h2>Client award dates <span class="count">${(d.award_dates || []).length}</span>
    <span class="hint">when OUR client hears whether THEY won — red means ring them</span></h2>
  <div class="glass">${(d.award_dates || []).map((l) => {
    const due = l.award_due <= today();
    return `<div class="row click" data-lead="${esc(l.key)}">
      <span class="t">${esc(l.title)}</span>
      <span class="m">${esc(l.company_name || l.company_key || "")}</span>
      <span class="pill ${due ? "red" : ""}">${due ? "call them" : "hears " + esc(l.award_due)}</span>
      <span class="v">${gbp(l.value)}</span></div>`; }).join("")
    || `<div class="empty">No award dates recorded. Adam asks for this on the pre-quote
        call — "when are you making a decision" — and it is what turns a chase into a
        timed call rather than a guess.</div>`}
  </div>

  <h2>Scoreboard <span class="hint">the outcome data the business never used to keep</span></h2>
  <div class="glass score">
    <div><b style="color:var(--accent-ink)">${won.n}</b><span>won · ${gbp(won.v)}</span></div>
    <div><b style="color:var(--red)">${lost.n}</b><span>lost · ${gbp(lost.v)}</span></div>
    <div><b>${rate === null ? "—" : rate + "%"}</b><span>win rate</span></div>
    <div><b>${out.length}</b><span>still undecided</span></div>
  </div>
  <div class="sub" style="margin-top:8px">Mark a quote won or lost from any job card — one click, and
    it sharpens both his targeting and Mary's accuracy.</div>

  <h2>The book <span class="count">${cos.length} companies · ${paid.length} have paid us</span></h2>
  <div class="filter-bar"><input type="text" id="co-q" placeholder="Search companies…"></div>
  <div class="glass" id="co-list"></div>`;
}

/* -------- JOSEPH: the PM. His clock is the site date, worked backwards. */
function josephBody(d) {
  const cts = d.contracts || [];
  const live = cts.filter((c) => c.status === "live");
  const steps = d.steps_due || [];
  const inv = d.invoices || [];
  const owed = inv.filter((i) => i.status !== "paid").reduce((a, i) => a + (i.value || 0), 0);

  return `
  ${needsSection(d)}

  <h2>Live contracts <span class="count">${live.length} · ${gbp(live.reduce((a, c) => a + (c.value || 0), 0))}</span>
    <span class="hint">a purchase order opens one of these</span></h2>
  <div class="grid cols-2">${cts.map((c) => {
    const doneN = (c.steps_total || 0) - (c.steps_open || 0);
    const pc = c.steps_total ? Math.round(100 * doneN / c.steps_total) : 0;
    return `<div class="glass card" style="cursor:pointer" data-ct="${esc(c.key)}">
      <div class="card-head"><b style="line-height:1.3">${esc(c.title)}</b>
        <span class="pill ${c.status === "live" ? "green" : ""}">${esc(c.status)}</span></div>
      <div class="sub" style="margin:5px 0 0">${esc(c.company_name || c.company_key)}
        · ${gbp(c.value) || "value not set"} · site ${esc(c.site_date || "date not set")}</div>
      <div class="progress"><i style="width:${pc}%"></i></div>
      <div class="sub" style="margin-top:6px">${c.steps_total
        ? `${doneN} of ${c.steps_total} steps done`
        : "no checklist yet — the twelve steps have not been seeded"}</div>
    </div>`; }).join("") || `<div class="glass card empty">No contracts on the record.</div>`}
  </div>

  ${steps.length && !steps.some((s) => s.due) ? `<div class="glass card"
    style="margin:0 0 12px;border-color:var(--amber)">
    <b>No step has a deadline, because nobody has recorded the lead times.</b>
    <div class="sub" style="margin:4px 0 0">Every step works backwards from the site
    date — but how many days before installation the frames and glass must be ordered
    is a Fenster fact only Adam or Paul knows, and inventing it would put made-up dates
    in front of the fitters. Say the numbers once, they go in
    <code>core/contract_template.py</code>, and every contract gets its dates.
    ${cts.some((c) => !c.site_date) ? " Site dates are missing too." : ""}</div></div>` : ""}

  <h2>Next steps due <span class="count">${steps.length}</span>
    <span class="hint">every deadline works backwards from the site date</span></h2>
  <div class="glass">${steps.map((s) => {
    const late = s.due && s.due < today();
    return `<div class="step click" data-ct="${esc(s.contract_key)}" style="cursor:pointer">
      <span class="n">${s.n}</span><span class="lbl">${esc(s.label)}</span>
      <span class="det">${esc(s.contract_title || "")}</span>
      <span class="m ${late ? "late" : ""}" style="flex:none">${s.due ? (late ? "LATE " : "due ") + esc(s.due) : "no date"}</span>
    </div>`; }).join("") || `<div class="empty">Nothing outstanding — or no checklists seeded yet.</div>`}
  </div>

  <h2>Money <span class="count">${inv.length} invoice${inv.length === 1 ? "" : "s"}${owed ? " · " + gbp(owed) + " outstanding" : ""}</span>
    <span class="hint">chase ladder: day 7 reminder, day 35 why-unpaid, day 75 escalation</span></h2>
  <div class="glass">${inv.map((i) => {
    const late = i.status !== "paid" && i.due ? dayn(i.due) : null;
    const rung = late === null || late < 0 ? null
      : late >= 75 ? { t: `${late}d overdue — ESCALATION, Adam decides`, c: "red" }
      : late >= 35 ? { t: `${late}d overdue — why has this not been paid`, c: "red" }
      : late >= 7 ? { t: `${late}d overdue — reminder due`, c: "amber" }
      : { t: `${late}d overdue`, c: "amber" };
    return `<div class="row click" data-ct="${esc(i.contract_key)}">
      <span class="t">${esc(i.ref || "(unreferenced)")}</span>
      <span class="m">${esc(i.contract_title || "")}</span>
      <span class="pill ${i.status === "paid" ? "green" : rung ? rung.c : ""}">${i.status === "paid" ? "paid" : rung ? rung.t : esc(i.status)}</span>
      <span class="m">${i.due ? "due " + esc(i.due) : "no due date"}</span>
      <span class="v">${gbp(i.value)}</span></div>`; }).join("")
    || `<div class="empty">No invoices raised. Step twelve raises the first one — the job
        date passes, Joseph knows it is done, and it comes here as "invoice to check"
        before anything goes to a client.</div>`}
  </div>`;
}

/* companies list lives on Jacob's page and is wired after render */
function wireCompanies(d) {
  const cos = d.companies || [];
  const list = $("#co-list"); if (!list) return;
  const row = (c) => `<div class="row click" data-co="${esc(c.key)}">
    <span class="t">${esc(c.name)}</span>
    <span class="pill ${c.relationship === "won" ? "green" : c.relationship === "quoted" ? "blue" : ""}">${esc(c.relationship)}</span>
    <span class="m">${c.open_leads ? c.open_leads + " open" : ""}</span>
    <span class="v">${gbp(c.lifetime_value)}</span></div>`;
  const render = (q) => {
    const rows = (q ? cos.filter((c) => (c.name + " " + c.key).toLowerCase().includes(q))
                    : cos.slice(0, 10));
    list.innerHTML = rows.map(row).join("") +
      (!q && cos.length > 10 ? `<div class="empty">Top 10 by lifetime value. Search above for the other ${cos.length - 10}.</div>` : "") ||
      `<div class="empty">No match.</div>`;
    wire(list);
  };
  render("");
  $("#co-q").oninput = (e) => render(e.target.value.toLowerCase().trim());
}

/* ---------------------------------------------------------------- ACTIVITY */
async function vActivity() {
  const evs = await api("/feed?limit=250");
  let who = "all", showMail = false;
  view.innerHTML = `
  <h1>Activity</h1>
  <div class="sub">The ledger — every fact, by every author, newest first.</div>
  <div class="filter-bar" id="chips">
    ${["all", "mary", "jacob", "joseph", "intake"].map((w) =>
      `<button class="chip ${w === "all" ? "on" : ""}" data-who="${w}">${w}</button>`).join("")}
    <button class="chip" id="chip-mail">show routine mail</button>
    <input type="text" id="q" placeholder="Search…">
  </div>
  <div class="glass feed" id="list"></div>`;
  const render = () => {
    const q = ($("#q").value || "").toLowerCase();
    const rows = evs.filter((e) =>
      (who === "all" || e.author === who) &&
      (showMail || !["mail_fyi", "mail_clerical"].includes(e.kind)) &&
      (!q || (e.author + e.kind + e.entity_key + e.body).toLowerCase().includes(q))).slice(0, 70);
    $("#list").innerHTML = rows.map((e) => `
      <div class="ev"><span class="ts">${esc(e.ts.slice(5, 16))}</span>
        <span class="k"><span class="pill ${e.kind === "catch" ? "amber" : e.kind.startsWith("mail") ? "blue" : ""}">${esc(e.kind)}</span></span>
        <span class="b"><b>${esc(e.author)}</b>${e.entity_key ? " · " + esc(e.entity_key) : ""} — ${esc(e.body)}</span></div>`).join("")
      || `<div class="empty">Nothing matches.</div>`;
  };
  $$("#chips .chip[data-who]").forEach((c) => c.onclick = () => {
    who = c.dataset.who;
    $$("#chips .chip[data-who]").forEach((x) => x.classList.toggle("on", x === c));
    render();
  });
  $("#chip-mail").onclick = () => { showMail = !showMail;
    $("#chip-mail").classList.toggle("on", showMail); render(); };
  $("#q").oninput = render;
  render();
}

/* ---------------------------------------------------------------- COST */
async function vCost() {
  const c = await api("/cost");
  const TARGET = 118e6;
  const byDay = {};
  (c.days || []).forEach((r) => { (byDay[r.day] ||= {})[r.persona] = r; });
  const days = Object.keys(byDay).sort().slice(-14);
  const totals = days.map((d) => Object.values(byDay[d]).reduce((a, r) => a + r.context, 0));
  const max = Math.max(TARGET * 0.4, ...totals);
  const t = byDay[today()] || {};
  const tTot = Object.values(t).reduce((a, r) => a + r.context, 0);
  let all = false;

  view.innerHTML = `
  <h1>Cost</h1>
  <div class="sub">Context tokens — the real meter, deduped per call. Target ${fmtTok(TARGET)} a day for the whole system.</div>
  <div class="grid cols-4">
    <div class="glass stat ${tTot > TARGET ? "bad" : "good"}"><div class="n">${fmtTok(tTot)}</div>
      <div class="l">today, all desks — ${Math.round(100 * tTot / TARGET)}% of target</div></div>
    ${Object.keys(PEOPLE).map((p) => `<div class="glass stat"><div class="n">${fmtTok((t[p] || {}).context || 0)}</div>
      <div class="l">${p} · ${(t[p] || {}).sessions || 0} session${((t[p] || {}).sessions || 0) === 1 ? "" : "s"}</div></div>`).join("")}
  </div>

  <h2>By day <span class="hint">bar height is context tokens; ⚠ marks a day over target</span></h2>
  <div class="glass">
    <div class="chart">${days.map((d, i) => {
      const rs = byDay[d], tot = totals[i];
      return `<div class="bar" title="${d}: ${fmtTok(tot)}">
        ${["joseph", "jacob", "mary"].map((p) => rs[p]
          ? `<i class="${p}" style="height:${Math.max(3, Math.round(110 * rs[p].context / max))}px"></i>` : "").join("")}
        <span class="d">${d.slice(5)}${tot > TARGET ? " ⚠" : ""}</span></div>`; }).join("")
      || `<div class="empty">No sessions metered yet.</div>`}</div>
    <div class="legend">${Object.keys(PEOPLE).map((p) =>
      `<span><i class="${p}" style="background:${p === "mary" ? "#1f9d5b" : p === "jacob" ? "#2470a8" : "#8a5fbf"}"></i>${PEOPLE[p].name.split(" ")[0]}</span>`).join("")}
      <span style="margin-left:auto">target ${fmtTok(TARGET)}/day</span></div>
  </div>

  <h2>Recent sessions <span class="hint">a fat session is a chat carrying too much, not a bot working hard</span></h2>
  <div class="glass"><table id="sess"></table>
    <div class="empty" style="padding:10px 14px"><a href="#" id="more">show all ${(c.recent || []).length}</a></div></div>`;

  const renderSess = () => {
    $("#sess").innerHTML = `<tr><th>when</th><th>desk</th><th>job</th><th>model</th>
      <th>calls</th><th>context</th><th>secs</th></tr>` +
      (c.recent || []).slice(0, all ? 999 : 12).map((r) => `<tr>
        <td>${esc(r.ts.slice(5, 16))}</td><td>${esc(r.persona)}</td>
        <td>${esc(r.entity_key || "—")}</td>
        <td>${esc((r.model || "").replace("claude-", ""))}</td>
        <td>${r.calls}</td><td>${fmtTok(r.context_tokens)}</td><td>${r.seconds}</td></tr>`).join("");
  };
  renderSess();
  $("#more").onclick = (e) => { e.preventDefault(); all = !all; renderSess();
    e.target.textContent = all ? "show fewer" : `show all ${(c.recent || []).length}`; };
}

/* ---------------------------------------------------------------- drawer */
function openDrawer(html) { $("#drawer-body").innerHTML = html; $("#drawer").hidden = false; }
$("#drawer-close").onclick = () => ($("#drawer").hidden = true);
$("#drawer").onclick = (e) => { if (e.target.id === "drawer") $("#drawer").hidden = true; };
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") { $("#drawer").hidden = true; $("#thread").hidden = true; }
});

async function openLead(key) {
  let c;
  try { c = await api("/card/lead/" + encodeURIComponent(key)); }
  catch { return; }
  const l = c.lead, co = c.company || {};
  openDrawer(`
    <h1>${esc(l.title)}</h1>
    <div class="sub">${esc(co.name || l.company_key)} ·
      <span class="pill blue">${esc(STAGE_LABEL[l.stage] || l.stage)}</span> · owner ${esc(l.owner)}</div>
    <div class="kv">
      <b>Value</b><span>${gbp(l.value) || "not set"} ex VAT</span>
      <b>Deadline</b><span>${esc(l.deadline || "not recorded")}</span>
      <b>Award due</b><span>${esc(l.award_due || "not recorded")}</span>
      <b>Next action</b><span>${esc(l.next_action_date || "")} ${esc(l.next_action || "none set")}</span>
      ${l.outcome ? `<b>Outcome</b><span>${esc(l.outcome)} ${esc(l.outcome_why || "")}</span>` : ""}
    </div>
    ${["quote_sent", "follow_up", "final_follow_up"].includes(l.stage) ? `
      <div style="display:flex;gap:8px;margin:4px 0 16px">
        <button class="btn small" id="won">Mark WON</button>
        <button class="btn small danger" id="lost">Mark LOST</button></div>` : ""}
    ${(c.quotes || []).length ? `<h2>Quotes</h2>` + c.quotes.map((q) =>
      `<div class="row"><span class="t">rev ${q.revision} — ${esc(q.status)}</span>
       <span class="m">${esc(q.issued_at || "")}</span><span class="v">${gbp(q.value)}</span></div>`).join("") : ""}
    ${l.position ? `<h2>Position <span class="hint">what the last session knew</span></h2>
      <div class="position">${esc(l.position)}</div>` : ""}
    ${(c.contacts || []).length ? `<h2>Contacts</h2>` + c.contacts.map((x) =>
      `<div class="row"><span class="t">${esc(x.name || "—")}</span>
       <span class="m">${esc(x.email || "")}</span></div>`).join("") : ""}
    <h2>Recent</h2>
    <div class="feed">${(c.recent_events || []).slice(0, 12).map((e) => `
      <div class="ev"><span class="ts">${esc(e.ts.slice(5, 16))}</span>
      <span class="b"><b>${esc(e.author)}</b> ${esc(e.kind)} — ${esc(e.body)}</span></div>`).join("")
      || `<div class="empty">Quiet.</div>`}</div>`);
  const mark = (o) => async () => {
    const why = prompt("Why? (one line, optional — it is what makes the data useful)") || "";
    await post("/outcome", { lead_key: key, outcome: o, why, by: whoAmI() });
    toast("Recorded"); $("#drawer").hidden = true; show(current);
  };
  if ($("#won")) $("#won").onclick = mark("won");
  if ($("#lost")) $("#lost").onclick = mark("lost");
}

async function openCompany(key) {
  const c = await api("/card/company/" + encodeURIComponent(key));
  const co = c.company;
  openDrawer(`
    <h1>${esc(co.name)}</h1>
    <div class="sub"><span class="pill ${co.relationship === "won" ? "green" : ""}">${esc(co.relationship)}</span>
      ${co.lifetime_value ? " · has paid us " + gbp(co.lifetime_value) : ""}
      ${co.payment_terms ? " · terms: " + esc(co.payment_terms) : ""}</div>
    ${co.position ? `<h2>Position</h2><div class="position">${esc(co.position)}</div>` : ""}
    ${(c.leads || []).length ? `<h2>Jobs</h2>` + c.leads.map((l) =>
      `<div class="row click" data-lead="${esc(l.key)}"><span class="t">${esc(l.title)}</span>
       <span class="m">${esc(STAGE_LABEL[l.stage] || l.stage)}</span>
       <span class="v">${gbp(l.value)}</span></div>`).join("") : ""}
    ${(c.contacts || []).length ? `<h2>Contacts</h2>` + c.contacts.map((x) =>
      `<div class="row"><span class="t">${esc(x.name || "—")}</span>
       <span class="m">${esc(x.email || "")}</span></div>`).join("") : ""}
    <h2>Recent</h2>
    <div class="feed">${(c.recent_events || []).slice(0, 12).map((e) => `
      <div class="ev"><span class="ts">${esc(e.ts.slice(5, 16))}</span>
      <span class="b"><b>${esc(e.author)}</b> ${esc(e.kind)} — ${esc(e.body)}</span></div>`).join("")
      || `<div class="empty">Quiet.</div>`}</div>`);
  wire($("#drawer-body"));
}

async function openContract(key) {
  const c = await api("/card/contract/" + encodeURIComponent(key));
  const ct = c.contract;
  openDrawer(`
    <h1>${esc(ct.title)}</h1>
    <div class="sub">${esc((c.company || {}).name || ct.company_key)} ·
      <span class="pill ${ct.status === "live" ? "green" : ""}">${esc(ct.status)}</span></div>
    <div class="kv">
      <b>PO</b><span>${esc(ct.po_ref || "none recorded")}</span>
      <b>Value</b><span>${gbp(ct.value) || "not set"} ex VAT</span>
      <b>Site date</b><span>${esc(ct.site_date || "not set — every step deadline works back from this")}</span>
    </div>
    <h2>The twelve steps</h2>
    <div>${(c.steps || []).map((s) => `
      <div class="step ${s.done_at ? "done" : ""}"><span class="n">${s.n}</span>
        <span class="lbl"><span class="what">${esc(s.label)}</span>${s.detail
          ? `<div class="det" style="white-space:normal">${esc(s.detail)}</div>` : ""}</span>
        <span class="m" style="flex:none">${s.done_at ? "done " + esc(s.done_at.slice(0, 10))
          : s.due ? "due " + esc(s.due) : "no date"}</span></div>`).join("")
      || `<div class="empty">No checklist seeded yet — Joseph builds it from the PO and the site date.</div>`}</div>
    ${(c.invoices || []).length ? `<h2>Invoices</h2>` + c.invoices.map((i) =>
      `<div class="row"><span class="t">${esc(i.ref || "draft")}</span>
       <span class="pill ${i.status === "paid" ? "green" : "amber"}">${esc(i.status)}</span>
       <span class="v">${gbp(i.value)}</span></div>`).join("") : ""}
    ${ct.position ? `<h2>Position</h2><div class="position">${esc(ct.position)}</div>` : ""}
    <h2>Recent</h2>
    <div class="feed">${(c.recent_events || []).slice(0, 12).map((e) => `
      <div class="ev"><span class="ts">${esc(e.ts.slice(5, 16))}</span>
      <span class="b"><b>${esc(e.author)}</b> ${esc(e.kind)} — ${esc(e.body)}</span></div>`).join("")
      || `<div class="empty">Quiet.</div>`}</div>`);
}

/* ---------------------------------------------------------------- thread */
let threadWith = null;
async function openThread(p) {
  threadWith = p;
  $("#thread").hidden = false;
  $("#thread-head").innerHTML = `
    <div class="avatar ${p}" style="width:38px;height:38px;font-size:15px">${p[0].toUpperCase()}</div>
    <div><div class="name">${PEOPLE[p].name}</div><div class="role">${PEOPLE[p].role}</div></div>
    <button class="close" title="Close">×</button>`;
  $("#thread-head .close").onclick = () => ($("#thread").hidden = true);
  $("#thread-input").placeholder = `Message ${PEOPLE[p].name.split(" ")[0]}…`;
  await paintThread();
  $("#thread-input").focus();
}
async function paintThread() {
  const p = threadWith;
  const msgs = (await api("/messages?persona=" + p)).reverse();
  let lastDay = "";
  $("#thread-body").innerHTML = msgs.map((m) => {
    const day = (m.ts || "").slice(0, 10);
    const mark = day !== lastDay ? (lastDay = day,
      `<div class="daymark">${new Date(day).toLocaleDateString("en-GB", { day: "numeric", month: "short" })}</div>`) : "";
    return mark + `<div class="bubble ${m.author === p ? "them" : "me"}">
      <div class="who">${esc(m.author)} · ${rel(m.ts)}</div>${esc(m.body)}</div>`;
  }).join("") || `<div class="empty">No messages yet. Anything you send here reaches
    ${PEOPLE[p].name.split(" ")[0]} as a trusted instruction.</div>`;
  const b = $("#thread-body"); b.scrollTop = b.scrollHeight;
}
$("#thread").onclick = (e) => { if (e.target.id === "thread") $("#thread").hidden = true; };
$("#thread-send").onclick = async () => {
  const el = $("#thread-input"), body = el.value.trim();
  if (!body) return;
  await post("/message", { persona: threadWith, body, author: whoAmI() });
  el.value = ""; el.style.height = "auto";
  await paintThread();
  toast("Sent — it is at the top of their queue");
  refreshBadges();
};
$("#thread-input").addEventListener("input", (e) => {
  e.target.style.height = "auto";
  e.target.style.height = Math.min(140, e.target.scrollHeight) + "px";
});
$("#thread-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); $("#thread-send").click(); }
});

/* ---------------------------------------------------------------- chrome */
async function refreshBadges(ov, decisions, drafts) {
  try {
    ov = ov || await api("/overview");
    decisions = decisions || ov.decisions || [];
    drafts = drafts || await api("/drafts?status=waiting");
    Object.keys(PEOPLE).forEach((p) => {
      const n = decisions.filter((d) => d.raised_by === p).length +
                drafts.filter((d) => d.author === p).length;
      const el = $(`[data-badge="${p}"]`);
      if (el) { el.textContent = n || ""; el.classList.toggle("on", !!n); }
    });
  } catch { /* badges are decoration; never break the page for them */ }
}

$$("#rail .nav button").forEach((b) => (b.onclick = () => show(b.dataset.view)));
$("#theme-toggle").onclick = () => {
  const cur = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = cur;
  localStorage.theme = cur;
};
if (localStorage.theme) document.documentElement.dataset.theme = localStorage.theme;
else if (matchMedia("(prefers-color-scheme: dark)").matches)
  document.documentElement.dataset.theme = "dark";
setInterval(() => ($("#clock").textContent =
  new Date().toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" })), 1000);
setInterval(() => { if (current === "today") vToday().catch(() => {}); }, 60000);

show("today");
refreshBadges();
