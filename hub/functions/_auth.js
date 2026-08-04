// Authentication for the Glasshouse. Individual accounts, two roles.
//
// Nobody's password is ever set for them: an admin creates the account and
// gets a one-time setup code, the person enters it once and chooses their own
// password. The server only ever stores a PBKDF2 hash and never sees a
// password again after that request.
//
//   admin     Zac and Adam. The whole hub: bots, decisions, drafts, the record.
//   delivery  Paul, Steve, fitters. Their day, and nothing else.

const enc = new TextEncoder();
const b64u = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf)))
  .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const unb64u = (s) => {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  return Uint8Array.from(atob(s + "=".repeat((4 - s.length % 4) % 4)), (c) => c.charCodeAt(0));
};

export function randomCode(n = 6) {
  const d = new Uint8Array(n);
  crypto.getRandomValues(d);
  return [...d].map((x) => "0123456789"[x % 10]).join("");
}
export function randomSalt() {
  const d = new Uint8Array(16);
  crypto.getRandomValues(d);
  return b64u(d);
}

export async function hashPassword(password, salt) {
  const key = await crypto.subtle.importKey("raw", enc.encode(password),
    "PBKDF2", false, ["deriveBits"]);
  // 100,000 is the ceiling Workers allows - it rejects anything higher outright,
  // which means a larger number here does not make logins slower, it makes them
  // impossible. Found the only way it can be: the first real setup failed.
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", salt: enc.encode(salt), iterations: 100000, hash: "SHA-256" },
    key, 256);
  return b64u(bits);
}

// Constant-time-ish compare so a wrong password cannot be timed character by
// character.
export function same(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

async function hmacKey(secret) {
  return crypto.subtle.importKey("raw", enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

export async function mintToken(secret, payload, days = 30) {
  const body = { ...payload, exp: Date.now() + days * 864e5 };
  const data = b64u(enc.encode(JSON.stringify(body)));
  const sig = b64u(await crypto.subtle.sign("HMAC", await hmacKey(secret), enc.encode(data)));
  return data + "." + sig;
}

export async function readToken(secret, token) {
  if (!token || !token.includes(".")) return null;
  const [data, sig] = token.split(".");
  try {
    const ok = await crypto.subtle.verify("HMAC", await hmacKey(secret),
      unb64u(sig), enc.encode(data));
    if (!ok) return null;
    const body = JSON.parse(new TextDecoder().decode(unb64u(data)));
    if (!body.exp || body.exp < Date.now()) return null;
    return body;
  } catch { return null; }
}
