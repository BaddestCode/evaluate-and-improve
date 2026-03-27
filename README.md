# Evaluate & Improve

A Claude Code skill that acts as a sceptical CTO, peer-reviewing external GitHub repos, YouTube videos, and articles against the goals of whatever repo it's installed in.

It scores sources on 5 dimensions, delivers one of four verdicts (Adopt / Adapt / Learn / Skip), and stores structured learnings your team can reference later. Built-in bias towards "not much to do here" - only recommends changes at high confidence.

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
4. **Scoring** against 5 weighted criteria (relevance, quality, freshness, integration effort, signal strength)
5. **Concrete PR planning** sketches what adoption would actually look like before deciding
6. **Verdict** with structured output in `learnings/<slug>/`

## The Four Verdicts

| Verdict | What it means | Composite score | How often |
|---------|--------------|-----------------|-----------|
| **Adopt** | Use as-is or near-verbatim. 95%+ confidence it's better than what you have. | 4.0+ with no conflicts | Rare |
| **Adapt** | Valuable, but your context needs modifications. Comes with a specific tailoring plan. | 3.0+ with minor/no conflicts | Occasional |
| **Learn** | Useful knowledge stored for future reference. No immediate changes. | 2.0+ | Most common |
| **Skip** | Not relevant right now. Brief note so you don't re-evaluate later. | <2.0 or major conflicts | Common |

The default is Learn or Skip. The skill is deliberately hard to impress.

## Output Structure

For each evaluation, the skill creates:

```
learnings/<source-slug>/
  summary.md              - what the source does, metadata, key stats
  analysis.md             - deep CTO review with scores and capability mapping
  recommendations.md      - verdict, patterns to remember, implementation plan (if warranted)
```

Plus an entry in `learnings/INDEX.md` with a patterns library that grows over time.

## How It Handles Different Sources

### GitHub Repos
Reads the README, file tree, key source files, and metadata via GitHub's API. Analyses architecture, patterns, documentation quality, and maintenance status.

### YouTube Videos
Extracts transcripts automatically using the included Python tool. Analyses techniques discussed, follows linked repos/resources, and evaluates the creator's credibility. Falls back to manual paste if captions are disabled.

### Articles & Blog Posts
Uses Claude Code's `WebFetch` to read the full page. Extracts key techniques, referenced tools, and actionable patterns. Follows links to any repos or tools mentioned.

## Scoring Criteria

| Criterion | Weight | What it measures |
|-----------|--------|-----------------|
| Relevance | 2x | Does this solve a problem you actually have? |
| Quality | 2x | Documentation, maintenance, community, code quality |
| Freshness | 1x | How recent? Using current tools/approaches? |
| Integration Effort | 1x | Drop-in vs. requires restructuring |
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
