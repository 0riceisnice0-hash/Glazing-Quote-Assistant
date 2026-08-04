-- GLASSHOUSE - the record. One database, three personas, every fact attributable.
--
-- Design rules, learned the hard way in the system this replaces:
--   * Values are EX VAT, always. De-VAT on the way in, never on the way out.
--   * Every write carries an author. "Who moved this to lost, on what evidence"
--     must be answerable months later.
--   * The event stream is append-only. State tables hold NOW; events hold HOW.
--   * position fields hold the distilled prose a worker seed needs - they are
--     the successor of the old data/jobs/*.md files, and they are capped by the
--     API (8,000 chars), because an uncapped memory file is a tax on every
--     future session.

CREATE TABLE IF NOT EXISTS company (
  key            TEXT PRIMARY KEY,           -- slug: 'stepnell'
  name           TEXT NOT NULL,
  relationship   TEXT NOT NULL DEFAULT 'prospect',  -- prospect|quoted|won|supplier|ruled_out
  lifetime_value REAL,                       -- ex VAT, what they have paid us
  payment_terms  TEXT,
  position       TEXT DEFAULT '',            -- distilled: who they are, how to work with them
  meta_json      TEXT DEFAULT '{}',
  created        TEXT NOT NULL DEFAULT (datetime('now')),
  updated        TEXT NOT NULL DEFAULT (datetime('now')),
  updated_by     TEXT NOT NULL DEFAULT 'system'
);

CREATE TABLE IF NOT EXISTS contact (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  company_key TEXT NOT NULL,
  name        TEXT,
  email       TEXT,
  phone       TEXT,
  role        TEXT,
  notes       TEXT DEFAULT '',
  UNIQUE(company_key, email)
);

CREATE TABLE IF NOT EXISTS lead (
  key              TEXT PRIMARY KEY,         -- slug: 'filwood'
  company_key      TEXT NOT NULL DEFAULT 'unknown',
  title            TEXT NOT NULL,
  stage            TEXT NOT NULL DEFAULT 'new',
  -- new|acknowledged|materials_out|awaiting_costs|quote_ready|pre_quote_call|
  -- quote_sent|follow_up|final_follow_up|closed
  owner            TEXT NOT NULL DEFAULT 'mary',   -- mary until quote_sent, then jacob
  value            REAL,                     -- ex VAT
  deadline         TEXT,                     -- tender return date
  award_due        TEXT,                     -- when OUR CLIENT hears if THEY won
  next_action      TEXT,
  next_action_date TEXT,
  outcome          TEXT,                     -- won|lost|no_bid|dead, set at closed
  outcome_why      TEXT,
  position         TEXT DEFAULT '',          -- distilled state of play for a worker seed
  meta_json        TEXT DEFAULT '{}',
  created          TEXT NOT NULL DEFAULT (datetime('now')),
  updated          TEXT NOT NULL DEFAULT (datetime('now')),
  updated_by       TEXT NOT NULL DEFAULT 'system'
);

CREATE TABLE IF NOT EXISTS quote (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_key  TEXT NOT NULL,
  revision  INTEGER NOT NULL DEFAULT 1,
  value     REAL,                            -- ex VAT
  status    TEXT DEFAULT 'draft',            -- draft|checked|issued|superseded
  issued_at TEXT,
  basis     TEXT DEFAULT '',                 -- what the price is built on
  file_path TEXT DEFAULT '',
  UNIQUE(lead_key, revision)
);

CREATE TABLE IF NOT EXISTS contract (
  key         TEXT PRIMARY KEY,
  lead_key    TEXT,
  company_key TEXT NOT NULL DEFAULT 'unknown',
  title       TEXT NOT NULL,
  po_ref      TEXT,
  value       REAL,                          -- ex VAT
  site_date   TEXT,                          -- installation date the steps work back from
  status      TEXT NOT NULL DEFAULT 'live',  -- live|complete|invoiced|paid|on_hold
  position    TEXT DEFAULT '',
  meta_json   TEXT DEFAULT '{}',
  created     TEXT NOT NULL DEFAULT (datetime('now')),
  updated     TEXT NOT NULL DEFAULT (datetime('now')),
  updated_by  TEXT NOT NULL DEFAULT 'system'
);

-- Joseph's checklist. Seeded from the 12-step template when a contract opens;
-- most steps are ticked CLERICALLY by intake when the confirming email arrives.
CREATE TABLE IF NOT EXISTS step (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  contract_key TEXT NOT NULL,
  n            INTEGER NOT NULL,
  label        TEXT NOT NULL,
  detail       TEXT DEFAULT '',              -- WHAT to order, not just that it is due
  due          TEXT,
  done_at      TEXT,
  done_by      TEXT,
  UNIQUE(contract_key, n)
);

-- THE WORK QUEUE. Replaces three directories of JSON files. Intake writes,
-- dispatch reads, finish closes. Attachments stay on the local disk; the
-- payload carries their paths.
CREATE TABLE IF NOT EXISTS task (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  assignee     TEXT NOT NULL,                -- mary|jacob|joseph
  entity_type  TEXT DEFAULT '',              -- lead|company|contract|'' (desk)
  entity_key   TEXT DEFAULT '',
  kind         TEXT NOT NULL DEFAULT 'email',-- email|hub|handover|agenda|chore
  title        TEXT NOT NULL,
  body         TEXT DEFAULT '',
  payload_json TEXT DEFAULT '{}',            -- {from,subject,received,body,attachments[],mailbox,...}
  needs        TEXT DEFAULT '',              -- 'pricing' upgrades the model
  priority     INTEGER NOT NULL DEFAULT 5,   -- 1 urgent .. 9 idle
  status       TEXT NOT NULL DEFAULT 'open', -- open|working|done|dropped
  created      TEXT NOT NULL DEFAULT (datetime('now')),
  created_by   TEXT NOT NULL DEFAULT 'intake',
  done_at      TEXT,
  done_by      TEXT,
  result       TEXT DEFAULT ''               -- one line: what happened
);
CREATE INDEX IF NOT EXISTS idx_task_open ON task(status, assignee, priority);

-- Append-only. The ledger. Everything that happens, by anyone, lands here.
CREATE TABLE IF NOT EXISTS event (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  ts          TEXT NOT NULL DEFAULT (datetime('now')),
  author      TEXT NOT NULL,                 -- mary|jacob|joseph|intake|zac|adam|hub
  entity_type TEXT DEFAULT '',
  entity_key  TEXT DEFAULT '',
  kind        TEXT NOT NULL,                 -- mail_in|mail_out|note|stage|quote_issued|task_done|catch|...
  body        TEXT NOT NULL,
  ref         TEXT DEFAULT ''                -- message id / file path / task id
);
CREATE INDEX IF NOT EXISTS idx_event_entity ON event(entity_type, entity_key, id);
CREATE INDEX IF NOT EXISTS idx_event_ts ON event(ts);

-- The human channel. Zac/Adam write to a persona; the persona answers through
-- finish. Posting from the hub UI requires the team PIN - that is the sender
-- verification, kept from the old hub because it worked.
CREATE TABLE IF NOT EXISTS message (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  ts        TEXT NOT NULL DEFAULT (datetime('now')),
  author    TEXT NOT NULL,                   -- zac|adam|mary|jacob|joseph
  persona   TEXT NOT NULL,                   -- which desk this belongs to
  body      TEXT NOT NULL,
  reply_to  INTEGER,
  read_at   TEXT                             -- set when a dispatch delivers it
);

-- "Needs a human." A persona raises one only for what a human alone can answer:
-- a price, a date, what a client meant. Answered in place on the hub.
CREATE TABLE IF NOT EXISTS decision (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  ts          TEXT NOT NULL DEFAULT (datetime('now')),
  raised_by   TEXT NOT NULL,
  entity_type TEXT DEFAULT '',
  entity_key  TEXT DEFAULT '',
  question    TEXT NOT NULL,
  context     TEXT DEFAULT '',
  status      TEXT NOT NULL DEFAULT 'open',  -- open|answered|withdrawn
  answer      TEXT,
  answered_by TEXT,
  answered_at TEXT
);

CREATE TABLE IF NOT EXISTS invoice (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  contract_key TEXT NOT NULL,
  ref          TEXT,
  value        REAL,                         -- ex VAT
  due          TEXT,
  status       TEXT NOT NULL DEFAULT 'draft',-- draft|checked|sent|paid|overdue
  paid_at      TEXT
);

-- Real cost, measured the right way: context re-read per call, deduped by
-- request. Written by dispatch at the end of every session.
CREATE TABLE IF NOT EXISTS usage (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  ts             TEXT NOT NULL DEFAULT (datetime('now')),
  persona        TEXT NOT NULL,
  entity_key     TEXT DEFAULT '',
  session_id     TEXT DEFAULT '',
  model          TEXT DEFAULT '',
  calls          INTEGER DEFAULT 0,
  context_tokens INTEGER DEFAULT 0,
  output_tokens  INTEGER DEFAULT 0,
  seconds        INTEGER DEFAULT 0
);

-- What the front desk threw away, and why. A wrong call has to be findable.
CREATE TABLE IF NOT EXISTS noise (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  ts      TEXT NOT NULL DEFAULT (datetime('now')),
  sender  TEXT DEFAULT '',
  subject TEXT DEFAULT '',
  why     TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS setting (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL DEFAULT ''
);
