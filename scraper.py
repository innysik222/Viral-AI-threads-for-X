import json
import os
import subprocess
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def get_latest_video_info(url, max_retries=3):
    """
    Uses yt-dlp to get the ID and Title of the latest video.
    Returns (id, title) or (None, None).
    Includes retry logic for transient failures.
    """
    import time
    import sys
    
    for attempt in range(max_retries):
        try:
            # Check if it's already a video URL for titles
            if "watch?v=" in url:
                command = [sys.executable, '-m', 'yt_dlp', '--get-id', '--get-title', url]
            else:
                command = [
                    sys.executable, '-m', 'yt_dlp',
                    '--get-id', '--get-title',
                    '--playlist-items', '1',
                    '--flat-playlist',
                    url
                ]
            result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=30)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                # yt-dlp prints title then ID with these flags
                return lines[1], lines[0]
            return lines[0], "Unknown Title"
        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            print(f"Timeout fetching video info for {url}")
            return None, None
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            # Regex fallback for ID if yt-dlp fails
            v_match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
            if v_match:
                return v_match.group(1), "Unknown Title"
            print(f"Error fetching video info for {url}: {e}")
            return None, None

def fetch_transcript(video_id):
    """
    Fetches the transcript for a given video ID.
    Simple direct fetch for first available English transcript.
    """
    try:
        # Use verified methods from inspection (instance methods)
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(['en'])
        data = transcript.fetch()
        return " ".join([t.text for t in data])
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None

def save_transcript(video_id, content, output_dir="output/transcripts"):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{video_id}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

if __name__ == "__main__":
    # Test with a known AI channel (e.g., Lex Fridman)
    test_url = "https://www.youtube.com/@lexfridman"
    print(f"Checking latest video for {test_url}...")
    vid, title = get_latest_video_info(test_url)
    if vid:
        print(f"Found latest video ID: {vid} (Title: {title})")
        text = fetch_transcript(vid)
        if text:
            path = save_transcript(vid, text)
            print(f"Transcript saved to {path} ({len(text)} characters)")
        else:
            print("No transcript found.")
    else:
        print("Could not find latest video.")
