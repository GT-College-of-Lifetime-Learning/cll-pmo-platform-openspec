# CLL-SPM Power Platform solution export + unpack routine (task 1.4).
# Exports the CLL-SPM solution from the default environment, unpacks it for
# git-friendly diffs, and stages changes for re-pack/re-import.
#
# Prereqs: Power Platform CLI (pac) installed and authenticated:
#   pac auth create --url https://gatech.crm.dynamics.com   (or tenant env URL from OIT)
# Design refs: D8 (build as code), D12 (default environment, unmanaged solution).
#
# Usage:
#   .\export-solution.ps1                    # export + unpack CLL-SPM (unmanaged)
#   .\export-solution.ps1 -Managed           # export managed variant
#   .\export-solution.ps1 -Commit            # also stage the unpacked tree for git

[CmdletBinding()]
param(
    [string]$SolutionName = 'CLL-SPM',
    [string]$OutDir = 'solution',            # flows/solution/<unpacked tree>
    [switch]$Managed,
    [switch]$Commit
)

$ErrorActionPreference = 'Stop'
$flowsRoot = $PSScriptRoot          # flows/
$stage = Join-Path $flowsRoot '_export'
New-Item -ItemType Directory -Force $stage | Out-Null

$zipName = if ($Managed) { "$SolutionName_managed" } else { $SolutionName }
$zip = Join-Path $stage "$zipName.zip"

Write-Host "Exporting solution $SolutionName..." -ForegroundColor Cyan
pac solution export --name $SolutionName --path $zip --managed:$Managed
if ($LASTEXITCODE -ne 0) { throw "pac solution export failed ($LASTEXITCODE)" }

$unpackRoot = Join-Path $flowsRoot $OutDir
Write-Host "Unpacking to $unpackRoot..." -ForegroundColor Cyan
if (Test-Path $unpackRoot) { Remove-Item -Recurse -Force $unpackRoot }
pac solution unpack --zipfile $zip --folder $unpackRoot
if ($LASTEXITCODE -ne 0) { throw "pac solution unpack failed ($LASTEXITCODE)" }

# The unpacked tree contains build artifacts that do not diff cleanly.
Remove-Item -Force (Join-Path $stage "$zipName.zip") -ErrorAction SilentlyContinue

if ($Commit) {
    Push-Location $flowsRoot
    git add -A -- $OutDir
    Pop-Location
    Write-Host "Staged $OutDir for commit. Review, then: git commit -m 'chore: export CLL-SPM solution'" -ForegroundColor Yellow
}

Write-Host "Done. Unpacked solution at $unpackRoot" -ForegroundColor Green
Write-Host "Reminder (D9): verify no flow ownership changed to a personal account before committing." -ForegroundColor DarkYellow