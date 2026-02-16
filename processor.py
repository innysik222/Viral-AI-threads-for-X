import ollama
import os
import re

class GemmaProcessor:
    def __init__(self, model="gemma3:12b"):
        self.model = model
        self.client = ollama.Client(host='http://localhost:11434')

    def generate_thread(self, transcript, video_title="Unknown Video", date="Unknown Date"):
        """
        Uses Gemma 3 to transform a transcript into a viral X thread AND a summary article.
        """
        prompt = f"""
You are a world-class social media strategist, elite tech journalist, and AI expert. 
Your task is to analyze the following interview transcript and create TWO distinct outputs:
1. A high-engagement, viral X (Twitter) thread.
2. A comprehensive, structured summary article.

VIDEO INFO:
Title: {video_title}
Date: {date}

TRANSCRIPT:
\"\"\"
{transcript}
\"\"\"

---

### PART 1: VIRAL X THREAD INSTRUCTIONS
1. Identify the most mind-blowing or controversial insight.
2. Structure: 5-7 posts.
3. Post 1 (Hook): Catchy, high-stakes, maximum curiosity.
4. Posts 2-6: Punchy takeaways, bullet points, dialogue reconstruction.
5. Post 7: specific 'Alpha' take + Call to Action.
6. Tone: Authoritative, forward-looking, "insider".
7. Length: <280 chars per post.

### PART 2: SUMMARY ARTICLE INSTRUCTIONS
1. Headline: Catchy, SEO-friendly headline (H1).
2. TL;DR: 2-3 sentence executive summary.
3. Key Insights: 3-5 bullet points of the most valuable takeaways.
4. Deep Dive: 3-4 paragraphs expanding on the core themes, arguments, and implications. Use subheaders (H2).
5. Quotes: Include 1-2 verbatim powerful quotes.
6. Conclusion: A final synthesizing thought.
7. Image Prompt: A highly descriptive prompt for Midjourney/DALL-E at the very end.

---

### REQUIRED OUTPUT FORMAT
(Do not output any introductory text, start directly with the Thread)

# {video_title} ({date})

## 🧵 VIRAL THREAD

Post 1: [Content]
---
Post 2: [Content]
...
Post 7: [Content]

---

## 📰 SUMMARY ARTICLE

# [Catchy Article Headline]

**TL;DR:** [Executive Summary]

### 🔑 Key Insights
*   [Insight 1]
*   [Insight 2]
...

### 🧠 Deep Dive
[Paragraphs with subheaders...]

### 💬 Notable Quotes
> "[Quote]"

### 🏁 Conclusion
[Final thoughts]

---
IMAGE GENERATION PROMPT: [Your prompt]
"""

        try:
            # Setting a large context window in the options
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "num_ctx": 65536,  # 64k tokens to be safe
                    "temperature": 0.7,
                }
            )
            return response['response']
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            return None

def save_thread(video_id, thread_content, channel_name="Unknown", date="Unknown", output_dir="output/threads"):
    # Create date-based subdirectory
    if date != "Unknown":
        output_dir = os.path.join(output_dir, date)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Sanitize channel name for filename
    clean_name = re.sub(r'[^\w\s-]', '', channel_name).strip().replace(' ', '_')
    file_name = f"{clean_name}_{video_id}.md" # Removed date from filename as it's in the folder now
    
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(thread_content)
    return file_path

if __name__ == "__main__":
    # Test with a dummy transcript if no local file exists
    dummy_text = "This is a test transcript about the future of AGI and how it will transform society."
    processor = GemmaProcessor()
    print("Generating test thread...")
    thread = processor.generate_thread(dummy_text)
    if thread:
        print("\n--- GENERATED THREAD ---\n")
        print(thread)
    else:
        print("Failed to generate thread.")
