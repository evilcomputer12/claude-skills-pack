#Requires -Version 5.1
<#
.SYNOPSIS
    Fetches and installs a curated pack of Claude Code skills and subagents.

.DESCRIPTION
    Clones (or downloads) each upstream source, then copies:
      - every skill (a folder containing SKILL.md) into  ~/.claude/skills/
      - every subagent (a Markdown file with name/description front-matter)
        into ~/.claude/agents/  (flattened)

    Idempotent: re-running overwrites existing copies with the latest version.
    Skill name collisions are resolved by install order (later sources win);
    Anthropic's official skills are installed LAST so their docx/pdf/pptx/xlsx
    take precedence over any same-named skills from other packs.

.PARAMETER SkillsDir
    Target skills directory. Default: ~/.claude/skills

.PARAMETER AgentsDir
    Target agents directory. Default: ~/.claude/agents

.PARAMETER WhatIf
    Show what would be installed without copying anything.

.EXAMPLE
    pwsh -File install.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File install.ps1 -SkillsDir D:\skills
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$SkillsDir = (Join-Path $HOME ".claude\skills"),
    [string]$AgentsDir = (Join-Path $HOME ".claude\agents")
)

$ErrorActionPreference = 'Stop'
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# --- Sources -----------------------------------------------------------------
# Skill repos are processed top-to-bottom; the official Anthropic pack is last
# so it wins any skill-name collisions (docx/pdf/pptx/xlsx).
$SkillRepos = @(
    @{ Repo = 'K-Dense-AI/scientific-agent-skills'; Note = '~143 scientific / bio / chem / ML skills' }
    @{ Repo = 'obra/superpowers';                   Note = '~14 workflow skills (TDD, debugging, planning...)' }
    @{ Repo = 'nextlevelbuilder/ui-ux-pro-max-skill'; Note = '7 UI/UX & design skills' }
    @{ Repo = 'netresearch/file-search-skill';      Note = '1 codebase-search skill' }
    @{ Repo = 'anthropics/skills';                  Note = '~17 official Anthropic skills (installed last)' }
)

$AgentRepos = @(
    @{ Repo = 'VoltAgent/awesome-claude-code-subagents'; Note = '~153 subagents (mobile, cybersec, sysadmin, ...)' }
)

# Skills shipped inside this repo (no upstream URL available).
$BundledSkills = Join-Path $ScriptRoot 'bundled'

# Folder names that look like skills but are scaffolding / templates.
$SkillExclude = @('template', '.template', 'example-skill')

# ----------------------------------------------------------------------------

$haveGit = [bool](Get-Command git -ErrorAction SilentlyContinue)

function Write-Step { param($m) Write-Host "==> $m" -ForegroundColor Cyan }
function Write-Ok   { param($m) Write-Host "    $m" -ForegroundColor Green }
function Write-Warn2{ param($m) Write-Host "    $m" -ForegroundColor Yellow }

function Get-Source {
    <# Clone (preferred) or download a GitHub repo into a temp dir; returns its path. #>
    param([string]$Repo, [string]$Dest)

    if ($haveGit) {
        git clone --depth 1 "https://github.com/$Repo.git" $Dest 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) { return $Dest }
        Write-Warn2 "git clone failed for $Repo, falling back to zip download"
    }

    foreach ($branch in @('main', 'master')) {
        $zip = "$Dest.zip"
        try {
            Invoke-WebRequest -Uri "https://github.com/$Repo/archive/refs/heads/$branch.zip" `
                -OutFile $zip -UseBasicParsing -ErrorAction Stop
            Expand-Archive -Path $zip -DestinationPath $Dest -Force
            Remove-Item $zip -Force
            # GitHub zips nest everything under <repo>-<branch>/
            $inner = Get-ChildItem $Dest -Directory | Select-Object -First 1
            return $inner.FullName
        } catch { }
    }
    throw "Could not fetch $Repo (tried git + main/master zip)."
}

function Install-Skill {
    param([System.IO.DirectoryInfo]$Dir)
    if ($SkillExclude -contains $Dir.Name.ToLower()) { return $false }
    $dst = Join-Path $SkillsDir $Dir.Name
    if ($PSCmdlet.ShouldProcess($Dir.Name, 'install skill')) {
        if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
        Copy-Item $Dir.FullName $dst -Recurse -Force
    }
    return $true
}

# --- Prep --------------------------------------------------------------------
New-Item -ItemType Directory -Force -Path $SkillsDir, $AgentsDir | Out-Null
$work = Join-Path ([System.IO.Path]::GetTempPath()) ("claude-skills-pack-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $work | Out-Null
Write-Host "Skills -> $SkillsDir"
Write-Host "Agents -> $AgentsDir`n"

$totalSkills = 0
$totalAgents = 0

try {
    # --- Bundled skills ------------------------------------------------------
    if (Test-Path $BundledSkills) {
        Write-Step "Installing bundled skills"
        Get-ChildItem $BundledSkills -Recurse -Filter SKILL.md | ForEach-Object {
            if (Install-Skill $_.Directory) { $totalSkills++; Write-Ok "skill: $($_.Directory.Name)" }
        }
    }

    # --- Skill repos ---------------------------------------------------------
    foreach ($src in $SkillRepos) {
        Write-Step "Fetching $($src.Repo)  ($($src.Note))"
        $dir = Get-Source -Repo $src.Repo -Dest (Join-Path $work ($src.Repo -replace '/', '_'))
        $found = 0
        Get-ChildItem $dir -Recurse -Filter SKILL.md | ForEach-Object {
            if (Install-Skill $_.Directory) { $found++; $totalSkills++ }
        }
        Write-Ok "installed $found skills from $($src.Repo)"
    }

    # --- Agent repos ---------------------------------------------------------
    foreach ($src in $AgentRepos) {
        Write-Step "Fetching $($src.Repo)  ($($src.Note))"
        $dir = Get-Source -Repo $src.Repo -Dest (Join-Path $work ($src.Repo -replace '/', '_'))
        $catRoot = Join-Path $dir 'categories'
        if (-not (Test-Path $catRoot)) { $catRoot = $dir }
        $seen = @{}; $found = 0
        Get-ChildItem $catRoot -Recurse -Filter *.md |
            Where-Object { $_.Name -notmatch '(?i)readme' -and $_.FullName -notmatch '\.claude-plugin' } |
            ForEach-Object {
                if ($seen.ContainsKey($_.Name)) { return }
                $seen[$_.Name] = $true
                if ($PSCmdlet.ShouldProcess($_.Name, 'install agent')) {
                    Copy-Item $_.FullName (Join-Path $AgentsDir $_.Name) -Force
                }
                $found++; $totalAgents++
            }
        Write-Ok "installed $found agents from $($src.Repo)"
    }
}
finally {
    Remove-Item $work -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host ("  Skills installed/updated: {0}  (total in dir: {1})" -f $totalSkills, (Get-ChildItem $SkillsDir -Directory).Count)
Write-Host ("  Agents installed/updated: {0}  (total in dir: {1})" -f $totalAgents, (Get-ChildItem $AgentsDir -Filter *.md).Count)
Write-Host "`nRestart Claude Code to load the new skills and agents." -ForegroundColor Yellow
