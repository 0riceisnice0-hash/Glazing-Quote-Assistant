# -*- coding: utf-8 -*-
"""Standing work, so an empty inbox is not an empty day.

Jacob did 7 things on 05/08 against Mary's 71 and Joseph's 61 - not because he
is worse, but because he only ever gets work when mail arrives addressed to
business development. Seven quotes were sitting out for decision and nobody
was chasing them, because chasing is not an email that lands, it is a date
that passes.

So: at a few fixed times a day, a desk with an EMPTY queue is given its
standing brief. Fixed times, not "every quiet hour" - the old system generated
work for itself around the clock and burned a night doing it.
"""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
import record

HOURS = (9, 13, 16)      # local time; only fires if the queue is empty

BRIEFS = {
    "mary": """STANDING WORK - your queue is empty, so pick the most valuable thing.
In order:
1. Any lead at quote_ready or pre_quote_call - is the quote actually built and
   checked, or is it waiting on you?
2. Leads with no value on the record. A lead nobody has priced is the one thing
   only you can fix. Use `python core\\rates.py --lookup "<category>"` for a
   benchmark and `python core\\mail.py --search "<job>"` for the supplier quotes
   that already exist. Supplier-backed beats benchmark; say which you used.
3. Deadlines inside the next fortnight with no price behind them - flag them
   before they are a week away, not after.
4. Any quote you have issued where the real cost has since landed: score it
   with `python core\\rates.py --score <lead> --mine <yours> --actual <real>`.
   That is the only thing that makes your accuracy a number instead of a
   feeling.""",

    "jacob": """STANDING WORK - your queue is empty, and an empty inbox is not an
empty day. This is most of your job; it never arrives as an email.
In order:
1. TODAY'S CALLS: every lead whose next_action_date is today or past. Work out
   what the next step actually is and draft it. Then set the NEXT date - a
   chase with no next date disappears.
2. Quotes issued and gone quiet. `python core\\mail.py --search "<client>"` will
   tell you whether they have replied and we missed it, before you chase
   someone who already answered.
3. Award dates: where a client told us when THEY hear, put it on the lead.
4. Company positions - 150 of 170 companies have none. Start with the ones with
   open work: who they are, who answers, how to approach them.
5. Outcomes. Anything decided and not recorded is data the business loses for
   good.""",

    "joseph": """STANDING WORK - your queue is empty. Work the contracts, not the
inbox.
In order:
1. Any live contract with NO SITE DATE. Everything else hangs off it. Search
   the mail for it before raising a decision - `python core\\mail.py --search`.
2. Steps due or overdue against a site date, worked backwards.
3. Steps with no `detail`. "Order glass" is half a task; what glass, what
   sizes, which supplier.
4. Anything delivered or completed where no invoice has been raised.
Remember the line: a job being QUOTED is not yours. If a task looks like
pricing a tender, hand it back rather than working it.""",
}


def due_now(state, now=None):
    """Which agenda hour we are in, if any, and not already done today."""
    now = now or dt.datetime.now()
    if now.hour not in HOURS:
        return None
    stamp = "%s-%02d" % (now.date().isoformat(), now.hour)
    return None if state.get("last") == stamp else stamp


PROJECTS = {
    "pricing": ("Work on the pricing engine", """PROJECT WORK - keep at this until it is measurably better.

The goal, in Zac's words: get your pricing as close to 1:1 with what Fenster
actually sends out. Not a benchmark, not a guess - the real quotes.

1. MEASURE FIRST so you can tell whether anything you do helps.
   `python scripts\\mary_backtest.py --loo` gives mean absolute error, median
   and bias, leave-one-job-out. Write the numbers down before you touch
   anything, then again after.
2. GROW THE CORPUS. You found 79 trustworthy sent quotes but only 30 reach the
   backtest. Work out why the other 49 are dropped and fix the reader if that
   is what it takes - you own this repo, so change the code, test it, commit it.
3. GO AFTER THE OUTLIERS. Take the worst-scoring jobs one at a time, find the
   real quote in the mail (`python core\\mail.py --search "<job>"`) and work out
   WHY the engine disagreed. A single wrong rule usually explains several.
4. RECORD IT. `python core\\rates.py --score <lead> --mine <x> --actual <y>` for
   anything you verify against a real figure.

Close out with the before-and-after numbers in your finish message. If you run
low on calls, stop, save what you learned, and say what you would do next -
this project comes back to you until the clock runs out."""),

    "leads": ("Find leads", """PROJECT WORK - go and find business. This is the half
of your job that never arrives as an email.

1. WHAT WE CAN ACTUALLY WIN. Check the record before chasing anything:
   decided outcomes say the win rate is 38% under GBP 10k and 0% over GBP 50k
   on the recent funnel. A big shiny tender we will not win is worth less than
   a small one we will.
2. SOURCE. Work `data/jacob/` - the Opportunity Log, the recovered contact
   book, public award and tender notices. Filter tender notices on CPV codes,
   never on the word "window": keyword matching has returned window CLEANING
   and a metaphor about a maternity door before now.
3. QUALIFY EACH ONE against what we do: commercial glazing, the postcode areas
   in our own PQQ, a value band we win in. Say why it is winnable, or drop it
   and say why not.
4. LOG WHAT SURVIVES as a company and a lead on the record, with a position
   saying who they are and who answers. Set a next_action_date on every one -
   a lead with no next date disappears.
5. WARM BEFORE COLD. Companies who have paid us before are the best source we
   have, and 150 of 170 have no position written. Start there.

Never approach anyone we are mid-tender with - check the record first. You
write no emails; anything that needs sending becomes a need with the detail."""),
}


def projects(state):
    """Standing projects with a clock: hand one back whenever the desk is idle."""
    started = []
    try:
        live = record.call("/api/projects") or {}
    except Exception:
        return started
    for persona, p in live.items():
        try:
            if record.tasks(persona, "open") or record.tasks(persona, "working"):
                continue                      # busy; the project waits
        except Exception:
            continue
        label, brief = PROJECTS.get(p.get("kind"), (p.get("label", "Project"), ""))
        if not brief:
            continue
        try:
            record.task_create(assignee=persona, title=label, body=brief,
                               kind="project", priority=6, created_by="project")
            started.append("%s: %s" % (persona, label))
        except Exception:
            pass
    return started


def run(state):
    """Give a standing brief to any desk with nothing to do. Returns a list of
    the personas briefed."""
    stamp = due_now(state)
    if not stamp:
        return []
    briefed = []
    for persona in config.PERSONAS:
        try:
            open_tasks = record.tasks(persona, "open")
            working = record.tasks(persona, "working")
        except Exception:
            continue
        if open_tasks or working:
            continue                     # they have real work; leave them to it
        try:
            record.task_create(
                assignee=persona, title="Standing work (queue empty)",
                body=BRIEFS[persona], kind="agenda", priority=6,
                created_by="agenda")
            briefed.append(persona)
        except Exception:
            pass
    state["last"] = stamp
    return briefed
