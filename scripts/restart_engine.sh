#!/usr/bin/env bash
# Restart the Glasshouse engine WITHOUT killing a session that is mid-flight.
#
# Killing a working session is not free: it dies before it can call finish, and
# everything it worked out is lost (2.7M tokens, 04/08). So wait for the
# current one to close out, then swap the engine over.
set -u
cd "$(dirname "$0")/.." || exit 1
LOG=test-results/glasshouse/dispatch.log
DEADLINE=$(( $(date +%s) + 3600 ))

alive() {
  powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process -Filter \"Name='claude.exe'\" | Where-Object {\$_.CommandLine -like '*--max-turns*'}).Count" \
    2>/dev/null | tr -d '\r\n '
}

echo "[$(date +%H:%M:%S)] waiting for in-flight sessions to close out..."
while [ "$(alive)" != "0" ] && [ "$(date +%s)" -lt "$DEADLINE" ]; do sleep 10; done

if [ "$(alive)" != "0" ]; then
  echo "[$(date +%H:%M:%S)] a session is STILL running after an hour - not touching it"
  exit 1
fi

echo "[$(date +%H:%M:%S)] all sessions closed. Last line:"
tail -1 "$LOG"

powershell -NoProfile -Command \
  "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object {\$_.CommandLine -like '*glasshouse.py*'} | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }"
sleep 4
nohup python -u core/glasshouse.py > test-results/glasshouse/engine.out 2>&1 &
sleep 12
cat test-results/glasshouse/engine.out
echo "[$(date +%H:%M:%S)] RESTARTED - all three desks can now run at once"
