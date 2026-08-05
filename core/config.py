# -*- coding: utf-8 -*-
"""Glasshouse configuration. One place, no drift.

The old system kept copies of the same number in three bridges and a preflight,
and they disagreed within a week. Every tunable lives here and nowhere else.
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")
MAIL_DIR = os.path.join(DATA, "mail")            # attachment files, keyed per task
LOG_DIR = os.path.join(REPO, "test-results", "glasshouse")
CLAUDE = os.path.join(os.path.expanduser("~"), ".local", "bin", "claude.exe")

PERSONAS = ("mary", "jacob", "joseph")

# ---------------------------------------------------------------- models
# Sonnet is the default for everything. Opus is the expensive specialist and it
# is reserved for the one thing that justifies it: pricing judgement, flagged
# per-task by intake. Everything on Opus was the single biggest cost mistake of
# the old system.
MODEL_DEFAULT = os.environ.get("GLASSHOUSE_MODEL", "sonnet")
MODEL_PRICING = os.environ.get("GLASSHOUSE_PRICING_MODEL", "opus")
MODEL_INTAKE = os.environ.get("GLASSHOUSE_INTAKE_MODEL", "claude-haiku-4-5-20251001")

# ---------------------------------------------------------------- cadence
INTAKE_EVERY = 120          # seconds between mailbox sweeps
BATCH_WAIT = 600            # a task waits up to this long for companions...
BATCH_URGENT_AT = 1         # ...unless priority <= this (hub messages): go now
DISPATCH_POLL = 15          # seconds between queue checks

# ---------------------------------------------------------------- breakers
# These are physics, not judgement. Everything else the old budget system
# tracked (windowed hours, session counts, day/night splits) is deleted -
# replaced by evidence in the seed and by these three walls.
DAY_CONTEXT_BREAKER = int(os.environ.get("GLASSHOUSE_DAY_BREAKER", 150_000_000))
SESSION_KILL_TOKENS = int(os.environ.get("GLASSHOUSE_SESSION_KILL", 20_000_000))
# Tool calls per session. 30 was too few for real work: Mary's first live run
# hit it at 411 seconds and 2.7M tokens, and because the limit kills the
# session before it can call finish, EVERY ONE OF THOSE TOKENS WAS LOST. The
# number matters less than the fact that a session must close out before it
# arrives - which is why the prompt now states the budget outright.
SESSION_MAX_TURNS = int(os.environ.get("GLASSHOUSE_MAX_TURNS", 70))
# Wall clock, and it is a second budget entirely separate from the turn count.
# Mary was killed at exactly 2,700s on the pricing project having used only 62
# of her 70 calls: she was pacing the thing she had been told about and had no
# idea the clock existed. 6.8M tokens died with her because a killed session
# never reaches finish. Project work gets longer, because measuring a pricing
# engine means backtest runs that take minutes each.
SESSION_TIMEOUT = 45 * 60
PROJECT_TIMEOUT = 80 * 60

# THE WORKING DAY, 08:00-18:00 (Zac, 04/08). Outside it the bots are off - with
# one exception, and it is the whole point of the exception: a message on the
# dashboard, or an email from Adam, still gets worked. Somebody deliberately
# asking for something at 19:00 is not the runaway this guard exists to stop.
WORK_HOURS = (8, 18)
NIGHT_FLAG = os.path.join(DATA, "night-allowed.json")  # lifts it for one night

DAY_TARGET = 118_000_000    # 5% of the weekly allowance - the design constraint


def env(name=".env.glasshouse"):
    out = {}
    path = os.path.join(REPO, name)
    if os.path.exists(path):
        for line in open(path, encoding="utf-8-sig"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def hub():
    e = env()
    return e.get("GLASSHOUSE_URL", "https://glasshouse-79z.pages.dev"), e.get("GLASSHOUSE_KEY", "")
