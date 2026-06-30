param(
  [string]$OutDir = "dist-pages"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$out = Join-Path $root $OutDir

if (Test-Path -LiteralPath $out) {
  Remove-Item -LiteralPath $out -Recurse -Force
}

New-Item -ItemType Directory -Path $out | Out-Null

Copy-Item -LiteralPath (Join-Path $root "index.html") -Destination $out
foreach ($dir in @("assets", "css", "js")) {
  Copy-Item -LiteralPath (Join-Path $root $dir) -Destination (Join-Path $out $dir) -Recurse
}

@"
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
"@ | Set-Content -LiteralPath (Join-Path $out "_headers") -Encoding UTF8

Write-Host "Cloudflare Pages artifact built at $out"
