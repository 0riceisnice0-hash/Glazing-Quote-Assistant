// Fenster Hub API - every bot, one Worker.
//
// The hub carries more than one bot (Mary Grace, estimating; Jacob Wright,
// business development; whoever comes next). Each bot owns the same set of
// channels - a human chat, a decisions queue, a live activity feed, a status
// line - so the routes are generic: `<bot>/<action>`, resolved through the
// CHANNELS registry below. Adding a bot to the API is one entry in that
// registry plus its tables in schema.sql. No handler is per-bot.
//
// Public (auth disabled per Zac 27/07): board data, message list/post,
// request list/answer, status/activity reads, pipeline overlay.
// Bot-only (X-Mary-Key header == MARY_API_KEY secret, shared by all bots):
// pending, reply, ask, status/activity writes, and the bot-to-bot line.
// Messages posted from the site are treated as instructions from Zac/Adam -
// re-enable the login gate before sharing the URL beyond the two of them.
import { DATA } from "../_data/dashboard-data.js";
import { JACOB } from "../_data/jacob-data.js";

/* One entry per bot. Mary predates the `<bot>_...` table convention, so her
   table and state-key names are the documented exception; everyone from Jacob
   onward follows the pattern. `requests` is null while a bot's decisions still
   live in its deployed board data rather than in D1 (Mary's do - see
   HUB-AUDIT.md for the plan to move them). */
const CHANNELS = {
  mary: {
    board: DATA,
    messages: "messages", seen: "seen_by_mary",
    requests: null, pipeline: null,
    statusKey: "mary", activityKey: "activity",
  },
  jacob: {
    board: JACOB,
    messages: "jacob_messages", seen: "seen_by_jacob",
    requests: "jacob_requests", pipeline: "jacob_pipeline",
    statusKey: "jacob", activityKey: "jacob_activity",
  },
};

/* The spellings the routes had before they were generic. Live bridges poll
   some of these every few seconds, so every one of them must keep answering
   forever - an alias costs a line, a broken bridge costs a working bot. */
const ALIASES = {
  "messages": "mary/messages",
  "status": "mary/status",
  "activity": "mary/activity",
  "jacob-activity": "jacob/activity",
  "jacob": "jacob/board",
  "data": "mary/board",
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

const now = () => new Date().toISOString();
const clip = (v, n) => String(v || "").slice(0, n);
/* Humans the hub knows by name; anything else posts as "team". */
const person = (v) =>
  ["zac", "adam"].includes(String(v || "").toLowerCase()) ? String(v).toLowerCase() : "team";

export async function onRequest(context) {
  const { request, env } = context;
  const raw = new URL(request.url).pathname.replace(/^\/api\/?/, "");
  const route = ALIASES[raw] || raw;
  const [botKey, ...restParts] = route.split("/");
  const action = restParts.join("/");
  const ch = CHANNELS[botKey] || null;
  const db = env.DB;
  const GET = request.method === "GET";
  const POST = request.method === "POST";

  try {
    /* ---------------- public: per-bot channels ---------------- */
    if (ch && action === "board") return json(ch.board);

    if (ch && action === "messages" && GET) {
      const { results } = await db.prepare(
        `SELECT id, created, author, body, context, in_reply_to, ${ch.seen} ` +
        `FROM ${ch.messages} ORDER BY id DESC LIMIT 200`).all();
      return json(results);
    }

    if (ch && action === "messages" && POST) {
      const b = await request.json().catch(() => ({}));
      const body = clip(b.body, 4000).trim();
      if (!body) return json({ error: "Empty message" }, 400);
      await db.prepare(
        `INSERT INTO ${ch.messages} (created, author, body, context) VALUES (?, ?, ?, ?)`)
        .bind(now(), person(b.author), body, clip(b.context, 300)).run();
      return json({ ok: true });
    }

    // What the bot is doing right now, written by its bridge. Public: it is
    // only ever a chat key and a queue depth. Missing row = bot has never
    // reported, which is a real state and not an error.
    if (ch && action === "status" && GET) {
      try {
        const row = await db.prepare("SELECT v, updated FROM state WHERE k = ?")
          .bind(ch.statusKey).first();
        if (!row) return json({ state: "unknown" });
        return json({ ...JSON.parse(row.v), updated: row.updated });
      } catch {
        return json({ state: "unknown" });
      }
    }

    // Live feed of what the bot is doing this second, tailed from its session
    // transcript by its bridge. Stored as one snapshot, not an append log -
    // nobody wants yesterday's tool calls.
    if (ch && action === "activity" && GET) {
      try {
        const row = await db.prepare("SELECT v, updated FROM state WHERE k = ?")
          .bind(ch.activityKey).first();
        if (!row) return json({ events: [] });
        return json({ ...JSON.parse(row.v), updated: row.updated });
      } catch {
        return json({ events: [] });
      }
    }

    // What is waiting to run and what kicked the last session off, published
    // by the bridge. The transparency Zac asked for on 29/07: five FYI
    // messages queued for Jacob and nothing on the hub showed it.
    if (ch && action === "queue" && GET) {
      try {
        const row = await db.prepare("SELECT v, updated FROM state WHERE k = ?")
          .bind(ch.statusKey + "_queue").first();
        if (!row) return json({ items: [] });
        return json({ ...JSON.parse(row.v), updated: row.updated });
      } catch {
        return json({ items: [] });
      }
    }

    // Decisions the bot cannot make alone. Reading is public; a bot with no
    // D1 requests table reads as "none open" rather than an error.
    if (ch && action === "requests" && GET) {
      if (!ch.requests) return json([]);
      const { results } = await db.prepare(
        `SELECT * FROM ${ch.requests} ORDER BY status = 'answered', id DESC`).all();
      return json(results);
    }

    // A human answering one of those decisions from the hub.
    if (ch && action === "requests" && POST) {
      if (!ch.requests) return json({ error: "This bot's requests are not in D1" }, 400);
      const b = await request.json().catch(() => ({}));
      const ref = clip(b.ref, 20);
      const answer = clip(b.answer, 2000).trim();
      if (!ref || !answer) return json({ error: "ref and answer required" }, 400);
      await db.prepare(
        `UPDATE ${ch.requests} SET status='answered', answer=?, answered_by=?, answered_at=? WHERE ref=?`)
        .bind(answer, clip(b.author || "team", 20), now(), ref).run();
      // The answer is also a message, so it reaches the bot through one channel.
      await db.prepare(
        `INSERT INTO ${ch.messages} (created, author, body, context) VALUES (?, ?, ?, ?)`)
        .bind(now(), clip(b.author || "team", 20), answer, ref).run();
      return json({ ok: true });
    }

    // The CRM overlay: the bot derives a state and a next action for every row
    // on its board; these rows are a human saying otherwise. Missing table
    // reads as "nobody has edited anything yet", which is true on a fresh
    // database and is not an error.
    if (ch && action === "pipeline" && GET) {
      if (!ch.pipeline) return json([]);
      try {
        const { results } = await db.prepare(
          `SELECT key, label, state, owner, next_action, next_date, note, notes, ` +
          `updated, updated_by FROM ${ch.pipeline} ORDER BY updated DESC LIMIT 800`).all();
        return json(results);
      } catch {
        // A database that predates next_date/notes still has a working board:
        // it just has no dates on it yet. Falling back is what turns the
        // migration into something the first write does rather than something
        // a human has to remember to run before the deploy.
        try {
          const { results } = await db.prepare(
            `SELECT key, label, state, owner, next_action, note, updated, updated_by ` +
            `FROM ${ch.pipeline} ORDER BY updated DESC LIMIT 800`).all();
          return json(results);
        } catch {
          return json([]);
        }
      }
    }

    if (ch && action === "pipeline" && POST) {
      if (!ch.pipeline) return json({ error: "This bot has no pipeline overlay" }, 400);
      const b = await request.json().catch(() => ({}));
      const key = clip(b.key, 120).trim();
      if (!key) return json({ error: "key required" }, 400);
      // Created here rather than in a migration so a hub deployed against a
      // database that predates this table still works on first use.
      await db.prepare(
        `CREATE TABLE IF NOT EXISTS ${ch.pipeline} (key TEXT PRIMARY KEY, label TEXT DEFAULT '', ` +
        `state TEXT DEFAULT '', owner TEXT DEFAULT '', next_action TEXT DEFAULT '', ` +
        `next_date TEXT DEFAULT '', note TEXT DEFAULT '', notes TEXT DEFAULT '[]', ` +
        `updated TEXT NOT NULL, updated_by TEXT DEFAULT 'team')`).run();
      // The two columns Adam asked for on 29/07 - a real date to call back on,
      // and a note that does not overwrite the last one. The table already
      // existed in production, so CREATE TABLE IF NOT EXISTS above will not add
      // them; ALTER does, and throws once the column is there. Swallowing that
      // is the migration.
      for (const [col, def] of [["next_date", "TEXT DEFAULT ''"],
                                ["notes", "TEXT DEFAULT '[]'"]]) {
        try {
          await db.prepare(`ALTER TABLE ${ch.pipeline} ADD COLUMN ${col} ${def}`).run();
        } catch { /* already there */ }
      }

      // A date is stored only if it IS one. Adam asking for "call back in two
      // months" turns into a date on the client; anything else this route is
      // handed is dropped rather than sorted as a string later.
      const nextDate = /^\d{4}-\d{2}-\d{2}$/.test(String(b.next_date || "").trim())
        ? String(b.next_date).trim() : "";

      // Append-only. "When we have called a client" is a history, not a field:
      // overwriting it loses the fact that we rang twice, which is exactly the
      // thing a chase needs to know. The newest entry stays in `note` as well,
      // so anything reading the old column still shows the latest word.
      const prev = await db.prepare(
        `SELECT notes, note FROM ${ch.pipeline} WHERE key = ?`).bind(key).first()
        .catch(() => null);
      let log = [];
      try { log = JSON.parse(prev?.notes || "[]"); } catch { log = []; }
      if (!Array.isArray(log)) log = [];
      // Typed into the wrong row, or typed twice. An append-only log with no
      // way back is not a thing to hand a Commercial Director - keyed on the
      // entry's own timestamp rather than its position, so a concurrent append
      // cannot make a delete land on the wrong line.
      if (b.drop_note) log = log.filter((n) => n.at !== b.drop_note);
      const entry = clip(b.add_note, 2000).trim();
      if (entry) {
        log.unshift({ at: now(), by: person(b.author), text: entry });
        log = log.slice(0, 60);
      }
      // `note` is the newest log entry, denormalised so a row can show its last
      // word without parsing the log. Once the log exists it is the only source
      // - otherwise deleting the last entry leaves it showing on the row.
      const latest = log.length ? log[0].text
        : (b.drop_note ? "" : (clip(b.note, 2000) || prev?.note || ""));

      await db.prepare(
        `INSERT INTO ${ch.pipeline} (key, label, state, owner, next_action, next_date, ` +
        `note, notes, updated, updated_by) ` +
        `VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(key) DO UPDATE SET ` +
        `label=excluded.label, state=excluded.state, owner=excluded.owner, ` +
        `next_action=excluded.next_action, next_date=excluded.next_date, ` +
        `note=excluded.note, notes=excluded.notes, ` +
        `updated=excluded.updated, updated_by=excluded.updated_by`)
        .bind(key, clip(b.label, 200), clip(b.state, 40), clip(b.owner, 40),
              clip(b.next_action, 600), nextDate, clip(latest, 2000),
              JSON.stringify(log), now(), person(b.author)).run();
      return json({ ok: true, next_date: nextDate, notes: log.length });
    }

    /* ---- Quote outcomes. Business-wide really, but Mary's board owns the
       recording UI, and this is the only place a win or loss gets recorded
       anywhere in the company. Deliberately public: the Won/Lost buttons on
       the hub have no key, so this must stay ABOVE the gate. ---- */
    if (route === "outcomes" && GET) {
      try {
        const { results } = await db.prepare(
          "SELECT id, created, job, result, value, winning_value, note, author FROM outcomes ORDER BY id DESC LIMIT 200").all();
        return json(results);
      } catch {
        return json([]);
      }
    }

    if (route === "outcomes" && POST) {
      const b = await request.json().catch(() => ({}));
      const job = clip(b.job, 200).trim();
      const result = ["won", "lost", "no-decision"].includes(b.result) ? b.result : "";
      if (!job || !result) return json({ error: "job and result are required" }, 400);
      const num = (v) => (v === null || v === undefined || v === "" || isNaN(Number(v)) ? null : Number(v));
      await db.prepare(
        "INSERT INTO outcomes (created, job, result, value, winning_value, note, author) VALUES (?, ?, ?, ?, ?, ?, ?)")
        .bind(now(), job, result, num(b.value), num(b.winning_value),
              clip(b.note, 1000), person(b.author)).run();
      return json({ ok: true });
    }

    // ---- Bot to bot. Readable by anyone; writing is bot-only (below). ----
    if (route === "botchat" && GET) {
      const { results } = await db.prepare(
        "SELECT id, created, sender, recipient, subject, body, in_reply_to, wants_reply, seen " +
        "FROM bot_chat ORDER BY id DESC LIMIT 100").all();
      return json(results);
    }

    /* ---------------- bot-only routes below this gate ---------------- */
    if (!env.MARY_API_KEY || request.headers.get("x-mary-key") !== env.MARY_API_KEY) {
      return json({ error: "Not found" }, 404);
    }

    // Ten messages per sender per hour, enforced HERE rather than in a prompt.
    // Enough for a real exchange - Jacob asks, Mary answers, he asks a
    // follow-up if her answer needs one - but a hard ceiling on two agents
    // talking each other in circles. A wall, not an instruction they can
    // reason their way around.
    if (route === "botchat" && POST) {
      const b = await request.json().catch(() => ({}));
      const sender = String(b.sender || "").toLowerCase();
      const body = clip(b.body, 4000).trim();
      if (!CHANNELS[sender]) return json({ error: "Unknown sender" }, 400);
      if (!body) return json({ error: "Empty message" }, 400);
      // Two bots means the other one; more than two will need an explicit
      // recipient on the message. Refuse rather than guess when that day comes.
      const others = Object.keys(CHANNELS).filter((k) => k !== sender);
      const recipient = String(b.recipient || (others.length === 1 ? others[0] : "")).toLowerCase();
      if (!CHANNELS[recipient] || recipient === sender) {
        return json({ error: "Say who it is for - more than one possible recipient" }, 400);
      }

      const HOURLY_LIMIT = 10;
      const since = new Date(Date.now() - 3600000).toISOString();
      const row = await db.prepare(
        "SELECT COUNT(*) AS n FROM bot_chat WHERE sender = ? AND created > ?")
        .bind(sender, since).first();
      if ((row?.n || 0) >= HOURLY_LIMIT) {
        return json({ error: "rate limited", limit: HOURLY_LIMIT,
                      sentThisHour: row.n,
                      hint: "You have said enough this hour. Carry on with your own work." }, 429);
      }
      await db.prepare(
        "INSERT INTO bot_chat (created, sender, recipient, subject, body, in_reply_to, wants_reply) " +
        "VALUES (?, ?, ?, ?, ?, ?, ?)")
        .bind(now(), sender, recipient, clip(b.subject, 140), body,
              b.in_reply_to || null, b.wants_reply ? 1 : 0).run();
      return json({ ok: true });
    }

    // Unseen messages addressed to me. Marking them seen is a separate call,
    // so a crashed session does not silently lose the message.
    if (route === "botchat/pending") {
      const who = new URL(request.url).searchParams.get("for") || "jacob";
      const { results } = await db.prepare(
        "SELECT id, created, sender, subject, body, in_reply_to, wants_reply " +
        "FROM bot_chat WHERE recipient = ? AND seen = 0 ORDER BY id").bind(who).all();
      return json(results);
    }

    if (route === "botchat/seen" && POST) {
      const b = await request.json().catch(() => ({}));
      for (const id of (b.ids || [])) {
        await db.prepare("UPDATE bot_chat SET seen = 1 WHERE id = ?").bind(parseInt(id, 10) || 0).run();
      }
      return json({ ok: true });
    }

    // Messages a human has left that the bot has not yet picked up.
    if (ch && action === "pending") {
      const { results } = await db.prepare(
        `SELECT id, created, author, body, context FROM ${ch.messages} ` +
        `WHERE ${ch.seen} = 0 AND author != ? ORDER BY id`).bind(botKey).all();
      return json(results);
    }

    // The bot answering back into its own thread.
    if (ch && action === "reply" && POST) {
      const b = await request.json().catch(() => ({}));
      const body = clip(b.body, 8000).trim();
      const replyTo = parseInt(b.in_reply_to, 10) || null;
      if (body) {
        await db.prepare(
          `INSERT INTO ${ch.messages} (created, author, body, context, in_reply_to, ${ch.seen}) ` +
          `VALUES (?, ?, ?, ?, ?, 1)`)
          .bind(now(), botKey, body, clip(b.context, 300), replyTo).run();
      }
      if (replyTo) {
        await db.prepare(`UPDATE ${ch.messages} SET ${ch.seen} = 1 WHERE id = ?`).bind(replyTo).run();
      }
      for (const id of (Array.isArray(b.mark_seen) ? b.mark_seen.slice(0, 50) : [])) {
        await db.prepare(`UPDATE ${ch.messages} SET ${ch.seen} = 1 WHERE id = ?`)
          .bind(parseInt(id, 10) || 0).run();
      }
      return json({ ok: true });
    }

    // The bot raising a question it cannot answer itself.
    if (ch && action === "ask" && POST) {
      if (!ch.requests) return json({ error: "This bot's requests are not in D1" }, 400);
      const b = await request.json().catch(() => ({}));
      const ref = clip(b.ref, 20);
      if (!ref || !b.title) return json({ error: "ref and title required" }, 400);
      await db.prepare(
        `INSERT INTO ${ch.requests} (created, ref, title, why, needs, options) ` +
        `VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(ref) DO UPDATE SET ` +
        `title=excluded.title, why=excluded.why, needs=excluded.needs, options=excluded.options`)
        .bind(now(), ref, clip(b.title, 300), clip(b.why, 2000),
              clip(b.needs, 2000), JSON.stringify(b.options || [])).run();
      return json({ ok: true });
    }

    if (ch && action === "queue" && POST) {
      const b = await request.json().catch(() => ({}));
      await db.prepare(
        "INSERT INTO state (k, v, updated) VALUES (?, ?, ?) " +
        "ON CONFLICT(k) DO UPDATE SET v = excluded.v, updated = excluded.updated")
        .bind(ch.statusKey + "_queue", JSON.stringify(b).slice(0, 90000), now()).run();
      return json({ ok: true });
    }

    if (ch && action === "status" && POST) {
      const b = await request.json().catch(() => ({}));
      await db.prepare(
        "INSERT INTO state (k, v, updated) VALUES (?, ?, ?) " +
        "ON CONFLICT(k) DO UPDATE SET v = excluded.v, updated = excluded.updated")
        .bind(ch.statusKey, JSON.stringify(b).slice(0, 2000), now()).run();
      return json({ ok: true });
    }

    if (ch && action === "activity" && POST) {
      const b = await request.json().catch(() => ({}));
      const events = Array.isArray(b.events) ? b.events.slice(-80) : [];
      const payload = JSON.stringify({ chat: b.chat || null, title: b.title || "", events });
      await db.prepare(
        "INSERT INTO state (k, v, updated) VALUES (?, ?, ?) " +
        "ON CONFLICT(k) DO UPDATE SET v = excluded.v, updated = excluded.updated")
        .bind(ch.activityKey, payload.slice(0, 90000), now()).run();
      return json({ ok: true });
    }

    return json({ error: "Not found" }, 404);
  } catch (error) {
    return json({ error: error.message || "Something went wrong" }, 500);
  }
}
