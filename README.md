# Evaluate & Improve

**Stop bookmarking repos you'll never revisit.** One command turns any GitHub repo, YouTube video, or article into a structured verdict: adopt it, adapt it, learn from it, or skip it.

```bash
# Install in 30 seconds:
mkdir -p .claude/skills && cd .claude/skills && git clone https://github.com/baddest-code/evaluate-and-improve.git
```

Then in Claude Code: `evaluate this https://github.com/someone/cool-repo`

---

## The problem

The rate of new tools, workflows, and techniques is relentless. Every week there's a repo with 10k stars, a YouTube video showing a clever trick, a blog post about a better way to handle context or memory or prompts. You watch it and think: *"That's smart. Would that actually help me with what I'm doing?"*

Answering that properly is a 30-minute job minimum. You'd need to deeply read the source, deeply understand your own setup, map one against the other, and make an honest call. Most people either skip it (and miss genuine improvements) or go down the rabbit hole and come out with "maybe?"

## What this does

**One command. Any source. A CTO-grade verdict in minutes.**

1. **It learns your repo first.** Reads your README, CLAUDE.md, package.json, architecture docs - whatever exists. It builds the same understanding a CTO would have after a week at your company: what you're building, how work flows, what you're trying to achieve.

2. **It deeply researches the source.** Three parallel agents pull apart the repo, video, or article. Not a skim - it reads source files, pulls full YouTube transcripts natively (no API key needed), follows linked resources, and checks what the community thinks. For YouTube, it uses a built-in transcript tool that the YouTube API doesn't offer - it grabs auto-generated captions directly.

3. **It protects your time.** The built-in bias is towards "not much to do here." It won't recommend changes just because something is popular or clever. It needs to see that the source genuinely improves something you're actively doing, frequently, with a clear path to integration. A CTO who says "yes" to everything isn't a good CTO.

## Your learnings compound

Every evaluation gets stored as structured files in a `learnings/` folder. This is the part that matters most over time.

Three months from now you're improving your memory system and you think: "What was that thing I saw about context management?" Instead of searching your browser history, you check `learnings/INDEX.md`. The full analysis is there - the specific patterns, how they work, and when you'd want to revisit them.

The skill builds a **patterns library** that grows with every evaluation. Each one extracts reusable techniques tagged by what they solve and when they'd become relevant. Your team's external knowledge accumulates in one searchable place. Not bookmarks. Not "I'll remember." Actual structured reference you'll use.

## Install

### Quick setup (~60 seconds)

```bash
# From your repo root:
mkdir -p .claude/skills && cd .claude/skills
git clone https://github.com/baddest-code/evaluate-and-improve.git

# YouTube transcript support (recommended):
cd ../.. && python3 -m venv .venv && source .venv/bin/activate && pip install youtube-transcript-api
```

That's it. The skill auto-discovers your repo on first use. No config file, no API keys.

### What you get

```
.claude/skills/evaluate-and-improve/
  SKILL.md                          # The skill itself
  references/evaluation-framework.md # Scoring criteria and verdict thresholds
  references/tools-setup.md          # Tool setup reference
  tools/youtube-transcript.py        # YouTube transcript extraction (no API key needed)
```

## Usage

```
evaluate this https://github.com/someone/cool-repo
evaluate this https://youtube.com/watch?v=abc123
what can we learn from https://blog.example.com/article
```

On first run, it creates `learnings/` with an INDEX.md. Every evaluation after that adds to it.

## How it works

1. **Three parallel agents** deeply analyse the source, your repo, and the competitive landscape
2. **Smell test** catches hype, invented problems, and sources that sound clever but lack evidence
3. **Capability mapping** compares what the source does against your current approach
4. **Concrete PR planning** - before deciding, it sketches what adoption would actually look like. If it can't describe the PR, the answer is "learn, don't act"
5. **Verdict** with full analysis in `learnings/<slug>/`

## The four verdicts

| Verdict | What it means | How often |
|---------|--------------|-----------|
| **Adopt** | This is genuinely better than what you have. Here's the implementation plan. 95%+ confidence. | Rare |
| **Adapt** | Parts of this are valuable. Here's what to take, what to leave, and how to tailor it. | Occasional |
| **Learn** | Smart patterns in here. Nothing to change now, but filed for when they become relevant. | Most common |
| **Skip** | Not useful for what you're doing. Noted so nobody re-evaluates it later. | Common |

## Sources it handles

| Source | How it works |
|--------|-------------|
| **GitHub repos** | Reads README, file tree, key source files, and metadata via GitHub API |
| **YouTube videos** | Extracts full transcripts natively using built-in tool (no API key). Follows linked repos and resources |
| **Articles & blogs** | Reads the full page via WebFetch. Follows referenced tools and repos |

## Scoring

| Criterion | Weight | What it measures |
|-----------|--------|-----------------|
| Relevance | 2x | Does this improve something you're actively doing, frequently? |
| Quality | 2x | Is this genuinely a good approach, or are there better ways? |
| Freshness | 1x | How recent? Using current tools? |
| Integration Effort | 1x | Drop-in vs. requires restructuring |
| Signal Strength | 1x | Author credibility, community reception |

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
- Python 3.8+ with `youtube-transcript-api` (for YouTube transcripts)

## License

MIT
