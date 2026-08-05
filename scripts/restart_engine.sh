#!/usr/bin/env bash
# Swap the engine over without killing a session mid-flight.
#
# Killing a working session is not free: it dies before it can call finish and
# everything it worked out is lost (2.7M tokens, 04/08). But simply "waiting
# for a gap" waits for ever - with three desks and a full queue the engine
# starts a new session seconds after each one ends.
#
# So: PAUSE it (finish what is running, start nothing new), let it drain,
# then swap. Only the OLD engine reads the pause file; the new one clears it.
set -u
cd "$(dirname "$0")/.." || exit 1
PAUSE=data/PAUSED
LOCK=data/RESTARTING

# ONE RESTART AT A TIME. Two of these ran concurrently on 05/08 and each
# started its own engine, so the machine ended up with two dispatchers both
# claiming work and both spending. The lock is checked and taken atomically -
# mkdir either succeeds or it does not.
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "[$(date +%H:%M:%S)] another restart is already running - doing nothing"
  exit 0
fi
cleanup() { rmdir "$LOCK" 2>/dev/null || true; }
trap cleanup EXIT
DEADLINE=$(( $(date +%s) + 3000 ))

alive() {
  powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process -Filter \"Name='claude.exe'\" | Where-Object {\$_.CommandLine -like '*--max-turns*'}).Count" \
    2>/dev/null | tr -d '\r\n '
}

echo "[$(date +%H:%M:%S)] pausing - running sessions will finish, no new ones start"
: > "$PAUSE"

while [ "$(alive)" != "0" ] && [ "$(date +%s)" -lt "$DEADLINE" ]; do
  echo "[$(date +%H:%M:%S)] draining - $(alive) session(s) still working"
  sleep 15
done

if [ "$(alive)" != "0" ]; then
  echo "[$(date +%H:%M:%S)] gave up after 50 minutes; leaving the old engine alone"
  rm -f "$PAUSE"
  exit 1
fi

echo "[$(date +%H:%M:%S)] drained. Swapping the engine over."
powershell -NoProfile -Command \
  "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object {\$_.CommandLine -like '*glasshouse.py*'} | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }"
sleep 3
rm -f "$PAUSE"
nohup python -u core/glasshouse.py > test-results/glasshouse/engine.out 2>&1 &
sleep 12
cat test-results/glasshouse/engine.out
echo "[$(date +%H:%M:%S)] RESTARTED"
