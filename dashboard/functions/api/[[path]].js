// Mary Dashboard API - mirrors the Marketing Dashboard pattern (catch-all
// route, cookie session) but with a single shared password held as a Pages
// secret. Fails closed: no DASHBOARD_PASSWORD secret => nobody can log in.
import { DATA } from "../_data/dashboard-data.js";

const USERS = ["zac", "adam"];
const COOKIE = "mary_session";
const DAY = 86400;

function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...headers },
  });
}

async function hmac(secret, value) {
  const key = await crypto.subtle.importKey(
    "raw", new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(value));
  return btoa(String.fromCharCode(...new Uint8Array(sig))).replace(/=+$/, "");
}

async function makeToken(env, user) {
  const exp = Math.floor(Date.now() / 1000) + 14 * DAY;
  const payload = `${user}.${exp}`;
  return `${payload}.${await hmac(env.COOKIE_SECRET, payload)}`;
}

async function getUser(request, env) {
  if (!env.COOKIE_SECRET) return null;
  const cookie = request.headers.get("cookie") || "";
  const match = cookie.match(new RegExp(`${COOKIE}=([^;]+)`));
  if (!match) return null;
  const [user, exp, sig] = match[1].split(".");
  if (!user || !exp || !sig) return null;
  if (parseInt(exp, 10) < Date.now() / 1000) return null;
  if ((await hmac(env.COOKIE_SECRET, `${user}.${exp}`)) !== sig) return null;
  return USERS.includes(user) ? user : null;
}

async function login(context) {
  const { env, request } = context;
  if (!env.DASHBOARD_PASSWORD || !env.COOKIE_SECRET) {
    return json({ error: "Dashboard not yet unlocked" }, 503);
  }
  const body = await request.json().catch(() => ({}));
  const user = String(body.username || "").toLowerCase();
  if (!USERS.includes(user) || body.password !== env.DASHBOARD_PASSWORD) {
    return json({ error: "Wrong user or password" }, 401);
  }
  const token = await makeToken(env, user);
  return json({ user }, 200, {
    "set-cookie": `${COOKIE}=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=${14 * DAY}`,
  });
}

export async function onRequest(context) {
  const route = new URL(context.request.url).pathname.replace(/^\/api\/?/, "");
  try {
    if (route === "login" && context.request.method === "POST") return login(context);
    if (route === "logout") {
      return json({ ok: true }, 200, { "set-cookie": `${COOKIE}=; Path=/; Max-Age=0` });
    }
    const user = await getUser(context.request, context.env);
    if (!user) return json({ error: "Not signed in" }, 401);
    if (route === "me") return json({ user });
    if (route === "data") return json(DATA);
    return json({ error: "Not found" }, 404);
  } catch (error) {
    return json({ error: error.message || "Something went wrong" }, 500);
  }
}
