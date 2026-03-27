# Evaluate & Improve

You watch a YouTube video about some clever workflow trick. You see a GitHub repo with 10k stars doing something your project kind of does, but differently. Someone drops a blog post in Slack about a new approach to memory management. And you think: *"That's smart. Would that actually help me, though?"*

Figuring that out properly takes ages. You'd need to deeply understand what the source is doing, deeply understand your own setup, map one against the other, and make an honest call about whether the juice is worth the squeeze. Most people either skip it entirely or spend an hour down a rabbit hole and come out with "maybe?"

This is a Claude Code skill that does that analysis for you. One command, any source.

## What it does

Drop in a GitHub repo, YouTube video, or article. The skill:

1. **Learns your repo first.** On first run, it reads your README, CLAUDE.md, package.json, docs, architecture files - whatever's available. It builds the same understanding a CTO would have after their first week at your company. What you're building, how work flows, what tools you use, what you're trying to achieve.

2. **Deeply researches the source.** Three parallel agents tear apart the repo, video, or article. Not a skim - it reads source files, pulls YouTube transcripts, follows linked resources, checks the author's credibility, and looks at what the community thinks.

3. **Makes the honest call.** It maps the source's capabilities against your actual setup. Not "this is cool" but "this is better than what we already do for X, and here's the concrete PR to adopt it." Built-in protection against wasting your time: it won't recommend changes unless it has high confidence they're a genuine improvement for your specific context. Most things get filed as useful knowledge, not action items.

## Your learnings compound

Every evaluation gets stored as structured files in a `learnings/` folder. This matters more than it sounds.

Three months from now, you're refactoring your memory system and you vaguely remember that repo someone shared about context management. Instead of searching your browser history, you check `learnings/INDEX.md`. There it is - the full analysis, the specific patterns worth remembering, and exactly when you'd want to revisit it.

The skill builds a **patterns library** over time. Each evaluation extracts reusable techniques - tagged by what they solve, how they work, and when they'd become relevant. Your team's knowledge about external approaches accumulates in one searchable place.

## Install (~2 minutes)

### 1. Copy the skill into your repo

```bash
# From your repo root:
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/baddest-code/evaluate-and-improve.git
```

Or download and copy manually - the skill is just files, no build step.

Your structure should look like:

```
.claude/skills/evaluate-and-improve/
  SKILL.md
  references/
    evaluation-framework.md
    tools-setup.md
  tools/
    youtube-transcript.py
```

### 2. Set up YouTube transcript extraction

```bash
# From your repo root:
python3 -m venv .venv
source .venv/bin/activate
pip install youtube-transcript-api
```

This lets the skill automatically pull transcripts from YouTube videos. If Python isn't available, you can paste transcripts manually, but the tool is strongly recommended.

### 3. You're done

The skill auto-discovers your repo on first use. No configuration needed.

## Usage

In Claude Code, say any of:

- `/evaluate-and-improve https://github.com/someone/cool-repo`
- `evaluate this: https://youtube.com/watch?v=...`
- `what can we learn from https://blog.example.com/some-article`
- `check this out: <paste a README or transcript>`

### First run

On first use, the skill creates a `learnings/` folder at your repo root with an INDEX.md. This is where all evaluations are stored.

### What happens

1. **Three parallel agents** deeply analyse the source, your repo, and the competitive context
2. **Smell test** catches hype, invented problems, and weak evidence
3. **Capability mapping** compares the source's approach to your current setup
4. **Concrete PR planning** - before deciding on a verdict, it sketches what adoption would actually look like. If it can't describe the PR, the answer is "learn, don't act"
5. **Verdict** with structured output in `learnings/<slug>/`

## The four verdicts

| Verdict | What it means | How often |
|---------|--------------|-----------|
| **Adopt** | This is genuinely better than what you have. Here's the implementation plan. 95%+ confidence. | Rare |
| **Adapt** | Parts of this are valuable, but your setup needs a tailored version. Here's what to take and what to leave. | Occasional |
| **Learn** | Smart stuff in here. Nothing to change right now, but the patterns are filed for when they become relevant. | Most common |
| **Skip** | Not useful for what you're doing. Brief note so nobody re-evaluates it later. | Common |

**The default is Learn or Skip.** The skill is protective of your time. It won't tell you to adopt something just because it's popular or clever. It needs to see that the source genuinely improves something you're actively doing, with a clear path to integration, before it recommends action. A CTO who says "yes" to everything isn't a good CTO.

## Output structure

For each evaluation, the skill creates:

```
learnings/<source-slug>/
  summary.md              - what the source does, metadata, key stats
  analysis.md             - deep CTO review with scores and capability mapping
  recommendations.md      - verdict, patterns to remember, implementation plan (if warranted)
```

Plus an entry in `learnings/INDEX.md` with a patterns library that grows over time.

## How it handles different sources

### GitHub Repos
Reads the README, file tree, key source files, and metadata via GitHub's API. Analyses architecture, patterns, documentation quality, and maintenance status.

### YouTube Videos
Extracts transcripts automatically using the included Python tool. Analyses techniques discussed, follows linked repos/resources, and evaluates the creator's credibility. Falls back to manual paste if captions are disabled.

### Articles & Blog Posts
Uses Claude Code's `WebFetch` to read the full page. Extracts key techniques, referenced tools, and actionable patterns. Follows links to any repos or tools mentioned.

## Scoring criteria

| Criterion | Weight | What it measures |
|-----------|--------|-----------------|
| Relevance | 2x | Does this help you do something you're actively doing, faster or better? |
| Quality | 2x | Documentation, maintenance, community, code quality |
| Freshness | 1x | How recent? Using current tools and approaches? |
| Integration Effort | 1x | Drop-in vs. requires restructuring your workflows |
| Signal Strength | 1x | Author credibility, stars, trusted recommendations |

## Customisation

The skill auto-discovers your repo by reading README.md, CLAUDE.md, package.json, and any docs or architecture files it can find. No configuration file needed.

If you want to influence the evaluation:
- A good **README.md** helps the skill understand what your project does
- A **CLAUDE.md** helps it understand your workflows and tool stack
- The skill reads whatever context is available and adapts

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
- Python 3.8+ (for YouTube transcripts)
- `youtube-transcript-api` package (installed via pip)

## License

MIT
