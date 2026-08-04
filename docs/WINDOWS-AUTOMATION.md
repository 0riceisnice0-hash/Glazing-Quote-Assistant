# Windows bot automation

This runbook covers the local Windows tasks that run Mary Grace and Jacob from
the Desktop checkout. It is the safe way to pause development without deleting
queues, credentials, logs, or task definitions.

## Current development pause

Development automation was paused on 30 July 2026 after the Claude allowance
was exhausted. Use `scripts/development-automation.ps1`; do not delete tasks or
queue files.

```powershell
# Inspect the current state
powershell -ExecutionPolicy Bypass -File scripts\development-automation.ps1 -Mode Status

# Disable every project task and stop the running bot process trees
powershell -ExecutionPolicy Bypass -File scripts\development-automation.ps1 -Mode Pause

# Restore only the tasks that were enabled before the pause
powershell -ExecutionPolicy Bypass -File scripts\development-automation.ps1 -Mode Resume
```

Pause/resume state is machine-specific and is stored outside Git at:

```text
%LOCALAPPDATA%\Glazing-Quote-Assistant\automation-pause.json
```

`Pause` is idempotent. Running it again does not overwrite the original
enabled/disabled snapshot. `Resume` deliberately leaves `MaryGracePoller`
disabled because it was already disabled before this pause.

## Root cause of the terminal popup

The visible terminal was not Claude Desktop. It came from unattended Claude
Code CLI children started by the bridges:

- `JacobBridge` found two queued work orders after the allowance ran out.
  `jacob_bridge.py` had no failure backoff, so its normal two-minute poll became
  a two-minute Claude retry. The bridge recorded 186 fast failures by 14:26 on
  30 July.
- `MaryGraceBridge` also had queued work, but its existing backoff reached one
  retry every 30 minutes.
- The five-minute `MaryGraceBridge` Task Scheduler trigger is a restart-if-dead
  heartbeat. `MultipleInstancesPolicy=IgnoreNew` means it does not create a
  second bridge while the first is alive.
- The bridge processes use `pythonw.exe`, but that alone does not suppress a
  console window created by their child `claude.exe`.

The durable code fix has three parts:

1. Jacob now backs off failed Claude launches at 2, 5, 15, then 30 minutes.
2. Every bridge/fallback/lab Claude child uses Windows
   `CREATE_NO_WINDOW`, so a future failure is logged without flashing a
   terminal.
3. `MaryGraceMorningUpdate` now runs
   `scripts/mary_morning_update.py` under `pythonw.exe` instead of launching
   the console-subsystem `claude.exe` directly.

Pausing remains the correct response to an exhausted allowance because it also
stops polling, overnight pricing, daily updates, and deployments.

## Managed task inventory

| Task | Normal role | Pause behaviour |
|---|---|---|
| `MaryGraceBridge` | Always-on intake and per-job Claude dispatch | Disabled and stopped |
| `JacobBridge` | Business-development intake and Claude dispatch | Disabled and stopped |
| `MaryGraceMorningUpdate` | Daily Claude run through the hidden wrapper | Disabled |
| `MaryGracePricingLab` | Overnight Claude pricing sessions | Disabled |
| `MaryGraceEvolve` | Nightly deterministic learning/deploy cycle | Disabled |
| `MaryGraceEvolveFull` | Weekly full learning/deploy cycle | Disabled |
| `MaryLibrarian` | Daily deterministic memory health report | Disabled |
| `JacobDaily` | Daily deterministic intake/deploy | Disabled |
| `MaryGracePoller` | Superseded 15-minute fallback | Remains disabled |

The task list is explicit in the script so a future unrelated Windows task is
never disabled just because its command contains the word "Claude".

## What pause preserves

Pause does not delete or move anything in:

- `test-results/mary-inbox/queue`
- `test-results/jacob-inbox/queue`
- either bot's processed history
- `.env.mary` or `.env.jacob`
- the Task Scheduler definitions
- bridge logs and state

New mail is not ingested while the bridges are paused. On resume, the existing
Graph polling/dedup logic catches up and the saved queue is processed. Review
the queue depth before resuming because every queued item may start a Claude
session.

## Verification

After pausing, `Status` must show:

```text
PauseActive    : True
BotProcessCount: 0
```

Every managed task must show `Enabled=False` and `State=Disabled`. Also verify
there is no Claude Code CLI child; Claude Desktop is unrelated and can remain
open:

```powershell
Get-CimInstance Win32_Process |
  Where-Object CommandLine -match '\\.local\\bin\\claude\.exe'
```

After resuming, both bridge tasks start immediately. The other tasks wait for
their ordinary schedules.

## 30 July 2026 incident evidence

At the time of diagnosis:

- `JacobBridge` was running continuously and launching Claude every two minutes.
- Jacob's queue contained two work orders and `fails` had reached 186.
- Mary's queue contained 25 work orders and `fails` had reached 15.
- `MaryGracePoller` was already disabled.
- Task Scheduler actions all pointed to
  `C:\Users\zacpl\Desktop\Glazing-Quote-Assistant`.

This is why the Desktop checkout, not the older Documents/OneDrive copies, is
the authoritative local automation checkout.
