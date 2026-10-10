<#
.SYNOPSIS
  Safe, Non-Destructive Installer for Vibe UI & vibe-ui-agent Skills Suite
.DESCRIPTION
  Installs or updates the 6 Vibe UI skills:
  - autonomous-intent-expander
  - visual-chemistry-engine
  - ui-kit
  - vibe-physics-engine
  - conversion-copy-engine
  - ui-verifier
.PARAMETER TargetDir
  Explicit target directory. Defaults to ~/.gemini/config/skills (Antigravity).
.PARAMETER Agent
  Target AI coding tool: "antigravity" (default), "claude", "cursor", "windsurf", or "custom".
.PARAMETER Backup
  Automatically backs up existing skill directories before updating (default: $true).
.PARAMETER Force
  Overwrites existing skills without creating backups.
#>

[CmdletBinding()]
param (
    [string]$TargetDir = "",
    [ValidateSet("antigravity", "gemini", "claude", "cursor", "windsurf", "custom")]
    [string]$Agent = "antigravity",
    [string]$Version = "v3.0.0-alpha.1",
    [switch]$Backup = $true,
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"

# Determine target directory based on selected Agent or explicit TargetDir
if ([string]::IsNullOrWhiteSpace($TargetDir)) {
    switch ($Agent) {
        { $_ -in @("antigravity", "gemini") } {
            $TargetDir = Join-Path $env:USERPROFILE ".gemini\config\skills"
        }
        "claude" {
            $TargetDir = Join-Path (Get-Location) ".claude\skills"
        }
        "cursor" {
            $TargetDir = Join-Path (Get-Location) ".cursor\skills"
        }
        "windsurf" {
            $TargetDir = Join-Path (Get-Location) ".windsurf\skills"
        }
        Default {
            $TargetDir = Join-Path $env:USERPROFILE ".gemini\config\skills"
        }
    }
}

Write-Host "Installing Vibe UI & AI Agent Skills Suite..." -ForegroundColor Cyan
Write-Host "Target Agent     : $Agent" -ForegroundColor DarkGray
Write-Host "Target Directory : $TargetDir" -ForegroundColor DarkGray
Write-Host "Safe Backup Mode : $(if ($Force) { 'Disabled (--Force)' } else { 'Enabled' })" -ForegroundColor DarkGray

if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$TempDir = $null
$SourceSkillsDir = $null

# Check if running from a local cloned repository
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "skills"))) {
    $SourceSkillsDir = Join-Path $PSScriptRoot "skills"
} elseif (Test-Path (Join-Path (Get-Location) "skills")) {
    $SourceSkillsDir = Join-Path (Get-Location) "skills"
} else {
    # Running remotely via 'irm ... | iex' - download archive from GitHub
    Write-Host "Fetching skills suite (version: $Version) from GitHub repository..." -ForegroundColor Cyan
    if ($Version -and $Version -ne "main") {
        $ZipUrl = "https://github.com/omid-io/vibe-ui-suite/archive/refs/tags/$Version.zip"
        $FolderPrefix = "vibe-ui-suite-$($Version.TrimStart('v'))"
    } else {
        $ZipUrl = "https://github.com/omid-io/vibe-ui-suite/archive/refs/heads/main.zip"
        $FolderPrefix = "vibe-ui-suite-main"
    }
    $TempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("vibe_ui_suite_" + [System.Guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    $ZipFile = Join-Path $TempDir "bundle.zip"
    
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $ZipUrl -OutFile $ZipFile -UseBasicParsing
        Expand-Archive -Path $ZipFile -DestinationPath $TempDir -Force
        
        # Look for skills directory inside extracted archive
        $extractedSkills = Get-ChildItem -Path $TempDir -Directory -Filter "skills" -Recurse | Select-Object -First 1
        if ($extractedSkills) {
            $SourceSkillsDir = $extractedSkills.FullName
        } else {
            $SourceSkillsDir = Join-Path $TempDir "$FolderPrefix\skills"
        }
    } catch {
        Write-Error "Failed to download skills archive from GitHub: $_"
        if ($TempDir -and (Test-Path $TempDir)) { Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue }
        exit 1
    }
}

if (-not (Test-Path $SourceSkillsDir)) {
    Write-Error "Could not locate 'skills' directory ($SourceSkillsDir)."
    if ($TempDir -and (Test-Path $TempDir)) { Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue }
    exit 1
}

$skills = Get-ChildItem -Path $SourceSkillsDir -Directory

foreach ($skill in $skills) {
    $dest = Join-Path $TargetDir $skill.Name
    
    # Safe non-destructive backup
    if ((Test-Path $dest) -and (-not $Force) -and $Backup) {
        $backupDest = "$dest.bak"
        if (Test-Path $backupDest) {
            Remove-Item -Path $backupDest -Recurse -Force
        }
        Move-Item -Path $dest -Destination $backupDest -Force
        Write-Host "  [i] Backed up existing $($skill.Name) -> $backupDest" -ForegroundColor DarkGray
    } elseif ((Test-Path $dest) -and $Force) {
        Remove-Item -Path $dest -Recurse -Force
    }

    Write-Host "[+] Installing skill: $($skill.Name) -> $dest" -ForegroundColor Green
    Copy-Item -Path $skill.FullName -Destination $dest -Recurse -Force
}

# Clean up temp files if created
if ($TempDir -and (Test-Path $TempDir)) {
    Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Successfully installed all $($skills.Count) Vibe UI skills into $TargetDir!" -ForegroundColor Yellow
Write-Host "Commanded by vibe-ui-agent with 70+ components, WCAG AA accessibility, and semantic RTL support." -ForegroundColor Cyan
