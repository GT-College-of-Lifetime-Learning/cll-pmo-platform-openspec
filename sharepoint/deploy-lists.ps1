# CLL-SPM provisioning skeleton — deploys registry lists to a test site or production.
# Task 1.2 of add-portfolio-registry-and-exec-dashboards.
#
# Usage:
#   .\deploy-lists.ps1 -Target test       # deploys to the TEST site URL (default)
#   .\deploy-lists.ps1 -Target prod       # deploys to the PRODUCTION site URL
#   .\deploy-lists.ps1 -Target prod -DryRun
#
# Prerequisites (task 0.10 confirms auth approach with OIT):
#   Install-Module PnP.PowerShell
#   Register-PnPEntraIDApp (interactive, one-time) or use -Interactive below.
#
# The tenant/site URLs below are placeholders until task 0.7 lands the real
# SharePoint site; override with -Url for ad-hoc targets.

[CmdletBinding()]
param(
    [ValidateSet('test', 'prod')]
    [string]$Target = 'test',
    [string]$Url,                      # ad-hoc override
    [string]$Template = 'registry-lists.json',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$sites = @{
    test = 'https://gatech.sharepoint.com/sites/CLL-SPM-TEST'   # placeholder until OIT 0.7
    prod = 'https://gatech.sharepoint.com/sites/CLL-SPM'       # placeholder until OIT 0.7
}

$siteUrl = if ($Url) { $Url } else { $sites[$Target] }
$root = Split-Path -Parent $PSScriptRoot
$templatePath = Join-Path $root $Template

if (-not (Test-Path $templatePath)) {
    throw "Template not found: $templatePath"
}

# Sanity: the template must parse before we touch SharePoint.
try { $null = Get-Content $templatePath -Raw | ConvertFrom-Json }
catch { throw "Template is not valid JSON: $_" }

if (-not (Get-Module -ListAvailable PnP.PowerShell)) {
    throw "PnP.PowerShell is not installed. Run: Install-Module PnP.PowerShell"
}

if ($DryRun) {
    Write-Host "[dry-run] Would deploy $templatePath to $siteUrl (target: $Target)" -ForegroundColor Cyan
    $null = Get-Content $templatePath -Raw | ConvertFrom-Json
    Write-Host "[dry-run] Template parsed: $((Get-Content $templatePath -Raw | ConvertFrom-Json).lists.Count) lists"
    return
}

Write-Host "Connecting to $siteUrl (target: $Target)..." -ForegroundColor Cyan
# Auth: interactive for now; switch to -ClientId of a registered app once OIT confirms (task 0.10).
Connect-PnPOnline -Url $siteUrl -Interactive

Write-Host "Applying provisioning template $templatePath..." -ForegroundColor Cyan
Invoke-PnPTemplate -Path $templatePath

Write-Host "Done. Lists deployed to $siteUrl" -ForegroundColor Green