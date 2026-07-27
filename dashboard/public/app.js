// Mary Grace's Desk - renders /api/data. Same shell pattern as the
// Marketing Dashboard: login view + sidebar tabs + single #view container.
const $ = (sel) => document.querySelector(sel);

const TABS = [
  { key: "deadlines", label: "Deadlines" },
  { key: "flags", label: "Waiting on humans" },
  { key: "emails", label: "Emails sent" },
  { key: "catches", label: "Catches" },
  { key: "sessions", label: "Sessions" },
];

let DATA = null;
let active = "deadlines";

async function api(route, options) {
  const res = await fetch(`/api/${route}`, options);
  if (!res.ok) throw Object.assign(new Error("api"), { status: res.status });
  return res.json();
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function daysUntil(iso) {
  return Math.ceil((new Date(iso + "T12:00:00") - Date.now()) / 86400000);
}

function rag(job) {
  if (job.stage === "submitted") return ["ok", "Submitted"];
  const d = daysUntil(job.deadline);
  if (d < 0) return ["danger", `${-d}d overdue`];
  if (d <= 2) return ["danger", d === 0 ? "TODAY" : `${d}d left`];
  if (d <= 5) return ["warn", `${d}d left`];
  return ["ok", `${d}d left`];
}

function card(inner) {
  return `<article class="card">${inner}</article>`;
}

const VIEWS = {
  deadlines() {
    const jobs = [...DATA.jobs].sort((a, b) => (a.stage === "submitted") - (b.stage === "submitted") || new Date(a.deadline) - new Date(b.deadline));
    return jobs.map((j) => {
      const [tone, badge] = rag(j);
      return card(`
        <header class="card-head">
          <div><strong>${esc(j.job)}</strong><small>${esc(j.client)}</small></div>
          <span class="pill ${tone}">${esc(badge)}</span>
        </header>
        <p>${esc(j.status)}</p>
        <footer class="card-foot"><span>Deadline: ${esc(j.deadline)}</span><span>${esc(j.value)}</span></footer>`);
    }).join("");
  },
  flags() {
    const open = DATA.flags.filter((f) => f.status === "open");
    if (!open.length) return card("<p>Nothing waiting - all flags closed.</p>");
    return open.map((f) => card(`
      <header class="card-head">
        <div><strong>${esc(f.job)}</strong><small>raised ${esc(f.raised)} - owner: ${esc(f.owner)}</small></div>
        <span class="pill warn">open</span>
      </header>
      <p>${esc(f.flag)}</p>`)).join("");
  },
  emails() {
    return DATA.emails.map((e) => card(`
      <header class="card-head">
        <div><strong>${esc(e.subject)}</strong><small>${esc(e.sent)} - to ${esc(e.to)}</small></div>
      </header>`)).join("");
  },
  catches() {
    return DATA.catches.map((c) => card(`
      <header class="card-head">
        <div><strong>${esc(c.job)}</strong><small>${esc(c.date)}</small></div>
        <span class="pill ok">${esc(c.type)}</span>
      </header>
      <p>${esc(c.catch)}</p>`)).join("");
  },
  sessions() {
    const s = DATA.sessions;
    return card(`
      <p><strong>${s.polls}</strong> inbox polls - <strong>${s.launched}</strong> working sessions - <strong>${s.emailsSent}</strong> emails ever sent</p>
      <p>Rate register: <strong>${DATA.register.lines.toLocaleString()}</strong> quote lines across <strong>${DATA.register.categories}</strong> categories.</p>
      <p>${esc(DATA.register.recent)}</p>
      <p><small>Recent no-action sessions: ${esc(s.noAction.join(" | ") || "none")}</small></p>`);
  },
};

function render() {
  $("#tabs").innerHTML = TABS.map((t) =>
    `<button class="tab${t.key === active ? " active" : ""}" data-key="${t.key}">${t.label}</button>`).join("");
  $("#view-title").textContent = TABS.find((t) => t.key === active).label;
  $("#view").innerHTML = `<div class="card-grid">${VIEWS[active]()}</div>`;
  $("#updated-at").textContent = new Date(DATA.updated).toLocaleString("en-GB");
}

async function boot(user) {
  DATA = await api("data");
  $("#login").hidden = true;
  $("#app").hidden = false;
  $("#active-user").textContent = user;
  render();
}

$("#tabs").addEventListener("click", (e) => {
  const key = e.target.dataset?.key;
  if (key) { active = key; render(); }
});

$("#login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  try {
    const { user } = await api("login", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ username: form.get("username"), password: form.get("password") }),
    });
    await boot(user);
  } catch (err) {
    $("#login-error").textContent = err.status === 503 ? "Dashboard not yet unlocked." : "Wrong user or password.";
  }
});

$("#logout").addEventListener("click", async () => {
  await api("logout");
  location.reload();
});

api("me").then(({ user }) => boot(user)).catch(() => {});
