// Mary Dashboard API.
//   Public (auth disabled per Zac 27/07): data, messages list/post.
//   Mary-only (X-Mary-Key header == MARY_API_KEY secret): pending, reply.
// Messages posted from the site are picked up by Mary's poller and treated
// as instructions from Zac/Adam - re-enable the login gate before sharing
// the URL beyond the two of them.
import { DATA } from "../_data/dashboard-data.js";

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

const now = () => new Date().toISOString();

export async function onRequest(context) {
  const { request, env } = context;
  const route = new URL(request.url).pathname.replace(/^\/api\/?/, "");
  const db = env.DB;
  try {
    if (route === "data") return json(DATA);

    if (route === "messages" && request.method === "GET") {
      const { results } = await db.prepare(
        "SELECT id, created, author, body, context, in_reply_to, seen_by_mary FROM messages ORDER BY id DESC LIMIT 200").all();
      return json(results);
    }

    if (route === "messages" && request.method === "POST") {
      const b = await request.json().catch(() => ({}));
      const author = ["zac", "adam"].includes(String(b.author || "").toLowerCase()) ? b.author.toLowerCase() : "team";
      const body = String(b.body || "").slice(0, 4000).trim();
      const ctx = String(b.context || "").slice(0, 300);
      if (!body) return json({ error: "Empty message" }, 400);
      await db.prepare("INSERT INTO messages (created, author, body, context) VALUES (?, ?, ?, ?)")
        .bind(now(), author, body, ctx).run();
      return json({ ok: true });
    }

    // ---- Mary-only routes ----
    if (!env.MARY_API_KEY || request.headers.get("x-mary-key") !== env.MARY_API_KEY) {
      return json({ error: "Not found" }, 404);
    }

    if (route === "mary/pending") {
      const { results } = await db.prepare(
        "SELECT id, created, author, body, context FROM messages WHERE seen_by_mary = 0 AND author != 'mary' ORDER BY id").all();
      return json(results);
    }

    if (route === "mary/reply" && request.method === "POST") {
      const b = await request.json().catch(() => ({}));
      const body = String(b.body || "").slice(0, 8000).trim();
      const replyTo = parseInt(b.in_reply_to, 10) || null;
      if (body) {
        await db.prepare("INSERT INTO messages (created, author, body, context, in_reply_to, seen_by_mary) VALUES (?, 'mary', ?, ?, ?, 1)")
          .bind(now(), body, String(b.context || "").slice(0, 300), replyTo).run();
      }
      if (replyTo) {
        await db.prepare("UPDATE messages SET seen_by_mary = 1 WHERE id = ?").bind(replyTo).run();
      }
      if (Array.isArray(b.mark_seen)) {
        for (const id of b.mark_seen.slice(0, 50)) {
          await db.prepare("UPDATE messages SET seen_by_mary = 1 WHERE id = ?").bind(parseInt(id, 10) || 0).run();
        }
      }
      return json({ ok: true });
    }

    return json({ error: "Not found" }, 404);
  } catch (error) {
    return json({ error: error.message || "Something went wrong" }, 500);
  }
}
