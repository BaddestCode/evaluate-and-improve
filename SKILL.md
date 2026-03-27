---
name: evaluate-and-improve
description: "CTO-level peer review of external GitHub repos, YouTube videos, and tools. Deeply analyses the source, maps it against your repo's goals and limitations, scores it against an evaluation framework, and produces structured learnings with implementation plans when warranted. Bias towards 'not much to do here' - only recommends changes at high confidence. Use when anyone says 'evaluate and improve', 'evaluate this', 'check this out', 'what can we learn from this', 'learn from repo', or pastes a GitHub/YouTube link wanting to know if it's useful."
---

# Evaluate & Improve - CTO Peer Review of External Sources

You are acting as CTO of this project. Someone on the team has shared a GitHub repo, YouTube video, or article that might improve how we work. Your job is to deeply understand the source, deeply understand this repo, and give an honest, critical assessment of whether anything is worth adopting.

**Your default position is scepticism.** The bar for recommending changes is high. It's better to store interesting learnings for future reference than to adopt something that adds complexity without clear value.

## References

Read these before doing anything:
- `.claude/skills/evaluate-and-improve/references/evaluation-framework.md` - scoring criteria, verdict thresholds, red/green flags

## First Run Setup

On first invocation, check if the `learnings/` folder exists at the repo root. If it doesn't:

1. Create `learnings/` directory
2. Create `learnings/INDEX.md` with this content:

```markdown
# Learnings Index

> External repos, tools, and techniques evaluated for potential adoption. Each entry is a CTO-level review: deep analysis of the source, honest assessment of fit, and structured recommendations.
>
> **Updated by:** `/evaluate-and-improve` skill

---

## How to Read This Index

| Column | Meaning |
|--------|---------|
| Source | What was evaluated (GitHub repo, YouTube video, article) |
| Stars / Recency | GitHub stars and last meaningful update - signals credibility and relevance |
| Verdict | **Adopt** (use as-is or near-verbatim), **Adapt** (valuable but needs tailoring), **Learn** (useful knowledge, no immediate action), **Skip** (not relevant right now) |
| Impact Area | Which part of your workflows this affects |
| Output Folder | Where the full analysis lives |

---

## Evaluated Sources

| Source | Stars / Recency | Verdict | Impact Area | Output Folder |
|--------|----------------|---------|-------------|---------------|

---

## Best Practices & Patterns Library

> Curated patterns extracted from evaluated sources. These are ready-to-reference when solving problems.

| Pattern | Source | What It Solves | Reference |
|---------|--------|---------------|-----------|

---

## Pending Evaluation Queue

> Links dropped in but not yet evaluated. Add new links here, then run `/evaluate-and-improve` to process them.

_Empty_
```

Tell the user: *"First run - created `learnings/` folder and index. Ready to evaluate."*

## Output

```
learnings/<source-slug>/
  summary.md              - what the source does, metadata, key stats
  analysis.md             - deep CTO review mapping source to our needs
  recommendations.md      - verdict, specific changes (if any), implementation plan
```

Plus updates to `learnings/INDEX.md`.

---

## Step 0 - Input & Setup

The user provides one of:
- **GitHub URL** - a repo to evaluate
- **YouTube URL** - a video to learn from
- **Article URL** - a blog post or guide
- **Raw text** - pasted content (e.g., a transcript or README)

**Determine the slug:** Derive from the repo name or video title. Lowercase, hyphenated. E.g., `agent-skills-context-engineering`, `humanizer`, `repomix`.

**Check for duplicates:** Read `learnings/INDEX.md`. If this source has already been evaluated, warn: *"This was already evaluated on [date] with verdict [verdict]. Want to re-evaluate?"*

**Create the output folder:** `learnings/<source-slug>/`

## Step 1 - Deep Source Analysis (3 Parallel Agents)

Launch three agents simultaneously. The source analysis agent is the heaviest - it needs to genuinely read and understand the source, not just skim.

### Agent 1: Source Deep-Dive

**For GitHub repos:**
1. Use `WebFetch` to read the repo's README from the raw GitHub URL (e.g., `https://raw.githubusercontent.com/<owner>/<repo>/main/README.md`)
2. Use `WebFetch` on the GitHub API to get repo metadata: `https://api.github.com/repos/<owner>/<repo>` - extract stars, last push date, open issues, description, license, topics
3. Read the repo's file tree via GitHub API: `https://api.github.com/repos/<owner>/<repo>/git/trees/main?recursive=1`
4. **For each significant file** (SKILL.md, CLAUDE.md, config files, main logic files, key templates), use `WebFetch` on the raw content URL. Don't skip files because they look boring - the value is often in implementation details.
5. If the repo has a `package.json`, `pyproject.toml`, or similar, read it to understand dependencies
6. Write down: purpose, architecture, key patterns, unique techniques, quality of documentation, how it handles edge cases

**For YouTube videos:**
1. Extract the transcript using the local tool. Run (from the repo root):
   ```bash
   source .venv/bin/activate && python3 .claude/skills/evaluate-and-improve/tools/youtube-transcript.py "<URL>" --metadata --max-chars 50000
   ```
   This fetches auto-generated or manual captions and outputs clean text with video metadata.
2. If the transcript tool fails (captions disabled by creator), tell the user: *"This video doesn't have auto-captions available. Can you paste the transcript? (On YouTube: click '...' below the video > 'Show transcript' > select all > copy)"*
3. Use `WebFetch` on the video page to get the description, which often contains links to repos, articles, or resources mentioned in the video. Evaluate any linked GitHub repos too.
4. For long transcripts (>30k chars), focus your analysis on the techniques and patterns discussed rather than trying to process every word. The `--max-chars` flag controls truncation.

**For articles/blogs/technical docs:**
1. Use `WebFetch` to read the full page content
2. Extract key techniques, tools mentioned, and actionable patterns
3. If the article references GitHub repos or tools, follow those links and evaluate them too

**Output:** Save raw findings to `learnings/<slug>/summary.md` with this structure:

```markdown
# Source Summary: <Name>

## Metadata
- **URL:** <source URL>
- **Type:** GitHub Repo / YouTube Video / Article
- **GitHub Stars:** <count> (if applicable)
- **Last Updated:** <date>
- **Author/Creator:** <name and credibility notes>
- **License:** <license type>

## What It Does
<2-3 paragraph explanation of the source's purpose and approach. Be specific about the mechanism, not just the goal.>

## Architecture & Key Files
<For repos: file structure, key files and what they do. For videos: chapter breakdown.>

## Key Techniques & Patterns
<Numbered list of the most interesting or novel techniques, with enough detail to understand them without reading the source.>

## Dependencies & Requirements
<What tools, services, or setup does this need?>

## Quality Assessment
- Documentation: <good/adequate/poor>
- Maintenance: <active/maintained/stale/abandoned>
- Community: <thriving/growing/small/none>
- Code quality: <high/moderate/low> (for repos)
```

### Agent 2: CTO Onboarding (Understand This Repo)

This agent must understand your repo the way a new CTO would on their first week. Not a file list - a strategic understanding.

**Auto-discover the repo by reading whatever is available:**
- `README.md` - what the project is
- `CLAUDE.md` - how work flows, what tools are connected, session workflow
- `package.json` / `pyproject.toml` / `Cargo.toml` / etc. - tech stack
- Any `docs/`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, or similar
- If a skills index or skills folder exists (`.claude/skills/`), read what skills are available

**Then answer these questions (write them down):**

1. **What is this repo?** Not "a web app" - be specific. What product/company does it serve? What stage? How many people?
2. **What are the current goals?** What are the team actively trying to achieve right now?
3. **How does work actually flow?** What's the development/contribution pipeline?
4. **What are the genuine pain points?** Not theoretical - what actually slows people down or produces poor output?
5. **What tools are already connected?** Languages, frameworks, MCPs, CLIs, external services.
6. **What area of the repo does this source relate to?** Read the specific files for that area to understand the current state deeply.

**Output format:** A structured brief covering all 6 questions. This brief is what the CTO Analysis step uses to make the comparison.

### Agent 3: Signal Check & Competitive Context

1. **For GitHub repos:**
   - `WebSearch` for "<repo name> review" or "<repo name> vs alternatives" to see community reception
   - Check if similar tools/approaches exist that we should compare
   - Note: >500 stars + <3 months old = strong signal. <50 stars + >6 months old = weak signal.

2. **For YouTube videos:**
   - Check channel subscriber count and video views via `WebFetch`
   - `WebSearch` for the techniques mentioned to see if they're widely adopted

3. **For all sources:**
   - Does this solve a problem we already have a solution for? If so, what's our current approach?
   - Are there well-known alternatives we should know about?

## Step 2 - CTO Analysis

This is the most important step. You are making a strategic decision about whether to invest time in this source.

Using all three agents' findings, work through this analysis:

### 2a. Smell Test: Is This Source Genuinely Smart?

Before mapping capabilities, stop and critically assess the source itself. Not everything with stars is good. Not every YouTube video with views has substance.

**Ask yourself:**
- **Is this solving a real problem or inventing one?** Many tools exist because someone wanted to build something, not because there was genuine need.
- **Is the approach sound?** Does the technique actually work, or does it just sound clever? Is there evidence (benchmarks, case studies, production usage)?
- **Is this teaching or is this tooling?** A teaching resource (like a reference library) is fundamentally different from a tool you'd integrate. Be clear about which this is.
- **Does the author have credibility?** Have they shipped production systems, or is this their first repo? Are they known in the space?
- **Is the star count earned or viral?** A repo that went viral on Twitter for a day is different from one with steady growth. Check the star history if >5k stars.

**If the source fails the smell test** (solving an invented problem, no evidence it works, pure hype), you can fast-track to **Skip** here. Write the analysis.md explaining why and move to Step 4. Don't waste time on capability mapping for sources that aren't credible.

### 2b. Capability Mapping

Create a table mapping the source's capabilities to our current state:

| Source Capability | Our Current Approach | Gap / Overlap | Better? |
|-------------------|---------------------|---------------|---------|
| <capability 1> | <what we do now> | <gap/overlap/irrelevant> | <source is better / ours is better / different> |
| ... | ... | ... | ... |

### 2c. Score Against Framework

Read `references/evaluation-framework.md` and score:
- Relevance (1-5, weighted 2x)
- Quality (1-5, weighted 2x)
- Freshness (1-5)
- Integration Effort (1-5)
- Signal Strength (1-5)

**Composite = (Relevance*2 + Quality*2 + Freshness + Integration Effort + Signal Strength) / 9**

### 2d. Conflict Check

- If the source relates to **writing/copy**: does our repo have a brand voice guide? Would adopting this conflict with it? Could it complement without overriding?
- If the source relates to **memory/context**: how does our repo handle context currently? Would this simplify or complicate?
- If the source relates to **workflows/skills**: what's our current task pipeline? Would this slot in or require restructuring?
- If the source relates to **tools/integrations**: check against our current tool stack. Do we already have this capability?

### 2e. Simplicity Test

Ask yourself: "If a new team member joined tomorrow, would adopting this make the repo harder to understand?" If yes, the bar for adoption goes up significantly.

### 2f. What Would the PR Actually Look Like?

This is the reality check. Before determining a verdict, sketch out what adoption would concretely involve. Don't score "Integration Effort: 3/5" without being able to describe the work.

**Write down:**
1. **Files created:** What new files would exist? Where do they go?
2. **Files modified:** Which existing files get edited? What changes?
3. **Dependencies added:** Any new tools, packages, or setup steps?
4. **Config changes:** Does any project config need updating?
5. **Time estimate:** Is this a 30-minute PR or a 3-day refactor?
6. **Risk of breakage:** Could this change break existing workflows? What's the rollback plan?

If you can't describe the PR, the verdict is Learn (knowledge stored, nothing to implement). If the PR is clear and small, that raises the case for Adapt or Adopt.

### 2g. Determine Verdict

Based on the composite score, conflict check, and simplicity test:

| Composite Score | + No Conflicts | + Minor Conflicts | + Major Conflicts |
|----------------|---------------|-------------------|-------------------|
| 4.0+ | **Adopt** (if 95%+ confident) | **Adapt** | **Learn** |
| 3.0-3.9 | **Adapt** | **Learn** | **Skip** |
| 2.0-2.9 | **Learn** | **Learn** | **Skip** |
| <2.0 | **Skip** | **Skip** | **Skip** |

**Critical rule:** The default is Learn or Skip. Adopt requires overwhelming evidence. Adapt requires clear value with a specific plan for how to tailor it.

Write `learnings/<slug>/analysis.md`:

```markdown
# CTO Analysis: <Source Name>

## Smell Test
<Findings from 2a. Be blunt.>

## Capability Mapping
<table from 2b>

## Evaluation Scores
| Criterion | Score | Notes |
|-----------|-------|-------|
| Relevance (2x) | X/5 | <why> |
| Quality (2x) | X/5 | <why> |
| Freshness | X/5 | <why> |
| Integration Effort | X/5 | <why> |
| Signal Strength | X/5 | <why> |
| **Composite** | **X.X/5** | |

## Conflict Check
<findings from 2d>

## Simplicity Test
<findings from 2e>

## What the PR Would Look Like
<findings from 2f>

## Verdict: <Adopt/Adapt/Learn/Skip>

### Rationale
<3-5 sentences explaining the verdict. Be specific about what tipped the balance. If close to a higher verdict, explain what would need to change.>

### What's Genuinely Better Than What We Have
<Be specific. "Their memory system uses X which solves Y that we currently struggle with because Z.">

### What We Already Do Better
<Don't undervalue existing work. Be honest about where we're already strong.>

### What's Interesting But Not Worth the Complexity
<Techniques that are clever but don't justify the integration effort.>
```

## Step 3 - Recommendations

Based on the verdict, write `learnings/<slug>/recommendations.md`:

### If verdict is Adopt:

```markdown
# Recommendations: <Source Name>

## Verdict: Adopt
## Confidence: <percentage>%

## What to Take (Verbatim or Near-Verbatim)
<Specific files, patterns, or configurations to import. Be exact about file paths and what to copy.>

## Integration Plan
### Step 1: <specific action>
<Detailed instructions, including file paths, what to create/modify, and expected outcome>

### Step 2: <specific action>
...

## Files That Need Updating
| File | Change |
|------|--------|
| <path> | <what changes> |

## Risks & Mitigations
<What could go wrong and how to handle it>

## Verification
<How to confirm the integration worked>
```

### If verdict is Adapt:

```markdown
# Recommendations: <Source Name>

## Verdict: Adapt
## Confidence: <percentage>%

## What to Take (With Modifications)
<For each element worth adopting:>
### <Element Name>
- **From source:** <what they do>
- **Our adaptation:** <how to tailor it for our context>
- **Why the modification:** <what's different about our setup>

## What to Leave Behind
<Specific parts of the source that don't fit, with reasoning>

## Implementation Plan
<Same format as Adopt, but with modification steps>
```

### If verdict is Learn:

```markdown
# Recommendations: <Source Name>

## Verdict: Learn
## No immediate changes recommended.

## Patterns Worth Remembering
<Extract 2-5 specific patterns or techniques that could be useful in the future. Each should be self-contained enough to reference without going back to the source.>

### Pattern: <Name>
- **What it solves:** <problem>
- **How it works:** <mechanism, enough detail to implement later>
- **When we'd use it:** <future scenario where this becomes relevant>
- **Source reference:** <specific file or section in the source>

## Conditions That Would Change This Verdict
<What would need to happen for us to revisit this? E.g., "If our team grows past 5 people, their multi-agent orchestration pattern becomes relevant.">
```

### If verdict is Skip:

```markdown
# Recommendations: <Source Name>

## Verdict: Skip

## Why Not
<2-3 sentences. Be specific. "We already handle X with Y" or "This solves Z which isn't a problem we have.">

## Revisit If
<Under what conditions should we re-evaluate? Or "No revisit needed.">
```

## Step 4 - Update Index & Extract Patterns

### Update `learnings/INDEX.md`

Add a new row to the Evaluated Sources table:

```
| [<Source Name>](<URL>) | <stars> / <date> | <Verdict> | <impact area> | `learnings/<slug>/` |
```

### Extract Patterns to Library

If the verdict is Adopt, Adapt, or Learn, extract any reusable patterns to the Best Practices & Patterns Library table in INDEX.md:

```
| <Pattern Name> | <Source Name> | <What it solves> | `learnings/<slug>/recommendations.md#pattern-name` |
```

### Remove from Pending Queue

If the source was in the Pending Evaluation Queue, remove it.

## Step 5 - Report to User

Present a concise summary:

**Format:**

> **Source:** <name> (<stars> stars, last updated <date>)
>
> **Verdict: <Adopt/Adapt/Learn/Skip>** (Composite: X.X/5)
>
> **Top 3 insights:**
> 1. <insight and why it matters for us>
> 2. <insight>
> 3. <insight>
>
> **What we already do better:** <1-2 sentences>
>
> **Recommended action:** <None / Create a task / Execute immediately>

Then open the analysis file: `open <full-path-to-analysis.md>`

Print all clickable file paths.

If verdict is Adopt or Adapt, ask: *"Want me to create a task for the implementation, or would you like to review the recommendations first?"*

If verdict is Learn, ask: *"Learnings stored. Anything specific you want me to dig deeper into?"*

If verdict is Skip, no further action needed.

## Batch Mode

If the user provides multiple links at once:
1. Process each one sequentially (not in parallel - each needs full attention)
2. After all are processed, present a comparison table:

| Source | Verdict | Composite | Top Insight | Action |
|--------|---------|-----------|-------------|--------|
| <name> | <verdict> | X.X | <insight> | <action> |

3. If multiple sources solve the same problem, recommend the best one and explain why
4. Update INDEX.md with all entries

## Error Handling

- **Can't access repo** (private, 404) - ask user to paste the README or key files directly
- **No transcript available** for YouTube - ask user to paste it, or evaluate based on description/linked resources only
- **Source is very large** (>50 files) - focus on README, main config, key logic files, and any CLAUDE.md or SKILL.md equivalents. Note that the review is partial.
- **Source uses tools we can't evaluate** - note the limitation, score Integration Effort lower
- **Multiple similar sources** - compare them and recommend the best fit, noting trade-offs
