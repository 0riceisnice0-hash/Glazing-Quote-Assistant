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
