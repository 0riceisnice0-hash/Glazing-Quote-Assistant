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

-- ===================================================================
-- THE CRM (P3, 03/08/2026). One record of the commercial world that all
-- three bots read and write, so a lead is logged once and never re-keyed.
--
-- WHY IT IS HERE AND NOT IN ADMINBASE. Zac, 03/08: run them in parallel.
-- But AdminBase has no API and no live feed - jacob_adminbase.py reads a CSV
-- Adam exported by hand on 28/07 and the promised feed never arrived, so
-- "parallel" cannot mean two systems kept in step by typing. The hub holds
-- the record; scripts/crm_export.py carries it back the other way.
--
-- SHAPE. Text primary keys, because every bot already works in slugs
-- (stepnell, gordon-court) and the files on disk reference them - an
-- autoincrement id would need a lookup table on both sides for nothing.
-- Every row carries updated_by, so any state change is attributable to a
-- named bot or a named person. All IF NOT EXISTS: applying this to
-- production never touches existing data.
--
-- Adam's test decides which table a thing belongs in: is it a job you are
-- quoting for (crm_lead, Jacob) or a job you have won (crm_contract, Joseph)?
-- ===================================================================

CREATE TABLE IF NOT EXISTS crm_company (
  key TEXT PRIMARY KEY,             -- slug: stepnell, chigwell-london-plc
  name TEXT NOT NULL,               -- trading name as they write it
  domains TEXT DEFAULT '[]',        -- JSON array - how their email is recognised
  relationship TEXT DEFAULT 'unknown', -- won | quoted | known | cold | unknown
  postcode TEXT DEFAULT '',
  lifetime_value REAL DEFAULT 0,    -- what they have actually paid us
  payment_terms TEXT DEFAULT '',    -- "30 days end of month" - Joseph learns these
  last_contact TEXT DEFAULT '',
  created TEXT NOT NULL,
  updated TEXT NOT NULL,
  updated_by TEXT DEFAULT 'bot'
);

CREATE TABLE IF NOT EXISTS crm_contact (
  id TEXT PRIMARY KEY,              -- company key + ':' + email
  company_key TEXT NOT NULL,
  name TEXT DEFAULT '',
  email TEXT DEFAULT '',
  phone TEXT DEFAULT '',
  role TEXT DEFAULT '',
  last_contact TEXT DEFAULT '',
  created TEXT NOT NULL,
  updated TEXT NOT NULL,
  updated_by TEXT DEFAULT 'bot'
);

-- A job we are quoting for. Jacob owns this from enquiry to closed, and it is
-- the exact pipeline Adam walked through on the AdminBase leads board: the
-- first half is estimating's, the second half is his.
CREATE TABLE IF NOT EXISTS crm_lead (
  key TEXT PRIMARY KEY,             -- slug, matches Mary's job key where one exists
  company_key TEXT NOT NULL,
  title TEXT NOT NULL,
  site TEXT DEFAULT '',
  postcode TEXT DEFAULT '',
  source TEXT DEFAULT '',           -- mailbox | adminbase | contracts-finder | dormant
  -- new -> acknowledged -> materials_out -> awaiting_costs -> quote_ready
  -- -> pre_quote_call -> quote_sent -> follow_up -> final_follow_up -> closed
  stage TEXT DEFAULT 'new',
  owner TEXT DEFAULT 'jacob',       -- jacob | mary | adam
  value REAL,                       -- ex VAT, ALWAYS. AdminBase's is inc VAT
  deadline TEXT DEFAULT '',         -- our return date
  award_due TEXT DEFAULT '',        -- when THEY hear if they won - the call date
  next_action TEXT DEFAULT '',
  next_action_date TEXT DEFAULT '',
  outcome TEXT DEFAULT '',          -- won | lost | no-decision | ''
  adminbase_ref TEXT DEFAULT '',    -- so the export can find its row again
  created TEXT NOT NULL,
  updated TEXT NOT NULL,
  updated_by TEXT DEFAULT 'bot'
);

-- What Mary priced and what actually left the building. Separate from the lead
-- because a lead can be quoted more than once, and a re-quote is the thing that
-- made AdminBase read "98 days silent" on a quote sent the previous afternoon.
CREATE TABLE IF NOT EXISTS crm_quote (
  id TEXT PRIMARY KEY,              -- lead key + ':' + revision
  lead_key TEXT NOT NULL,
  revision INTEGER DEFAULT 1,
  value REAL,                       -- ex VAT
  basis TEXT DEFAULT '',            -- supplier-backed | benchmark | provisional
  status TEXT DEFAULT 'draft',      -- draft | to_check | approved | issued | superseded
  issued_at TEXT DEFAULT '',        -- VERIFIED send, not the CRM's guess
  issued_by TEXT DEFAULT '',
  issued_to TEXT DEFAULT '',
  document TEXT DEFAULT '',         -- path to the pack that went
  created TEXT NOT NULL,
  updated TEXT NOT NULL,
  updated_by TEXT DEFAULT 'bot'
);

-- A job we have WON. Joseph's half; the 12-step checklist lives in crm_task
-- against this row. Created when a purchase order lands, which is the moment
-- AdminBase converts a lead into a contract.
CREATE TABLE IF NOT EXISTS crm_contract (
  key TEXT PRIMARY KEY,
  lead_key TEXT DEFAULT '',         -- where it came from, if we have it
  company_key TEXT NOT NULL,
  title TEXT NOT NULL,
  value REAL,                       -- ex VAT
  po_ref TEXT DEFAULT '',
  site_date TEXT DEFAULT '',        -- every deadline works backwards from this
  status TEXT DEFAULT 'live',       -- live | complete | invoiced | paid
  created TEXT NOT NULL,
  updated TEXT NOT NULL,
  updated_by TEXT DEFAULT 'bot'
);

-- The checklist, for a lead or a contract. Joseph maintains his own from the
-- email traffic (Zac, 03/08: "the bot manages it") - every AdminBase box being
-- red is what happens when a checklist waits on human data entry.
CREATE TABLE IF NOT EXISTS crm_task (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_type TEXT NOT NULL,        -- lead | contract
  entity_key TEXT NOT NULL,
  step TEXT NOT NULL,               -- order_glass, submit_designs, send_rams
  label TEXT NOT NULL,
  due TEXT DEFAULT '',
  done_at TEXT DEFAULT '',
  done_by TEXT DEFAULT '',
  detail TEXT DEFAULT '',           -- WHAT to order, not just that it is due
  created TEXT NOT NULL,
  updated TEXT NOT NULL,
  updated_by TEXT DEFAULT 'bot'
);

-- Everything anyone knows, attached to anything. Append-only: overwriting a
-- note loses the fact that we rang twice, which is exactly what a chase needs.
CREATE TABLE IF NOT EXISTS crm_note (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_type TEXT NOT NULL,        -- company | contact | lead | quote | contract
  entity_key TEXT NOT NULL,
  body TEXT NOT NULL,
  source TEXT DEFAULT 'bot',        -- email | call | hub | bot
  source_ref TEXT DEFAULT '',       -- message id, ledger ref, whatever proves it
  author TEXT NOT NULL,             -- jacob | mary | joseph | adam | zac
  created TEXT NOT NULL
);

-- Money out and money in. Joseph's, and deliberately thin until P5 settles
-- what an invoice actually is here - applications and final accounts are
-- different animals on commercial work and Adam has not ruled on it yet (D3).
CREATE TABLE IF NOT EXISTS crm_invoice (
  id TEXT PRIMARY KEY,
  contract_key TEXT NOT NULL,
  kind TEXT DEFAULT 'invoice',      -- invoice | application
  value REAL,
  issued_at TEXT DEFAULT '',
  due_at TEXT DEFAULT '',
  paid_at TEXT DEFAULT '',
  chase_stage INTEGER DEFAULT 0,    -- 0-6; 6 is formal escalation at day 75
  created TEXT NOT NULL,
  updated TEXT NOT NULL,
  updated_by TEXT DEFAULT 'bot'
);

-- Who changed what. The meeting's requirement that every state change is
-- attributable, and the thing that lets a human see a bot's reasoning after
-- the fact rather than only its result.
CREATE TABLE IF NOT EXISTS crm_event (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_type TEXT NOT NULL,
  entity_key TEXT NOT NULL,
  field TEXT DEFAULT '',
  was TEXT DEFAULT '',
  now TEXT DEFAULT '',
  why TEXT DEFAULT '',
  author TEXT NOT NULL,
  created TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_crm_lead_company ON crm_lead(company_key);
CREATE INDEX IF NOT EXISTS idx_crm_lead_stage ON crm_lead(stage);
CREATE INDEX IF NOT EXISTS idx_crm_lead_next ON crm_lead(next_action_date);
CREATE INDEX IF NOT EXISTS idx_crm_quote_lead ON crm_quote(lead_key);
CREATE INDEX IF NOT EXISTS idx_crm_contact_company ON crm_contact(company_key);
CREATE INDEX IF NOT EXISTS idx_crm_note_entity ON crm_note(entity_type, entity_key);
CREATE INDEX IF NOT EXISTS idx_crm_task_entity ON crm_task(entity_type, entity_key);
CREATE INDEX IF NOT EXISTS idx_crm_task_due ON crm_task(due);
