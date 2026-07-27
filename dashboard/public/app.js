// Mary Grace Estimating Hub - all-in-one view of Mary's world plus two-way
// messaging (messages persist in D1; Mary's poller collects them and her
// replies land back here).
const $ = (s) => document.querySelector(s);

const TABS = [
  { key: "overview", label: "Overview" },
  { key: "deadlines", label: "Deadlines" },
  { key: "flags", label: "Needs a human" },
  { key: "messages", label: "Message Mary" },
  { key: "emails", label: "Mary's emails" },
  { key: "inbox", label: "Inbox seen" },
  { key: "catches", label: "Catches" },
];

let DATA = null;
let MESSAGES = [];
let active = "overview";

async function api(route, options) {
  const res = await fetch(`/api/${route}`, options);
  if (!res.ok) throw Object.assign(new Error("api"), { status: res.status });
  return res.json();
}

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const who = () => $("#who").value;
const daysUntil = (iso) => Math.ceil((new Date(iso + "T12:00:00") - Date.now()) / 86400000);

function rag(job) {
  if (job.stage === "submitted") return ["ok", "Submitted"];
  const d = daysUntil(job.deadline);
  if (d < 0) return ["danger", `${-d}d overdue`];
  if (d <= 2) return ["danger", d === 0 ? "DUE TODAY" : `${d}d left`];
  if (d <= 5) return ["warn", `${d}d left`];
  return ["ok", `${d}d left`];
}

/* ---------- drawer ---------- */
function openDrawer(html) {
  $("#drawer-body").innerHTML = html;
  $("#drawer").hidden = false;
  $("#drawer-veil").hidden = false;
}
function closeDrawer() {
  $("#drawer").hidden = true;
  $("#drawer-veil").hidden = true;
}
$("#drawer-close").addEventListener("click", closeDrawer);
$("#drawer-veil").addEventListener("click", closeDrawer);
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeDrawer(); });

function related(jobName) {
  const n = jobName.toLowerCase().split(" ").filter((w) => w.length > 4);
  const match = (t) => n.some((w) => (t || "").toLowerCase().includes(w));
  return {
    flags: DATA.flags.filter((f) => match(f.job)),
    catches: DATA.catches.filter((c) => match(c.job)),
    emails: DATA.emails.filter((e) => match(e.subject)),
    inbox: (DATA.inbox || []).filter((i) => match(i.subject)),
  };
}

function jobDrawer(j) {
  const [tone, badge] = rag(j);
  const r = related(j.job);
  const li = (arr, fmt, empty) => arr.length ? `<div class="mini-list">${arr.map(fmt).join("")}</div>` : `<p class="empty">${empty}</p>`;
  openDrawer(`
    <h3>${esc(j.job)}</h3>
    <p class="sub">${esc(j.client)} - deadline ${esc(j.deadline)} <span class="pill ${tone}">${esc(badge)}</span></p>
    <div class="drawer-section"><h4>Position</h4><p>${esc(j.status)}</p><p><strong>${esc(j.value)}</strong></p></div>
    <div class="drawer-section"><h4>Open flags</h4>${li(r.flags.filter((f) => f.status === "open"), (f) => `<div class="mini-item static">${esc(f.flag)}<small>owner: ${esc(f.owner)} - raised ${esc(f.raised)}</small></div>`, "None")}</div>
    <div class="drawer-section"><h4>Catches on this job</h4>${li(r.catches, (c) => `<div class="mini-item static">${esc(c.catch)}<small>${esc(c.date)}</small></div>`, "None")}</div>
    <div class="drawer-section"><h4>Mary's emails about it</h4>${li(r.emails, (e, i) => `<div class="mini-item" data-email="${DATA.emails.indexOf(e)}">${esc(e.subject)}<small>${esc(e.sent)}</small></div>`, "None yet")}</div>
    <div class="drawer-section"><h4>Seen in the inbox</h4>${li(r.inbox.slice(0, 8), (i) => `<div class="mini-item" data-inbox="${(DATA.inbox || []).indexOf(i)}">${esc(i.subject)}<small>${esc(i.from)} - ${esc(i.received)}</small></div>`, "Nothing filed")}</div>
    <div class="drawer-section"><h4>Ask Mary about this job</h4>
      <div class="reply-inline"><textarea id="job-ask" placeholder="e.g. chase the supplier, re-price with the new quote, explain the number..."></textarea>
      <button class="primary" id="job-ask-send">Send to Mary</button></div>
    </div>`);
  $("#job-ask-send").addEventListener("click", async () => {
    const body = $("#job-ask").value.trim();
    if (!body) return;
    await sendMessage(body, j.job);
    closeDrawer();
    active = "messages";
    render();
  });
}

function emailDrawer(e) {
  openDrawer(`
    <h3>${esc(e.subject)}</h3>
    <p class="sub">Sent ${esc(e.sent)} - to ${esc(e.to)}</p>
    <div class="drawer-section"><h4>Full email</h4><div class="email-body">${esc(e.body || "(body not captured for this email)")}</div></div>`);
}

function inboxDrawer(i) {
  openDrawer(`
    <h3>${esc(i.subject) || "(no subject)"}</h3>
    <p class="sub">From ${esc(i.from)} - ${esc(i.received)}${i.attachments ? ` - ${i.attachments} attachment(s)` : ""}</p>
    <div class="drawer-section"><h4>What Mary read</h4><div class="email-body">${esc(i.body || "(body not stored)")}</div></div>`);
}

function flagDrawer(f) {
  openDrawer(`
    <h3>${esc(f.job)}</h3>
    <p class="sub">Raised ${esc(f.raised)} - owner: ${esc(f.owner)}</p>
    <div class="drawer-section"><h4>What Mary needs</h4><p>${esc(f.flag)}</p></div>
    <div class="drawer-section"><h4>Answer Mary here</h4>
      <div class="reply-inline"><textarea id="flag-reply" placeholder="Give the decision or the info - Mary picks this up within 15 minutes."></textarea>
      <button class="primary" id="flag-reply-send">Send answer</button></div>
    </div>`);
  $("#flag-reply-send").addEventListener("click", async () => {
    const body = $("#flag-reply").value.trim();
    if (!body) return;
    await sendMessage(body, `FLAG: ${f.job} - ${f.flag.slice(0, 120)}`);
    closeDrawer();
    active = "messages";
    render();
  });
}

/* ---------- messaging ---------- */
async function sendMessage(body, context = "") {
  await api("messages", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ author: who(), body, context }),
  });
  MESSAGES = await api("messages");
}

/* ---------- views ---------- */
const VIEWS = {
  overview() {
    const open = DATA.flags.filter((f) => f.status === "open").length;
    const overdue = DATA.jobs.filter((j) => j.stage === "overdue").length;
    const dueSoon = DATA.jobs.filter((j) => j.stage !== "submitted" && j.stage !== "overdue" && daysUntil(j.deadline) <= 3).length;
    const unseen = MESSAGES.filter((m) => m.author !== "mary" && !m.seen_by_mary).length;
    const urgent = [...DATA.jobs].filter((j) => j.stage !== "submitted").sort((a, b) => new Date(a.deadline) - new Date(b.deadline)).slice(0, 4);
    return `
      <div class="kpis">
        <div class="kpi"><div class="n">${DATA.jobs.length}</div><div class="l">Live jobs tracked</div></div>
        <div class="kpi ${dueSoon ? "" : "green"}"><div class="n">${dueSoon}</div><div class="l">Due within 3 days</div></div>
        <div class="kpi"><div class="n">${overdue}</div><div class="l">Overdue</div></div>
        <div class="kpi"><div class="n">${open}</div><div class="l">Waiting on a human</div></div>
        <div class="kpi green"><div class="n">${DATA.catches.length}</div><div class="l">Catches logged</div></div>
      </div>
      <div class="card-grid">
        ${urgent.map((j) => this._jobCard(j)).join("")}
        <div class="card static">
          <div class="card-head"><strong>Mary's engine room</strong></div>
          <p>${DATA.sessions.polls.toLocaleString()} inbox polls - ${DATA.sessions.launched} working sessions - ${DATA.sessions.emailsSent} emails sent${unseen ? ` - <strong>${unseen} message(s) waiting for Mary's next cycle</strong>` : ""}</p>
          <p>${esc(DATA.register.recent)}</p>
        </div>
      </div>`;
  },
  _jobCard(j) {
    const [tone, badge] = rag(j);
    return `<article class="card" data-job="${esc(j.job)}">
      <header class="card-head"><div><strong>${esc(j.job)}</strong><small>${esc(j.client)}</small></div><span class="pill ${tone}">${esc(badge)}</span></header>
      <p>${esc(j.status)}</p>
      <footer class="card-foot"><span>Deadline: ${esc(j.deadline)}</span><span>${esc(j.value)}</span></footer></article>`;
  },
  deadlines() {
    const jobs = [...DATA.jobs].sort((a, b) => (a.stage === "submitted") - (b.stage === "submitted") || new Date(a.deadline) - new Date(b.deadline));
    return `<div class="card-grid">${jobs.map((j) => this._jobCard(j)).join("")}</div>`;
  },
  flags() {
    const open = DATA.flags.filter((f) => f.status === "open");
    if (!open.length) return `<p class="empty">Nothing waiting - every flag has been answered.</p>`;
    return `<div class="card-grid">${open.map((f, i) => `
      <article class="card" data-flag="${DATA.flags.indexOf(f)}">
        <header class="card-head"><div><strong>${esc(f.job)}</strong><small>raised ${esc(f.raised)} - needs: ${esc(f.owner)}</small></div><span class="pill warn">answer me</span></header>
        <p>${esc(f.flag)}</p>
        <footer class="card-foot"><span>Click to answer Mary directly</span></footer>
      </article>`).join("")}</div>`;
  },
  messages() {
    const thread = [...MESSAGES].reverse();
    return `<div class="chat">
      <div class="chat-thread">${thread.length ? thread.map((m) => `
        <div class="msg ${m.author === "mary" ? "mary" : "human"}${m.author !== "mary" && !m.seen_by_mary ? " unseen" : ""}">
          <div class="meta">${esc(m.author.toUpperCase())} - ${esc(m.created.slice(0, 16).replace("T", " "))}${m.author !== "mary" ? (m.seen_by_mary ? " - seen" : " - waiting for Mary") : ""}</div>
          ${m.context ? `<div class="ctx">${esc(m.context)}</div>` : ""}${esc(m.body)}
        </div>`).join("") : `<p class="empty">No messages yet - say hello.</p>`}</div>
      <div class="chat-compose">
        <textarea id="chat-body" placeholder="Ask Mary anything - price a job, chase something, explain a number. She checks every 15 minutes and replies here."></textarea>
        <div class="chat-actions">
          <span class="chat-hint">Sending as <strong id="chat-as">${esc(who())}</strong> - Mary picks messages up on her next poll cycle</span>
          <button class="primary" id="chat-send">Send to Mary</button>
        </div>
      </div></div>`;
  },
  emails() {
    return `<div class="card-grid">${DATA.emails.map((e, i) => `
      <article class="card" data-email="${i}">
        <header class="card-head"><div><strong>${esc(e.subject)}</strong><small>${esc(e.sent)} - to ${esc(e.to)}</small></div><span class="pill navy">sent</span></header>
        <footer class="card-foot"><span>Click to read the full email</span></footer>
      </article>`).join("")}</div>`;
  },
  inbox() {
    const items = DATA.inbox || [];
    if (!items.length) return `<p class="empty">No processed inbox items captured yet.</p>`;
    return `<div class="card-grid">${items.map((m, i) => `
      <article class="card" data-inbox="${i}">
        <header class="card-head"><div><strong>${esc(m.subject) || "(no subject)"}</strong><small>${esc(m.from)} - ${esc(m.received)}</small></div>${m.attachments ? `<span class="pill navy">${m.attachments} att</span>` : ""}</header>
        <p>${esc((m.body || "").slice(0, 140))}...</p>
      </article>`).join("")}</div>`;
  },
  catches() {
    return `<div class="card-grid">${DATA.catches.map((c) => `
      <article class="card static">
        <header class="card-head"><div><strong>${esc(c.job)}</strong><small>${esc(c.date)}</small></div><span class="pill ok">${esc(c.type)}</span></header>
        <p>${esc(c.catch)}</p>
      </article>`).join("")}</div>`;
  },
};

const EYEBROWS = {
  overview: "Everything at a glance", deadlines: "Every live tender, most urgent first",
  flags: "Mary is blocked without you", messages: "Two-way line to the estimating AI",
  emails: "Every email Mary has ever sent", inbox: "What Mary has read and filed",
  catches: "Errors and savings Mary has caught",
};

function render() {
  const openFlags = DATA.flags.filter((f) => f.status === "open").length;
  const counts = { flags: openFlags || "", messages: MESSAGES.filter((m) => m.author !== "mary" && !m.seen_by_mary).length || "" };
  $("#tabs").innerHTML = TABS.map((t) =>
    `<button class="tab${t.key === active ? " active" : ""}" data-key="${t.key}">${t.label}${counts[t.key] ? `<span class="count">${counts[t.key]}</span>` : ""}</button>`).join("");
  $("#view-title").textContent = TABS.find((t) => t.key === active).label;
  $("#view-eyebrow").textContent = EYEBROWS[active];
  $("#view").innerHTML = VIEWS[active] ? VIEWS[active].call(VIEWS) : "";
  $("#updated-at").textContent = "updated " + new Date(DATA.updated).toLocaleString("en-GB", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" });
  const send = $("#chat-send");
  if (send) send.addEventListener("click", async () => {
    const body = $("#chat-body").value.trim();
    if (!body) return;
    send.disabled = true;
    await sendMessage(body);
    render();
  });
}

document.addEventListener("click", (e) => {
  const t = e.target.closest("[data-key],[data-job],[data-flag],[data-email],[data-inbox]");
  if (!t) return;
  if (t.dataset.key) { active = t.dataset.key; render(); return; }
  if (t.dataset.job) { const j = DATA.jobs.find((x) => x.job === t.dataset.job); if (j) jobDrawer(j); return; }
  if (t.dataset.flag !== undefined) { flagDrawer(DATA.flags[+t.dataset.flag]); return; }
  if (t.dataset.email !== undefined) { emailDrawer(DATA.emails[+t.dataset.email]); return; }
  if (t.dataset.inbox !== undefined) { inboxDrawer((DATA.inbox || [])[+t.dataset.inbox]); return; }
});

$("#who").addEventListener("change", () => { const el = $("#chat-as"); if (el) el.textContent = who(); });

(async () => {
  try {
    [DATA, MESSAGES] = await Promise.all([api("data"), api("messages")]);
    render();
    setInterval(async () => { try { MESSAGES = await api("messages"); if (active === "messages" || active === "overview") render(); } catch {} }, 30000);
  } catch (err) {
    $("#view").innerHTML = `<p class="empty">Could not load the hub (${err.status || err.message}).</p>`;
  }
})();
