import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime


THREADS_DIR = "output/threads"
DIGESTS_DIR = "output/digests"
DEFAULT_DIGEST_MODEL = "qwen2.5:7b"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_DIGEST_MODE = "single"


@dataclass
class DigestItem:
    channel_name: str
    video_id: str
    video_url: str
    title: str
    summary: str
    key_insights: list[str]
    details: str
    notable_quotes: list[str]
    source_path: str


def clean_channel_name(name):
    return re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")


def get_latest_thread_date(threads_dir=THREADS_DIR):
    if not os.path.isdir(threads_dir):
        return None

    dates = [
        name
        for name in os.listdir(threads_dir)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", name)
        and os.path.isdir(os.path.join(threads_dir, name))
    ]
    return max(dates) if dates else None


def _extract_title(content, default_title):
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return default_title


def _extract_summary(content):
    tldr_match = re.search(
        r"\*\*TL;DR:\*\*\s*(.*?)(?:\n\n|###|\Z)", content, flags=re.DOTALL
    )
    if tldr_match:
        return re.sub(r"\s+", " ", tldr_match.group(1)).strip()

    insights_match = re.search(
        r"### .*?Key Insights\s*(.*?)(?:\n###|\Z)", content, flags=re.DOTALL
    )
    if insights_match:
        bullets = [
            re.sub(r"^[*\-\s]+", "", line).strip()
            for line in insights_match.group(1).splitlines()
            if line.strip().startswith(("*", "-"))
        ]
        if bullets:
            return " ".join(bullets[:3])

    return re.sub(r"\s+", " ", content[:800]).strip()


def _extract_section(content, heading_text):
    pattern = rf"### .*?{re.escape(heading_text)}\s*(.*?)(?:\n### |\Z)"
    match = re.search(pattern, content, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def _strip_markdown(text):
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = text.replace("—", "-")
    return re.sub(r"\s+", " ", text).strip()


def _extract_key_insights(content, limit=5):
    section = _extract_section(content, "Key Insights")
    insights = []
    for line in section.splitlines():
        if not line.strip().startswith(("*", "-")):
            continue
        insight = re.sub(r"^[*\-\s]+", "", line).strip()
        insight = _strip_markdown(insight)
        if insight:
            insights.append(insight)
    return insights[:limit]


def _extract_details(content, limit=1400):
    section = _extract_section(content, "Deep Dive") or _extract_section(content, "Conclusion")
    details = _strip_markdown(section)
    return _truncate(details, limit) if details else ""


def _extract_notable_quotes(content, limit=2):
    section = _extract_section(content, "Notable Quotes")
    quotes = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith(">"):
            continue
        quote = _strip_markdown(line.lstrip("> ").strip().strip('"'))
        if quote:
            quotes.append(quote)
    return quotes[:limit]


def _match_channel(file_name, channels):
    for channel in sorted(channels, key=lambda c: len(clean_channel_name(c["name"])), reverse=True):
        prefix = f"{clean_channel_name(channel['name'])}_"
        if file_name.startswith(prefix):
            video_id = file_name[len(prefix) : -3]
            return channel["name"], video_id

    stem = file_name[:-3]
    channel_name, _, video_id = stem.rpartition("_")
    return channel_name.replace("_", " ") or "Unknown", video_id


def load_digest_items(date, config, threads_dir=THREADS_DIR):
    date_dir = os.path.join(threads_dir, date)
    if not os.path.isdir(date_dir):
        return []

    items = []
    channels = config.get("channels", [])
    for file_name in sorted(os.listdir(date_dir)):
        if not file_name.endswith(".md"):
            continue

        path = os.path.join(date_dir, file_name)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        channel_name, video_id = _match_channel(file_name, channels)
        title = _extract_title(content, file_name[:-3].replace("_", " "))
        summary = _extract_summary(content)
        key_insights = _extract_key_insights(content)
        details = _extract_details(content)
        notable_quotes = _extract_notable_quotes(content)
        items.append(
            DigestItem(
                channel_name=channel_name,
                video_id=video_id,
                video_url=f"https://www.youtube.com/watch?v={video_id}",
                title=title,
                summary=summary,
                key_insights=key_insights,
                details=details,
                notable_quotes=notable_quotes,
                source_path=path,
            )
        )

    return items


class DigestGenerator:
    def __init__(self, model=DEFAULT_DIGEST_MODEL, host=DEFAULT_OLLAMA_HOST):
        self.model = model
        self.host = host.rstrip("/")

    def _generate_text(self, prompt, num_ctx=16384, temperature=0.25, timeout=180):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": num_ctx,
                "temperature": temperature,
            },
        }
        request = urllib.request.Request(
            f"{self.host}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data.get("response", "").strip()
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Ollama API error {e.code}: {detail}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Ollama is not reachable at {self.host}: {e}") from e

    def generate_video_brief(self, item):
        insights = "\n".join(f"- {insight}" for insight in item.key_insights)
        quotes = "\n".join(f"- {quote}" for quote in item.notable_quotes)
        prompt = f"""
You are preparing one source brief for an AI-focused Telegram digest.

Use only the source material below. Do not add facts, examples, or claims that are not present.
The goal is to help a reader understand the video without opening YouTube.

Return this exact structure:

## [clean title]
Core thesis:
[2-3 dense sentences]

Key claims:
- [claim 1]
- [claim 2]
- [claim 3]
- [claim 4 if useful]

Concrete examples:
- [specific example, mechanism, or number from the source]
- [specific example, mechanism, or number from the source]

Useful takeaway:
[1 specific implication for builders, investors, operators, or AI-watchers]

Best quote:
[quote if there is a good one, otherwise "No strong quote."]

Source: {item.channel_name} - {item.video_url}

SOURCE
Title: {item.title}
Channel: {item.channel_name}
URL: {item.video_url}
TLDR: {item.summary}
Key insights:
{insights}
Details:
{item.details}
Quotes:
{quotes}
"""
        return self._generate_text(prompt, num_ctx=12000, temperature=0.2)

    def _source_block(self, item, index):
        insights = "\n".join(f"- {insight}" for insight in item.key_insights)
        quotes = "\n".join(f"- {quote}" for quote in item.notable_quotes)
        return "\n".join(
            [
                f"ITEM {index}",
                f"Channel: {item.channel_name}",
                f"Title: {item.title}",
                f"URL: {item.video_url}",
                f"TLDR: {item.summary}",
                f"Key insights:\n{insights}",
                f"Details: {item.details}",
                f"Quotes:\n{quotes}",
            ]
        )

    def generate_single_pass(self, items, date=None, max_items=7):
        if not items:
            return None

        selected = items[:max_items]
        date = date or datetime.now().strftime("%Y-%m-%d")
        source_blocks = [
            self._source_block(item, index)
            for index, item in enumerate(selected, start=1)
        ]

        prompt = f"""
You are an editor for a high-signal Telegram channel about AI, technology, and the future of work.

Create one Telegram-native detailed daily digest from the source material below.

Rules:
- Write in English.
- Be clear, detailed, and editorial, not hypey or vague.
- Cover every source item unless two items substantially overlap.
- Merge overlapping stories instead of repeating them.
- Open with "AI Digest - {date}".
- Add "Today's theme:" with one sentence connecting the videos.
- For each video, include:
  1. short headline
  2. "What the video argues:" with 2-4 sentences of substance
  3. "Key details:" with 3 bullets
  4. "Why it matters:" with a specific, non-generic implication
  5. "Source:" with channel name and URL
- Add "What changed my mind:" with 1-2 bullets.
- Add "What to watch next:" with 1-2 questions.
- End with a short "Bottom line:" that names the common theme.
- Do not invent facts beyond the provided source material.
- Plain Markdown only. No HTML. No introductory explanation.
- Keep the total under 6000 characters.

Source material:
{chr(10).join(source_blocks)}
"""

        return self._generate_text(prompt, num_ctx=12000, temperature=0.3, timeout=120)

    def generate_deep(self, items, date=None, max_items=7):
        if not items:
            return None

        selected = items[:max_items]
        date = date or datetime.now().strftime("%Y-%m-%d")
        briefs = [self.generate_video_brief(item) for item in selected]

        prompt = f"""
You are an editor for a high-signal Telegram channel about AI, technology, and the future of work.

Create one Telegram-native detailed daily digest from the source briefs below.

Rules:
- Write in English.
- Be clear, detailed, and editorial, not hypey.
- Cover every source brief unless two briefs substantially overlap.
- Open with "AI Digest - {date}".
- Add "Today's theme:" with one sentence connecting the videos.
- For each video, include:
  1. short headline
  2. "What the video argues:" with 2-4 sentences of substance
  3. "Key details:" with 3 bullets
  4. "Why it matters:" with a specific, non-generic implication
  5. "Source:" with channel name and URL
- Add "What changed my mind:" with 1-2 bullets.
- Add "What to watch next:" with 1-2 questions.
- End with a short "Bottom line:" that names the common theme.
- Do not invent facts beyond the provided briefs.
- Plain Markdown only. No HTML. No introductory explanation.
- Keep the total under 7000 characters.

Source briefs:
{chr(10).join(briefs)}
"""

        return self._generate_text(prompt, num_ctx=16384, temperature=0.3, timeout=180)

    def generate(self, items, date=None, max_items=7, mode="single"):
        if mode == "deep":
            return self.generate_deep(items, date=date, max_items=max_items)
        return self.generate_single_pass(items, date=date, max_items=max_items)


def save_digest(content, date, output_dir=DIGESTS_DIR):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{date}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")
    return path


def _truncate(text, limit):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def generate_fallback_digest(items, date, max_items=7):
    lines = [f"AI Digest - {date}", ""]

    for index, item in enumerate(items[:max_items], start=1):
        title = re.sub(r"\s*\(\d{4}-\d{2}-\d{2}\)\s*$", "", item.title).strip()
        insights = item.key_insights[:4] or [_truncate(item.summary, 260)]
        lines.extend(
            [
                f"{index}. {title}",
                "",
                "What the video argues:",
                _truncate(item.summary, 520),
                "",
                "Key details:",
            ]
        )

        for insight in insights:
            lines.append(f"- {_truncate(insight, 260)}")

        if item.details:
            lines.extend(["", "More context:", _truncate(item.details, 900)])

        if item.notable_quotes:
            lines.extend(["", "Notable quote:", f"\"{_truncate(item.notable_quotes[0], 300)}\""])

        lines.extend(
            [
                "",
                f"Why it matters: This gives readers the useful substance of the {item.channel_name} video without needing to watch the full episode first.",
                f"Source: {item.channel_name} - {item.video_url}",
                "",
            ]
        )

    lines.extend(
        [
            "Bottom line:",
            "Today's batch points to AI moving deeper into work, infrastructure, and decision-making.",
        ]
    )
    return "\n".join(lines).strip()


def generate_daily_digest(config, date=None, model=None, mode=None):
    model = model or os.getenv("DIGEST_MODEL") or DEFAULT_DIGEST_MODEL
    mode = mode or os.getenv("DIGEST_MODE") or DEFAULT_DIGEST_MODE
    date = date or get_latest_thread_date()
    if not date:
        print("No thread dates found for digest generation.")
        return None, None

    items = load_digest_items(date, config)
    if not items:
        print(f"No thread files found for digest date {date}.")
        return None, None

    try:
        generator = DigestGenerator(model=model)
        digest = generator.generate(items, date=date, mode=mode)
    except Exception as e:
        print(
            f"Ollama digest generation with {model} in {mode} mode failed, "
            f"using fallback digest: {e}"
        )
        digest = generate_fallback_digest(items, date)

    if not digest:
        print("Digest generation returned no content.")
        return None, None

    path = save_digest(digest, date)
    return digest, path
