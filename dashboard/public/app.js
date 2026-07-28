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
  } else if (s.state === "held") {
    // Budget spent. Without its own branch this fell through to "N queued" in
    // the busy tone, which reads as "about to be worked" - the opposite of the
    // truth. The queue is safe; it just is not moving until the window turns.
    text = s.queue_depth > 0 ? `Holding ${s.queue_depth} until 07:00` : "Holding until 07:00";
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

/* ---------------- live feed ----------------
   One feed, two boards: Mary's Live tab and Jacob's render identical event
   rows, so the markup lives here once.

   A feed update must never call render(). render() replaces #page.innerHTML,
   which collapses the page height, and the browser paints a frame at scroll
   0 before anything can put the position back - that painted frame is the
   flash. Restoring scroll afterwards cannot fix it because it has already
   been seen. So a poll patches #ev-feed in place and touches nothing else. */
const EV_ICON = { say: "&#9679;", think: "&#8230;", tool: "&#9656;", result: "&#8629;" };
const maryChip = () => (STATUS?.state === "working"
  ? { tone: "warn", text: "working" }
  : STATUS?.state === "held" ? { tone: "stalled", text: "held - budget" }
  : { tone: "ok", text: "idle" });

const feedRows = (events) => (events || []).map((e) => `
  <div class="ev ev-${esc(e.kind)}">
    <span class="ev-mark">${EV_ICON[e.kind] || "&#9679;"}</span>
    <div class="ev-body">${esc(e.text)}</div>
  </div>`).join("");

const feedWhen = (a) => (a && a.updated
  ? new Date(a.updated).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", second: "2-digit" })
  : "");

/* Returns false when there is nothing on screen to patch - first paint, or
   coming out of the empty state - and the caller falls back to render(). */
function paintFeed(a, chip) {
  const feed = $("#ev-feed");
  if (!feed || !((a && a.events) || []).length) return false;
  // Follow new events only if the reader was already at the bottom. Scrolling
  // up to read an earlier step has to hold, or the feed is unreadable.
  const stick = feed.scrollHeight - feed.scrollTop - feed.clientHeight < 40;
  feed.innerHTML = feedRows(a.events);
  if (stick) feed.scrollTop = feed.scrollHeight;
  const when = $(".live-head .live-when");
  if (when) when.textContent = `last step ${feedWhen(a)}`;
  // The head chip tracks STATUS, not the feed, and used to stay fresh only
  // because the whole page was being rebuilt every three seconds.
  const dot = chip && $(".live-head .chip");
  if (dot) { dot.className = `chip ${chip.tone}`; dot.textContent = chip.text; }
  return true;
}

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

/* ---------------- Jacob: editing a row ----------------
   Anything on his board with a key can be opened and corrected. What he
   derived stays visible next to what you set, so it is always clear which
   is which - and "dead" or "done" takes the row off Today for good. */
function findJacobRow(key) {
  if (!JACOB) return null;
  const pools = [
    [JACOB.threads, (t) => ({ title: t.person || t.contact, sub: `${t.company} - ${t.mailbox}@`,
      evidence: `<p><strong>${esc(t.subject)}</strong></p><p>${t.messages} message${t.messages === 1 ? "" : "s"} between ${esc(t.first)} and ${esc(t.last)}, from ${esc(t.contact)}. Fenster history: ${esc(t.relationship)}.</p>`,
      unknowns: t.unknowns })],
    [JACOB.warm.concat(JACOB.known, JACOB.cold), (r) => ({ title: r.supplier,
      sub: `${r.client ? r.client + " - " : ""}${gbp(r.total || r.value)}`,
      evidence: `<p><strong>${esc(r.title)}</strong></p><p>Buyer ${esc(r.buyer) || "not named"}. Awarded ${esc(r.awarded) || "date not published"}${r.n > 1 ? `, ${r.n} live contracts in the window` : ""}. ${esc(r.area) ? "Postcode area " + esc(r.area) + "." : ""}</p>${r.url ? `<p><a href="${esc(r.url)}" target="_blank" rel="noopener">The notice on Contracts Finder</a></p>` : ""}`,
      unknowns: r.confidence === "possible" ? ["Whether this is the same company as the archive folder. Single-word names throw false positives."] : [] })],
    [JACOB.relationships.rows, (x) => ({ title: x.company, sub: x.domain || "from the archive",
      evidence: `<p>${x.messages || "No"} message${x.messages === 1 ? "" : "s"} in the window${x.lastContact ? `, last on ${esc(x.lastContact)}` : ""}. Known from ${x.sources.join(", ")}.</p><p>${x.contacts.length ? x.contacts.map((c) => esc(c.name || c.address)).join(", ") : "No named contact."}</p>`,
      unknowns: [] })],
  ];
  for (const [list, shape] of pools) {
    const hit = (list || []).find((r) => r.key === key);
    if (hit) return { ...hit, ...shape(hit) };
  }
  const q = quotesOut().find((r) => r.key === key);
  if (q) {
    return { ...q, title: q.job, sub: `${q.client} - ${q.value}`,
      evidence: `<p>Issued against a return date of ${esc(q.sent)}${q.days > 0 ? `, ${q.days} days ago` : ""}. Read from Mary's job records - she owns that row, Jacob only looks at it.</p>`,
      unknowns: ["Whether the client has answered. Nothing records that anywhere yet."] };
  }
  return null;
}

function crmPanel(key) {
  const item = findJacobRow(key);
  if (!item) { toast("Cannot find that row - the board may have been rebuilt"); return; }
  const o = jp(key);
  const pick = (id, list, current) => `<div class="req-options" id="${id}">${list.map((v) =>
    `<span class="opt${current === v ? " sel" : ""}" data-pick="${id}">${esc(v)}</span>`).join("")}</div>`;
  openPanel(`
    <h2>${esc(item.title)}</h2>
    <p class="sub">${esc(item.sub || "")}</p>
    <div class="panel-sec"><h4>What Jacob can see</h4><div class="rt">${item.evidence}</div></div>
    ${item.unknowns?.length ? `<div class="panel-sec"><h4>What he cannot</h4>
      <ul class="unk">${item.unknowns.map((u) => `<li>${esc(u)}</li>`).join("")}</ul></div>` : ""}
    <div class="panel-sec"><h4>State</h4>${pick("jstate", JSTATES, jState(item))}
      <p class="page-sub">Jacob derived <strong>${esc(item.state || "nothing")}</strong> from the evidence.
      Picking one here overrides that and survives every rebuild.</p></div>
    <div class="panel-sec"><h4>Who does the next thing</h4>${pick("jowner", JOWNERS, jOwner(item))}</div>
    <div class="panel-sec"><h4>Next action</h4>
      <div class="ask-inline"><textarea id="jnext" rows="3">${esc(jNext(item))}</textarea></div></div>
    <div class="panel-sec"><h4>What happened last</h4>
      <div class="ask-inline"><textarea id="jnote" rows="3" placeholder="Rang him - wants a price by Friday...">${esc(o.note || "")}</textarea></div>
      ${o.updated ? `<p class="page-sub">Last edited by ${esc(o.updated_by || "team")} on ${esc((o.updated || "").slice(0, 10))}.</p>` : ""}</div>
    <div class="panel-sec panel-btns">
      <button class="btn" id="jsave">Save</button>
      <button class="btn ghost" id="jdone">Done - take it off the list</button>
    </div>`);

  const save = async (state) => {
    const btn = $("#jsave");
    if (btn) { btn.disabled = true; btn.textContent = "Saving..."; }
    try {
      await api("jacob/pipeline", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          key, label: item.title, author: who(),
          state: state || $("#jstate .opt.sel")?.textContent.trim() || "",
          owner: $("#jowner .opt.sel")?.textContent.trim() || "",
          next_action: $("#jnext").value.trim(),
          note: $("#jnote").value.trim(),
        }),
      });
      JPIPE = Object.fromEntries((await api("jacob/pipeline")).map((r) => [r.key, r]));
      closePanel();
      toast(`Saved - ${item.title}`);
      render();
    } catch {
      if (btn) { btn.disabled = false; btn.textContent = "Save"; }
      toast("Could not save that - try again");
    }
  };
  $("#jsave").addEventListener("click", () => save());
  $("#jdone").addEventListener("click", () => save("done"));
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
  enquiries: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 11a9 9 0 0 1 9-9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1.5"/></svg>',
  chasing: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/></svg>',
  companies: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><path d="M17 8.5a3 3 0 0 1 0 5"/><path d="M19.5 20a5.5 5.5 0 0 0-3-4.9"/></svg>',
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
  //
  // Ordered the way the job is actually done. "Today" is a list of things to
  // do, not a summary of what was found; Enquiries and Chasing are the two
  // places money is either won or quietly lost; everything else is reference.
  { key: "overview", label: "Today", group: "Work", sub: () => `${jActions().length} things to do, most urgent first` },
  { key: "enquiries", label: "Enquiries", group: "Work", sub: () => `${JACOB?.totals.buyers || 0} live conversations with a buyer, out of ${JACOB?.totals.signals || 0} raw messages` },
  { key: "chasing", label: "Chasing", group: "Work", sub: () => `${quotesWaiting().length} quotes past their return date, ${JACOB?.totals.quietBuyers || 0} enquiries gone quiet` },
  { key: "leads", label: "Leads", group: "Work", sub: () => `${(JACOB?.totals.warm || 0) + (JACOB?.totals.known || 0)} winners Fenster knows, ${JACOB?.totals.cold || 0} it does not` },
  { key: "companies", label: "Companies", group: "People", sub: () => `${JACOB?.relationships.total || 0} companies, ${JACOB?.totals.dormantWon || 0} who have paid us and gone silent` },
  { key: "jayk", label: "Jayk's book", group: "People", sub: () => `${JACOB?.totals.jaykContacts || 0} contacts recovered from the former BDM` },
  { key: "jmessages", label: "Messages", group: "Talk", sub: () => "Two-way line with Jacob" },
  { key: "botchat", label: "Internal chat", group: "Talk", sub: () => "What Jacob and Mary say to each other - max ten an hour each" },
  { key: "decisions", label: "Jacob needs you", group: "Talk", sub: () => `${openJacobReqs().length} open, ${JACOB?.decisions.length || 0} standing` },
  { key: "sources", label: "How this works", group: "Build", sub: () => "Where leads come from, what is wired up, and what still is not" },
  { key: "jlive", label: "Live", group: "Build", sub: () => "What Jacob is doing right now" },
];

/* Jacob's own channels. Loaded alongside his board; a failure here leaves the
   rest of his section working rather than blanking the page. */
let JMSGS = [];
let JREQS = [];
let BOTCHAT = [];
let JACTIVITY = null;
/* The CRM overlay. Jacob derives a state and a next action for everything
   from the evidence; this is a human saying otherwise, keyed by the stable
   key his generator emits. It survives a rebuild of jacob-data.js, which is
   the whole point - a board you cannot correct is a report, not a CRM. */
let JPIPE = {};
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

/* A stat tile is read at a glance and has one line to do it in. "GBP 548,513"
   wraps and stops being a glance. */
const gbpShort = (v) => (!v ? "none" : v >= 1e6 ? `GBP ${(v / 1e6).toFixed(1)}m`
  : v >= 1e4 ? `GBP ${Math.round(v / 1000)}k` : gbp(v));

/* ---------------- Jacob's CRM layer ----------------
   Every row on his board has a key, a state, an owner and a next action.
   The generator derives all four; anything a human has changed wins. */
const jp = (key) => JPIPE[key] || {};
const jState = (r) => jp(r.key).state || r.state || "";
const jOwner = (r) => jp(r.key).owner || r.owner || "-";
const jNext = (r) => jp(r.key).next_action || r.next || "";
const jNote = (r) => jp(r.key).note || "";
/* Done and dead both mean "stop showing me this", and both are human-set. */
const jShut = (r) => ["done", "dead"].includes(jState(r));

const JSTATES = ["live", "waiting", "quoted", "gone quiet", "dormant", "dead", "done"];
const JOWNERS = ["Adam", "Jacob", "Gintare", "Mary", "Zac", "-"];

/* One colour vocabulary across every page, so "amber" always means the same
   thing whether it is a company, an enquiry or a quote sitting out. */
function stateTone(s) {
  if (["live", "done"].includes(s)) return "ok";
  if (["waiting", "quoted", "dormant - has bought", "dormant"].includes(s)) return "warn";
  if (["gone quiet", "stale"].includes(s)) return "danger";
  return "navy";
}
const stateChip = (r) => `<span class="chip ${stateTone(jState(r))}">${esc(jState(r) || "no state")}</span>`;

/* An owner with nothing to do is honest; a blank one is an unfinished row. */
const ownerTag = (r) => {
  const o = jOwner(r);
  return o === "-" ? `<span class="who-tag none">nobody</span>` : `<span class="who-tag">${esc(o)}</span>`;
};

/* Mary's board, read only. Fenster's second handover - the quote has gone
   out and it comes back to Jacob to chase - is the one nobody currently
   does, and her job records are the only place the issued quotes exist.
   Everything here is defensive: her file is hers and its shape can change. */
function quotesOut() {
  // Priced and approved is not the same as sent, and "not yet priced" is
  // neither. Both tests are anchored on the stage rather than the value, so a
  // value reading "not yet priced" cannot match the word "priced" and land an
  // unpriced tender on a chase list. Unsent is checked first: "approved to
  // issue" jobs carry a quoted value and have still not gone anywhere.
  const isUnsent = (j) => /approved to issue|awaiting send|drafted|priced -/i.test(j.stage || "");
  const isOut = (j) => /submitted/i.test(j.stage || "") || /\b(quoted|tendered)\b/i.test(j.value || "");
  const jobs = (DATA?.jobs || []).filter((j) => isUnsent(j) || isOut(j));
  return jobs.map((j) => {
    const days = /^\d{4}-\d{2}-\d{2}$/.test(j.deadline || "") ? -daysUntil(j.deadline) : null;
    const key = `job:${String(j.job).toLowerCase().replace(/[^a-z0-9]+/g, "-").slice(0, 50)}`;
    const unsent = isUnsent(j);
    let state, next, owner = "Adam";
    if (unsent) {
      state = "not issued"; owner = "Gintare";
      next = `Not out yet - priced and waiting to be issued. Nothing to chase until it has gone.`;
    } else if (days === null) {
      state = "quoted"; owner = "Jacob";
      next = `No date on this one. Find out when ${j.client} was sent it, then chase.`;
    } else if (days < 0) {
      state = "not due"; owner = "-";
      next = `Return date is ${niceDate(j.deadline)}. Chase the week after, not before.`;
    } else if (days < 7) {
      state = "quoted"; owner = "-";
      next = `Out ${days} day${days === 1 ? "" : "s"}. Leave it until day seven, then Adam calls ${j.client}.`;
    } else if (days < 21) {
      next = `Adam calls ${j.client}. ${j.value} has been out ${days} days with nothing back.`;
      state = "waiting";
    } else {
      state = "gone quiet";
      next = `Adam calls ${j.client} - ${days} days, no answer. Ask outright: won, lost or parked.`;
    }
    return { key, job: j.job, client: j.client, value: j.value, due: j.deadline,
             days, unsent, state, owner, next };
  }).sort((a, b) => (b.days ?? -999) - (a.days ?? -999));
}
/* Only what has genuinely left the building and is past its return date. */
const quotesWaiting = () => quotesOut().filter((q) => !q.unsent && (q.days === null || q.days >= 0));
const poundsOf = (s) => parseFloat(String(s).replace(/[^\d.]/g, "")) || 0;

/* Does Mary already have this? Two words of five letters or more in common
   is enough to be worth showing and tight enough that "House" alone never
   matches. Wrong here costs a chip on a row, not a decision. */
const bigWords = (s) => [...new Set(String(s || "").toLowerCase().match(/[a-z]{5,}/g) || [])];
function maryHas(text) {
  const t = String(text || "").toLowerCase();
  return (DATA?.jobs || []).find((j) => bigWords(j.job).filter((w) => t.includes(w)).length >= 2);
}

/* Everything on the Today list: what Jacob derived, minus anything a human
   has ticked off, plus the quotes sitting out on Mary's board. */
function jActions() {
  if (!JACOB) return [];
  const out = (JACOB.actions || []).filter((a) => !jShut(a));
  for (const q of quotesOut()) {
    // Not due and not yet issued are both real states and neither is a thing
    // to do today. They live on Chasing so nothing disappears.
    if (jShut(q) || q.owner === "-" || q.unsent) continue;
    out.push({
      key: q.key, company: q.client, headline: q.job, what: `${q.value} - issued, nothing back`,
      owner: jOwner(q), next: jNext(q), state: jState(q), page: "chasing",
      score: q.days >= 21 ? 90 : 70,
    });
  }
  return out.sort((a, b) => (b.score || 0) - (a.score || 0));
}

const JACOB_RENDER = {
  /* One row shape for everything with a next action against it. Company,
     what happened, what to do, who does it - in that order, because that is
     the order the question gets asked in. */
  _acts(list, empty) {
    if (!list.length) return `<div class="empty"><strong>${empty}</strong></div>`;
    return `<div class="acts">${list.map((a, i) => `
      <div class="act ${stateTone(jState(a))}" data-jkey="${esc(a.key)}">
        <div class="act-no">${i + 1}</div>
        <div class="act-main">
          <div class="act-top"><strong>${esc(a.headline || a.company)}</strong>
            ${a.headline && a.company !== a.headline ? `<span class="act-co">${esc(a.company)}</span>` : ""}
            ${stateChip(a)}</div>
          <div class="act-what">${inline(a.what || "")}</div>
          <div class="act-next">${inline(jNext(a) || "No next action set - open it and give it one.")}</div>
          ${jNote(a) ? `<div class="act-note">Last note: ${esc(jNote(a))}</div>` : ""}
        </div>
        <div class="act-side">${ownerTag(a)}<small data-go="${esc(a.page || "overview")}">${esc(a.page || "")} &rarr;</small></div>
      </div>`).join("")}</div>`;
  },

  overview() {
    const t = JACOB.totals;
    const acts = jActions();
    const mine = (o) => acts.filter((a) => jOwner(a) === o).length;
    const outValue = quotesWaiting().reduce((n, q) => n + poundsOf(q.value), 0);
    return `
      <div class="stats">
        <div class="stat ${mine("Adam") ? "red" : "green"}"><div class="n">${mine("Adam")}</div><div class="l">Waiting on Adam - a call or a decision</div></div>
        <div class="stat amber" data-go="enquiries"><div class="n">${t.liveBuyers}</div><div class="l">Buyers mid-conversation right now</div></div>
        <div class="stat amber" data-go="chasing"><div class="n">${gbpShort(outValue)}</div><div class="l">Quoted and waiting on an answer</div></div>
        <div class="stat" data-go="leads"><div class="n">${gbpShort(t.knownWinnerValue)}</div><div class="l">Live contracts won by companies we know</div></div>
        <div class="stat amber" data-go="companies"><div class="n">${t.dormantWon}</div><div class="l">Have paid Fenster, silent 180 days</div></div>
      </div>

      <div class="section"><div class="section-head"><h3>Do these today</h3>
        <span class="page-sub">Ranked by how close it is to a real enquiry from a real buyer</span></div>
        ${this._acts(acts, "Nothing outstanding")}</div>

      <div class="section"><div class="section-head"><h3>What Jacob cannot see</h3></div>
        <div class="planned-note">
          <p><strong>Whether anyone has already replied.</strong> Mailbox intake reads
          received mail only, so an enquiry Gintare answered an hour ago looks exactly like
          one nobody has touched. Every "check for a reply, then call" above exists because
          of that gap. <a data-go="decisions">JAC-5</a> asks for sent items.</p>
          <p><strong>Anything private-sector before it is awarded.</strong> All the free feeds
          are public procurement. Stepnell, Borras, Chigwell and Guildmore - four of Fenster's
          real clients - appear in none of them.</p>
        </div></div>`;
  },

  /* ------------------------------------------------ enquiries */
  _threadRows(list) {
    return `<table class="tbl"><thead><tr>
        <th>Who</th><th>What they want</th><th>State</th><th>Next action</th><th>Owner</th></tr></thead><tbody>
      ${list.map((t) => {
        const job = maryHas(t.subject);
        return `<tr data-jkey="${esc(t.key)}">
        <td class="job-cell"><strong>${esc(t.person || t.company)}</strong>
          <small>${esc(t.person ? t.company : t.contact)} &middot; ${t.messages} msg${t.messages === 1 ? "" : "s"} &middot; last ${esc(t.last)}</small></td>
        <td>${esc(t.subject)}
          ${t.relationship !== "unknown" ? ` <span class="pill ${t.relationship === "won" ? "exact" : "strong"}">${esc(t.relationship)}</span>` : ""}
          ${job ? ` <span class="pill live">Mary has this</span>` : ""}</td>
        <td>${stateChip(t)}<small class="dim">${t.days}d</small></td>
        <td style="max-width:340px">${inline(jNext(t))}</td>
        <td>${ownerTag(t)}</td></tr>`;
      }).join("")}
    </tbody></table>`;
  },

  enquiries() {
    if (!JACOB.threads) {
      return `<div class="planned-note">Mailbox intake has not run yet.
        <code>python scripts/jacob_intake.py</code></div>`;
    }
    const T = JACOB.threads.filter((t) => !jShut(t));
    const buyers = T.filter((t) => t.kind === "buyer");
    const open = buyers.filter((t) => !["gone quiet", "stale"].includes(t.state));
    const quiet = buyers.filter((t) => ["gone quiet", "stale"].includes(t.state));
    const portal = T.filter((t) => t.kind === "portal");
    const other = T.filter((t) => ["supplier", "domestic"].includes(t.kind));
    const t = JACOB.totals;
    return `
      <div class="section"><div class="section-head"><h3>Buyers, mid-conversation</h3></div>
        ${open.length ? this._threadRows(open) : `<div class="empty"><strong>Nothing open</strong></div>`}</div>

      ${quiet.length ? `<div class="section"><div class="section-head"><h3>Buyers who have gone quiet</h3>
        <a data-go="chasing">Chasing &rarr;</a></div>
        ${this._threadRows(quiet)}</div>` : ""}

      ${portal.length ? `<div class="section"><div class="section-head"><h3>Portal notices</h3></div>
        ${this._threadRows(portal)}</div>` : ""}

      <div class="section"><div class="section-head"><h3>Why this list is short</h3></div>
        <div class="planned-note">
          <p>The mailboxes produced <strong>${t.signals}</strong> messages the classifier called
          enquiries. They are <strong>${t.threads}</strong> conversations, and only
          <strong>${t.buyers}</strong> of those are a buyer asking Fenster for something.</p>
          <p>The rest: <strong>${t.supplierThreads}</strong> are fabricators and glass suppliers
          <em>replying to Fenster</em> - a subject line like "Fenster Glazing - Quote - Raj" is
          Fenster asking Truframe for a price, not Truframe asking us for one. Counting those as
          leads inflates the number by two thirds and points Adam at his own supply chain.
          <strong>${t.domestic}</strong> are householders replying to quotes Fenster has already
          issued - real work, but Gintare's, not business development.</p>
          <p>A hundred names nobody will ever call is worse than three companies with a live
          project and a person who knows us. The permanent fix belongs in
          <code>jacob_intake.py</code>'s classifier; today it is done here.</p>
        </div></div>

      ${other.length ? `<div class="section"><div class="section-head"><h3>Not enquiries - listed so the count adds up</h3></div>
        ${this._threadRows(other)}</div>` : ""}`;
  },

  /* ------------------------------------------------ chasing */
  chasing() {
    const out = quotesOut().filter((q) => !jShut(q));
    const quiet = (JACOB.threads || []).filter(
      (t) => t.kind === "buyer" && ["gone quiet", "stale"].includes(t.state) && !jShut(t));
    const total = quotesWaiting().reduce((n, q) => n + poundsOf(q.value), 0);
    return `
      <div class="section"><div class="section-head"><h3>The handover nobody does</h3></div>
        <div class="planned-note">
          <p>Fenster finds it, Mary prices it, the quote goes out - and then nothing happens.
          That second handover, back to business development to chase, is not a job anyone
          currently holds, which is why quotes go quiet and nobody notices.</p>
          <p><strong>${gbp(total)}</strong> is past its return date with no answer recorded.
          Rows still inside their return date, and rows priced but not yet issued, are listed
          too but carry no chase - calling about a quote that never left the building is worse
          than not calling. All of this is read from Mary's job records: she owns them, Jacob
          only looks.</p>
        </div></div>

      <div class="section"><div class="section-head"><h3>Quotes out, no answer recorded</h3></div>
        ${out.length ? `<table class="tbl"><thead><tr>
          <th>Job</th><th>Value</th><th>Return date</th><th>State</th><th>Next action</th><th>Owner</th></tr></thead><tbody>
        ${out.map((q) => `<tr data-jkey="${esc(q.key)}">
          <td class="job-cell"><strong>${esc(q.job)}</strong><small>${esc(q.client)}</small></td>
          <td class="money">${esc(q.value)}</td>
          <td class="num">${esc(q.due)}${q.days > 0 && !q.unsent ? ` <small class="dim">${q.days}d ago</small>` : ""}</td>
          <td>${stateChip(q)}</td>
          <td style="max-width:320px">${inline(jNext(q))}</td>
          <td>${ownerTag(q)}</td></tr>`).join("")}
        </tbody></table>` : `<div class="empty"><strong>Nothing issued and waiting</strong>Either every quote has had an answer, or Mary's board has not been rebuilt.</div>`}</div>

      <div class="section"><div class="section-head"><h3>Enquiries that went quiet</h3></div>
        ${quiet.length ? this._threadRows(quiet)
          : `<div class="empty"><strong>None</strong>Every buyer who wrote in has been answered inside ten days.</div>`}</div>`;
  },

  /* ------------------------------------------------ leads */
  _leadTable(rows, showClient) {
    if (!rows.length) return `<div class="empty"><strong>Nothing here yet</strong></div>`;
    return `<table class="tbl"><thead><tr>
        <th>Winner</th>${showClient ? "<th>Fenster history</th>" : ""}
        <th>What they won</th><th>Value</th><th>Where</th>${showClient ? "<th>Next action</th><th>Owner</th>" : "<th>Awarded</th>"}</tr></thead><tbody>
      ${rows.map((r) => `<tr data-jkey="${esc(r.key)}">
        <td class="job-cell"><strong>${esc(r.supplier)}</strong><small>awarded ${esc(r.awarded) || "date not published"}</small></td>
        ${showClient ? `<td>${esc(r.client)} <span class="pill ${r.confidence}">${r.confidence}</span></td>` : ""}
        <td>${esc(r.title)}</td>
        <td class="money">${gbp(r.total || r.value)}</td>
        <td>${esc(r.area) || "-"}</td>
        ${showClient ? `<td style="max-width:300px">${inline(jNext(r))}</td><td>${ownerTag(r)}</td>`
                     : `<td>${esc(r.awarded) || "-"}</td>`}</tr>`).join("")}
    </tbody></table>`;
  },

  leads() {
    const warm = JACOB.warm.filter((r) => !jShut(r));
    const known = JACOB.known.filter((r) => !jShut(r));
    return `
      <div class="section"><div class="section-head"><h3>They have bought from Fenster, and they have just won work</h3></div>
        <div class="planned-note">A warm name beats a perfect-fit stranger nearly every time.
        In this trade a relationship buys one thing: being asked to price.</div>
        ${this._leadTable(warm, true)}</div>

      <div class="section"><div class="section-head"><h3>Quoted before, never won - and building again</h3></div>
        ${this._leadTable(known, true)}</div>

      <div class="section"><div class="section-head"><h3>Cold - no relationship at all</h3>
        <span class="pill planned">blocked</span></div>
        <div class="planned-note">${JACOB.totals.cold} live building contracts whose winner Fenster
        has never spoken to. Nobody is assigned to any of them: cold approach needs
        <a data-go="decisions">JAC-2</a> answered and a separate sending domain. They are here so
        the moment that changes there is a list to work, not so anyone acts on them today.</div>
        ${this._leadTable(JACOB.cold, false)}</div>

      <div class="section"><div class="section-head"><h3>How a name gets on this page</h3></div>
        <div class="planned-note">
          <p>${JACOB.totals.awardRows.toLocaleString()} construction award rows over
          ${JACOB.window.days} days, ${JACOB.totals.winners.toLocaleString()} unique winners,
          cross-referenced against ${JACOB.totals.clients} client folders in the archive
          (${JACOB.totals.clientsWon} of which actually bought).</p>
          <p>Leads are scored on what a contract <em>is</em> - CPV building families - not what its
          title says. Keyword matching returned window <em>cleaning</em>, STI <em>screening</em>, and
          one award that matched only on the phrase "the front door to maternity services". A notice
          counts only if the award is recent <em>and</em> the job is still running: one published 469
          days late described a contract that had already finished. And anything marked
          <span class="pill possible">possible</span> waits for a human to confirm it once -
          "Atlas" matched a window-cleaning contractor.</p>
          <p><strong>An award is the weakest signal there is.</strong> By the time it publishes the
          main contractor has picked their subcontractors. It is on the board because it is free and
          it names companies; the stage that matters is tender, and that feed is not built.</p>
        </div></div>`;
  },

  /* ------------------------------------------------ companies */
  companies() {
    const r = JACOB.relationships;
    const rows = (r.rows || []).filter((x) => !jShut(x));
    const group = (...states) => rows.filter((x) => states.includes(jState(x)));
    const tbl = (list, cap) => `<table class="tbl"><thead><tr>
        <th>Company</th><th>History</th><th>State</th><th>Next action</th><th>Owner</th><th>Known from</th></tr></thead><tbody>
      ${list.slice(0, cap).map((x) => `<tr data-jkey="${esc(x.key)}">
        <td class="job-cell"><strong>${esc(x.company)}</strong>
          <small>${x.contacts.slice(0, 2).map((c) => esc(c.name || c.address)).join(", ") || "no named contact"
            }${x.contacts.length > 2 ? ` +${x.contacts.length - 2}` : ""}</small></td>
        <td>${x.relationship === "unknown" ? "-" :
             `<span class="pill ${x.relationship === "won" ? "exact"
               : x.relationship === "quoted" ? "strong" : "possible"}">${esc(x.relationship)}</span>`}</td>
        <td>${stateChip(x)}<small class="dim">${esc(x.lastContact) || "no email"}</small></td>
        <td style="max-width:300px">${inline(jNext(x))}</td>
        <td>${ownerTag(x)}</td>
        <td>${x.sources.map((s) => `<span class="pill possible">${esc(s)}</span>`).join(" ")}</td>
      </tr>`).join("")}
    </tbody></table>${list.length > cap ? `<div class="planned-note">Showing ${cap} of ${list.length}. Use the filter box to find a name.</div>` : ""}`;

    const bought = group("dormant - has bought");
    const quiet = group("gone quiet", "stale");
    const talking = group("live", "waiting");
    const cold = group("dormant - quoted only", "no contact on record");
    return `
      <div class="stats">
        <div class="stat amber"><div class="n">${bought.length}</div><div class="l">Have paid Fenster, silent 180 days</div></div>
        <div class="stat red"><div class="n">${quiet.length}</div><div class="l">Went quiet mid-conversation</div></div>
        <div class="stat green"><div class="n">${talking.length}</div><div class="l">Talking to us right now</div></div>
        <div class="stat"><div class="n">${cold.length}</div><div class="l">Quoted once, long ago</div></div>
      </div>

      <div class="section"><div class="section-head"><h3>They bought, then we stopped talking</h3></div>
        <div class="planned-note">
          <p>The cheapest lead in the business. Every one of these paid Fenster for something and
          has not been emailed since. No cold-contact question applies - they are existing
          customers.</p>
          ${bought.filter((x) => !x.contacts.length).length ? `<p><strong>${bought.filter((x) => !x.contacts.length).length}
          of them have no contact address anywhere.</strong> The archive stores a folder with the
          company's name on it, not the person who signed the order, and their mail predates the
          180-day window. Until somebody has a name, these are companies, not leads - which is
          what <a data-go="jayk">Jayk's book</a> is for.</p>` : ""}
        </div>
        ${tbl(bought, 60)}</div>

      <div class="section"><div class="section-head"><h3>Went quiet mid-conversation</h3></div>
        ${tbl(quiet, 40)}</div>

      <div class="section"><div class="section-head"><h3>Currently talking to us</h3></div>
        ${tbl(talking, 40)}</div>

      <div class="section"><div class="section-head"><h3>Quoted once, nothing since</h3></div>
        <div class="planned-note">${cold.length} companies in the archive with a tender folder and
        no email in the 180-day window. Not worth a call each; worth an email the day one of them
        turns up in a feed.</div>
        ${tbl(cold, 40)}</div>`;
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

  /* Outreach had a page of its own and nothing on it was wired up. It is a
     paragraph in the honest answer to "where does this come from", not a
     section of the board someone opens looking for work. */
  sources() {
    const o = JACOB.outreach;
    return `
      <div class="section"><div class="section-head"><h3>The thing worth knowing</h3></div>
        <div class="planned-note">
          <p>Fenster is a <strong>subcontractor</strong>. Almost nothing it wins is advertised - what
          gets published is the main contract the contractor was bidding for. So the job is not
          "find tenders". It is: find the scheme, find who is bidding it, and get Fenster onto their
          enquiry list, ideally before the list is drawn up.</p>
          <p>Every feed below is <strong>public sector only</strong>. Stepnell, Borras, Chigwell,
          Guildmore and Zelltec - real Fenster clients - appear in none of them. That is what
          <a data-go="decisions">JAC-3</a> is about.</p>
        </div></div>

      <div class="section"><div class="section-head"><h3>Feeds</h3></div>
        <table class="tbl"><thead><tr><th>Source</th><th>Status</th><th>Gives us</th><th>Detail</th><th>Cost</th></tr></thead><tbody>
        ${JACOB.sources.map((s) => `<tr>
          <td><strong>${esc(s.name)}</strong></td>
          <td><span class="pill ${s.status === "live" ? "live" : s.status === "planned" ? "planned" : "notstarted"}">${esc(s.status)}</span></td>
          <td>${esc(s.kind)}</td><td>${esc(s.detail)}</td><td>${esc(s.cost)}</td></tr>`).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>Outreach</h3><span class="pill planned">planned</span></div>
        <div class="planned-note"><p>${esc(o.note)}</p></div>
        <table class="tbl"><thead><tr><th>Type</th><th>When it fires</th><th>Example we already have</th><th>Autonomy</th></tr></thead><tbody>
        ${o.classes.map((c) => `<tr>
          <td><strong>${esc(c.name)}</strong></td><td>${esc(c.why)}</td>
          <td>${esc(c.example)}</td><td>${esc(c.autonomy)}</td></tr>`).join("")}
        </tbody></table></div>`;
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
    if (!(a.events || []).length) {
      return `<div class="empty"><strong>Nothing running</strong>When Jacob picks up
        a message or a lead, every step he takes appears here as it happens.</div>`;
    }
    return `
      <div class="live-head">
        <span class="chip warn">working</span>
        <strong>${esc(a.title || "Business development")}</strong>
        <span class="live-when">last step ${esc(feedWhen(a))}</span>
      </div>
      <div class="ev-feed" id="ev-feed">${feedRows(a.events)}</div>`;
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
    if (!(a.events || []).length) {
      return `<div class="empty"><strong>Nothing running</strong>${STATUS?.state === "working"
        ? "Mary is working - her first step will appear here in a moment."
        : "When Mary picks up a job, everything she does appears here as it happens."}</div>`;
    }
    const c = maryChip();
    return `
      <div class="live-head">
        <span class="chip ${c.tone}">${c.text}</span>
        <strong>${esc(a.title || a.chat || "")}</strong>
        <span class="live-when">last step ${esc(feedWhen(a))}</span>
      </div>
      <div class="ev-feed" id="ev-feed">${feedRows(a.events)}</div>`;
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
  $$("#page tr[data-job], #page tr[data-jkey], #page .act, #page .req, #page .mail-row, #page .catch, #page .bubble").forEach((el) => {
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

  // Jacob's Send. This was missing entirely: the button rendered and did
  // nothing, because the patch that added it anchored on a selector that does
  // not exist in this file and silently replaced nothing.
  const jsend = $("#jacob-send");
  if (jsend) jsend.addEventListener("click", async () => {
    const ta = $('[data-draft="jacob-msg"]');
    const text = (ta?.value || "").trim();
    if (!text) return;
    jsend.disabled = true;
    try {
      await sendToJacob(text);
      delete DRAFTS["jacob-msg"];
      if (ta) ta.value = "";
      render();
    } catch {
      toast("Could not send that");
      jsend.disabled = false;
    }
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
  // Picking a state or an owner inside Jacob's edit panel. Must come before
  // the generic .req-options handler below, which assumes a .req card around
  // it and throws on anything else.
  const pick = e.target.closest(".opt[data-pick]");
  if (pick) {
    [...pick.parentElement.querySelectorAll(".opt")]
      .forEach((o) => o.classList.toggle("sel", o === pick));
    return;
  }
  // Any row on Jacob's board with a key: open it and correct it.
  const jrow = e.target.closest("[data-jkey]");
  if (jrow) { crmPanel(jrow.dataset.jkey); return; }
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
    let pipe = [];
    [JMSGS, JREQS, BOTCHAT, pipe] = await Promise.all([
      api("jacob/messages").catch(() => []),
      api("jacob/requests").catch(() => []),
      api("botchat").catch(() => []),
      // No edits yet is the normal state on a fresh board, not a failure.
      api("jacob/pipeline").catch(() => []),
    ]);
    JPIPE = Object.fromEntries(pipe.map((r) => [r.key, r]));
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
        // Patch the feed if it is on screen; render() only for the first
        // paint or when coming out of the empty state.
        if (!paintFeed(fresh)) render();
      } catch {}
    }, 3000);

    setInterval(async () => {
      if (page !== "live") return;
      try {
        const fresh = await api("activity");
        if (JSON.stringify(fresh) === JSON.stringify(ACTIVITY)) return;
        ACTIVITY = fresh;
        if (!paintFeed(fresh, maryChip())) render();
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

    // The same beat for Jacob's channels. Without this his replies only
    // appeared on a page reload, which made the Messages tab look broken:
    // you sent something and nothing ever came back.
    let jacobSig = "";
    setInterval(async () => {
      if (BOT !== "jacob") return;
      if (!["jmessages", "botchat", "decisions", "overview"].includes(page)) return;
      try {
        const [msgs, chat, reqs] = await Promise.all([
          api("jacob/messages").catch(() => JMSGS),
          api("botchat").catch(() => BOTCHAT),
          api("jacob/requests").catch(() => JREQS),
        ]);
        const sig = [msgs.length, chat.length, reqs.length,
                     msgs[0]?.id, chat[0]?.id,
                     reqs.filter((r) => r.status !== "answered").length].join(":");
        if (sig === jacobSig) return;   // nothing new - never redraw over the user
        jacobSig = sig;
        JMSGS = msgs; BOTCHAT = chat; JREQS = reqs;
        render();
      } catch {}
    }, 10000);
  } catch (err) {
    $("#page").innerHTML = `<div class="empty"><strong>Could not load the hub</strong>${err.status || err.message}</div>`;
  }
})();
