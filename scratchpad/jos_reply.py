import json, os, urllib.request

BODY = """Built it. Seven tabs, and the shape is: the four Work tabs answer a
different question each, and none of them repeats Contracts - a won job is the
company's record and all three of us read it, so what is mine is the programme
on top of it.

**Today** - what is going to go wrong, worst first, each with the move that
answers it. Six things on it right now, four of them red.

**The twelve steps** - your checklist. The whole portfolio as a grid first, four
jobs across twelve columns, so I can see it in one look; then every job in full
with what each tick was inferred from underneath it. An empty box is a dashed
outline, not a blank, because on these four jobs it means UNDATED and not "on
time" - nothing can be late against a date that does not exist.

**Waiting on** - the four questions on you and Adam, oldest first, and the four
jobs stalled for want of a site date with what is already bought sitting behind
them.

**Money** - where the value is, and the three questions blocking the back half
(D2 the chase ladder, D3 applications vs final invoices, D4 where the figure
comes from with variations). I left the space for them and did not invent a
ladder to fill it.

**What I changed** - the audit trail, so a wrong tick can be understood rather
than quietly corrected.

Two things I changed in the code rather than working around:

1. **A new API route, `/api/crm/programme`.** Neither existing route could
   answer my question in one call, and worse, both would have lied. 33 contracts
   read "live" - 29 of them are rows seeded from the AdminBase export with no PO
   and nobody running them. My board says "4 jobs I am running, 29 more rows read
   live and nobody is running them" rather than putting 33 on a tile.

2. **Your side panel was lying about me.** My messages and requests were not on
   the hub's 10-second refresh - Mary's and Jacob's were - so a reply written to
   me left the badge on my card frozen at whatever it was when you loaded the
   page. Added, along with the programme, which only refetches while one of my
   work pages is open.

The number I built the board around is **"soonest possible"**. Every one of the
twelve steps counts back from the day we go on site, so the longest lead time
still outstanding IS the earliest we could be on site. On a job with a date it
tells me whether the date survives before the week it is missed in; on these
four, which have no date, it is the only honest thing to put in the column.
Stoke Park is 2026-10-27 on today's outstanding work. It is arithmetic off the
assumed lead times in crm_contract.py, and it says so on the page every time it
appears - those numbers came from the shape of the trade, not from anything
Fenster has measured.

And the board earned its keep in the first ten minutes: it showed Stoke Park at
12 weeks outstanding when Manor Lodge and Towcester were at 11, which was step 1
unticked on a job whose PO I had already recorded - AdminBase 3475, dated
11/06/2026, identical evidence to the two I had ticked. Fixed, with the reason
on the tick.

What is still true and is not a dashboard problem: **all four live jobs have no
site date**, GBP 275,000 of them, and Stoke Park's frames and glass are already
on order against it. That is JOE-3 and it is the one that costs money."""

import sys
sys.path.insert(0, 'scripts')
import joseph_bridge as jb
cfg = jb.env()

url = cfg.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev") + "/api/joseph/reply"
req = urllib.request.Request(url, method="POST",
    data=json.dumps({"body": BODY, "in_reply_to": 2}).encode())
req.add_header("content-type", "application/json")
req.add_header("x-mary-key", cfg.get("MARY_API_KEY", ""))
# Cloudflare 403s the default Python-urllib agent; the bridge sets one too.
req.add_header("user-agent", "JosephBridge/1.0")
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.status, r.read().decode())

