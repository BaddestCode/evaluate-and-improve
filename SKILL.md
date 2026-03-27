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

Read `references/evaluation-framework.md` for the full filter definitions. Then, using all three agents' findings, run the source through the five filters below. Most things get caught early - that's by design.

### Filter 1: "Does this touch something I'm actually dealing with?"

Not theoretically relevant. Specifically: is the team wrestling with this problem right now? Is this something they're actively building, maintaining, or trying to improve?

**Using Agent 2's repo understanding:** match the source's capabilities against what the team is actually working on. If the connection requires stretching, it fails this filter.

**If it fails:** The source might be interesting, but it's not addressing anything active. Redirect to **Learn** (store patterns for later) or **Skip** (genuinely irrelevant).

### Filter 2: "Is this actually good?"

This is taste, not a checklist. After reading the source deeply through Agent 1's findings, does the approach feel right?

**Ask yourself:**
- Is this solving a real problem or inventing one?
- Does the technique actually work, or does it just sound clever? Any evidence of production usage?
- Is the star count earned or viral? (A repo that went viral on Twitter for a day is different from one with steady growth.)
- Are there well-known better alternatives? (Agent 3's competitive context helps here.)

**If it fails** (solving an invented problem, no evidence it works, pure hype): fast-track to **Skip**. Write the analysis.md explaining why and move to Step 4. Don't waste time on downstream filters for sources that aren't credible.

### Filter 3: "What specifically would I pinch?"

Be a cherry-picker. Look at the source and name the exact things worth taking. Not "their approach to X" but "their specific technique of doing Y in file Z."

**Create a table:**

| What I'd Pinch | What We Do Now | Why Theirs Is Better |
|----------------|---------------|---------------------|
| <specific technique/pattern> | <our current approach, or "nothing"> | <concrete reason> |
| ... | ... | ... |

**If you can't name anything specific:** the source is interesting but there's nothing concrete to take. Redirect to **Learn** (extract the patterns that might be useful later).

### Filter 4: "Can I see the change?"

Can you literally picture the PR? This is the reality check.

**Write down:**
1. **Files created:** What new files would exist? Where do they go?
2. **Files modified:** Which existing files get edited? What changes?
3. **Dependencies added:** Any new tools, packages, or setup steps?
4. **Config changes:** Does any project config need updating?
5. **Time estimate:** Is this a 30-minute PR or a 3-day refactor?
6. **Risk of breakage:** Could this change break existing workflows? What's the rollback plan?

**If you can't describe the PR:** the verdict is **Learn**. The knowledge is valuable but you're not ready to act on it. Store the patterns.

### Filter 5: "Is the juice worth the squeeze?"

Given the specific change you'd make: is the improvement worth the disruption?

- **Maintenance burden** - who maintains this after it's in? Does it add ongoing complexity?
- **Cognitive load** - would a new team member look at this and be confused?
- **Opportunity cost** - is this the best use of time right now?
- **Reversibility** - can you try it and back out if it doesn't work?

**If it fails:** the improvement is marginal, the disruption is high, or there are more important things to do. Redirect to **Learn** - store the pattern for when the calculus changes.

### Determine Verdict

The verdict comes from where the source lands in the filter chain:

| Where it lands | Verdict |
|---------------|---------|
| Passes all 5 filters. The change is clear, the improvement is significant, and you'd do it this week. | **Adopt** |
| Passes filters 1-4, but needs tailoring. The technique is sound but the context requires modification. | **Adapt** |
| Caught at filter 1 (not active right now), filter 3 (nothing specific to pinch), or filter 4 (can't describe the PR). Source has genuine value worth remembering. | **Learn** |
| Caught at filter 2 (not actually good). Not relevant, not useful, or we already do it better. | **Skip** |

**Critical rule:** The default is Learn or Skip. Adopt is rare - it requires passing every filter with confidence. Most things are interesting but not actionable right now, and that's fine. The learnings folder exists precisely for this.

Write `learnings/<slug>/analysis.md`:

```markdown
# CTO Analysis: <Source Name>

## Filter 1: Does this touch something we're actually dealing with?
<What specific thing in our repo/workflow does this relate to? Are we actively working on it?>

## Filter 2: Is this actually good?
<Taste assessment. Is the approach sound? Evidence it works? Better alternatives? Be blunt.>

## Filter 3: What specifically would I pinch?

| What I'd Pinch | What We Do Now | Why Theirs Is Better |
|----------------|---------------|---------------------|
| <specific thing> | <our approach> | <why> |

<If nothing specific, say so.>

## Filter 4: Can I see the change?
<The PR sketch. Files created, files modified, dependencies, time estimate, risk.>
<If you can't describe it, say so.>

## Filter 5: Is the juice worth the squeeze?
<Disruption vs. improvement. Maintenance burden. Opportunity cost.>

## Verdict: <Adopt/Adapt/Learn/Skip>
**Caught at:** <which filter stopped it, or "passed all">

### Rationale
<3-5 sentences explaining the verdict. Be specific about what tipped the balance.>

### What's Genuinely Better Than What We Have
<Be specific. "Their technique for X solves Y that we currently struggle with because Z.">

### What We Already Do Better
<Don't undervalue existing work. Be honest about where we're already strong.>

### What's Worth Remembering
<Patterns or techniques to file for future reference, even if not acting now.>
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
> **Verdict: <Adopt/Adapt/Learn/Skip>**
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

| Source | Verdict | Filter caught at | Top Insight | Action |
|--------|---------|-----------------|-------------|--------|
| <name> | <verdict> | <filter or "passed all"> | <insight> | <action> |

3. If multiple sources solve the same problem, recommend the best one and explain why
4. Update INDEX.md with all entries

## Error Handling

- **Can't access repo** (private, 404) - ask user to paste the README or key files directly
- **No transcript available** for YouTube - ask user to paste it, or evaluate based on description/linked resources only
- **Source is very large** (>50 files) - focus on README, main config, key logic files, and any CLAUDE.md or SKILL.md equivalents. Note that the review is partial.
- **Source uses tools we can't evaluate** - note the limitation, score Integration Effort lower
- **Multiple similar sources** - compare them and recommend the best fit, noting trade-offs
