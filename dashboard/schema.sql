CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TEXT NOT NULL,
  author TEXT NOT NULL,
  body TEXT NOT NULL,
  context TEXT DEFAULT '',
  in_reply_to INTEGER,
  seen_by_mary INTEGER DEFAULT 0
);

-- Small key/value side table. Today it holds one row, 'mary': what the bridge
-- is doing right now, so the hub can say "working on Grange Hill" instead of
-- "she'll pick this up within 15 minutes".
CREATE TABLE IF NOT EXISTS state (
  k TEXT PRIMARY KEY,
  v TEXT NOT NULL,
  updated TEXT NOT NULL
);

-- Did the quote win? Nothing else records this: the Estimating Log's W/L
-- column is 93% empty, so there is no history to mine. One click on the hub
-- when a result comes in is what builds the dataset from here on.
CREATE TABLE IF NOT EXISTS outcomes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TEXT NOT NULL,
  job TEXT NOT NULL,
  result TEXT NOT NULL,          -- won | lost | no-decision
  value REAL,                    -- our quoted value, if known
  winning_value REAL,            -- what it went for, if they tell us
  note TEXT DEFAULT '',
  author TEXT DEFAULT 'team'
);

-- ===================================================================
-- Jacob Wright. Separate tables from Mary's on purpose: her `messages`
-- table is hers, and nothing here can affect it.
--
-- CONVENTION for every bot from Jacob onward: `<bot>_messages`,
-- `<bot>_requests`, and optionally `<bot>_pipeline`, in these shapes.
-- Mary's unprefixed `messages` predates the convention and stays as the
-- documented exception (the API's CHANNELS registry maps her to it).
-- Adding a bot = copy Jacob's three tables under the new prefix; the file
-- is all IF NOT EXISTS, so applying it to production never touches data.
-- ===================================================================

-- Humans <-> Jacob, same shape as Mary's messages.
CREATE TABLE IF NOT EXISTS jacob_messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TEXT NOT NULL,
  author TEXT NOT NULL,             -- zac | adam | team | jacob
  body TEXT NOT NULL,
  context TEXT DEFAULT '',
  in_reply_to INTEGER,
  seen_by_jacob INTEGER DEFAULT 0
);

-- Things Jacob cannot decide alone. He raises one instead of guessing, and
-- carries on with everything the answer does not block.
CREATE TABLE IF NOT EXISTS jacob_requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TEXT NOT NULL,
  ref TEXT NOT NULL UNIQUE,         -- JAC-1, JAC-2...
  title TEXT NOT NULL,
  why TEXT DEFAULT '',              -- why he is blocked
  needs TEXT DEFAULT '',            -- exactly what he needs back
  options TEXT DEFAULT '[]',        -- JSON array of quick answers
  status TEXT DEFAULT 'open',       -- open | answered
  answer TEXT DEFAULT '',
  answered_by TEXT DEFAULT '',
  answered_at TEXT
);

-- The CRM overlay on Jacob's board. His generator derives a state and a next
-- action for every company, thread and lead from the evidence; this table is
-- where a human overrides it - moves something to "dead", puts Adam's name on
-- it, or ticks it done. Keyed by the stable key Jacob emits (thread:..,
-- co:.., lead:..), so a rebuild of jacob-data.js never orphans an edit.
CREATE TABLE IF NOT EXISTS jacob_pipeline (
  key TEXT PRIMARY KEY,
  label TEXT DEFAULT '',            -- what it was called when it was edited
  state TEXT DEFAULT '',            -- overrides the derived state; '' = leave it
  owner TEXT DEFAULT '',            -- who does the next thing
  next_action TEXT DEFAULT '',
  next_date TEXT DEFAULT '',        -- ISO date to do it on. Adam, 29/07: "they
                                    -- said call back in 2 months" needs a date,
                                    -- not a sentence, or nothing can sort by it
  note TEXT DEFAULT '',             -- the LATEST note, denormalised out of `notes`
  notes TEXT DEFAULT '[]',          -- the call log: [{at, by, text}], newest first,
                                    -- append-only. Overwriting loses the fact that
                                    -- we rang twice, which is what a chase needs
  updated TEXT NOT NULL,
  updated_by TEXT DEFAULT 'team'
);
-- These two columns arrived after the table was live, so the API adds them with
-- ALTER on first write and swallows the "duplicate column" error. Applying this
-- file to a fresh database gets them from the CREATE above; applying it to
-- production is a no-op, which is the point of the IF NOT EXISTS.

-- Bot to bot. Jacob knows what is being quoted; Mary knows who is buying.
-- Neither is obliged to reply - a message that needs no answer gets none,
-- which is the main thing stopping two agents talking each other in circles.
-- The API also refuses more than one message per sender per hour.
CREATE TABLE IF NOT EXISTS bot_chat (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TEXT NOT NULL,
  sender TEXT NOT NULL,             -- jacob | mary
  recipient TEXT NOT NULL,          -- mary | jacob
  subject TEXT DEFAULT '',
  body TEXT NOT NULL,
  in_reply_to INTEGER,
  wants_reply INTEGER DEFAULT 0,    -- 0 = FYI, do not answer
  seen INTEGER DEFAULT 0
);
