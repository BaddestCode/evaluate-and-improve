# Tools Setup

> Tools used by `/evaluate-and-improve`. Set up once, then forget about it.

## YouTube Transcript Extraction (Required)

**Tool:** `.claude/skills/evaluate-and-improve/tools/youtube-transcript.py`
**Dependency:** `youtube-transcript-api` (Python package)

### Setup (one-time, ~60 seconds)

```bash
# From your repo root:
python3 -m venv .venv
source .venv/bin/activate
pip install youtube-transcript-api
```

### Usage

The skill calls this automatically. If you need to run it manually:

```bash
source .venv/bin/activate && python3 .claude/skills/evaluate-and-improve/tools/youtube-transcript.py "<URL>" --metadata --max-chars 50000
```

### Options
- `--metadata` - include video title, channel, URL header
- `--max-chars N` - truncate output (default 50000, 0 for unlimited)
- `--json` - structured JSON output with timestamps

### If Python Isn't Available

If you don't have Python 3 installed, the skill will ask you to paste transcripts manually. On YouTube: click '...' below the video > 'Show transcript' > select all > copy.

But the tool is strongly recommended - it handles formatting, truncation, and metadata extraction automatically.

### Known Limitations
- Some creators disable captions - the tool will error with a helpful message
- Auto-generated captions have no punctuation or capitalisation - still readable but rough
- YouTube may rate-limit heavy usage from a single IP

### Fallback
If the tool fails, the skill will ask you to manually copy the transcript from YouTube's built-in "Show transcript" feature.

## GitHub Repo Analysis

No special tools needed - uses `WebFetch` on GitHub's raw content and API URLs:
- README: `https://raw.githubusercontent.com/<owner>/<repo>/main/README.md`
- Metadata: `https://api.github.com/repos/<owner>/<repo>`
- File tree: `https://api.github.com/repos/<owner>/<repo>/git/trees/main?recursive=1`
- Individual files: `https://raw.githubusercontent.com/<owner>/<repo>/main/<path>`

GitHub API has a 60 requests/hour limit for unauthenticated requests. For repos with many files, prioritise: README, CLAUDE.md, SKILL.md files, config files, main logic files.

## Articles & Blog Posts

No special tools needed - uses Claude Code's built-in `WebFetch` tool to read web pages and extract content. Works with any publicly accessible URL.
