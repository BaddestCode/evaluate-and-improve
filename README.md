# Evaluate & Improve

You see a clever repo. Watch a smart video. Read a blog post with a technique you've never tried. And you think: *"That's smart... would that actually help me with what I'm building?"*

Answering that properly takes 30 minutes minimum. So you bookmark it. You never come back.

**Evaluate & Improve** is a Claude Code skill that does that work for you.

```bash
# One command to install:
mkdir -p .claude/skills && cd .claude/skills && git clone https://github.com/BaddestCode/evaluate-and-improve.git
```

```
# One command to run:
evaluate this <github-url / youtube-url / article-url>
```

---

## What it does

**1. Learns your repo first**

First run, it reads your README, CLAUDE.md, package.json, architecture docs — whatever's there. Same context a CTO would absorb in their first week at your company: your goals, your stack, how your team works. Done in one command.

**2. Deeply researches the source**

Three parallel agents pull apart the repo, video, or article. Not a skim — it reads actual source files, not just the README. Pulls full YouTube transcripts natively, with no API key and no copy-pasting. (The YouTube API doesn't offer transcripts. This tool grabs auto-generated captions directly — it's genuinely unusual.)

**3. Filters with built-in protection over your time**

Not a hype machine. The built-in bias is towards "not much to do here." It only recommends a change when there's something specific worth pinching, a clear PR to write, and confidence the disruption is worth it. A CTO who says yes to everything isn't a good CTO.

## Your learnings don't disappear

Every evaluation gets stored in a `learnings/` folder. Six months later you're improving your memory system and think: *"What was that context management pattern I read about?"* Your learnings index has the answer — the specific technique, why it was filed, and when you'd use it.

You might not need it today. The best CTOs have incredible recall — they remember things exist when the right problem surfaces. This is that, but searchable.

## Install

### Quick setup (~60 seconds)

```bash
# From your repo root:
mkdir -p .claude/skills && cd .claude/skills
git clone https://github.com/BaddestCode/evaluate-and-improve.git

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
2. **Five filters** - the same way a great CTO actually thinks: is this relevant to what I'm doing? Is it actually good? What specifically would I pinch? Can I picture the PR? Is it worth the disruption?
3. **Most things get caught early.** If the source is hype, filter 2 catches it. Interesting but vague? Filter 3. Can't describe the change? Filter 4.
4. **Verdict** with full analysis in `learnings/<slug>/`

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

## How it decides

No arbitrary scoring formula. The skill runs the source through five filters, the same way a great CTO actually thinks:

| Filter | The question | If it fails |
|--------|-------------|-------------|
| **1. Active problem?** | Does this touch something you're actually dealing with right now? | Learn or Skip |
| **2. Actually good?** | Is the approach sound, or is it hype? Any evidence it works in production? | Fast-track to Skip |
| **3. What would I pinch?** | Name the specific techniques worth taking. Not "generally interesting" - specific. | Learn |
| **4. Can I see the change?** | Can you picture the PR? What files change? How long? | Learn |
| **5. Worth the disruption?** | Is the improvement worth the maintenance burden and cognitive load? | Learn |

Most things get caught early. That's by design.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
- Python 3.8+ with `youtube-transcript-api` (for YouTube transcripts)

## License

MIT
