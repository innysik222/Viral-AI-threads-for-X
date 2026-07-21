import argparse
import ast
import json
import os
import plistlib
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime


PYTHON_FILES = [
    "main.py",
    "scraper.py",
    "processor.py",
    "digest.py",
    "growth_posts.py",
    "telegram_poster.py",
    "git_sync.py",
]
JSON_FILES = ["channels.json", "telegram_config.example.json"]
PLIST_FILE = "com.ai.viral.snippets.plist"
TELEGRAM_CONFIG = "telegram_config.json"
OLLAMA_HOST = "http://localhost:11434"


def ok(name, detail):
    return ("OK", name, detail)


def warn(name, detail):
    return ("WARN", name, detail)


def fail(name, detail):
    return ("FAIL", name, detail)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_syntax():
    results = []
    for path in PYTHON_FILES:
        if not os.path.exists(path):
            results.append(fail("python syntax", f"{path} is missing"))
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                ast.parse(f.read(), filename=path)
            results.append(ok("python syntax", path))
        except SyntaxError as e:
            results.append(fail("python syntax", f"{path}: {e}"))
    return results


def check_json_files():
    results = []
    for path in JSON_FILES:
        if not os.path.exists(path):
            results.append(fail("json config", f"{path} is missing"))
            continue
        try:
            load_json(path)
            results.append(ok("json config", path))
        except json.JSONDecodeError as e:
            results.append(fail("json config", f"{path}: {e}"))
    return results


def check_channels():
    try:
        config = load_json("channels.json")
    except Exception as e:
        return [fail("channels", str(e))]

    channels = config.get("channels", [])
    last_processed = config.get("last_processed", {})
    missing = [
        index
        for index, channel in enumerate(channels, start=1)
        if not all(channel.get(key) for key in ("name", "id", "url"))
    ]
    results = []
    if channels and not missing:
        results.append(ok("channels", f"{len(channels)} configured"))
    else:
        results.append(fail("channels", f"invalid channel entries: {missing}"))

    if len(last_processed) >= len(channels):
        results.append(ok("last_processed", f"{len(last_processed)} entries"))
    else:
        results.append(warn("last_processed", f"{len(last_processed)} entries for {len(channels)} channels"))
    return results


def check_telegram_config():
    if not os.path.exists(TELEGRAM_CONFIG):
        return [fail("telegram config", f"{TELEGRAM_CONFIG} is missing")]

    try:
        config = load_json(TELEGRAM_CONFIG)
    except Exception as e:
        return [fail("telegram config", str(e))]

    results = []
    bot_token = (config.get("bot_token") or "").strip()
    chat_id = (config.get("chat_id") or "").strip()
    share_chat_id = (config.get("share_chat_id") or "").strip()
    threads_chat_id = (config.get("threads_chat_id") or "").strip()

    if re.match(r"^(bot)?\d+:[A-Za-z0-9_-]+$", bot_token):
        results.append(ok("telegram token", "present and token-shaped"))
    else:
        results.append(fail("telegram token", "missing or malformed"))

    if chat_id and chat_id != "@your_channel_username":
        results.append(ok("digest chat", chat_id))
    else:
        results.append(fail("digest chat", "missing or placeholder"))

    if config.get("auto_post_share") is True:
        if share_chat_id and share_chat_id != "@your_channel_username":
            results.append(ok("share chat", share_chat_id))
        else:
            results.append(ok("share chat", "falls back to digest chat"))

    if config.get("auto_post_threads") is True:
        if threads_chat_id and threads_chat_id != "@your_threads_channel_username":
            results.append(ok("threads chat", threads_chat_id))
        else:
            results.append(fail("threads chat", "auto_post_threads is true but threads_chat_id is missing"))
    else:
        results.append(warn("threads channel", "disabled"))

    results.append(ok("automation config", f"auto_post={config.get('auto_post') is True}, auto_post_share={config.get('auto_post_share') is True}"))
    results.append(ok("models config", f"digest={config.get('digest_model')}, share={config.get('share_model')}, thread={config.get('thread_model')}"))
    return results


def check_outputs():
    results = []
    threads_root = "output/threads"
    if not os.path.isdir(threads_root):
        return [fail("outputs", "output/threads is missing")]

    dates = sorted(
        name
        for name in os.listdir(threads_root)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", name)
        and os.path.isdir(os.path.join(threads_root, name))
    )
    if not dates:
        return [warn("outputs", "no dated thread outputs found")]

    latest = dates[-1]
    latest_dir = os.path.join(threads_root, latest)
    thread_count = len([name for name in os.listdir(latest_dir) if name.endswith(".md")])
    results.append(ok("latest threads", f"{latest}: {thread_count} markdown files"))

    for label, path in [
        ("latest digest", os.path.join("output", "digests", f"{latest}.md")),
        ("latest share post", os.path.join("output", "share_posts", f"{latest}.share.md")),
    ]:
        if os.path.exists(path):
            results.append(ok(label, path))
        else:
            results.append(warn(label, f"{path} not found"))

    return results


def check_plist():
    if not os.path.exists(PLIST_FILE):
        return [warn("launchd plist", f"{PLIST_FILE} missing")]
    try:
        with open(PLIST_FILE, "rb") as f:
            plist = plistlib.load(f)
    except Exception as e:
        return [fail("launchd plist", str(e))]

    args = plist.get("ProgramArguments", [])
    workdir = plist.get("WorkingDirectory")
    schedule = plist.get("StartCalendarInterval", {})
    results = [
        ok("launchd plist", f"label={plist.get('Label')}"),
        ok("launchd command", " ".join(args)),
        ok("launchd workdir", str(workdir)),
        ok("launchd schedule", f"{schedule.get('Hour'):02}:{schedule.get('Minute'):02}"),
    ]
    if workdir and not os.path.isdir(workdir):
        results.append(fail("launchd workdir", f"{workdir} does not exist"))
    return results


def check_launchd_runtime():
    uid = os.getuid()
    label = "com.ai.viral.snippets"
    try:
        result = subprocess.run(
            ["launchctl", "print", f"gui/{uid}/{label}"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except Exception as e:
        return [warn("launchd runtime", f"could not inspect launchd: {e}")]

    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        return [fail("launchd runtime", detail or f"{label} is not loaded")]

    output = result.stdout
    state_match = re.search(r"state = (.*)", output)
    runs_match = re.search(r"runs = (.*)", output)
    exit_match = re.search(r"last exit code = (.*)", output)
    state = state_match.group(1).strip() if state_match else "unknown"
    runs = runs_match.group(1).strip() if runs_match else "unknown"
    exit_code = exit_match.group(1).strip() if exit_match else "unknown"

    results = [ok("launchd runtime", f"loaded, state={state}, runs={runs}, last_exit={exit_code}")]
    if exit_code not in {"0", "unknown"}:
        results.append(warn("launchd last exit", exit_code))
    return results


def request_json(url, timeout=20):
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def post_form(url, payload, timeout=20):
    data = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def check_ollama():
    try:
        data = request_json(f"{OLLAMA_HOST}/api/tags", timeout=10)
    except Exception as e:
        return [fail("ollama", f"not reachable: {e}")]

    models = sorted(model.get("name", "") for model in data.get("models", []))
    try:
        tg_config = load_json(TELEGRAM_CONFIG)
    except Exception:
        tg_config = {}
    required = {
        "qwen2.5:7b",
        tg_config.get("digest_model"),
        tg_config.get("share_model"),
        tg_config.get("thread_model"),
    }
    required = {model for model in required if model}
    missing = sorted(model for model in required if model not in models)

    results = [ok("ollama", f"{len(models)} models available")]
    if missing:
        results.append(fail("ollama models", f"missing: {', '.join(missing)}"))
    else:
        results.append(ok("ollama models", f"required present: {', '.join(sorted(required))}"))
    return results


def check_telegram_api():
    try:
        config = load_json(TELEGRAM_CONFIG)
    except Exception as e:
        return [fail("telegram api", str(e))]

    token = (config.get("bot_token") or "").strip()
    if token.startswith("bot"):
        token = token[3:]
    if not token:
        return [fail("telegram api", "missing bot token")]

    base = f"https://api.telegram.org/bot{token}"
    results = []
    try:
        me = request_json(f"{base}/getMe", timeout=20)
        if me.get("ok"):
            user = me.get("result", {})
            results.append(ok("telegram getMe", f"@{user.get('username')}"))
        else:
            results.append(fail("telegram getMe", str(me)))
    except urllib.error.HTTPError as e:
        results.append(fail("telegram getMe", f"HTTP {e.code}"))
    except Exception as e:
        results.append(fail("telegram getMe", str(e)))

    chat_ids = [("digest chat", config.get("chat_id"))]
    if config.get("auto_post_share") is True:
        chat_ids.append(("share chat", config.get("share_chat_id") or config.get("chat_id")))
    if config.get("auto_post_threads") is True:
        chat_ids.append(("threads chat", config.get("threads_chat_id")))

    for label, chat_id in chat_ids:
        if not chat_id or str(chat_id).startswith("@your_"):
            results.append(fail(label, "missing or placeholder"))
            continue
        try:
            response = post_form(f"{base}/getChat", {"chat_id": chat_id}, timeout=20)
            if response.get("ok"):
                chat = response.get("result", {})
                results.append(ok(label, f"{chat.get('type')} {chat.get('title') or chat.get('username') or chat_id}"))
            else:
                results.append(fail(label, str(response)))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            results.append(fail(label, f"HTTP {e.code}: {detail}"))
        except Exception as e:
            results.append(fail(label, str(e)))
    return results


def print_results(results):
    severity_order = {"FAIL": 0, "WARN": 1, "OK": 2}
    for status, name, detail in sorted(results, key=lambda row: (severity_order[row[0]], row[1])):
        print(f"[{status}] {name}: {detail}")


def main():
    parser = argparse.ArgumentParser(description="Healthcheck the AI viral snippets pipeline")
    parser.add_argument("--network", action="store_true", help="Check Ollama and Telegram APIs")
    args = parser.parse_args()

    results = []
    results.extend(check_syntax())
    results.extend(check_json_files())
    results.extend(check_channels())
    results.extend(check_telegram_config())
    results.extend(check_outputs())
    results.extend(check_plist())
    results.extend(check_launchd_runtime())

    if args.network:
        results.extend(check_ollama())
        results.extend(check_telegram_api())
    else:
        results.append(warn("network checks", "skipped; run with --network"))

    print(f"Pipeline healthcheck at {datetime.now().isoformat(timespec='seconds')}")
    print_results(results)

    has_fail = any(status == "FAIL" for status, _, _ in results)
    sys.exit(1 if has_fail else 0)


if __name__ == "__main__":
    main()
