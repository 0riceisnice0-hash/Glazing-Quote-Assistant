# Jacob Wright - Exchange setup. Run this in a window where you have already
# run Connect-ExchangeOnline.
#
#   .\scripts\setup-jacob-exchange.ps1 -ReaderAppId <guid> -SenderAppId <guid>
#
# Safe to re-run: every step checks before it creates, so a partial run can
# simply be run again. It makes NO change until all the pre-flight checks pass.
#
# What it does:
#   1. resolves Jay's real mailbox address instead of assuming jayk@
#   2. creates the jacob@ shared mailbox
#   3. creates a hidden scope group: commercial@, info@, jacob@, Jay
#   4. restricts both Jacob apps to that group (by object id, not address -
#      the address form fails with "identity of the policy scope could not
#      be resolved" because the group takes the .onmicrosoft.com domain)
#   5. blocks jacob@ from sending outside the company
#   6. verifies, including that Mary and Jacob cannot see into each other

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string] $ReaderAppId,
    [Parameter(Mandatory = $true)][string] $SenderAppId,
    [string] $JayAddress = "jayk@fensterglazing.com",
    [string] $Domain     = "fensterglazing.com",
    # Mary's reader - used only to prove the two bots stay separated.
    [string] $MaryReaderAppId = "a058a159-e04b-41f3-b5cc-d90d5717164c"
)

$ErrorActionPreference = "Stop"
function Say  ($m) { Write-Host "  $m" }
function Step ($m) { Write-Host "`n=== $m" -ForegroundColor Cyan }
function Ok   ($m) { Write-Host "  OK   $m" -ForegroundColor Green }
function Warn ($m) { Write-Host "  NOTE $m" -ForegroundColor Yellow }

# ---------------------------------------------------------------- pre-flight
Step "Pre-flight - nothing is changed until these all pass"

if (-not (Get-Command Get-DistributionGroup -ErrorAction SilentlyContinue)) {
    throw "Not connected to Exchange Online. Run Connect-ExchangeOnline first, in this same window."
}
Ok "Exchange Online session is live"

# Jay: resolve rather than assume. If the given address is wrong, look for a
# sensible candidate and stop so a human can confirm - never guess silently.
$jay = $null
try { $jay = Get-Recipient $JayAddress -ErrorAction Stop } catch { }
if ($null -eq $jay) {
    Warn "$JayAddress did not resolve. Candidates:"
    Get-Recipient -ResultSize Unlimited |
        Where-Object { $_.PrimarySmtpAddress -like "*jay*" -or $_.DisplayName -like "*Jay*" } |
        Format-Table DisplayName, PrimarySmtpAddress, RecipientTypeDetails | Out-Host
    throw "Re-run with -JayAddress <the correct address> once you have picked one from the list above."
}
Ok ("Jay resolves: {0} <{1}> [{2}]" -f $jay.DisplayName, $jay.PrimarySmtpAddress, $jay.RecipientTypeDetails)
if ($jay.RecipientTypeDetails -like "*UserMailbox*") {
    Warn "This is a personal mailbox, not a shared one. Jacob will be able to read all of it."
}

foreach ($m in @("commercial@$Domain", "info@$Domain")) {
    if (-not (Get-Recipient $m -ErrorAction SilentlyContinue)) { throw "$m does not resolve." }
    Ok "$m resolves"
}

# ---------------------------------------------------------------- mailbox
Step "Jacob's mailbox"
$jacobAddr = "jacob@$Domain"
if (Get-Recipient $jacobAddr -ErrorAction SilentlyContinue) {
    Ok "$jacobAddr already exists - leaving it alone"
} else {
    New-Mailbox -Shared -Name "Jacob Wright" -DisplayName "Jacob Wright" `
                -Alias jacob -PrimarySmtpAddress $jacobAddr | Out-Null
    Ok "created $jacobAddr"
    Say "waiting for it to become addressable..."
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 10
        if (Get-Recipient $jacobAddr -ErrorAction SilentlyContinue) { break }
    }
    if (-not (Get-Recipient $jacobAddr -ErrorAction SilentlyContinue)) {
        throw "Mailbox created but not addressable yet. Wait a few minutes and re-run this script."
    }
    Ok "addressable"
}

# ---------------------------------------------------------------- scope group
Step "Read-scope group"
$members = @("commercial@$Domain", "info@$Domain", $jacobAddr, $jay.PrimarySmtpAddress)
$group = Get-DistributionGroup -Identity jacob-scope -ErrorAction SilentlyContinue
if ($null -eq $group) {
    New-DistributionGroup -Name "Jacob Mailbox Scope" -Alias jacob-scope `
                          -Type Security -Members $members | Out-Null
    $group = Get-DistributionGroup -Identity jacob-scope
    Ok "created jacob-scope"
} else {
    Ok "jacob-scope already exists - topping up members"
    $have = (Get-DistributionGroupMember -Identity jacob-scope).PrimarySmtpAddress
    foreach ($m in $members) {
        if ($have -notcontains $m) {
            Add-DistributionGroupMember -Identity jacob-scope -Member $m
            Ok "added $m"
        }
    }
}
Set-DistributionGroup -Identity jacob-scope -HiddenFromAddressListsEnabled $true
$scopeId = $group.ExternalDirectoryObjectId
Ok "object id $scopeId"
Say "members:"
Get-DistributionGroupMember -Identity jacob-scope |
    Select-Object -ExpandProperty PrimarySmtpAddress | ForEach-Object { Say "  - $_" }

# ---------------------------------------------------------------- policies
Step "Restricting both apps to that group"
$existing = Get-ApplicationAccessPolicy -ErrorAction SilentlyContinue
foreach ($pair in @(@($ReaderAppId, "Jacob-Reader"), @($SenderAppId, "Jacob-Sender"))) {
    $appId = $pair[0]; $label = $pair[1]
    if ($existing | Where-Object { $_.AppId -eq $appId }) {
        Ok "$label already has a policy - skipping"
        continue
    }
    New-ApplicationAccessPolicy -AppId $appId -PolicyScopeGroupId $scopeId `
        -AccessRight RestrictAccess -Description "${label}: BD mailboxes only" | Out-Null
    Ok "$label restricted"
}

# ---------------------------------------------------------------- transport
Step "Blocking outbound to anyone outside the company"
if (Get-TransportRule -Identity "Jacob internal only" -ErrorAction SilentlyContinue) {
    Ok "rule already exists"
} else {
    New-TransportRule -Name "Jacob internal only" -From $jacobAddr `
        -SentToScope NotInOrganization `
        -RejectMessageReasonText "Jacob is not yet approved to send externally" | Out-Null
    Ok "rule created - remove it only when an approval queue exists"
}

# ---------------------------------------------------------------- verify
Step "Verifying"
function Check ($mailbox, $appId, $expect, $why) {
    try {
        $r = (Test-ApplicationAccessPolicy -Identity $mailbox -AppId $appId).AccessCheckResult
        if ($r -eq $expect) { Ok  ("{0,-34} {1,-8} {2}" -f $mailbox, $r, $why) }
        else                { Warn ("{0,-34} {1,-8} EXPECTED {2} - {3}" -f $mailbox, $r, $expect, $why) }
    } catch { Warn "$mailbox - could not test: $($_.Exception.Message)" }
}
Check $jay.PrimarySmtpAddress $ReaderAppId "Granted" "Jacob reads Jay"
Check "commercial@$Domain"    $ReaderAppId "Granted" "Jacob reads commercial"
Check "info@$Domain"          $ReaderAppId "Granted" "Jacob reads info"
Check "paul@$Domain"          $ReaderAppId "Denied"  "Jacob cannot read personal mailboxes"
Check $jacobAddr              $MaryReaderAppId "Denied" "Mary cannot read Jacob"
Check "estimating@$Domain"    $ReaderAppId "Denied"  "Jacob cannot read estimating (Mary's)"

Write-Host "`nDone. Two things that look wrong and are not:" -ForegroundColor Cyan
Say "Policies take well over an hour to actually bite, so Graph may keep serving"
Say "mailboxes that Test- already reports as Denied."
Say "Next: create .env.jacob with the five values. Never paste secrets into chat."
