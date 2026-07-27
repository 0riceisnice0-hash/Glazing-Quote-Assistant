/* Mary Grace - Fenster Estimating Hub.
   Single-page app over /api/data (deployed state) + /api/messages (D1)
   + /api/status (what her bridge is doing right now).
   Anything written here is picked up by the bridge within seconds and routed
   to that job's own permanent chat, then answered back into this hub. */

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];

let DATA = null;
let MESSAGES = [];
let page = "overview";
let commsTab = "sent";

/* Anything a human has typed but not yet sent. render() throws the whole page
   away and rebuilds it, so without this a background refresh mid-sentence
   wipes what you were writing. Keyed by the textarea's data-draft attribute;
   selected request options and the search term ride along for the same reason. */
const DRAFTS = {};
/* Answers sent from this browser. DATA.requests only flips to "answered" when
   Mary redeploys the board, so without this your reply vanishes the instant you
   send it and the card looks untouched. */
const SENT_ANSWERS = {};
let searchTerm = "";
let msgSig = "";
let STATUS = null;
let OUTCOMES = [];
const signature = (msgs) => msgs.map((m) => `${m.id}:${m.seen_by_mary ? 1 : 0}`).join(",");

/* ---------------- api ---------------- */
async function api(route, options) {
  const res = await fetch(`/api/${route}`, options);
  if (!res.ok) throw Object.assign(new Error("api"), { status: res.status });
  return res.json();
}
const who = () => $("#who").value;

async function sendToMary(body, context = "") {
  await api("messages", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ author: who(), body, context }),
  });
  MESSAGES = await api("messages");
  msgSig = signature(MESSAGES);
  toast(STATUS?.state === "working" ? "Sent - queued, Mary is mid-job right now" : "Sent - Mary picks this up in seconds");
}

/* The live pill in the sidebar: what the bridge is doing this second. */
function renderStatus() {
  const el = $("#mary-state");
  const dot = $("#mary-dot");
  if (!el) return;
  const s = STATUS || {};
  let text = "Live", tone = "";
  if (s.state === "working") {
    // Job names get long ("Air Separation Unit, Vesuvius Way Worksop") - trim to
    // something that reads as a sentence, full name in the tooltip.
    const short = String(s.title || "").split(" (")[0].split(",")[0].trim();
    text = short ? `Working on ${short}` : "Working";
    tone = "busy";
  } else if (s.state === "backoff") {
    text = "Paused - retrying shortly";
    tone = "stalled";
  } else if (s.queue_depth > 0) {
    text = `${s.queue_depth} queued`;
    tone = "busy";
  }
  el.textContent = text;
  el.title = [s.title, s.detail].filter(Boolean).join(" - ");
  if (dot) dot.className = `dot ${tone}`;
}

function toast(text) {
  const t = $("#toast");
  t.textContent = text;
  t.hidden = false;
  clearTimeout(t._h);
  t._h = setTimeout(() => { t.hidden = true; }, 3200);
}

/* ---------------- rich text ----------------
   Mary writes plain text with conventions (blank lines, ALL-CAPS headers,
   "- " bullets, "1." numbered items). Render it as clean HTML so nothing
   ever looks like a raw text dump. */
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function inline(s) {
  let h = esc(s);
  h = h.replace(/(GBP\s?[\d,]+(?:\.\d\d)?|£[\d,]+(?:\.\d\d)?)/g, '<span class="money">$1</span>');
  return h;
}

function fmt(text) {
  const blocks = String(text || "").trim().split(/\n\s*\n/);
  const out = [];
  for (const block of blocks) {
    const lines = block.split("\n").map((l) => l.trim()).filter(Boolean);
    if (!lines.length) continue;
    const first = lines[0];
    const alpha = first.replace(/[^a-zA-Z]/g, "");
    const isCaps = alpha.length >= 3 && alpha === alpha.toUpperCase() && first.length < 70;
    if (lines.length === 1 && isCaps) {
      out.push(`<h6>${inline(first)}</h6>`);
    } else if (lines.every((l) => /^[-•]\s/.test(l))) {
      out.push(`<ul>${lines.map((l) => `<li>${inline(l.replace(/^[-•]\s/, ""))}</li>`).join("")}</ul>`);
    } else if (/^\d+[.)]\s/.test(first)) {
      out.push(`<div class="item"><strong>${inline(first)}</strong>${lines.slice(1).map((l) => `<div>${inline(l)}</div>`).join("")}</div>`);
    } else {
      out.push(`<p>${lines.map(inline).join("<br>")}</p>`);
    }
  }
  return `<div class="rt">${out.join("")}</div>`;
}

/* ---------------- helpers ---------------- */
const daysUntil = (iso) => Math.ceil((new Date(iso + "T12:00:00") - Date.now()) / 86400000);
function rag(job) {
  if (job.stage === "submitted") return ["ok", "Submitted"];
  const d = daysUntil(job.deadline);
  if (d < 0) return ["danger", `${-d} days overdue`];
  if (d === 0) return ["danger", "Due today"];
  if (d <= 2) return ["danger", `${d} day${d > 1 ? "s" : ""} left`];
  if (d <= 5) return ["warn", `${d} days left`];
  return ["ok", `${d} days left`];
}
const niceDate = (iso) => new Date(iso + "T12:00:00").toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" });
const openReqs = () => (DATA.requests || []).filter((r) => r.status === "open");
/* Still needing a human - one you have already answered is with Mary, not you. */
const awaitingReqs = () => openReqs().filter((r) => !SENT_ANSWERS[r.id]);
const unseenMsgs = () => MESSAGES.filter((m) => m.author !== "mary" && !m.seen_by_mary).length;

/* ---------------- panel ---------------- */
function openPanel(html) { $("#panel-body").innerHTML = html; $("#panel").hidden = false; $("#panel-veil").hidden = false; }
function closePanel() { $("#panel").hidden = true; $("#panel-veil").hidden = true; }
$("#panel-close").addEventListener("click", closePanel);
$("#panel-veil").addEventListener("click", closePanel);
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closePanel(); });

function related(jobName) {
  const words = jobName.toLowerCase().split(" ").filter((w) => w.length > 4);
  const match = (t) => words.some((w) => (t || "").toLowerCase().includes(w));
  return {
    reqs: (DATA.requests || []).filter((r) => match(r.job)),
    catches: DATA.catches.filter((c) => match(c.job)),
    emails: DATA.emails.filter((e) => match(e.subject)),
    inbox: (DATA.inbox || []).filter((i) => match(i.subject)),
  };
}

function jobPanel(j) {
  const [tone, badge] = rag(j);
  const r = related(j.job);
  const mini = (arr, f, empty) => arr.length ? `<div class="mini">${arr.map(f).join("")}</div>` : `<p class="page-sub">${empty}</p>`;
  openPanel(`
    <h2>${esc(j.job)}</h2>
    <p class="sub">${esc(j.client)} &middot; deadline ${niceDate(j.deadline)} &nbsp;<span class="chip ${tone}">${esc(badge)}</span></p>
    <div class="panel-sec"><h4>Where it stands</h4>${fmt(j.status)}<p style="margin-top:8px"><strong>${esc(j.value)}</strong></p></div>
    <div class="panel-sec"><h4>Open requests on this job</h4>${mini(r.reqs.filter((x) => x.status === "open"), (x) => `<div class="mini-row" data-goreq="${x.id}"><strong>${esc(x.title)}</strong><small>needs ${esc(x.owner)} - raised ${esc(x.raised)}</small></div>`, "None - nothing blocked here.")}</div>
    <div class="panel-sec"><h4>Catches</h4>${mini(r.catches, (c) => `<div class="mini-row static">${esc(c.catch)}<small>${esc(c.date)}</small></div>`, "None on this job.")}</div>
    <div class="panel-sec"><h4>Mary's emails about it</h4>${mini(r.emails, (e) => `<div class="mini-row" data-email="${DATA.emails.indexOf(e)}"><strong>${esc(e.subject)}</strong><small>${esc(e.sent)}</small></div>`, "None yet.")}</div>
    <div class="panel-sec"><h4>Read from the inbox</h4>${mini(r.inbox.slice(0, 8), (i) => `<div class="mini-row" data-inbox="${(DATA.inbox || []).indexOf(i)}"><strong>${esc(i.subject || "(no subject)")}</strong><small>${esc(i.from)} - ${esc(i.received)}</small></div>`, "Nothing filed.")}</div>
    <div class="panel-sec"><h4>Ask Mary about this job</h4>
      <div class="ask-inline"><textarea id="panel-ask" placeholder="Chase the supplier, re-price it, explain the number..."></textarea>
      <button class="btn" id="panel-ask-send">Send to Mary</button></div></div>`);
  $("#panel-ask-send").addEventListener("click", async (e) => {
    const body = $("#panel-ask").value.trim();
    if (!body) return;
    e.target.disabled = true;
    e.target.textContent = "Sending...";
    await sendToMary(body, j.job);
    closePanel();
  });
}

function emailPanel(e) {
  openPanel(`
    <h2>${esc(e.subject)}</h2>
    <p class="sub">Sent ${esc(e.sent)} &middot; to ${esc(e.to)}</p>
    <div class="panel-sec"><h4>Full email</h4><div class="rt-box">${fmt(e.body || "(body not captured)")}</div></div>`);
}

function inboxPanel(i) {
  openPanel(`
    <h2>${esc(i.subject || "(no subject)")}</h2>
    <p class="sub">From ${esc(i.from)} &middot; ${esc(i.received)}${i.attachments ? ` &middot; ${i.attachments} attachment(s)` : ""}</p>
    <div class="panel-sec"><h4>What Mary read</h4><div class="rt-box">${fmt(i.body || "(body not stored)")}</div></div>`);
}

/* ---------------- pages ---------------- */
const ICONS = {
  overview: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>',
  pipeline: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 8v4l2.5 2.5"/><circle cx="12" cy="12" r="9"/></svg>',
  requests: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4m0 4h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>',
  messages: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/></svg>',
  comms: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
  catches: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>',
  scoreboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="m7 15 4-5 3 3 5-7"/></svg>',
};

const PAGES = [
  { key: "overview", label: "Overview", sub: () => "Everything Mary is holding, at a glance" },
  { key: "pipeline", label: "Pipeline", sub: () => "Every live tender, most urgent first" },
  { key: "requests", label: "Mary needs you", sub: () => `${awaitingReqs().length} decision${awaitingReqs().length === 1 ? "" : "s"} she cannot make without a human` },
  { key: "messages", label: "Messages", sub: () => "Two-way line - she picks up what you write within seconds" },
  { key: "comms", label: "Comms log", sub: () => "Everything sent and everything read" },
  { key: "catches", label: "Catches", sub: () => "Errors found and money saved" },
  { key: "scoreboard", label: "Scoreboard", sub: () => "How close Mary is getting, and whether we won" },
];

const RENDER = {
  overview() {
    const overdue = DATA.jobs.filter((j) => j.stage === "overdue");
    const dueSoon = DATA.jobs.filter((j) => j.stage === "tender" && daysUntil(j.deadline) <= 3);
    const urgent = [...DATA.jobs].filter((j) => j.stage !== "submitted").sort((a, b) => new Date(a.deadline) - new Date(b.deadline)).slice(0, 5);
    return `
      <div class="stats">
        <div class="stat" data-go="pipeline"><div class="n">${DATA.jobs.length}</div><div class="l">Live jobs tracked</div></div>
        <div class="stat ${dueSoon.length ? "amber" : "green"}" data-go="pipeline"><div class="n">${dueSoon.length}</div><div class="l">Due in the next 3 days</div></div>
        <div class="stat ${overdue.length ? "red" : "green"}" data-go="pipeline"><div class="n">${overdue.length}</div><div class="l">Overdue</div></div>
        <div class="stat amber" data-go="requests"><div class="n">${awaitingReqs().length}</div><div class="l">Decisions Mary needs</div></div>
        <div class="stat green" data-go="catches"><div class="n">${DATA.catches.length}</div><div class="l">Catches logged</div></div>
      </div>
      <div class="section"><div class="section-head"><h3>Most urgent</h3><a data-go="pipeline">Full pipeline &rarr;</a></div>
        ${this._table(urgent)}</div>
      <div class="section"><div class="section-head"><h3>Engine room</h3></div>
        <div class="mail-list"><div class="mail-row" style="cursor:default">
          <div class="mail-ico in">MG</div>
          <div><strong>${DATA.sessions.polls.toLocaleString()} inbox polls &middot; ${DATA.sessions.launched} working sessions &middot; ${DATA.sessions.emailsSent} emails sent</strong>
          <small>${esc(DATA.register.recent)}</small></div>
          <span class="mail-when">${DATA.register.lines.toLocaleString()} rates</span>
        </div></div></div>`;
  },
  _table(jobs) {
    return `<table class="tbl"><thead><tr><th>Job</th><th>Status</th><th>Deadline</th><th>Value</th><th></th></tr></thead><tbody>
      ${jobs.map((j) => {
        const [tone, badge] = rag(j);
        return `<tr data-job="${esc(j.job)}">
          <td class="job-cell"><strong>${esc(j.job)}</strong><small>${esc(j.client)}</small></td>
          <td style="max-width:380px">${esc(j.status.split(". ")[0])}.</td>
          <td class="num">${niceDate(j.deadline)}</td>
          <td class="num">${esc(j.value)}</td>
          <td><span class="chip ${tone}">${esc(badge)}</span></td></tr>`;
      }).join("")}</tbody></table>`;
  },
  pipeline() {
    const jobs = [...DATA.jobs].sort((a, b) => (a.stage === "submitted") - (b.stage === "submitted") || new Date(a.deadline) - new Date(b.deadline));
    return this._table(jobs);
  },
  requests() {
    const open = openReqs();
    const done = (DATA.requests || []).filter((r) => r.status !== "open");
    if (!open.length && !done.length) return `<div class="empty"><strong>Nothing needed</strong>Mary has no open requests.</div>`;
    const card = (r) => r.status === "open" ? `
      <article class="req" data-req="${r.id}">
        <div class="req-top"><div><h3>${esc(r.title)}</h3><div class="meta">${esc(r.job)} &middot; raised ${esc(r.raised)} &middot; needs <strong>${esc(r.owner)}</strong></div></div>
        <span class="chip ${SENT_ANSWERS[r.id] ? "ok" : "warn"}">${SENT_ANSWERS[r.id] ? "sent to Mary" : "waiting"}</span></div>
        <div class="req-block"><h5>Why Mary is blocked</h5><p>${inline(r.why)}</p></div>
        <div class="req-block needs"><h5>What she needs from you</h5><p>${inline(r.needs)}</p></div>
        ${SENT_ANSWERS[r.id] ? `
        <div class="req-answer sent">
          <h5>Your answer &middot; sent ${esc(SENT_ANSWERS[r.id].at)}</h5>
          ${fmt(SENT_ANSWERS[r.id].body)}
          <p class="sent-note">With Mary now - she will reply in Messages and mark this resolved.</p>
        </div>` : `
        <div class="req-answer">
          ${r.options?.length ? `<div class="req-options">${r.options.map((o, i) => `<button class="opt" data-opt="${i}">${esc(o)}</button>`).join("")}</div>` : ""}
          <div class="req-compose"><textarea data-draft="req:${r.id}" placeholder="Your answer (or pick an option above and add detail)..."></textarea>
          <button class="btn" data-answer="${r.id}">Answer</button></div>
        </div>`}
      </article>` : `
      <article class="req resolved">
        <div class="req-top"><div><h3>${esc(r.title)}</h3><div class="meta">${esc(r.job)} &middot; answered ${esc(r.answered_at || "")} by ${esc(r.answered_by || "team")}</div></div><span class="chip ok">resolved</span></div>
        <div class="answered"><h5>The answer</h5>${fmt(r.answer || "")}</div>
      </article>`;
    return `<div class="req-grid">${open.map(card).join("")}${done.length ? `<div class="section-head" style="margin-top:14px"><h3>Resolved</h3></div>` + done.map(card).join("") : ""}</div>`;
  },
  messages() {
    const thread = [...MESSAGES].reverse();
    let lastDay = "";
    const parts = [];
    for (const m of thread) {
      const day = m.created.slice(0, 10);
      if (day !== lastDay) { parts.push(`<div class="chat-day">${new Date(day).toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" })}</div>`); lastDay = day; }
      const mine = m.author !== "mary";
      parts.push(`<div class="bubble ${mine ? "human" : "mary"}${mine && !m.seen_by_mary ? " pending" : ""}">
        <div class="who">${esc(m.author === "mary" ? "MARY GRACE" : m.author.toUpperCase())} <time>${esc(m.created.slice(11, 16))}</time>
        ${mine && !m.seen_by_mary ? '<span class="wait-note">waiting for Mary</span>' : ""}</div>
        ${m.context ? `<span class="ctx">${esc(m.context)}</span>` : ""}${fmt(m.body)}</div>`);
    }
    return `<div class="chat">
      <div class="chat-thread">${parts.length ? parts.join("") : `<div class="empty"><strong>No messages yet</strong>Say hello - Mary replies right here.</div>`}</div>
      <div class="chat-compose">
        <textarea id="chat-body" data-draft="chat" placeholder="Ask Mary anything - price a job, chase something, explain a number..."></textarea>
        <div class="chat-actions"><span class="chat-hint">Sending as <strong>${esc(who())}</strong> &middot; ${STATUS?.state === "working" ? "she is mid-job - this queues behind it" : "picked up within seconds"}</span>
        <button class="btn" id="chat-send">Send</button></div>
      </div></div>`;
  },
  comms() {
    const sent = DATA.emails.map((e, i) => `
      <div class="mail-row" data-email="${i}"><div class="mail-ico out">&uarr;</div>
        <div><strong>${esc(e.subject)}</strong><small>to ${esc(e.to)}</small></div>
        <span class="mail-when">${esc(e.sent)}</span></div>`).join("");
    const seen = (DATA.inbox || []).map((m, i) => `
      <div class="mail-row" data-inbox="${i}"><div class="mail-ico in">&darr;</div>
        <div><strong>${esc(m.subject || "(no subject)")}</strong><small>${esc(m.from)}${m.attachments ? ` &middot; ${m.attachments} attachment(s)` : ""}</small></div>
        <span class="mail-when">${esc(m.received)}</span></div>`).join("");
    return `
      <div class="subtabs">
        <button class="subtab${commsTab === "sent" ? " active" : ""}" data-comms="sent">Sent by Mary (${DATA.emails.length})</button>
        <button class="subtab${commsTab === "seen" ? " active" : ""}" data-comms="seen">Read by Mary (${(DATA.inbox || []).length})</button>
      </div>
      <div class="mail-list">${commsTab === "sent" ? (sent || '<div class="empty">Nothing sent yet.</div>') : (seen || '<div class="empty">Nothing captured yet.</div>')}</div>`;
  },
  scoreboard() {
    const sb = DATA.scoreboard;
    if (!sb) return `<div class="empty"><strong>No scoreboard yet</strong>Run scripts/mary_scoreboard.py and redeploy.</div>`;
    const a = sb.accuracy || { n: 0, points: [] };
    const log = sb.estimating_log || {};
    const decided = OUTCOMES.filter((o) => o.result !== "no-decision");
    const won = decided.filter((o) => o.result === "won").length;
    const recorded = OUTCOMES.map((o) => o.job.toLowerCase());
    const awaiting = DATA.jobs.filter((j) => !recorded.includes(j.job.toLowerCase()));

    const acc = a.n ? `
      <div class="stats">
        <div class="stat"><div class="n">${a.mean_abs_error_pct}%</div><div class="l">Average miss, either way</div></div>
        <div class="stat ${Math.abs(a.mean_error_pct) < 3 ? "green" : "amber"}"><div class="n">${a.mean_error_pct > 0 ? "+" : ""}${a.mean_error_pct}%</div><div class="l">Bias (high or low)</div></div>
        <div class="stat"><div class="n">${a.within_10pct}/${a.n}</div><div class="l">Within 10%</div></div>
        <div class="stat"><div class="n">${a.within_5pct}/${a.n}</div><div class="l">Within 5%</div></div>
      </div>
      <table class="tbl"><thead><tr><th>Job</th><th class="num">Mary said</th><th class="num">Actual</th><th class="num">Out by</th><th>What it taught her</th></tr></thead><tbody>
      ${a.points.map((p) => `<tr>
        <td class="job-cell"><strong>${esc(p.job)}</strong><small>${esc(p.client || "")} &middot; ${esc(p.date)}</small></td>
        <td class="num">${p.mary_estimate.toLocaleString("en-GB", { minimumFractionDigits: 2 })}</td>
        <td class="num">${p.actual.toLocaleString("en-GB", { minimumFractionDigits: 2 })}</td>
        <td class="num"><span class="chip ${p.abs_error_pct <= 5 ? "ok" : p.abs_error_pct <= 10 ? "warn" : "danger"}">${p.error_pct > 0 ? "+" : ""}${p.error_pct}%</span></td>
        <td style="max-width:420px;font-size:var(--t-13)">${esc(p.lesson || "")}</td></tr>`).join("")}
      </tbody></table>`
      : `<div class="empty"><strong>No comparisons yet</strong>Every time Mary prices something a human also priced, it lands here.</div>`;

    return `
      <div class="verdict"><h4>Can we stop double-checking?</h4><p>${esc(sb.verdict)}</p></div>
      <div class="section"><div class="section-head"><h3>How close is she?</h3></div>${acc}</div>
      <div class="section"><div class="section-head"><h3>Did we win it?</h3></div>
        <p class="page-sub" style="margin-bottom:14px">The Estimating Log carries a W/L mark on ${log.with_outcome || 0} of ${log.logged || 0} jobs
          (${log.outcome_coverage_pct || 0}%), so there is no history to learn from. One click here is what builds it.
          ${decided.length ? `<strong>So far: ${won} won, ${decided.length - won} lost.</strong>` : "<strong>Nothing recorded yet.</strong>"}</p>
        <div class="mail-list">
          ${awaiting.length ? awaiting.map((j) => `
            <div class="mail-row outcome-row" style="cursor:default">
              <div><strong>${esc(j.job)}</strong><small>${esc(j.client)} &middot; ${esc(j.value)}</small></div>
              <div class="outcome-btns">
                <button class="opt win" data-outcome="won" data-job="${esc(j.job)}">Won</button>
                <button class="opt loss" data-outcome="lost" data-job="${esc(j.job)}">Lost</button>
                <button class="opt" data-outcome="no-decision" data-job="${esc(j.job)}">No decision</button>
              </div>
            </div>`).join("") : '<div class="empty">Every live job has an outcome recorded.</div>'}
        </div>
      </div>
      ${OUTCOMES.length ? `<div class="section"><div class="section-head"><h3>Recorded</h3></div>
        <div class="mail-list">${OUTCOMES.map((o) => `
          <div class="mail-row" style="cursor:default"><div class="mail-ico ${o.result === "won" ? "out" : "in"}">${o.result === "won" ? "&#10003;" : o.result === "lost" ? "&times;" : "&ndash;"}</div>
          <div><strong>${esc(o.job)}</strong><small>${esc(o.result)}${o.note ? " &middot; " + esc(o.note) : ""}</small></div>
          <span class="mail-when">${esc((o.created || "").slice(0, 10))}</span></div>`).join("")}</div></div>` : ""}`;
  },
  catches() {
    return `<div class="catch-grid">${DATA.catches.map((c) => `
      <article class="catch"><div class="req-top"><div><h3 style="font-size:15px">${esc(c.job)}</h3>
        <div class="meta" style="font-size:12px;color:var(--muted)">${esc(c.date)} &middot; ${esc(c.type)}</div></div>
        <span class="value">${esc(c.value || "")}</span></div>
        <p style="margin:10px 0 0">${inline(c.catch)}</p></article>`).join("")}</div>`;
  },
};

/* ---------------- render / routing ---------------- */
function restoreDrafts() {
  $$("[data-draft]").forEach((el) => { if (DRAFTS[el.dataset.draft]) el.value = DRAFTS[el.dataset.draft]; });
  $$(".req").forEach((card) => {
    const chosen = DRAFTS[`opt:${card.dataset.req}`];
    if (chosen === undefined) return;
    card.querySelectorAll(".opt").forEach((o, i) => o.classList.toggle("sel", i === chosen));
  });
}

function applyFilter() {
  const q = searchTerm.toLowerCase();
  $$("#page tr[data-job], #page .req, #page .mail-row, #page .catch, #page .bubble").forEach((el) => {
    el.style.display = !q || el.textContent.toLowerCase().includes(q) ? "" : "none";
  });
}

function render() {
  // Hold on to what the user is doing, so a background refresh cannot eat it.
  const active = document.activeElement;
  const focusKey = active?.dataset?.draft || (active?.id === "search" ? "search" : null);
  const caret = focusKey && active.setSelectionRange ? [active.selectionStart, active.selectionEnd] : null;
  const thread = $(".chat-thread");
  const stickToBottom = !thread || thread.scrollHeight - thread.scrollTop - thread.clientHeight < 40;

  const badges = { requests: awaitingReqs().length, messages: unseenMsgs() };
  $("#nav-items").innerHTML = PAGES.map((p) => `
    <button class="nav-item${p.key === page ? " active" : ""}" data-nav="${p.key}">${ICONS[p.key]}${p.label}
    ${badges[p.key] ? `<span class="badge${p.key === "requests" ? " hot" : ""}">${badges[p.key]}</span>` : ""}</button>`).join("");
  const meta = PAGES.find((p) => p.key === page);
  $("#page-title").textContent = meta.label;
  $("#page-sub").textContent = meta.sub();
  $("#page").innerHTML = RENDER[page] ? RENDER[page].call(RENDER) : "";
  $("#updated-at").textContent = "Board updated " + new Date(DATA.updated).toLocaleString("en-GB", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
  $("#search").value = searchTerm;

  restoreDrafts();
  applyFilter();
  if (focusKey) {
    const el = focusKey === "search" ? $("#search") : $(`[data-draft="${focusKey}"]`);
    if (el) {
      el.focus();
      if (caret && el.setSelectionRange) el.setSelectionRange(caret[0], caret[1]);
    }
  }
  // Land on the newest message, and keep following it unless you have
  // deliberately scrolled up to read something older.
  const t = $(".chat-thread");
  if (t && stickToBottom) {
    t.style.scrollBehavior = "auto";       // no visible lurch on first paint
    t.scrollTop = t.scrollHeight;
    requestAnimationFrame(() => { t.scrollTop = t.scrollHeight; t.style.scrollBehavior = ""; });
  }

  const send = $("#chat-send");
  if (send) send.addEventListener("click", async () => {
    const body = $("#chat-body").value.trim();
    if (!body) return;
    send.disabled = true;
    await sendToMary(body);
    delete DRAFTS.chat;
    render();
  });
}

document.addEventListener("input", (e) => {
  const key = e.target.dataset?.draft;
  if (key) DRAFTS[key] = e.target.value;
});

document.addEventListener("click", async (e) => {
  const nav = e.target.closest("[data-nav],[data-go],[data-goreq]");
  if (nav) {
    if (nav.dataset.goreq) { closePanel(); page = "requests"; render(); return; }
    page = nav.dataset.nav || nav.dataset.go; render(); return;
  }
  // Scoped to .req-options: the scoreboard's Won/Lost buttons reuse .opt and
  // were being swallowed here before ever reaching their own handler.
  const opt = e.target.closest(".req-options .opt");
  if (opt) {
    const opts = [...opt.closest(".req-options").querySelectorAll(".opt")];
    opts.forEach((o) => o.classList.toggle("sel", o === opt));
    DRAFTS[`opt:${opt.closest(".req").dataset.req}`] = opts.indexOf(opt);
    return;
  }
  const answer = e.target.closest("[data-answer]");
  if (answer) {
    const req = (DATA.requests || []).find((r) => r.id === answer.dataset.answer);
    const card = answer.closest(".req");
    const chosen = card.querySelector(".opt.sel")?.textContent || "";
    const extra = card.querySelector("textarea").value.trim();
    const body = [chosen && `Decision: ${chosen}`, extra].filter(Boolean).join("\n\n");
    if (!body) { toast("Pick an option or type an answer first"); return; }
    answer.disabled = true;
    answer.textContent = "Sending...";
    try {
      await sendToMary(body, `${req.id}: ${req.title}`);
    } catch {
      answer.disabled = false;
      answer.textContent = "Answer";
      toast("Could not send - check your connection and try again");
      return;
    }
    SENT_ANSWERS[req.id] = { body, at: new Date().toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }) };
    delete DRAFTS[`req:${req.id}`];
    delete DRAFTS[`opt:${req.id}`];
    render();
    toast(`Answer sent - ${req.id} is with Mary`);
    return;
  }
  const outcome = e.target.closest("[data-outcome]");
  if (outcome) {
    const job = outcome.dataset.job;
    const result = outcome.dataset.outcome;
    outcome.closest(".outcome-btns").querySelectorAll("button").forEach((b) => { b.disabled = true; });
    outcome.textContent = "Saving...";
    try {
      await api("outcomes", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ job, result, author: who() }),
      });
      OUTCOMES = await api("outcomes");
      toast(`Recorded: ${job} - ${result}`);
      render();
    } catch {
      toast("Could not record that - try again");
      render();
    }
    return;
  }
  const sub = e.target.closest("[data-comms]");
  if (sub) { commsTab = sub.dataset.comms; render(); return; }
  const row = e.target.closest("[data-job],[data-email],[data-inbox]");
  if (row) {
    if (row.dataset.job) { const j = DATA.jobs.find((x) => x.job === row.dataset.job); if (j) jobPanel(j); }
    else if (row.dataset.email !== undefined) emailPanel(DATA.emails[+row.dataset.email]);
    else if (row.dataset.inbox !== undefined) inboxPanel((DATA.inbox || [])[+row.dataset.inbox]);
  }
});

$("#search").addEventListener("input", (e) => {
  searchTerm = e.target.value;
  applyFilter();
});

/* ---------------- boot ---------------- */
(async () => {
  try {
    [DATA, MESSAGES, STATUS, OUTCOMES] = await Promise.all([
      api("data"), api("messages"), api("status").catch(() => null), api("outcomes").catch(() => []),
    ]);
    msgSig = signature(MESSAGES);
    render();
    renderStatus();
    setInterval(async () => {
      try {
        const [fresh, status] = await Promise.all([api("messages"), api("status").catch(() => STATUS)]);
        const statusChanged = JSON.stringify(status) !== JSON.stringify(STATUS);
        STATUS = status;
        if (statusChanged) renderStatus();
        const sig = signature(fresh);
        if (sig === msgSig) return;   // nothing changed - never redraw over the user
        MESSAGES = fresh;
        msgSig = sig;
        if (page === "messages" || page === "overview") render();
      } catch {}
    }, 10000);
  } catch (err) {
    $("#page").innerHTML = `<div class="empty"><strong>Could not load the hub</strong>${err.status || err.message}</div>`;
  }
})();
