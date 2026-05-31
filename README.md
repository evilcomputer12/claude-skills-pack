# claude-skills-pack

One-command installer for a curated pack of **Claude Code skills and subagents**.

It fetches each upstream source and installs:

- **skills** → `~/.claude/skills/` (each is a folder containing a `SKILL.md`)
- **subagents** → `~/.claude/agents/` (each is a Markdown file with `name`/`description` front-matter)

Total: **~185 skills** and **~153 subagents** across the sources below.

---

## Quick start

### PowerShell (Windows / pwsh)

```powershell
# clone, then run
git clone https://github.com/evilcomputer12/claude-skills-pack.git
cd claude-skills-pack
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Or one-liner (downloads + runs):

```powershell
irm https://raw.githubusercontent.com/evilcomputer12/claude-skills-pack/main/install.ps1 | iex
```

> The one-liner installs from upstream repos but **skips the bundled `perplexity-search` skill**
> (that one lives only in this repo). Clone the repo if you want it.

Then **restart Claude Code** to load everything.

### Options

```powershell
.\install.ps1 -SkillsDir D:\custom\skills -AgentsDir D:\custom\agents
.\install.ps1 -WhatIf      # preview without copying
```

---

## What gets installed

| Source | Type | Count | Notes |
|--------|------|------:|-------|
| [`anthropics/skills`](https://github.com/anthropics/skills) | skills | ~17 | Official Anthropic skills (docx, pdf, pptx, xlsx, frontend-design, mcp-builder, skill-creator, …). Installed **last** so it wins name collisions. |
| [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills) | skills | ~143 | Science / bio / chem / ML (rdkit, qiskit, scanpy, biopython, matplotlib, …). |
| [`obra/superpowers`](https://github.com/obra/superpowers) | skills | ~14 | Workflow skills (TDD, systematic-debugging, brainstorming, writing-plans, git-worktrees, …). |
| [`nextlevelbuilder/ui-ux-pro-max-skill`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | skills | 7 | UI/UX & design (`banner-design`, `brand`, `design`, `design-system`, `slides`, `ui-styling`, `ui-ux-pro-max`). |
| [`netresearch/file-search-skill`](https://github.com/netresearch/file-search-skill) | skills | 1 | Fast codebase search (ripgrep / ast-grep / fd / rga / tokei / scc). |
| **`perplexity-search`** (bundled in `bundled/`) | skill | 1 | AI web search via Perplexity through OpenRouter. No upstream repo — shipped here directly. |
| [`VoltAgent/awesome-claude-code-subagents`](https://github.com/VoltAgent/awesome-claude-code-subagents) | agents | ~153 | Subagents across core-dev, language specialists, infrastructure, **cybersec**, **sysadmin**, **mobile**, data/AI, and more. |

---

## How it works

`install.ps1`:

1. Creates `~/.claude/skills` and `~/.claude/agents` if missing.
2. For each **skill repo**, clones it (`git clone --depth 1`, with a zip-download fallback) and
   copies **every folder that contains a `SKILL.md`** into the skills directory. This handles all
   upstream layouts automatically — root-level, `skills/*`, and `.claude/skills/*`.
3. For the **agent repo**, copies every `*.md` under `categories/` (excluding READMEs and
   `.claude-plugin/`) into the agents directory, flattened.
4. Skips scaffolding folders named `template` / `example-skill`.
5. Is **idempotent** — re-run any time to update to the latest upstream versions.

### Collision handling

A few skill names exist in more than one source (e.g. `docx`, `pdf`, `pptx`, `xlsx`).
The script installs the Anthropic pack last, so its official versions take precedence.

---

## Requirements

- **Windows PowerShell 5.1+** or **PowerShell 7+**
- **git** (recommended). Without git, the script falls back to downloading branch zips.
- **Claude Code** (skills/agents are read from `~/.claude/`).

Some individual skills need extra tooling at run time (e.g. `file-search` wants `ripgrep`;
`perplexity-search` needs an OpenRouter API key — see `bundled/perplexity-search/references/`).

---

## Using it with Claude (prompt)

Prefer to have Claude do the install conversationally? See **[`INSTALL_PROMPT.md`](INSTALL_PROMPT.md)** —
paste it into Claude Code and it will fetch and install everything for you.

---

## Uninstall

Skills and agents are plain folders/files:

```powershell
# remove a single skill
Remove-Item "$HOME\.claude\skills\<skill-name>" -Recurse -Force
# remove a single agent
Remove-Item "$HOME\.claude\agents\<agent-name>.md" -Force
```

---

## Credits

All skills and subagents belong to their respective authors/repositories (linked above).
This repo only provides the installer and bundles the `perplexity-search` skill that has no
upstream home. Licenses are those of each source project.
