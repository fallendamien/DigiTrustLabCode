# Change Propagation Protocol

> When user requests ANY policy/style/standard change, auto-scan all related files and apply everywhere — never make the user ask "also update X."

---

## When to Activate

| Trigger Pattern | Example User Message | Action |
|----------------|---------------------|--------|
| "update the policy" / "change the policy" | "Update the voice policy to..." | Ripple scan + apply to all related files |
| "new rule" / "add a rule" | "Add a new rule for italicizing English terms" | Ripple scan + apply to all related files |
| "update our docs" / "update everything" | "Update our whole doc for this policy" | Ripple scan + apply to all related files |
| "also update" / "don't forget to update" | User had to remind agent → LESSON | Agent failed to propagate — fix immediately |
| "wtf, update the rest" / "why didn't you update X" | User frustrated about missed files | Agent failed to propagate — fix immediately |
| Style/visual change to live content | "Change the blockquote style" | Ripple scan docs + apply to all Bricks elements that use it |
| Voice/language standard change | "We're now using semi-formal BM" | Ripple scan ALL docs + ALL WordPress content |
| Formatting rule change | "Always use blockquote for notes" | Ripple scan docs + check all live pages for existing notes |
| "remember to always" / "from now on" | "Remember to always use that blockquote style" | Ripple scan + apply to all related files + docs |
| "update the workflow" / "update the skill" | "Update our workflow on this" | Ripple scan + apply to all related files |

**Rule:** If ANY trigger pattern appears, do NOT ask "should I also update X?" — just DO IT.

---

## The 4-Step Process

### Step 1: Ripple Scan
Before making the first edit, scan ALL documentation files that could reference or depend on the changed policy:

| Scan Target | How to Find | What to Look For |
|-------------|-------------|------------------|
| `AGENTS.md` | Always check | Voice rules, style policies, section summaries |
| `.devin/skills/*/SKILL.md` | `find_by_name SKILL.md` | Any skill that references the policy domain |
| `.devin/rules/*.md` | `find_by_name *.md` in `.devin/rules/` | Operational rules that enforce the policy |
| `.windsurf/rules/*.md` | `find_by_name *.md` in `.windsurf/rules/` | Behavioral rules that reference the policy |
| `content/content-calendar.md` | Direct read | Writer notes, briefs that reference the policy |
| `ROADMAP.md`, `NEXT.md`, `STATE.json` | Direct read | Any references to the old standard |
| WordPress content (via Respira MCP) | Check pages/posts that may contain the old style | Live content that needs updating |

### Step 2: Build the Change Set
List every file + the specific edit needed. Present to user as a quick table BEFORE executing:

```
Policy change: [description]
Files to update:
1. AGENTS.md — update section X
2. malay-voice-guide/SKILL.md — update section Y
3. content-calendar.md — update note for writer
4. WordPress Post #1 — italicize terms
```

### Step 3: Execute ALL Changes
Apply every edit in the change set. Do NOT stop after one file and wait. Do NOT make the user ask "also update X."

### Step 4: Verify
Confirm each file was updated. For WordPress content, purge cache and verify live.

---

## When NOT to Trigger

| User Says | Ripple Scan Required? |
|-----------|----------------------|
| "Fix this one typo in this one file" | ❌ No — single file fix |
| "Change this button color" | ❌ No — single element fix |

---

## Anti-Pattern (NEVER do this)

```
❌ User: "Add italic policy for English terms"
❌ Agent: *updates SKILL.md only*
❌ Agent: "Done!"
❌ User: "wtf, update the rest too"
❌ Agent: *updates AGENTS.md only*
❌ User: "and the writerzen skill??"
```

**Instead:**

```
✅ User: "Add italic policy for English terms"
✅ Agent: *scans all docs, finds 4 files + Post #1 need updating*
✅ Agent: "I'll update: SKILL.md, AGENTS.md, WriterZen SKILL.md, content-calendar.md, and Post #1. Proceeding."
✅ Agent: *updates all 5 in sequence*
✅ Agent: "All done. Here's what changed."
```

**The user should NEVER have to ask "also update X." That's the agent's job.**
