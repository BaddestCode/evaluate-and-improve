#!/usr/bin/env python3
"""
Fetch YouTube transcript as clean text.

Usage:
    python3 tools/youtube-transcript.py <url_or_video_id> [--max-chars 50000] [--json]

Outputs clean text by default (just the spoken words, no timestamps).
Use --json for structured output with timestamps.
Use --max-chars to limit output size for context efficiency.

Requires: pip install youtube-transcript-api (installed in .venv)
"""

import sys
import re
import json
import argparse


def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube video ID from various URL formats or return as-is if already an ID."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def fetch_transcript(video_id: str, languages: list[str] | None = None) -> list[dict]:
    """Fetch transcript for a video. Tries English first, falls back to auto-generated."""
    from youtube_transcript_api import YouTubeTranscriptApi

    ytt_api = YouTubeTranscriptApi()

    if languages is None:
        languages = ["en", "en-GB", "en-US"]

    try:
        transcript = ytt_api.fetch(video_id, languages=languages)
        return [{"text": snippet.text, "start": snippet.start, "duration": snippet.duration} for snippet in transcript]
    except Exception:
        # Fall back to listing available transcripts and picking the first one
        transcript_list = ytt_api.list(video_id)
        for t in transcript_list:
            try:
                transcript = t.fetch()
                return [{"text": snippet.text, "start": snippet.start, "duration": snippet.duration} for snippet in transcript]
            except Exception:
                continue
        raise RuntimeError(f"No transcripts available for video {video_id}")


def transcript_to_text(transcript: list[dict], max_chars: int = 0) -> str:
    """Convert transcript to clean readable text. Joins lines into paragraphs."""
    lines = [entry["text"] for entry in transcript]
    # Join into flowing text, replacing newlines within entries
    text = " ".join(line.replace("\n", " ") for line in lines)
    # Clean up multiple spaces
    text = re.sub(r" {2,}", " ", text).strip()

    if max_chars > 0 and len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[Transcript truncated at {max_chars} characters. Full length: {len(text)} characters]"

    return text


def get_video_metadata(video_id: str) -> dict:
    """Get basic video metadata from the page (title, channel) without API key."""
    import urllib.request
    import html

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="replace")

        title_match = re.search(r'<title>(.*?)</title>', content)
        title = html.unescape(title_match.group(1).replace(" - YouTube", "").strip()) if title_match else "Unknown"

        channel_match = re.search(r'"ownerChannelName":"(.*?)"', content)
        channel = channel_match.group(1) if channel_match else "Unknown"

        return {"title": title, "channel": channel, "video_id": video_id, "url": f"https://www.youtube.com/watch?v={video_id}"}
    except Exception:
        return {"title": "Unknown", "channel": "Unknown", "video_id": video_id, "url": f"https://www.youtube.com/watch?v={video_id}"}


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript as clean text")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--max-chars", type=int, default=50000, help="Max characters (0 for unlimited, default 50000)")
    parser.add_argument("--json", action="store_true", help="Output as JSON with timestamps")
    parser.add_argument("--metadata", action="store_true", help="Include video metadata header")
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        transcript = fetch_transcript(video_id)
    except Exception as e:
        error_msg = str(e)
        if "no longer available" in error_msg.lower() or "Could not retrieve" in error_msg:
            print(f"Error: No transcript available for this video.", file=sys.stderr)
            print(f"This usually means captions are disabled by the creator.", file=sys.stderr)
            print(f"Workaround: paste the transcript manually (many browsers can copy from the '...' > 'Show transcript' button on YouTube).", file=sys.stderr)
        else:
            print(f"Error fetching transcript: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        if args.metadata:
            metadata = get_video_metadata(video_id)
            output = {"metadata": metadata, "transcript": transcript}
        else:
            output = transcript
        print(json.dumps(output, indent=2))
    else:
        output_parts = []

        if args.metadata:
            metadata = get_video_metadata(video_id)
            output_parts.append(f"# {metadata['title']}")
            output_parts.append(f"**Channel:** {metadata['channel']}")
            output_parts.append(f"**URL:** {metadata['url']}")
            output_parts.append("")

        text = transcript_to_text(transcript, max_chars=args.max_chars)
        output_parts.append(text)
        print("\n".join(output_parts))


if __name__ == "__main__":
    main()
