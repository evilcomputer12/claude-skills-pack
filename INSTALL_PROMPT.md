# Claude install prompt

Paste the block below into **Claude Code** (on the machine where you want the skills).
Claude will fetch each source and install the skills and subagents into `~/.claude/`.

---

```text
You are installing a curated pack of Claude Code skills and subagents onto this machine.

Targets:
- Skills  -> ~/.claude/skills/   (each skill is a folder containing SKILL.md)
- Agents  -> ~/.claude/agents/   (each agent is a single .md file with name/description front-matter)

Do this:

1. Create ~/.claude/skills and ~/.claude/agents if they do not exist.

2. For each SKILL repo below: clone it shallow (git clone --depth 1), then copy EVERY folder
   that contains a SKILL.md into ~/.claude/skills/ (folder name = skill name). This handles
   root-level, skills/*, and .claude/skills/* layouts. Skip any folder named "template" or
   "example-skill". Install the Anthropic repo LAST so its docx/pdf/pptx/xlsx win name collisions.

     - K-Dense-AI/scientific-agent-skills      (~143 science/bio/chem/ML skills)
     - obra/superpowers                        (~14 workflow skills)
     - nextlevelbuilder/ui-ux-pro-max-skill    (7 UI/UX skills, under .claude/skills/)
     - netresearch/file-search-skill           (1 codebase-search skill, under skills/)
     - anthropics/skills                        (~17 official skills, under skills/) -- LAST

3. For the AGENT repo below: copy every *.md under its categories/ directory (EXCLUDING any
   README files and anything under .claude-plugin/) into ~/.claude/agents/, flattened
   (file name unchanged). Skip duplicate file names.

     - VoltAgent/awesome-claude-code-subagents  (~153 subagents: mobile, cybersec, sysadmin, ...)

4. The "perplexity-search" skill has NO upstream repo. If a ./bundled/perplexity-search folder
   is present next to this prompt, copy it into ~/.claude/skills/ too; otherwise skip it.

5. Clean up any temp clone directories.

6. Print a summary: number of skills installed, number of agents installed, and note that
   Claude Code must be restarted to load them.

Use the platform shell. On Windows use PowerShell. Be idempotent (overwrite existing copies).
```

---

## Shortcut

If you cloned this repo, you don't need Claude at all — just run the script:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
