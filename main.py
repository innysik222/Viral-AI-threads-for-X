import json
import os
import argparse
import subprocess
from datetime import datetime
from scraper import get_latest_video_info, fetch_transcript, save_transcript
from digest import generate_daily_digest
from growth_posts import (
    SHARE_POSTS_DIR,
    generate_thread_discussion_post,
    generate_share_post,
    save_post,
    save_thread_post,
)
from telegram_poster import load_telegram_config, post_to_telegram

def load_config(config_path="channels.json"):
    with open(config_path, "r") as f:
        return json.load(f)

def save_config(config, config_path="channels.json"):
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

def load_automation_settings():
    settings = load_telegram_config()
    return {
        "auto_post": settings.get("auto_post") is True,
        "auto_post_share": settings.get("auto_post_share") is True,
        "auto_post_threads": settings.get("auto_post_threads") is True,
        "share_chat_id": settings.get("share_chat_id"),
        "threads_chat_id": settings.get("threads_chat_id"),
        "digest_model": settings.get("digest_model"),
        "digest_mode": settings.get("digest_mode"),
        "share_model": settings.get("share_model"),
        "thread_model": settings.get("thread_model"),
    }

def main(
    test_mode=False,
    video_url=None,
    digest_only=False,
    post_digest=False,
    digest_date=None,
    digest_model=None,
    digest_mode=None,
    post_share=False,
    post_threads=False,
):
    config = load_config()
    automation_settings = load_automation_settings()
    digest_model = digest_model or automation_settings["digest_model"]
    digest_mode = digest_mode or automation_settings["digest_mode"]
    share_model = automation_settings["share_model"] or digest_model
    thread_model = automation_settings["thread_model"] or share_model
    date_str = digest_date or datetime.now().strftime("%Y-%m-%d")

    if digest_only:
        generate_and_maybe_post_digest(
            config,
            date_str,
            post_digest=post_digest,
            digest_model=digest_model,
            digest_mode=digest_mode,
            post_share=post_share,
            share_chat_id=automation_settings["share_chat_id"],
            share_model=share_model,
        )
        return

    from processor import GemmaProcessor

    processor = GemmaProcessor()
    
    # Single video mode (for manual test)
    if video_url:
        print(f"Manual mode: Processing {video_url}")
        video_id, title = get_latest_video_info(video_url)
        if not video_id:
            print("Failed to get video ID.")
            return
        thread_path = process_video(video_id, title, "Manual", date_str, processor)
        if thread_path:
            if post_threads or automation_settings["auto_post_threads"]:
                post_thread_posts(
                    [thread_path],
                    date_str,
                    automation_settings["threads_chat_id"],
                    model=thread_model,
                )
            generate_and_maybe_post_digest(
                config,
                date_str,
                post_digest=post_digest,
                digest_model=digest_model,
                digest_mode=digest_mode,
                post_share=post_share,
                share_chat_id=automation_settings["share_chat_id"],
                share_model=share_model,
            )
        return

    # Automation mode: Check all curated channels
    print(f"Automation mode: Checking {len(config['channels'])} channels...")
    processed_any = False
    new_thread_paths = []
    for channel in config["channels"]:
        name = channel["name"]
        url = channel["url"]
        
        print(f"  Checking {name}...")
        latest_id, latest_title = get_latest_video_info(url)
        
        if not latest_id:
            continue
            
        last_id = config.get("last_processed", {}).get(name)
        
        if latest_id == last_id and not test_mode:
            print(f"    No new video for {name}.")
            continue
            
        print(f"    New video found: {latest_title} ({latest_id}). Processing...")
        thread_path = process_video(latest_id, latest_title, name, date_str, processor)
        if thread_path:
            processed_any = True
            new_thread_paths.append(thread_path)
            if not test_mode:
                config.setdefault("last_processed", {})[name] = latest_id
                save_config(config)

    # Auto-Sync to GitLab if new content was generated
    if processed_any and not test_mode:
        digest_should_post = (
            post_digest
            or os.getenv("TELEGRAM_AUTO_POST") == "1"
            or automation_settings["auto_post"]
        )
        share_should_post = post_share or automation_settings["auto_post_share"]
        threads_should_post = post_threads or automation_settings["auto_post_threads"]
        if threads_should_post:
            post_thread_posts(
                new_thread_paths,
                date_str,
                automation_settings["threads_chat_id"],
                model=thread_model,
            )

        generate_and_maybe_post_digest(
            config,
            date_str,
            post_digest=digest_should_post,
            digest_model=digest_model,
            digest_mode=digest_mode,
            post_share=share_should_post,
            share_chat_id=automation_settings["share_chat_id"],
            share_model=share_model,
        )

        from git_sync import sync_to_gitlab
        sync_to_gitlab(os.getcwd())
    elif post_digest:
        generate_and_maybe_post_digest(
            config,
            date_str,
            post_digest=True,
            digest_model=digest_model,
            digest_mode=digest_mode,
            post_share=post_share,
            share_chat_id=automation_settings["share_chat_id"],
            share_model=share_model,
        )


def generate_and_maybe_post_digest(
    config,
    date_str,
    post_digest=False,
    digest_model=None,
    digest_mode=None,
    post_share=False,
    share_chat_id=None,
    share_model=None,
):
    print(f"Generating Telegram digest for {date_str}...")
    digest, path = generate_daily_digest(
        config,
        date=date_str,
        model=digest_model,
        mode=digest_mode,
    )
    if not digest:
        print("Digest was not generated.")
        return False

    print(f"Digest saved to {path}")
    if post_digest:
        print("Posting digest to Telegram...")
        try:
            post_to_telegram(digest)
        except Exception as e:
            print(f"Failed to post digest to Telegram: {e}")
            return False
        print("Digest posted to Telegram.")

    if post_share:
        print("Generating share post...")
        share_post = generate_share_post(digest, date_str, model=share_model)
        share_path = save_post(share_post, date_str, SHARE_POSTS_DIR, "share")
        print(f"Share post saved to {share_path}")
        print("Posting share post to Telegram...")
        try:
            post_to_telegram(share_post, chat_id=share_chat_id)
        except Exception as e:
            print(f"Failed to post share post to Telegram: {e}")
            return False
        print("Share post posted to Telegram.")

    return True

def process_video(video_id, title, channel_name, date_str, processor):
    from processor import save_thread

    transcript = fetch_transcript(video_id)
    if not transcript:
        return False
    
    print("    Generating viral thread...")
    thread = processor.generate_thread(transcript, video_title=title, date=date_str)
    if not thread:
        print("    Failed to generate thread.")
        return False
    
    path = save_thread(video_id, thread, channel_name=channel_name, date=date_str)
    print(f"    Success! Thread saved to {path}")
    
    # Optional: Send a macOS notification
    try:
        msg = f"Thread generated: {title}"
        script = f'display notification "{apple_script_string(msg)}" with title "AI Snippets"'
        subprocess.run(["osascript", "-e", script], check=False, timeout=10)
    except:
        pass
        
    return path


def apple_script_string(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def post_thread_posts(thread_paths, date_str, threads_chat_id=None, model=None):
    if not thread_paths:
        return True

    if not threads_chat_id:
        print("Skipping thread channel posts: missing threads_chat_id in telegram_config.json.")
        return False

    ok = True
    for thread_path in thread_paths:
        post = generate_thread_discussion_post(thread_path, model=model)
        if not post:
            print(f"Skipping thread post; no discussion post generated for {thread_path}")
            ok = False
            continue

        saved_path = save_thread_post(post, thread_path, date_str)
        print(f"Thread post saved to {saved_path}")
        try:
            post_to_telegram(post, chat_id=threads_chat_id)
            print(f"Thread post sent from {thread_path}")
        except Exception as e:
            print(f"Failed to post thread from {thread_path}: {e}")
            ok = False

    return ok

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Interview Viral Snippets Orchestrator")
    parser.add_argument("--test", action="store_true", help="Run without updating last processed state")
    parser.add_argument("--url", type=str, help="Manually process a specific YouTube URL")
    parser.add_argument("--digest", action="store_true", help="Generate a Telegram digest from saved thread files")
    parser.add_argument("--post-digest", action="store_true", help="Post the generated digest to Telegram")
    parser.add_argument("--post-share", action="store_true", help="Post a short shareable digest takeaway")
    parser.add_argument("--post-threads", action="store_true", help="Post viral thread outputs to the configured threads channel")
    parser.add_argument("--date", type=str, help="Digest/process date in YYYY-MM-DD format")
    parser.add_argument("--digest-model", type=str, help="Ollama model for digest generation")
    parser.add_argument(
        "--digest-mode",
        choices=["single", "deep"],
        help="Digest generation mode. single is faster; deep runs a per-video brief pass first.",
    )
    
    args = parser.parse_args()
    main(
        test_mode=args.test,
        video_url=args.url,
        digest_only=args.digest,
        post_digest=args.post_digest,
        digest_date=args.date,
        digest_model=args.digest_model,
        digest_mode=args.digest_mode,
        post_share=args.post_share,
        post_threads=args.post_threads,
    )
