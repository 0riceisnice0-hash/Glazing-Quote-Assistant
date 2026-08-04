[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("Pause", "Resume", "Status")]
    [string]$Mode
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$stateDirectory = Join-Path $env:LOCALAPPDATA "Glazing-Quote-Assistant"
$stateFile = Join-Path $stateDirectory "automation-pause.json"

# This is intentionally explicit. The command must never disable unrelated
# Windows tasks merely because a future task happens to mention "Claude".
$taskNames = @(
    "JacobBridge",
    "JacobDaily",
    "JosephBridge",
    "MaryGraceBridge",
    "MaryGraceEvolve",
    "MaryGraceEvolveFull",
    "MaryGraceMorningUpdate",
    "MaryGracePoller",
    "MaryGracePricingLab",
    "MaryLibrarian"
)
$bridgeTaskNames = @("JacobBridge", "JosephBridge", "MaryGraceBridge")

# SUPERSEDED, AND RESUME MUST NOT TURN THEM BACK ON. Resume restores whatever
# was enabled before the pause, which is right for a pause but wrong for a task
# the system has since replaced.
#
# MaryGracePoller runs mary_poller.py, the mail path the front desk replaced on
# 04/08. It reads estimating@ and mary@ with no triage, queues everything to
# Mary whoever it belongs to, and launches sessions outside the batching and
# one-sitting rules. Running it beside scripts/frontdesk.py would double-queue
# every message and undo the cost work. Its own docstring already says the
# bridge supersedes it.
$supersededTaskNames = @("MaryGracePoller")

function Get-TaskRecord {
    param([string]$Name)

    $task = Get-ScheduledTask -TaskName $Name -ErrorAction SilentlyContinue
    if ($null -eq $task) {
        return [pscustomobject]@{
            Name = $Name
            Exists = $false
            Enabled = $false
            State = "Missing"
            LastRunTime = $null
            NextRunTime = $null
        }
    }

    $info = Get-ScheduledTaskInfo -TaskName $Name
    return [pscustomobject]@{
        Name = $Name
        Exists = $true
        Enabled = [bool]$task.Settings.Enabled
        State = [string]$task.State
        LastRunTime = $info.LastRunTime
        NextRunTime = $info.NextRunTime
    }
}

function Get-BotProcesses {
    $escapedRoot = [regex]::Escape($repoRoot)
    @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
        $_.ProcessId -ne $PID -and $_.CommandLine -and (
            $_.CommandLine -match $escapedRoot -or
            $_.CommandLine -match "\\.local\\bin\\claude\.exe.*Fenster Glazing"
        )
    })
}

function Stop-BotProcesses {
    # Capture the process tree before stopping Task Scheduler: a Claude child
    # may otherwise be orphaned when its pythonw parent exits.
    $all = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue)
    $escapedRoot = [regex]::Escape($repoRoot)
    $roots = @($all | Where-Object {
        $_.ProcessId -ne $PID -and $_.CommandLine -and (
            $_.CommandLine -match $escapedRoot -or
            $_.CommandLine -match "\\.local\\bin\\claude\.exe.*Fenster Glazing"
        )
    })
    $orderedIds = [System.Collections.Generic.List[int]]::new()
    $frontier = [System.Collections.Generic.List[int]]::new()
    foreach ($process in $roots) {
        if (-not $orderedIds.Contains([int]$process.ProcessId)) {
            $orderedIds.Add([int]$process.ProcessId)
            $frontier.Add([int]$process.ProcessId)
        }
    }
    for ($index = 0; $index -lt $frontier.Count; $index++) {
        $parentId = $frontier[$index]
        foreach ($child in @($all | Where-Object { $_.ParentProcessId -eq $parentId })) {
            if (-not $orderedIds.Contains([int]$child.ProcessId)) {
                $orderedIds.Add([int]$child.ProcessId)
                $frontier.Add([int]$child.ProcessId)
            }
        }
    }

    $ids = @($orderedIds)
    [array]::Reverse($ids)
    foreach ($processId in $ids) {
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
}

function Remove-StaleRuntimeFiles {
    foreach ($relativePath in @(
        "test-results\jacob-inbox\bridge.pid",
        "test-results\jacob-inbox\session.lock",
        "test-results\mary-inbox\bridge.pid",
        "test-results\mary-inbox\session.lock"
    )) {
        $path = Join-Path $repoRoot $relativePath
        if (Test-Path -LiteralPath $path) {
            Remove-Item -LiteralPath $path -Force
        }
    }
}

function Show-Status {
    $pauseState = $null
    if (Test-Path -LiteralPath $stateFile) {
        $pauseState = Get-Content -Raw -LiteralPath $stateFile | ConvertFrom-Json
    }

    [pscustomobject]@{
        PauseActive = [bool]($pauseState -and $pauseState.active)
        StateFile = $stateFile
        BotProcessCount = @(Get-BotProcesses).Count
    } | Format-List
    $taskNames | ForEach-Object { Get-TaskRecord -Name $_ } |
        Format-Table -AutoSize
}

if ($Mode -eq "Status") {
    Show-Status
    exit 0
}

New-Item -ItemType Directory -Path $stateDirectory -Force | Out-Null

if ($Mode -eq "Pause") {
    $existingState = $null
    if (Test-Path -LiteralPath $stateFile) {
        $existingState = Get-Content -Raw -LiteralPath $stateFile |
            ConvertFrom-Json
    }

    if (-not ($existingState -and $existingState.active)) {
        $snapshot = [ordered]@{
            version = 1
            active = $true
            capturedAt = (Get-Date).ToString("o")
            repoRoot = $repoRoot
            tasks = @($taskNames | ForEach-Object {
                Get-TaskRecord -Name $_
            })
        }
        $snapshot | ConvertTo-Json -Depth 5 |
            Set-Content -LiteralPath $stateFile -Encoding UTF8
    }

    # Capture and stop the live process trees before Task Scheduler can orphan a
    # Claude child by terminating only its pythonw parent.
    Stop-BotProcesses
    # Then stop the task instances and disable their repetition/logon triggers.
    foreach ($name in $taskNames) {
        $task = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
        if ($null -ne $task) {
            Stop-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
            Disable-ScheduledTask -TaskName $name | Out-Null
        }
    }
    # A trigger could have landed during the small stop/disable window.
    Stop-BotProcesses
    Remove-StaleRuntimeFiles
    Show-Status
    exit 0
}

if (-not (Test-Path -LiteralPath $stateFile)) {
    throw "No pause snapshot exists at $stateFile. Nothing can be resumed safely."
}
$resumeState = Get-Content -Raw -LiteralPath $stateFile | ConvertFrom-Json
if (-not $resumeState.active) {
    Write-Output "Automation is already resumed."
    Show-Status
    exit 0
}

foreach ($record in $resumeState.tasks) {
    if ($record.Exists -and $record.Enabled) {
        # A superseded task was enabled before the pause and must still not come
        # back - see $supersededTaskNames. Restoring it would be faithful to the
        # snapshot and wrong for the system.
        if ($supersededTaskNames -contains $record.Name) {
            Write-Output "Leaving $($record.Name) disabled - superseded, see the note in this script."
            continue
        }
        $task = Get-ScheduledTask -TaskName $record.Name `
            -ErrorAction SilentlyContinue
        if ($null -ne $task) {
            Enable-ScheduledTask -TaskName $record.Name | Out-Null
        }
    }
}
foreach ($name in $bridgeTaskNames) {
    $record = @($resumeState.tasks | Where-Object { $_.Name -eq $name }) |
        Select-Object -First 1
    if ($record -and $record.Exists -and $record.Enabled) {
        Start-ScheduledTask -TaskName $name
    }
}

$resumeState.active = $false
$resumeState | Add-Member -NotePropertyName resumedAt `
    -NotePropertyValue (Get-Date).ToString("o") -Force
$resumeState | ConvertTo-Json -Depth 5 |
    Set-Content -LiteralPath $stateFile -Encoding UTF8
Show-Status
