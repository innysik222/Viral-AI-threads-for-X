import json
import os
import urllib.error
import urllib.parse
import urllib.request


TELEGRAM_LIMIT = 4096
CONFIG_PATH = "telegram_config.json"


def split_message(text, limit=3900):
    paragraphs = text.strip().split("\n\n")
    chunks = []
    current = ""

    for paragraph in paragraphs:
        candidate = paragraph if not current else f"{current}\n\n{paragraph}"
        if len(candidate) <= limit:
            current = candidate
            continue

        if current:
            chunks.append(current)
            current = ""

        while len(paragraph) > limit:
            chunks.append(paragraph[:limit].rstrip())
            paragraph = paragraph[limit:].lstrip()

        current = paragraph

    if current:
        chunks.append(current)

    return chunks


def load_telegram_config(config_path=CONFIG_PATH):
    if not os.path.exists(config_path):
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _is_missing(value):
    return not value or value in {
        "paste_bot_token_here",
        "@your_channel_username",
        "your_channel_id_or_username",
    }


def _normalize_bot_token(value):
    if not value:
        return value

    value = value.strip()
    if value.startswith("bot") and len(value) > 3 and value[3].isdigit():
        return value[3:]
    return value


def _normalize_chat_id(value):
    return value.strip() if isinstance(value, str) else value


def post_to_telegram(text, bot_token=None, chat_id=None, parse_mode=None, config_path=CONFIG_PATH):
    config = load_telegram_config(config_path)
    bot_token = bot_token or config.get("bot_token") or os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or config.get("chat_id") or os.getenv("TELEGRAM_CHAT_ID")
    bot_token = _normalize_bot_token(bot_token)
    chat_id = _normalize_chat_id(chat_id)

    if _is_missing(bot_token):
        raise ValueError(
            "Missing Telegram bot token. Set TELEGRAM_BOT_TOKEN or paste it into telegram_config.json."
        )
    if _is_missing(chat_id):
        raise ValueError(
            "Missing Telegram chat id. Set TELEGRAM_CHAT_ID or paste it into telegram_config.json."
        )

    sent = []
    for chunk in split_message(text, TELEGRAM_LIMIT - 200):
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "disable_web_page_preview": True,
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode

        data = urllib.parse.urlencode(payload).encode("utf-8")
        request = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data=data,
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                sent.append(json.loads(response.read().decode("utf-8")))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            if e.code == 404:
                raise RuntimeError(
                    "Telegram API error 404: bot token was not accepted. "
                    "Check bot_token in telegram_config.json."
                ) from e
            raise RuntimeError(f"Telegram API error {e.code}: {detail}") from e

    return sent
