# -*- coding: utf-8 -*-
"""Safety rails for letting Mary build the hub herself.

She can add pages, tabs, charts, endpoints - whatever she needs to show
something. What she must never do, even by accident, is take the lock off the
door or leak a secret. So rather than freezing files (which would stop her
working), this asserts the handful of INVARIANTS that actually matter, and
refuses the deploy if any of them broke.

Checked before every deploy:
  1. The Mary-only routes are still behind the x-mary-key gate.
  2. No secret is hardcoded anywhere in the deployed bundle.
  3. _headers still carries noindex and no-store.
  4. Every JS file parses.
  5. The hub still has its own data - a page that renders nothing is a
     regression even if it is syntactically perfect.

Run automatically by mary_dashboard.py --deploy. Standalone:
  python scripts/mary_hub_guard.py
"""
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASH = os.path.join(REPO, "dashboard")
API = os.path.join(DASH, "functions", "api", "[[path]].js")
HEADERS = os.path.join(DASH, "public", "_headers")
PUBLIC = os.path.join(DASH, "public")

# Anything that looks like a credential sitting in code rather than in env.
SECRET_PATTERNS = [
    (r"MARY_API_KEY\s*=\s*['\"][^'\"]{8,}", "MARY_API_KEY assigned a literal value"),
    (r"(?i)password\s*[:=]\s*['\"][^'\"]{4,}", "a literal password"),
    (r"(?i)(client_secret|api_key|secret)\s*[:=]\s*['\"][A-Za-z0-9_~.\-]{16,}", "an embedded secret"),
    (r"[A-Za-z0-9_~.\-]{32,}\.[A-Za-z0-9_~.\-]{16,}\.[A-Za-z0-9_~.\-]{16,}", "something shaped like a JWT"),
]


def fail(msg, detail=""):
    return {"ok": False, "msg": msg, "detail": detail}


def ok(msg):
    return {"ok": True, "msg": msg, "detail": ""}


def check_key_gate():
    """The gate must exist, and every mary-only route must sit AFTER it."""
    if not os.path.exists(API):
        return fail("the API function is missing entirely")
    with open(API, encoding="utf-8") as fh:
        src = fh.read()
    m = re.search(r"x-mary-key", src)
    if not m:
        return fail("the x-mary-key gate has been removed",
                    "Mary-only routes would be open to anyone who guessed the URL.")
    if not re.search(r"env\.MARY_API_KEY", src):
        return fail("the gate no longer compares against env.MARY_API_KEY")
    gate_at = m.start()
    exposed = [mm.group(1) for mm in re.finditer(r'route === "(mary/[^"]+)"', src)
               if mm.start() < gate_at]
    if exposed:
        return fail("mary-only route(s) declared before the key gate: %s" % ", ".join(exposed),
                    "Move them below the gate or they are public.")
    return ok("mary-only routes are behind the x-mary-key gate")


def check_no_secrets():
    hits = []
    for root, _dirs, files in os.walk(DASH):
        if "node_modules" in root or ".wrangler" in root:
            continue
        for name in files:
            if not name.endswith((".js", ".json", ".html", ".css", ".toml")):
                continue
            path = os.path.join(root, name)
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            for pattern, what in SECRET_PATTERNS:
                for mm in re.finditer(pattern, text):
                    # The generated data file is gitignored but still deployed;
                    # flag it the same as anything else.
                    hits.append("%s: %s" % (os.path.relpath(path, REPO), what))
                    break
    if hits:
        return fail("possible secret in the deployed bundle", "; ".join(sorted(set(hits))[:5]))
    return ok("no hardcoded secrets in anything being deployed")


def check_headers():
    if not os.path.exists(HEADERS):
        return fail("_headers is missing", "the hub would become indexable")
    with open(HEADERS, encoding="utf-8") as fh:
        text = fh.read().lower()
    missing = [w for w in ("noindex", "no-store") if w not in text]
    if missing:
        return fail("_headers lost: %s" % ", ".join(missing),
                    "noindex keeps the hub out of search; no-store stopped three deploys being "
                    "masked by browser cache.")
    return ok("_headers still sets noindex and no-store")


def check_js_parses():
    bad = []
    targets = [API] + [os.path.join(PUBLIC, f) for f in os.listdir(PUBLIC) if f.endswith(".js")]
    for path in targets:
        r = subprocess.run(["node", "--check", path], capture_output=True, text=True,
                           shell=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            first = (r.stderr or "").strip().split("\n")
            bad.append("%s: %s" % (os.path.basename(path), first[-1] if first else "parse error"))
    if bad:
        return fail("JavaScript does not parse", "; ".join(bad))
    return ok("every JS file parses (%d checked)" % len(targets))


def check_data_present():
    data = os.path.join(DASH, "functions", "_data", "dashboard-data.js")
    if not os.path.exists(data):
        return fail("dashboard-data.js has not been generated", "the hub would load empty")
    if os.path.getsize(data) < 2000:
        return fail("dashboard-data.js is suspiciously small (%d bytes)" % os.path.getsize(data))
    return ok("dashboard data is present (%d KB)" % (os.path.getsize(data) // 1024))


CHECKS = [check_key_gate, check_no_secrets, check_headers, check_js_parses, check_data_present]


def run(verbose=True):
    results = [c() for c in CHECKS]
    failed = [r for r in results if not r["ok"]]
    if verbose:
        print("HUB GUARD")
        for r in results:
            print("  [%s] %s" % ("ok  " if r["ok"] else "STOP", r["msg"]))
            if r["detail"]:
                print("         %s" % r["detail"])
        if failed:
            print("\nDEPLOY BLOCKED - %d invariant(s) broken. Fix them, do not work around them."
                  % len(failed))
        else:
            print("\nSafe to deploy.")
    return not failed


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
