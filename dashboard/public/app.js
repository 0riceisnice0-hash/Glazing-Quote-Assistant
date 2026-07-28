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
/* Two bots share this hub. BOT decides which set of pages the board shows;
   Mary's data lives in DATA, Jacob's in JACOB, and neither reads the other. */
let BOT = "mary";
let JACOB = null;

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
let ACTIVITY = null;
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
  // Any number of decimals plus an optional m/k suffix, otherwise "GBP 14.9m"
  // renders as a highlighted "GBP 14" trailed by a stray ".9m".
  h = h.replace(/((?:GBP\s?|£)[\d,]+(?:\.\d+)?(?:\s?[mk])?)\b/gi, '<span class="money">$1</span>');
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
  live: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12h4l3-8 4 16 3-8h6"/></svg>',
  leads: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
  signals: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 11a9 9 0 0 1 9-9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1.5"/></svg>',
  jmessages: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/></svg>',
  jlive: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12h4l3-8 4 16 3-8h6"/></svg>',
  botchat: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 10h8M8 14h5"/><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8A2.5 2.5 0 0 1 17.5 16H9l-5 5Z"/></svg>',
  jayk: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v18H6.5A2.5 2.5 0 0 1 4 18.5Z"/><path d="M8 7h8M8 11h8"/></svg>',
  relationships: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><path d="M17 8.5a3 3 0 0 1 0 5"/><path d="M19.5 20a5.5 5.5 0 0 0-3-4.9"/></svg>',
  outreach: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>',
  sources: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>',
  decisions: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4m0 4h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>',
};

const PAGES = [
  { key: "overview", label: "Overview", group: "Work", sub: () => "Everything Mary is holding, at a glance" },
  { key: "pipeline", label: "Pipeline", group: "Work", sub: () => "Every live tender, most urgent first" },
  { key: "requests", label: "Mary needs you", group: "Work", sub: () => `${awaitingReqs().length} decision${awaitingReqs().length === 1 ? "" : "s"} she cannot make without a human` },
  { key: "messages", label: "Messages", group: "Talk", sub: () => "Two-way line - she picks up what you write within seconds" },
  { key: "comms", label: "Comms log", group: "Talk", sub: () => "Everything sent and everything read" },
  { key: "catches", label: "Catches", group: "Record", sub: () => "Errors found and money saved" },
  { key: "scoreboard", label: "Scoreboard", group: "Record", sub: () => "How close Mary is getting, and whether we won" },
  { key: "live", label: "Live", group: "Record", sub: () => ACTIVITY?.title ? `Working on ${ACTIVITY.title}` : "What Mary is doing right now" },
];

/* ---------------- Jacob Wright - business development ----------------
   A second bot on the same hub. Everything below is his; Mary's PAGES and
   RENDER above are untouched. His data comes from /api/jacob, generated by
   scripts/jacob_dashboard.py, and is entirely separate from DATA.

   Sections that are not built yet render a "planned" note rather than an
   empty table - an empty table reads as "nothing to do", which is a lie. */
const JACOB_PAGES = [
  // Order matters: the group heading is emitted when the group changes,
  // so pages in the same group have to sit together or the heading repeats.
  { key: "overview", label: "Overview", group: "Find", sub: () => "What Jacob has found, and what is still to build" },
  { key: "signals", label: "Signals", group: "Find", sub: () => `${JACOB?.totals.signals || 0} enquiries and portal notices found in the mailboxes` },
  { key: "leads", label: "Leads", group: "Find", sub: () => `${(JACOB?.totals.warm || 0) + (JACOB?.totals.known || 0)} matched to a Fenster relationship, ${JACOB?.totals.cold || 0} cold` },
  { key: "relationships", label: "Relationships", group: "People", sub: () => `${JACOB?.relationships.rows.length || 0} companies, ${JACOB?.totals.dormant || 0} with no recent contact` },
  { key: "jayk", label: "Jayk's book", group: "People", sub: () => `${JACOB?.jayk?.messages || 0} recovered messages from the former BDM` },
  { key: "jmessages", label: "Messages", group: "Talk", sub: () => "Two-way line with Jacob" },
  { key: "botchat", label: "Internal chat", group: "Talk", sub: () => "What Jacob and Mary say to each other - max ten an hour each" },
  { key: "decisions", label: "Jacob needs you", group: "Talk", sub: () => `${openJacobReqs().length} open, ${JACOB?.decisions.length || 0} standing` },
  { key: "outreach", label: "Outreach", group: "Build", sub: () => "Nothing sends without a human approving it" },
  { key: "sources", label: "Sources", group: "Build", sub: () => "Where leads come from, and which feeds are live" },
  { key: "jlive", label: "Live", group: "Build", sub: () => "What Jacob is doing right now" },
];

/* Jacob's own channels. Loaded alongside his board; a failure here leaves the
   rest of his section working rather than blanking the page. */
let JMSGS = [];
let JREQS = [];
let BOTCHAT = [];
let JACTIVITY = null;
/* What was on screen last time render() ran. A background refresh must leave
   the page exactly where you left it; only a deliberate tab change resets it. */
let LAST_VIEW = { page: null, bot: null };
const openJacobReqs = () => JREQS.filter((r) => r.status !== "answered");

async function sendToJacob(body, context = "") {
  await api("jacob/messages", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ author: who(), body, context }),
  });
  JMSGS = await api("jacob/messages").catch(() => JMSGS);
  toast("Sent - Jacob picks this up on his next pass");
}

const gbp = (v) => {
  if (!v) return "n/a";
  if (v >= 1e6) return `GBP ${(v / 1e6).toFixed(1)}m`;
  return `GBP ${Math.round(v).toLocaleString()}`;
};

const JACOB_RENDER = {
  _leadTable(rows, showClient) {
    if (!rows.length) return `<div class="empty"><strong>Nothing here yet</strong></div>`;
    return `<table class="tbl"><thead><tr>
        <th>Winner</th>${showClient ? "<th>Fenster history</th>" : ""}
        <th>What they won</th><th>Value</th><th>Where</th><th>Awarded</th></tr></thead><tbody>
      ${rows.map((r) => `<tr data-jlead="${esc(r.supplier)}">
        <td><strong>${esc(r.supplier)}</strong></td>
        ${showClient ? `<td>${esc(r.client)} <span class="pill ${r.confidence}">${r.confidence}</span></td>` : ""}
        <td>${esc(r.title)}</td>
        <td class="money">${gbp(r.total || r.value)}</td>
        <td>${esc(r.area) || "-"}</td>
        <td>${esc(r.awarded) || "-"}</td></tr>`).join("")}
    </tbody></table>`;
  },

  overview() {
    const t = JACOB.totals;
    return `
      <div class="stats">
        <div class="stat green" data-go="signals"><div class="n">${t.signals}</div><div class="l">Live signals in the mailboxes</div></div>
        <div class="stat green" data-go="leads"><div class="n">${t.warm}</div><div class="l">Warm - they have bought from us</div></div>
        <div class="stat amber" data-go="leads"><div class="n">${t.known}</div><div class="l">Known - quoted, never won</div></div>
        <div class="stat" data-go="leads"><div class="n">${t.cold}</div><div class="l">Cold building contracts</div></div>
        <div class="stat amber" data-go="relationships"><div class="n">${t.dormant}</div><div class="l">Gone quiet - no recent contact</div></div>
        <div class="stat amber" data-go="decisions"><div class="n">${JACOB.decisions.length}</div><div class="l">Decisions Jacob needs</div></div>
      </div>

      ${JACOB.intake ? `<div class="section"><div class="section-head"><h3>Newest signals</h3><a data-go="signals">All signals &rarr;</a></div>
        ${this._signalTable(JACOB.intake.signals.slice(0, 8))}</div>` : ""}

      <div class="section"><div class="section-head"><h3>Warm - call these first</h3><a data-go="leads">All leads &rarr;</a></div>
        ${this._leadTable(JACOB.warm, true)}</div>

      <div class="section"><div class="section-head"><h3>How this was built</h3></div>
        <div class="planned-note">
          <p>${t.awardRows.toLocaleString()} construction award rows over ${JACOB.window.days} days
          (${JACOB.window.from} to ${JACOB.window.to}), ${t.winners.toLocaleString()} unique winning
          companies, cross-referenced against ${t.clients} client folders in the OneDrive archive
          (${t.clientsWon} of which have actually bought).</p>
          <p><strong>Two rules do most of the filtering.</strong> Leads are scored on what the contract
          <em>is</em> (CPV building families) rather than what its title says - keyword matching
          returned window <em>cleaning</em>, STI <em>screening</em>, and one award that matched only on
          the phrase "the front door to maternity services". And a notice only counts if the award is
          recent and the job is still running: one was published 469 days after the award, on a
          contract that had already finished.</p>
          <p><strong>Confidence matters.</strong> Single-word company names throw false positives -
          "Atlas" matched a window-cleaning contractor. Anything marked
          <span class="pill possible">possible</span> needs a human to confirm it once.</p>
        </div></div>`;
  },

  leads() {
    return `
      <div class="section"><div class="section-head"><h3>Warm - Fenster has delivered for them</h3></div>
        ${this._leadTable(JACOB.warm, true)}</div>
      <div class="section"><div class="section-head"><h3>Known - quoted before, never won</h3></div>
        ${this._leadTable(JACOB.known, true)}</div>
      <div class="section"><div class="section-head"><h3>Cold - building contracts, no relationship yet</h3></div>
        ${this._leadTable(JACOB.cold, false)}</div>`;
  },

  _signalTable(rows) {
    if (!rows || !rows.length) return `<div class="empty"><strong>No signals</strong></div>`;
    return `<table class="tbl"><thead><tr>
        <th>When</th><th>Type</th><th>Company</th><th>Who</th><th>Subject</th><th>In</th></tr></thead><tbody>
      ${rows.map((s) => `<tr>
        <td>${esc(s.date)}</td>
        <td><span class="pill ${s.kind === "portal" ? "planned" : "live"}">${esc(s.kind)}</span></td>
        <td><strong>${esc(s.company)}</strong>${s.relationship && s.relationship !== "unknown"
            ? ` <span class="pill ${s.relationship === "won" ? "exact" : "strong"}">${esc(s.relationship)}</span>` : ""}</td>
        <td>${esc(s.name || s.contact)}</td>
        <td>${esc(s.subject)}</td>
        <td>${esc(s.mailbox)}</td></tr>`).join("")}
    </tbody></table>`;
  },

  signals() {
    if (!JACOB.intake) {
      return `<div class="planned-note">Mailbox intake has not run yet.
        <code>python scripts/jacob_intake.py</code></div>`;
    }
    const i = JACOB.intake;
    const boxes = Object.entries(i.perMailbox)
      .map(([m, n]) => `${m.split("@")[0]} ${n}`).join(" &middot; ");
    return `
      <div class="section"><div class="section-head"><h3>What the mailboxes are holding</h3></div>
        <div class="planned-note">
          <p>Last ${i.windowDays} days: ${esc(boxes)}. Classified as
          ${Object.entries(i.counts).sort((a, b) => b[1] - a[1])
            .map(([k, n]) => `<strong>${n}</strong> ${esc(k)}`).join(", ")}.</p>
          <p>Everything below arrived as ordinary email. No portal login, no scraper.</p>
        </div></div>
      <div class="section"><div class="section-head"><h3>Enquiries and portal notices</h3></div>
        ${this._signalTable(i.signals)}</div>`;
  },

  relationships() {
    const r = JACOB.relationships;
    const rows = r.rows || [];
    const active = rows.filter((x) => x.lastContact);
    const quiet = rows.filter((x) => !x.lastContact && x.relationship !== "unknown");
    const tbl = (list) => `<table class="tbl"><thead><tr>
        <th>Company</th><th>History</th><th>Last contact</th><th>Msgs</th><th>Contacts</th><th>Known from</th></tr></thead><tbody>
      ${list.map((x) => `<tr>
        <td><strong>${esc(x.company)}</strong></td>
        <td>${x.relationship === "unknown" ? "-" :
             `<span class="pill ${x.relationship === "won" ? "exact"
               : x.relationship === "quoted" ? "strong" : "possible"}">${esc(x.relationship)}</span>`}</td>
        <td>${esc(x.lastContact) || "-"}</td>
        <td>${x.messages || "-"}</td>
        <td>${x.contacts.slice(0, 2).map((c) => esc(c.name || c.address)).join(", ")
             }${x.contacts.length > 2 ? ` +${x.contacts.length - 2}` : ""}</td>
        <td>${x.sources.map((s) => `<span class="pill possible">${esc(s)}</span>`).join(" ")}</td>
      </tr>`).join("")}
    </tbody></table>`;
    return `
      <div class="stats">
        <div class="stat green"><div class="n">${r.won}</div><div class="l">Have bought from Fenster</div></div>
        <div class="stat"><div class="n">${r.quoted}</div><div class="l">Quoted, no recorded win</div></div>
        <div class="stat amber"><div class="n">${quiet.length}</div><div class="l">No contact in the window</div></div>
      </div>
      <div class="section"><div class="section-head"><h3>Active - they have emailed us recently</h3></div>
        ${tbl(active.slice(0, 60))}</div>
      <div class="section"><div class="section-head"><h3>Gone quiet - quoted before, nothing lately</h3></div>
        <div class="planned-note">The cheapest lead in the business: they already asked
        Fenster for a price once. Showing the first 60 of ${quiet.length}.</div>
        ${tbl(quiet.slice(0, 60))}</div>`;
  },

  jayk() {
    if (!JACOB.jayk) {
      return `<div class="planned-note">Not recovered yet.
        <code>python scripts/jacob_jayk_recovery.py</code></div>`;
    }
    const j = JACOB.jayk;
    return `
      <div class="section"><div class="section-head"><h3>The former BDM's contact book</h3></div>
        <div class="planned-note">
          <p>Jayk was Fenster's business development manager. His mailbox no longer exists -
          no soft-deleted copy, no inactive copy - so <strong>${j.messages}</strong> messages were
          recovered from the threads that copied a role mailbox instead.</p>
          <p>This is a one-off recovery, not a feed. It is here so the relationships outlast
          the person who held them.</p>
        </div></div>
      <div class="section"><div class="section-head"><h3>Who he was dealing with</h3></div>
        <table class="tbl"><thead><tr><th>Contact</th><th>Company</th><th>Messages</th></tr></thead><tbody>
        ${j.contacts.map(([addr, n, name]) => `<tr>
          <td><strong>${esc(name || addr)}</strong></td>
          <td>${esc(addr.split("@")[1])}</td>
          <td>${n}</td></tr>`).join("")}
        </tbody></table></div>
      <div class="section"><div class="section-head"><h3>What was live when he left</h3></div>
        <table class="tbl"><thead><tr><th>Date</th><th>Mailbox</th><th>Subject</th></tr></thead><tbody>
        ${j.subjects.map(([d, box, subj]) => `<tr>
          <td>${esc(d)}</td><td>${esc(box)}</td><td>${esc(subj)}</td></tr>`).join("")}
        </tbody></table></div>`;
  },

  outreach() {
    const o = JACOB.outreach;
    return `
      <div class="section"><div class="section-head"><h3>Not wired up yet</h3><span class="pill planned">planned</span></div>
        <div class="planned-note"><p>${esc(o.note)}</p></div></div>
      <div class="section"><div class="section-head"><h3>Message types, and how much rope each gets</h3></div>
        <table class="tbl"><thead><tr><th>Type</th><th>When it fires</th><th>Example we already have</th><th>Autonomy</th></tr></thead><tbody>
        ${o.classes.map((c) => `<tr>
          <td><strong>${esc(c.name)}</strong></td><td>${esc(c.why)}</td>
          <td>${esc(c.example)}</td><td>${esc(c.autonomy)}</td></tr>`).join("")}
        </tbody></table></div>`;
  },

  sources() {
    return `
      <div class="section"><div class="section-head"><h3>Feeds</h3></div>
        <table class="tbl"><thead><tr><th>Source</th><th>Status</th><th>Gives us</th><th>Detail</th><th>Cost</th></tr></thead><tbody>
        ${JACOB.sources.map((s) => `<tr>
          <td><strong>${esc(s.name)}</strong></td>
          <td><span class="pill ${s.status === "live" ? "live" : s.status === "planned" ? "planned" : "notstarted"}">${esc(s.status)}</span></td>
          <td>${esc(s.kind)}</td><td>${esc(s.detail)}</td><td>${esc(s.cost)}</td></tr>`).join("")}
        </tbody></table></div>
      <div class="section"><div class="section-head"><h3>The thing worth knowing</h3></div>
        <div class="planned-note">
          <p>Fenster is a <strong>subcontractor</strong>. Almost nothing it wins is advertised - what
          gets published is the main contract the contractor was bidding for. So the job is not
          "find tenders", it is find the scheme, then find who is bidding it and get on their list.</p>
          <p>All of these feeds are <strong>public sector only</strong>. Stepnell, Borras, Chigwell,
          Guildmore and Zelltec work appears in none of them.</p>
        </div></div>`;
  },

  jmessages() {
    const rows = [...JMSGS].reverse();
    return `
      <div class="chat">
        <div class="chat-thread">
          ${rows.length ? rows.map((m) => `
            <div class="bubble ${m.author === "jacob" ? "them" : "me"}">
              <div class="bubble-who">${esc(m.author === "jacob" ? "Jacob Wright" : m.author)}
                <em>${esc((m.created || "").replace("T", " ").slice(0, 16))}</em>
                ${m.context ? `<span class="pill possible">${esc(m.context)}</span>` : ""}</div>
              <div>${fmt(m.body)}</div>
            </div>`).join("")
            : `<div class="empty"><strong>Nothing yet</strong>Ask him something - what he has found, who is worth calling, why a lead scored the way it did.</div>`}
        </div>
        <div class="chat-compose">
          <textarea data-draft="jacob-msg" rows="3" placeholder="Message Jacob..."></textarea>
          <button id="jacob-send" class="btn">Send</button>
        </div>
      </div>`;
  },

  botchat() {
    const rows = [...BOTCHAT].reverse();
    return `
      <div class="section"><div class="section-head"><h3>How this works</h3></div>
        <div class="planned-note">
          <p>Jacob knows who is buying; Mary knows what is being quoted. This is the line
          between them, and everything on it is visible to you.</p>
          <p><strong>Ten messages an hour each</strong>, refused by the API beyond that -
          a wall rather than an instruction, because two agents with something to say will
          otherwise talk all night. And <strong>neither has to reply</strong>: a message
          marked FYI gets no answer unless the other has something to add. Silence is the
          normal outcome.</p>
        </div></div>
      <div class="chat">
        <div class="chat-thread">
          ${rows.length ? rows.map((m) => `
            <div class="bubble ${m.sender === "jacob" ? "me" : "them"}">
              <div class="bubble-who">${esc(m.sender === "jacob" ? "Jacob Wright" : "Mary Grace")}
                &rarr; ${esc(m.recipient)}
                <em>${esc((m.created || "").replace("T", " ").slice(0, 16))}</em>
                ${m.wants_reply ? `<span class="pill strong">wants a reply</span>`
                                : `<span class="pill possible">FYI</span>`}</div>
              ${m.subject ? `<div><strong>${esc(m.subject)}</strong></div>` : ""}
              <div>${fmt(m.body)}</div>
            </div>`).join("")
            : `<div class="empty"><strong>They have not spoken yet</strong>Nothing to report to each other is a perfectly good state.</div>`}
        </div>
      </div>`;
  },

  jlive() {
    const a = JACTIVITY || {};
    const events = a.events || [];
    if (!events.length) {
      return `<div class="empty"><strong>Nothing running</strong>When Jacob picks up
        a message or a lead, every step he takes appears here as it happens.</div>`;
    }
    const icon = { say: "&#9679;", think: "&#8230;", tool: "&#9656;", result: "&#8629;" };
    const when = a.updated ? new Date(a.updated).toLocaleTimeString("en-GB",
      { hour: "2-digit", minute: "2-digit", second: "2-digit" }) : "";
    return `
      <div class="live-head">
        <span class="chip warn">working</span>
        <strong>${esc(a.title || "Business development")}</strong>
        <span class="live-when">last step ${esc(when)}</span>
      </div>
      <div class="ev-feed" id="ev-feed">${events.map((e) => `
        <div class="ev ev-${esc(e.kind)}">
          <span class="ev-mark">${icon[e.kind] || "&#9679;"}</span>
          <div class="ev-body">${esc(e.text)}</div>
        </div>`).join("")}</div>`;
  },

  decisions() {
    const open = openJacobReqs();
    return `
      ${open.length ? `<div class="section"><div class="section-head"><h3>He is blocked on these</h3></div>
        <div class="cards">${open.map((r) => `<div class="card">
          <div class="card-head"><strong>${esc(r.title)}</strong><span class="pill strong">${esc(r.ref)}</span></div>
          ${r.why ? `<p>${esc(r.why)}</p>` : ""}
          ${r.needs ? `<p><strong>Needs:</strong> ${esc(r.needs)}</p>` : ""}
          <div class="req-options">${(JSON.parse(r.options || "[]")).map((o) =>
            `<span class="opt" data-jreq="${esc(r.ref)}">${esc(o)}</span>`).join("")}</div>
        </div>`).join("")}</div></div>` : ""}

      <div class="section"><div class="section-head"><h3>Standing decisions</h3></div>
        <div class="planned-note">These are not blocking him day to day, but they decide
        how far he is allowed to go.</div>
        <div class="cards">
        ${JACOB.decisions.map((d) => `<div class="card">
          <div class="card-head"><strong>${esc(d.title)}</strong><span class="pill planned">${esc(d.id)}</span></div>
          <p>${esc(d.why)}</p>
          <div class="req-options">${d.options.map((o) => `<span class="opt" data-jreq="${esc(d.id)}">${esc(o)}</span>`).join("")}</div>
        </div>`).join("")}
        </div></div>`;
  },
};

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
  live() {
    const a = ACTIVITY || {};
    const events = a.events || [];
    if (!events.length) {
      return `<div class="empty"><strong>Nothing running</strong>${STATUS?.state === "working"
        ? "Mary is working - her first step will appear here in a moment."
        : "When Mary picks up a job, everything she does appears here as it happens."}</div>`;
    }
    const icon = { say: "&#9679;", think: "&#8230;", tool: "&#9656;", result: "&#8629;" };
    const rows = events.map((e) => `
      <div class="ev ev-${esc(e.kind)}">
        <span class="ev-mark">${icon[e.kind] || "&#9679;"}</span>
        <div class="ev-body">${esc(e.text)}</div>
      </div>`).join("");
    const when = a.updated ? new Date(a.updated).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", second: "2-digit" }) : "";
    return `
      <div class="live-head">
        <span class="chip ${STATUS?.state === "working" ? "warn" : "ok"}">${STATUS?.state === "working" ? "working" : "idle"}</span>
        <strong>${esc(a.title || a.chat || "")}</strong>
        <span class="live-when">last step ${esc(when)}</span>
      </div>
      <div class="ev-feed" id="ev-feed">${rows}</div>`;
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
  // Scroll state, captured before the page is thrown away and rebuilt.
  // "Same view" means a background refresh, so everything stays put. A tab
  // change is deliberate and starts at the top.
  const sameView = LAST_VIEW.page === page && LAST_VIEW.bot === BOT;
  const winY = window.scrollY;
  const atBottom = (el) => !el || el.scrollHeight - el.scrollTop - el.clientHeight < 40;
  const thread = $(".chat-thread");
  const stickToBottom = atBottom(thread);
  const threadTop = thread ? thread.scrollTop : 0;
  const feedBefore = $("#ev-feed");
  const feedStick = atBottom(feedBefore);
  const feedTop = feedBefore ? feedBefore.scrollTop : 0;

  const jacob = BOT === "jacob";
  const pages = jacob ? JACOB_PAGES : PAGES;
  const renderer = jacob ? JACOB_RENDER : RENDER;
  const badges = jacob ? {} : { requests: awaitingReqs().length, messages: unseenMsgs() };
  $$(".nav-bot").forEach((b) => b.classList.toggle("active", b.dataset.bot === BOT));

  // Group headings break an 11-item list into something scannable. Only
  // emitted when the group changes, so ungrouped pages still render flat.
  let lastGroup = null;
  $("#nav-items").innerHTML = pages.map((p) => {
    const head = p.group && p.group !== lastGroup
      ? `<div class="nav-group">${esc((lastGroup = p.group))}</div>` : "";
    return `${head}<button class="nav-item${p.key === page ? " active" : ""}" data-nav="${p.key}">${ICONS[p.key]}${p.label}
    ${badges[p.key] ? `<span class="badge${p.key === "requests" ? " hot" : ""}">${badges[p.key]}</span>` : ""}</button>`;
  }).join("");
  // Switching bots can leave `page` pointing at a section the other one does
  // not have ("catches" -> Jacob). Fall back rather than render a blank board.
  const meta = pages.find((p) => p.key === page) || pages[0];
  page = meta.key;
  $("#page-title").textContent = meta.label;
  $("#page-sub").textContent = meta.sub();
  $("#page").innerHTML = renderer[page] ? renderer[page].call(renderer) : "";
  // This label lives inside Mary's sidebar card, so it always shows HER board's
  // timestamp regardless of which bot is on screen. Jacob's is on his overview.
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
  // deliberately scrolled up to read something older. Scrolling up used to be
  // pointless on the live feed - it jumped back to the bottom every few
  // seconds whether you were reading or not.
  const feed = $("#ev-feed");
  if (feed) {
    if (!sameView || feedStick) feed.scrollTop = feed.scrollHeight;
    else feed.scrollTop = feedTop;
  }

  const t = $(".chat-thread");
  if (t) {
    if (!sameView || stickToBottom) {
      t.style.scrollBehavior = "auto";     // no visible lurch on first paint
      t.scrollTop = t.scrollHeight;
      requestAnimationFrame(() => { t.scrollTop = t.scrollHeight; t.style.scrollBehavior = ""; });
    } else {
      t.scrollTop = threadTop;
    }
  }

  // The page itself. Rebuilding #page changes its height, which drops the
  // window to the top mid-read on every background refresh.
  window.scrollTo({ top: sameView ? winY : 0, behavior: "auto" });
  LAST_VIEW = { page, bot: BOT };

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
  // Swap the whole board between Mary and Jacob.
  const bot = e.target.closest("[data-bot]");
  if (bot) {
    if (bot.dataset.bot !== BOT) {
      BOT = bot.dataset.bot;
      page = "overview";
      searchTerm = "";
      closePanel();
      render();
    }
    return;
  }
  const nav = e.target.closest("[data-nav],[data-go],[data-goreq]");
  if (nav) {
    if (nav.dataset.goreq) { closePanel(); page = "requests"; render(); return; }
    page = nav.dataset.nav || nav.dataset.go; render(); return;
  }
  // Jacob's questions post to his own endpoint, not Mary's.
  const jopt = e.target.closest(".req-options .opt[data-jreq]");
  if (jopt) {
    const ref = jopt.dataset.jreq;
    const answer = jopt.textContent.trim();
    [...jopt.closest(".req-options").querySelectorAll(".opt")]
      .forEach((o) => o.classList.toggle("on", o === jopt));
    try {
      await api("jacob/requests", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ ref, answer, author: who() }),
      });
      JREQS = await api("jacob/requests").catch(() => JREQS);
      toast(`Answered ${ref} - Jacob picks it up on his next pass`);
      render();
    } catch { toast("Could not save that answer"); }
    return;
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
    // Jacob's board is optional - if his data file is missing the hub still
    // loads and only his section is empty, rather than Mary going down with it.
    [DATA, MESSAGES, STATUS, OUTCOMES, ACTIVITY, JACOB] = await Promise.all([
      api("data"), api("messages"), api("status").catch(() => null),
      api("outcomes").catch(() => []), api("activity").catch(() => null),
      api("jacob").catch(() => null),
    ]);
    // His channels are separate calls so one failing endpoint cannot blank
    // the whole section.
    [JMSGS, JREQS, BOTCHAT] = await Promise.all([
      api("jacob/messages").catch(() => []),
      api("jacob/requests").catch(() => []),
      api("botchat").catch(() => []),
    ]);
    JACTIVITY = await api("jacob-activity").catch(() => null);
    if (!JACOB) $$(".nav-bot[data-bot='jacob']").forEach((b) => { b.hidden = true; });

    // The live feed needs a faster beat than the rest of the hub, but only
    // while somebody is actually watching it.
    // Jacob's live feed, same beat as Mary's and only while somebody is watching.
    setInterval(async () => {
      if (!(BOT === "jacob" && page === "jlive")) return;
      try {
        const fresh = await api("jacob-activity");
        if (JSON.stringify(fresh) === JSON.stringify(JACTIVITY)) return;
        JACTIVITY = fresh;
        render();
      } catch {}
    }, 3000);

    setInterval(async () => {
      if (page !== "live") return;
      try {
        const fresh = await api("activity");
        if (JSON.stringify(fresh) === JSON.stringify(ACTIVITY)) return;
        ACTIVITY = fresh;
        render();
      } catch {}
    }, 3000);
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
        if (BOT === "mary" && (page === "messages" || page === "overview")) render();
      } catch {}
    }, 10000);
  } catch (err) {
    $("#page").innerHTML = `<div class="empty"><strong>Could not load the hub</strong>${err.status || err.message}</div>`;
  }
})();
