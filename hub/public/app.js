/* GLASSHOUSE — the app. Vanilla JS, no build step.
   Reads are open; every write that steers a bot asks for the team PIN once
   and keeps it locally — that is the sender check, kept because it worked. */

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const view = $("#view");

const STAGES = ["new", "acknowledged", "materials_out", "awaiting_costs", "quote_ready",
  "pre_quote_call", "quote_sent", "follow_up", "final_follow_up"];
const STAGE_LABEL = {
  new: "New", acknowledged: "Acknowledged", materials_out: "Materials out",
  awaiting_costs: "Awaiting costs", quote_ready: "Quote ready",
  pre_quote_call: "Pre-quote call", quote_sent: "Quote sent",
  follow_up: "Follow-up", final_follow_up: "Final follow-up", closed: "Closed",
};
const PERSONAS = { mary: "Estimating", jacob: "Business development", joseph: "Project management" };

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const gbp = (v) => v == null || v === "" ? "" :
  "£" + Number(v).toLocaleString("en-GB", { maximumFractionDigits: 0 });
const fmtTok = (n) => n >= 1e6 ? (n / 1e6).toFixed(1) + "M" : n >= 1e3 ? (n / 1e3).toFixed(0) + "k" : String(n || 0);
const today = () => new Date().toISOString().slice(0, 10);
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
    const pin = prompt("Team PIN (this is the sender check — it proves the instruction comes from you):");
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

/* ---------------------------------------------------------------- views */
const VIEWS = { today: vToday, pipeline: vPipeline, companies: vCompanies,
  contracts: vContracts, team: vTeam, activity: vActivity, cost: vCost };
let current = "today";

async function show(name) {
  current = name;
  $$("#rail .nav button").forEach((b) => b.classList.toggle("active", b.dataset.view === name));
  view.innerHTML = `<div class="empty">Loading…</div>`;
  try { await VIEWS[name](); } catch (e) {
    view.innerHTML = `<div class="glass card">The hub could not load <b>${esc(name)}</b>: ${esc(e.message)}</div>`;
  }
}

/* ------------------------------------------------ today */
async function vToday() {
  const [ov, td] = await Promise.all([api("/overview"), api("/today")]);
  const open = ov.decisions || [];
  const cost = ov.cost_today || {};
  const taskN = (ov.task_counts || []).reduce((a, r) => a + r.n, 0);
  const pipeVal = (ov.pipeline || []).reduce((a, r) => a + (r.v || 0), 0);

  view.innerHTML = `
  <h1>Today</h1>
  <div class="sub">${new Date().toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" })} — the whole company under one roof of glass.</div>

  <div class="grid cols-4">
    <div class="glass stat ${open.length ? "warn" : "good"}"><div class="n">${open.length}</div><div class="l">need a human</div></div>
    <div class="glass stat"><div class="n">${taskN}</div><div class="l">tasks in the queue</div></div>
    <div class="glass stat"><div class="n">${gbp(pipeVal) || "£0"}</div><div class="l">open pipeline ex VAT</div></div>
    <div class="glass stat"><div class="n">${fmtTok(cost.c || 0)}</div><div class="l">context tokens today (${cost.n || 0} sessions)</div></div>
  </div>

  ${open.length ? `<h2>Needs a human — answer in place</h2><div class="grid">${open.map(dDecision).join("")}</div>` : ""}

  <h2>Calls due today</h2>
  <div class="glass">${rows(td.due, "Nothing lands today.")}</div>

  ${td.overdue?.length ? `<h2>Overdue — worst first, work these down</h2><div class="glass">${rows(td.overdue)}</div>` : ""}

  <h2>Deadlines this week</h2>
  <div class="glass">${rows(td.deadlines, "No tender deadlines inside seven days.", "deadline")}</div>

  <h2>The desks</h2>
  <div class="grid cols-3">${Object.keys(PERSONAS).map((p) => {
    const st = (ov.statuses || {})[p] || {};
    const n = (ov.task_counts || []).filter((r) => r.assignee === p).reduce((a, r) => a + r.n, 0);
    return `<div class="glass card persona-mini" style="cursor:pointer" onclick="show('team')">
      <header style="display:flex;gap:10px;align-items:center">
        <div class="avatar ${p}">${p[0].toUpperCase()}</div>
        <div><div class="name">${p[0].toUpperCase() + p.slice(1)}</div>
        <div class="role">${PERSONAS[p]}</div></div>
        <span class="pill ${st.state === "working" ? "green" : ""}" style="margin-left:auto">${st.state || "offline"}</span>
      </header>
      <div class="sub" style="margin:8px 0 0">${n} open task${n === 1 ? "" : "s"}${st.detail ? " — " + esc(st.detail) : ""}</div>
    </div>`; }).join("")}
  </div>`;
  wireDecisions();
  wireRows();
}

function dDecision(d) {
  return `<div class="glass decision" data-id="${d.id}">
    <div class="q">${esc(d.question)}</div>
    ${d.context ? `<div class="ctx">${esc(d.context)}</div>` : ""}
    <div class="who">raised by ${esc(d.raised_by)} · ${rel(d.ts)}${d.entity_key ? " · " + esc(d.entity_key) : ""}</div>
    <div class="answer-box"><input type="text" placeholder="Your answer — it lands straight in ${esc(d.raised_by)}'s queue">
    <button class="btn">Answer</button></div>
  </div>`;
}
function wireDecisions() {
  $$(".decision").forEach((el) => {
    const send = async () => {
      const val = $("input", el).value.trim();
      if (!val) return;
      await post("/decision/answer", { id: +el.dataset.id, answer: val, by: whoAmI() });
      toast("Answered — it is in the queue");
      show(current);
    };
    $(".btn", el).onclick = send;
    $("input", el).onkeydown = (e) => e.key === "Enter" && send();
  });
}

function rows(list, empty = "Nothing.", dateField = "next_action_date") {
  if (!list || !list.length) return `<div class="empty">${empty}</div>`;
  return list.map((l) => {
    const late = l[dateField] && l[dateField] < today();
    return `<div class="row" data-lead="${esc(l.key)}">
      <span class="t">${esc(l.title)}</span>
      <span class="m">${esc(STAGE_LABEL[l.stage] || l.stage)}</span>
      <span class="m ${late ? "late" : ""}" style="${late ? "color:var(--red)" : ""}">${esc(l[dateField] || "")}</span>
      <span class="v">${gbp(l.value)}</span>
    </div>`;
  }).join("");
}
function wireRows() { $$("[data-lead]").forEach((r) => r.onclick = () => openLead(r.dataset.lead)); }

/* ------------------------------------------------ pipeline */
async function vPipeline() {
  const p = await api("/pipeline");
  const byStage = {};
  (p.open || []).forEach((l) => (byStage[l.stage] ||= []).push(l));
  view.innerHTML = `
  <h1>Pipeline</h1>
  <div class="sub">Every open lead, Mary's half then Jacob's. Click a card for the record. Values ex VAT.</div>
  <div class="board">${STAGES.map((s) => {
    const ls = byStage[s] || [];
    const sum = ls.reduce((a, l) => a + (l.value || 0), 0);
    return `<div class="col glass"><h3>${STAGE_LABEL[s]}<span class="sum">${ls.length ? gbp(sum) : ""}</span></h3>
      ${ls.map(leadCard).join("") || `<div class="empty" style="padding:8px 14px">—</div>`}
    </div>`; }).join("")}
  </div>
  <h2>Recently closed</h2>
  <div class="glass">${(p.closed || []).map((l) => `
    <div class="row" data-lead="${esc(l.key)}">
      <span class="t">${esc(l.title)}</span>
      <span class="pill ${l.outcome === "won" ? "green" : l.outcome === "lost" ? "red" : ""}">${esc(l.outcome || "closed")}</span>
      <span class="v">${gbp(l.value)}</span>
    </div>`).join("") || `<div class="empty">Nothing closed yet.</div>`}
  </div>`;
  $$(".lead-card").forEach((c) => c.onclick = () => openLead(c.dataset.lead));
  wireRows();
}
function leadCard(l) {
  const late = l.deadline && l.deadline < today() && l.stage !== "quote_sent";
  return `<div class="lead-card" data-lead="${esc(l.key)}">
    <div class="t">${esc(l.title)}</div>
    <div class="c">${esc(l.company_name || l.company_key)}</div>
    <div class="foot"><span class="val">${gbp(l.value)}</span>
    <span class="due ${late ? "late" : ""}">${esc(l.deadline || l.next_action_date || "")}</span></div>
  </div>`;
}

/* ------------------------------------------------ companies */
async function vCompanies() {
  const cs = await api("/companies");
  view.innerHTML = `
  <h1>Companies</h1>
  <div class="sub">${cs.length} on record. Lifetime values ex VAT.</div>
  <div class="filter-bar"><input type="text" id="co-filter" placeholder="Filter…"></div>
  <div class="glass" id="co-list">${cs.map(coRow).join("") || `<div class="empty">None yet.</div>`}</div>`;
  const wire = () => $$("[data-co]").forEach((r) => r.onclick = () => openCompany(r.dataset.co));
  wire();
  $("#co-filter").oninput = (e) => {
    const q = e.target.value.toLowerCase();
    $("#co-list").innerHTML = cs.filter((c) => (c.name + c.key).toLowerCase().includes(q)).map(coRow).join("")
      || `<div class="empty">No match.</div>`;
    wire();
  };
}
const coRow = (c) => `<div class="row" data-co="${esc(c.key)}">
  <span class="t">${esc(c.name)}</span>
  <span class="pill ${c.relationship === "won" ? "green" : c.relationship === "quoted" ? "blue" : ""}">${esc(c.relationship)}</span>
  <span class="m">${c.open_leads ? c.open_leads + " open" : ""}</span>
  <span class="v">${gbp(c.lifetime_value)}</span></div>`;

/* ------------------------------------------------ contracts */
async function vContracts() {
  const cs = await api("/contracts");
  view.innerHTML = `
  <h1>Contracts</h1>
  <div class="sub">Won jobs, purchase order to final payment — Joseph's world.</div>
  <div class="grid cols-2">${cs.map((c) => {
    const doneN = (c.steps_total || 0) - (c.steps_open || 0);
    const pc = c.steps_total ? Math.round(100 * doneN / c.steps_total) : 0;
    return `<div class="glass card" style="cursor:pointer" data-ct="${esc(c.key)}">
      <div style="display:flex;justify-content:space-between;gap:10px">
        <b>${esc(c.title)}</b>
        <span class="pill ${c.status === "live" ? "green" : ""}">${esc(c.status)}</span></div>
      <div class="sub" style="margin:4px 0 0">${esc(c.company_name || c.company_key)}
        · ${gbp(c.value)} · site ${esc(c.site_date || "tbc")}</div>
      <div class="progress"><i style="width:${pc}%"></i></div>
      <div class="sub" style="margin-top:6px">${doneN}/${c.steps_total || 0} steps done</div>
    </div>`; }).join("") || `<div class="glass card empty">No contracts on record yet — the next PO starts one.</div>`}
  </div>`;
  $$("[data-ct]").forEach((c) => c.onclick = () => openContract(c.dataset.ct));
}

/* ------------------------------------------------ team */
async function vTeam() {
  const [ov, msgs] = await Promise.all([api("/overview"), api("/messages")]);
  view.innerHTML = `
  <h1>The team</h1>
  <div class="sub">Three desks. Type to one and it lands in their queue as a trusted instruction — the PIN is the proof it is you.</div>
  <div class="grid cols-3" style="align-items:start">${Object.keys(PERSONAS).map((p) => {
    const st = (ov.statuses || {})[p] || {};
    const thread = (msgs || []).filter((m) => m.persona === p).slice(0, 20).reverse();
    return `<div class="glass persona" data-p="${p}">
      <header><div class="avatar ${p}">${p[0].toUpperCase()}</div>
        <div><div class="name">${p[0].toUpperCase() + p.slice(1)} ${p === "mary" ? "Grace" : p === "jacob" ? "Wright" : "Scott"}</div>
        <div class="role">${PERSONAS[p]}</div></div>
        <span class="state pill ${st.state === "working" ? "green" : ""}">${st.state || "offline"}</span></header>
      <div class="thread">${thread.map((m) => `
        <div class="msg ${m.author === p ? "bot" : "human"}"><div class="who">${esc(m.author)} · ${rel(m.ts)}</div>${esc(m.body)}</div>`).join("")
        || `<div class="empty">No conversation yet.</div>`}</div>
      <div class="composer"><textarea placeholder="Message ${p[0].toUpperCase() + p.slice(1)}…"></textarea>
      <button class="btn">Send</button></div>
    </div>`; }).join("")}
  </div>`;
  $$(".persona").forEach((el) => {
    $(".btn", el).onclick = async () => {
      const body = $("textarea", el).value.trim();
      if (!body) return;
      await post("/message", { persona: el.dataset.p, body, author: whoAmI() });
      toast("Sent — it is in the queue");
      vTeam();
    };
  });
}

/* ------------------------------------------------ activity */
async function vActivity() {
  const evs = await api("/feed?limit=150");
  view.innerHTML = `
  <h1>Activity</h1>
  <div class="sub">The event stream — every fact, by every author, newest first.</div>
  <div class="filter-bar"><input type="text" id="ev-filter" placeholder="Filter (author, kind, text)…"></div>
  <div class="glass feed" id="ev-list"></div>`;
  const render = (q = "") => {
    const list = evs.filter((e) => !q ||
      (e.author + " " + e.kind + " " + e.entity_key + " " + e.body).toLowerCase().includes(q));
    $("#ev-list").innerHTML = list.map((e) => `
      <div class="ev"><span class="ts">${esc(e.ts.slice(5, 16))}</span>
      <span class="k"><span class="pill ${e.kind === "catch" ? "amber" : e.kind.startsWith("mail") ? "blue" : ""}">${esc(e.kind)}</span></span>
      <span class="b"><b>${esc(e.author)}</b>${e.entity_key ? " · " + esc(e.entity_key) : ""} — ${esc(e.body)}</span></div>`).join("")
      || `<div class="empty">Nothing yet.</div>`;
  };
  render();
  $("#ev-filter").oninput = (e) => render(e.target.value.toLowerCase());
}

/* ------------------------------------------------ cost */
async function vCost() {
  const c = await api("/cost");
  const byDay = {};
  (c.days || []).forEach((r) => { (byDay[r.day] ||= {})[r.persona] = r; });
  const days = Object.keys(byDay).sort();
  const max = Math.max(1, ...days.map((d) => Object.values(byDay[d]).reduce((a, r) => a + r.context, 0)));
  const TARGET = 118e6;
  view.innerHTML = `
  <h1>Cost</h1>
  <div class="sub">Context tokens per day — the real meter, deduped per call. Target: ${fmtTok(TARGET)}/day for the whole system.</div>
  <div class="glass">
    <div class="bars">${days.map((d) => {
      const rs = byDay[d];
      const tot = Object.values(rs).reduce((a, r) => a + r.context, 0);
      return `<div class="bar" title="${d}: ${fmtTok(tot)}">
        ${["joseph", "jacob", "mary"].map((p) => rs[p] ?
          `<i class="${p}" style="height:${Math.round(120 * rs[p].context / max)}px"></i>` : "").join("")}
        <span class="d">${d.slice(5)}${tot > TARGET ? " ⚠" : ""}</span></div>`; }).join("")
      || `<div class="empty">No sessions metered yet.</div>`}</div>
    <div class="legend"><span><i style="background:#1f9d5b"></i>Mary</span>
    <span><i style="background:#2470a8"></i>Jacob</span>
    <span><i style="background:#8a5fbf"></i>Joseph</span></div>
  </div>
  <h2>Recent sessions</h2>
  <div class="glass" style="overflow-x:auto"><table>
    <tr><th>when</th><th>persona</th><th>entity</th><th>model</th><th>calls</th><th>context</th><th>secs</th></tr>
    ${(c.recent || []).map((r) => `<tr><td>${esc(r.ts.slice(5, 16))}</td><td>${esc(r.persona)}</td>
      <td>${esc(r.entity_key)}</td><td>${esc((r.model || "").replace("claude-", ""))}</td>
      <td>${r.calls}</td><td>${fmtTok(r.context_tokens)}</td><td>${r.seconds}</td></tr>`).join("")}
  </table></div>`;
}

/* ------------------------------------------------ drawers */
function openDrawer(html) {
  $("#drawer-body").innerHTML = html;
  $("#drawer").hidden = false;
}
$("#drawer-close").onclick = () => ($("#drawer").hidden = true);
$("#drawer").onclick = (e) => { if (e.target.id === "drawer") $("#drawer").hidden = true; };

async function openLead(key) {
  const c = await api("/card/lead/" + encodeURIComponent(key));
  const l = c.lead, co = c.company || {};
  openDrawer(`
    <h1>${esc(l.title)}</h1>
    <div class="sub">${esc(co.name || l.company_key)} · <span class="pill blue">${esc(STAGE_LABEL[l.stage] || l.stage)}</span>
      · owner ${esc(l.owner)}</div>
    <div class="kv">
      <b>Value</b><span>${gbp(l.value) || "—"} ex VAT</span>
      <b>Deadline</b><span>${esc(l.deadline || "—")}</span>
      <b>Award due</b><span>${esc(l.award_due || "—")}</span>
      <b>Next action</b><span>${esc((l.next_action_date || "") + " " + (l.next_action || "—"))}</span>
      ${l.outcome ? `<b>Outcome</b><span>${esc(l.outcome)} ${esc(l.outcome_why || "")}</span>` : ""}
    </div>
    ${["quote_sent", "follow_up", "final_follow_up"].includes(l.stage) ? `
      <div style="display:flex;gap:8px;margin:6px 0 14px">
        <button class="btn small" id="btn-won">Mark WON</button>
        <button class="btn small danger" id="btn-lost">Mark LOST</button>
      </div>` : ""}
    ${(c.quotes || []).length ? `<h2>Quotes</h2>` + c.quotes.map((q) =>
      `<div class="row"><span class="t">r${q.revision} — ${esc(q.status)}</span>
       <span class="m">${esc(q.issued_at || "")}</span><span class="v">${gbp(q.value)}</span></div>`).join("") : ""}
    ${l.position ? `<h2>Position</h2><div class="position">${esc(l.position)}</div>` : ""}
    ${(c.contacts || []).length ? `<h2>Contacts</h2>` + c.contacts.map((ct) =>
      `<div class="row"><span class="t">${esc(ct.name || "?")}</span><span class="m">${esc(ct.email || "")}</span></div>`).join("") : ""}
    <h2>Recent</h2>
    ${(c.recent_events || []).map((e) => `<div class="ev"><span class="ts">${esc(e.ts.slice(5, 16))}</span>
      <span class="b"><b>${esc(e.author)}</b> ${esc(e.kind)} — ${esc(e.body)}</span></div>`).join("") || `<div class="empty">Quiet.</div>`}
  `);
  const outcome = (o) => async () => {
    const why = prompt("Why? (optional, one line)") || "";
    await post("/outcome", { lead_key: key, outcome: o, why, by: whoAmI() });
    toast("Recorded — that data did not exist before you clicked");
    $("#drawer").hidden = true; show(current);
  };
  if ($("#btn-won")) $("#btn-won").onclick = outcome("won");
  if ($("#btn-lost")) $("#btn-lost").onclick = outcome("lost");
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
    ${(c.leads || []).length ? `<h2>Leads</h2>` + c.leads.map((l) =>
      `<div class="row" data-lead="${esc(l.key)}"><span class="t">${esc(l.title)}</span>
       <span class="m">${esc(STAGE_LABEL[l.stage] || l.stage)}</span><span class="v">${gbp(l.value)}</span></div>`).join("") : ""}
    ${(c.contacts || []).length ? `<h2>Contacts</h2>` + c.contacts.map((ct) =>
      `<div class="row"><span class="t">${esc(ct.name || "?")}</span><span class="m">${esc(ct.email || "")}</span>
       <span class="m">${esc(ct.role || "")}</span></div>`).join("") : ""}
    <h2>Recent</h2>
    ${(c.recent_events || []).map((e) => `<div class="ev"><span class="ts">${esc(e.ts.slice(5, 16))}</span>
      <span class="b"><b>${esc(e.author)}</b> ${esc(e.kind)} — ${esc(e.body)}</span></div>`).join("") || `<div class="empty">Quiet.</div>`}
  `);
  $$("#drawer-body [data-lead]").forEach((r) => r.onclick = () => openLead(r.dataset.lead));
}

async function openContract(key) {
  const c = await api("/card/contract/" + encodeURIComponent(key));
  const ct = c.contract;
  openDrawer(`
    <h1>${esc(ct.title)}</h1>
    <div class="sub">${esc((c.company || {}).name || ct.company_key)} ·
      <span class="pill ${ct.status === "live" ? "green" : ""}">${esc(ct.status)}</span>
      · PO ${esc(ct.po_ref || "—")} · ${gbp(ct.value)} · site ${esc(ct.site_date || "tbc")}</div>
    <h2>The twelve steps</h2>
    ${(c.steps || []).map((s) => `<div class="row" style="cursor:default">
      <span class="t" style="${s.done_at ? "text-decoration:line-through;opacity:.55" : ""}">${s.n}. ${esc(s.label)}</span>
      <span class="m">${esc(s.detail || "")}</span>
      <span class="m">${s.done_at ? "done " + esc(s.done_at.slice(0, 10)) : "due " + esc(s.due || "tbc")}</span>
    </div>`).join("") || `<div class="empty">No steps seeded yet.</div>`}
    ${(c.invoices || []).length ? `<h2>Invoices</h2>` + c.invoices.map((i) =>
      `<div class="row"><span class="t">${esc(i.ref || "draft")}</span>
       <span class="pill ${i.status === "paid" ? "green" : i.status === "overdue" ? "red" : ""}">${esc(i.status)}</span>
       <span class="v">${gbp(i.value)}</span></div>`).join("") : ""}
    ${ct.position ? `<h2>Position</h2><div class="position">${esc(ct.position)}</div>` : ""}
    <h2>Recent</h2>
    ${(c.recent_events || []).map((e) => `<div class="ev"><span class="ts">${esc(e.ts.slice(5, 16))}</span>
      <span class="b"><b>${esc(e.author)}</b> ${esc(e.kind)} — ${esc(e.body)}</span></div>`).join("") || `<div class="empty">Quiet.</div>`}
  `);
}

/* ------------------------------------------------ chrome */
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
