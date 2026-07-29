# Adam Butcher - how he reads, decides, and replies

Commercial Director. The person almost everything Mary produces is for. This file is
distilled from every reply he has sent (hub + email, ledger-backed) and it is LOADED
CONTEXT for every session: write for the man described here, not for a general reader.
When he teaches something new, add it here at close-out with the date - and delete
anything he contradicts. Keep this file under 120 lines.

## How he reads

- **On his phone, between other things.** One screen is the budget. He said "this word
  count is insane. I will not be reading this" three times in one evening (REQ-9, -15,
  -22, 28/07) about requests that buried the decision under the briefing.
- **Bullets, not prose.** "Send me an email with the bullet points of the other errors"
  (REQ-12). When he wants detail, he asks for exactly the list - never the essay.
- **Lead with the thing.** His own emails are two to five lines: instruction first,
  reason only if needed ("We've missed the deadline on this, it was 17th July. Can you
  please send me a list of all current outstanding tenders...").
- **Four words can be a whole reply.** "It still says uPVC..." means: not fixed, go
  again, don't come back until it is.
- **He answers direct questions and ignores narration.** In the 42h to 29/07: 33 sends,
  4 replies - and every reply was to an error, a decision, or a question he was asked.
  Activity reports got silence. Silence is not consent; it is the bin.

## How he decides

- **By precedent.** "If you look at the large tender we did for Brandon Estate (for
  Elkins I believe) then you will see we included a cost for removal of frames" (28/07).
  Bring him the comparable, not the abstraction - he trusts jobs over arguments.
- **Deadlines outrank everything.** "It's critical that we are hitting deadlines... if
  there's any issues holding you up please let me know so we can work out a solution"
  (24/07). A slipped date is ALWAYS worth an interruption; a met one is never news.
- **Commercially pragmatic, small margins matter.** Adds a 2.5% MCD to close a deal,
  applies a GBP 100 goodwill discount, moves EPDM/mastic from optional into the main
  quote so the offer reads clean. Expects the quote to carry drawings when they exist.
- **Phone for nuance.** "Give me a call back" - when a thing needs discussion he moves
  it OFF email. Mary cannot call, so the equivalent is: give him the decision points so
  he can make the call himself.
- **He corrects course instantly on new facts** (Target rang about the door; reprice
  went out within the hour). Stale information is worse to him than no information.

## Standing decisions (do not re-raise; the full settled list is `mary_recall --settled`)

- **Strip-out**: addressed by email 28/07 21:01 with the Brandon Estate precedent.
  Closed. Raising it again got "I have already addressed this with you."
- **Suppliers get deadlines** on every RFQ - "as I have said before" (24/07).
- **Timestamps in UK time** on everything he reads (28/07).
- **The handover rule** (28/07): a job is Mary's while it is being priced, Jacob's the
  moment the quote goes out.
- **Concise or unread** (28/07, three times): title = the decision; options = the
  answers; evidence lives in the job file, not the request.
- **No deadline given = a DEFAULT of 7 days, labelled as one** (29/07, dashmsg-93): *"If we
  have not been given a deadline, we should set a week as default but note that it's a
  default deadline. Then one can be provided at a later date if required."* Implemented in
  `mary_dashboard.py` (fills blanks, writes back, sets `deadline_is_default`). Setting a real
  date means overwriting `deadline` AND dropping that flag. He does NOT want blanks - but a
  default must never read like a client's return date.
- **07:45 morning update** is where non-urgent findings belong. He reads it.

## Before interrupting him

Run `python scripts\mary_send.py --check --subject "..."` - it shows what has already
gone today, the last send on this job, whether the topic is settled, and his reply
rate. Then apply his own test: does he DO something different because this arrived?
Errors and moved deadlines: always. A direct answer to his question: always, once,
complete. Everything else: the morning update.

**A moving number is one email when it settles** (29/07: Redditch got five as each
supplier answer landed; two Grange Hill sends eight minutes apart, the second reversing
the first). If inputs are still inbound, either wait, or send one line: "number moving,
do not act on any figure until I confirm." A chain of corrections is worse than either.
