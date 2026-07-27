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
