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
// Re-queried whenever the shell is rebuilt (sign in, sign out). Held as a
// const it went stale the moment login replaced the shell, and every page
// rendered into a node that was no longer on the document.
let view = $("#view");

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

/* The bots write Markdown - headings, **bold**, lists - and it was being shown
   as literal asterisks and hashes. This renders the small subset they actually
   use. It ESCAPES FIRST and only then adds tags, so nothing in a supplier's
   email can inject markup: by the time any of these patterns are matched,
   every < > & " in the source is already inert. */
function md(src) {
  const t = esc(src).replace(/\r\n/g, "\n")
    .replace(/`([^`\n]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[\s(])\*([^*\n]+)\*(?=[\s.,;:)]|$)/g, "$1<em>$2</em>")
    .replace(/(^|[\s(])_([^_\n]+)_(?=[\s.,;:)]|$)/g, "$1<em>$2</em>");
  const out = [];
  let para = [], list = null;
  const flushP = () => { if (para.length) { out.push("<p>" + para.join(" ") + "</p>"); para = []; } };
  const flushL = () => { if (list) { out.push("<" + list.tag + ">" + list.items.join("") +
    "</" + list.tag + ">"); list = null; } };
  for (const line of t.split("\n")) {
    const h = line.match(/^(#{1,4})\s+(.*)$/);
    const ul = line.match(/^\s*[-*+]\s+(.*)$/);
    const ol = line.match(/^\s*\d+[.)]\s+(.*)$/);
    if (h) { flushP(); flushL(); out.push("<h4 class='md-h'>" + h[2] + "</h4>"); continue; }
    if (ul || ol) {
      flushP();
      const tag = ul ? "ul" : "ol";
      if (!list || list.tag !== tag) { flushL(); list = { tag, items: [] }; }
      list.items.push("<li>" + (ul ? ul[1] : ol[1]) + "</li>");
      continue;
    }
    flushL();
    // A blank line ends the paragraph; otherwise the bots' hard-wrapped lines
    // are joined back into one, instead of becoming a paragraph each.
    if (!line.trim()) flushP(); else para.push(line.trim());
  }
  flushP(); flushL();
  return out.join("");
}
const gbp = (v) => v == null || v === "" ? "" :
  "£" + Number(v).toLocaleString("en-GB", { maximumFractionDigits: 0 });
const fmtTok = (n) => !n ? "0" : n >= 1e6 ? (n / 1e6).toFixed(1) + "M"
  : n >= 1e3 ? Math.round(n / 1e3) + "k" : String(n);
const today = () => new Date().toISOString().slice(0, 10);
// The record stores UTC. Showing that raw tells someone in August that a job
// finishes an hour before it does - the exact trap written into Mary's own
// charter, made here in her hub.
const hhmm = (iso) => new Date(iso).toLocaleTimeString("en-GB",
  { hour: "2-digit", minute: "2-digit" });
const dayn = (d) => d ? Math.floor((Date.now() - new Date(d + (d.length < 11 ? "T12:00:00Z" : "")).getTime()) / 864e5) : null;
const rel = (ts) => {
  if (!ts) return "";
  const d = (Date.now() - new Date(ts.replace(" ", "T") + "Z").getTime()) / 1000;
  if (d < 90) return "just now";
  if (d < 5400) return Math.round(d / 60) + "m ago";
  if (d < 129600) return Math.round(d / 3600) + "h ago";
  return Math.round(d / 86400) + "d ago";
};

/* ---------------------------------------------------------------- session */
let ME = null;   // {name, display, role}
const authHeaders = () => localStorage.gh_token
  ? { authorization: "Bearer " + localStorage.gh_token } : {};

async function api(path) {
  const r = await fetch("/api" + path, { headers: authHeaders() });
  if (r.status === 401) { signOut(); throw new Error("signed out"); }
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).error || r.status);
  return r.json();
}
async function post(path, body) {
  const r = await fetch("/api" + path, {
    method: "POST",
    headers: { "content-type": "application/json", ...authHeaders() },
    body: JSON.stringify(body),
  });
  if (r.status === 401) { signOut(); throw new Error("signed out"); }
  if (!r.ok) {
    const e = (await r.json().catch(() => ({}))).error;
    toast(e || "That did not save");
    throw new Error(e || r.status);
  }
  return r.json();
}
const whoAmI = () => (ME && ME.name) || "team";
function signOut() {
  delete localStorage.gh_token;
  ME = null;
  renderLogin();
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

/* A NEED is the one thing a human must act on.

   Two buttons, then a list, then the detail. It used to render every question
   AND its full context inline - twenty-four of those is a wall nobody reads,
   which is the opposite of the point. Now the counts are on a button, the
   button opens one-line rows, and a row opens the whole thing in the drawer
   where there is room for it. */
let NEEDS = [];          // whatever the current page loaded
let needOpen = null;     // "fenster" | "supplier" | null

function needTiles(list, where) {
  const us = list.filter((d) => d.source !== "supplier");
  const them = list.filter((d) => d.source === "supplier");
  if (!list.length) return "";
  const tile = (kind, n, title, sub) => `
    <button class="glass need-tile ${needOpen === kind ? "open" : ""} ${kind}"
            data-need="${kind}" ${n ? "" : "disabled"}>
      <span class="n">${n}</span>
      <span class="t">${title}</span>
      <span class="s">${sub}</span>
      <span class="chev">${needOpen === kind ? "▾" : "›"}</span>
    </button>`;
  return `
  <h2>Needs you <span class="count">${list.length}</span></h2>
  <div class="grid cols-2 need-tiles">
    ${tile("fenster", us.length, "We hold the answer",
           "a price, a date, what an instruction meant")}
    ${tile("supplier", them.length, "Somebody outside holds it",
           "a lead time, a delivery, a spec")}
  </div>
  <div class="glass need-list" id="need-list" ${needOpen ? "" : "hidden"}></div>`;
}

function needRow(d) {
  return `<div class="row click" data-open-need="${d.id}">
    <span class="t">${esc(d.question)}</span>
    <span class="m">${esc(d.entity_key || "-")}</span>
    <span class="m">${esc(d.raised_by)}</span>
    <span class="m">${rel(d.ts)}</span>
  </div>`;
}

function paintNeedList() {
  const box = $("#need-list");
  if (!box) return;
  box.hidden = !needOpen;
  if (!needOpen) return;
  const rows = NEEDS.filter((d) => (needOpen === "supplier")
    ? d.source === "supplier" : d.source !== "supplier");
  box.innerHTML = rows.map(needRow).join("") || `<div class="empty">Nothing here.</div>`;
  $$("[data-open-need]", box).forEach((r) =>
    r.onclick = () => openNeed(+r.dataset.openNeed));
}

function wireNeeds(list, reload) {
  NEEDS = list;
  needReload = reload;
  $$("[data-need]").forEach((b) => b.onclick = () => {
    needOpen = needOpen === b.dataset.need ? null : b.dataset.need;
    $$("[data-need]").forEach((x) => {
      x.classList.toggle("open", x.dataset.need === needOpen);
      $(".chev", x).textContent = x.dataset.need === needOpen ? "▾" : "›";
    });
    paintNeedList();
  });
  paintNeedList();
}

let needReload = () => {};

/* The whole thing, with room to read it. */
function openNeed(id) {
  const d = NEEDS.find((x) => x.id === id);
  if (!d) return;
  const supplier = d.source === "supplier";
  openDrawer(`
    <h1>${esc(d.question)}</h1>
    <div class="sub">
      <span class="pill ${supplier ? "amber" : "blue"}">${supplier ? "ask the supplier" : "we hold the answer"}</span>
      · raised by ${esc(d.raised_by)} ${rel(d.ts)}
      ${d.entity_key ? `· <a href="#" id="need-job">${esc(d.entity_key)}</a>` : ""}
    </div>
    ${d.context ? `<h2>The detail</h2><div class="position prose">${md(d.context)}</div>` : ""}
    <h2>${supplier ? "What you found out" : "Your answer"}</h2>
    <div class="sub" style="margin-bottom:8px">${supplier
      ? "Somebody has to ask them. Put what they said here and it goes back to "
        + esc(d.raised_by) + " as a task."
      : "It goes straight into " + esc(d.raised_by) + "'s queue as a task."}</div>
    <textarea id="need-answer" rows="4" placeholder="${supplier
      ? "e.g. AFS confirmed 3 weeks from Rev C sign-off"
      : "e.g. reissue it, and tell Stepnell why"}"></textarea>
    <div style="display:flex;gap:8px;margin-top:10px">
      <button class="btn" id="need-send">Answer</button>
      <button class="btn ghost" id="need-cancel">Close</button>
    </div>`);
  const job = $("#need-job");
  if (job) job.onclick = (e) => {
    e.preventDefault();
    (d.entity_type === "contract" ? openContract : d.entity_type === "company"
      ? openCompany : openLead)(d.entity_key);
  };
  $("#need-cancel").onclick = () => ($("#drawer").hidden = true);
  const send = async () => {
    const v = $("#need-answer").value.trim();
    if (!v) return;
    await post("/decision/answer", { id: d.id, answer: v, by: whoAmI() });
    toast("Answered - it is in their queue");
    $("#drawer").hidden = true;
    needReload();
  };
  $("#need-send").onclick = send;
  $("#need-answer").onkeydown = (e) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) send();
  };
  $("#need-answer").focus();
}

/* ---------------------------------------------------------------- routing */
const VIEWS = { today: vToday, live: vLive, mary: vDesk, jacob: vDesk, joseph: vDesk,
  delivery: vDelivery, activity: vActivity, cost: vCost };
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
const PROJECT_BTN = { mary: { kind: "pricing", label: "Work on pricing engine" },
                      jacob: { kind: "leads", label: "Find leads" } };
async function vToday() {
  const ov = await api("/overview");
  const projects = await api("/projects").catch(() => ({}));
  const decisions = ov.decisions || [];
  const cost = ov.cost_today || {};
  const fromUs = decisions.filter((d) => d.source !== "supplier");
  const fromThem = decisions.filter((d) => d.source === "supplier");
  const needs = decisions.length;

  const deskCard = (p) => {
    const st = (ov.statuses || {})[p] || {};
    const n = (ov.task_counts || []).filter((r) => r.assignee === p).reduce((a, r) => a + r.n, 0);
    const working = (ov.working || []).find((w) => w.assignee === p);
    const evs = (ov.desk_events || []).filter((e) => e.author === p).slice(0, 3);
    const sess = (ov.last_sessions || []).find((s) => s.persona === p);
    const myDec = decisions.filter((d) => d.raised_by === p).length;
    const proj = projects[p];
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
      </div>
      <div class="lately">${evs.map((e) => `<div class="ev tight">
        <span class="ts">${rel(e.ts)}</span>
        <span class="b">${esc(e.kind)}${e.entity_key ? " · " + esc(e.entity_key) : ""} — ${esc(e.body.slice(0, 80))}</span>
      </div>`).join("") || `<div class="empty tightpad">Nothing done yet.</div>`}</div>
      <div style="font-size:11.5px;color:var(--ink-3);border-top:1px solid var(--line);padding-top:8px">
        ${sess ? `last session ${rel(sess.ts)} · ${fmtTok(sess.context_tokens)} · ${sess.calls} calls`
               : "no sessions yet"}</div>
      ${PROJECT_BTN[p] ? (proj
        ? `<button class="btn small ghost proj-stop" data-p="${p}">
             ${esc(PROJECT_BTN[p].label)} · until ${hhmm(proj.until)} — stop</button>`
        : `<button class="btn small proj-go" data-p="${p}">${esc(PROJECT_BTN[p].label)}</button>`) : ""}
    </div>`;
  };

  const msgs = (ov.messages || []).slice(0, 6);
  view.innerHTML = `
  <h1>Today</h1>
  <div class="sub">${new Date().toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" })}
    — three desks, ${needs ? needs + " thing" + (needs > 1 ? "s" : "") + " waiting on you" : "nothing waiting on you"}.</div>

  <div class="grid cols-3" style="align-items:start">${Object.keys(PEOPLE).map(deskCard).join("")}</div>

  ${needTiles(decisions, "today")}

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
  wire();
  $$(".proj-go").forEach((b) => b.onclick = async (e) => {
    e.stopPropagation();
    const p = b.dataset.p, cfg = PROJECT_BTN[p];
    await post("/project", { persona: p, kind: cfg.kind, label: cfg.label, minutes: 60 });
    toast(`${cfg.label} — ${p} will keep at it for an hour`);
    vToday();
  });
  $$(".proj-stop").forEach((b) => b.onclick = async (e) => {
    e.stopPropagation();
    await post("/project", { persona: b.dataset.p, minutes: 0 });
    toast("Stopped"); vToday();
  });
  wireNeeds(decisions, vToday);
  refreshBadges(ov, decisions);
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
  const us = open.filter((x) => x.source !== "supplier");
  const them = open.filter((x) => x.source === "supplier");
  const n = open.length;
  if (!n && !extra) return "";
  // No heading here - needTiles writes its own, and two "NEEDS YOU" stacked on
  // top of each other is what the desk page was showing.
  return `${extra}${needTiles(open, "desk")}`;
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
  wireNeeds((d.decisions || []).filter((x) => x.status === "open"), () => vDesk(p));
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

/* ---------------------------------------------------------------- LIVE
   What the bots are doing RIGHT NOW - their thinking, every tool call, every
   result - streamed out of the session transcripts as they are written.
   Zac: "i want to see everything going on as if it was a claude session in
   the desktop app." */
let liveTimer = null, liveSince = 0, liveWho = "";
const LIVE_EVERY = 2500;

async function vLive() {
  liveSince = 0; liveWho = "";
  view.innerHTML = `
  <h1>Live</h1>
  <div class="sub">Every session as it happens — thinking, tool calls and results,
    straight from the transcript. Updates on its own.</div>
  <div class="filter-bar" id="live-chips">
    ${["", "mary", "jacob", "joseph"].map((w) =>
      `<button class="chip ${w === "" ? "on" : ""}" data-who="${w}">${w || "everyone"}</button>`).join("")}
    <label class="live-follow"><input type="checkbox" id="live-follow" checked> follow</label>
    <span class="live-dot" id="live-dot"></span>
  </div>
  <div class="glass stream" id="stream"><div class="empty">Waiting for a session…</div></div>`;

  $$("#live-chips .chip").forEach((c) => c.onclick = () => {
    liveWho = c.dataset.who; liveSince = 0;
    $$("#live-chips .chip").forEach((x) => x.classList.toggle("on", x === c));
    $("#stream").innerHTML = "";
    tick();
  });
  clearInterval(liveTimer);
  liveTimer = setInterval(() => { if (current === "live") tick(); else clearInterval(liveTimer); },
    LIVE_EVERY);
  tick();
}

function traceRow(r) {
  const time = (r.ts || "").slice(11, 19);
  const who = `<span class="who ${esc(r.persona)}">${esc(r.persona)}</span>`;
  if (r.kind === "start" || r.kind === "end")
    return `<div class="tr mark ${r.kind}"><span class="tt">${time}</span>${who}
      <span class="tb">${r.kind === "start" ? "▶ started" : "■ "}${esc(r.body)}${
        r.entity_key ? " · " + esc(r.entity_key) : ""}</span></div>`;
  if (r.kind === "thinking")
    return `<div class="tr think"><span class="tt">${time}</span>${who}
      <span class="tb">${esc(r.body)}</span></div>`;
  if (r.kind === "tool")
    return `<div class="tr tool"><span class="tt">${time}</span>${who}
      <span class="tname">${esc(r.tool)}</span><span class="tb mono">${esc(r.body)}</span></div>`;
  if (r.kind === "result")
    return `<div class="tr res"><span class="tt">${time}</span>${who}
      <span class="tb mono">${esc(r.body)}</span></div>`;
  return `<div class="tr say"><span class="tt">${time}</span>${who}
    <span class="tb">${esc(r.body)}</span></div>`;
}

async function tick() {
  let rows;
  try { rows = await api(`/trace?since=${liveSince}&persona=${liveWho}`); }
  catch { return; }
  const dot = $("#live-dot");
  if (!rows.length) { if (dot) dot.classList.remove("on"); return; }
  liveSince = Math.max(...rows.map((r) => r.id));
  const box = $("#stream");
  if (!box) return;
  if ($(".empty", box)) box.innerHTML = "";
  const nearBottom = box.scrollHeight - box.scrollTop - box.clientHeight < 120;
  box.insertAdjacentHTML("beforeend", rows.map(traceRow).join(""));
  while (box.children.length > 400) box.removeChild(box.firstChild);
  if (dot) { dot.classList.add("on"); setTimeout(() => dot.classList.remove("on"), 1200); }
  const follow = $("#live-follow");
  if (follow && follow.checked && nearBottom) box.scrollTop = box.scrollHeight;
}

/* ---------------------------------------------------------------- ACTIVITY */
let feedTimer = null;
async function vActivity() {
  let evs = await api("/feed?limit=250");
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
  // Keeps itself current, without losing your filter or your scroll position.
  clearInterval(feedTimer);
  feedTimer = setInterval(async () => {
    if (current !== "activity") return clearInterval(feedTimer);
    try {
      const fresh = await api("/feed?limit=250");
      if (fresh.length && (!evs.length || fresh[0].id !== evs[0].id)) { evs = fresh; render(); }
    } catch { /* leave what is on screen */ }
  }, 8000);
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
      <div class="position prose">${md(l.position)}</div>` : ""}
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
    ${co.position ? `<h2>Position</h2><div class="position prose">${md(co.position)}</div>` : ""}
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
    ${ct.position ? `<h2>Position</h2><div class="position prose">${md(ct.position)}</div>` : ""}
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
async function refreshBadges(ov, decisions) {
  try {
    ov = ov || await api("/overview");
    decisions = decisions || ov.decisions || [];
    Object.keys(PEOPLE).forEach((p) => {
      const n = decisions.filter((d) => d.raised_by === p).length;
      const el = $(`[data-badge="${p}"]`);
      if (el) { el.textContent = n || ""; el.classList.toggle("on", !!n); }
    });
  } catch { /* badges are decoration; never break the page for them */ }
}

/* ---------------------------------------------------------------- login
   ONE form, two steps. You type your name, the hub works out whether you
   still need to set a password, and shows you the right fields. The first
   version made you find "first time" in small print at the bottom - which
   was the ONLY usable route, since nobody had a password yet. */
const shell = (inner) => {
  document.body.classList.add("signed-out");
  $("#shell").innerHTML = `
  <div class="signin"><div class="glass card signin-card">
    <div class="brand" style="padding-bottom:16px">
      <svg viewBox="0 0 32 32" class="brand-mark"><path d="M16 3 3 13v16h26V13z"
        fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M16 3v26M3 13h26" stroke="currentColor" stroke-width="1.5"/></svg>
      <div class="brand-name">Glasshouse<span>Fenster Glazing</span></div>
    </div>${inner}
  </div></div>`;
};
const enterFires = (ids, fn) => ids.forEach((id) => {
  const el = $("#" + id);
  if (el) el.onkeydown = (e) => { if (e.key === "Enter") { e.preventDefault(); fn(); } };
});
const signedIn = (d) => {
  localStorage.gh_token = d.token;
  ME = { name: d.name, display: d.display, role: d.role };
  boot();
};

function renderLogin(msg = "", prefill = "") {
  shell(`
    ${msg ? `<div class="signin-msg">${esc(msg)}</div>` : ""}
    <label for="li-name">Your name</label>
    <input type="text" id="li-name" autocomplete="username" autocapitalize="none"
      spellcheck="false" placeholder="e.g. paul" value="${esc(prefill)}">
    <button class="btn" id="li-go" style="width:100%;margin-top:16px">Continue</button>
    <div class="signin-alt">First time here? Type your name and we will ask for
      the setup code you were given.</div>`);
  const go = async () => {
    const name = $("#li-name").value.trim().toLowerCase();
    if (!name) return;
    $("#li-go").textContent = "…";
    try {
      const r = await fetch("/api/start", { method: "POST",
        headers: { "content-type": "application/json" }, body: JSON.stringify({ name }) });
      const d = await r.json();
      (d.mode === "setup" ? renderSetup : renderPassword)(name, d.display || name);
    } catch { renderLogin("Could not reach the hub", name); }
  };
  $("#li-go").onclick = go;
  enterFires(["li-name"], go);
  $("#li-name").focus();
}

function renderPassword(name, display, msg = "") {
  shell(`
    ${msg ? `<div class="signin-msg">${esc(msg)}</div>` : ""}
    <div class="signin-who">Signing in as <b>${esc(display)}</b>
      <a href="#" id="li-back">not you?</a></div>
    <label for="li-pass">Password</label>
    <input type="password" id="li-pass" autocomplete="current-password">
    <button class="btn" id="li-go" style="width:100%;margin-top:16px">Sign in</button>`);
  const go = async () => {
    try {
      const r = await fetch("/api/login", { method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ name, password: $("#li-pass").value }) });
      const d = await r.json();
      if (!r.ok) return renderPassword(name, display, d.error || "That did not work");
      signedIn(d);
    } catch { renderPassword(name, display, "Could not reach the hub"); }
  };
  $("#li-go").onclick = go;
  $("#li-back").onclick = (e) => { e.preventDefault(); renderLogin(); };
  enterFires(["li-pass"], go);
  $("#li-pass").focus();
}

function renderSetup(name, display, msg = "") {
  shell(`
    ${msg ? `<div class="signin-msg">${esc(msg)}</div>` : ""}
    <div class="signin-who">Welcome, <b>${esc(display)}</b>
      <a href="#" id="li-back">not you?</a></div>
    <div class="signin-note">You have not set a password yet. Enter the one-off
      setup code you were given, then choose a password only you know.</div>
    <label for="li-code">Setup code</label>
    <input type="text" id="li-code" inputmode="numeric" autocomplete="one-time-code"
      placeholder="6 digits">
    <label for="li-pass">Choose a password <span class="hint2">8 characters or more</span></label>
    <input type="password" id="li-pass" autocomplete="new-password">
    <button class="btn" id="li-go" style="width:100%;margin-top:16px">Set my password</button>`);
  const go = async () => {
    try {
      const r = await fetch("/api/setup", { method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ name, code: $("#li-code").value.trim(),
          password: $("#li-pass").value }) });
      const d = await r.json();
      if (!r.ok) return renderSetup(name, display, d.error || "That did not work");
      signedIn(d);
    } catch { renderSetup(name, display, "Could not reach the hub"); }
  };
  $("#li-go").onclick = go;
  $("#li-back").onclick = (e) => { e.preventDefault(); renderLogin(); };
  enterFires(["li-code", "li-pass"], go);
  $("#li-code").focus();
}

/* ---------------------------------------------------------------- delivery
   ONE CARD PER JOB, and every field on it is editable by the person doing the
   work. The first version listed steps across all jobs, so Steve saw four
   identical "book installation" boxes and asked "what the fuck is this?", then
   "how do i edit it?". Both were fair: he thinks in jobs, and a board the
   fitters cannot correct is exactly how AdminBase died. */
async function vDelivery() {
  const d = await api("/delivery");
  const admin = ME.role === "admin";
  const t = today();

  // A step reads as a line. The inputs only appear when you ask for them, so
  // the page is a checklist you scan, not a wall of empty boxes.
  const stepLine = (job, s) => {
    const done = !!s.done_at;
    const late = !done && s.due && s.due < t;
    const dueSoon = !done && s.due === t;
    return `<div class="jstep ${done ? "is-done" : ""} ${late ? "is-late" : ""}"
      data-job="${esc(job.key)}" data-n="${s.n}">
      <div class="jstep-row">
        <button class="tick" title="${done ? "Un-tick" : "Mark done"}">${done ? "✓" : ""}</button>
        <span class="jstep-label">${s.n}. ${esc(s.label)}</span>
        ${done
          ? `<span class="jstep-by">done ${esc((s.done_at || "").slice(0, 10))}${
              s.done_by ? " · " + esc(s.done_by) : ""}</span>`
          : `<span class="jstep-due ${late ? "late" : dueSoon ? "soon" : ""}">${
              s.due ? (late ? "LATE " : dueSoon ? "TODAY " : "due ") + esc(s.due) : "no date"}</span>`}
        <button class="edit" title="Edit this step">✎</button>
      </div>
      ${s.detail ? `<div class="jstep-spec">${esc(s.detail)}</div>` : ""}
      <div class="jstep-edit" hidden>
        <label>Due<input type="date" class="d-due" value="${esc(s.due || "")}"></label>
        <label class="wide">What exactly
          <input type="text" class="d-detail" placeholder="sizes, spec, supplier…"
            value="${esc(s.detail || "")}"></label>
      </div>
    </div>`;
  };

  // The list. Closed by default - you open the job you are working on.
  const jobCard = (job) => `
    <section class="glass job" data-job="${esc(job.key)}">
      <button class="job-head" aria-expanded="false">
        <span class="chev">›</span>
        <span class="job-id">
          <span class="job-title">${esc(job.title)}</span>
          <span class="job-sub">${esc(job.company_name || job.company_key)}${
            job.value ? " · " + gbp(job.value) : ""}</span>
        </span>
        <span class="job-meta">
          ${job.late ? `<span class="pill red">${job.late} late</span>` : ""}
          <span class="pill">${job.done}/${job.total} done</span>
          <span class="job-when">${job.site_date ? "on site " + esc(job.site_date) : "no site date"}</span>
        </span>
      </button>
      <div class="job-body" hidden>
        <div class="job-bar">
          <label class="job-site">On site
            <input type="date" class="d-site" value="${esc(job.site_date || "")}"></label>
          <div class="job-prog">
            <div class="progress"><i style="width:${job.total ? Math.round(100 * job.done / job.total) : 0}%"></i></div>
            <span>${job.done} of ${job.total} done${job.po_ref ? " · PO " + esc(job.po_ref) : ""}</span>
          </div>
        </div>
        <div class="jsteps">${job.steps.map((s) => stepLine(job, s)).join("")
          || `<div class="empty">No checklist on this job yet.</div>`}</div>
        <div class="job-notes">
          ${job.notes.slice(0, 3).map((n) => `<div class="jnote"><b>${esc(n.author)}</b>
            <span>${rel(n.ts)}</span>${esc(n.body)}</div>`).join("")}
          <div class="jnote-add">
            <input type="text" class="d-note" placeholder="Add a note — what happened, what changed…">
            <button class="btn small">Save note</button>
          </div>
        </div>
      </div>
    </section>`;

  const c = d.counts || {};
  view.innerHTML = `
  <h1>${admin ? "Site" : "Your jobs"}</h1>
  <div class="sub">${new Date().toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" })}
    — ${admin ? "exactly what Paul and Steve see. Everything here is editable by them."
      : esc(ME.display) + ". One card per job. Tick things off, set the dates, write down what happened."}</div>

  <div class="grid cols-4" style="margin-bottom:18px">
    <div class="glass stat ${c.late ? "bad" : "good"}"><div class="n">${c.late || 0}</div><div class="l">late</div></div>
    <div class="glass stat ${c.today ? "warn" : ""}"><div class="n">${c.today || 0}</div><div class="l">due today</div></div>
    <div class="glass stat"><div class="n">${c.week || 0}</div><div class="l">due this week</div></div>
    <div class="glass stat"><div class="n">${(d.jobs || []).length}</div><div class="l">live jobs</div></div>
  </div>

  ${!c.late && !c.today && !c.week && (d.jobs || []).length ? `
    <div class="glass card" style="margin-bottom:16px;border-color:var(--amber)">
      <b>Nothing has a date yet, so nothing can be late or due.</b>
      <div class="sub" style="margin:4px 0 0">Set <b>On site</b> on a job and put dates against its
      steps and this page starts telling you what to do and when. Anyone here can set them.</div>
    </div>` : ""}

  ${(d.jobs || []).map(jobCard).join("")
    || `<div class="glass card empty">No live jobs. One starts when a purchase order lands.</div>`}`;

  // --- everything below is the editing. Save on change, no Save button to forget.
  const save = async (path, payload, msg) => {
    try { await post(path, payload); if (msg) toast(msg); }
    catch { /* post() has already said so */ }
  };
  $$(".job").forEach((el) => {
    const key = el.dataset.job;
    const head = $(".job-head", el), bodyEl = $(".job-body", el);
    head.onclick = () => {
      const open = !bodyEl.hidden;
      bodyEl.hidden = open;
      el.classList.toggle("open", !open);
      head.setAttribute("aria-expanded", String(!open));
      if (!open) openJobs.add(key); else openJobs.delete(key);
    };
    if (openJobs.has(key)) head.click();   // survive a re-render after saving

    $(".d-site", el).onchange = (e) =>
      save("/jobsite", { key, site_date: e.target.value }, "Site date saved");
    const noteBtn = $(".jnote-add .btn", el), noteInput = $(".d-note", el);
    const addNote = async () => {
      const body = noteInput.value.trim();
      if (!body) return;
      await save("/jobnote", { key, body }, "Note saved");
      vDelivery();
    };
    noteBtn.onclick = addNote;
    noteInput.onkeydown = (e) => { if (e.key === "Enter") { e.preventDefault(); addNote(); } };
  });
  $$(".jstep").forEach((el) => {
    const contract_key = el.dataset.job, n = +el.dataset.n;
    $(".tick", el).onclick = async () => {
      const done = el.classList.contains("is-done");
      await save(done ? "/step/undone" : "/step/done", { contract_key, n },
        done ? "Un-ticked" : "Ticked");
      vDelivery();
    };
    $(".edit", el).onclick = () => {
      const box = $(".jstep-edit", el);
      box.hidden = !box.hidden;
      el.classList.toggle("editing", !box.hidden);
      if (!box.hidden) { const f = $("input", box); if (f) f.focus(); }
    };
    const due = $(".d-due", el);
    if (due) due.onchange = (e) =>
      save("/step/set", { contract_key, n, due: e.target.value }, "Date saved");
    const det = $(".d-detail", el);
    if (det) det.onchange = async (e) => {
      await save("/step/set", { contract_key, n, detail: e.target.value }, "Saved");
      vDelivery();
    };
  });
}
// Which jobs the user had open, so saving something does not close them all.
const openJobs = new Set();

/* ---------------------------------------------------------------- boot */
async function boot() {
  document.body.classList.remove("signed-out");
  $("#shell").innerHTML = SHELL_HTML;
  view = $("#view");
  const isAdmin = ME.role === "admin";
  if (!isAdmin) {
    // Delivery sees one page. No desks, no decisions, no cost.
    $("#rail").innerHTML = `
      <div class="brand"><svg viewBox="0 0 32 32" class="brand-mark">
        <path d="M16 3 3 13v16h26V13z" fill="none" stroke="currentColor" stroke-width="2.5"
          stroke-linejoin="round"/><path d="M16 3v26M3 13h26" stroke="currentColor"
          stroke-width="1.5"/></svg>
        <div class="brand-name">Glasshouse<span>${esc(ME.display)}</span></div></div>
      <div class="nav"><button class="active"><span class="ic">✓</span>Your day</button></div>
      <div class="rail-foot"><button id="sign-out" class="btn small ghost">Sign out</button></div>`;
    $("#sign-out").onclick = signOut;
    await vDelivery();
    return;
  }
  wireChrome();
  await show("today");
  refreshBadges();
}

let SHELL_HTML = "";
function wireChrome() {
  $$("#rail .nav button").forEach((b) => (b.onclick = () => show(b.dataset.view)));
  const so = $("#sign-out");
  if (so) so.onclick = signOut;
  $("#theme-toggle").onclick = toggleTheme;
}
function toggleTheme() {
  const cur = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = cur;
  localStorage.theme = cur;
};
// Light unless somebody pressed the toggle. The browser's own dark-mode
// setting is deliberately ignored - it was turning Paul's job sheets dark.
if (localStorage.theme === "dark") document.documentElement.dataset.theme = "dark";
setInterval(() => {
  const c = $("#clock");
  if (c) c.textContent = new Date().toLocaleTimeString("en-GB",
    { hour: "2-digit", minute: "2-digit" });
}, 1000);
setInterval(() => { if (ME && ME.role === "admin" && current === "today")
  vToday().catch(() => {}); }, 60000);

/* Keep the signed-in shell so it can be restored after a sign-out, then
   decide which hub this person gets. */
SHELL_HTML = $("#shell").innerHTML;
(async () => {
  if (!localStorage.gh_token) return renderLogin();
  try {
    ME = await api("/me");
    await boot();
  } catch { renderLogin(); }
})();
