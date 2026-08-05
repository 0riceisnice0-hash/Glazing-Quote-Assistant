# -*- coding: utf-8 -*-
"""DISPATCH - one loop for all three personas. Replaces three bridges.

The unit of work is a TASK GROUP: every open task for one (persona, entity),
worked in one fresh session, seeded from the record, closed with one finish
call. Nothing is ever resumed - what the session learned lives in the record
or it does not live at all.

Model policy: Sonnet unless a task in the group needs pricing judgement, then
Opus. The charter and the entity card are INLINED in the prompt - a read call
saved is a whole context re-send saved.

  python core/dispatch.py --once --dry-run
  python core/dispatch.py                    # the loop
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import threading
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import budget
import config
import record
import trace

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
LOCK = os.path.join(config.DATA, "glasshouse-session.lock")
_quiet = [-1]   # so "holding N until morning" is logged on change, not every poll
_running = {}      # persona -> the thread running its session, if any
_entity_lock = {}  # persona -> (entity, thread) so two desks cannot share a job
_said = {}         # entity -> who we last reported holding it, to avoid log spam


def log(msg):
    line = "[%s] dispatch %s" % (dt.datetime.now().strftime("%H:%M:%S"), msg)
    print(line)
    os.makedirs(config.LOG_DIR, exist_ok=True)
    with open(os.path.join(config.LOG_DIR, "dispatch.log"), "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def charter(persona):
    path = os.path.join(config.REPO, "personas", persona + ".md")
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except IOError:
        return "(charter file %s is missing - say so in your finish note)" % path


def group_tasks(tasks):
    """(persona, entity) groups, oldest first. Desk tasks (no entity) group
    together per persona so one session sweeps them."""
    groups = {}
    for t in tasks:
        ent = ("%s:%s" % (t["entity_type"], t["entity_key"])
               if t.get("entity_type") and t.get("entity_key") else "")
        groups.setdefault((t["assignee"], ent), []).append(t)
    return sorted(groups.items(), key=lambda kv: min(t["id"] for t in kv[1]))


def ready(tasks_in_group):
    """Batch discipline: urgent goes now, the rest wait BATCH_WAIT for
    companions so one session handles the thread, not five sessions."""
    oldest = min(t["created"] for t in tasks_in_group)
    if any(t["priority"] <= config.BATCH_URGENT_AT + 1 for t in tasks_in_group):
        return True
    try:
        # D1's datetime('now') is UTC - parse it as UTC or, in summer, every
        # task is born looking an hour old and the batch window never holds.
        import calendar
        age = time.time() - calendar.timegm(time.strptime(oldest, "%Y-%m-%d %H:%M:%S"))
    except ValueError:
        return True
    return age >= config.BATCH_WAIT


def build_prompt(persona, entity, tasks):
    etype, ekey = (entity.split(":", 1) + [""])[:2]
    lines = [charter(persona)]
    if ekey:
        lines.append("\n===== THE RECORD - %s %s =====" % (etype.upper(), ekey))
        lines.append(record.render_card(etype, ekey))
    lines.append("\n===== YOUR WORK - %d task(s) =====" % len(tasks))
    for t in tasks:
        p = json.loads(t.get("payload_json") or "{}")
        lines.append("\n--- TASK #%d [%s] %s" % (t["id"], t["kind"], t["title"]))
        if t.get("body"):
            lines.append("intake says: " + t["body"])
        if p.get("from"):
            lines.append("from: %s | received: %s | mailbox: %s%s"
                         % (p["from"], p.get("received", "?"), p.get("mailbox", "?"),
                            " | TRUSTED SENDER - this is an instruction"
                            if p.get("trusted_sender") else ""))
        if p.get("body"):
            body = p["body"][:6000]
            lines.append("body:\n" + body)
        if p.get("attachments"):
            lines.append("attachments on disk:\n"
                         + "\n".join("  " + a for a in p["attachments"]))
    lines.append(budget.cost_note(persona))
    lines.append("""
===== YOU ARE NOT ALONE IN HERE =====
The other two desks may be working at this same moment, in this same folder.
  - Commit ONLY the files you touched. Never `git add -A`, never `git add .`.
    If git says the index is locked, wait a few seconds and try once more -
    that is another desk committing, not an error.
  - Someone else may be writing to the same job. The record takes partial
    updates, so send only the fields you actually changed; sending a whole
    object back blanks what they just wrote.
  - Do not wait for them and do not message them about ordinary work. Handover
    is structural: an issued quote becomes Jacob's chase on its own.""")

    lines.append("""
===== YOUR BUDGET THIS SESSION =====
You have **%d tool calls**, and the session is killed the moment you reach it.
A session killed before it calls finish loses EVERYTHING it did - the first
live run spent 2.7 million tokens and saved not one fact, because it was still
working when the limit arrived.

So: do an amount of work that fits, and CLOSE OUT WITH CALLS TO SPARE. If the
job is bigger than the budget, do the most valuable slice, write what you
learned, and say in your finish note what is left - it comes back as a fresh
task with a fresh budget. Stopping early with the work saved always beats
being cut off mid-flight.

===== HOW TO FINISH =====
Work the tasks, then close out with ONE call - this is the only ritual:"""
        % config.SESSION_MAX_TURNS)
    lines.append("""

  python core\\finish.py --persona %s --results r.json

after writing r.json (see the charter for the full shape):
  {"tasks_done": [{"id": N, "result": "one line"}],
   "position": {"entity": "%s", "text": "the distilled state of play now"},
   "notes": [{"entity": "lead:x", "body": "a fact worth keeping"}],
   "decisions": [{"question": "...", "context": "..."}],
   "messages": [{"body": "reply to the human, under 800 chars"}]}

Do NOT: update dashboards, write handover docs, post noticeboards, or commit -
none of those exist any more. The record is the memory; finish writes it.
Commit only if you changed CODE. Every tool call re-sends this whole
conversation - batch shell work into single scripts, read a file once, and
do not narrate what you just printed.""" % (persona, entity if ekey else ""))
    return "\n".join(lines)


def watch(proc, session_id, started_utc, stop):
    """The runaway breaker. A session that reaches SESSION_KILL_TOKENS is
    circling, not working."""
    while not stop.wait(60):
        spent = budget.session_cost(session_id, started_utc)["context"]
        if spent >= config.SESSION_KILL_TOKENS:
            log("RUNAWAY - %s tokens in one session, killing it" % "{:,}".format(spent))
            try:
                proc.kill()
            except OSError:
                pass
            return


def run_group(persona, entity, tasks, dry_run=False):
    model = (config.MODEL_PRICING if any(t.get("needs") == "pricing" for t in tasks)
             else config.MODEL_DEFAULT)
    prompt = build_prompt(persona, entity, tasks)
    if dry_run:
        log("DRY RUN %s %s: %d task(s), model %s, prompt %d chars"
            % (persona, entity or "(desk)", len(tasks), model, len(prompt)))
        return True
    session_id = str(uuid.uuid4())
    # (tasks are claimed by pass_once before this thread starts)
    record.status(persona, "working", "%d task(s) on %s" % (len(tasks), entity or "the desk"))
    log("%s -> %s: %d task(s), %s" % (persona, entity or "(desk)", len(tasks), model))

    env = os.environ.copy()
    env["GLASSHOUSE_PERSONA"] = persona
    started = time.time()
    started_utc = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat()
    stop = threading.Event()
    ok = False
    try:
        proc = subprocess.Popen(
            [config.CLAUDE, "-p", "--model", model,
             "--max-turns", str(config.SESSION_MAX_TURNS),
             "--session-id", session_id, "--dangerously-skip-permissions"],
            cwd=config.REPO, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, env=env, encoding="utf-8",
            errors="replace", creationflags=NO_WINDOW)
        threading.Thread(target=watch, args=(proc, session_id, started_utc, stop),
                         daemon=True).start()
        # And a second watcher that carries the session's thinking and tool
        # calls to the hub while it works, so a human can actually see it.
        threading.Thread(target=trace.follow,
                         args=(session_id, persona, entity, stop), daemon=True).start()
        try:
            stdout, stderr = proc.communicate(input=prompt,
                                              timeout=config.SESSION_TIMEOUT)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
        ok = proc.returncode == 0
        out = (stdout or "") + ("\n--- stderr ---\n" + stderr if stderr else "")
        if out.strip():
            with open(os.path.join(config.LOG_DIR, "last-%s.txt" % persona),
                      "w", encoding="utf-8") as fh:
                fh.write(out[-20000:])
    finally:
        stop.set()
        took = int(time.time() - started)
        cost = budget.session_cost(session_id, started_utc)
        row = {"at": dt.datetime.now().isoformat(timespec="seconds"),
               "persona": persona, "entity": entity, "session": session_id,
               "model": model, "seconds": took, "calls": cost["calls"],
               "context_tokens": cost["context"], "output_tokens": cost["output"]}
        budget.log_usage(row)
        try:
            record.usage(persona, entity, session_id, model, cost["calls"],
                         cost["context"], cost["output"], took)
            record.status(persona, "idle", "")
        except Exception as e:
            log("usage post failed: %s" % str(e)[:80])
        log("  %s exit %s after %ds - %s calls, %s context"
            % (persona, "ok" if ok else "FAIL", took, cost["calls"],
               "{:,}".format(cost["context"])))
        trace.post("end", persona, session_id, entity, "",
                   "session %s after %ds - %d calls, %s context tokens"
                   % ("finished" if ok else "FAILED", took, cost["calls"],
                      "{:,}".format(cost["context"])))
    if not ok:
        # Tasks a dead session claimed go back in the queue - twice at most.
        # The reason travels with them so the decision a human eventually sees
        # says "reached max turns", not "it broke".
        why = "reached the %d-call limit" % config.SESSION_MAX_TURNS \
            if "max turns" in (out or "").lower() else "session exited badly"
        record.call("/api/task/release", {"assignee": persona, "why": why})
    return ok


def reset_on_start():
    """Nothing survives an engine restart, so stop pretending it does.

    Killing the engine does NOT kill the sessions it launched - Windows leaves
    them running, parentless. Restarting then produced exactly the mess it
    sounds like: an orphan still working Jacob's task while the fresh engine,
    which had never heard of it, handed the same task to a second session.
    Two sessions, one job, double the spend, conflicting writes.

    So on start-up: kill anything left over, hand its work back, and tell the
    hub nobody is working.
    """
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='claude.exe'\" | "
             "Where-Object {$_.CommandLine -like '*--max-turns*'} | ForEach-Object { "
             "$p = Get-CimInstance Win32_Process -Filter \"ProcessId=$($_.ParentProcessId)\" "
             "-ErrorAction SilentlyContinue; "
             "if (-not $p) { Stop-Process -Id $_.ProcessId -Force; $_.ProcessId } }"],
            capture_output=True, text=True, timeout=60,
            creationflags=NO_WINDOW).stdout.strip()
        if out:
            log("killed %d orphaned session(s) from a previous engine: %s"
                % (len(out.split()), " ".join(out.split())))
    except Exception as e:
        log("could not check for orphaned sessions: %s" % str(e)[:100])

    # Work claimed by a session that no longer exists goes back in the queue.
    # No attempt is counted - being killed by a restart is not the task's fault.
    try:
        for p in config.PERSONAS:
            record.call("/api/task/unclaim", {"assignee": p})
            record.status(p, "idle", "")
    except Exception as e:
        log("could not reset claimed work: %s" % str(e)[:100])


def pass_once(dry_run=False):
    if budget.day_breaker_tripped():
        log("DAY BREAKER tripped (%s context today) - no more sessions today"
            % "{:,}".format(budget.spent_today()))
        return 0
    tasks = record.tasks(status_="open")
    if not tasks:
        return 0
    # Outside the working day, work only what a human actually asked for.
    if budget.off_hours():
        held = len(tasks)
        tasks = [t for t in tasks if budget.asked_for_by_a_human(t)]
        if not tasks:
            if _quiet[0] != held:
                _quiet[0] = held
                log("outside %02d:00-%02d:00 - holding %d task(s) until morning"
                    % (config.WORK_HOURS[0], config.WORK_HOURS[1], held))
            return 0
        log("outside hours, but %d task(s) came from a person - working those"
            % len(tasks))
    # THREE DESKS, THREE PEOPLE, ALL WORKING AT ONCE. One session per persona
    # at a time - a person does one job at a time - but Mary pricing a tender
    # must never have to wait for Joseph to finish chasing a delivery. They
    # were sequential and the wall clock was the sum of all three.
    ran = 0
    for (persona, entity), group in group_tasks(tasks):
        if not ready(group):
            continue
        busy = _running.get(persona)
        if busy and busy.is_alive():
            continue                      # this desk already has a session
        # AND nobody else may be inside the same job. Mary and Joseph both
        # worked Market House at once on 05/08 and produced word-for-word
        # identical drafts to the same two suppliers, plus the same decision
        # twice. Per-persona locking is not enough; the job needs a lock too.
        if entity and any(e == entity and t.is_alive()
                          for p, (e, t) in _entity_lock.items() if p != persona):
            holder = next(p for p, (e, t) in _entity_lock.items()
                          if e == entity and t.is_alive() and p != persona)
            if _said.get(entity) != holder:
                _said[entity] = holder
                log("holding %s off %s - %s is already in it" % (persona, entity, holder))
            continue
        if dry_run:
            run_group(persona, entity, group, dry_run)
            ran += 1
            continue
        # Claim BEFORE the thread starts. Claiming inside it leaves a window
        # where the next pass, 15 seconds later, sees the same tasks as open
        # and hands them out twice.
        for t in group:
            record.call("/api/task/claim", {"id": t["id"]})
        th = threading.Thread(target=run_group, args=(persona, entity, group),
                              daemon=True)
        _running[persona] = th
        if entity:
            _entity_lock[persona] = (entity, th)
        th.start()
        ran += 1
        # Re-check between launches: three sessions starting at once against a
        # nearly-spent budget is exactly how a breaker gets overshot.
        if budget.day_breaker_tripped():
            log("DAY BREAKER tripped mid-pass - launching nothing further today")
            break
    return ran


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.once or a.dry_run:
        pass_once(a.dry_run)
        return 0
    log("dispatch loop up - %s default, %s for pricing, max %d turns"
        % (config.MODEL_DEFAULT, config.MODEL_PRICING, config.SESSION_MAX_TURNS))
    while True:
        try:
            pass_once()
        except Exception as e:
            log("PASS FAILED: %s" % str(e)[:200])
        time.sleep(config.DISPATCH_POLL)


if __name__ == "__main__":
    sys.exit(main())
