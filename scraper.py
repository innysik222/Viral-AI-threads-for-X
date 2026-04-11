import json
import os
import subprocess
import re

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

def fetch_transcript(video_id, output_dir="/tmp/transcripts"):
    import sys
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    os.makedirs(output_dir, exist_ok=True)
    temp_prefix = os.path.join(output_dir, f"sub_{video_id}")
    
    try:
        command = [
            sys.executable, '-m', 'yt_dlp',
            '--skip-download',
            '--write-auto-sub',
            '--sub-lang', 'en',
            '--sub-format', 'vtt',
            '-o', temp_prefix,
            url
        ]
        subprocess.run(command, capture_output=True, text=True, check=True)
        
        # yt-dlp generates the file with .en.vtt appended
        vtt_file = f"{temp_prefix}.en.vtt"
        if not os.path.exists(vtt_file):
            print(f"No VTT file generated for {video_id}.")
            return None
            
        with open(vtt_file, 'r', encoding='utf-8') as f:
            vtt_content = f.read()
            
        # Parse VTT
        text_lines = []
        for line in vtt_content.split('\n'):
            line = line.strip()
            # Skip timestamps, headers, metadata, and empty lines
            if not line or 'WEBVTT' in line or '-->' in line or line.startswith('Kind:') or line.startswith('Language:') or line.startswith('Style:'):
                continue
            # Strip inline tags e.g. <c> or timestamps
            clean_line = re.sub(r'<[^>]+>', '', line)
            if clean_line:
                # Basic deduplication for overlapping subtitle renders
                if not text_lines or text_lines[-1] != clean_line:
                    text_lines.append(clean_line)
                
        # Clean up temp file
        os.remove(vtt_file)
        return " ".join(text_lines)
    except Exception as e:
        print(f"Error fetching transcript via yt-dlp for {video_id}: {e}")
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
