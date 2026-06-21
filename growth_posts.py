import os
import re

from digest import DEFAULT_DIGEST_MODEL, DigestGenerator


SHARE_POSTS_DIR = "output/share_posts"
THREAD_POSTS_DIR = "output/thread_posts"


def _truncate(text, limit):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def save_post(content, date, output_dir, suffix):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{date}.{suffix}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")
    return path


def generate_share_post(digest, date, model=None):
    model = model or DEFAULT_DIGEST_MODEL
    prompt = f"""
You are writing one Telegram-native conversation starter based on a daily AI digest.

Use only the digest below. Do not invent new facts.

Goal:
- Make one sharp idea from the digest easy to forward.
- It should feel like a thoughtful channel post, not an X/Twitter thread.
- It should invite replies if the Telegram channel has discussion enabled.

Rules:
- No numbered thread format.
- No clickbait.
- No hashtags.
- No links.
- No markdown heading.
- 2 short paragraphs plus one discussion question.
- The question must be specific and answerable, not generic.
- Plain text only.
- Keep it under 900 characters.

Preferred shape:
[A sharp observation in 1-2 sentences]

[Why this observation matters in 2-3 sentences]

Question: [specific discussion question]

Avoid:
- "Here is..."
- "In today's digest..."
- "What do you think?"
- generic engagement bait.
- No hashtags.

Digest date: {date}

Digest:
{digest}
"""
    try:
        generator = DigestGenerator(model=model)
        return generator._generate_text(prompt, num_ctx=8000, temperature=0.45, timeout=90)
    except Exception as e:
        print(f"Share post generation with {model} failed, using fallback: {e}")
        return generate_fallback_share_post(digest)


def generate_fallback_share_post(digest):
    theme_match = re.search(r"Today's theme:\s*(.*)", digest)
    theme = theme_match.group(1).strip() if theme_match else ""
    changed_match = re.search(
        r"What changed my mind:?\s*(.*?)(?:\n#+\s*What to watch next|\nWhat to watch next|\Z)",
        digest,
        flags=re.DOTALL,
    )
    changed = changed_match.group(1).strip() if changed_match else ""

    lines = ["The useful AI signal today is not another model demo."]
    if theme:
        lines.extend(["", _truncate(theme, 300)])
    if changed:
        first_bullet = next(
            (
                re.sub(r"^[*\-\s]+", "", line).strip()
                for line in changed.splitlines()
                if line.strip().startswith(("*", "-"))
            ),
            "",
        )
        if first_bullet:
            lines.extend(["", _truncate(first_bullet, 300)])

    lines.extend(
        [
            "",
            "Question: Which bottleneck matters more over the next year: model capability, data efficiency, or the disappearance of entry-level work?",
        ]
    )
    return "\n".join(lines).strip()


def _extract_title(content, default="AI discussion"):
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return default


def _extract_tldr(content):
    match = re.search(r"\*\*TL;DR:\*\*\s*(.*?)(?:\n\n|###|\Z)", content, flags=re.DOTALL)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


def _extract_key_insights(content, limit=5):
    match = re.search(r"### .*?Key Insights\s*(.*?)(?:\n###|\Z)", content, flags=re.DOTALL)
    if not match:
        return []

    insights = []
    for line in match.group(1).splitlines():
        if not line.strip().startswith(("*", "-")):
            continue
        insight = re.sub(r"^[*\-\s]+", "", line).strip()
        insight = re.sub(r"\*\*(.*?)\*\*", r"\1", insight)
        if insight:
            insights.append(insight)
    return insights[:limit]


def _extract_deep_dive(content, limit=1800):
    match = re.search(r"### .*?Deep Dive\s*(.*?)(?:\n### |\Z)", content, flags=re.DOTALL)
    if not match:
        return ""
    deep_dive = re.sub(r"^#+\s*", "", match.group(1), flags=re.MULTILINE)
    deep_dive = re.sub(r"\*\*(.*?)\*\*", r"\1", deep_dive)
    return _truncate(deep_dive, limit)


def generate_thread_discussion_post(thread_path, model=None):
    model = model or DEFAULT_DIGEST_MODEL
    with open(thread_path, "r", encoding="utf-8") as f:
        content = f.read()

    title = _extract_title(content)
    tldr = _extract_tldr(content)
    insights = _extract_key_insights(content)
    deep_dive = _extract_deep_dive(content)
    insights_text = "\n".join(f"- {insight}" for insight in insights)

    prompt = f"""
You are writing a Telegram channel post designed to start discussion.

Use only the source material below. Do not invent facts.

Goal:
- Make readers understand the video's central tension.
- Invite thoughtful replies from builders, researchers, founders, and AI-watchers.
- Do not write an X/Twitter thread.

Return this exact structure:

[One-line provocative but accurate claim]

Context:
[2-4 sentences explaining the actual argument]

The tension:
[1-2 sentences naming the tradeoff, uncertainty, or disagreement]

Question:
[One specific question that people can answer in comments]

Source: [video title]

Rules:
- No hashtags.
- No numbered thread format.
- No "what do you think?"
- No generic engagement bait.
- Keep it under 1800 characters.
- Plain text only.

Source material:
Title: {title}
TLDR: {tldr}
Key insights:
{insights_text}
Deep dive:
{deep_dive}
"""
    try:
        generator = DigestGenerator(model=model)
        return generator._generate_text(prompt, num_ctx=10000, temperature=0.4, timeout=90)
    except Exception as e:
        print(f"Discussion post generation with {model} failed, using fallback: {e}")
        return generate_fallback_thread_discussion_post(title, tldr, insights)


def generate_fallback_thread_discussion_post(title, tldr, insights):
    lines = [title]
    if tldr:
        lines.extend(["", "Context:", _truncate(tldr, 420)])
    if insights:
        lines.extend(["", "The tension:", _truncate(insights[0], 300)])
    lines.extend(
        [
            "",
            "Question:",
            "Which part of this argument is most likely to be wrong: the timeline, the technical assumption, or the economic incentive?",
            "",
            f"Source: {title}",
        ]
    )
    return "\n".join(lines).strip()


def extract_viral_thread(thread_path):
    with open(thread_path, "r", encoding="utf-8") as f:
        content = f.read()

    title = "AI thread"
    for line in content.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    match = re.search(
        r"## .*?VIRAL THREAD\s*(.*?)(?:\n---\s*\n\n## |\Z)",
        content,
        flags=re.DOTALL,
    )
    if not match:
        return None

    section = match.group(1).strip()
    posts = []
    for post_match in re.finditer(
        r"Post\s+(\d+):\s*(.*?)(?=\n---\s*\nPost\s+\d+:|\nPost\s+\d+:|\Z)",
        section,
        flags=re.DOTALL,
    ):
        number = post_match.group(1)
        text = re.sub(r"\s+", " ", post_match.group(2)).strip()
        if text:
            posts.append(f"{number}/ {text}")

    if not posts:
        cleaned = re.sub(r"\n---\s*", "\n\n", section).strip()
        return f"{title}\n\n{cleaned}" if cleaned else None

    return f"{title}\n\n" + "\n\n".join(posts)


def save_thread_post(content, thread_path, date):
    base_name = os.path.splitext(os.path.basename(thread_path))[0]
    os.makedirs(THREAD_POSTS_DIR, exist_ok=True)
    path = os.path.join(THREAD_POSTS_DIR, f"{date}.{base_name}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")
    return path
