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

1. WHAT WE CAN ACTUALLY WIN - AND WE WIN BIG WORK. Fenster has won many jobs
   over GBP 50k; the largest is GBP 630k. Seven companies on the record have
   paid us more than GBP 50,000 (CONAMAR GBP 917k, Fortis Vision GBP 670k,
   Borras GBP 261k). Do NOT filter out large tenders.
   Any "win rate" you may have seen that says otherwise came from the
   Opportunity Log or the AdminBase export - both are funnels of OPEN and LOST
   work. All 264 AdminBase rows read "Live - Quoted"; not one is marked won.
   A dataset with no wins in it cannot tell you the win rate. The real
   evidence is `lifetime_value` on the company record and the completed-jobs
   folders in OneDrive under `2. Projects\\2. Completed`.
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

    "delivery": ("Get the board ready", """PROJECT WORK - make the delivery board
worth opening. Right now Paul and Steve see a list of jobs with no dates on
any of them, so it cannot tell them a single thing about their day. Steve's
verdict on the first version was "what the fuck is this?" and he was right.

1. SITE DATES. Not one of the live contracts has one, and every other deadline
   hangs off it. SEARCH THE MAIL PROPERLY before you raise a need for one:
   `python core\\mail.py --search "<job name>"`, then the client's name, then
   the order reference. Programme dates usually arrive in an order
   acknowledgement or a site email, not in anything labelled "site date".
   Only raise a need if it genuinely is not there - and say where you looked.
2. WHAT TO ORDER. Most steps have no `detail`. "Order glass" is half a task;
   Adam's whole complaint about the old system was that it never said WHICH
   glass. Take the spec off the order confirmations and quotes you can find -
   sizes, makeup, finish, supplier - and put it on the step. Write it for
   somebody standing on site with a phone.
3. WON JOBS THAT ARE ON NOBODY'S BOARD. You found two this morning by reading
   the mail. A won job nobody is running is the worst thing this system can
   have. Look for purchase orders, order acknowledgements and "please proceed"
   in the last two months and check each one against the contracts on record.
4. MONEY. Any job whose site date has passed with no invoice raised. Payment
   terms belong on the company record - learn them from the client's own
   emails and put them there.

Do not invent a date. A made-up date on that board is worse than an empty one,
because somebody will plan a day around it."""),
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
