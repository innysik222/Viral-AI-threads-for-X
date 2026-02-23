import json
import os
import argparse
from datetime import datetime
from scraper import get_latest_video_info, fetch_transcript, save_transcript
from processor import GemmaProcessor, save_thread

def load_config(config_path="channels.json"):
    with open(config_path, "r") as f:
        return json.load(f)

def save_config(config, config_path="channels.json"):
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

def main(test_mode=False, video_url=None):
    config = load_config()
    processor = GemmaProcessor()
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Single video mode (for manual test)
    if video_url:
        print(f"Manual mode: Processing {video_url}")
        video_id, title = get_latest_video_info(video_url)
        if not video_id:
            print("Failed to get video ID.")
            return
        process_video(video_id, title, "Manual", date_str, processor)
        return

    # Automation mode: Check all curated channels
    print(f"Automation mode: Checking {len(config['channels'])} channels...")
    processed_any = False
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
        if process_video(latest_id, latest_title, name, date_str, processor):
            processed_any = True
            if not test_mode:
                config.setdefault("last_processed", {})[name] = latest_id
                save_config(config)

    # Auto-Sync to GitLab if new content was generated
    if processed_any and not test_mode:
        from git_sync import sync_to_gitlab
        sync_to_gitlab(os.getcwd())

def process_video(video_id, title, channel_name, date_str, processor):
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
        # Sanitize title for shell osascript
        safe_title = title.replace('"', '\\"')
        os.system(f'osascript -e \'display notification "Thread generated: {safe_title}" with title "AI Snippets"\'')
    except:
        pass
        
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Interview Viral Snippets Orchestrator")
    parser.add_argument("--test", action="store_true", help="Run without updating last processed state")
    parser.add_argument("--url", type=str, help="Manually process a specific YouTube URL")
    
    args = parser.parse_args()
    main(test_mode=args.test, video_url=args.url)
