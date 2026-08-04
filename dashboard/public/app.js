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
let page = "today";
let commsTab = "sent";
/* BOT decides which board is on screen: "work" (the five sections a job can
   be in), "team", or a bot's key. The hub OPENS ON THE WORK, not on a bot -
   the first question is "what needs doing", not "what has Mary been up to". */
let BOT = "work";
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
/* ---------------- who is at the keyboard ----------------
   Adam, 29/07 (hub-66): "it defaults to Zac... it's been Adam the whole time."
   The sidebar was a two-option <select>, and a select has a first option -
   which is what every message posted as unless somebody remembered to change
   it. Four of his instructions on 29/07 alone reached Jacob under Zac's name,
   and one of them (hub-58) was him saying so.

   There is no login on this hub and no way for it to know whose phone it is -
   a browser cannot see the person, only the device. So the honest version of
   what he asked for is: ASK on any device that has not answered yet, block the
   page until it has, then remember the answer on that device forever. Same
   effect as knowing it is his phone, after the first time.

   ME is null until answered, and null never posts: an instruction filed under
   the wrong name is worse than an interruption. */
const ME_KEY = "fenster-hub-who";
const PEOPLE = { adam: "Adam", zac: "Zac" };
let ME = null;
try {
  const saved = localStorage.getItem(ME_KEY);
  if (PEOPLE[saved]) ME = saved;
} catch { /* private mode, no storage - it just asks every time */ }
const who = () => ME || "";
const meName = () => PEOPLE[ME] || "nobody";

/* Kept in memory as well as in storage, so a browser that refuses to persist
   still gets one question per session rather than one per message. */
function setMe(key) {
  if (!PEOPLE[key]) return;
  ME = key;
  try { localStorage.setItem(ME_KEY, key); } catch {}
  closeSignIn();
  paintMe();
  // Answered before the board finished loading is the normal case on a cold
  // open. Boot's own render() covers that one; this only repaints a page that
  // is already up, so "Sending as" is right the moment you switch.
  if (DATA) render();
}

function paintMe() {
  const name = $("#who-name");
  if (name) name.textContent = meName();
  const chip = $("#who-chip");
  if (chip) { chip.hidden = !ME; chip.textContent = meName(); }
}

/* `optional` is a switch mid-session - you are already signed in and changing
   your mind, so it can be dismissed. The first ask cannot: there is nothing to
   fall back to. */
function askWho(optional = false) {
  const gate = $("#signin");
  if (!gate) return;
  gate.hidden = false;
  const cancel = $("#signin-cancel");
  if (cancel) cancel.hidden = !optional;
}
function closeSignIn() {
  const gate = $("#signin");
  if (gate) gate.hidden = true;
}

/* Every write to either bot goes through here. The gate makes this close to
   unreachable, but "close to" is not the same as a check. */
function requireMe(what = "This") {
  if (ME) return true;
  askWho(false);
  toast(`${what} goes on the record under your name - say who you are first`);
  return false;
}

async function sendToMary(body, context = "") {
  if (!requireMe("A message to Mary")) return;
  const res = await api("messages", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ author: who(), body, context }),
  });
  MESSAGES = await api("messages");
  msgSig = signature(MESSAGES);
  if (cutOff(res)) return;
  toast(STATUS?.state === "working" ? "Sent - queued, Mary is mid-job right now" : "Sent - Mary picks this up in seconds");
}

/* A long paste that arrives half-eaten is the worst outcome here - the bot acts
   on a spec neither end knows is incomplete. It happened once (Adam, 29/07, a
   4,000-character rewrite that stopped mid-word). The cap is now 20,000 and the
   API returns how much it dropped; this makes sure somebody is told. */
function cutOff(res) {
  if (!res || !res.truncated) return false;
  toast(`Sent, but ${res.truncated.toLocaleString()} characters were cut - the limit is `
        + `${res.limit.toLocaleString()}. Send the rest as a second message.`);
  return true;
}

/* The live pill on a bot's sidebar card: what its bridge is doing this
   second. Returns {text, tone, title} so the card renderer stays generic. */
/* A bridge that is running says so every sixty seconds. So a "working" status
   nobody has touched for a quarter of an hour is not a working bot - it is the
   last thing a dead bridge said, and the hub has no other way to tell.

   Mary's card read "Working on Triage" from 30/07 to 04/08 because her bridge
   was killed mid-session and the row it left behind was the newest thing in
   the table. Nothing was wrong with the data; the page just had no notion that
   a fact can go out of date. Five days is a long time to be told a lie by a
   status light. */
const STATUS_STALE_MS = 15 * 60 * 1000;

function statusAge(s) {
  if (!s || !s.updated) return Infinity;
  const t = new Date(s.updated).getTime();
  return isNaN(t) ? Infinity : Date.now() - t;
}

function bridgeStatus(s) {
  s = s || {};
  const age = statusAge(s);
  /* STALE IS STALE WHATEVER IT SAID. A bridge that is up reports every sixty
     seconds, so a status nobody has touched for fifteen minutes means the
     bridge is down - and that is just as true of an "idle" row as a "working"
     one. Checking only working/batching left a bot that went idle five days
     ago showing a green "Live", which is the same lie in a nicer font. */
  if (s.state && s.state !== "unknown" && age > STATUS_STALE_MS) {
    const short = String(s.title || "").split(" (")[0].split(",")[0].trim();
    const when = age > 86400000 ? `${Math.floor(age / 86400000)}d`
               : `${Math.max(1, Math.round(age / 3600000))}h`;
    const midJob = ["working", "batching"].includes(s.state);
    return {
      text: midJob ? (short ? `Stopped mid-job - ${short}` : "Stopped mid-job")
                   : "Not running",
      tone: midJob ? "stalled" : "off",
      thought: String(s.thought || "").trim(),
      title: `Last said anything ${when} ago. The bridge is not running.`,
    };
  }
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
  /* The line under the header. Zac, 04/08: "the sub text is the last message/
     thought it had." The state alone does not tell you whether a bot is moving
     - "Working on St Mary's" reads the same at two minutes and at forty. The
     last thing it actually said is what distinguishes them. */
  return { text, tone, thought: String(s.thought || "").trim(),
           title: [s.title, s.detail].filter(Boolean).join(" - ") };
}

/* The whole left-hand column of bot cards, generated from the registry.
   Regenerated whenever a status or badge changes - the cards hold no input
   state, so a rebuild can never eat anything a human was doing. */
function renderSidebar() {
  const host = $("#bot-cards");
  if (!host) return;
  /* THE WORK SITS ABOVE THE STAFF, and it is not a card. A card says "here is
     somebody, go and see what they have"; these are the five places a job can
     be, and a job is in exactly one of them. The bots underneath are who is
     doing it, which is a different question and a smaller one. */
  const work = BOTS.work;
  const workNav = `<div class="nav-group">The work</div>
    ${work.pages.map((p) => {
      const on = BOT === "work" && page === p.key;
      return `<button class="nav-item${on ? " active" : ""}" data-work="${p.key}" type="button">
        ${ICONS[p.icon || p.key] || ""}${p.label}</button>`;
    }).join("")}
    <div class="nav-group">The staff</div>`;

  host.innerHTML = workNav + Object.values(BOTS).filter((b) => !b.hidden && !b.isWork).map((b) => {
    const s = b.status ? b.status() : null;
    const n = b.needsYou ? b.needsYou() : 0;
    return `<button class="nav-mary nav-bot" data-bot="${b.key}" type="button">
      <div class="avatar ${b.accent || ""}">${b.initials}</div>
      <div>
        <strong>${b.name}${n ? `<span class="card-badge" title="Waiting on a human">${n}</span>` : ""}</strong>
        ${s ? `<span class="live"><i class="dot ${s.tone}"></i> <span class="bot-state" title="${esc(s.title)}">${esc(s.text)}</span></span>` : ""}
        ${s && s.thought
            ? `<span class="bot-thought" title="${esc(s.thought)}"><span>${esc(s.thought)}</span></span>`
            : `<span class="role">${esc(b.role)}</span>`}
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
/* Returns null - never NaN - when there is no usable date. A blank deadline used
   to produce new Date("T12:00:00"), and the card then read "NaN days left"
   (Adam, 29/07: "What does NaN mean?"). Every caller must handle null. */
const daysUntil = (iso) => {
  const t = new Date((iso || "") + "T12:00:00").getTime();
  return Number.isNaN(t) ? null : Math.ceil((t - Date.now()) / 86400000);
};
function rag(job) {
  if (job.stage === "submitted") return ["ok", "Submitted"];
  const d = daysUntil(job.deadline);
  if (d === null) return ["warn", "No deadline set"];
  /* A default is a placeholder, not a commitment from anyone. It is shown in the
     amber tone whatever the count, so it can never read like a client date. */
  if (job.deadline_is_default) return ["warn", d < 0 ? `default date passed (${-d}d)` : `${d} days (DEFAULT, not client-set)`];
  if (d < 0) return ["danger", `${-d} days overdue`];
  if (d === 0) return ["danger", "Due today"];
  if (d <= 2) return ["danger", `${d} day${d > 1 ? "s" : ""} left`];
  if (d <= 5) return ["warn", `${d} days left`];
  return ["ok", `${d} days left`];
}
/* Same rule as ukShortDay below - a date outside the current year says so.
   This one is the Chasing page's issue dates, where an out-of-year quote is
   exactly the one somebody needs to notice. */
const niceDate = (iso) => {
  const d = new Date((iso || "") + "T12:00:00");
  if (Number.isNaN(d.getTime())) return "not set";   /* never "Invalid Date" */
  const short = d.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" });
  return d.getFullYear() === new Date().getFullYear() ? short : `${short} ${d.getFullYear()}`;
};
/* Every `created` in D1 is new Date().toISOString() - i.e. UTC with a Z. Slicing
   the string (which this file used to do in five places) published UK times an
   hour early all through BST: Adam sent a message at 22:07 and the thread said
   21:07. Always go through these. Europe/London is pinned rather than left to
   the browser so the board reads the same from anywhere. */
const UK = "Europe/London";
const ukTime = (iso) => iso ? new Date(iso).toLocaleTimeString("en-GB", { timeZone: UK, hour: "2-digit", minute: "2-digit" }) : "";
const ukDay = (iso) => iso ? new Date(iso).toLocaleDateString("en-GB", { timeZone: UK, weekday: "long", day: "numeric", month: "long" }) : "";
/* A date with no year on it is read as this year, and on the Leads page that
   is wrong for a large share of the rows: AdminBase carries quoted leads back
   to May 2025, so "12 May" is a fourteen-month-old quote presented as one from
   this spring. Adam, 29/07 (hub-60; filed under Zac's name by the old sidebar
   default, corrected by him in hub-66). Anything outside the current year now carries it;
   anything inside it stays short, because a year on every row is noise. */
const ukYearOf = (d) => d.toLocaleDateString("en-GB", { timeZone: UK, year: "numeric" });
const ukShortDay = (iso) => {
  if (!iso) return "";
  const d = new Date(iso);
  const short = d.toLocaleDateString("en-GB", { timeZone: UK, day: "2-digit", month: "short" });
  const y = ukYearOf(d);
  return y === ukYearOf(new Date()) ? short : `${short} ${y}`;
};
const ukStamp = (iso) => iso ? `${ukShortDay(iso)} ${ukTime(iso)}` : "";
/* Generator data carries dates as raw ISO strings ("2026-07-14"). Show them
   like every other date on the board; pass anything else through untouched. */
const fdate = (v) => /^\d{4}-\d{2}-\d{2}/.test(String(v || "")) ? ukShortDay(String(v).slice(0, 10)) : String(v || "");
const openReqs = () => (DATA.requests || []).filter((r) => r.status === "open");
/* Still needing a human - one you have already answered is with Mary, not you. */
const awaitingReqs = () => openReqs().filter((r) => !SENT_ANSWERS[r.id]);
const unseenMsgs = () => MESSAGES.filter((m) => m.author !== "mary" && !m.seen_by_mary).length;
const unseenJacobMsgs = () => JMSGS.filter((m) => m.author !== "jacob" && !m.seen_by_jacob).length;
const unseenJosephMsgs = () => JOMSGS.filter((m) => m.author !== "joseph" && !m.seen_by_joseph).length;

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
      <div class="chat-actions"><span class="chat-hint">Sending as <strong>${esc(meName())}</strong> &middot; ${c.hint()}</span>
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

/* One live feed page for every bot - the markup #ev-feed polling patches.
   The head says what KICKED the session off, because "why is she even
   running" used to be unanswerable from the hub. */
function livePage(a, chip, fallbackTitle, empty, kick, queueKey) {
  const kickLine = kick ? `
    <div class="planned-note" style="margin-bottom:12px"><strong>Kicked off ${esc(ukStamp(kick.at))} by:</strong>
      ${esc((kick.orders || [])[0] || kick.title || "?")}${(kick.orders || []).length > 1 ? ` (+${kick.orders.length - 1} more)` : ""}
      &middot; <a data-nav="${queueKey}">the queue &amp; full starting prompt &rarr;</a></div>` : "";
  if (!((a || {}).events || []).length) {
    return `${kickLine}<div class="empty"><strong>Nothing running</strong>${empty}</div>`;
  }
  return `${kickLine}
    <div class="live-head">
      <span class="chip ${chip.tone}">${chip.text}</span>
      <strong>${esc(a.title || a.chat || fallbackTitle)}</strong>
      <span class="live-when">last step ${esc(feedWhen(a))}</span>
    </div>
    <div class="ev-feed" id="ev-feed">${feedRows(a.events)}</div>`;
}

/* The Queue tab: what is waiting, why it routed where it did, and the last
   session's kick - starting prompt included, folded. */
function queuePage(q) {
  const items = q?.items || [];
  const k = q?.last_kick;
  // Why nothing is running. A bot held back by its own session budget used to
  // say so only in bridge.log, so the hub showed a queue with orders in it, an
  // old last_kick, and no explanation - Zac had to guess that Jacob had "hit
  // some hard limit" (dashmsg-95, 29/07). Absent on a bridge that does not
  // publish it, which is not an error.
  const b = q?.budget;
  const budgetLine = !b ? "" : `
    <div class="planned-note" style="margin-bottom:12px">
      <span class="chip ${b.held ? "warn" : b.session_running ? "ok" : "navy"}">${
        b.held ? "HELD BACK" : b.session_running ? "RUNNING" : "IDLE"}</span>
      ${esc(String(b.used_hours))} of ${esc(String(b.of_hours))} session-hours used this window,
      resets ${esc(b.resets || "07:00")}${items.length && b.held ? ` &middot; <strong>${items.length} order(s) waiting on this</strong>` : ""}
      ${b.note ? `<div style="margin-top:6px"><small>${esc(b.note)}</small></div>` : ""}
    </div>`;
  return `${budgetLine}
    ${k ? `<div class="section"><div class="section-head"><h3>What kicked the last session off</h3>
      <span class="page-sub">${esc(k.title || k.chat || "")} &middot; ${esc(ukStamp(k.at))}</span></div>
      <div class="mail-list">${(k.orders || []).map((o) => `
        <div class="mail-row" style="cursor:default"><div class="mail-ico in">&rarr;</div>
          <div><strong>${esc(o)}</strong></div></div>`).join("")}</div>
      <details class="req-detail"><summary>The full starting prompt, exactly as sent</summary>
        <pre class="draft-body">${esc(k.prompt || "(not captured)")}</pre></details></div>`
      : `<div class="planned-note">No session has been kicked since this view went live - the next dispatch fills it.</div>`}

    <div class="section"><div class="section-head"><h3>Waiting now (${items.length})</h3>
      <span class="page-sub">Oldest runs first; each row says why it routed where it did</span></div>
      ${items.length ? `<table class="tbl"><thead><tr>
        <th>What</th><th>From</th><th>Routed to</th><th>Why</th></tr></thead><tbody>
        ${items.map((i, n) => `<tr data-qitem="${n}">
          <td class="job-cell"><strong>${esc(i.subject || i.file)}</strong>
            <small>${esc(i.mailbox || "")}${i.context ? ` &middot; ${esc(i.context)}` : ""} &middot; ${esc(i.file || "")}</small></td>
          <td>${esc(i.from || "")}</td>
          <td><span class="chip navy">${esc(i.route || "")}</span></td>
          <td style="max-width:360px"><div class="clamp4">${esc(i.why || "")}</div></td></tr>`).join("")}
      </tbody></table>` : `<div class="empty"><strong>Queue empty</strong>Nothing waiting to run.</div>`}
    </div>`;
}

/* A queued item in full - the row clamps, the panel does not. */
function queueItemPanel(i) {
  openPanel(`
    <h2>${esc(i.subject || i.file)}</h2>
    <p class="sub">${esc(i.from || "?")} &middot; ${esc(i.mailbox || "")}${i.received ? ` &middot; ${esc(ukStamp(i.received) || i.received)}` : ""}</p>
    <div class="panel-sec"><h4>Routed to</h4><p><span class="chip navy">${esc(i.route || "?")}</span>
      <small class="dim" style="display:block;margin-top:6px">${esc(i.why || "")}</small></p></div>
    ${i.context ? `<div class="panel-sec"><h4>Context</h4><p>${esc(i.context)}</p></div>` : ""}
    <div class="panel-sec"><h4>What it says</h4>
      <div class="rt-box">${fmt(i.body || "(this work order carries no body - it is a signal, and the file itself has the detail)")}</div></div>
    <p class="page-sub" style="margin-top:14px">Full JSON: test-results\\...\\queue\\${esc(i.file || "")}</p>`);
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
    ${j.deadline_basis ? `<p class="page-sub" style="margin-top:-4px">${esc(j.deadline_basis)}</p>` : ""}
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
      evidence: `<p><strong>${esc(t.subject)}</strong></p><p>${t.messages} message${t.messages === 1 ? "" : "s"} between ${esc(fdate(t.first))} and ${esc(fdate(t.last))}, from ${esc(t.contact)}. Fenster history: ${esc(t.relationship)}.</p>`,
      unknowns: t.unknowns })],
    [JACOB.warm.concat(JACOB.known, JACOB.cold), (r) => ({ title: r.supplier,
      sub: `${r.client ? r.client + " - " : ""}${gbp(r.total || r.value)}`,
      evidence: `<p><strong>${esc(r.title)}</strong></p><p>Buyer ${esc(r.buyer) || "not named"}. Awarded ${esc(r.awarded) || "date not published"}${r.n > 1 ? `, ${r.n} live contracts in the window` : ""}. ${esc(r.area) ? "Postcode area " + esc(r.area) + "." : ""}</p>${r.url ? `<p><a href="${esc(r.url)}" target="_blank" rel="noopener">The notice on Contracts Finder</a></p>` : ""}`,
      unknowns: r.confidence === "possible" ? ["Whether this is the same company as the archive folder. Single-word names throw false positives."] : [] })],
    [JACOB.relationships.rows, (x) => ({ title: x.company, sub: x.domain || "from the archive",
      evidence: `<p>${x.messages || "No"} message${x.messages === 1 ? "" : "s"} in the window${x.lastContact ? `, last on ${esc(x.lastContact)}` : ""}. Known from ${x.sources.join(", ")}.</p><p>${x.contacts.length ? x.contacts.map((c) => esc(c.name || c.address)).join(", ") : "No named contact."}</p>`,
      unknowns: [] })],
  ];
  /* ---- The quoted work ----
     These four pools were missing until 29/07 and it was not a cosmetic gap:
     the overlay had exactly ONE row in it, a `lead:`, because a `lead:` was
     the only key this function could resolve. Every quote on the register,
     every AdminBase row, every tender and every draft opened the panel, failed
     to find itself and toasted "the board may have been rebuilt". Adam's
     "the chase list isn't very user friendly" is that bug described from the
     outside: it was not a list you could work, it was a list you could read. */
  pools.push(
    [(hand()?.issued || []), (r) => ({ title: r.job, sub: `${r.client} - ${gbp(r.value)}`,
      evidence: `<p>Issued <strong>${esc(fdate(r.issued))}${r.issuedTime ? ` at ${esc(r.issuedTime)}` : ""}</strong>${
        r.daysOut ? `, ${r.daysOut} days ago` : ""}${r.verified ? " - read out of the sent message, not inferred" : ""}.
        ${r.lastClientContact ? `Last heard from them ${esc(fdate(r.lastClientContact))}.` : "Nothing back from them since."}</p>
        ${r.contact ? `<p><strong>${esc(r.contact)}</strong>${r.contactRole ? `, ${esc(r.contactRole)}` : ""}${
          r.email ? ` &middot; ${esc(r.email)}` : ""}${r.contactMobile ? ` &middot; ${esc(r.contactMobile)}` : ""}${
          r.contactPhone ? ` &middot; ${esc(r.contactPhone)}` : ""}</p>` : ""}
        ${r.history ? `<p>${inline(r.history)}</p>` : ""}
        ${r.expires ? `<p><strong>Validity dies ${esc(fdate(r.expires))}.</strong> ${esc(r.expiryNote || "")}</p>` : ""}
        ${r.blockedReason ? `<p><strong>Cannot answer yet:</strong> ${esc(r.blockedReason)}</p>` : ""}`,
      unknowns: [
        ...(r.openOnTheIssuedDocument || []).map(
          (x) => `Still open on the copy the client is holding: ${typeof x === "string" ? x : (x.what || x.note || JSON.stringify(x))}`),
        ...(r.nextChase ? [] : ["When to go back to them. Nothing has set a date on this row."]),
      ] })],
    [(hand()?.held || []), (r) => ({ title: r.job, sub: `${r.client} - ${r.value ? gbp(r.value) : "not published"}`,
      evidence: `<p>Priced but <strong>never issued</strong>${r.since ? `, since ${esc(fdate(r.since))}` : ""}. Held by ${esc(r.heldBy || "-")}.
        Calling a client about a quote that never left the building is worse than not calling.</p>
        ${r.caveat ? `<p>${esc(r.caveat)}</p>` : ""}`,
      unknowns: ["Whether it is still going out at all."] })],
    [(crm()?.rows || []).map((r) => ({ ...r, key: "ab:" + r.lead })), (r) => ({
      title: r.job || "no site recorded", sub: `${r.client} - ${gbp(r.value)} ex VAT`,
      evidence: `<p>AdminBase lead <strong>${esc(r.lead)}</strong>, ${esc(r.result || "Live - Quoted")}${
        r.leadDate ? `, dated ${esc(fdate(r.leadDate))}` : ""}${r.days === null || r.days === undefined ? "" : ` - ${r.days} days silent`}.
        ${r.postcode ? `Site ${esc(r.postcode)}. ` : ""}${r.email ? esc(r.email) : "No address on the row."}</p>
        ${r.staleDate ? `<p><strong>The CRM date is not the send date.</strong> AdminBase says ${esc(fdate(r.staleDate.crmDate))};
          the price actually left on ${esc(fdate(r.staleDate.issued))}${r.staleDate.reQuote ? " - this is a re-quote and AdminBase re-dates nothing" : ""}.</p>` : ""}
        ${r.fit ? `<p>The BD log converts ${r.fit.winRate}% at this size. ${esc(r.fit.note || "")}</p>` : ""}`,
      unknowns: ['"Live - Quoted" is what the CRM says, not what the client says. Nobody has asked them.'] })],
    [(JACOB.tenders || []), (t) => ({ title: t.title, sub: `${t.buyer || "buyer not named"}${t.closes ? ` - closes ${fdate(t.closes)}` : ""}`,
      evidence: `<p>${esc(t.why || t.scope || "")}${t.daysLeft !== null && t.daysLeft !== undefined ? ` <strong>${t.daysLeft} days left.</strong>` : ""}</p>
        ${t.url || t.link ? `<p><a href="${esc(t.url || t.link)}" target="_blank" rel="noopener">The notice</a></p>` : ""}`,
      unknowns: t.manual ? ["This one came in by email, not off a feed - the value and the closing date are whatever the sender wrote."] : [] })],
  );
  for (const [list, shape] of pools) {
    const hit = (list || []).find((r) => r.key === key);
    if (hit) return { ...hit, ...shape(hit) };
  }
  const q = quotesOut().find((r) => r.key === key);
  if (q) {
    return { ...q, title: q.job, sub: `${q.client} - ${q.value}`,
      evidence: `<p>Issued against a return date of ${esc(q.due)}${q.days > 0 ? `, ${q.days} days ago` : ""}. Read from Mary's job records - she owns that row, Jacob only looks at it.</p>`,
      unknowns: ["Whether the client has answered. Nothing records that anywhere yet."] };
  }
  const d = (JACOB.drafts?.drafts || []).find((x) => "draft:" + x.id === key);
  if (d) {
    return { key, title: d.subject || d.job || "draft",
      sub: `${d.client || ""} - written for ${d.send_as || "a human"} to send to ${d.to_name || d.to || "them"}`,
      evidence: `<p>${inline((d.body || "").slice(0, 600))}</p>`,
      unknowns: ["Whether anybody has sent it. Jacob drafts; a human sends."] };
  }
  return null;
}

function crmPanel(key) {
  const item = findJacobRow(key);
  if (!item) { toast("Cannot find that row - the board may have been rebuilt"); return; }
  const o = jp(key);
  const log = jNotes(item);
  /* Whatever the row is due on, human or derived - the box opens on it so
     saving never silently drops a date the board had worked out. */
  const dv = jDate(item);
  const dateVal = /^\d{4}-\d{2}-\d{2}$/.test(dv) ? dv : "";
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

    <!-- Adam, 29/07: "they said call back in 2 months". The buttons write the
         date; the box is there for the ones nobody can round to a month. A
         date the generator worked out is shown but not treated as somebody's
         word until a human saves over it. -->
    <div class="panel-sec"><h4>Next action date</h4>
      <div class="req-options" id="jwhen">
        <span class="opt" data-days="1">Tomorrow</span>
        <span class="opt" data-days="7">1 week</span>
        <span class="opt" data-days="14">2 weeks</span>
        <span class="opt" data-days="30">1 month</span>
        <span class="opt" data-days="61">2 months</span>
        <span class="opt" data-days="91">3 months</span>
      </div>
      <div class="ask-inline"><input type="date" id="jdate" value="${esc(dateVal)}"></div>
      <p class="page-sub">${dateVal
        ? (o.next_date
            ? `Set by ${esc(o.updated_by || "team")}.`
            : `Nothing human has set a date on this one - ${esc(fdate(dateVal))} is what the board worked out. Saving makes it ours.`)
        : `Nothing is due on this until somebody says when.`}
        <button class="btn ghost sm" id="jclear">Clear the date</button></p></div>

    <div class="panel-sec"><h4>Add a note</h4>
      <div class="ask-inline"><textarea id="jnote" rows="3" placeholder="Rang Chris - said they are still waiting on the main contract, call back in Sept..."></textarea></div>
      <p class="page-sub">This is added to the log below, not written over it.</p>
      ${log.length ? `<ul class="notelog">${log.map((n) => `<li>
        <span class="dim">${esc(fdate((n.at || "").slice(0, 10)))} &middot; ${esc(n.by || "team")}
          <a class="drop-note" data-at="${esc(n.at)}">remove</a></span>
        <div>${inline(n.text || "")}</div></li>`).join("")}</ul>`
        : `<p class="page-sub">${o.note
            ? `Nothing logged yet. The last note on this row reads: &ldquo;${esc(o.note)}&rdquo;`
            : `Nobody has written anything against this yet.`}</p>`}
      ${o.updated ? `<p class="page-sub">Last edited by ${esc(o.updated_by || "team")} on ${esc((o.updated || "").slice(0, 10))}.</p>` : ""}</div>
    <div class="panel-sec panel-btns">
      <button class="btn" id="jsave">Save</button>
      <button class="btn ghost" id="jdone">Done - take it off the list</button>
    </div>`);

  /* The quick buttons are a calculator for the date box, not a second field -
     so what gets saved is always whatever is showing in the box. */
  $$("#jwhen .opt").forEach((el) => el.addEventListener("click", () => {
    const d = new Date();
    d.setDate(d.getDate() + Number(el.dataset.days));
    $("#jdate").value = d.toISOString().slice(0, 10);
    $$("#jwhen .opt").forEach((o2) => o2.classList.remove("sel"));
    el.classList.add("sel");
  }));
  $("#jclear").addEventListener("click", () => {
    $("#jdate").value = "";
    $$("#jwhen .opt").forEach((o2) => o2.classList.remove("sel"));
  });

  const save = async (state, dropNote) => {
    if (!requireMe("This edit")) return;
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
          next_date: $("#jdate").value.trim(),
          add_note: $("#jnote").value.trim(),
          drop_note: dropNote || "",
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
  /* Removing a note saves everything else in the panel too, then reopens it -
     so the log is one entry shorter and nothing you had typed is lost. */
  $$("#panel .drop-note").forEach((el) => el.addEventListener("click", async () => {
    await save(null, el.dataset.at);
    crmPanel(key);
  }));
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
  /* The register: a list with dates against it, which is what the page is. */
  register: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/><path d="m8.5 14.5 2 2 4-4"/></svg>',
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
  /* The front desk: a sorting tray. Post comes in at the top and leaves down
     one of three routes, which is exactly what the page shows. */
  frontdesk: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 13h5l1.5 2.5h5L16 13h5"/><path d="M4.7 5.4 3 13v5a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1v-5l-1.7-7.6a1.5 1.5 0 0 0-1.5-1.1H6.2a1.5 1.5 0 0 0-1.5 1.1Z"/></svg>',
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
  { key: "queue", label: "Queue", group: "Record", icon: "chaselist", sub: () => `${MQUEUE?.items?.length || 0} waiting, and what kicked the last session off` },
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
  // ADAM, hub-74, 29/07/2026 - the Work section is four pages, in this order:
  // Today, Opportunities, Leads, Ready to Send. That is not cosmetic. It is
  // the two things he says Jacob is for, with the daily list above them and
  // the outbox below: find work Fenster has not been asked for yet
  // (Opportunities), and stay on top of what it has already priced (Leads).
  //
  // What moved, and why nothing was lost. Chasing and the Chase list stopped
  // being working pages - everything on them that a person acts on is now IN
  // Leads (the verified register, the checklist step, the next-chase date and
  // the chase history), and the raw pages survive under Data for audit, which
  // is what he asked for. Out to bid folded into Opportunities: an open tender
  // and a fresh award are both "work Fenster has found and not yet contacted",
  // and splitting them across two pages ranked a cold award notice level with
  // a tender closing on Friday. Enquiries moved to Data as a SOURCE - see the
  // note on that entry, and JAC-16, which is the open question about it.
  { key: "overview", label: "Today", group: "Work", sub: () => `${jToday().length} actions need attention today` },
  { key: "opportunities", label: "Opportunities", group: "Work", icon: "leads", sub: () => {
      const o = oppRows();
      const open = o.filter((r) => r.oppClass === "open").length;
      return `${open} open now, ${o.length - open} prospecting rows behind them`;
    } },
  { key: "leads", label: "Leads", group: "Work", icon: "register", sub: () => {
      const r = registerRows();
      const late = r.filter((x) => jOverdue(x)).length;
      const none = r.filter((x) => jDueIn(x) === null && !x.blocked).length;
      return `${r.length} live quoted jobs - ${late} due now, ${none} with no date set`;
    } },
  { key: "drafts", label: "Ready to Send", group: "Work", sub: () => `${jdrafts().length} drafts written, waiting for a named human to send them` },
  // Reference, not work: what the history says, who Fenster knows, and the
  // book recovered from the last BDM. Grouped apart so the four pages where
  // money moves are not visually equal to the three you read once a week.
  { key: "outcomes", label: "What we win", group: "Know", sub: () => JACOB?.archive
      ? `${JACOB.archive.won} jobs won on record across ${JACOB.archive.distinctClients} clients - ${JACOB.archive.valuedCount} valued so far, largest ${gbpShort(JACOB.archive.knownValues?.[0]?.value)}`
      : JACOB?.outcomes ? `${JACOB.outcomes.summary.won} won on the BD log` : "Nothing read yet" },
  { key: "companies", label: "Companies", group: "Know", sub: () => `${JACOB?.relationships.total || 0} companies, ${JACOB?.totals.dormantWon || 0} who have paid us and gone silent` },
  { key: "jayk", label: "Jayk's book", group: "Know", icon: "jayk", sub: () => `${JACOB?.totals.jaykContacts || 0} contacts recovered from the former BDM` },
  { key: "jmessages", label: "Messages", group: "Talk", icon: "messages", layout: "chat", sub: () => "Two-way line - he picks up what you write on his next pass" },
  { key: "decisions", label: "Jacob needs you", group: "Talk", icon: "requests", sub: () => `${openJacobReqs().length} open, ${JACOB?.decisions.length || 0} standing` },
  // Adam, hub-74: "The separate Chasing and Chase List pages are no longer
  // working pages ... The raw AdminBase Chase List may remain under System or
  // Data for audit purposes, but it must only act as a source feeding Leads."
  // So these four are sources. Nothing here has an action against it that is
  // not already on Leads, Opportunities or Today; they exist so a number on a
  // working page can be traced back to the thing it was read out of.
  { key: "enquiries", label: "Enquiries (mailbox)", group: "Data", sub: () => `Source - ${JACOB?.totals.buyers || 0} buyer conversations out of ${JACOB?.totals.signals || 0} raw messages` },
  { key: "chasing", label: "Issued register", group: "Data", sub: () => JACOB?.handover
      ? `Source - ${JACOB.totals.handoverIssued} verified sends, feeding Leads`
      : "Source - the verified register has not been built" },
  { key: "chaselist", label: "AdminBase (raw)", group: "Data", icon: "chaselist", sub: () => crm()
      ? `Source - ${crm().totals.rows} CRM rows, ${crm().totals.due} of them feeding Leads`
      : "AdminBase has not been read yet" },
  { key: "tenders", label: "Tender feed (raw)", group: "Data", sub: () => `Source - ${JACOB?.totals.tenders || 0} notices, feeding Opportunities` },
  { key: "sources", label: "How this works", group: "System", sub: () => "Where leads come from, what is wired up, and what still is not" },
  { key: "jqueue", label: "Queue", group: "System", icon: "chaselist", sub: () => `${JQUEUE?.items?.length || 0} waiting, and what kicked the last session off` },
  { key: "jlive", label: "Live", group: "System", icon: "live", sub: () => "What Jacob is doing right now" },
];

/* Jacob's own channels. Loaded alongside his board; a failure here leaves the
   rest of his section working rather than blanking the page. */
let JMSGS = [];
let JREQS = [];
/* Joseph's channels. Same shape as Jacob's - the third bot is registry entries
   and these four lines, which is the whole point of the 29/07 restructure. */
let JOMSGS = [];
let JOREQS = [];
let JOSTATUS = null;
/* Every call the front desk has made. Null until the first fetch; `never:true`
   from the API means it has genuinely never run, which the page says out loud
   rather than showing four zeroes. */
let FD = null;
/* What Joseph has changed in the CRM, from the crm_event audit trail. */
let JOEVENTS = [];
let BOTCHAT = [];
let JACTIVITY = null;
/* His bridge can report a status line the same way Mary's does; until it
   starts doing so this stays "unknown" and the card infers from the feed. */
let JSTATUS = null;
/* What is waiting to run and what kicked the last session off, per bot -
   published by the bridges. Zac, 29/07: five messages sat queued for Jacob
   and nothing on the hub could say what they were. */
let MQUEUE = null;
let JQUEUE = null;
/* The CRM overlay. Jacob derives a state and a next action for everything
   from the evidence; this is a human saying otherwise, keyed by the stable
   key his generator emits. It survives a rebuild of jacob-data.js, which is
   the whole point - a board you cannot correct is a report, not a CRM. */
let JPIPE = {};
/* What was on screen last time render() ran. A background refresh must leave
   the page exactly where you left it; only a deliberate tab change resets it. */
let LAST_VIEW = { page: null, bot: null };
const openJacobReqs = () => JREQS.filter((r) => r.status !== "answered");
const openJosephReqs = () => JOREQS.filter((r) => r.status !== "answered");

async function sendToJoseph(body, context = "") {
  if (!requireMe("A message to Joseph")) return;
  const res = await api("joseph/messages", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ author: who(), body, context }),
  });
  JOMSGS = await api("joseph/messages").catch(() => JOMSGS);
  if (cutOff(res)) return;
  toast("Sent - Joseph picks this up on his next pass");
}

async function sendToJacob(body, context = "") {
  if (!requireMe("A message to Jacob")) return;
  const res = await api("jacob/messages", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ author: who(), body, context }),
  });
  JMSGS = await api("jacob/messages").catch(() => JMSGS);
  if (cutOff(res)) return;
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
/* Won, lost and closed are different: the job is over, but the record is the
   most valuable one on the board - it is the only place at Fenster an outcome
   gets written down at all. So a decided row leaves the live bands and the
   chase list and keeps its own section on Leads. It never disappears. */
const jDecided = (r) => ["won", "lost", "closed"].includes(jState(r));

/* ---- The two things Adam asked for on 29/07 ----
   A date to do it on, and a log of what was said - not one note that the next
   call overwrites. A human date always wins over one the generator derived
   (nextChase on the register, followUp in AdminBase): a person who has just
   spoken to the client knows something no file does. */
const jDate = (r) => jp(r.key).next_date || r.nextChase || r.nextAction || "";
const jDateIsHuman = (r) => !!jp(r.key).next_date;
const jNotes = (r) => {
  const raw = jp(r.key).notes;
  if (!raw) return [];
  try { const a = JSON.parse(raw); return Array.isArray(a) ? a : []; } catch { return []; }
};
/* Sorting a register by when to act on it needs one number per row. Overdue
   first (most overdue at the top), then dated, then everything nobody has put
   a date on - which is the pile that matters most and reads as the least
   urgent, so the page counts it out loud instead of burying it. */
const jDueIn = (r) => {
  const d = jDate(r);
  return /^\d{4}-\d{2}-\d{2}$/.test(d) ? daysUntil(d) : null;
};
const jOverdue = (r) => { const n = jDueIn(r); return n !== null && n <= 0; };

/* How much a date is worth, which is not the same as how overdue it is.
   Sorting the register on overdue days alone opened the page on a Bradford
   Watts row 524 days past a follow-up date AdminBase set in 2025, and buried
   Leys Park, Ninn Lane and St Mary's - three verified quotes genuinely due
   today - forty rows down. A promise a human made outranks a date read out of
   a sent message, which outranks a date a CRM nobody closes happens to hold. */
const jRank = (r) => jDateIsHuman(r) ? 0
  : r.tier === "register" ? 1 : r.tier === "priced" ? 2 : 3;
const byDue = (a, b) => jRank(a) - jRank(b) || (jDueIn(a) ?? 1e6) - (jDueIn(b) ?? 1e6);

/* One chip that says when, in the words somebody would use out loud. */
function dueChip(r) {
  const d = jDate(r);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) {
    /* A row with no date is usually a hole. Brandon Estate is the exception
       that proves it has to be checked: GBP 7.2m, deliberately undated,
       because Elkins cannot answer until they hear on their own bid and Chris
       Conlon has undertaken to tell us. `reviewOn` is the day to check whether
       that has happened - it is explicitly NOT a day to ring anyone, so it is
       shown as a review and never sorted with the chase dates. */
    if (r.blocked) {
      return `<span class="chip warn">cannot answer yet</span>`
        + (r.reviewOn ? `<small class="dim">review ${esc(fdate(r.reviewOn))}</small>` : "");
    }
    return `<span class="chip danger">no date set</span>`;
  }
  const n = daysUntil(d);
  const tone = n <= 0 ? "danger" : n <= 7 ? "warn" : "navy";
  const word = n < 0 ? `${-n}d overdue` : n === 0 ? "today" : `in ${n}d`;
  return `<span class="chip ${tone}">${esc(fdate(d))}</span>`
    + `<small class="dim">${word}${jDateIsHuman(r) ? "" : " &middot; derived"}</small>`;
}

/* Adam, hub-74: a Lead's status is "live, won, lost, on hold or closed". Those
   five were not in the list, so there was no way to record on the board that a
   job had been won - the only honest options were "done" and "dead", which say
   nothing about which. The older words stay because two hundred rows already
   carry them and deleting a state silently re-labels every row that had it. */
const JSTATES = ["live", "waiting", "quoted", "gone quiet", "on hold", "won",
                 "lost", "closed", "dormant", "dead", "done"];
const JOWNERS = ["Adam", "Jacob", "Gintare", "Mary", "Zac", "-"];

/* One colour vocabulary across every page, so "amber" always means the same
   thing whether it is a company, an enquiry or a quote sitting out. */
function stateTone(s) {
  if (["live", "done", "won"].includes(s)) return "ok";
  if (["waiting", "quoted", "dormant - has bought", "dormant", "on hold"].includes(s)) return "warn";
  if (["gone quiet", "stale", "lost"].includes(s)) return "danger";
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

/* ---------------- The lead register ----------------
   Adam, 29/07: "we need all of our current live leads that need chasing and
   updating in one clear dashboard ... a dashboard on which we can manage all
   live projects we have quoted."

   Everything Fenster has priced and sent lived on three pages that could not
   see each other: the verified handover register (Chasing), the jobs still
   only in Mary's records (also Chasing, dated off a different clock), and the
   264 AdminBase rows (Chase list). Nothing joined them, nothing sorted by when
   to act, and the CRM overlay could not even open most of them. This is the
   one list, ordered by the only question that matters on a Monday: what is due.

   The three tiers are kept visible rather than blended. A date read out of a
   sent message and a date AdminBase happens to hold are not the same class of
   fact, and a single table that hides which is which is how they get confused. */
const TIERS = {
  register: { label: "Register", note: "Issue date read out of the sent message" },
  priced: { label: "Mary's records", note: "Dated off a return date, not a send - treat the day count as a guess" },
  adminbase: { label: "AdminBase", note: "The CRM's word that it is quoted, not the client's" },
};

function registerRows() {
  const out = [];
  for (const r of handIssued()) {
    out.push({ ...r, tier: "register", quotedOn: r.issued,
      silent: r.daysSinceClient === null || r.daysSinceClient === undefined
        ? r.daysOut : r.daysSinceClient });
  }
  for (const q of quotesOut()) {
    // Priced and never issued is a real state and it is not chaseable - it
    // belongs to Mary until she says it has been sent (Adam, hub-77, 29/07).
    if (q.unsent || jShut(q)) continue;
    out.push({ ...q, tier: "priced", value: poundsOf(q.value) || null,
      valueText: q.value, quotedOn: q.due, silent: q.days });
  }
  for (const r of (crm()?.due || [])) {
    // `onBoard` is the same job already on the register under its verified
    // key. Showing it twice would double the money on this page.
    if (r.onBoard) continue;
    if (r.outlier && !r.confirmed) continue;
    const row = { ...r, key: "ab:" + r.lead, tier: "adminbase",
      // A re-quote leaves the AdminBase date alone, so where a verified send
      // says otherwise the send wins - that is the only date worth chasing on.
      quotedOn: r.staleDate ? r.staleDate.issued : r.leadDate,
      silent: r.days };
    if (jShut(row)) continue;
    out.push(row);
  }
  return out;
}

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
      // Adam, hub-77, 29/07: a priced job that has not been submitted sits with
      // Mary, and it is not Jacob's until she says it has gone to the client.
      state = "not issued"; owner = "Mary";
      next = `Not out yet - priced and waiting to be issued. Mary's until she says it has gone to the client; nothing to chase before that.`;
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
    // to do today. They live on Leads so nothing disappears.
    if (jShut(q) || q.owner === "-" || q.unsent) continue;
    out.push({
      key: q.key, company: q.client, headline: q.job, project: q.job,
      what: `${q.value} - issued, nothing back`,
      owner: jOwner(q), next: jNext(q), state: jState(q), page: "leads",
      deadline: q.due,
      why: q.days === null ? "Issued with no date recorded against it"
        : `Return date was ${q.days} day${q.days === 1 ? "" : "s"} ago and nothing has come back`,
      score: q.days >= 21 ? 90 : 70,
    });
  }
  /* A date somebody set, that has now arrived. This is the whole point of
     asking for one: "call back in two months" is worthless if the two months
     pass and nothing says so. It outranks everything else on the page, because
     everything else is the board's opinion and this is a promise a human made.
     Anything already on the list from the generator is left alone. */
  const already = new Set(out.map((a) => a.key));
  for (const r of registerRows()) {
    if (already.has(r.key) || !jDateIsHuman(r) || !jOverdue(r)) continue;
    const late = -jDueIn(r);
    out.push({
      key: r.key, company: r.client, headline: r.job, project: r.job,
      what: `${r.value ? gbp(r.value) : r.valueText || "no value"} - you said you would go back to them ${
        late === 0 ? "today" : `${late} day${late === 1 ? "" : "s"} ago`}`,
      owner: jOwner(r), next: jNext(r), state: jState(r), page: "leads",
      deadline: jDate(r),
      why: late === 0 ? "You set today as the day to go back to them"
        : `You said you would go back to them ${late} day${late === 1 ? "" : "s"} ago`,
      score: 100 + Math.min(late, 20),
    });
  }
  return out.sort((a, b) => (b.score || 0) - (a.score || 0));
}

/* ---------------- Opportunities ----------------
   Adam, hub-74: "Opportunities must contain new commercial glazing work that
   Jacob has found and that Fenster has not yet contacted", covering open
   tenders, glazing packages, main contracts whose bidders still have to be
   found, and awards where there is still a credible contact opportunity.

   That is one page, and it used to be two. "Out to bid" held the tender feed
   and "Opportunities" held companies that had just won an award - which meant
   a job closing on Friday and a notice published after the enquiry list was
   drawn up sat on separate pages, each looking like the whole picture.

   His other instruction here is the one that changes the shape: "Cold or weak
   award notices must not be presented as equal to genuine open tender
   opportunities." So an award notice is never in the same table as a live
   tender - it is behind a fold, marked prospecting, and it says on its face
   that by the time an award publishes the subcontractors are usually chosen. */
function oppRows() {
  if (!JACOB) return [];
  const out = [];
  const src = (t) => t.manual ? `Email alert${t.ref ? ` - ${t.ref}` : ""}`
    : t.procontract ? "ProContract advert (public)"
    : "Contracts Finder / Find a Tender";
  for (const t of (JACOB.tenders || [])) {
    if (jShut(t)) continue;
    // Confident and still open is an opportunity somebody can act on today.
    // Everything else on this feed is a reading job first.
    const open = t.confident && t.tier !== "text-only"
      && t.coverage !== "outside coverage"
      && (t.daysLeft === null || t.daysLeft === undefined || t.daysLeft >= 0);
    out.push({
      ...t,
      oppClass: open ? "open" : "read",
      company: t.buyer || "",
      project: t.title,
      location: t.where || t.regions?.[0] || "",
      scope: t.why || t.scope || t.cpv || "",
      sourceName: src(t),
      deadline: t.closes || "",
      relevance: [
        t.tier === "direct" ? "The buyer is asking for glazing work by name"
          : t.tier === "main-contract" ? "A building contract with a glazing package inside it - the job is finding who is bidding"
          : "Matched on wording, not on a CPV code - read it before acting",
        t.record ? `Fenster has ${t.record.won}W ${t.record.lost}L with this buyer` : "",
        t.knownBuyer ? "Fenster knows this buyer" : "",
        t.fit?.note || "",
      ].filter(Boolean).join(". "),
    });
  }
  const award = (r, cls, relevance) => ({
    ...r,
    oppClass: cls,
    company: r.supplier,
    project: r.title,
    location: r.area || "",
    scope: r.cpv || "",
    sourceName: "Contracts Finder award notice",
    deadline: "",
    value: r.total || r.value,
    relevance: [relevance, r.fit?.note || ""].filter(Boolean).join(". "),
    state: r.state || "not contacted",
  });
  for (const r of (JACOB.warm || [])) {
    if (jShut(r)) continue;
    out.push(award(r, "prospect", `Has bought from Fenster and has just won ${fdate(r.awarded) || "recent"} work`));
  }
  for (const r of (JACOB.known || [])) {
    if (jShut(r)) continue;
    out.push(award(r, "prospect", "Quoted before with no recorded win, and building again"));
  }
  for (const r of (JACOB.cold || [])) {
    if (jShut(r)) continue;
    out.push(award(r, "cold", "No relationship at all - cold approach is blocked on JAC-2"));
  }
  return out;
}

/* Adam's core rule, hub-74: "Every active Opportunity and Lead must have a
   clearly stated next action. Every active Lead must also have a next-action
   deadline and a named owner. Where any of these are missing, the record must
   appear on Today as an exception requiring attention."

   Deliberately NOT counted as exceptions: a row blocked by something the
   client cannot control (Brandon Estate has no date on purpose, because
   Elkins cannot answer until they hear on their own bid), and a row whose
   owner is honestly nobody because Adam has ruled it out. Flagging those
   every day is how a red number stops meaning anything.

   And the split. The first version of this listed all 64 exceptions on Today
   and 53 of them were AdminBase rows nobody has ever opened - a CRM export of
   264 rows that was bulk-loaded on 28/07, not 53 separate oversights. That is
   one fact printed 53 times, and it pushed the four verified quotes genuinely
   due today off the first screen. So `.crm` is the untouched CRM tail, kept
   whole and counted, and `.own` is everything Fenster has actually worked.
   Both are on the page; only one of them is a list. */
function jExceptions() {
  const own = [], crm = [];
  const flag = (r, page, project, missing) => {
    const row = {
      key: r.key, company: r.client || r.company || "", project, page,
      owner: jOwner(r), next: jNext(r), state: jState(r), deadline: jDate(r),
      missing, why: `Missing ${missing.join(" and ")}`,
      what: r.value ? gbp(r.value) : (r.valueText || ""),
      score: 95,
    };
    // Touched by a human in any way - a date, a note, an owner, a state - and
    // it is Fenster's row rather than a line in an import.
    const worked = jDateIsHuman(r) || jNotes(r).length || !!jp(r.key).owner
      || !!jp(r.key).state || !!jp(r.key).next_action;
    (r.tier === "adminbase" && !worked ? crm : own).push(row);
  };
  for (const r of registerRows()) {
    if (r.blocked || jDecided(r)) continue;
    const missing = [];
    if (!jNext(r)) missing.push("a next action");
    if (jDueIn(r) === null) missing.push("a next-action deadline");
    if (jOwner(r) === "-") missing.push("an owner");
    if (missing.length) flag(r, "leads", r.job || "no site recorded", missing);
  }
  for (const r of oppRows()) {
    // Cold rows are unowned by decision, not by omission - JAC-2.
    if (r.oppClass === "cold") continue;
    if (!jNext(r)) flag(r, "opportunities", r.project || "", ["a next action"]);
  }
  return { own, crm };
}

/* The Today page itself. Adam: "Today must pull these actions from the
   relevant individual pages. It must not hold separate duplicate records."
   So this is a union of the pages' own rows, deduplicated on the key that
   every board row already carries - not a second list with its own state. */
function jToday() {
  const seen = new Set();
  const out = [];
  const take = (rows) => {
    for (const a of rows) {
      if (!a || seen.has(a.key) || jShut(a)) continue;
      seen.add(a.key);
      out.push(a);
    }
  };
  // The same union, in the same order, as the page renders - so the count in
  // the sidebar is the number of rows a person will actually find when they
  // open it. Leads first: Adam, hub-76, puts due and overdue Leads at the top
  // of Today and nothing is folded out of them any more.
  take(jLeadsDue().map(jLeadRow));
  take(jLeadsTomorrow().map(jLeadRow));
  take(jActions());
  const ex = jExceptions();
  take(ex.own);
  take(ex.crm);
  return out;
}

/* Everything on Leads that is due or overdue today, and everything falling due
   tomorrow. Shared by the Today page and the daily chase email so the two can
   never disagree about what is due.

   THIS USED TO FILTER OUT THE CRM TAIL and it no longer does. Adam, hub-76,
   29/07/2026: "Do not block, fold, hide or exclude Leads because their dates
   came from AdminBase, are historic, or have not yet been manually verified ...
   We accept that there is a backlog to work through. These records must remain
   visible until somebody reviews, closes or reschedules them. Records with
   unverified or system-generated dates may be clearly labelled, but they must
   still be included."

   The previous version counted those rows in one line at the foot of the page,
   because 134 of them are a CRM export nobody has opened and listing them
   pushed the four quotes genuinely due off the first screen. That was a real
   problem and it was my call to make it that way. It is Adam's backlog and he
   has looked at it and said list them. So they are listed, and the labelling is
   the half of the bargain I owe him: every row says where its date came from,
   and the verified ones sort to the top. */
const jDateSource = (r) => (jDateIsHuman(r) ? "Set by a person"
  : r.tier === "adminbase" ? "Unverified - AdminBase generated this date"
  : "From the verified quote register");
const jVerified = (r) => jDateIsHuman(r) || r.tier !== "adminbase";

const jLeadsDue = () => registerRows()
  .filter((r) => !r.blocked && !jShut(r) && !jDecided(r) && jOverdue(r))
  .sort((a, b) => (jVerified(b) - jVerified(a)) || (jDueIn(a) - jDueIn(b))
    || ((b.value || 0) - (a.value || 0)));

const jLeadsTomorrow = () => registerRows()
  .filter((r) => !r.blocked && !jShut(r) && !jDecided(r) && jDueIn(r) === 1)
  .sort((a, b) => (jVerified(b) - jVerified(a)) || ((b.value || 0) - (a.value || 0)));

/* A Leads row in the shape the Today table renders. `why` is Adam's "reason it
   appears on Today" column and it carries the date source, because an overdue
   date a person set and an overdue date a CRM invented call for different
   phone calls. */
const jLeadRow = (r) => {
  const late = -jDueIn(r);
  return {
    key: r.key, company: r.client, headline: r.job, project: r.job,
    what: r.value ? gbp(r.value) : r.valueText || "no value recorded",
    owner: jOwner(r), next: jNext(r), state: jState(r), page: "leads",
    deadline: jDate(r), verified: jVerified(r),
    why: `${late > 0 ? `${late} day${late === 1 ? "" : "s"} overdue`
      : late === 0 ? "Due today" : "Due tomorrow"}. ${jDateSource(r)}`,
    score: 100 + Math.min(late, 20),
  };
};

const JACOB_RENDER = {
  /* Adam, hub-74: four pages are working pages and the rest are sources. A
     page that used to be one and is now the other has to SAY so at the top,
     or somebody works it for a fortnight and wonders why nothing they do
     shows up on Today. */
  _source(feeds, note) {
    return `<div class="planned-note"><p><strong>This is a source page, not a working page.</strong>
      Everything on it that somebody acts on is on <a data-go="${esc(feeds[0])}">${esc(feeds[1])}</a>
      and on <a data-go="overview">Today</a>. It is kept for audit - so a number on a working page can
      be traced back to the thing it was read out of. ${note || ""}</p></div>`;
  },

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

  /* ------------------------------------------------ Today
     Adam, hub-74: "Today must act as the main daily action list ... Every item
     shown on Today must include: Client. Project. Current stage. Owner. Next
     action. Action deadline. Reason it appears on Today."

     That last column is the one the page did not have. A row could be here
     because a date arrived, because a quote has gone unanswered for a month,
     or because nobody has ever been given it - and the card told you what to
     do without ever telling you which of those it was. */
  _todayRows(list) {
    if (!list.length) return `<div class="empty"><strong>Nothing outstanding</strong></div>`;
    return `<table class="tbl"><thead><tr>
        <th>Client</th><th>Project</th><th>Stage</th><th>Next action</th>
        <th>Deadline</th><th>Why it is here</th><th>Owner</th></tr></thead><tbody>
      ${list.map((a) => `<tr data-jkey="${esc(a.key)}">
        <td class="job-cell"><strong>${esc(a.company || "client not named")}</strong>
          ${a.what ? `<small>${esc(String(a.what).slice(0, 90))}</small>` : ""}</td>
        <td>${esc(a.project || a.headline || "-")}</td>
        <td>${stateChip(a)}</td>
        <td style="max-width:360px"><div class="clamp4">${inline(jNext(a)) || `<span class="dim">Nothing written - open it and give it one</span>`}</div>
          ${jNote(a) ? `<span class="lognote">Last note: ${esc(jNote(a).slice(0, 140))}</span>` : ""}</td>
        <td class="num">${a.deadline
          ? `<strong>${esc(fdate(a.deadline))}</strong>${/^\d{4}-\d{2}-\d{2}$/.test(a.deadline)
              ? `<small class="dim">${daysUntil(a.deadline) < 0 ? `${-daysUntil(a.deadline)}d overdue`
                 : daysUntil(a.deadline) === 0 ? "today" : `in ${daysUntil(a.deadline)}d`}</small>` : ""}`
          : `<span class="chip danger">none set</span>`}</td>
        <td style="max-width:240px"><small>${esc(a.why || "")}</small>
          <small class="dim" data-go="${esc(a.page || "overview")}">${esc(a.page || "")} &rarr;</small></td>
        <td>${ownerTag(a)}</td></tr>`).join("")}
    </tbody></table>`;
  },

  /* Adam, hub-76, 29/07/2026, and the section order below is his:
       "Today must show: 1. Due and overdue Lead actions. 2. Tomorrow's Lead
        actions in a separate upcoming section. 3. Opportunity actions requiring
        attention. 4. Ready-to-Send items. 5. Records missing an owner, next
        action or deadline."
     plus "Do not block or fold overdue Leads out of the Today workload" and
     "Historic or unverified CRM records may be labelled clearly, but they must
     remain visible until somebody updates, closes or reschedules them."

     So nothing on this page is behind a fold any more. The exceptions block,
     which used to lead, is now last because that is the order he asked for. */
  overview() {
    const t = JACOB.totals;
    const acts = jActions().filter((a) => !jShut(a));
    const seen = new Set();
    const fresh = (rows) => rows.filter((a) => !seen.has(a.key) && seen.add(a.key));

    // 1 and 2: every Lead due, overdue or falling due tomorrow - CRM tail and
    // all, each row labelled with where its date came from.
    const leadsDue = fresh(jLeadsDue().map(jLeadRow));
    const leadsTomorrow = fresh(jLeadsTomorrow().map(jLeadRow));
    const opps = fresh(acts.filter((a) => a.page === "opportunities"));
    const readyToSend = fresh(acts.filter((a) => a.page === "drafts"));
    const rest = fresh(acts.filter(
      (a) => !["leads", "opportunities", "drafts"].includes(a.page)));
    // 5: the completeness exceptions. `.own` is what somebody has worked and
    // `.crm` is the untouched import - both listed now, kept apart so the
    // difference is legible rather than hidden.
    const ex = jExceptions();
    const exceptions = ex.own.filter((a) => !seen.has(a.key));
    const crmGaps = ex.crm.filter((a) => !seen.has(a.key));

    const total = leadsDue.length + leadsTomorrow.length + opps.length
      + readyToSend.length + rest.length + exceptions.length + crmGaps.length;
    const unverified = leadsDue.filter((a) => !a.verified).length;
    const mine = (o) => [...leadsDue, ...opps, ...rest, ...exceptions]
      .filter((a) => jOwner(a) === o).length;
    // Verified sends where we have them; the old return-date guess only as a
    // fallback, because a headline number ought to be the sourced one.
    const outValue = t.handoverValue || quotesWaiting().reduce((n, q) => n + poundsOf(q.value), 0);
    const heldBack = Math.max(...[0, ...(JACOB.actions || []).map((a) => a.heldBack || 0)]);
    return `
      <div class="stats">
        <div class="stat ${total ? "red" : "green"}"><div class="n">${total}</div><div class="l">Actions needing attention today</div></div>
        <div class="stat ${leadsDue.length ? "red" : "green"}"><div class="n">${leadsDue.length}</div><div class="l">Leads due or overdue${unverified ? `, ${unverified} on an unverified date` : ""}</div></div>
        <div class="stat ${mine("Adam") ? "amber" : "green"}"><div class="n">${mine("Adam")}</div><div class="l">Waiting on Adam - a call or a decision</div></div>
        <div class="stat amber" data-go="leads"><div class="n">${gbpShort(outValue)}</div><div class="l">Issued and waiting on an answer, ${t.handoverDue ?? "?"} chaseable today</div></div>
        <div class="stat ${t.tendersClosing ? "red" : ""}" data-go="opportunities"><div class="n">${t.tenders || 0}</div><div class="l">Open opportunities, ${t.tendersClosing || 0} closing this week</div></div>
        <div class="stat" data-go="drafts"><div class="n">${jdrafts().length}</div><div class="l">Drafts written, waiting for a human to send</div></div>
      </div>

      <div class="section"><div class="section-head"><h3>1. Leads due or overdue today</h3>
        <a data-go="leads">Leads &rarr;</a></div>
        ${unverified ? `<div class="planned-note"><strong>Nothing is folded out of this list.</strong>
        Adam, ${esc(niceDate("2026-07-29"))}: overdue Leads stay on Today, labelled, until somebody
        reviews, closes or reschedules them. ${unverified} of the ${leadsDue.length} below carry a date
        AdminBase generated rather than one a person set - the "why it is here" column says which, and
        the rows a person has worked are at the top. Touch one and it moves up.</div>` : ""}
        ${this._todayRows(leadsDue)}</div>

      <div class="section"><div class="section-head"><h3>2. Coming up tomorrow</h3>
        <span class="page-sub">Advance notice only - nothing here needs doing today</span></div>
        ${leadsTomorrow.length ? this._todayRows(leadsTomorrow)
          : `<div class="empty"><strong>Nothing is scheduled for tomorrow</strong></div>`}</div>

      <div class="section"><div class="section-head"><h3>3. Opportunities needing attention</h3>
        <a data-go="opportunities">Opportunities &rarr;</a></div>
        ${this._todayRows(opps)}</div>

      <div class="section"><div class="section-head"><h3>4. Ready to send</h3>
        <a data-go="drafts">Ready to Send &rarr;</a></div>
        ${this._todayRows(readyToSend)}</div>

      <div class="section"><div class="section-head">
        <h3>5. Records missing an owner, a next action or a deadline</h3>
        <span class="page-sub">Adam's completeness rule - a record without these three is not finished</span></div>
        <div class="planned-note">These are not overdue. They are worse: nothing on them says who does
        what or by when, so they cannot go overdue. Rows blocked by something the client cannot
        control are deliberately left out - Brandon Estate has no date on purpose, and it is named at
        the foot of the daily email instead.</div>
        ${this._todayRows(exceptions)}
        ${crmGaps.length ? `<div class="planned-note" style="margin-top:14px"><strong>The
        ${crmGaps.length} below are the same problem, on rows nobody has opened yet.</strong> They
        arrived as one AdminBase export on 28 July and have not been touched since, so they are one
        fact rather than ${crmGaps.length} separate oversights - kept in their own block for that
        reason, and listed rather than folded on Adam's instruction of 29 July. The moment somebody
        sets a date, writes a note or takes ownership of one, it moves into the list above.</div>
        ${this._todayRows(crmGaps)}` : ""}</div>

      ${rest.length ? `<div class="section"><div class="section-head"><h3>Buyers writing in, and companies worth a call</h3>
        <span class="page-sub">Neither an opportunity Jacob found nor a job Fenster has quoted - see JAC-16</span></div>
        ${this._todayRows(rest)}</div>` : ""}

      ${heldBack ? `<div class="section"><div class="section-head">
        <h3>What this page is deliberately not listing</h3></div>
        <div class="planned-note"><p><strong>${heldBack} further ranked items</strong> did not fit the
        per-page room on the digest and are on their own pages.</p></div></div>` : ""}

      <div class="section"><div class="section-head"><h3>What Jacob cannot see</h3></div>
        <div class="planned-note">
          <p><strong>Whether anyone has already replied.</strong> Mailbox intake reads
          received mail only, so an enquiry Gintare answered an hour ago looks exactly like
          one nobody has touched. Every "check for a reply, then call" above exists because
          of that gap. <a data-go="decisions">JAC-5</a> asks for sent items.</p>
          <p><strong>Ten quotes are now the exception.</strong> Mary read estimating@ sent
          items on 28/07 and dated every one of them against the message that actually left
          the building, so the <a data-go="leads">Leads</a> register is sourced rather than
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
          <small>${esc(t.person ? t.company : t.contact)} &middot; ${t.messages} msg${t.messages === 1 ? "" : "s"} &middot; last ${esc(fdate(t.last))}</small></td>
        <td>${esc(t.subject)}
          ${t.stage === "decided" ? ` <span class="pill exact">they have answered</span>` : ""}
          ${t.relationship !== "unknown" ? ` <span class="pill ${t.relationship === "won" ? "exact" : "strong"}">${esc(t.relationship)}</span>` : ""}
          ${job ? ` <span class="pill live">Mary has this</span>` : ""}</td>
        <td>${stateChip(t)}<small class="dim">${t.days}d</small></td>
        <td style="max-width:340px"><div class="clamp4">${inline(jNext(t))}</div></td>
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
      ${this._source(["overview", "Today"], `A live buyer conversation is neither an Opportunity nor a
        quoted Lead in Adam's structure, so for now anything actionable on it is surfaced on Today and
        the raw conversations live here. That gap is <a data-go="decisions">JAC-16</a>.`)}
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
        <a data-go="leads">Leads &rarr;</a></div>
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

  /* ------------------------------------------------ the register
     Adam's page. One table, every live quoted job, ordered by when somebody
     said they would go back to it - and the rows nobody has said that about
     counted out loud rather than sorted to the bottom and forgotten. */
  leads() {
    const all = registerRows();
    const decided = all.filter((r) => jDecided(r));
    const rows = all.filter((r) => !jDecided(r));
    const h = hand();
    if (!all.length) {
      return `<div class="empty"><strong>Nothing quoted and live</strong>
        Either the register has not been built or everything on it is closed.</div>`;
    }
    const dated = rows.filter((r) => jDueIn(r) !== null);
    const overdue = dated.filter((r) => jDueIn(r) <= 0).sort(byDue);
    const soon = dated.filter((r) => jDueIn(r) > 0).sort(byDue);
    const undated = rows.filter((r) => jDueIn(r) === null)
      .sort((a, b) => jRank(a) - jRank(b) || (b.value || 0) - (a.value || 0));
    // A blocked row has no date on purpose - the client physically cannot
    // answer. Counting it as a gap turns Brandon Estate into a red number
    // every day until Elkins hear, which trains people to ignore the number.
    const gaps = undated.filter((r) => !r.blocked);
    const val = (list) => list.reduce((n, r) => n + (r.value || 0), 0);
    const week = soon.filter((r) => jDueIn(r) <= 7);
    const human = rows.filter((r) => jDateIsHuman(r)).length;
    const noted = rows.filter((r) => jNotes(r).length).length;

    /* AdminBase is 200-odd rows and the register is eleven. Showing all of it
       here would bury the eleven, so the tail is capped by value INSIDE each
       band and the page says how many it is holding back. Anything verified is
       never capped - a cap that can hide Gordon Court is a bug, not a limit. */
    const CAP = 25;
    const band = (list, title, blurb) => {
      // The cap falls on AdminBase's own rows only, and never on one somebody
      // has actually put a date against - a human's edit outranks its origin.
      const kept = [], tail = [];
      for (const r of list) (r.tier === "adminbase" && !jDateIsHuman(r) ? tail : kept).push(r);
      const shown = kept.concat(tail.slice(0, CAP));
      const held = tail.length - Math.min(tail.length, CAP);
      if (!list.length) return "";
      return `<div class="section"><div class="section-head"><h3>${title}</h3>
        <span class="page-sub">${list.length} job${list.length === 1 ? "" : "s"}, ${gbpShort(val(list))}</span></div>
        ${blurb ? `<div class="planned-note">${blurb}</div>` : ""}
        ${this._regTable(shown)}
        ${held ? `<p class="page-sub">${held} further AdminBase row${held === 1 ? " is" : "s are"} in this
          band and not shown - <a data-go="chaselist">the AdminBase list</a> has all of them. Nothing on
          the register is ever held back, and neither is anything you have put a date on.</p>` : ""}
      </div>`;
    };

    return `
      <div class="stats">
        <div class="stat ${overdue.length ? "red" : "green"}"><div class="n">${overdue.length}</div>
          <div class="l">Due today or overdue - ${gbpShort(val(overdue))}</div></div>
        <div class="stat ${week.length ? "amber" : ""}"><div class="n">${week.length}</div>
          <div class="l">Due inside a week</div></div>
        <div class="stat ${gaps.length ? "red" : "green"}"><div class="n">${gaps.length}</div>
          <div class="l">No next action date on them at all${
            undated.length - gaps.length ? `, plus ${undated.length - gaps.length} that cannot answer yet` : ""}</div></div>
        <div class="stat"><div class="n">${gbpShort(val(rows))}</div>
          <div class="l">Quoted, live and not yet decided - ${rows.length} jobs</div></div>
      </div>

      <div class="section"><div class="section-head"><h3>What this page is</h3></div>
        <div class="planned-note">
          <p><strong>Every live job Fenster has quoted, in one list, ordered by when to go back to it.</strong>
          Click any row to set a date, write down what was said, change the status or hand it to
          somebody. What you write survives every rebuild of this board.</p>
          <p><strong>Where the rows come from, because it changes how much you should trust them.</strong>
          ${rows.filter((r) => r.tier === "register").length} are on the verified register - the issue date on
          those was read out of the message that actually left estimating@.
          ${rows.filter((r) => r.tier === "priced").length} are still only in Mary's job records and are dated
          off a return date, which is a different date on a different clock.
          ${rows.filter((r) => r.tier === "adminbase").length} are AdminBase rows saying "Live - Quoted",
          which is what the CRM says and not what the client says. Every figure here is ex VAT;
          AdminBase's own are not.</p>
          <p><strong>${human} of ${rows.length} rows carry a date a human has set.</strong>
          The rest show either a date the board worked out - marked <em>derived</em>, which is a
          suggestion, not somebody's word - or nothing at all. ${noted} carry a note.
          A quote with no next date is how one goes quiet without anybody noticing, which is the
          thing this page exists to stop.</p>
        </div></div>

      ${h?.checklist ? `<div class="section"><div class="section-head"><h3>What a chase is for</h3>
        <span class="page-sub">Adam's own fifteen-step checklist - steps 8-15 are the ones on this page</span></div>
        <div class="planned-note">
          <p><strong>Not "any news".</strong> ${esc(h.checklist.why)} A chase has to come back with
          one of these six, and whichever one does sets the next date:
          ${h.checklist.asks_of_a_chase.map((q) => esc(q)).join(" &middot; ")}.</p>
          <p>${esc(h.checklist.standing_warning_from_adam)}
          <em>${esc(h.checklist.unconfirmed)}</em></p>
          <p><strong>${esc(h.rule?.text || "")}</strong> Every issue date on a Register row was read out
          of the message that actually left estimating@ - ${esc(h.verification?.source || "")}. That is
          why the tier is on the row: it changes how much the date is worth.</p>
        </div></div>` : ""}

      ${band(overdue, "Due now", `Most overdue first. A day count is not on its own an
        instruction - a row marked <em>cannot answer yet</em> is blocked by something the client
        cannot control, and ringing them about it wastes the relationship.`)}
      ${band(soon, "Coming up", "")}
      ${band(undated, "Nobody has said when", `Largest first. These are not less urgent
        than the ones above - they are the ones no date has ever been set on, which is a different
        and worse problem. Give each one a date and it moves into the bands above.
        The exception is a row marked <em>cannot answer yet</em>: that one is undated on purpose,
        because the client is waiting on something they do not control.`)}

      ${this._repricing()}

      ${decided.length ? `<div class="section"><div class="section-head"><h3>Decided</h3>
        <span class="page-sub">${decided.length} marked won, lost or closed - ${gbpShort(val(decided))}</span></div>
        <div class="planned-note">Off the chase list and off Today, kept here because this is the only
        place in the company an outcome gets written down at all. The Opportunity Log's W/L column and
        the Estimating Log's are both mostly empty; a row here is worth more than either.</div>
        ${this._regTable(decided)}</div>` : ""}

      ${handHeld().length ? `<div class="section"><div class="section-head">
        <h3>Priced but never issued - Mary's, not chaseable</h3>
        <span class="page-sub">${gbpShort(handHeld().reduce((n, r) => n + (r.value || 0), 0))} of work that has not left the building</span></div>
        <div class="planned-note"><strong>Adam, hub-77, 29 July 2026: all three are waiting to be
        submitted to the client, they sit with Mary, and they are not Jacob's until Mary says they
        have been sent.</strong> They are listed here so the money is visible and so nobody assumes a
        priced job went out - not as work on this page. Calling a client about a quote that never left
        the building is worse than not calling.</div>
        <table class="tbl"><thead><tr>
          <th>Job</th><th>Value</th><th>Held by</th><th>Why it is not out</th></tr></thead><tbody>
        ${handHeld().map((r) => `<tr data-jkey="${esc(r.key)}">
          <td class="job-cell"><strong>${esc(r.job)}</strong><small>${esc(r.client)}</small></td>
          <td class="money">${r.value ? gbp(r.value) : "not published"}</td>
          <td>${ownerTag(r)}</td>
          <td style="max-width:420px"><div class="clamp4">${inline(jNext(r))}</div>
            ${r.caveat ? `<small class="dim">${esc(r.caveat)}</small>` : ""}</td></tr>`).join("")}
        </tbody></table></div>` : ""}

      ${(h?.corrections || []).length ? `<details class="req-detail">
        <summary>What this register had wrong, and when it stopped being wrong</summary>
        <table class="tbl" style="margin-top:10px"><thead><tr>
          <th>It said</th><th>It is</th><th>Why it happened</th></tr></thead><tbody>
        ${h.corrections.map((c) => `<tr><td>${esc(c.was)}</td><td><strong>${esc(c.now)}</strong></td>
          <td class="dim">${esc(c.why)}</td></tr>`).join("")}
        </tbody></table></details>` : ""}`;
  },

  /* Adam's Lead columns, hub-74: client, project, quote value ex VAT, quote
     issue date, current stage, owner, last meaningful contact, next action,
     next-action deadline, chase history, expected decision date and status.

     Three of those were not on the row before and each of them came off the
     Chasing page, which he has retired: the checklist STEP (his own numbering,
     8-15 are the chasing half), the LAST HEARD date, and the EXPECTED DECISION
     date - which is not a chase date and must never be sorted with them.
     Gordon Court is the case that proves it: jLiving does not decide before
     16 September, so the expected decision is known, the chase date is the
     week before it, and the two are ten weeks apart. */
  _regTable(rows) {
    return `<table class="tbl"><thead><tr>
        <th>Job and client</th><th>Value ex VAT</th><th>Quoted / last heard</th>
        <th>Stage</th><th>Status</th><th>Next action date</th>
        <th>Next action, and the chase history</th><th>Owner</th>
      </tr></thead><tbody>
      ${rows.map((r) => this._regRow(r)).join("")}
      </tbody></table>`;
  },

  _regRow(r) {
    const note = jNote(r);
    const log = jNotes(r);
    // "Expected decision" is a fact about the client's own timetable. Only
    // shown where somebody has actually written one down.
    const decides = r.blockedUntil || r.expectedDecision || "";
    return `<tr data-jkey="${esc(r.key)}">
      <td class="job-cell"><strong>${esc(r.job || "no site recorded")}</strong>
        <small>${esc(r.client || "client not named")}${
          r.contact && r.contact !== r.client ? ` &middot; ${esc(r.contact)}` : ""}</small>
        <small class="tier">${esc(TIERS[r.tier].label)}${
          r.lead ? ` ${esc(r.lead)}` : ""}${r.blocked ? " &middot; cannot answer yet" : ""}</small></td>
      <td class="money">${r.value ? gbp(r.value) : esc(r.valueText || "not published")}</td>
      <td class="num">${r.quotedOn ? esc(fdate(r.quotedOn)) : `<small class="dim">no date</small>`}
        ${r.silent === null || r.silent === undefined ? "" : `<small class="dim">${r.silent}d silent</small>`}
        ${r.lastClientContact ? `<small class="dim">last heard ${esc(fdate(r.lastClientContact))}</small>` : ""}</td>
      <td class="num">${r.stage
        ? `<strong>${r.stage}</strong><small class="dim">${esc(r.stageName || "")}</small>`
        : `<small class="dim">no step</small>`}</td>
      <td>${stateChip(r)}
        ${decides ? `<small class="dim">decision expected ${esc(fdate(decides))}</small>` : ""}</td>
      <td class="num">${dueChip(r)}</td>
      <td style="max-width:380px"><div class="clamp4">${inline(jNext(r)) || `<span class="dim">Nothing written</span>`}</div>
        ${r.blockedReason ? `<small class="dim">${esc(r.blockedReason)}</small>` : ""}
        ${r.chaseNote ? `<small class="dim">${esc(r.chaseNote)}</small>` : ""}
        ${r.decision ? `<small class="dim"><strong>${esc(r.decision.ref)} &middot; ${esc(r.decision.by)},
          ${esc(r.decision.at || "")}:</strong> &ldquo;${esc(r.decision.answer)}&rdquo;
          ${esc(r.decision.effect || "")}</small>` : ""}
        ${note ? `<span class="lognote">Last note${log.length ? ` of ${log.length}` : ""}: ${esc(note.slice(0, 180))}${note.length > 180 ? "..." : ""}</span>` : ""}
        ${log.length > 1 ? `<small class="dim">${log.slice(1, 4).map((n) =>
          `${esc(String(n.at || "").slice(0, 10))} ${esc(n.by || "")}: ${esc(String(n.text || "").slice(0, 90))}`).join(" &middot; ")}</small>` : ""}</td>
      <td>${ownerTag(r)}</td></tr>`;
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
      <!-- Adam's own checklist numbering, from the screenshot he sent on
           29/07. Steps 8-15 are the chasing half and they are this page. A
           row with no date says so rather than showing a blank cell. -->
      <td class="num">${r.stage ? `<strong>${r.stage}. ${esc(r.stageName || "")}</strong>` : `<small class="dim">no step</small>`}
        ${r.nextChase
          ? `<small class="${r.chaseDue ? "" : "dim"}">${r.chaseDue ? "due " : ""}${esc(niceDate(r.nextChase))}</small>`
          : `<small class="dim">no date set</small>`}</td>
      <td style="max-width:340px"><div class="clamp4">${inline(jNext(r))}</div>
        ${r.blockedReason ? `<small class="dim">${esc(r.blockedReason)}</small>` : ""}
        ${r.chaseNote ? `<small class="dim">${esc(r.chaseNote)}</small>` : ""}
        <!-- A human's answer to a request, on the row it was about. Grange
             Hill, 29/07: JAC-13 asked whether to clarify six open items and
             the answer was "I will chase Luke up" - which changes the owner
             and not the six. The row has to say both. -->
        ${r.decision ? `<small class="dim"><strong>${esc(r.decision.ref)} &middot; ${esc(r.decision.by)},
          ${esc(r.decision.at || "")}:</strong> &ldquo;${esc(r.decision.answer)}&rdquo;
          ${esc(r.decision.effect || "")}</small>` : ""}
        ${r.retender ? `<small class="dim">Re-tender: ${esc(r.retender.note)}</small>` : ""}
        ${r.routing ? `<small class="dim">Routing: ${esc(r.routing.note)}</small>` : ""}</td>
      <td>${ownerTag(r)}</td></tr>`;

    return `
      ${this._source(["leads", "Leads"], `Adam retired this as a working page on 29/07: the verified
        register, the checklist step, the next-chase date and the chase history are all on Leads now,
        on the same row as the AdminBase and Mary's-records tiers of the same job.`)}
      ${h ? `<div class="stats">
        <div class="stat"><div class="n">${gbpShort(t.issuedValue)}</div><div class="l">Issued and with a client - ${t.issued} quotes</div></div>
        <div class="stat ${t.due ? "red" : "green"}"><div class="n">${t.due}</div><div class="l">Chaseable today, ${gbpShort(t.dueValue)}</div></div>
        <div class="stat"><div class="n">${t.oldest}d</div><div class="l">Longest a quote has been out</div></div>
        <!-- Adam, 29/07: "When we chase a job, we need to then set a date as
             to when we will get back in touch." A quote with no next date is
             how one goes quiet without anybody noticing. -->
        <div class="stat ${t.noChaseDate ? "amber" : "green"}"><div class="n">${t.noChaseDate ?? "?"}</div><div class="l">Issued with no next-chase date set</div></div>
        <div class="stat amber"><div class="n">${gbpShort(t.heldValue)}</div><div class="l">Priced but never issued - not chaseable</div></div>
      </div>` : ""}

      <div class="section"><div class="section-head"><h3>The handover, now somebody's job</h3></div>
        <div class="planned-note">
          ${h ? `<p><strong>Adam's rule, ${esc(niceDate(h.rule?.date))}:</strong> ${esc(h.rule?.text)}
          The ${t.issued} below have gone out, so they are Jacob's. The ${t.held} under them have not,
          so they are not - and calling a client about a quote that never left the building is
          worse than not calling.</p>
          ${h.checklist ? `<p><strong>The steps are Adam's, not this board's.</strong>
          ${esc(h.checklist.why)} ${esc(h.checklist.standing_warning_from_adam)}
          <em>${esc(h.checklist.unconfirmed)}</em></p>
          <p><strong>What a chase is for.</strong> Not "any news" - these six answers, and
          whichever one comes back sets the next date:
          ${h.checklist.asks_of_a_chase.map((q) => esc(q)).join(" &middot; ")}.</p>` : ""}
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
          <th>Step / next chase</th><th>Next action</th><th>Owner</th></tr></thead><tbody>
        ${handIssued().map(hrow).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>Not issued - Mary's, and not chaseable</h3>
        <span class="page-sub">Adam, hub-77: with Mary until she says they have gone to the client</span></div>
        <table class="tbl"><thead><tr>
          <th>Job</th><th>Value</th><th>Held by</th><th>Why it is not out</th></tr></thead><tbody>
        ${handHeld().map((r) => `<tr data-jkey="${esc(r.key)}">
          <td class="job-cell"><strong>${esc(r.job)}</strong><small>${esc(r.client)}</small></td>
          <td class="money">${r.value ? gbp(r.value) : "not published"}</td>
          <td>${ownerTag(r)}</td>
          <td style="max-width:420px"><div class="clamp4">${inline(jNext(r))}</div>
            ${r.caveat ? `<small class="dim">${esc(r.caveat)}</small>` : ""}</td></tr>`).join("")}
        </tbody></table></div>

      ${(h.corrections || []).length ? `<div class="section"><div class="section-head">
        <h3>What this board had wrong, and when it stopped being wrong</h3></div>
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
          <td class="num">${esc(fdate(q.due))}${q.days > 0 && !q.unsent ? ` <small class="dim">${q.days}d ago</small>` : ""}</td>
          <td>${stateChip(q)}</td>
          <td style="max-width:320px"><div class="clamp4">${inline(jNext(q))}</div></td>
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
    const src = `${this._source(["opportunities", "Opportunities"], `The raw feed, before the award
      notices are merged onto it and before the fold that keeps a cold award out of the same table as
      a tender closing on Friday.`)}`;
    const tbl = (list, empty) => list.length ? `<table class="tbl"><thead><tr>
        <th>Closes</th><th>What it is</th><th>Buyer</th><th>Value</th>
        <th>Next action</th><th>Owner</th></tr></thead><tbody>
      ${list.map((t) => `<tr data-jkey="${esc(t.key)}">
        <td class="num"><strong>${esc(fdate(t.closes)) || "no date"}</strong>
          ${t.daysLeft !== null && t.daysLeft !== undefined
            ? `<small class="dim">${t.daysLeft}d left</small>` : ""}</td>
        <td class="job-cell"><strong>${(t.url || t.link) ? `<a href="${esc(t.url || t.link)}" target="_blank" rel="noopener">${esc(t.title)}</a>` : esc(t.title)}</strong>
          <small>${esc(t.why || t.scope || "")}${t.regions?.length ? ` &middot; ${esc(t.regions[0])}` : ""}</small>
          <!-- A hand-entered lead has to say where it came from on its face,
               or in a week nobody can tell it from a feed row. -->
          ${t.manual ? `<small class="dim">By email, not from a feed &middot; ${esc(t.ref || t.source || "")}</small>` : ""}</td>
        <td>${t.buyer ? esc(t.buyer) : `<small class="dim">not named</small>`}${t.record ? ` <span class="pill ${t.record.won ? "exact" : "strong"}">${t.record.won}W ${t.record.lost}L with us</span>` : ""}
          ${t.manual && t.buyerNote ? `<small class="dim">${esc(t.buyerNote)}</small>` : ""}</td>
        <td class="money">${gbp(t.value)}
          ${t.fit?.note ? `<small class="dim">${esc(t.fit.note)}</small>` : ""}</td>
        <td style="max-width:320px"><div class="clamp4">${inline(jNext(t))}</div></td>
        <td>${ownerTag(t)}</td></tr>`).join("")}
      </tbody></table>` : `<div class="empty"><strong>${empty}</strong></div>`;

    return `
      ${src}
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
    const a = JACOB.archive;
    const o = JACOB.outcomes;
    if (!a && !o) {
      return `<div class="planned-note">Neither the archive nor the Opportunity Log has been read yet.</div>`;
    }
    const s = o?.summary;
    const conv = o ? o.clients.filter((c) => c.decided >= 3) : [];
    const open = o?.openThisYear || [];
    /* The page is led by the ARCHIVE - what Fenster has actually won, from its
       own filing - because the BD log once shipped a false "no big wins" story
       as a headline while Headrow Court (GBP 630k) sat in the archive. The log
       survives folded at the bottom for the one thing it is good for:
       conversion rates on the CURRENT pipeline. */
    return `
      ${a ? `<div class="stats">
        <div class="stat green"><div class="n">${a.won}</div><div class="l">Jobs won on record, across ${a.distinctClients} clients</div></div>
        <div class="stat green"><div class="n">${gbpShort(a.valuedTotal)}</div><div class="l">Known won value - ${a.valuedCount} of ${a.won} jobs valued so far</div></div>
        ${a.knownValues?.length ? `<div class="stat"><div class="n">${gbpShort(a.knownValues[0].value)}</div><div class="l">Largest known win - ${esc(a.knownValues[0].job)}</div></div>` : ""}
        <div class="stat amber"><div class="n">${a.evidenceCovered}</div><div class="l">More wins with value documents indexed, awaiting reading</div></div>
        <div class="stat"><div class="n">${a.unmarked}</div><div class="l">Archive jobs with no outcome recorded either way</div></div>
      </div>

      <div class="section"><div class="section-head"><h3>Known values</h3>
        <span class="page-sub">Every number carries its source. Mining candidates get promoted only after review.</span></div>
        <table class="tbl"><thead><tr>
          <th>Job</th><th>Client</th><th>Value</th><th>Where the number comes from</th></tr></thead><tbody>
          ${a.knownValues.map((v) => `<tr>
            <td class="job-cell"><strong>${esc(v.job)}</strong>
              ${v.archiveGap ? `<small>no win recorded in the archive - the filing itself has a gap</small>` : ""}</td>
            <td>${esc(v.client)}</td>
            <td class="money">${gbp(v.value)}</td>
            <td><span class="pill ${v.basis === "document" ? "exact" : "strong"}">${esc(v.basis)}</span>
              <small class="dim">${esc(v.source)}</small></td></tr>`).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>The wins, client by client</h3>
        <span class="page-sub">From Fenster's own filing, back to 2023. The filter box finds a name.</span></div>
        <table class="tbl"><thead><tr>
          <th>Client</th><th>Wins</th><th>Known value</th><th>The jobs</th></tr></thead><tbody>
        ${a.clientsDetail.map((c) => `<tr>
          <td class="job-cell"><strong>${esc(c.client)}</strong></td>
          <td class="num">${c.won}</td>
          <td class="money">${c.value ? gbp(c.value) : `<small class="dim">not yet valued</small>`}</td>
          <td style="max-width:460px"><div class="clamp4">${c.jobs.map(esc).join(" &middot; ")}${c.won > c.jobs.length ? ` &middot; +${c.won - c.jobs.length} more` : ""}</div></td></tr>`).join("")}
        </tbody></table></div>

      <div class="section"><div class="section-head"><h3>Where the numbers come from, and what is missing</h3></div>
        <div class="planned-note">
          <p>${esc(a.note)} <strong>${a.evidenceCovered} wins</strong> already have their valuation,
          final-account or PO documents indexed (scripts/mine_won_values.py); Mary reads them into
          the table above as she works the queue - invoice amounts are interim and POs carry
          insurance lines, so a checked number beats an extracted one.</p>
          <p><strong>${a.unmarked} archive jobs carry no outcome at all</strong>, and the brochure has
          already proven the filing has gaps - Franklin House (GBP 180k, won, completed) is not in
          the archive. One click on the Scoreboard when a result lands is what stops this growing.</p>
        </div></div>` : ""}

      ${o ? `<details class="req-detail"><summary>The 2025-26 BD funnel (the Opportunity Log) - kept for one job: how the CURRENT pipeline converts</summary>
        <div class="planned-note" style="margin-top:10px">
          <p>The recent funnel, NOT the win history: its biggest win is ${gbp(s.biggestWon)} against the
          archive's ${a?.knownValues?.length ? gbp(a.knownValues[0].value) : "larger record"}. Use it to rank
          live enquiries - a GBP 20m academy is still a bad bet because the recent funnel converts small -
          and for nothing else. Win rate ${s.winRate}% over ${s.decided} decided rows; median log win
          ${gbp(s.wonMedian)}. Value filled on ${s.valueFilled} of ${o.rows} rows.</p>
        </div>
        <table class="tbl"><thead><tr><th>Job size</th><th>Won</th><th>Lost</th><th>Win rate (log-only)</th></tr></thead><tbody>
        ${o.bands.map((b) => `<tr>
          <td><strong>${esc(b.label)}</strong></td>
          <td class="num">${b.won}</td><td class="num">${b.lost}</td>
          <td class="num">${b.winRate === null ? "-" : `${Math.round(b.winRate)}%`}
            ${b.decided && !b.won ? ` <span class="pill planned">0 on log</span>` : ""}</td>
        </tr>`).join("")}
        </tbody></table>

        <div class="section" style="margin-top:18px"><div class="section-head"><h3>Clients the recent funnel converts</h3>
          <span class="page-sub">Three or more decided log outcomes</span></div>
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

        <div class="section"><div class="section-head"><h3>Why the funnel loses</h3>
          <span class="pill planned">legend ${esc(o.lostLegend?.status || "unknown")}</span></div>
          <table class="tbl"><thead><tr>
            <th>Code</th><th>Rows</th><th>Share of losses</th><th>What the notes say</th><th>Confidence</th></tr></thead><tbody>
          ${o.lostReasons.map((r) => `<tr>
            <td><strong>${esc(r.code)}</strong></td>
            <td class="num">${r.count}</td><td class="num">${r.shareOfLosses}%</td>
            <td style="max-width:420px">${esc(r.reading)}<small class="dim">${esc(r.evidence)}</small></td>
            <td><span class="chip ${r.confidence === "high" ? "ok" : r.confidence === "low" ? "danger" : "warn"}">${esc(r.confidence)}</span></td>
          </tr>`).join("")}
          </tbody></table></div>

        <div class="section"><div class="section-head"><h3>Still open on this year's sheet</h3>
          <span class="page-sub">${open.filter((r) => !r.chased).length} of ${open.length} have nothing in the Chased column</span></div>
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

        <div class="planned-note">${esc(o.source)}. Read-only, from a copy. Last read ${esc(ukStamp(o.updated))}.</div>
      </details>` : ""}`;
  },

  /* ------------------------------------------------ Opportunities
     Adam's page, hub-74. Work Jacob has found that Fenster has not yet been
     asked to price - open tenders, main contracts whose bidders still have to
     be identified, and award notices where there is still somebody worth
     ringing. One page, with the ten fields he listed on every row.

     The fold is the instruction: "Cold or weak award notices must not be
     presented as equal to genuine open tender opportunities." */
  _oppRow(r) {
    return `<tr data-jkey="${esc(r.key)}">
      <td class="job-cell"><strong>${esc(r.company || "not named")}</strong>
        ${r.record ? `<small><span class="pill ${r.record.won ? "exact" : "strong"}">${r.record.won}W ${r.record.lost}L with us</span></small>` : ""}
        ${r.confidence ? `<small><span class="pill ${r.confidence}">${esc(r.confidence)} match</span></small>` : ""}
        <small class="dim">${esc(r.sourceName)}</small></td>
      <td class="job-cell"><strong>${(r.url || r.link)
        ? `<a href="${esc(r.url || r.link)}" target="_blank" rel="noopener">${esc(r.project)}</a>`
        : esc(r.project)}</strong>
        ${r.scope ? `<small>${esc(String(r.scope).slice(0, 120))}</small>` : ""}</td>
      <td>${esc(r.location) || `<small class="dim">not stated</small>`}</td>
      <td class="money">${gbp(r.value)}
        ${r.valueNote ? `<small class="dim">${esc(r.valueNote)}</small>` : ""}</td>
      <td class="num">${r.deadline
        ? `<strong>${esc(fdate(r.deadline))}</strong>${r.daysLeft !== null && r.daysLeft !== undefined
            ? `<small class="dim">${r.daysLeft}d left</small>` : ""}`
        : r.awarded ? `<small class="dim">awarded ${esc(fdate(r.awarded))}</small>`
        : `<small class="dim">none</small>`}</td>
      <td style="max-width:260px"><small>${esc(r.relevance || "")}</small></td>
      <td style="max-width:320px"><div class="clamp4">${inline(jNext(r)) || `<span class="dim">Nothing written</span>`}</div></td>
      <td>${stateChip(r)}</td>
      <td>${ownerTag(r)}</td></tr>`;
  },

  _oppTable(rows, empty) {
    if (!rows.length) return `<div class="empty"><strong>${empty}</strong></div>`;
    return `<table class="tbl"><thead><tr>
        <th>Company or authority</th><th>Project and scope</th><th>Location</th><th>Value</th>
        <th>Deadline</th><th>Why it is relevant</th><th>Recommended next action</th>
        <th>Status</th><th>Owner</th></tr></thead><tbody>
      ${rows.map((r) => this._oppRow(r)).join("")}</tbody></table>`;
  },

  /* Customers who bought, stopped, and nobody noticed.
     Adam, hub-78, asked for decent leads. This is the list the evidence
     points at: 59% of everything Fenster has ever won came from an existing
     customer and THREE contracts in the company's history came from a tender
     portal. It is above the tender tables on purpose. */
  _dormant() {
    const d = JACOB.dormantClients;
    if (!d || !(d.clients || []).length) return "";
    // Give every row the key the hub overlay is stored under, so an owner or a
    // next action somebody types on this page actually sticks. Without it
    // jOwner/jNext fall through to the file every time and the edit vanishes.
    const rows = d.clients.map((r) => ({ ...r, key: "dormant:" + r.client }))
      .filter((r) => !jShut(r));
    if (!rows.length) return "";
    return `<div class="section"><div class="section-head">
      <h3>Customers who have stopped ringing</h3>
      <span class="page-sub">${rows.length} past buyers, nothing quoted to them right now</span></div>
      <div class="planned-note"><strong>These are the highest-converting leads Fenster has, and
      they cost a phone call.</strong> ${esc(d.why || "")}
      <br><br><em>${esc(d.caveat || "")}</em></div>
      <table class="tbl"><thead><tr><th>Client</th><th>Jobs</th><th>Lifetime</th>
        <th>Silent</th><th>Last job</th><th>Next action</th><th>Owner</th></tr></thead><tbody>
      ${rows.map((r) => `<tr data-jkey="${esc(r.key)}">
        <td class="job-cell"><strong>${esc(r.client)}</strong>
          ${r.phone ? `<small>${esc(r.phone)}</small>` : `<small class="dim">no number on file</small>`}</td>
        <td class="num">${r.jobs}</td>
        <td class="money">${gbp(r.value)}</td>
        <td class="num"><strong>${r.quietDays}d</strong>${r.wasJayks
          ? `<small class="dim">was Jayk's</small>` : ""}</td>
        <td><small>${esc((r.lastSite || "").slice(0, 44))}<br>${esc(fdate(r.lastContract))}</small></td>
        <td style="max-width:340px"><div class="clamp4">${inline(jNext(r) || r.next)}</div></td>
        <td>${ownerTag(r)}</td></tr>`).join("")}
      </tbody></table></div>`;
  },

  /* Jayk's own re-quote shortlist, emailed 19/12/2025 to adam@, commercial@,
     estimating@ and nick@, and then left behind when he did. He sold 51 of
     the 204 contracts Fenster has ever won - a quarter of the company - and
     jayk@ is a hard 404, so this is the last of his reasoning anyone can read.

     It sits on Leads rather than Opportunities because every row has already
     been priced. And it leads with SECURED: five rows record that our own
     client won the main contract, which is step two of the entire job (find
     the scheme, find who won it, get on their list) already done for us.

     The banner is not decoration. Every fact here is seven months old and the
     deadlines are all 2025 - a reader who takes a row at face value and rings
     a client about a job that finished in March has been let down by this
     panel, not by the spreadsheet. */
  _repricing() {
    const p = JACOB.repricing;
    if (!p || !(p.rows || []).length) return "";
    const rows = p.rows.map((r, i) => ({ ...r, key: "reprice:" + i }))
      .filter((r) => !jShut(r));
    if (!rows.length) return "";
    const c = p.counts || {};
    const TIER = {
      secured: ["ok", "Client WON the main contract"],
      "asked-of-us": ["warn", "They asked us for something"],
      "price-good": ["ok", "Our price was right"],
      stalled: ["navy", "Held up by someone else"],
      "no-feedback": ["", "Never answered"],
      unclassified: ["", "Notes say nothing"],
    };
    const group = (tier) => rows.filter((r) => r.tier === tier);
    const money = (list) => list.reduce((n, r) => n + (r.value || 0), 0);
    const table = (list) => `<table class="tbl"><thead><tr>
        <th>Client</th><th>Project</th><th>Quoted</th><th>Where it stood</th>
        <th>In the CRM now</th><th>Age</th></tr></thead><tbody>
      ${list.map((r) => `<tr data-jkey="${esc(r.key)}">
        <td class="job-cell"><strong>${esc(r.client)}</strong>
          ${r.crmSpellings && r.crmSpellings.length > 1
            ? `<small class="dim">CRM also spells this ${esc(r.crmSpellings.join(" / "))}</small>`
            : r.clientMatch === "none"
              ? `<small class="chip warn">not in AdminBase at all</small>` : ""}</td>
        <td style="max-width:240px"><div class="clamp4">${esc(r.project)}</div>
          ${r.responsible ? `<small class="dim">was ${esc(r.responsible)}'s</small>` : ""}</td>
        <td class="money">${r.value ? gbp(r.value) : `<small class="dim">${esc(r.valueRaw || "-")}</small>`}
          ${r.newValue ? `<small class="dim">re-priced ${gbp(r.newValue)}</small>` : ""}</td>
        <td style="max-width:360px"><div class="clamp4"><small>${esc(
          [r.chased, r.notes].filter(Boolean).join(" — ").slice(0, 320))}</small></div></td>
        <td><small>${(r.stillOpenInCrm || []).length
          ? `<span class="chip navy">still open, same figure</span>
             ${(r.stillOpenInCrm || []).map((q) => `lead ${esc(q.lead)}`).join(", ")}`
          : r.crmSince
            ? `<span class="dim">${r.crmSince} newer quote${r.crmSince === 1 ? "" : "s"}
               for this client, none for this job</span>`
            : `<span class="dim">nothing since</span>`}</small></td>
        <td class="num"><small>${r.noteAgeDays !== null && r.noteAgeDays !== undefined
          ? `${r.noteAgeDays}d` : "-"}</small></td></tr>`).join("")}
      </tbody></table>`;

    const block = (tier) => {
      const list = group(tier);
      if (!list.length) return "";
      const [chip, label] = TIER[tier] || ["", tier];
      const why = (list[0] || {}).why || "";
      return `<div class="section-head" style="margin-top:18px">
          <h4><span class="chip ${chip}">${esc(label)}</span>
          ${list.length} row${list.length === 1 ? "" : "s"}, ${gbpShort(money(list))}</h4></div>
        <div class="planned-note"><small>${esc(why)}</small></div>
        ${table(list)}`;
    };

    return `<div class="section"><div class="section-head">
      <h3>The list Jayk left behind</h3>
      <span class="page-sub">${c.rows} quotes, ${gbpShort(c.value)}, ${c.clients} clients
        - his own shortlist of what to go back to and why</span></div>
      <div class="planned-note">
        <p><strong>Read the age column before you read anything else.</strong> ${esc(p.caveat || "")}</p>
        <p>${esc(p.why || "")}</p>
        <p><strong>${esc(p.worked || "")}</strong></p>
        <p><em>${esc(p.notARequote || "")}</em></p>
      </div>
      ${["secured", "asked-of-us", "price-good", "stalled", "no-feedback",
         "unclassified"].map(block).join("")}
      ${(p.absentFromCrm || []).length ? `<div class="section-head" style="margin-top:18px">
        <h4><span class="chip warn">Invisible to the rest of this board</span>
        ${c.clientsAbsentFromCrm} clients, ${gbpShort(c.absentValue)}</h4></div>
        <div class="planned-note"><small>${esc(p.absentNote || "")}</small></div>
        <table class="tbl"><thead><tr><th>Client</th><th>Rows here</th>
          <th>Quoted</th></tr></thead><tbody>
        ${p.absentFromCrm.map((a) => `<tr><td><strong>${esc(a.client)}</strong></td>
          <td class="num">${a.rows}</td><td class="money">${gbp(a.value)}</td></tr>`).join("")}
        </tbody></table>` : ""}
      </div>`;
  },

  /* Planning applications - the only source that reaches a scheme BEFORE an
     enquiry list exists, and the free half of what Barbour ABI sells. */
  _planning() {
    const p = JACOB.planning;
    if (!p || !(p.applications || []).length) return "";
    const rows = p.applications.map((r) => ({ ...r, key: "plan:" + r.id }))
      .filter((r) => !jShut(r));
    const named = rows.filter((r) => r.applicant);
    const show = [...named, ...rows.filter((r) => !r.applicant)].slice(0, 60);
    return `<div class="section"><div class="section-head">
      <h3>Schemes at planning stage - before anyone draws up an enquiry list</h3>
      <span class="page-sub">${rows.length} in ${p.windowDays} days, ${named.length} with the applicant named</span></div>
      <div class="planned-note"><p><strong>This is where Barbour gets it.</strong> ${esc(p.why || "")}</p>
        ${(p.limits || []).map((l) => `<p>${esc(l)}</p>`).join("")}</div>
      <table class="tbl"><thead><tr><th>Applicant</th><th>Scheme</th><th>Where</th>
        <th>Size</th><th>Registered</th><th>Tier</th></tr></thead><tbody>
      ${show.map((r) => `<tr data-jkey="${esc(r.key)}">
        <td class="job-cell">${r.applicant
          ? `<strong>${esc(r.applicant)}</strong>${r.warm
              ? `<small class="chip ok">Fenster has worked for them</small>` : ""}`
          : `<span class="dim">not named</span>`}
          <small class="dim">${esc(r.applicantWhy || "")}</small></td>
        <td style="max-width:400px"><div class="clamp4">${esc(r.description.slice(0, 260))}</div>
          <small class="dim">${esc(r.address.slice(0, 60))}</small></td>
        <td><small>${esc(r.council)}<br>${esc(r.postcode || "")}</small></td>
        <td class="num">${r.dwellings ? `${esc(String(r.dwellings))} homes` : `<span class="dim">-</span>`}</td>
        <td class="num"><small>${esc(fdate(r.registered))}</small></td>
        <td><span class="chip ${r.tier === "direct" ? "ok" : "navy"}">${esc(r.tier)}</span>
          <small class="dim">${esc((r.why || "").slice(0, 44))}</small></td></tr>`).join("")}
      </tbody></table>
      ${rows.length > show.length ? `<p class="page-sub">${show.length} of ${rows.length} shown.</p>` : ""}
      </div>`;
  },

  opportunities() {
    if (!JACOB.tenders) {
      return `<div class="planned-note">The tender feed has not run yet.
        <code>python scripts/jacob_tenders.py</code></div>`;
    }
    const rows = oppRows();
    const direct = rows.filter((r) => r.oppClass === "open" && r.tier === "direct");
    const main = rows.filter((r) => r.oppClass === "open" && r.tier === "main-contract");
    const read = rows.filter((r) => r.oppClass === "read");
    const prospect = rows.filter((r) => r.oppClass === "prospect");
    const cold = rows.filter((r) => r.oppClass === "cold");
    const noAction = rows.filter((r) => r.oppClass !== "cold" && !jNext(r)).length;
    const closing = rows.filter((r) => (r.daysLeft ?? 99) <= 7 && r.oppClass === "open").length;
    const f = JACOB.tenderFeed || {};
    const t = JACOB.totals;
    return `
      <div class="stats">
        <div class="stat ${direct.length ? "green" : ""}"><div class="n">${direct.length}</div>
          <div class="l">Open now - the buyer wants glazing by name</div></div>
        <div class="stat ${closing ? "red" : ""}"><div class="n">${closing}</div>
          <div class="l">Closing inside a week</div></div>
        <div class="stat ${main.length ? "amber" : ""}"><div class="n">${main.length}</div>
          <div class="l">Main contracts - find who is bidding</div></div>
        <div class="stat ${noAction ? "red" : "green"}"><div class="n">${noAction}</div>
          <div class="l">With no next action written - these are on Today</div></div>
      </div>

      <div class="section"><div class="section-head"><h3>What is on this page</h3></div>
        <div class="planned-note">
          <p><strong>Work Fenster has not been asked to price yet.</strong> Once somebody at Fenster
          has decided to pursue it, or a price has gone out, it belongs on
          <a data-go="leads">Leads</a> and not here.</p>
          <p><strong>The two tiers below the fold are not the same thing as the two above it.</strong>
          An open tender has a closing date and an enquiry list still being drawn up. An award notice
          is published <em>after</em> the main contractor picked their subcontractors - median 25 days
          after, and 10% of them more than 180. It is a reason to make a call, not a job Fenster is
          in for, and it is folded away so it cannot be mistaken for one.</p>
        </div></div>

      ${this._dormant()}

      <div class="section"><div class="section-head"><h3>Open now - Fenster can price these itself</h3>
        <span class="page-sub">The buyer is asking for glazing work by name. Soonest closing first.</span></div>
        ${this._oppTable(direct, "Nothing open in this tier today")}</div>

      ${this._planning()}

      <div class="section"><div class="section-head"><h3>Main contracts with a glazing package in them</h3>
        <span class="page-sub">Fenster cannot bid these - the job is finding who is</span></div>
        ${this._oppTable(main, "Nothing open in this tier today")}</div>

      ${read.length ? `<details class="req-detail"><summary>${read.length} notice${read.length === 1 ? "" : "s"}
        that need reading before anyone acts - broad CPV, no glazing word, or outside England and Wales</summary>
        <div class="planned-note" style="margin-top:10px">Words lie: keyword matching has previously
        returned window <em>cleaning</em>, STI <em>screening</em>, and one contract that matched only
        on the phrase "the front door to maternity services".</div>
        ${this._oppTable(read, "None")}</details>` : ""}

      <details class="req-detail"><summary>Prospecting - ${prospect.length} compan${prospect.length === 1 ? "y" : "ies"}
        Fenster knows that have just won work (weaker: an award publishes after the enquiry list is drawn up)</summary>
        <div class="planned-note" style="margin-top:10px">A warm name beats a perfect-fit stranger
        nearly every time - in this trade a relationship buys one thing, being asked to price. But
        the signal underneath these rows is the weakest on the board, which is why they are here and
        not in the tables above. Anything marked <span class="pill possible">possible</span> waits for
        a human to confirm it once: "Atlas" matched a window-cleaning contractor.</div>
        ${this._oppTable(prospect, "Nothing warm this window")}</details>

      <details class="req-detail"><summary>Cold - ${cold.length} winners Fenster has never spoken to
        (blocked on JAC-2, nobody is assigned)</summary>
        <div class="planned-note" style="margin-top:10px">${t.cold} live building contracts whose
        winner Fenster has never spoken to. Cold approach needs <a data-go="decisions">JAC-2</a>
        answered and a separate sending domain. They are here so the moment that changes there is a
        list to work, not so anyone acts on them today.</div>
        ${this._oppTable(cold.slice(0, 60), "None")}</details>

      <div class="section"><div class="section-head"><h3>Where these come from, and how thin it really is</h3></div>
        <div class="planned-note">
          <p>Contracts Finder publishes roughly <strong>eleven</strong> tender-stage notices a day
          across every sector, against about <strong>110</strong> award notices. Over
          ${esc(f.from || "the window")} to today, ${Object.entries(f.sources || {}).map(([k, v]) =>
            `<strong>${esc(k)}</strong> returned ${v.releases ?? "?"} releases`).join(", ")}, and
          <strong>${(JACOB.tenders || []).length}</strong> of them survived the filter. The award
          side is ${t.awardRows.toLocaleString()} rows over ${JACOB.window.days} days,
          ${t.winners.toLocaleString()} unique winners, cross-referenced against ${t.clients} client
          folders in the archive (${t.clientsWon} of which actually bought).</p>
          <p>That is not a bug and it is not a small number for the wrong reason: almost nothing
          Fenster actually wins is publicly advertised, because it is a subcontractor. These feeds
          are worth running because the few they find are live, not because it is where the work is.
          The work is in the mailbox and in who is bidding - which is what
          <a data-go="decisions">JAC-3</a> is about.</p>
          <p>Everything is filtered on what a contract <em>is</em> - CPV building families - and never
          on what its title says. A notice counts only if the award is recent <em>and</em> the job is
          still running: one published 469 days late described a contract that had already finished.</p>
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
        <td>${stateChip(x)}<small class="dim">${esc(fdate(x.lastContact)) || "no email"}</small></td>
        <td style="max-width:300px"><div class="clamp4">${inline(jNext(x))}</div></td>
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

  /* What JAC-1's answer produced. Zac chose "decide later - drafts only" - his
     call, on Adam's own split of the roles (hub-68): Zac built me and owns what
     I am allowed to do, Adam owns the pipeline. So
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

      <!-- JAC-4, Zac, 29/07: "Either". Two approvers is why this queue is on the
           hub rather than in somebody's inbox, so the page has to say who can
           clear a row - and has to say the three things "either" does NOT mean,
           because none of them are visible in the word. -->
      ${d.approvalRoute ? `<div class="section"><div class="section-head">
        <h3>Who can clear a row</h3>
        <span class="pill strong">${esc(d.approvalRoute.ref)}</span>
        <span class="page-sub">${esc(d.approvalRoute.approvers.join(" or "))} &mdash;
          either of them, whichever opens this first</span></div>
        <div class="planned-note">
          <p><strong>${esc(d.approvalRoute.question)}</strong> &mdash;
          ${esc(d.approvalRoute.by)}, ${esc(niceDate(d.approvalRoute.date))}:
          <em>&ldquo;${esc(d.approvalRoute.answer)}&rdquo;</em></p>
          <p>${esc(d.approvalRoute.where)}</p>
          <p>${esc(d.approvalRoute.senderIsSeparate)}</p>
          <p><strong>${esc(d.approvalRoute.notASendPath)}</strong></p>
        </div></div>` : ""}

      <div class="section"><div class="section-head"><h3>The rules these were written under</h3></div>
        <ul class="plain">${d.rules.map((r) => `<li>${esc(r)}</li>`).join("")}</ul></div>

      <!-- A draft that was wrong and got caught is worth more on the page than
           off it. It is the only evidence that the rule about where a figure
           came from is doing anything. -->
      ${(d.corrections || []).length ? `<div class="section"><div class="section-head">
        <h3>Withdrawn before anybody sent it</h3></div>
        <table class="tbl"><thead><tr><th>Draft</th><th>It said</th><th>It is</th>
          <th>Why it happened</th></tr></thead><tbody>
        ${d.corrections.map((c) => `<tr>
          <td><strong>${esc(c.draft)}</strong><small class="dim">${esc(niceDate(c.date))}</small></td>
          <td>${esc(c.was)}</td>
          <td><strong>${esc(c.now)}</strong></td>
          <td class="dim">${esc(c.why)}${c.cost_if_sent
            ? `<small class="dim">Cost if it had gone: ${esc(c.cost_if_sent)}</small>` : ""}</td>
        </tr>`).join("")}
        </tbody></table></div>` : ""}

      ${rows.map((r) => `<div class="section" data-jkey="draft:${esc(r.id)}">
        <div class="section-head">
          <h3>${esc(r.job)}</h3>
          <span class="pill strong">${esc(r.id)}</span>
          <span class="page-sub">${esc(r.client)}${r.value
            ? ` &middot; ${gbp(r.value)}` : ""} &middot; send as <strong>${esc(r.send_as)}</strong></span>
        </div>
        <div class="planned-note">
          ${r.purpose ? `<p><strong>Purpose:</strong> ${esc(r.purpose)}</p>` : ""}
          <p><strong>Why now:</strong> ${esc(r.why_now)}</p></div>
        <table class="tbl"><tbody>
          <tr><td style="width:150px" class="dim">Linked client</td><td><strong>${esc(r.client)}</strong></td></tr>
          <tr><td class="dim">Linked project</td><td>${esc(r.job)}${r.value ? ` &middot; ${gbp(r.value)}` : ""}</td></tr>
          <tr><td class="dim">Intended recipient</td>
            <td><strong>${esc(r.to)}</strong>${r.to_name
              ? `<small class="dim">${esc(r.to_name)}${r.to_caveat
                  ? ` &mdash; ${esc(r.to_caveat)}` : ""}</small>` : ""}</td></tr>
          ${r.cc ? `<tr><td class="dim">Cc</td><td>${esc(r.cc)}</td></tr>` : ""}
          <tr><td class="dim">Intended sender</td><td><strong>${esc(r.send_as)}</strong>
            <small class="dim">from their own mailbox, under their own name</small></td></tr>
          <tr><td class="dim">Subject</td><td><strong>${esc(r.subject)}</strong></td></tr>
        </tbody></table>
        <pre class="draft-body">${esc(r.body)}</pre>
        <table class="tbl"><tbody>
          <tr><td style="width:150px" class="dim">Evidence used</td><td>${esc(r.evidence)}</td></tr>
          <tr><td class="dim">Figures</td><td>${esc(r.value_source)}</td></tr>
          <tr><td class="dim">Wording to avoid</td><td>${esc(r.must_not_say)}</td></tr>
          ${r.blocked_on ? `<tr><td class="dim">Open</td><td>${esc(r.blocked_on)}</td></tr>` : ""}
          <tr><td class="dim">Approval status</td><td><span class="chip ${r.approvedBy
            ? "ok" : "warn"}">${esc(r.approval || r.status)}</span>
            ${r.approvedBy ? `<small class="dim">Approved by
              <strong>${esc(r.approvedBy)}</strong>${r.approvedAt
                ? ` on ${esc(niceDate(r.approvedAt))}` : ""} &mdash; wording cleared.
              ${esc(r.send_as)} still sends it.</small>` : ""}
            <small class="dim">Jacob does not send these. A named human reads it, changes what they want and sends it.</small></td></tr>
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
    /* Adam, hub-74: "The raw AdminBase Chase List may remain under System or
       Data for audit purposes, but it must only act as a source feeding
       Leads." So the rows are here whole, and nothing on this page is a thing
       to do. The chaseable ones are on Leads, on one clock with everything
       else Fenster has priced. */
    /* The CRM's own key on these rows is the client's email domain, which is
       right for grouping and wrong for the overlay - twelve Bradford Watts
       rows would all share one human correction. The board key is per lead. */
    /* An outlier stays out of the arithmetic but comes back into the chase
       list the moment a human confirms it is real - Adam did that for Brandon
       Estate on 29/07. Big is not the same as wrong. */
    const due = c.due
      .map((r) => ({ ...r, key: "ab:" + r.lead }))
      .filter((r) => (!r.outlier || r.confirmed) && !jShut(r))
      .slice(0, 60);
    return `
      ${this._source(["leads", "Leads"], `The whole CRM export is here for audit. ${t.due} of these
        ${t.rows} rows feed Leads; the rest are being priced, already on the verified register, or
        held out of the totals as outliers.`)}
      <div class="stats">
        <div class="stat"><div class="n">${t.rows}</div><div class="l">Quoted leads in the CRM, ${t.clients} clients</div></div>
        <div class="stat red"><div class="n">${t.due}</div><div class="l">Nobody has been back to, ${gbpShort(t.dueValue)}</div></div>
        <div class="stat amber"><div class="n">${t.yearSilent}</div><div class="l">Silent for over a year and still open</div></div>
        <div class="stat ${t.winnable ? "green" : "amber"}"><div class="n">${gbpShort(t.winnableValue)}</div><div class="l">Of that, in a band the BD log converts in - ${t.winnable} jobs</div></div>
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
          <!-- JAC-14, answered by ADAM 29/07 - it went on the record as Zac
               because the sidebar defaulted to him, and Adam corrected it in
               hub-66. It matters here: this is the Commercial Director telling
               me not to close his backlog, not the operator. I asked for a rule
               that CLOSED it and got the opposite, which is the right answer: a
               row I close on my own arithmetic is a job nobody ever rings again. -->
          <p><strong>Nothing here gets closed on silence.</strong> Adam, 29/07, answering
          JAC-14: <em>&ldquo;They all need chasing up, and a final word from the client which is
          also a good opportunity to get any feedback and tout more opportunities. Treat all as
          live until updated.&rdquo;</em> So every chaseable row now carries the same three-part
          ask instead of an empty cell - is it live or gone and to whom, how our price looked,
          and what else they have coming. The four rows that join a verified send are the
          exception: those keep the next action written for them on the register, because two
          of the four say do not chase.</p>
          <p><strong>And the size does not match what the recent funnel converts.</strong> The
          Opportunity Log's decided rows (2025-26) say: under GBP 10k it wins 38% of the time,
          GBP 10k-50k 13%, and above GBP 50,000 no win on the log - 52 priced, 52 lost; median
          log win GBP 1,822. The log is not the whole win history (Headrow Court, GBP 50k+,
          completed, never entered it) - but as a guide to how THIS list will convert, it stands.</p>
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

      ${(c.sameSite || []).length ? `<div class="section"><div class="section-head">
        <h3>One site, the same client quoted twice</h3>
        <span class="page-sub">up to ${gbpShort(t.sameSiteAtRisk)} counted more than once -
        and invisible to the panel above, which needs two different clients</span></div>
        <div class="planned-note"><p>The multi-bidder check finds the same job priced for
        different main contractors on the penny-exact figure. It cannot see a job the
        <strong>same</strong> client asked us to price twice, because it requires two customer
        keys and a job priced twice is priced at two different numbers. This panel is that blind
        spot. <strong>Nothing here is merged or closed</strong> - two quotes at one address can
        be two options for one job or two genuine packages, and the <em>product</em> column is
        usually the tell: aluminium against uPVC at one address reads as a choice, aluminium
        against secondary glazing reads as two packages. Somebody who knows the job settles it;
        this list only makes sure the question gets asked.</p></div>
        <table class="tbl"><thead><tr><th>Site</th><th>Rows</th><th>On the board</th><th>Counted twice, at most</th></tr></thead><tbody>
        ${c.sameSite.map((s) => `<tr>
          <td class="job-cell"><strong>${esc(s.job)}</strong><small>${esc(s.client)} &middot;
            ${esc(s.postcode)} &middot; matched on ${s.shared.map(esc).join(", ")}</small></td>
          <td>${s.rows.map((r) => `<small>${esc(r.lead)} &middot; ${gbp(r.value)} &middot;
            ${esc(r.product || "product not stated")}${r.worked ? " &middot; researched" : ""}
            &middot; ${esc(niceDate(r.leadDate))}</small>`).join("<br>")}</td>
          <td class="money">${gbp(s.total)}</td>
          <td class="money">${gbp(s.atRisk)}</td>
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
        <h3>Held out of every total on this page</h3>
        <span class="page-sub">Out of the averages because of their size, not because anyone
        doubts them. A confirmed row is still on the chase list.</span></div>
        <table class="tbl"><thead><tr><th>Job</th><th>Quoted ex VAT</th><th>Why it is not counted</th></tr></thead><tbody>
        ${c.rows.filter((r) => r.outlier).map((r) => `<tr>
          <td class="job-cell"><strong>${esc(r.job)}</strong><small>${esc(r.client)} &middot; ${esc(niceDate(r.leadDate))}</small></td>
          <td class="money">${gbp(r.value)}</td>
          <td>Large enough to move the pipeline figure on its own, so it is kept out of the
            medians and the totals.
            ${r.confirmed ? `<small class="dim"><strong>Confirmed real.</strong>
              ${esc(r.confirmed)} It is on the chase list.</small>`
            : `<small class="dim">Nobody has confirmed it yet - a question for Adam before
              it is a number.</small>`}</td></tr>`).join("")}
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
          <!-- On a re-quote AdminBase updates the value and leaves the dates,
               so the row can read months old on a price sent yesterday. Where
               a verified send says otherwise, the send's date is shown. -->
          <td class="num">${r.staleDate ? `${esc(niceDate(r.staleDate.issued))}
            <small class="dim">CRM says ${esc(niceDate(r.staleDate.crmDate))}${r.staleDate.reQuote ? " - re-quote" : ""}</small>`
            : r.leadDate ? esc(niceDate(r.leadDate)) : "-"}</td>
          <td class="num">${r.days === null ? "-" : `${r.days}d`}
            ${r.staleDate ? `<small class="dim">not ${r.staleDate.crmDays}d</small>` : ""}</td>
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
      "When Jacob picks up a message or a lead, every step he takes appears here as it happens.",
      JQUEUE?.last_kick, "jqueue");
  },
  jqueue() { return queuePage(JQUEUE); },

  decisions() {
    return decisionsSection("jacob", openJacobReqs(),
                            JREQS.filter((r) => r.status === "answered")) + `

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
      : "When Mary picks up a job, everything she does appears here as it happens.",
      MQUEUE?.last_kick, "queue");
  },
  queue() { return queuePage(MQUEUE); },
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
        ${JACOB ? `<div class="stat ${JACOB.totals.handoverDue ? "red" : ""}" data-bot-go="jacob:leads"><div class="n">${JACOB.totals.handoverDue ?? 0}</div><div class="l">Quotes chaseable today</div></div>` : ""}
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
/* "what is it even doing" - Zac, 04/08. Fair question: his page showed four
   zeroes and a note saying it was a placeholder, which answers nothing. Every
   CRM write lands a crm_event with an author, so this is what he has actually
   changed, straight off the audit trail. If it is empty it says which of the
   two reasons that is, because "no events" and "never ran" are different
   things and only one of them is a problem. */
function josephActivity() {
  const s = JOSTATUS || {};
  const now = `<div class="planned-note"><p><strong>Right now:</strong>
    ${esc(bridgeStatus(s).text)}${s.thought ? ` - ${esc(s.thought)}` : ""}</p></div>`;
  const ev = JOEVENTS || [];
  if (!ev.length) {
    return now + `<div class="empty">
      <strong>${s.updated ? "He has not changed anything in the CRM yet."
                          : "He has never run."}</strong>
      <p>${s.updated ? "He has run, but every pass so far ended without a record-level change - that is normal on a day with no site dates set."
                     : "Nothing has started his bridge, so there is nothing to show."}</p></div>`;
  }
  return now + `<div class="tbl-wrap"><table class="tbl crm-tbl">
    <thead><tr><th>When</th><th>Job</th><th>Changed</th><th>Why</th></tr></thead>
    <tbody>${ev.slice(0, 25).map((e) => `<tr>
      <td class="nowrap dim">${esc(fdWhen(e.created))}</td>
      <td class="crm-title"><span>${esc(e.entity_key || "")}</span></td>
      <td class="crm-title"><span><strong>${esc(e.field || "")}</strong>
        ${e.was ? `<small class="dim">was ${esc(String(e.was).slice(0, 60))}</small>` : ""}
        ${e.now ? `<small class="dim">now ${esc(String(e.now).slice(0, 60))}</small>` : ""}</span></td>
      <td class="crm-title"><span class="dim">${esc(e.why || "-")}</span></td>
    </tr>`).join("")}</tbody></table></div>`;
}

function josephStatus() {
  if (JOSTATUS && JOSTATUS.state && JOSTATUS.state !== "unknown") return bridgeStatus(JOSTATUS);
  /* No bridge has ever run for him yet, and saying "Live" when nothing is
     listening would be the same lie the pause-verification told. */
  return { text: "Not started", tone: "off", title: "His bridge has not been run yet" };
}

function jacobStatus() {
  if (JSTATUS && JSTATUS.state && JSTATUS.state !== "unknown") return bridgeStatus(JSTATUS);
  // His bridge reports a status line now, so this only runs before he has ever
  // started. Fall back to the live feed: steps inside the last ten minutes
  // mean a session is running.
  const age = JACTIVITY?.updated ? Date.now() - new Date(JACTIVITY.updated).getTime() : Infinity;
  if (age < 600000) return { text: "Working", tone: "busy", title: JACTIVITY?.title || "" };
  /* NOT "Live". Nothing here is evidence a bridge is running - it is the
     absence of evidence, which is the state the pause leaves behind and the
     one a person most needs told. */
  return { text: "Not running", tone: "off",
           title: "No status and no recent activity - his bridge is not up" };
}

/* ---------------- THE CRM ----------------
   One record of the commercial world, shared by all three bots and read
   straight from /api/crm/* rather than from a deployed board file. That is
   the difference between this and the pages above: Mary's and Jacob's boards
   are snapshots their generators build, so they are only as fresh as the last
   deploy. This is live - a chase date Adam moves by email is on this page the
   moment the CRM has it.

   Two audiences, deliberately separated (Zac, 03/08): admin is Adam and Zac,
   and the Delivery page is what Paul and Steve get - their day, nothing else
   to learn. */
let CRM = { today: null, leads: [], companies: [], contracts: [], delivery: null };

const crmLead = (key) => CRM.leads.find((l) => l.key === key);
const crmCo = (key) => CRM.companies.find((c) => c.key === key);
/* Our own stages in the words a person would use out loud. */
/* The handover is at quote_sent: everything before it is estimating's,
   everything after is business development's. Kept in step with STAGES in
   scripts/crm.py - if one moves, move both. */
const MARY_STAGES = ["new", "acknowledged", "materials_out", "awaiting_costs",
                     "quote_ready", "pre_quote_call"];
const STAGE_LABEL = {
  new: "New", acknowledged: "Acknowledged", materials_out: "Out to suppliers",
  awaiting_costs: "Awaiting costs", quote_ready: "Quote to check",
  pre_quote_call: "Pre-quote call", quote_sent: "Quoted",
  follow_up: "Chasing", final_follow_up: "Final chase", closed: "Closed",
};
/* The stylesheet defines ok / warn / danger / navy and nothing else - inventing
   a tone name here just renders an unstyled chip. */
const stageTone = (s) => (s === "closed" ? "navy"
  : ["quote_sent", "follow_up", "final_follow_up"].includes(s) ? "warn" : "ok");

function crmDays(d) {
  if (!d) return null;
  return Math.round((new Date(d) - new Date(new Date().toISOString().slice(0, 10))) / 864e5);
}

/* WHAT THE DATA ACTUALLY LOOKS LIKE, measured 03/08/2026, because the pages
   below are shaped by it rather than by what a CRM usually shows:

     272 live leads. 184 carry a date and 173 OF THOSE ARE LATE - 112 of them
     by more than three months. Five are in the future. So this is not a
     pipeline with a bit of slippage, it is eleven live conversations and a
     graveyard, and a page that lists them together buries the eleven.

     Nothing has a deadline or an award date. Zero of each. Any view built on
     "closing this week" would render empty forever.

     Every lead is owned by "jacob", so owner is not a filter, it is a constant.

     26 leads hold GBP 17.7m of the GBP 25.9m, and one of them is GBP 7.2m.
     A headline total is that one job plus noise; the median is GBP 21,837.

     80 companies have actually bought, GBP 2.8m between them, and the top ten
     are 86% of it. FIFTY-FOUR of those eighty have nothing live right now,
     while 147 live quotes sit with companies that have never bought anything.
     Against a 59% of wins coming from existing customers, that is the single
     most useful thing in the database. */
const QUIET_DAYS = 90;

/* Which tab is showing and how it is sorted. Held outside render() because
   render() throws the page away and rebuilds it on every background refresh -
   the same reason drafts and the caret are held. */
const CRMV = {
  leadFilter: "live", leadSort: { col: "next_action_date", dir: 1 },
  coFilter: "customers", coSort: { col: "lifetime_value", dir: -1 },
  conFilter: "live", conSort: { col: "site_date", dir: 1 },
  fdFilter: "all",
};

const CRM_FILTERS = {
  lead: {
    all: () => true,
    live: (l) => !l.outcome && isLive(l),
    quiet: (l) => !l.outcome && isQuiet(l),
    pricing: (l) => !l.outcome && MARY_STAGES.includes(l.stage),
    undated: (l) => !l.outcome && leadAge(l) === null,
    flagged: (l) => !l.outcome && flagged(l),
    closed: (l) => !!l.outcome,
  },
  co: {
    all: () => true,
    customers: (c) => c.relationship === "won",
    dormant: (c) => c.relationship === "won" && !crmHasLive(c.key),
    active: (c) => crmHasLive(c.key),
    never: (c) => c.relationship !== "won",
  },
  con: {
    all: () => true,
    live: (c) => c.status === "live",
    complete: (c) => c.status !== "live",
  },
};

function crmHasLive(key) {
  return CRM.leads.some((l) => !l.outcome && l.company_key === key);
}

/* WHERE THE RECORD ARGUES WITH ITSELF.
   The chase DATE was seeded from AdminBase's next-action column; the chase
   TEXT is Jacob's own reading of the mailboxes. Nothing ever checked the two
   agree, and on 14 leads holding GBP 3.0m they do not - The Hub Alkerden reads
   503 days overdue while its own note says Sinden asked us for an updated
   quotation in July 2026 and explicitly says DO NOT ask them if it is live.

   These are FLAGGED, not corrected. A regex over prose is decent evidence that
   two fields disagree and poor evidence about which one is right, and silently
   rewriting a commercial date on that basis is how a CRM starts lying
   confidently. A human or the Overseer decides; this just refuses to let it
   hide. */
const DATE_IN_TEXT = /\b(\d{1,2})\/(\d{1,2})\/(20\d{2})\b/g;
const DO_NOT_CHASE = /\bdo not (ask|chase|contact|approach)\b/i;

function leadFlags(l) {
  const out = [];
  const txt = l.next_action || "";
  if (DO_NOT_CHASE.test(txt)) out.push({ k: "hold", label: "Do not chase",
    why: "This lead's own note says not to approach them." });
  const nad = l.next_action_date;
  if (nad && txt) {
    let newest = null, m;
    DATE_IN_TEXT.lastIndex = 0;
    while ((m = DATE_IN_TEXT.exec(txt))) {
      const d = `${m[3]}-${String(+m[2]).padStart(2, "0")}-${String(+m[1]).padStart(2, "0")}`;
      if (!newest || d > newest) newest = d;
    }
    if (newest && newest > nad) {
      out.push({ k: "stale", label: "Date looks wrong",
        why: `The chase date is ${nad}, but the note refers to ${newest}. The date came from AdminBase and the note from the mailboxes; they were never reconciled.` });
    }
  }
  return out;
}
const flagged = (l) => leadFlags(l).length > 0;

/* Sort keys that are not columns on the row itself. */
const CRM_SORTVAL = {
  company: (r) => ((crmCo(r.company_key) || {}).name || r.company_key || "").toLowerCase(),
  openval: (r) => money(CRM.leads.filter((l) => !l.outcome && l.company_key === r.key)).total,
};

function crmFilterSort(list, filterKey, sort) {
  const family = list === CRM.companies ? "co" : list === CRM.contracts ? "con" : "lead";
  const test = CRM_FILTERS[family][filterKey] || (() => true);
  const out = list.filter(test);
  const get = (r) => {
    const v = CRM_SORTVAL[sort.col] ? CRM_SORTVAL[sort.col](r) : r[sort.col];
    return v === null || v === undefined || v === "" ? null : v;
  };
  out.sort((a, b) => {
    const x = get(a), y = get(b);
    /* Blanks always sink, whichever way the column is pointing - a row with no
       date is not "earliest", it is unset, and floating them to the top of an
       ascending sort buries everything real. */
    if (x === null && y === null) return 0;
    if (x === null) return 1;
    if (y === null) return -1;
    if (typeof x === "number" && typeof y === "number") return (x - y) * sort.dir;
    return String(x).localeCompare(String(y)) * sort.dir;
  });
  return out;
}

/* ---------------- a decision, whoever raised it ----------------
   Jacob's card carried the note "a decision is a decision whichever bot
   raised it, and two designs for one concept is how the hub got chaotic in
   the first place" - and then Joseph got a third design anyway: a title, the
   reason, and nothing to answer with. Zac, 04/08: "joseph needs the same
   format as the others with messages and the needs you bit. cos you cant
   reply to it."

   So it is one component now and both call it. Buttons first with the essay
   folded; an option SELECTS rather than sends, because a button that posts on
   first touch turns a mis-click into an instruction. */
function decisionCard(bot, r) {
  let opts = [];
  try { opts = JSON.parse(r.options || "[]"); } catch { opts = []; }
  return `<article class="req" data-req="${esc(r.ref)}">
    <div class="req-top"><div><h3>${esc(r.title)}</h3>
      <div class="meta">${esc(r.ref)} &middot; raised ${esc(ukShortDay(r.created))} &middot; he carries on with everything this does not block</div></div>
    <span class="chip warn">waiting</span></div>
    <div class="req-answer">
      ${opts.length ? `<div class="req-options">${opts.map((o) => `<button class="opt">${esc(o)}</button>`).join("")}</div>` : ""}
      <div class="req-compose"><textarea data-draft="${bot}req-${esc(r.ref)}" placeholder="Your answer (or pick an option above and add the reason - he acts on the why)..."></textarea>
      <button class="btn" data-reqsend="${bot}:${esc(r.ref)}">Answer</button></div>
    </div>
    ${reqDetail("What he needs from you", r.needs, 400)}
    ${reqDetail("Why he is blocked", r.why, 0)}
  </article>`;
}

function decisionsSection(bot, open, answered) {
  return `
    ${open.length ? `<div class="req-grid">${open.map((r) => decisionCard(bot, r)).join("")}</div>` : ""}
    ${answered.length ? `<div class="section" style="margin-top:26px"><div class="section-head"><h3>Resolved</h3></div>
      <div class="req-grid">${answered.map((r) => `<article class="req resolved">
        <div class="req-top"><div><h3>${esc(r.title)}</h3>
          <div class="meta">${esc(r.ref)} &middot; answered ${esc(ukShortDay(r.answered_at))} by ${esc(r.answered_by || "team")}</div></div>
        <span class="chip ok">resolved</span></div>
        <div class="answered"><h5>The answer</h5>${fmt(r.answer || "")}</div>
      </article>`).join("")}</div></div>` : ""}`;
}

const crmTabs = (fam, tabs, current) => `<div class="crm-tabs">${tabs.map(([k, label, n]) =>
  `<button class="crm-tab${k === current ? " on" : ""}" data-crmtab="${fam}:${k}" type="button">
    ${esc(label)}<span>${n}</span></button>`).join("")}</div>`;

const crmTh = (fam, col, label, num) => {
  const s = CRMV[fam + "Sort"];
  const on = s.col === col;
  return `<th class="${num ? "num " : ""}sortable${on ? " sorted" : ""}"
    data-crmsort="${fam}:${col}">${esc(label)}${on ? (s.dir === 1 ? " &uarr;" : " &darr;") : ""}</th>`;
};

const crmCount = (n, total, one, many) =>
  `<p class="crm-count">${n} ${n === 1 ? one : (many || one + "s")}${
    n < total ? ` of ${total}` : ""}</p>`;

function leadAge(l) {
  return crmDays(l.next_action_date);
}
const isLive = (l) => { const n = leadAge(l); return n !== null && n >= -28; };
const isQuiet = (l) => { const n = leadAge(l); return n !== null && n < -QUIET_DAYS; };
const isSlipping = (l) => { const n = leadAge(l); return n !== null && n < -28 && n >= -QUIET_DAYS; };

/* A total dominated by one GBP 7.2m row is not a summary of anything. */
function money(list) {
  const v = list.map((l) => l.value || 0).filter(Boolean).sort((a, b) => a - b);
  if (!v.length) return { n: 0, total: 0, median: 0, top: 0 };
  return { n: v.length, total: v.reduce((s, x) => s + x, 0),
           median: v[Math.floor(v.length / 2)], top: v[v.length - 1] };
}

/* A date with its lateness said in words. "2026-06-22" tells you nothing at a
   glance; "6 weeks late" is the whole point of the row. */
function whenChip(d) {
  const n = crmDays(d);
  if (n === null) return "";
  const late = n < 0;
  const abs = Math.abs(n);
  const t = abs === 0 ? "today" : abs < 14 ? `${abs} day${abs === 1 ? "" : "s"}`
    : abs < 90 ? `${Math.round(abs / 7)} weeks` : `${Math.round(abs / 30)} months`;
  return `<span class="chip ${late ? "danger" : n === 0 ? "warn" : "navy"}">${
    abs === 0 ? "due today" : late ? `${t} late` : `in ${t}`}</span>`;
}

/* The same row shape the record lists use, so a job looks identical wherever
   it appears. Today used to build its own and came out at 226px a row against
   64 on Leads - the same data, twice as tall, on the page most likely to be
   read in a hurry. */
function crmRows(list, empty) {
  if (!list.length) return `<div class="empty"><strong>${empty}</strong></div>`;
  return `<table class="tbl crm-tbl"><thead><tr>
      <th>Job</th><th>Client</th><th>Stage</th><th class="num">Value</th>
      <th>Next action</th><th>Due</th></tr></thead><tbody>
    ${list.map((l) => `<tr data-crm="${esc(l.key)}">
      <td class="crm-title"><span><strong>${esc(l.title || l.key)}</strong></span></td>
      <td class="crm-title"><span>${esc((crmCo(l.company_key) || {}).name || l.company_key)}</span></td>
      <td><span class="chip ${stageTone(l.stage)}">${esc(STAGE_LABEL[l.stage] || l.stage)}</span></td>
      <td class="num">${l.value ? gbp(l.value) : "-"}</td>
      <td class="crm-next"><span>${esc((l.next_action || "").slice(0, 160)) || "<em>nothing set</em>"}</span></td>
      <td class="nowrap">${whenChip(l.next_action_date || l.award_due)}
        ${leadFlags(l).map((f) => `<span class="chip danger" title="${esc(f.why)}">${esc(f.label)}</span>`).join("")}</td>
    </tr>`).join("")}</tbody></table>`;
}

/* A record you can CHANGE, which is the whole difference between a CRM and a
   report. Save writes through /api/crm/edit, which whitelists the columns a
   person may touch and logs every one to crm_event, so a human moving a chase
   date is as traceable as a bot doing it. */
async function crmSave(type, key, fields, why) {
  const r = await api("crm/edit", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ type, key, fields, why, author: who() }),
  });
  if (!r || r.error) throw new Error((r && r.error) || "save failed");
  return r;
}

function crmField(id, label, value, opts) {
  if (opts) {
    return `<label class="crm-f"><span>${esc(label)}</span>
      <select id="${id}">${opts.map((o) =>
        `<option value="${esc(o[0])}"${o[0] === (value || "") ? " selected" : ""}>${esc(o[1])}</option>`
      ).join("")}</select></label>`;
  }
  return `<label class="crm-f"><span>${esc(label)}</span>
    <input id="${id}" value="${esc(value || "")}"></label>`;
}

/* A company record: who they are, what they have paid, every job we have
   quoted them, and the people we deal with. */
async function crmPanelCompany(key) {
  openPanel(`<h2>Loading...</h2>`);
  let d;
  try { d = await api("crm/company/" + encodeURIComponent(key)); }
  catch { toast("Could not load that company"); closePanel(); return; }
  if (!d || d.error) { toast("No such company"); closePanel(); return; }
  const C = d.company;
  const leads = (d.leads || []);
  const live = leads.filter((l) => !l.outcome);
  openPanel(`
    <h2>${esc(C.name)}</h2>
    <p class="sub">${esc(C.relationship)}${C.postcode ? " &middot; " + esc(C.postcode) : ""}</p>
    <div class="stats">
      <div class="stat"><div class="n">${C.lifetime_value ? gbpShort(C.lifetime_value) : "-"}</div>
        <div class="l">They have paid us</div></div>
      <div class="stat"><div class="n">${live.length}</div>
        <div class="l">Live quotes</div></div>
      <div class="stat"><div class="n">${gbpShort(money(live).total)}</div>
        <div class="l">Out with them</div></div>
    </div>
    <div class="panel-sec"><h4>Edit</h4>
      <div class="crm-form">
        ${crmField("cy-name", "Name", C.name)}
        ${crmField("cy-rel", "Relationship", C.relationship,
          [["won", "has bought"], ["quoted", "quoted only"], ["known", "known"],
           ["cold", "cold"], ["unknown", "unknown"]])}
        ${crmField("cy-terms", "Payment terms", C.payment_terms)}
        ${crmField("cy-pc", "Postcode", C.postcode)}
      </div>
      <div class="crm-actions">
        <button id="cy-save" class="btn-primary" type="button">Save</button>
        <span id="cy-msg" class="crm-msg"></span>
      </div>
    </div>
    <div class="panel-sec"><h4>Who we deal with</h4>
      ${(d.contacts || []).length ? `<ul class="unk">${d.contacts.map((c) => {
        const named = (c.name || "").trim();
        return `<li>${esc(named || c.email)}${c.role ? " - " + esc(c.role) : ""}
          ${named && c.email ? `<br><small>${esc(c.email)}</small>` : ""}
          ${c.phone ? `<br><small>${esc(c.phone)}</small>` : ""}</li>`;
      }).join("")}</ul>` : `<p class="page-sub">No contacts on record.</p>`}
    </div>
    <div class="panel-sec"><h4>Their jobs <span class="chip navy">${leads.length}</span></h4>
      ${leads.length ? `<table class="tbl crm-tbl"><thead><tr>
          <th>Job</th><th class="num">Value</th><th>Stage</th></tr></thead><tbody>
        ${leads.map((l) => `<tr data-crm="${esc(l.key)}">
          <td class="crm-title"><span>${esc(l.title || l.key)}</span></td>
          <td class="num">${l.value ? gbp(l.value) : "-"}</td>
          <td><span class="chip ${stageTone(l.stage)}">${esc(STAGE_LABEL[l.stage] || l.stage)}</span></td>
        </tr>`).join("")}</tbody></table>`
        : `<p class="page-sub">Nothing quoted to them yet.</p>`}
    </div>`);
  $("#cy-save")?.addEventListener("click", async () => {
    const el = $("#cy-msg");
    el.textContent = "Saving...";
    try {
      const fields = { name: $("#cy-name").value.trim(), relationship: $("#cy-rel").value,
                       payment_terms: $("#cy-terms").value.trim(), postcode: $("#cy-pc").value.trim() };
      await crmSave("company", key, fields, "edited on the hub");
      Object.assign(crmCo(key) || {}, fields);
      el.textContent = "Saved";
      render();
    } catch { el.textContent = "Could not save"; }
  });
}

/* A won job: the twelve steps, tickable, and the site date everything counts
   backwards from. Setting that date is the single edit that turns the whole
   contracts page on. */
async function crmPanelContract(key) {
  openPanel(`<h2>Loading...</h2>`);
  let d;
  try { d = await api("crm/contract/" + encodeURIComponent(key)); }
  catch { toast("Could not load that contract"); closePanel(); return; }
  if (!d || d.error) { toast("No such contract"); closePanel(); return; }
  const C = d.contract, co = d.company || {};
  const tasks = (d.tasks || []);
  openPanel(`
    <h2>${esc(C.title || C.key)}</h2>
    <p class="sub">${esc(co.name || C.company_key)}</p>
    <div class="panel-sec"><h4>Edit</h4>
      <div class="crm-form">
        ${crmField("cc-site", "On site", C.site_date)}
        ${crmField("cc-value", "Value, ex VAT", C.value || "")}
        ${crmField("cc-po", "PO reference", C.po_ref)}
        ${crmField("cc-status", "Status", C.status,
          [["live", "live"], ["complete", "complete"], ["invoiced", "invoiced"], ["paid", "paid"]])}
      </div>
      <div class="crm-actions">
        <button id="cc-save" class="btn-primary" type="button">Save</button>
        <span id="cc-msg" class="crm-msg">${C.site_date ? ""
          : "No site date - the twelve steps have no dates until one is set."}</span>
      </div>
    </div>
    <div class="panel-sec"><h4>The twelve steps</h4>
      ${tasks.length ? `<ul class="crm-steps">${tasks.map((t) => `
        <li class="${t.done_at ? "done" : ""}">
          <strong>${esc(t.label)}</strong>
          <span>${t.done_at ? `done ${esc(t.done_at)}` : (t.due ? esc(t.due) : "no date")}</span>
          ${t.detail ? `<small>${esc(t.detail)}</small>` : ""}
        </li>`).join("")}</ul>`
      : `<p class="page-sub">No steps yet. They are laid out from the site date.</p>`}
    </div>`);
  $("#cc-save")?.addEventListener("click", async () => {
    const el = $("#cc-msg");
    el.textContent = "Saving...";
    try {
      await crmSave("contract", key, {
        site_date: $("#cc-site").value.trim(),
        value: parseFloat($("#cc-value").value) || null,
        po_ref: $("#cc-po").value.trim(),
        status: $("#cc-status").value,
      }, "edited on the hub");
      el.textContent = "Saved";
      const row = (CRM.contracts || []).find((c) => c.key === key);
      if (row) row.site_date = $("#cc-site").value.trim();
      render();
    } catch { el.textContent = "Could not save"; }
  });
}

/* One job, everything against it - the meeting's "I should just be able to
   click into the job and see all that sort of stuff as well". Fetched on open
   rather than held, because the joined view is big and mostly unread. */
async function crmPanelLead(key) {
  openPanel(`<h2>Loading...</h2>`);
  let d;
  try { d = await api("crm/lead/" + encodeURIComponent(key)); }
  catch { toast("Could not load that job"); closePanel(); return; }
  if (!d || d.error) { toast("No such job"); closePanel(); return; }
  const L = d.lead, C = d.company || {};
  const sec = (title, body) => body ? `<div class="panel-sec"><h4>${title}</h4>${body}</div>` : "";
  const flags = leadFlags(L);
  openPanel(`
    <h2>${esc(L.title || L.key)}</h2>
    <p class="sub">${esc(C.name || L.company_key)}${L.site ? " &middot; " + esc(L.site) : ""}</p>
    ${flags.length ? `<div class="crm-flags">${flags.map((f) =>
      `<p><strong>${esc(f.label)}.</strong> ${esc(f.why)}</p>`).join("")}</div>` : ""}
    <div class="panel-sec"><h4>Edit</h4>
      <div class="crm-form">
        ${crmField("cl-stage", "Stage", L.stage,
          Object.entries(STAGE_LABEL).map(([k, v]) => [k, v]))}
        ${crmField("cl-outcome", "Outcome", L.outcome,
          [["", "still open"], ["won", "won"], ["lost", "lost"], ["no-decision", "no decision"]])}
        ${crmField("cl-value", "Value, ex VAT", L.value || "")}
        ${crmField("cl-date", "Next action date", L.next_action_date)}
        ${crmField("cl-deadline", "Our return date", L.deadline)}
        ${crmField("cl-award", "They hear on", L.award_due)}
      </div>
      <label class="crm-f"><span>Next action</span>
        <textarea id="cl-next" rows="2">${esc(L.next_action || "")}</textarea></label>
      <div class="crm-actions">
        <button id="cl-save" class="btn-primary" type="button">Save</button>
        <button data-quick="7" class="btn-quiet" type="button">Chase in 1 week</button>
        <button data-quick="30" class="btn-quiet" type="button">Chase in 1 month</button>
        <span id="cl-msg" class="crm-msg"></span>
      </div>
    </div>

    <div class="panel-sec"><h4>Notes</h4>
      <textarea id="cl-note" rows="2" placeholder="What was said, and by whom"></textarea>
      <div class="crm-actions"><button id="cl-note-save" class="btn-quiet" type="button">Add note</button></div>
      ${(d.notes || []).length ? `<div class="rt crm-notes">${d.notes.slice(0, 20).map((n) =>
        `<p><small>${esc(n.created.slice(0, 16).replace("T", " "))} &middot;
          ${esc(n.author)} &middot; ${esc(n.source)}</small><br>${esc(n.body.slice(0, 600))}</p>`
        ).join("")}</div>`
        : `<p class="page-sub">Nothing recorded against this job yet.</p>`}
    </div>
    ${sec("Who we deal with", (d.contacts || []).length ? `<ul class="unk">${d.contacts.map((c) => {
      /* Most seeded contacts are an address and nothing else, so falling back
         to the email for the name printed it twice. Name the person when we
         know them; otherwise the address IS the identity. */
      const named = (c.name || "").trim();
      return `<li>${esc(named || c.email)}${c.role ? " - " + esc(c.role) : ""}
        ${named && c.email ? `<br><small>${esc(c.email)}</small>` : ""}
        ${c.phone ? `<br><small>${esc(c.phone)}</small>` : ""}</li>`;
    }).join("")}</ul>` : "")}
    ${sec("The quote that went out", (d.quotes || []).length ? `<table class="tbl"><thead><tr>
        <th>Rev</th><th class="num">Value</th><th>Status</th><th>Issued</th></tr></thead><tbody>
      ${d.quotes.map((q) => `<tr><td>${q.revision}</td><td class="num">${q.value ? gbp(q.value) : "-"}</td>
        <td>${esc(q.status)}</td><td>${esc(q.issued_at || "-")}</td></tr>`).join("")}
      </tbody></table>` : "")}
    ${sec("What changed, and who changed it", (d.events || []).length ? `<div class="rt">
      ${d.events.slice(0, 20).map((e) => `<p><small>${esc(e.created.slice(0, 16).replace("T", " "))}
        &middot; ${esc(e.author)}</small><br>
        <strong>${esc(e.field)}</strong> ${e.was ? esc(e.was) + " &rarr; " : "set to "}${esc(e.now)}
        ${e.why ? `<br><small>${esc(e.why)}</small>` : ""}</p>`).join("")}</div>` : "")}
  `);

  const msg = (t) => { const el = $("#cl-msg"); if (el) el.textContent = t; };
  const collect = () => ({
    stage: $("#cl-stage").value,
    outcome: $("#cl-outcome").value,
    value: parseFloat($("#cl-value").value) || null,
    next_action_date: $("#cl-date").value.trim(),
    deadline: $("#cl-deadline").value.trim(),
    award_due: $("#cl-award").value.trim(),
    next_action: $("#cl-next").value.trim(),
  });
  const push = async (fields, note) => {
    msg("Saving...");
    try {
      await crmSave("lead", key, fields, note || "edited on the hub");
      // Patch the row in memory so the table behind the panel agrees with what
      // was just saved, without refetching 272 leads to change one of them.
      const row = crmLead(key);
      if (row) Object.assign(row, fields);
      msg("Saved");
      render();
    } catch (e) { msg("Could not save"); toast("Could not save that change"); }
  };

  $("#cl-save")?.addEventListener("click", () => push(collect()));
  $$("#panel [data-quick]").forEach((b) => b.addEventListener("click", () => {
    const d2 = new Date(Date.now() + (+b.dataset.quick) * 864e5).toISOString().slice(0, 10);
    $("#cl-date").value = d2;
    push(Object.assign(collect(), { next_action_date: d2 }), "chase date set on the hub");
  }));
  $("#cl-note-save")?.addEventListener("click", async () => {
    const body = $("#cl-note").value.trim();
    if (!body) return;
    try {
      await api("crm/note", { method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ entity_type: "lead", entity_key: key, body, author: who() }) });
      $("#cl-note").value = "";
      toast("Note added");
      crmPanelLead(key);
    } catch { toast("Could not add that note"); }
  });
}

/* THE NAV IS THE BUSINESS, NOT THE STAFF (03/08/2026).
   It used to be a card per bot, so one job appeared in three places - Mary's
   pipeline, Jacob's leads, the CRM's leads - and you had to know which bot to
   ask before you could find anything. Adding a CRM card made a fourth. Zac,
   03/08: "this is horrible... you should have the crm in the same section as
   the bots... re think the entire UX."

   So the sections below are the work: a job lives in exactly ONE of them. The
   bots do not disappear - they become a name on the row saying who did this
   and what they are waiting on, plus a card underneath for talking to them and
   seeing how they are doing. Their own boards stay under those cards, because
   catches, calibration and award feeds are real and are about the BOT rather
   than about a job.

   Money is deliberately inside Contracts rather than its own section: it is
   empty until Adam answers D2-D4, and an empty nav item teaches people to
   ignore a nav item. */
const WORK_PAGES = [
  { key: "today", label: "Today", icon: "home",
    sub: () => "What needs a person today - nothing else" },
  { key: "leads", label: "Leads", icon: "leads",
    sub: () => `${CRM.leads.filter((l) => !l.outcome).length} jobs we are quoting for` },
  { key: "contracts", label: "Contracts", icon: "register",
    sub: () => `${CRM.delivery?.counts?.late || 0} late, ${CRM.delivery?.counts?.due || 0} due today` },
  { key: "companies", label: "Companies", icon: "companies",
    sub: () => `${CRM.companies.length} on the books` },
  /* The front desk. It belongs under The work rather than on a bot card
     because it is not one bot's - it is the thing that decides whose the work
     is, and the question it answers ("what came in and where did it go") is
     about all three at once. */
  { key: "frontdesk", label: "Front desk", icon: "frontdesk",
    sub: () => FD?.totals
      ? `${FD.totals.seen} judged, ${FD.totals.noise} binned`
      : "has not run yet" },
];

/* Who is waiting on a human, across every bot, as one list. This is the
   question the hub exists to answer and it used to take three tabs. */
function needsAHuman() {
  const out = [];
  for (const r of (typeof awaitingReqs === "function" ? awaitingReqs() : [])) {
    out.push({ who: "Mary", title: r.title, why: r.why || r.needs || "", page: "requests", bot: "mary" });
  }
  for (const r of (typeof openJacobReqs === "function" ? openJacobReqs() : [])) {
    out.push({ who: "Jacob", title: r.title, why: r.why || r.needs || "", page: "decisions", bot: "jacob" });
  }
  return out;
}

const CRM_RENDER = {
  /* THE FRONT PAGE, and it answers one question: what does a person have to do
     today? Strictly that - no bot activity, no "what happened overnight". The
     moment it lists things nobody has to act on it stops being a to-do list
     and becomes another board to skim. */
  today() {
    const t = CRM.today;
    const needs = needsAHuman();
    const del = CRM.delivery;
    const calls = t?.due || [];
    const soon = t?.upcoming || [];
    const onsite = [...(del?.late || []), ...(del?.due || [])];
    const nothing = !needs.length && !calls.length && !onsite.length;

    const head = (label, n, tone) => `<h3>${label}${
      n ? ` <span class="chip ${tone || "navy"}">${n}</span>` : ""}</h3>`;

    return `
      ${nothing ? `<div class="empty"><strong>Nothing needs you today.</strong>
        <p>Everything with a date on it is ahead of us. ${t?.counts?.overdue
          ? `There are ${t.counts.overdue} jobs behind - they are on <a data-go="leads">Leads</a>.`
          : ""}</p></div>` : ""}

      ${needs.length ? `${head("Needs you", needs.length, "danger")}
        <p class="page-sub">A bot has stopped and cannot go on until somebody decides.${
          needs.length > 6 ? ` Six of ${needs.length} here - the rest are on each
          bot's own page, because a front page listing twenty decisions is a
          backlog wearing a to-do list's clothes.` : ""}</p>
        <div class="acts">${needs.slice(0, 6).map((n, i) => `
          <div class="act danger" data-bot-go="${esc(n.bot)}:${esc(n.page)}">
            <div class="act-no">${i + 1}</div>
            <div class="act-main">
              <div class="act-top"><strong>${esc(n.title)}</strong>
                <span class="act-co">${esc(n.who)} is blocked</span></div>
              <div class="act-what">${esc((n.why || "").slice(0, 200))}</div>
            </div>
            <div class="act-side"><small>answer &rarr;</small></div>
          </div>`).join("")}</div>
        ${needs.length > 6 ? `<p class="page-sub">${needs.length - 6} more:
          <a data-bot-go="mary:requests">Mary</a> &middot;
          <a data-bot-go="jacob:decisions">Jacob</a></p>` : ""}` : ""}

      ${calls.length ? `${head("Calls", calls.length, "warn")}
        ${crmRows(calls, "")}` : ""}

      ${onsite.length ? `${head("On site", onsite.length, del?.counts?.late ? "danger" : "warn")}
        <p class="page-sub">Ordering and bookings that have reached their date.</p>
        <div class="acts">${onsite.map((r, i) => `
          <div class="act ${r.due < del.date ? "danger" : "warn"}">
            <div class="act-no">${i + 1}</div>
            <div class="act-main">
              <div class="act-top"><strong>${esc(r.label)}</strong>
                <span class="act-co">${esc(r.job)}</span>${whenChip(r.due)}</div>
              <div class="act-what">${esc(r.detail || "")}</div>
            </div>
            <div class="act-side"><small>Joseph</small></div>
          </div>`).join("")}</div>` : ""}

      ${soon.length ? `<h3>Coming this week</h3>${crmRows(soon, "")}` : ""}

      ${t?.counts?.overdue ? `<p class="page-sub" style="margin-top:1.5rem">
        ${t.counts.overdue} jobs are past their chase date and are not listed here -
        a backlog is not a to-do list. They are on <a data-go="leads">Leads</a>,
        biggest first.</p>` : ""}`;
  },

  /* Every job we are quoting for, in one list, ordered by what is most
     overdue. Split by WHO HAS IT rather than by stage: the only thing a
     person wants to know here is whether it is sitting with estimating or
     out with the client, and that is exactly where the Mary/Jacob handover
     falls. */
  /* ---------------------------------------------------------------- LEADS
     A RECORD LIST, not an essay about one. Filter, sort, open, change. The
     version before this grouped everything into five commentaried sections
     and had nothing you could click or edit, which is a report, not a CRM. */
  leads() {
    const rows = crmFilterSort(CRM.leads, CRMV.leadFilter, CRMV.leadSort);
    const counts = {
      all: CRM.leads.length,
      live: CRM.leads.filter((l) => !l.outcome && isLive(l)).length,
      quiet: CRM.leads.filter((l) => !l.outcome && isQuiet(l)).length,
      pricing: CRM.leads.filter((l) => !l.outcome && MARY_STAGES.includes(l.stage)).length,
      undated: CRM.leads.filter((l) => !l.outcome && leadAge(l) === null).length,
      flagged: CRM.leads.filter((l) => !l.outcome && flagged(l)).length,
      closed: CRM.leads.filter((l) => l.outcome).length,
    };
    return `
      ${crmTabs("lead", [
        ["all", "All", counts.all], ["live", "Live", counts.live],
        ["quiet", "Gone quiet", counts.quiet], ["pricing", "With estimating", counts.pricing],
        ["undated", "No date", counts.undated],
        ["flagged", "Needs checking", counts.flagged], ["closed", "Closed", counts.closed],
      ], CRMV.leadFilter)}
      ${crmCount(rows.length, CRM.leads.length, "job")}
      <table class="tbl crm-tbl">
        <thead><tr>
          ${crmTh("lead", "title", "Job")}
          ${crmTh("lead", "company", "Client")}
          ${crmTh("lead", "stage", "Stage")}
          ${crmTh("lead", "value", "Value", true)}
          ${crmTh("lead", "next_action", "Next action")}
          ${crmTh("lead", "next_action_date", "Due")}
        </tr></thead>
        <tbody>${rows.map((l) => `<tr data-crm="${esc(l.key)}">
          <td class="crm-title"><span><strong>${esc(l.title || l.key)}</strong></span></td>
          <td class="crm-title"><span>${esc((crmCo(l.company_key) || {}).name || l.company_key)}</span></td>
          <td><span class="chip ${stageTone(l.stage)}">${esc(STAGE_LABEL[l.stage] || l.stage)}</span>
              ${l.outcome ? `<span class="chip ${l.outcome === "won" ? "ok" : "danger"}">${esc(l.outcome)}</span>` : ""}</td>
          <td class="num">${l.value ? gbp(l.value) : "-"}</td>
          <td class="crm-next"><span>${esc((l.next_action || "").slice(0, 160)) || "<em>none set</em>"}</span></td>
          <td class="nowrap">${l.next_action_date
              ? `${esc(l.next_action_date)} ${whenChip(l.next_action_date)}` : "-"}
            ${leadFlags(l).map((f) => `<span class="chip danger" title="${esc(f.why)}">${esc(f.label)}</span>`).join("")}</td>
        </tr>`).join("")}</tbody>
      </table>
      ${rows.length ? "" : `<div class="empty"><strong>Nothing matches.</strong></div>`}`;
  },

  /* ------------------------------------------------------------ COMPANIES */
  companies() {
    const rows = crmFilterSort(CRM.companies, CRMV.coFilter, CRMV.coSort);
    const liveLeads = CRM.leads.filter((l) => !l.outcome);
    const withLead = new Set(liveLeads.map((l) => l.company_key));
    const bought = CRM.companies.filter((c) => c.relationship === "won");
    return `
      ${crmTabs("co", [
        ["all", "All", CRM.companies.length],
        ["customers", "Customers", bought.length],
        ["dormant", "Bought, nothing live", bought.filter((c) => !withLead.has(c.key)).length],
        ["active", "Quoting now", CRM.companies.filter((c) => withLead.has(c.key)).length],
        ["never", "Never bought", CRM.companies.filter((c) => c.relationship !== "won").length],
      ], CRMV.coFilter)}
      ${crmCount(rows.length, CRM.companies.length, "company", "companies")}
      <table class="tbl crm-tbl">
        <thead><tr>
          ${crmTh("co", "name", "Company")}
          ${crmTh("co", "relationship", "Relationship")}
          ${crmTh("co", "lifetime_value", "Paid us", true)}
          ${crmTh("co", "openval", "Live quotes", true)}
          ${crmTh("co", "last_contact", "Last contact")}
        </tr></thead>
        <tbody>${rows.map((c) => {
          const q = liveLeads.filter((l) => l.company_key === c.key);
          return `<tr data-crmco="${esc(c.key)}">
            <td class="crm-title"><span><strong>${esc(c.name)}</strong></span></td>
            <td><span class="chip ${c.relationship === "won" ? "ok" : "navy"}">${esc(c.relationship)}</span></td>
            <td class="num">${c.lifetime_value ? gbp(c.lifetime_value) : "-"}</td>
            <td class="num">${q.length ? `${q.length} &middot; ${gbpShort(money(q).total)}` : "-"}</td>
            <td class="nowrap">${esc((c.last_contact || "").slice(0, 10)) || "-"}</td>
          </tr>`;
        }).join("")}</tbody>
      </table>
      ${rows.length ? "" : `<div class="empty"><strong>Nothing matches.</strong></div>`}`;
  },

  /* ------------------------------------------------------------ CONTRACTS */
  contracts() {
    const d = CRM.delivery;
    const cons = CRM.contracts || [];
    const liveCons = cons.filter((c) => c.status === "live");
    const schedulable = liveCons.filter((c) => c.site_date);
    const rows = crmFilterSort(cons, CRMV.conFilter, CRMV.conSort);
    const task = (r, i) => `
      <div class="act ${r.due < (d ? d.date : "") ? "danger" : "warn"}" data-crmcon="${esc(r.entity_key)}">
        <div class="act-no">${i + 1}</div>
        <div class="act-main">
          <div class="act-top"><strong>${esc(r.label)}</strong>
            <span class="act-co">${esc(r.job)}</span>${whenChip(r.due)}</div>
          <div class="act-what">${esc(r.detail || "")}</div>
        </div>
        <div class="act-side"><small>on site ${esc(r.site_date || "-")}</small></div>
      </div>`;
    const due = [...((d && d.late) || []), ...((d && d.due) || [])];
    return `
      ${due.length ? `<h3>Due now <span class="chip danger">${due.length}</span></h3>
        <div class="acts">${due.map(task).join("")}</div>` : ""}
      ${liveCons.length && !schedulable.length ? `<div class="planned-note"><p>
        <strong>${liveCons.length} live contracts and none has a site date, so nothing
        can be scheduled.</strong> Every step counts backwards from the day we go on
        site. Open a contract and set one.</p></div>` : ""}
      ${crmTabs("con", [
        ["live", "Live", liveCons.length],
        ["all", "All", cons.length],
        ["complete", "Complete", cons.filter((c) => c.status !== "live").length],
      ], CRMV.conFilter)}
      ${crmCount(rows.length, cons.length, "contract")}
      <table class="tbl crm-tbl">
        <thead><tr>
          ${crmTh("con", "title", "Job")}
          ${crmTh("con", "company", "Client")}
          ${crmTh("con", "value", "Value", true)}
          ${crmTh("con", "site_date", "On site")}
          ${crmTh("con", "status", "Status")}
        </tr></thead>
        <tbody>${rows.map((c) => `<tr data-crmcon="${esc(c.key)}">
          <td class="crm-title"><span><strong>${esc(c.title || c.key)}</strong></span></td>
          <td class="crm-title"><span>${esc((crmCo(c.company_key) || {}).name || c.company_key)}</span></td>
          <td class="num">${c.value ? gbp(c.value) : "-"}</td>
          <td class="nowrap">${c.site_date ? `${esc(c.site_date)} ${whenChip(c.site_date)}`
            : `<em>not set</em>`}</td>
          <td><span class="chip ${c.status === "live" ? "ok" : "navy"}">${esc(c.status)}</span></td>
        </tr>`).join("")}</tbody>
      </table>`;
  },

  /* THE FRONT DESK. Zac, 04/08: "so we can see everything, what everyone is
     working on etc. how many tasks have been assigned to each bot. how much
     spam. everything the front desk sees i want to see."

     Three questions in that, in this order: who is doing what right now, what
     has been handed to whom, and what came through the door. The last one is
     the whole stream including the binned mail - the point of showing what was
     thrown away is that a wrong call is only findable if it is on a page. */
  frontdesk() {
    if (!FD || FD.never || !FD.totals) {
      return `<div class="empty"><strong>The front desk has not run yet</strong>
        It is the cheap sorter that reads the mailboxes and decides whose each
        message is. Nothing has been through it, so there is nothing to show -
        which is not the same as "no mail came in".
        <p class="page-sub" style="margin-top:10px">Runs as part of the bot
        automation. Residential mail to info@ is deliberately not read.</p></div>`;
    }
    const t = FD.totals, today = FD.today || {};
    const stream = (FD.stream || []).slice().reverse();
    const F = {
      all: () => true,
      work: (r) => r.verdict === "work",
      fyi: (r) => r.verdict === "fyi",
      noise: (r) => r.verdict === "noise",
      mary: (r) => r.bot === "mary",
      jacob: (r) => r.bot === "jacob",
      joseph: (r) => r.bot === "joseph",
    };
    const rows = stream.filter(F[CRMV.fdFilter] || F.all);
    const pct = t.seen ? Math.round((t.noise / t.seen) * 100) : 0;

    /* What each bot is doing, and what it has been handed. The two belong
       together: "Jacob has 23 queued" means one thing if he is working and
       another if he has not started. */
    const staff = ["mary", "jacob", "joseph"].map((k) => {
      const b = BOTS[k];
      const s = b && b.status ? b.status() : null;
      const got = t.bots[k] || { work: 0, fyi: 0, total: 0 };
      const q = { mary: MQUEUE, jacob: JQUEUE }[k];
      const queued = q && Array.isArray(q.items) ? q.items.length : null;
      return `<div class="fd-bot">
        <div class="fd-bot-h">
          <div class="avatar ${b?.accent || ""}">${b?.initials || "?"}</div>
          <div>
            <strong>${esc(b?.name || k)}</strong>
            <span class="fd-state"><i class="dot ${s?.tone || ""}"></i>${esc(s?.text || "Not started")}</span>
          </div>
        </div>
        <p class="fd-thought">${s?.thought ? esc(s.thought)
          : `<em class="dim">Nothing said yet - the last thing it says appears here.</em>`}</p>
        <div class="fd-nums">
          <span><strong>${got.work}</strong> to work</span>
          <span><strong>${got.fyi}</strong> to read</span>
          ${queued === null ? "" : `<span><strong>${queued}</strong> in the queue</span>`}
        </div>
      </div>`;
    }).join("");

    return `
      <p class="page-sub" style="margin:0 0 16px">One cheap pass over the
      mailboxes that decides whose each message is, so no bot has to wake up to
      find out. Every call it has made is here, including the ones it binned.</p>

      <!-- The card is a pointer with a hover lift, so it has to do something
           when you click it. Each one filters the stream below to exactly what
           it counted, through the tab handler that already exists. -->
      <div class="stats">
        <div class="stat" data-crmtab="fd:all"><div class="n">${t.seen}</div>
          <div class="l">Messages judged</div></div>
        <div class="stat green" data-crmtab="fd:work"><div class="n">${t.work}</div>
          <div class="l">Became somebody's work</div></div>
        <div class="stat" data-crmtab="fd:fyi"><div class="n">${t.fyi}</div>
          <div class="l">To read, nothing to do</div></div>
        <div class="stat" data-crmtab="fd:noise"><div class="n">${t.noise}</div>
          <div class="l">Binned as spam - ${pct}% of everything</div></div>
      </div>
      ${today.seen ? `<p class="crm-count">${today.seen} of them in the last 24 hours -
        ${today.work} work, ${today.noise} binned.</p>`
        : `<p class="crm-count">Nothing in the last 24 hours.</p>`}

      <h3 class="fd-h">Who is on what</h3>
      <div class="fd-bots">${staff}</div>

      ${t.worst?.length ? `<h3 class="fd-h">Where the spam comes from</h3>
        <p class="dim" style="margin:-4px 0 10px">Anything here worth a standing rule goes in
        <code>data/knowledge/noise.md</code> - then the classifier stops being asked about it at all.</p>
        <table class="tbl crm-tbl"><thead><tr><th>Sender</th><th class="num">Binned</th></tr></thead>
        <tbody>${t.worst.map(([addr, n]) => `<tr>
          <td class="crm-title"><span>${esc(addr)}</span></td>
          <td class="num">${n}</td></tr>`).join("")}</tbody></table>` : ""}

      <h3 class="fd-h">Everything it has seen</h3>
      ${crmTabs("fd", [
        ["all", "All", t.seen],
        ["work", "Work", t.work],
        ["fyi", "Read only", t.fyi],
        ["noise", "Binned", t.noise],
        ["mary", "Mary", (t.bots.mary || {}).total || 0],
        ["jacob", "Jacob", (t.bots.jacob || {}).total || 0],
        ["joseph", "Joseph", (t.bots.joseph || {}).total || 0],
      ], CRMV.fdFilter)}
      ${crmCount(rows.length, stream.length, "message")}
      ${rows.length ? `<div class="tbl-wrap"><table class="tbl crm-tbl">
        <thead><tr>
          <th>When</th><th>From</th><th>Subject</th>
          <th>Went to</th><th>Call</th><th>Because</th>
        </tr></thead>
        <tbody>${rows.map((r) => `<tr>
          <td class="nowrap dim">${esc(fdWhen(r.ts))}</td>
          <td class="crm-title"><span>${esc(r.from || "-")}</span>
            ${r.mailbox ? `<small class="dim">to ${esc(r.mailbox.split("@")[0])}</small>` : ""}</td>
          <td class="crm-title"><span>${esc(r.subject || "(no subject)")}</span></td>
          <td class="nowrap">${r.verdict === "noise" ? `<span class="dim">nobody</span>`
            : esc(BOTS[r.bot]?.name?.split(" ")[0] || r.bot)}</td>
          <td><span class="chip ${r.verdict === "noise" ? "warn"
            : r.verdict === "fyi" ? "navy" : "ok"}">${esc(r.verdict)}</span></td>
          <td class="crm-title"><span class="dim">${esc(r.why || "-")}</span></td>
        </tr>`).join("")}</tbody></table></div>`
        : `<div class="empty">Nothing under this filter.</div>`}

      <p class="dim" style="margin-top:14px">The archive is
      <code>data/frontdesk-ledger.jsonl</code> on the bot machine; this is the
      last ${FD.stream?.length || 0}. Counts start from when the ledger was
      built and exclude 25 info@ messages removed on 03/08 - that mailbox is
      residential and is no longer read.</p>`;
  },
};

/* "14:32 today" beats a full timestamp on a feed you read top-down, but a
   date has to appear the moment it is not today or the rows silently merge. */
function fdWhen(ts) {
  if (!ts) return "-";
  const d = new Date(ts);
  if (isNaN(d)) return String(ts).slice(0, 16).replace("T", " ");
  const today = new Date();
  const sameDay = d.toDateString() === today.toDateString();
  const hm = d.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
  return sameDay ? hm
    : `${d.toLocaleDateString("en-GB", { day: "numeric", month: "short" })} ${hm}`;
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
  /* THE WORK. Not a bot and not a card - this is the top of the nav, and it is
     what the hub opens on. Everything in it is one record shared by all three
     bots, read live from /api/crm/* rather than from a board file, which is
     what makes "Adam moves a date by email and it is on the page" true. */
  work: {
    key: "work", name: "The work", role: "", initials: "", accent: "",
    pages: WORK_PAGES, render: CRM_RENDER,
    isWork: true,
    status: null, badges: () => ({}),
    needsYou: () => 0,
  },
  /* Joseph Scott, project management. His board IS the Contracts page under
     The work - he has no generated data file of his own, because the CRM is
     already the record for won jobs. So his card carries the two things that
     are his alone: talking to him, and the decisions he cannot make. */
  joseph: {
    key: "joseph", name: "Joseph Scott", role: "Project management", initials: "JS", accent: "js",
    pages: [
      { key: "delivery", label: "Delivery", group: "Work", icon: "register",
        sub: () => "How the won work is running" },
      { key: "decisions", label: "Joseph needs you", group: "Talk",
        sub: () => `${openJosephReqs().length} decision${openJosephReqs().length === 1 ? "" : "s"} he cannot make alone` },
      { key: "jomessages", label: "Messages", group: "Talk", layout: "chat",
        sub: () => "Two-way line - he picks this up on his next pass" },
    ],
    render: {
      /* A WORKING DEFAULT, AND HE IS EXPECTED TO REPLACE IT. The brief is in
         JOSEPH-HUB-DEV.md: build the page you would want open while you do the
         job. This exists so nothing waits on him, not because it is right. */
      delivery() {
        const cons = (CRM.contracts || []).filter((c) => c.status === "live");
        const dated = cons.filter((c) => c.site_date);
        const d = CRM.delivery || { counts: { late: 0, due: 0, coming: 0 } };
        const soon = [...dated].sort((a, b) => (a.site_date || "").localeCompare(b.site_date || ""));
        return `
          <div class="stats">
            <div class="stat" data-go="contracts"><div class="n">${cons.length}</div>
              <div class="l">Live jobs</div></div>
            <div class="stat"><div class="n">${dated.length}</div>
              <div class="l">Have a site date, so can be scheduled</div></div>
            <div class="stat"><div class="n">${d.counts.late}</div>
              <div class="l">Steps late</div></div>
            <div class="stat"><div class="n">${d.counts.due}</div>
              <div class="l">Due today</div></div>
          </div>
          ${cons.length && !dated.length ? `<div class="planned-note"><p>
            <strong>${cons.length} won jobs and not one has a site date, so nothing can
            be scheduled.</strong> Every step counts backwards from the day we go on
            site. Open a job on <a data-go="contracts">Contracts</a> and set one - that
            is the single edit that turns this page on.</p></div>` : ""}
          <h3>Going on site next</h3>
          ${soon.length ? `<table class="tbl crm-tbl"><thead><tr>
              <th>Job</th><th>Client</th><th>On site</th></tr></thead><tbody>
            ${soon.slice(0, 15).map((c) => `<tr data-crmcon="${esc(c.key)}">
              <td class="crm-title"><span>${esc(c.title || c.key)}</span></td>
              <td class="crm-title"><span>${esc((crmCo(c.company_key) || {}).name || c.company_key)}</span></td>
              <td class="nowrap">${esc(c.site_date)} ${whenChip(c.site_date)}</td>
            </tr>`).join("")}</tbody></table>`
            : `<div class="empty"><strong>Nothing is scheduled.</strong>
                <p>No live job has a site date yet.</p></div>`}
          <h3>What he has been doing</h3>
          ${josephActivity()}
          <div class="planned-note"><p>His jobs themselves live on
            <a data-go="contracts">Contracts</a>, with Leads and Companies, because a
            won job is the company's record and not his. This page is a working
            default he is briefed to replace - see <code>JOSEPH-HUB-DEV.md</code>.</p></div>`;
      },
      decisions() {
        const open = openJosephReqs();
        const answered = JOREQS.filter((r) => r.status === "answered");
        if (!open.length && !answered.length) {
          return `<div class="empty"><strong>Nothing is waiting on you.</strong>
            <p>When he cannot decide something alone it appears here with the
            options and a box to answer in, and he picks your answer up on his
            next pass. His work itself is on <a data-go="contracts">Contracts</a>.</p></div>`;
        }
        return decisionsSection("joseph", open, answered);
      },
      jomessages() { return chatPage(BOTS.joseph); },
    },
    status: () => josephStatus(),
    needsYou: () => openJosephReqs().length + unseenJosephMsgs(),
    badges: () => ({ decisions: openJosephReqs().length, jomessages: unseenJosephMsgs() }),
    send: sendToJoseph,
    chat: {
      msgs: () => JOMSGS, seen: "seen_by_joseph", draft: "joseph-msg",
      placeholder: "Message Joseph - a site date, a delivery that has moved, who is fitting what...",
      empty: "Tell him something about a won job and he picks it up on his next pass.",
      hint: () => "picked up on his next pass",
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
  // The work's own sections are already listed at the top of the sidebar by
  // renderSidebar - listing them again here would put the same four buttons
  // on screen twice.
  $("#nav-items").innerHTML = bot.isWork ? "" : pages.map((p) => {
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

/* ---------------- the sign-in card ----------------
   Deliberately outside the render loop: it must be answerable before any board
   data has loaded, and it must survive a render() that throws the page away.
   No Escape handler and no backdrop click - the first ask is the one thing on
   this hub you are not allowed to skip. */
$$("#signin .signin-pick").forEach((b) =>
  b.addEventListener("click", () => setMe(b.dataset.me)));
$("#signin-cancel")?.addEventListener("click", closeSignIn);
$("#who-switch")?.addEventListener("click", () => askWho(Boolean(ME)));
$("#who-chip")?.addEventListener("click", () => askWho(Boolean(ME)));
// Synchronous, so the question is on screen before the first board request
// comes back rather than after it.
paintMe();
if (!ME) askWho(false);

document.addEventListener("click", async (e) => {
  // Anything chosen inside the drawer has served its purpose - get out of the way.
  if (e.target.closest("#nav [data-nav], #nav [data-bot], #nav [data-work]")) setNav(false);
  // A work section: Today, Leads, Contracts, Companies. These sit above the
  // staff cards and are where a job actually lives.
  const wk = e.target.closest("[data-work]");
  if (wk) {
    BOT = "work";
    page = wk.dataset.work;
    searchTerm = "";
    closePanel();
    render();
    return;
  }
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
  // Switching the tab on a record list.
  const tab = e.target.closest("[data-crmtab]");
  if (tab) {
    const [fam, key] = tab.dataset.crmtab.split(":");
    CRMV[fam + "Filter"] = key;
    render();
    return;
  }
  // Sorting one. Clicking the column you are already on flips it.
  const th = e.target.closest("[data-crmsort]");
  if (th) {
    const [fam, col] = th.dataset.crmsort.split(":");
    const s = CRMV[fam + "Sort"];
    if (s.col === col) s.dir = -s.dir; else { s.col = col; s.dir = 1; }
    render();
    return;
  }
  // A CRM row: open the whole job - company, contacts, quote, notes, history.
  const cr = e.target.closest("[data-crm]");
  if (cr) { crmPanelLead(cr.dataset.crm); return; }
  // A company opens the COMPANY. It used to jump to Leads with the company
  // name typed into the search box, which was wrong twice over: a CRM should
  // open the record you clicked, and applyFilter() never matched CRM rows
  // anyway, so the search did nothing and you landed on an unfiltered list
  // wondering what you were looking at.
  const cc = e.target.closest("[data-crmco]");
  if (cc) { crmPanelCompany(cc.dataset.crmco); return; }
  const cn = e.target.closest("[data-crmcon]");
  if (cn) { crmPanelContract(cn.dataset.crmcon); return; }
  // A queued work order: open the full text - the row only has room to clamp.
  const qi = e.target.closest("[data-qitem]");
  if (qi) {
    const item = ((BOT === "jacob" ? JQUEUE : MQUEUE)?.items || [])[+qi.dataset.qitem];
    if (item) queueItemPanel(item);
    return;
  }
  // Any row on Jacob's board with a key: open it and correct it.
  const jrow = e.target.closest("[data-jkey]");
  if (jrow) { crmPanel(jrow.dataset.jkey); return; }
  // Answering one of Jacob's open questions: the chosen option (if any) plus
  // whatever was typed - the same composition Mary's Answer button makes.
  /* Answering a decision, for whichever bot raised it. One handler, because
     Joseph's page had no send path at all - his cards were read-only, so a
     decision he was blocked on could be looked at and not answered. */
  const jrs = e.target.closest("[data-reqsend]");
  if (jrs) {
    const [bot, ref] = jrs.dataset.reqsend.split(":");
    const ta = document.querySelector(`[data-draft="${bot}req-${ref}"]`);
    const chosen = jrs.closest(".req")?.querySelector(".opt.sel")?.textContent.trim() || "";
    const extra = (ta?.value || "").trim();
    const answer = [chosen && `Decision: ${chosen}`, extra].filter(Boolean).join("\n\n");
    if (!answer) { toast("Pick an option or type an answer first"); return; }
    if (!requireMe("An answer to a decision")) return;
    jrs.disabled = true;
    try {
      await api(`${bot}/requests`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ ref, answer, author: who() }),
      });
      delete DRAFTS[`${bot}req-${ref}`];
      delete DRAFTS[`opt:${ref}`];
      if (bot === "jacob") {
        JREQS = await api("jacob/requests").catch(() => JREQS);
        JMSGS = await api("jacob/messages").catch(() => JMSGS);
      } else {
        JOREQS = await api("joseph/requests").catch(() => JOREQS);
        JOMSGS = await api("joseph/messages").catch(() => JOMSGS);
      }
      toast(`Answered ${ref} - ${BOTS[bot]?.name?.split(" ")[0] || bot} picks it up on his next pass`);
      render();
    } catch { toast("Could not save that"); jrs.disabled = false; }
    return;
  }

  // Jacob's questions post to his own endpoint, not Mary's.
  const jopt = e.target.closest(".req-options .opt[data-jreq]");
  if (jopt) {
    const ref = jopt.dataset.jreq;
    const answer = jopt.textContent.trim();
    if (!requireMe("An answer to a decision")) return;
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
    if (!requireMe("A won/lost result")) return;
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
    [JACTIVITY, JSTATUS, MQUEUE, JQUEUE] = await Promise.all([
      api("jacob-activity").catch(() => null),
      api("jacob/status").catch(() => null),
      api("mary/queue").catch(() => null),
      api("jacob/queue").catch(() => null),
    ]);
    // A bot whose board data is missing loses its card but takes nothing
    // else down - the registry entry stays so its data can still be read.
    if (!JACOB) BOTS.jacob.hidden = true;

    // The CRM. Four independent calls so one slow table cannot hold the hub
    // up, and every one falls back to empty rather than taking the page down.
    const [cToday, cLeads, cCos, cCons, cDel] = await Promise.all([
      api("crm/today").catch(() => null),
      api("crm/leads").catch(() => []),
      api("crm/companies").catch(() => []),
      api("crm/contracts").catch(() => []),
      api("crm/delivery").catch(() => null),
    ]);
    CRM = { today: cToday, leads: cLeads || [], companies: cCos || [],
            contracts: cCons || [], delivery: cDel };

    [JOMSGS, JOREQS, JOSTATUS, FD] = await Promise.all([
      api("joseph/messages").catch(() => []),
      api("joseph/requests").catch(() => []),
      api("joseph/status").catch(() => null),
      api("frontdesk").catch(() => null),
    ]);
    JOEVENTS = await api("crm/events?author=joseph&limit=40").catch(() => []);

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
        /* All three statuses in one request rather than three. They are read
           on every beat for the sidebar, so this is the cheapest place a
           round trip could be removed - and it keeps the three cards
           consistent with each other, which separate calls did not. */
        const [fresh, all, jmsgs, chat, reqs, mq, jq, fd] = await Promise.all([
          api("messages").catch(() => MESSAGES),
          api("bots").catch(() => null),
          api("jacob/messages").catch(() => JMSGS),
          api("botchat").catch(() => BOTCHAT),
          api("jacob/requests").catch(() => JREQS),
          api("mary/queue").catch(() => MQUEUE),
          api("jacob/queue").catch(() => JQUEUE),
          page === "frontdesk" ? api("frontdesk").catch(() => FD) : Promise.resolve(FD),
        ]);
        const queueChanged = (mq?.updated !== MQUEUE?.updated) || (jq?.updated !== JQUEUE?.updated);
        MQUEUE = mq; JQUEUE = jq;
        if (queueChanged && ["queue", "jqueue", "live", "jlive"].includes(page)) render();
        const statusChanged = JSON.stringify(all) !== JSON.stringify(
          { mary: STATUS, jacob: JSTATUS, joseph: JOSTATUS });
        if (all) { STATUS = all.mary; JSTATUS = all.jacob; JOSTATUS = all.joseph; }
        const fdChanged = fd?.updated !== FD?.updated;
        FD = fd;
        if (fdChanged && page === "frontdesk") render();
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
