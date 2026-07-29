/* Fenster Hub - every bot on one board.
   Single-page app over the hub API. Each bot has a board (deployed state), a
   two-way message line (D1), a decisions queue, and a live feed; the Team view
   above them shows everything that needs a human, across all of them at once.
   Anything written here is picked up by that bot's bridge within seconds.

   ADDING A BOT: one entry in the BOTS registry below (pages + render map +
   channel accessors), one entry in the API's CHANNELS registry, tables in
   schema.sql. The sidebar, nav, routing, polling and badges all derive from
   the registry - nothing else in this file should need to know the bot. */

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];

let DATA = null;
let MESSAGES = [];
let page = "home";
let commsTab = "sent";
/* BOT decides which board is on screen: "team", or a bot's key. Mary's data
   lives in DATA, Jacob's in JACOB, and neither reads the other. */
let BOT = "team";
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

/* The live pill on a bot's sidebar card: what its bridge is doing this
   second. Returns {text, tone, title} so the card renderer stays generic. */
function bridgeStatus(s) {
  s = s || {};
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
  return { text, tone, title: [s.title, s.detail].filter(Boolean).join(" - ") };
}

/* The whole left-hand column of bot cards, generated from the registry.
   Regenerated whenever a status or badge changes - the cards hold no input
   state, so a rebuild can never eat anything a human was doing. */
function renderSidebar() {
  const host = $("#bot-cards");
  if (!host) return;
  host.innerHTML = Object.values(BOTS).filter((b) => !b.hidden).map((b) => {
    const s = b.status ? b.status() : null;
    const n = b.needsYou ? b.needsYou() : 0;
    return `<button class="nav-mary nav-bot" data-bot="${b.key}" type="button">
      <div class="avatar ${b.accent || ""}">${b.initials}</div>
      <div>
        <strong>${b.name}${n ? `<span class="card-badge" title="Waiting on a human">${n}</span>` : ""}</strong>
        <span class="role">${b.role}</span>
        ${s ? `<span class="live"><i class="dot ${s.tone}"></i> <span class="bot-state" title="${esc(s.title)}">${esc(s.text)}</span></span>` : ""}
        ${b.updatedLine ? `<span class="live-when">${esc(b.updatedLine() || "")}</span>` : ""}
      </div>
    </button>`;
  }).join("");
  $$(".nav-bot").forEach((el) => el.classList.toggle("active", el.dataset.bot === BOT));
  // The sidebar is a drawer on a phone, so Mary's state has to live in the top
  // bar too - otherwise "is she working right now" costs you a tap.
  const m = bridgeStatus(STATUS);
  const dotM = $("#mary-dot-m");
  if (dotM) { dotM.className = `dot ${m.tone}`; dotM.title = m.text; }
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
  // Mary writes **emphasis** constantly - job statuses, request bodies. It
  // used to reach the page as literal asterisks, which reads as a glitch.
  h = h.replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>");
  // Any number of decimals plus an optional m/k suffix, otherwise "GBP 14.9m"
  // renders as a highlighted "GBP 14" trailed by a stray ".9m".
  h = h.replace(/((?:GBP\s?|£)[\d,]+(?:\.\d+)?(?:\s?[mk])?)\b/gi, '<span class="money">$1</span>');
  return h;
}

/* A request is a DECISION, so the buttons are the point of the card and they go
   first; the reasoning sits underneath, folded.

   The card used to run title -> why -> needs -> buttons. On 29/07 the open
   requests carried 29,004 characters of why-and-needs between them - REQ-32's
   "why" alone was 3,969 - which on a phone put the thing Adam has to click
   about eight hundred words below the fold. That is the same as not shipping it.

   Open when it is short: a two-line "needs" is not worth a click, a
   seventeen-hundred-character one is.

   And fmt(), not inline(). inline() only escapes and highlights money, so every
   bullet Mary wrote in a request was being flattened into one grey slab.
   Messages have always used fmt; requests never did. */
function reqDetail(label, text, openBelow) {
  const body = String(text || "").trim();
  if (!body) return "";
  const isOpen = openBelow > 0 && body.length < openBelow;
  return `<details class="req-detail"${isOpen ? " open" : ""}>
    <summary>${esc(label)}${isOpen ? "" : ` <span class="req-len">${body.length > 900 ? "long" : "detail"}</span>`}</summary>
    ${fmt(body)}
  </details>`;
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
/* Every `created` in D1 is new Date().toISOString() - i.e. UTC with a Z. Slicing
   the string (which this file used to do in five places) published UK times an
   hour early all through BST: Adam sent a message at 22:07 and the thread said
   21:07. Always go through these. Europe/London is pinned rather than left to
   the browser so the board reads the same from anywhere. */
const UK = "Europe/London";
const ukTime = (iso) => iso ? new Date(iso).toLocaleTimeString("en-GB", { timeZone: UK, hour: "2-digit", minute: "2-digit" }) : "";
const ukDay = (iso) => iso ? new Date(iso).toLocaleDateString("en-GB", { timeZone: UK, weekday: "long", day: "numeric", month: "long" }) : "";
const ukShortDay = (iso) => iso ? new Date(iso).toLocaleDateString("en-GB", { timeZone: UK, day: "2-digit", month: "short" }) : "";
const ukStamp = (iso) => iso ? `${ukShortDay(iso)} ${ukTime(iso)}` : "";
const openReqs = () => (DATA.requests || []).filter((r) => r.status === "open");
/* Still needing a human - one you have already answered is with Mary, not you. */
const awaitingReqs = () => openReqs().filter((r) => !SENT_ANSWERS[r.id]);
const unseenMsgs = () => MESSAGES.filter((m) => m.author !== "mary" && !m.seen_by_mary).length;
const unseenJacobMsgs = () => JMSGS.filter((m) => m.author !== "jacob" && !m.seen_by_jacob).length;

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

/* ---------------- shared chat ----------------
   One renderer for every human <-> bot thread; the per-bot config lives on the
   BOTS registry. Jacob's thread used to be a diverged copy with bubble classes
   no stylesheet rule matched, so his messages rendered unstyled - the shared
   renderer is how that class of drift stops happening.
   (.bubble.mary is the navy "the bot said this" style; the class name predates
   the second bot and is not worth a CSS migration.) */
function chatPage(bot) {
  const c = bot.chat;
  const thread = [...c.msgs()].reverse();
  let lastDay = "";
  const parts = [];
  for (const m of thread) {
    /* Group by the UK day, not the UTC one - a message sent at 00:30 BST
       lands at 23:30Z the day before and would file under yesterday. */
    const day = ukDay(m.created);
    if (day !== lastDay) { parts.push(`<div class="chat-day">${esc(day)}</div>`); lastDay = day; }
    const mine = m.author !== bot.key;
    const pending = mine && !m[c.seen];
    parts.push(`<div class="bubble ${mine ? "human" : "mary"}${pending ? " pending" : ""}">
      <div class="who">${esc((mine ? m.author : bot.name).toUpperCase())} <time>${esc(ukTime(m.created))}</time>
      ${pending ? `<span class="wait-note">waiting for ${esc(bot.name.split(" ")[0])}</span>` : ""}</div>
      ${m.context ? `<span class="ctx">${esc(m.context)}</span>` : ""}${fmt(m.body)}</div>`);
  }
  return `<div class="chat">
    <div class="chat-thread">${parts.length ? parts.join("") : `<div class="empty"><strong>No messages yet</strong>${c.empty}</div>`}</div>
    <div class="chat-compose">
      <textarea data-draft="${c.draft}" placeholder="${c.placeholder}"></textarea>
      <div class="chat-actions"><span class="chat-hint">Sending as <strong>${esc(who())}</strong> &middot; ${c.hint()}</span>
      <button class="btn" data-chatsend="${bot.key}">Send</button></div>
    </div></div>`;
}

/* What the bots say to each other. Lives on the Team board - it is a channel
   between two of them, not a page of either. Mary reads navy, everyone else
   white, same vocabulary as the human threads. */
function botchatPage() {
  const rows = [...BOTCHAT].reverse();
  return `
    <details class="req-detail"><summary>How this works</summary>
      <div class="planned-note">
        <p>Jacob knows who is buying; Mary knows what is being quoted. This is the line
        between them, and everything on it is visible to you.</p>
        <p><strong>Ten messages an hour each</strong>, refused by the API beyond that -
        a wall rather than an instruction, because two agents with something to say will
        otherwise talk all night. And <strong>neither has to reply</strong>: a message
        marked FYI gets no answer unless the other has something to add. Silence is the
        normal outcome.</p>
      </div></details>
    <div class="chat">
      <div class="chat-thread">
        ${rows.length ? rows.map((m) => `
          <div class="bubble ${m.sender === "mary" ? "mary" : "human"}">
            <div class="who">${esc((BOTS[m.sender]?.name || m.sender).toUpperCase())}
              &rarr; ${esc(BOTS[m.recipient]?.name || m.recipient)}
              <time>${esc(ukStamp(m.created))}</time>
              ${m.wants_reply ? `<span class="pill strong">wants a reply</span>`
                              : `<span class="pill possible">FYI</span>`}</div>
            ${m.subject ? `<div><strong>${esc(m.subject)}</strong></div>` : ""}
            ${fmt(m.body)}
          </div>`).join("")
          : `<div class="empty"><strong>They have not spoken yet</strong>Nothing to report to each other is a perfectly good state.</div>`}
      </div>
    </div>`;
}

/* One live feed page for every bot - the markup #ev-feed polling patches. */
function livePage(a, chip, fallbackTitle, empty) {
  if (!((a || {}).events || []).length) {
    return `<div class="empty"><strong>Nothing running</strong>${empty}</div>`;
  }
  return `
    <div class="live-head">
      <span class="chip ${chip.tone}">${chip.text}</span>
      <strong>${esc(a.title || a.chat || fallbackTitle)}</strong>
      <span class="live-when">last step ${esc(feedWhen(a))}</span>
    </div>
    <div class="ev-feed" id="ev-feed">${feedRows(a.events)}</div>`;
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
  drafts: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 20h4L19 9a2.8 2.8 0 0 0-4-4L4 16Z"/><path d="M14.5 5.5 18.5 9.5"/></svg>',
  chaselist: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 7v5l3 2"/><path d="M3.5 12a8.5 8.5 0 1 0 2.2-5.7"/><path d="M3 4v4h4"/></svg>',
  tenders: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 3h8l4 4v14H6Z"/><path d="M14 3v4h4"/><path d="M9 13h6M9 17h4"/></svg>',
  outcomes: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 20h16"/><rect x="6" y="11" width="3" height="6"/><rect x="11" y="7" width="3" height="10"/><rect x="16" y="13" width="3" height="4"/></svg>',
  botchat: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 10h8M8 14h5"/><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8A2.5 2.5 0 0 1 17.5 16H9l-5 5Z"/></svg>',
  jayk: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v18H6.5A2.5 2.5 0 0 1 4 18.5Z"/><path d="M8 7h8M8 11h8"/></svg>',
  sources: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>',
  enquiries: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 11a9 9 0 0 1 9-9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1.5"/></svg>',
  chasing: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/></svg>',
  companies: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><path d="M17 8.5a3 3 0 0 1 0 5"/><path d="M19.5 20a5.5 5.5 0 0 0-3-4.9"/></svg>',
  home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 10 9-7 9 7"/><path d="M5 8.5V21h14V8.5"/><path d="M10 21v-6h4v6"/></svg>',
};
/* Pages that share an icon point at it with `icon:` on their nav entry -
   the SVGs above exist once each. */

const PAGES = [
  { key: "overview", label: "Overview", group: "Work", sub: () => "Everything Mary is holding, at a glance" },
  { key: "pipeline", label: "Pipeline", group: "Work", sub: () => "Every live tender, most urgent first" },
  { key: "requests", label: "Mary needs you", group: "Work", sub: () => `${awaitingReqs().length} decision${awaitingReqs().length === 1 ? "" : "s"} she cannot make without a human` },
  { key: "messages", label: "Messages", group: "Talk", layout: "chat", sub: () => "Two-way line - she picks up what you write within seconds" },
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
  // Chasing sits second on purpose. A quote already out is money Fenster has
  // spent and can still lose; an enquiry is money it has not spent yet.
  { key: "chasing", label: "Chasing", group: "Work", sub: () => JACOB?.handover
      ? `${JACOB.totals.handoverIssued} quotes issued and with a client, ${JACOB.totals.handoverDue} chaseable today`
      : `${quotesWaiting().length} quotes past their return date, ${JACOB?.totals.quietBuyers || 0} enquiries gone quiet` },
  // Drafts sit directly under Chasing because they are the same work one step
  // further on: the chase, written. The only thing left is a human sending it.
  { key: "drafts", label: "Ready to send", group: "Work", sub: () => `${jdrafts().length} drafts written, waiting for a human to send them` },
  { key: "chaselist", label: "Chase list", group: "Work", sub: () => crm()
      ? `${crm().totals.due} quoted jobs nobody has been back to, out of ${crm().totals.rows} in AdminBase`
      : "AdminBase has not been read yet" },
  { key: "enquiries", label: "Enquiries", group: "Work", sub: () => `${JACOB?.totals.buyers || 0} live conversations with a buyer, out of ${JACOB?.totals.signals || 0} raw messages` },
  { key: "tenders", label: "Out to bid", group: "Work", sub: () => `${JACOB?.totals.tenders || 0} contracts still open, ${JACOB?.totals.tendersClosing || 0} closing inside a week` },
  { key: "leads", label: "Leads", group: "Work", sub: () => `${(JACOB?.totals.warm || 0) + (JACOB?.totals.known || 0)} winners Fenster knows, ${JACOB?.totals.cold || 0} it does not` },
  // Reference, not work: what the history says, who Fenster knows, and the
  // book recovered from the last BDM. Grouped apart so the seven pages where
  // money moves are not visually equal to the three you read once a week.
  { key: "outcomes", label: "What we win", group: "Know", sub: () => JACOB?.outcomes ? `${JACOB.outcomes.summary.won} won, ${JACOB.outcomes.summary.lost} lost - a ${JACOB.outcomes.summary.winRate}% win rate over two years` : "The Opportunity Log has not been read yet" },
  { key: "companies", label: "Companies", group: "Know", sub: () => `${JACOB?.relationships.total || 0} companies, ${JACOB?.totals.dormantWon || 0} who have paid us and gone silent` },
  { key: "jayk", label: "Jayk's book", group: "Know", icon: "jayk", sub: () => `${JACOB?.totals.jaykContacts || 0} contacts recovered from the former BDM` },
  { key: "jmessages", label: "Messages", group: "Talk", icon: "messages", layout: "chat", sub: () => "Two-way line - he picks up what you write on his next pass" },
  { key: "decisions", label: "Jacob needs you", group: "Talk", icon: "requests", sub: () => `${openJacobReqs().length} open, ${JACOB?.decisions.length || 0} standing` },
  { key: "sources", label: "How this works", group: "System", sub: () => "Where leads come from, what is wired up, and what still is not" },
  { key: "jlive", label: "Live", group: "System", icon: "live", sub: () => "What Jacob is doing right now" },
];

/* Jacob's own channels. Loaded alongside his board; a failure here leaves the
   rest of his section working rather than blanking the page. */
let JMSGS = [];
let JREQS = [];
let BOTCHAT = [];
let JACTIVITY = null;
/* His bridge can report a status line the same way Mary's does; until it
   starts doing so this stays "unknown" and the card infers from the feed. */
let JSTATUS = null;
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

/* ---------------- The handover register ----------------
   Adam's rule, 28/07/2026: a job is Mary's while it is being priced and
   Jacob's the moment the quote goes out. These rows are that boundary, and
   every issue date on them was read out of the message that actually left
   estimating@ rather than inferred from a job record.

   That distinction is the whole point. quotesOut() below derives its chase
   state from the tender *return* date, which is a different date on a
   different clock, and it got three of the seven wrong: Gordon Court showed
   as "not due until 16 September" while a GBP 368k quote sat unanswered for
   eighteen days, and Chester Thomas showed as never issued when it had gone
   out on the 27th. Verified rows win; unverified ones still show, marked. */
/* ---------------- AdminBase and the drafts ----------------
   Adam exported the CRM to Jacob on 28/07. It sees 264 quoted leads back to
   May 2025 - most of them older than any window this board reads, and
   therefore invisible to it until now.

   Two things to keep straight when reading anything below. Its VALUE column
   is inclusive of VAT and every quote Fenster issues is exclusive of it, so
   these figures are de-VATed and will not match the CSV. And "Live - Quoted"
   is what the CRM says, not what the client says: 212 of the 264 rows qualify
   as chaseable, which is a statement about a system that closes nothing
   rather than about 212 live opportunities. */
const crm = () => JACOB?.adminbase || null;
const jdrafts = () => (JACOB?.drafts?.drafts || []).filter((d) => !jShut({ key: "draft:" + d.id }));

const hand = () => JACOB?.handover || null;
const handIssued = () => (hand()?.issued || []).filter((r) => !jShut(r));
const handHeld = () => (hand()?.held || []).filter((r) => !jShut(r));
const handKeys = () => new Set([...(hand()?.issued || []), ...(hand()?.held || [])].map((r) => r.key));
/* Chaseable today: out, not blocked by something the client cannot control,
   and nothing back from them for a week. */
const handDue = () => handIssued().filter(
  (r) => !r.blocked && (r.daysSinceClient === null || r.daysSinceClient >= 7) && (r.daysOut || 0) >= 7);

/* Mary's board, read only. Her job records are the only place jobs that have
   NOT reached the register still exist. Everything here is defensive: her
   file is hers and its shape can change. */
function quotesOut() {
  // Priced and approved is not the same as sent, and "not yet priced" is
  // neither. Both tests are anchored on the stage rather than the value, so a
  // value reading "not yet priced" cannot match the word "priced" and land an
  // unpriced tender on a chase list. Unsent is checked first: "approved to
  // issue" jobs carry a quoted value and have still not gone anywhere.
  const isUnsent = (j) => /approved to issue|awaiting send|drafted|priced -/i.test(j.stage || "");
  const isOut = (j) => /submitted/i.test(j.stage || "") || /\b(quoted|tendered)\b/i.test(j.value || "");
  const known = handKeys();
  const jobs = (DATA?.jobs || []).filter((j) => isUnsent(j) || isOut(j))
    // Anything the register has verified is shown from there, once.
    .filter((j) => !known.has(`job:${String(j.job).toLowerCase().replace(/[^a-z0-9]+/g, "-").slice(0, 50)}`));
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
    // Verified sends where we have them; the old return-date guess only as a
    // fallback, because a headline number ought to be the sourced one.
    const outValue = t.handoverValue || quotesWaiting().reduce((n, q) => n + poundsOf(q.value), 0);
    return `
      <div class="stats">
        <div class="stat ${mine("Adam") ? "red" : "green"}"><div class="n">${mine("Adam")}</div><div class="l">Waiting on Adam - a call or a decision</div></div>
        <div class="stat amber" data-go="chasing"><div class="n">${gbpShort(outValue)}</div><div class="l">Issued and waiting on an answer, ${t.handoverDue ?? "?"} chaseable today</div></div>
        <div class="stat amber" data-go="enquiries"><div class="n">${t.liveBuyers}</div><div class="l">Buyers mid-conversation right now</div></div>
        <div class="stat ${t.tendersClosing ? "red" : ""}" data-go="tenders"><div class="n">${t.tenders || 0}</div><div class="l">Contracts still out to bid, ${t.tendersClosing || 0} closing this week</div></div>
        <div class="stat" data-go="outcomes"><div class="n">${t.winRate ?? "-"}%</div><div class="l">Win rate, and nothing won over ${gbpShort(t.noWinAbove)}</div></div>
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
          <p><strong>Ten quotes are now the exception.</strong> Mary read estimating@ sent
          items on 28/07 and dated every one of them against the message that actually left
          the building, so the <a data-go="chasing">Chasing</a> page is sourced rather than
          inferred. It found three errors, including a quote this board was calling "not yet
          issued" that had gone out the day before. Everything not on that register is still
          dated off a return date and should be read as a guess.</p>
          ${(t.mailExcluded || []).length ? `<p><strong>info@ is off the list.</strong>
          ${(t.mailExcluded || []).map((m) => `${esc(m.mailbox)} - ${esc(m.why)}`).join("; ")}.
          That is Adam's instruction of 28/07 and it removes about three quarters of the raw
          message volume, nearly all of it residential. The one thing it also removes is
          portal notices: 79 of 88 arrived at info@. All 79 were Hightown, who are
          do-not-quote, so nothing is lost today - see <a data-go="sources">JAC-7</a>.</p>` : ""}
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
          ${t.stage === "decided" ? ` <span class="pill exact">they have answered</span>` : ""}
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
    const decided = buyers.filter((t) => t.stage === "decided");
    const t = JACOB.totals;
    return `
      ${decided.length ? `<div class="section"><div class="section-head"><h3>They have told us the answer</h3>
        <span class="page-sub">Won or lost, somebody has said what happened - nothing else on this board is that certain</span></div>
        <div class="planned-note">These were being filed as ordinary correspondence. A client
        writing "the works were awarded to an alternative contractor" or "we can proceed with
        Fenster Glazing" uses none of the words a quote request uses, so the classifier never
        saw them. Each one of these also closes or corrects a row in the Opportunity Log.</div>
        ${this._threadRows(decided)}</div>` : ""}

      <div class="section"><div class="section-head"><h3>Buyers, mid-conversation</h3></div>
        ${open.length ? this._threadRows(open) : `<div class="empty"><strong>Nothing open</strong></div>`}</div>

      ${quiet.length ? `<div class="section"><div class="section-head"><h3>Buyers who have gone quiet</h3>
        <a data-go="chasing">Chasing &rarr;</a></div>
        ${this._threadRows(quiet)}</div>` : ""}

      ${portal.length ? `<div class="section"><div class="section-head"><h3>Portal notices</h3></div>
        ${this._threadRows(portal)}</div>` : ""}

      <div class="section"><div class="section-head"><h3>Why this list is short</h3></div>
        <div class="planned-note">
          <p>One mailbox now, not four. Adam took info@ off the list on 28/07 - it belongs to
          the residential team and anything commercial gets forwarded to commercial@. That
          removed about three quarters of the raw volume, and it was the right call: 22% of the
          senders in info@ were hotmail and gmail addresses, against 4% in commercial@.</p>
          <p>What is left produced <strong>${t.signals}</strong> signals over 180 days. They are
          <strong>${t.threads}</strong> conversations, and <strong>${t.buyers}</strong> of those
          are a buyer asking Fenster for something. The board shows the last
          <strong>${t.boardDays}</strong> days of them; ${t.signalsOlder} older signals are held
          back rather than deleted.</p>
          <p>Suppliers (<strong>${t.supplierThreads}</strong>) and householders
          (<strong>${t.domestic}</strong>) are listed at the bottom so the count adds up. A
          subject line like "Fenster Glazing - Quote - Raj" is Fenster asking Truframe for a
          price, not Truframe asking us for one - counting those as leads points Adam at his
          own supply chain.</p>
          <p>A hundred names nobody will ever call is worse than three companies with a live
          project and a person who knows us.</p>
        </div></div>

      ${other.length ? `<div class="section"><div class="section-head"><h3>Not enquiries - listed so the count adds up</h3></div>
        ${this._threadRows(other)}</div>` : ""}`;
  },

  /* ------------------------------------------------ chasing */
  chasing() {
    const h = hand();
    const out = quotesOut().filter((q) => !jShut(q));
    const quiet = (JACOB.threads || []).filter(
      (t) => t.kind === "buyer" && ["gone quiet", "stale"].includes(t.state) && !jShut(t));
    const total = quotesWaiting().reduce((n, q) => n + poundsOf(q.value), 0);
    const t = h?.totals || {};

    /* One row of the register. The day count and the next action are
       deliberately not the same thing: Gordon Court is the longest silence on
       the board and the one row nobody should ring about yet, because the
       client is waiting on jLiving and physically cannot answer. A board that
       cannot say that just tells Adam to make a call that wastes a
       relationship. */
    const hrow = (r) => `<tr data-jkey="${esc(r.key)}">
      <td class="job-cell"><strong>${esc(r.job)}</strong>
        <small>${esc(r.client)}${r.contact && r.contact !== r.client ? ` &middot; ${esc(r.contact)}` : ""}</small></td>
      <td class="money">${gbp(r.value)}</td>
      <td class="num"><strong>${esc(niceDate(r.issued))}</strong>
        <small class="dim">${r.daysOut === 0 ? "today" : `${r.daysOut}d ago`}</small></td>
      <td class="num">${r.lastClientContact
        ? `${esc(niceDate(r.lastClientContact))}<small class="dim">${r.daysSinceClient}d</small>`
        : `<small class="dim">nothing back</small>`}</td>
      <td>${stateChip(r)}${r.blocked ? ` <span class="chip">cannot answer yet</span>` : ""}</td>
      <td style="max-width:340px">${inline(jNext(r))}
        ${r.blockedReason ? `<small class="dim">${esc(r.blockedReason)}</small>` : ""}
        ${r.retender ? `<small class="dim">Re-tender: ${esc(r.retender.note)}</small>` : ""}</td>
      <td>${ownerTag(r)}</td></tr>`;

    return `
      ${h ? `<div class="stats">
        <div class="stat" data-go="chasing"><div class="n">${gbpShort(t.issuedValue)}</div><div class="l">Issued and with a client - ${t.issued} quotes</div></div>
        <div class="stat ${t.due ? "red" : "green"}"><div class="n">${t.due}</div><div class="l">Chaseable today, ${gbpShort(t.dueValue)}</div></div>
        <div class="stat"><div class="n">${t.oldest}d</div><div class="l">Longest a quote has been out</div></div>
        <div class="stat amber"><div class="n">${gbpShort(t.heldValue)}</div><div class="l">Priced but never issued - not chaseable</div></div>
      </div>` : ""}

      <div class="section"><div class="section-head"><h3>The handover, now somebody's job</h3></div>
        <div class="planned-note">
          ${h ? `<p><strong>Adam's rule, ${esc(niceDate(h.rule?.date))}:</strong> ${esc(h.rule?.text)}
          The seven below have gone out, so they are Jacob's. The three under them have not,
          so they are not - and calling a client about a quote that never left the building is
          worse than not calling.</p>
          <p><strong>Every issue date here was read out of the sent message, not inferred.</strong>
          ${esc(h.verification?.source)}. That matters because the page used to date these off the
          tender return date, which is a different date on a different clock, and it got three of
          the seven wrong. ${esc(h.verification?.timezone)}</p>`
          : `<p>The verified register has not been built.
             <code>data/jacob/handover.json</code></p>`}
        </div></div>

      ${h ? `<div class="section"><div class="section-head"><h3>Issued - these are Jacob's</h3>
        <span class="page-sub">Longest silence first. A day count is not on its own an instruction.</span></div>
        <table class="tbl"><thead><tr>
          <th>Job</th><th>Value</th><th>Issued</th><th>Last heard</th><th>State</th>
          <th>Next action</th><th>Owner</th></tr></thead><tbody>
        ${handIssued().map(hrow).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>Not issued - not Jacob's, and not chaseable</h3></div>
        <table class="tbl"><thead><tr>
          <th>Job</th><th>Value</th><th>Held by</th><th>Why it is not out</th></tr></thead><tbody>
        ${handHeld().map((r) => `<tr data-jkey="${esc(r.key)}">
          <td class="job-cell"><strong>${esc(r.job)}</strong><small>${esc(r.client)}</small></td>
          <td class="money">${r.value ? gbp(r.value) : "not published"}</td>
          <td>${ownerTag(r)}</td>
          <td style="max-width:420px">${inline(jNext(r))}
            ${r.caveat ? `<small class="dim">${esc(r.caveat)}</small>` : ""}</td></tr>`).join("")}
        </tbody></table></div>

      ${(h.corrections || []).length ? `<div class="section"><div class="section-head">
        <h3>What this board had wrong until 28/07</h3></div>
        <table class="tbl"><thead><tr><th>It said</th><th>It is</th><th>Why it happened</th></tr></thead><tbody>
        ${h.corrections.map((c) => `<tr><td>${esc(c.was)}</td><td><strong>${esc(c.now)}</strong></td>
          <td class="dim">${esc(c.why)}</td></tr>`).join("")}
        </tbody></table></div>` : ""}` : ""}

      ${out.length ? `<div class="section"><div class="section-head"><h3>Priced jobs not yet in the register</h3>
        <span class="page-sub">Dated off a return date, not a send. Treat the day counts as a guess until verified.</span></div>
        <table class="tbl"><thead><tr>
          <th>Job</th><th>Value</th><th>Return date</th><th>State</th><th>Next action</th><th>Owner</th></tr></thead><tbody>
        ${out.map((q) => `<tr data-jkey="${esc(q.key)}">
          <td class="job-cell"><strong>${esc(q.job)}</strong><small>${esc(q.client)}</small></td>
          <td class="money">${esc(q.value)}</td>
          <td class="num">${esc(q.due)}${q.days > 0 && !q.unsent ? ` <small class="dim">${q.days}d ago</small>` : ""}</td>
          <td>${stateChip(q)}</td>
          <td style="max-width:320px">${inline(jNext(q))}</td>
          <td>${ownerTag(q)}</td></tr>`).join("")}
        </tbody></table></div>` : ""}

      <div class="section"><div class="section-head"><h3>Enquiries that went quiet</h3></div>
        ${quiet.length ? this._threadRows(quiet)
          : `<div class="empty"><strong>None</strong>Every buyer who wrote in has been answered inside ten days.</div>`}</div>`;
  },

  /* ------------------------------------------------ out to bid
     The only stage at which a subcontractor can still get onto an enquiry
     list. Sorted by closing date and nothing else - a big one closing in six
     weeks is worth less than a small one closing on Friday, because the list
     on the small one is being drawn up now. */
  tenders() {
    if (!JACOB.tenders) {
      return `<div class="planned-note">The tender feed has not run yet.
        <code>python scripts/jacob_tenders.py</code></div>`;
    }
    const rows = JACOB.tenders.filter((t) => !jShut(t));
    const direct = rows.filter((t) => t.tier === "direct");
    const main = rows.filter((t) => t.tier === "main-contract");
    const loose = rows.filter((t) => t.tier === "text-only");
    const f = JACOB.tenderFeed || {};
    const tbl = (list, empty) => list.length ? `<table class="tbl"><thead><tr>
        <th>Closes</th><th>What it is</th><th>Buyer</th><th>Value</th>
        <th>Next action</th><th>Owner</th></tr></thead><tbody>
      ${list.map((t) => `<tr data-jkey="${esc(t.key)}">
        <td class="num"><strong>${esc(t.closes) || "no date"}</strong>
          ${t.daysLeft !== null && t.daysLeft !== undefined
            ? `<small class="dim">${t.daysLeft}d left</small>` : ""}</td>
        <td class="job-cell"><strong>${t.url ? `<a href="${esc(t.url)}" target="_blank" rel="noopener">${esc(t.title)}</a>` : esc(t.title)}</strong>
          <small>${esc(t.why)}${t.regions?.length ? ` &middot; ${esc(t.regions[0])}` : ""}</small></td>
        <td>${esc(t.buyer)}${t.record ? ` <span class="pill ${t.record.won ? "exact" : "strong"}">${t.record.won}W ${t.record.lost}L with us</span>` : ""}</td>
        <td class="money">${gbp(t.value)}
          ${t.fit?.note ? `<small class="dim">${esc(t.fit.note)}</small>` : ""}</td>
        <td style="max-width:320px">${inline(jNext(t))}</td>
        <td>${ownerTag(t)}</td></tr>`).join("")}
      </tbody></table>` : `<div class="empty"><strong>${empty}</strong></div>`;

    return `
      <div class="section"><div class="section-head"><h3>Fenster can price these itself</h3>
        <span class="page-sub">The buyer is asking for glazing work by name</span></div>
        <div class="planned-note">Matched on the CPV codes Adam gave on 28/07/2026.
        These are the only notices where Fenster is the contractor being asked, rather than
        a package inside somebody else's contract.</div>
        ${tbl(direct, "Nothing open in this tier today")}</div>

      <div class="section"><div class="section-head"><h3>Main contracts with a glazing package in them</h3>
        <span class="page-sub">Fenster cannot bid these - the job is finding who is</span></div>
        ${tbl(main, "Nothing open in this tier today")}</div>

      ${loose.length ? `<div class="section"><div class="section-head"><h3>Matched on wording only - read before acting</h3></div>
        <div class="planned-note">No useful CPV code, so these matched on the words in the
        notice. Words lie: keyword matching has previously returned window <em>cleaning</em>,
        STI <em>screening</em>, and one contract that matched only on the phrase "the front
        door to maternity services".</div>
        ${tbl(loose, "None")}</div>` : ""}

      <div class="section"><div class="section-head"><h3>How thin this feed really is</h3></div>
        <div class="planned-note">
          <p>Contracts Finder publishes roughly <strong>eleven</strong> tender-stage notices a
          day across every sector, against about <strong>110</strong> award notices. Over
          ${esc(f.from || "the window")} to today, ${Object.entries(f.sources || {}).map(([k, v]) =>
            `<strong>${esc(k)}</strong> returned ${v.releases ?? "?"} releases`).join(", ")},
          and <strong>${rows.length}</strong> of them survived the filter.</p>
          <p>That is not a bug and it is not a small number for the wrong reason: almost
          nothing Fenster actually wins is publicly advertised, because it is a subcontractor.
          This feed is worth running because the few it finds are live, not because it is
          where the work is. The work is in the mailbox and in who is bidding.</p>
        </div></div>`;
  },

  /* ------------------------------------------------ what we win */
  outcomes() {
    if (!JACOB.outcomes) {
      return `<div class="planned-note">The Opportunity Log has not been read yet.
        <code>python scripts/jacob_outcomes.py</code></div>`;
    }
    const o = JACOB.outcomes;
    const s = o.summary;
    const conv = o.clients.filter((c) => c.decided >= 3);
    const open = o.openThisYear || [];
    return `
      <div class="stats">
        <div class="stat green"><div class="n">${s.winRate}%</div><div class="l">Win rate over ${s.decided} decided outcomes</div></div>
        <div class="stat"><div class="n">${gbpShort(s.wonMedian)}</div><div class="l">Median job Fenster wins</div></div>
        <div class="stat red"><div class="n">${gbpShort(s.lostMedian)}</div><div class="l">Median job Fenster loses</div></div>
        <div class="stat red"><div class="n">${s.lostAboveThat}</div><div class="l">Tried and lost above ${gbpShort(s.noWinAbove)} - none won</div></div>
        <div class="stat amber"><div class="n">${open.length}</div><div class="l">Still open on this year's sheet</div></div>
      </div>

      <div class="section"><div class="section-head"><h3>The one number that should change what we chase</h3></div>
        <div class="planned-note">
          <p>Fenster has never won a job over <strong>${gbp(s.noWinAbove)}</strong>.
          ${s.lostAboveThat} were priced and ${s.lostAboveThat} were lost. The biggest job it
          has won in two years is <strong>${gbp(s.biggestWon)}</strong>, and the median win is
          <strong>${gbp(s.wonMedian)}</strong>.</p>
          <p>That is the opposite of how this board used to rank things, and the opposite of
          most of what has been pointed at it - GBP 20m academies, national frameworks. Value
          now buys a row a warning, not a place at the top.</p>
          <p class="dim">Value is filled on ${s.valueFilled} of ${o.rows} rows, so the bands
          below describe the rows that carry a number, not every enquiry.</p>
        </div>
        <table class="tbl"><thead><tr><th>Job size</th><th>Won</th><th>Lost</th><th>Win rate</th></tr></thead><tbody>
        ${o.bands.map((b) => `<tr>
          <td><strong>${esc(b.label)}</strong></td>
          <td class="num">${b.won}</td><td class="num">${b.lost}</td>
          <td class="num">${b.winRate === null ? "-" : `${Math.round(b.winRate)}%`}
            ${b.decided && !b.won ? ` <span class="pill planned">never</span>` : ""}</td>
        </tr>`).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>Clients Fenster actually converts</h3>
        <span class="page-sub">Three or more decided outcomes, so it is a pattern and not a coincidence</span></div>
        <table class="tbl"><thead><tr>
          <th>Client</th><th>Won</th><th>Lost</th><th>Rate</th><th>Still open</th><th>Last enquiry</th></tr></thead><tbody>
        ${conv.map((c) => `<tr>
          <td class="job-cell"><strong>${esc(c.client)}</strong>
            <small>${esc((c.projects || []).slice(0, 2).join(" &middot; "))}</small></td>
          <td class="num">${c.won}</td><td class="num">${c.lost}</td>
          <td class="num"><span class="chip ${c.winRate >= 50 ? "ok" : c.winRate >= 20 ? "warn" : "danger"}">${Math.round(c.winRate)}%</span></td>
          <td class="num">${c.open || "-"}</td>
          <td class="num">${esc(c.lastEnquiry) || "-"}</td></tr>`).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>Why we lose</h3>
        <span class="pill planned">legend unconfirmed</span></div>
        <div class="planned-note">${esc(o.lostLegend?.note || "")}
        The legend is ${esc(o.lostLegend?.status || "unknown")}.</div>
        <table class="tbl"><thead><tr>
          <th>Code</th><th>Rows</th><th>Share of losses</th><th>What the notes on those rows say</th><th>Confidence</th></tr></thead><tbody>
        ${o.lostReasons.map((r) => `<tr>
          <td><strong>${esc(r.code)}</strong></td>
          <td class="num">${r.count}</td><td class="num">${r.shareOfLosses}%</td>
          <td style="max-width:420px">${esc(r.reading)}<small class="dim">${esc(r.evidence)}</small></td>
          <td><span class="chip ${r.confidence === "high" ? "ok" : r.confidence === "low" ? "danger" : "warn"}">${esc(r.confidence)}</span></td>
        </tr>`).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>Still open on this year's sheet</h3>
        <span class="page-sub">Fenster's own record of quotes with no outcome written against them</span></div>
        <div class="planned-note">These are not analysis. They are ${open.length} enquiries the
        BD log says are still live, and
        <strong>${open.filter((r) => !r.chased).length}</strong> of them have nothing in the
        Chased column. The same column was filled
        ${(o.chased || []).map((c) => `${c.pct}% of the time in ${esc(c.sheet)}`).join(", ")} -
        that is a habit that stopped, not a business that got quieter.</div>
        <table class="tbl"><thead><tr>
          <th>Client</th><th>Project</th><th>Value</th><th>Quote returned</th><th>Chased?</th></tr></thead><tbody>
        ${open.slice(0, 60).map((r) => `<tr>
          <td><strong>${esc(r.client)}</strong></td>
          <td>${esc(r.project)}<small class="dim">${esc(r.notes || "")}</small></td>
          <td class="money">${gbp(r.value)}</td>
          <td class="num">${esc(r.returned) || "not recorded"}</td>
          <td>${r.chased ? `<span class="chip ok">yes</span>` : `<span class="chip danger">no</span>`}</td>
        </tr>`).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>Where this comes from</h3></div>
        <div class="planned-note">${esc(o.source)}. Read-only: the workbook is copied into
        <code>test-results\\jacob-bd\\</code> and opened from the copy, because Gintare, Adam
        and Steve are working in that drive. Last read ${esc(ukStamp(o.updated))}.</div></div>`;
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
        <td class="money">${gbp(r.total || r.value)}
          ${r.fit?.note ? `<small class="dim">${esc(r.fit.note)}</small>` : ""}</td>
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

  /* What JAC-1's answer produced. Zac chose "decide later - drafts only", so
     the drafting half is live and the sending half is not: every one of these
     is addressed to a named person and waiting for a named human to send it
     from their own mailbox, under their own name.

     The body is shown in full and is selectable, because the entire workflow
     is somebody reading it, changing what they want and pasting it into
     Outlook. A draft you have to click twice to read does not get sent. */
  drafts() {
    const d = JACOB?.drafts;
    const rows = jdrafts();
    if (!d) {
      return `<div class="empty"><strong>No drafts</strong>JAC-1 has not been
        answered, so nothing is being written. <code>data/jacob/drafts.json</code></div>`;
    }
    return `
      <div class="section"><div class="section-head"><h3>What was decided</h3>
        <span class="pill strong">${esc(d.decision.ref)}</span></div>
        <div class="planned-note">
          <p><strong>${esc(d.decision.question)}</strong> &mdash; ${esc(d.decision.by)},
          ${esc(niceDate(d.decision.date))}: <em>&ldquo;${esc(d.decision.answer)}&rdquo;</em></p>
          <p>${esc(d.decision.effect)} ${esc(d.note)}</p>
        </div></div>

      <div class="section"><div class="section-head"><h3>The rules these were written under</h3></div>
        <ul class="plain">${d.rules.map((r) => `<li>${esc(r)}</li>`).join("")}</ul></div>

      ${rows.map((r) => `<div class="section" data-jkey="draft:${esc(r.id)}">
        <div class="section-head">
          <h3>${esc(r.job)}</h3>
          <span class="pill strong">${esc(r.id)}</span>
          <span class="page-sub">${esc(r.client)}${r.value
            ? ` &middot; ${gbp(r.value)}` : ""} &middot; send as <strong>${esc(r.send_as)}</strong></span>
        </div>
        <div class="planned-note"><p><strong>Why now:</strong> ${esc(r.why_now)}</p></div>
        <table class="tbl"><tbody>
          <tr><td style="width:120px" class="dim">To</td>
            <td><strong>${esc(r.to)}</strong>${r.to_name
              ? `<small class="dim">${esc(r.to_name)}${r.to_caveat
                  ? ` &mdash; ${esc(r.to_caveat)}` : ""}</small>` : ""}</td></tr>
          ${r.cc ? `<tr><td class="dim">Cc</td><td>${esc(r.cc)}</td></tr>` : ""}
          <tr><td class="dim">Subject</td><td><strong>${esc(r.subject)}</strong></td></tr>
        </tbody></table>
        <pre class="draft-body">${esc(r.body)}</pre>
        <table class="tbl"><tbody>
          <tr><td style="width:120px" class="dim">Evidence</td><td>${esc(r.evidence)}</td></tr>
          <tr><td class="dim">Figures</td><td>${esc(r.value_source)}</td></tr>
          <tr><td class="dim">Must not say</td><td>${esc(r.must_not_say)}</td></tr>
          ${r.blocked_on ? `<tr><td class="dim">Open</td><td>${esc(r.blocked_on)}</td></tr>` : ""}
          <tr><td class="dim">State</td><td><span class="chip warn">${esc(r.status)}</span></td></tr>
        </tbody></table></div>`).join("")}

      ${(d.not_drafted || []).length ? `<div class="section"><div class="section-head">
        <h3>Deliberately not drafted</h3>
        <span class="page-sub">Saying why is the point. A silence with no reason behind it is just a gap.</span></div>
        <table class="tbl"><thead><tr><th>What</th><th>Why not</th><th>What happens instead</th></tr></thead><tbody>
        ${d.not_drafted.map((n) => `<tr>
          <td class="job-cell"><strong>${esc(n.what)}</strong></td>
          <td style="max-width:520px">${esc(n.why_not)}</td>
          <td>${esc(n.next)}</td></tr>`).join("")}
        </tbody></table></div>` : ""}`;
  },

  /* AdminBase. The largest single addition this board has had, and the one
     most likely to be misread - so the page leads with what the numbers are
     not before it shows any of them. */
  chaselist() {
    const c = crm();
    if (!c) {
      return `<div class="empty"><strong>AdminBase has not been read</strong>
        Run <code>python scripts/jacob_adminbase.py</code>.</div>`;
    }
    const t = c.totals;
    /* The CRM's own key on these rows is the client's email domain, which is
       right for grouping and wrong for the overlay - twelve Bradford Watts
       rows would all share one human correction. The board key is per lead. */
    const due = c.due
      .map((r) => ({ ...r, key: "ab:" + r.lead }))
      .filter((r) => !r.outlier && !jShut(r))
      .slice(0, 60);
    return `
      <div class="stats">
        <div class="stat"><div class="n">${t.rows}</div><div class="l">Quoted leads in the CRM, ${t.clients} clients</div></div>
        <div class="stat red"><div class="n">${t.due}</div><div class="l">Nobody has been back to, ${gbpShort(t.dueValue)}</div></div>
        <div class="stat amber"><div class="n">${t.yearSilent}</div><div class="l">Silent for over a year and still open</div></div>
        <div class="stat ${t.winnable ? "green" : "amber"}"><div class="n">${gbpShort(t.winnableValue)}</div><div class="l">Of that, in a band Fenster has ever won in - ${t.winnable} jobs</div></div>
      </div>

      <div class="section"><div class="section-head"><h3>Read this before you read the numbers</h3></div>
        <div class="planned-note">
          <p><strong>Where it came from.</strong> ${esc(c.source.from)} sent this to jacob@ at
          ${esc(c.source.received.slice(11))} on ${esc(niceDate(c.source.received.slice(0, 10)))} -
          an export from ${esc(c.source.system)}. ${esc(c.source.note)}</p>
          <p><strong>Every figure on this page is ex VAT and the CSV's are not.</strong>
          ${esc(c.vat.evidence)} ${esc(c.vat.consequence)}</p>
          <p><strong>&ldquo;Live - Quoted&rdquo; is what the CRM says, not what the client says.</strong>
          ${t.due} of ${t.rows} rows qualify as chaseable and ${t.overdue} carry a follow-up date
          that has already passed, against ${t.future} in the future. That is a system nobody
          closes anything in - the same pattern as the Opportunity Log's Chased column, which was
          filled 382 times in 2025 and 7 times in 2026. Treat every row as a question, not
          as an opportunity.</p>
          <p><strong>And the size does not match what Fenster wins.</strong> The Opportunity
          Log's 224 decided rows say: under GBP 10k it wins 38% of the time, GBP 10k-50k 13%,
          and above GBP 50,000 it has never won at all - 52 priced, 52 lost. Median win
          GBP 1,822; largest win ever GBP 40,850.</p>
          <p><strong>So of the ${gbpShort(t.dueValue)} sitting on this list, ${gbpShort(t.winnableValue)}
          is in a band Fenster has ever converted</strong> - ${t.winnable} jobs out of ${t.due}.
          The other ${t.neverWonBand} are in bands with a nil record. The list below is still
          ranked by value, because re-ranking a Commercial Director's chase list on my own
          reading of the history is his call and not mine - but every row says which band it
          is in, and the top of the list is mostly the half that does not convert.</p>
        </div></div>

      ${(c.schemes || []).length ? `<div class="section"><div class="section-head">
        <h3>One scheme, several bidders</h3>
        <span class="page-sub">${gbpShort(t.doubleCounted)} of the pipeline is the same job counted more than once</span></div>
        <div class="planned-note"><p>Fenster is a subcontractor, so the same scheme arrives once
        per main contractor on the enquiry list. These were found on the penny-exact quoted
        figure rather than the site name - the same estimate sent to five bidders carries the
        same number, while the site gets typed five different ways. They are one job each, and
        the useful question is who won the main contract, not which of the five to chase.</p></div>
        <table class="tbl"><thead><tr><th>Scheme</th><th>Quoted</th><th>Bidders</th><th>Silent</th></tr></thead><tbody>
        ${c.schemes.map((s) => `<tr>
          <td class="job-cell"><strong>${esc(s.job)}</strong><small>${s.count} bidders${
            (s.alsoPricedAt || []).length ? ` &middot; the same site also priced at ${
              s.alsoPricedAt.map(gbp).join(" and ")} - one job, two versions` : ""}</small></td>
          <td class="money">${gbp(s.value)}</td>
          <td>${s.bidders.map((b) => `${esc(b.client)}`).join("<br>")}</td>
          <td class="num">${Math.min(...s.bidders.map((b) => b.days ?? 0))}-${Math.max(...s.bidders.map((b) => b.days ?? 0))}d</td>
        </tr>`).join("")}
        </tbody></table></div>` : ""}

      ${(c.conflicts || []).length ? `<div class="section"><div class="section-head">
        <h3>Where the CRM and the sent items disagree</h3></div>
        <table class="tbl"><thead><tr><th>Job</th><th>AdminBase says</th><th>It actually is</th></tr></thead><tbody>
        ${c.conflicts.map((x) => `<tr>
          <td class="job-cell"><strong>${esc(x.job)}</strong><small>${esc(x.client)} &middot; ${gbp(x.value)}</small></td>
          <td>${esc(x.crm)}</td><td><strong>${esc(x.truth)}</strong><small class="dim">${esc(x.why)}</small></td>
        </tr>`).join("")}
        </tbody></table></div>` : ""}

      ${t.outliers ? `<div class="section"><div class="section-head">
        <h3>Held out of every total on this page</h3></div>
        <table class="tbl"><thead><tr><th>Job</th><th>Quoted ex VAT</th><th>Why it is not counted</th></tr></thead><tbody>
        ${c.rows.filter((r) => r.outlier).map((r) => `<tr>
          <td class="job-cell"><strong>${esc(r.job)}</strong><small>${esc(r.client)} &middot; ${esc(niceDate(r.leadDate))}</small></td>
          <td class="money">${gbp(r.value)}</td>
          <td>An order of magnitude past the GBP 20k-400k package Fenster puts on its own PQQ,
            and large enough to move the pipeline figure on its own. It is a question for
            Adam before it is a number.</td></tr>`).join("")}
        </tbody></table></div>` : ""}

      <div class="section"><div class="section-head"><h3>By client</h3>
        <span class="page-sub">Where the money actually sits. Companies merged on their email domain, not their name.</span></div>
        <table class="tbl"><thead><tr>
          <th>Client</th><th>Open</th><th>Quoted ex VAT</th><th>Oldest</th><th>Who to write to</th></tr></thead><tbody>
        ${c.clients.filter((x) => x.quoted).slice(0, 25).map((x) => `<tr>
          <td class="job-cell"><strong>${esc(x.client)}</strong>
            ${x.onBoard ? `<small>already on the chasing register</small>` : ""}</td>
          <td class="num">${x.quoted}${x.rows !== x.quoted ? ` <small class="dim">of ${x.rows}</small>` : ""}</td>
          <td class="money">${gbp(x.value)}</td>
          <td class="num">${x.oldest}d</td>
          <td>${x.email ? esc(x.email) : `<small class="dim">no address on any row</small>`}
            ${x.phone ? `<small class="dim">${esc(x.phone)}</small>` : ""}</td></tr>`).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>The chase list</h3>
        <span class="page-sub">Largest first. ${due.length} of ${t.due} shown.</span></div>
        <table class="tbl"><thead><tr>
          <th>Job</th><th>Client</th><th>Quoted ex VAT</th><th>Ever won at this size?</th>
          <th>Quoted</th><th>Silent</th><th>State</th><th>Contact</th></tr></thead><tbody>
        ${due.map((r) => `<tr data-jkey="${esc(r.key)}">
          <td class="job-cell"><strong>${esc(r.job || "no site recorded")}</strong>
            ${r.postcode ? `<small>${esc(r.postcode)}</small>` : ""}</td>
          <!-- TOWN in the export is the client's own town, not the site's -
               Kemdoc is in Bristol and its Churchdown job is in Gloucester.
               It belongs against the company, not against the job. -->
          <td>${esc(r.client)}${r.town ? `<small class="dim">${esc(r.town)}</small>` : ""}</td>
          <td class="money">${gbp(r.value)}</td>
          <td>${r.fit ? `<span class="chip ${r.fit.winRate >= 38 ? "ok"
            : r.fit.winRate > 0 ? "warn" : "danger"}">${r.fit.winRate}%</span>
            <small class="dim">${esc(r.fit.note)}</small>` : `<small class="dim">no value</small>`}</td>
          <td class="num">${r.leadDate ? esc(niceDate(r.leadDate)) : "-"}</td>
          <td class="num">${r.days === null ? "-" : `${r.days}d`}</td>
          <td>${stateChip(r)}</td>
          <td>${r.email ? esc(r.email) : `<small class="dim">no address</small>`}</td></tr>`).join("")}
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

  jmessages() { return chatPage(BOTS.jacob); },

  jlive() {
    return livePage(JACTIVITY, { tone: "warn", text: "working" }, "Business development",
      "When Jacob picks up a message or a lead, every step he takes appears here as it happens.");
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
          <!-- Buttons only cover what he thought to ask. The interesting answer
               is usually the one he did not anticipate, and the reason matters
               more than the choice - he acts on the why. -->
          <div class="req-reply">
            <textarea data-draft="jreq-${esc(r.ref)}" rows="2"
              placeholder="Or answer in your own words - the reason matters more than the choice"></textarea>
            <button class="btn ghost" data-jreqsend="${esc(r.ref)}">Reply</button>
          </div>
        </div>`).join("")}</div></div>` : ""}

      <div class="section"><div class="section-head"><h3>Standing decisions</h3></div>
        <div class="planned-note">These are not blocking him day to day, but they decide
        how far he is allowed to go. An answered one stays on the page with the answer on
        it - what was decided and what it changed is worth more than a shorter list.</div>
        <div class="cards">
        ${JACOB.decisions.map((d) => `<div class="card${d.answer ? " answered" : ""}">
          <div class="card-head"><strong>${esc(d.title)}</strong>
            <span class="pill ${d.answer ? "live" : "planned"}">${esc(d.id)}</span></div>
          <p>${esc(d.why)}</p>
          ${d.answer ? `<p><strong>${esc(d.answeredBy)} chose &ldquo;${esc(d.answer)}&rdquo;</strong>
              on ${esc(niceDate(d.answered))}.</p>
            <p>${esc(d.effect)}</p>
            <div class="req-options">${d.options.map((o) => `<span class="opt${o === d.answer
              ? " chosen" : ""}" data-jreq="${esc(d.id)}">${esc(o)}</span>`).join("")}</div>`
          : `<div class="req-options">${d.options.map((o) => `<span class="opt" data-jreq="${esc(d.id)}">${esc(o)}</span>`).join("")}</div>`}
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
          <td style="max-width:380px"><div class="clamp">${inline(j.status.split(". ")[0])}.</div></td>
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
        ${reqDetail("What she needs from you", r.needs, 400)}
        ${reqDetail("Why she is blocked", r.why, 0)}
      </article>` : `
      <article class="req resolved">
        <div class="req-top"><div><h3>${esc(r.title)}</h3><div class="meta">${esc(r.job)} &middot; answered ${esc(r.answered_at || "")} by ${esc(r.answered_by || "team")}</div></div><span class="chip ok">resolved</span></div>
        <div class="answered"><h5>The answer</h5>${fmt(r.answer || "")}</div>
      </article>`;
    /* Fifteen open cards is a normal morning, and a flat scroll of them hides
       the shape of the day. Grouped by job, biggest cluster first, the page
       reads as "St Mary's has four questions" before a single card is read. */
    const byJob = new Map();
    for (const r of open) {
      const k = r.job || "General";
      if (!byJob.has(k)) byJob.set(k, []);
      byJob.get(k).push(r);
    }
    const groups = [...byJob.entries()].sort((a, b) => b[1].length - a[1].length);
    const openHtml = groups.map(([job, rs]) => `
      ${groups.length > 1 ? `<div class="section-head req-job-head"><h3>${esc(job)}</h3>
        <span class="page-sub">${rs.length === 1 ? "one decision" : `${rs.length} decisions`}</span></div>` : ""}
      ${rs.map(card).join("")}`).join("");
    return `<div class="req-grid">${openHtml}${done.length ? `<div class="section-head" style="margin-top:14px"><h3>Resolved</h3></div>` + done.map(card).join("") : ""}</div>`;
  },
  messages() { return chatPage(BOTS.mary); },
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
    return livePage(ACTIVITY, maryChip(), "", STATUS?.state === "working"
      ? "Mary is working - her first step will appear here in a moment."
      : "When Mary picks up a job, everything she does appears here as it happens.");
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
          <span class="mail-when">${esc(ukShortDay(o.created))}</span></div>`).join("")}</div></div>` : ""}`;
  },
  catches() {
    return `<div class="catch-grid">${DATA.catches.map((c) => `
      <article class="catch"><div class="req-top"><div><h3 style="font-size:15px">${esc(c.job)}</h3>
        <div class="meta" style="font-size:12px;color:var(--muted)">${esc(c.date)} &middot; ${esc(c.type)}</div></div>
        <span class="value">${esc(c.value || "")}</span></div>
        <p style="margin:10px 0 0">${inline(c.catch)}</p></article>`).join("")}</div>`;
  },
};

/* ---------------- the Team board ----------------
   The front door. Neither bot's board - the one page that answers "does
   anything need a human right now" without checking each bot in turn.
   Built entirely from data the app has already fetched. */
const TEAM_PAGES = [
  { key: "home", label: "Today", group: "Team", icon: "home", sub: () => "Everything that needs a human, across every bot" },
  { key: "botchat", label: "Internal chat", group: "Team", icon: "botchat", layout: "chat", sub: () => "What the bots say to each other - max ten an hour each" },
];

const TEAM_RENDER = {
  home() {
    const mReqs = awaitingReqs();
    const jReqs = openJacobReqs();
    const overdue = DATA.jobs.filter((j) => j.stage === "overdue");
    const dueSoon = DATA.jobs.filter((j) => j.stage === "tender" && daysUntil(j.deadline) <= 3);
    const urgent = [...DATA.jobs].filter((j) => j.stage !== "submitted")
      .sort((a, b) => new Date(a.deadline) - new Date(b.deadline)).slice(0, 5);
    const acts = JACOB ? jActions().slice(0, 5) : [];
    const unseen = unseenMsgs() + unseenJacobMsgs();
    const decisions = mReqs.length + jReqs.length;

    /* Twenty open decisions is a normal morning here, so the unit on this
       page is the JOB, not the request: one compact card per cluster, each
       title clamped to a line, and the click lands on the right board with
       the page search already filtered to that cluster. The flat one-row-
       per-decision list this replaced put the fold at decision four. */
    const byJob = new Map();
    for (const r of mReqs) {
      const k = r.job || "General";
      if (!byJob.has(k)) byJob.set(k, []);
      byJob.get(k).push(r);
    }
    const clusters = [...byJob.entries()].sort((a, b) => b[1].length - a[1].length);
    // Titles mostly open with the job's own name ("Filwood: install line...") -
    // inside a card already headed by the job, that prefix is noise.
    const strip = (t, job) => {
      const i = t.indexOf(":");
      if (i > 0 && i < 34 && job.toLowerCase().includes(t.slice(0, i).toLowerCase().split(/[\s,(]/)[0])) {
        return t.slice(i + 1).trim();
      }
      return t;
    };
    // Owners arrive as "Adam" on one request and "adam" on the next -
    // dedupe case-blind or the card says "needs Adam, adam".
    const owners = (rs) => {
      const seen = new Map();
      for (const o of rs.map((r) => String(r.owner || "").trim()).filter(Boolean)) {
        const k = o.toLowerCase();
        if (!seen.has(k)) seen.set(k, o[0].toUpperCase() + o.slice(1));
      }
      return [...seen.values()].join(", ") || "a human";
    };
    const cluster = ([job, rs]) => `
      <div class="need" data-bot-go="mary:requests" data-filter="${esc(job.slice(0, 40))}">
        <div class="need-top"><span class="need-bot">MG</span><strong title="${esc(job)}">${esc(job)}</strong></div>
        <div class="need-titles">${rs.map((r) => `<span title="${esc(r.title)}">${esc(strip(r.title, job))}</span>`).join("")}</div>
        <div class="need-meta">${rs.length === 1 ? "1 decision" : `${rs.length} decisions`} &middot; needs ${esc(owners(rs))}</div>
      </div>`;
    const jcluster = (r) => `
      <div class="need" data-bot-go="jacob:decisions" data-filter="${esc(r.ref)}">
        <div class="need-top"><span class="need-bot jw">JW</span><strong title="${esc(r.title)}">${esc(r.title)}</strong></div>
        <div class="need-meta">${esc(r.ref)} &middot; he carries on with everything this does not block</div>
      </div>`;

    return `
      <div class="stats">
        <div class="stat ${decisions ? "amber" : "green"}"><div class="n">${decisions}</div><div class="l">Decisions waiting on a human</div></div>
        <div class="stat ${unseen ? "amber" : "green"}"><div class="n">${unseen}</div><div class="l">Messages not yet picked up by a bot</div></div>
        <div class="stat ${overdue.length ? "red" : "green"}" data-bot-go="mary:pipeline"><div class="n">${overdue.length}</div><div class="l">Tenders overdue</div></div>
        <div class="stat ${dueSoon.length ? "amber" : "green"}" data-bot-go="mary:pipeline"><div class="n">${dueSoon.length}</div><div class="l">Due in the next 3 days</div></div>
        ${JACOB ? `<div class="stat ${JACOB.totals.handoverDue ? "red" : ""}" data-bot-go="jacob:chasing"><div class="n">${JACOB.totals.handoverDue ?? 0}</div><div class="l">Quotes chaseable today</div></div>` : ""}
      </div>

      <div class="section"><div class="section-head"><h3>Needs you</h3>
        <span class="page-sub">${decisions ? `${decisions} open decision${decisions === 1 ? "" : "s"} across ${clusters.length + jReqs.length} job${clusters.length + jReqs.length === 1 ? "" : "s"} - click one to answer` : "Every open decision, whoever raised it"}</span></div>
        ${decisions ? `<div class="needs-grid">
          ${clusters.map(cluster).join("")}
          ${jReqs.map(jcluster).join("")}
        </div>` : `<div class="empty"><strong>Nothing waiting</strong>Every question either bot has raised is answered.</div>`}</div>

      <div class="section"><div class="section-head"><h3>Mary - most urgent</h3><a data-bot-go="mary:pipeline">Full pipeline &rarr;</a></div>
        ${RENDER._table(urgent)}</div>

      ${JACOB ? `<div class="section"><div class="section-head"><h3>Jacob - top of the list</h3><a data-bot-go="jacob:overview">His whole day &rarr;</a></div>
        ${JACOB_RENDER._acts(acts, "Nothing outstanding")}</div>` : ""}

      ${BOTCHAT.length ? `<div class="section"><div class="section-head"><h3>Latest between the bots</h3><a data-nav="botchat">The whole line &rarr;</a></div>
        <div class="mail-list">${BOTCHAT.slice(0, 2).map((m) => `
          <div class="mail-row" data-nav="botchat">
            <div class="mail-ico ${m.sender === "mary" ? "out" : "in"}">${esc(BOTS[m.sender]?.initials || "?")}</div>
            <div><strong>${esc(m.subject || m.body.slice(0, 80))}</strong><small>${esc(BOTS[m.sender]?.name || m.sender)} &rarr; ${esc(BOTS[m.recipient]?.name || m.recipient)}</small></div>
            <span class="mail-when">${esc(ukStamp(m.created))}</span>
          </div>`).join("")}</div></div>` : ""}`;
  },
  botchat: botchatPage,
};

/* ---------------- the registry ----------------
   Everything the shell needs to know about a board, in one place. The
   sidebar, nav, routing, polling, badges and chat all read from here;
   adding a bot is adding an entry, not editing the shell. */
function jacobStatus() {
  if (JSTATUS && JSTATUS.state && JSTATUS.state !== "unknown") return bridgeStatus(JSTATUS);
  // His bridge does not report a status line yet - infer from the live feed:
  // steps inside the last ten minutes mean a session is running now.
  const age = JACTIVITY?.updated ? Date.now() - new Date(JACTIVITY.updated).getTime() : Infinity;
  if (age < 600000) return { text: "Working", tone: "busy", title: JACTIVITY?.title || "" };
  return { text: "Live", tone: "", title: "" };
}

const BOTS = {
  team: {
    key: "team", name: "Fenster team", role: "The whole picture", initials: "FG", accent: "team",
    pages: TEAM_PAGES, render: TEAM_RENDER,
    status: null, needsYou: null, badges: () => ({}),
  },
  mary: {
    key: "mary", name: "Mary Grace", role: "Estimating", initials: "MG", accent: "",
    pages: PAGES, render: RENDER,
    status: () => bridgeStatus(STATUS),
    updatedLine: () => DATA ? "Board updated " + new Date(DATA.updated).toLocaleString("en-GB", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }) : "",
    needsYou: () => awaitingReqs().length + unseenMsgs(),
    badges: () => ({ requests: awaitingReqs().length, messages: unseenMsgs() }),
    send: sendToMary,
    chat: {
      msgs: () => MESSAGES, seen: "seen_by_mary", draft: "chat",
      placeholder: "Ask Mary anything - price a job, chase something, explain a number...",
      empty: "Say hello - Mary replies right here.",
      hint: () => STATUS?.state === "working" ? "she is mid-job - this queues behind it" : "picked up within seconds",
    },
  },
  jacob: {
    key: "jacob", name: "Jacob Wright", role: "Business development", initials: "JW", accent: "jw",
    pages: JACOB_PAGES, render: JACOB_RENDER,
    status: jacobStatus,
    needsYou: () => openJacobReqs().length + unseenJacobMsgs(),
    badges: () => ({ decisions: openJacobReqs().length, jmessages: unseenJacobMsgs() }),
    send: sendToJacob,
    chat: {
      msgs: () => JMSGS, seen: "seen_by_jacob", draft: "jacob-msg",
      placeholder: "Message Jacob - what he has found, who is worth calling, why a lead scored...",
      empty: "Ask him something - what he has found, who is worth calling, why a lead scored the way it did.",
      hint: () => "picked up on his next pass",
    },
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
  $$("#page tr[data-job], #page tr[data-jkey], #page .act, #page .req, #page .mail-row, #page .catch, #page .bubble, #page .card, #page .need").forEach((el) => {
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

  const bot = BOTS[BOT] || BOTS.team;
  const pages = bot.pages;
  const renderer = bot.render;
  const badges = bot.badges ? bot.badges() : {};
  renderSidebar();

  // Group headings break an 11-item list into something scannable. Only
  // emitted when the group changes, so ungrouped pages still render flat.
  let lastGroup = null;
  $("#nav-items").innerHTML = pages.map((p) => {
    const head = p.group && p.group !== lastGroup
      ? `<div class="nav-group">${esc((lastGroup = p.group))}</div>` : "";
    return `${head}<button class="nav-item${p.key === page ? " active" : ""}" data-nav="${p.key}">${ICONS[p.icon || p.key] || ""}${p.label}
    ${badges[p.key] ? `<span class="badge${["requests", "decisions"].includes(p.key) ? " hot" : ""}">${badges[p.key]}</span>` : ""}</button>`;
  }).join("");
  // Switching bots can leave `page` pointing at a section the other one does
  // not have ("catches" -> Jacob). Fall back rather than render a blank board.
  const meta = pages.find((p) => p.key === page) || pages[0];
  page = meta.key;
  $("#page-title").textContent = meta.label;
  $("#page-sub").textContent = meta.sub();
  // The layout keys off this: a page declared `layout: "chat"` becomes a
  // full-height flex column rather than a fixed-offset box. CSS cannot ask
  // "which page is this", so the page has to say - via the registry, never a
  // list of page names in the stylesheet (that is how Internal chat missed out).
  $("#page").dataset.page = page;
  $("#page").dataset.layout = meta.layout || "";
  $("#page").innerHTML = renderer[page] ? renderer[page].call(renderer) : "";
  // Twenty-six tables are written as bare <table class="tbl"> across both
  // boards. A table cannot scroll itself, so on a phone each one widens the
  // whole page and every OTHER screen inherits a sideways wobble. Wrapping them
  // here is one place instead of twenty-six template strings.
  $$("#page table.tbl").forEach((t) => {
    if (t.parentElement?.classList.contains("tbl-wrap")) return;
    const wrap = document.createElement("div");
    wrap.className = "tbl-wrap";
    t.replaceWith(wrap);
    wrap.appendChild(t);
  });
  // The drawer hides the section name, so the top bar carries it.
  const mt = $("#mobile-title");
  if (mt) mt.textContent = meta.label;
  // One dot on the burger for "there is something for you behind this menu" -
  // otherwise a closed drawer hides the only signal that anything needs you.
  // Counted across EVERY bot, because the drawer hides all of them.
  const dot = $("#nav-dot");
  if (dot) dot.hidden = !Object.values(BOTS).reduce((n, b) => n + (b.needsYou ? b.needsYou() : 0), 0);
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
}

document.addEventListener("input", (e) => {
  const key = e.target.dataset?.draft;
  if (key) DRAFTS[key] = e.target.value;
});

/* ---------------- the phone drawer ----------------
   Below 900px the sidebar is off-screen until asked for. Three ways out, because
   a drawer you cannot dismiss is worse than no drawer: the backdrop, Escape, and
   picking anything inside it. The body lock stops the page behind scrolling
   under your finger while the drawer is open. */
function setNav(open) {
  const nav = $("#nav"), veil = $("#nav-veil"), btn = $("#nav-toggle");
  if (!nav) return;
  nav.classList.toggle("open", open);
  if (veil) veil.hidden = !open;
  if (btn) btn.setAttribute("aria-expanded", String(open));
  document.body.classList.toggle("nav-open", open);
}
$("#nav-toggle")?.addEventListener("click", () => setNav(!$("#nav").classList.contains("open")));
$("#nav-veil")?.addEventListener("click", () => setNav(false));
document.addEventListener("keydown", (e) => { if (e.key === "Escape") setNav(false); });

document.addEventListener("click", async (e) => {
  // Anything chosen inside the drawer has served its purpose - get out of the way.
  if (e.target.closest("#nav [data-nav], #nav [data-bot]")) setNav(false);
  // Swap the whole board between the Team view and a bot's board.
  const bot = e.target.closest("[data-bot]");
  if (bot) {
    if (bot.dataset.bot !== BOT && BOTS[bot.dataset.bot]) {
      BOT = bot.dataset.bot;
      page = BOTS[BOT].pages[0].key;
      searchTerm = "";
      closePanel();
      render();
    }
    return;
  }
  // Cross-board link: "bot:page", used by the Team view to land on the exact
  // page a row belongs to, whichever board it lives on. A data-filter riding
  // along pre-fills that page's search, so a click on the St Mary's cluster
  // lands on the requests page showing only St Mary's.
  const bg = e.target.closest("[data-bot-go]");
  if (bg) {
    const [b, p] = bg.dataset.botGo.split(":");
    if (BOTS[b]) { BOT = b; page = p; searchTerm = bg.dataset.filter || ""; closePanel(); render(); }
    return;
  }
  const nav = e.target.closest("[data-nav],[data-go],[data-goreq]");
  if (nav) {
    if (nav.dataset.goreq) { closePanel(); page = "requests"; render(); return; }
    page = nav.dataset.nav || nav.dataset.go; render(); return;
  }
  // Send on any bot's chat page - the registry says whose thread it is.
  const cs = e.target.closest("[data-chatsend]");
  if (cs) {
    const b = BOTS[cs.dataset.chatsend];
    const ta = document.querySelector(`[data-draft="${b.chat.draft}"]`);
    const text = (ta?.value || "").trim();
    if (!text) return;
    cs.disabled = true;
    try {
      await b.send(text);
      delete DRAFTS[b.chat.draft];
      if (ta) ta.value = "";
      render();
    } catch {
      toast("Could not send that");
      cs.disabled = false;
    }
    return;
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
  // Free-text answer to one of his questions.
  const jrs = e.target.closest("[data-jreqsend]");
  if (jrs) {
    const ref = jrs.dataset.jreqsend;
    const ta = document.querySelector(`[data-draft="jreq-${ref}"]`);
    const answer = (ta?.value || "").trim();
    if (!answer) { toast("Nothing typed"); return; }
    jrs.disabled = true;
    try {
      await api("jacob/requests", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ ref, answer, author: who() }),
      });
      delete DRAFTS[`jreq-${ref}`];
      JREQS = await api("jacob/requests").catch(() => JREQS);
      JMSGS = await api("jacob/messages").catch(() => JMSGS);
      toast(`Answered ${ref}`);
      render();
    } catch { toast("Could not save that"); jrs.disabled = false; }
    return;
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
    let pipe = [];
    [JMSGS, JREQS, BOTCHAT, pipe] = await Promise.all([
      api("jacob/messages").catch(() => []),
      api("jacob/requests").catch(() => []),
      api("botchat").catch(() => []),
      // No edits yet is the normal state on a fresh board, not a failure.
      api("jacob/pipeline").catch(() => []),
    ]);
    JPIPE = Object.fromEntries(pipe.map((r) => [r.key, r]));
    [JACTIVITY, JSTATUS] = await Promise.all([
      api("jacob-activity").catch(() => null),
      api("jacob/status").catch(() => null),
    ]);
    // A bot whose board data is missing loses its card but takes nothing
    // else down - the registry entry stays so its data can still be read.
    if (!JACOB) BOTS.jacob.hidden = true;

    msgSig = signature(MESSAGES);
    render();

    // The live feeds need a faster beat than the rest of the hub, but only
    // while somebody is actually watching one. A poll patches #ev-feed in
    // place; render() only for the first paint or coming out of empty.
    setInterval(async () => {
      const maryLive = BOT === "mary" && page === "live";
      const jacobLive = BOT === "jacob" && page === "jlive";
      if (!maryLive && !jacobLive) return;
      try {
        const fresh = await api(maryLive ? "activity" : "jacob-activity");
        if (maryLive) {
          if (JSON.stringify(fresh) === JSON.stringify(ACTIVITY)) return;
          ACTIVITY = fresh;
          if (!paintFeed(fresh, maryChip())) render();
        } else {
          if (JSON.stringify(fresh) === JSON.stringify(JACTIVITY)) return;
          JACTIVITY = fresh;
          if (!paintFeed(fresh)) render();
        }
      } catch {}
    }, 3000);

    // Everything else on one 10-second beat, for every bot at once - the
    // sidebar badges have to stay honest about the board you are NOT looking
    // at, or the Team view's whole promise is broken. The page itself only
    // redraws when its own data changed: never over the user.
    let jacobSig = [JMSGS.length, BOTCHAT.length, JREQS.length,
                    JMSGS[0]?.id, BOTCHAT[0]?.id,
                    JREQS.filter((r) => r.status !== "answered").length].join(":");
    setInterval(async () => {
      try {
        const [fresh, status, jmsgs, chat, reqs] = await Promise.all([
          api("messages").catch(() => MESSAGES),
          api("status").catch(() => STATUS),
          api("jacob/messages").catch(() => JMSGS),
          api("botchat").catch(() => BOTCHAT),
          api("jacob/requests").catch(() => JREQS),
        ]);
        const statusChanged = JSON.stringify(status) !== JSON.stringify(STATUS);
        STATUS = status;
        const sig = signature(fresh);
        const jsig = [jmsgs.length, chat.length, reqs.length,
                      jmsgs[0]?.id, chat[0]?.id,
                      reqs.filter((r) => r.status !== "answered").length].join(":");
        const maryChanged = sig !== msgSig;
        const jacobChanged = jsig !== jacobSig;
        if (maryChanged) { MESSAGES = fresh; msgSig = sig; }
        if (jacobChanged) { JMSGS = jmsgs; BOTCHAT = chat; JREQS = reqs; jacobSig = jsig; }
        if (statusChanged || maryChanged || jacobChanged) renderSidebar();
        const watching =
          (BOT === "mary" && maryChanged && ["messages", "overview"].includes(page)) ||
          (BOT === "jacob" && jacobChanged && ["jmessages", "decisions", "overview"].includes(page)) ||
          (BOT === "team" && (maryChanged || jacobChanged) && ["home", "botchat"].includes(page));
        if (watching) render();
      } catch {}
    }, 10000);
  } catch (err) {
    $("#page").innerHTML = `<div class="empty"><strong>Could not load the hub</strong>${err.status || err.message}</div>`;
  }
})();
