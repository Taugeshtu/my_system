#!/usr/bin/env -S uv run --script --quiet
# /// script
# dependencies = [
#   "yt-dlp",
#   "youtube-transcript-api",
# ]
# ///

import os
import sys
import re
import urllib.parse
from datetime import datetime
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Set of common English stop words to filter out when generating filename slug
STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could',
    "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for',
    'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's",
    'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm",
    "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't",
    'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours',
    'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't",
    'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
    "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't",
    'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why',
    "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours',
    'yourself', 'yourselves'
}

def extract_video_id(url_or_id):
    """
    Extracts the 11-character video ID from a YouTube URL or direct ID.
    """
    url_or_id = url_or_id.strip()
    
    # If it is exactly 11 characters and looks like an ID, return it
    if len(url_or_id) == 11 and re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
        
    parsed = urllib.parse.urlparse(url_or_id)
    
    # Handle youtu.be/ID
    if parsed.netloc == 'youtu.be':
        return parsed.path.strip('/')
        
    # Handle youtube.com paths
    if parsed.netloc in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
        if parsed.path.startswith('/watch'):
            query = urllib.parse.parse_qs(parsed.query)
            return query.get('v', [None])[0]
        if parsed.path.startswith(('/embed/', '/v/', '/shorts/')):
            parts = parsed.path.split('/')
            if len(parts) >= 3:
                return parts[2]
                
    # Generic regex fallback for query parameters or other formats
    match = re.search(r'(?:v=|\/v\/|\/embed\/|\/shorts\/|youtu\.be\/|\/watch\?v=)([^#\&\?]{11})', url_or_id)
    if match:
        return match.group(1)
        
    return None

def get_video_title(video_id):
    """
    Scrapes the title of the YouTube video using yt-dlp.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', None)

def slugify_title(title):
    """
    Converts video title to a kebab-case string using the first 4-5 significant words.
    """
    if not title:
        return "youtube-video"
        
    # Convert to lowercase
    title_lower = title.lower()
    
    # Replace hyphens and underscores with spaces to handle word boundaries
    spaced = re.sub(r'[-_]', ' ', title_lower)
    
    # Remove everything except lowercase letters, numbers, and spaces
    cleaned = re.sub(r'[^a-z0-9\s]', '', spaced)
    
    # Split into words
    words = cleaned.split()
    
    # Filter out stop words
    sig_words = [w for w in words if w not in STOP_WORDS]
    
    # Fallback to all words if no significant words remain
    if not sig_words:
        sig_words = words
        
    # Take first 5 significant words
    chosen_words = sig_words[:5]
    
    # Fallback if still empty
    if not chosen_words:
        return "youtube-video"
        
    # Join with hyphens
    return "-".join(chosen_words)

def get_transcript_text(video_id):
    """
    Retrieves the transcript list, preferring manually created English,
    falling back to auto-generated English, or translating another language to English.
    """
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        # Try to find manual English transcript
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except NoTranscriptFound:
            # Fallback to auto-generated English transcript
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except NoTranscriptFound:
                # Fallback to translating the first available transcript to English
                try:
                    first_transcript = next(iter(transcript_list))
                    transcript = first_transcript.translate('en')
                except Exception:
                    raise Exception("No transcript could be found or translated to English.")
                    
        return transcript.fetch()
    except TranscriptsDisabled:
        raise Exception("Subtitles/transcripts are disabled for this video.")
    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {str(e)}")

def format_transcript(transcript_list):
    """
    Format the list of transcript entries into continuous, readable paragraphs.
    """
    paragraphs = []
    current_paragraph = []
    
    for entry in transcript_list:
        if hasattr(entry, 'text'):
            text = entry.text
        elif isinstance(entry, dict) and 'text' in entry:
            text = entry['text']
        else:
            continue
            
        text = text.strip()
        # Replace internal newlines with space
        text = text.replace('\n', ' ')
        current_paragraph.append(text)
        
        # Combine accumulated sentences
        combined_text = ' '.join(current_paragraph)
        
        # New paragraph logic:
        # 1. Segment ends with sentence-ending punctuation (. or ! or ?) and length is >= 350 chars
        # 2. Accumulated text is getting too long (>= 750 chars) to prevent giant walls of text
        ends_with_punctuation = text.endswith(('.', '!', '?'))
        
        if (ends_with_punctuation and len(combined_text) >= 350) or len(combined_text) >= 750:
            paragraphs.append(combined_text)
            current_paragraph = []
            
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
        
    return '\n\n'.join(paragraphs)

def print_help():
    help_text = """Yoink - YouTube Transcript Grabber

WHY:
  Yoink exists to convert YouTube video watching into a reading experience.
  It extracts the raw transcript of any English video (supporting manually written captions,
  auto-generated English, or translated fallbacks) and reformats it into clean, flowing paragraphs
  ready for reading or processing by LLMs/agents.

PRINCIPLE OF OPERATION:
  1. Extract the 11-character video ID from the provided URL.
  2. Scrape the video title using yt-dlp.
  3. Fetch the transcript using youtube-transcript-api.
  4. Format the individual timeline segments into cohesive markdown paragraphs.
  5. Either output to stdout or write to a kebab-case markdown file based on the arguments.

USAGE:
  yoink <youtube_url_or_id>
    Prints the formatted markdown transcript directly to stdout. Very useful for piping.
    Example: yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ > transcript.md

  yoink <dest_folder> <youtube_url_or_id>
    Saves the transcript to a kebab-case filename (using the first 4-5 significant words
    of the video title) inside the specified folder.
    Example: yoink ./readings https://www.youtube.com/watch?v=dQw4w9WgXcQ
    This will save the file to ./readings/rick-astley-never-gonna-give.md

    If the target file already exists, the following fallbacks are attempted:
      1. Add "YYYYMMDD_" prefix (e.g., 20260521_rick-astley-never-gonna-give.md)
      2. Morph prefix to "YYYYMMDD-HHMM_" (e.g., 20260521-1747_rick-astley-never-gonna-give.md)
      3. If that still exists, the script exits with an error.
"""
    print(help_text)

def main():
    # If no arguments are passed, or -h/--help is requested, print the full help page
    if len(sys.argv) == 2 and sys.argv[1] in ('-h', '--help'):
        print_help()
        sys.exit(0)
        
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print_help()
        sys.exit(1)
        
    if len(sys.argv) == 2:
        dest_folder = None
        url = sys.argv[1]
    else:
        dest_folder = sys.argv[1]
        url = sys.argv[2]
        
    video_id = extract_video_id(url)
    if not video_id:
        print(f"Error: Could not parse YouTube video ID from '{url}'", file=sys.stderr)
        sys.exit(1)
        
    try:
        print(f"Fetching metadata for video ID {video_id}...", file=sys.stderr)
        title = get_video_title(video_id)
        if not title:
            title = f"youtube-video-{video_id}"
        print(f"Title: {title}", file=sys.stderr)
        
        print("Fetching subtitles/transcript...", file=sys.stderr)
        transcript_data = get_transcript_text(video_id)
        
        print("Formatting transcript...", file=sys.stderr)
        formatted_text = format_transcript(transcript_data)
        
        # Create output content
        content = f"# {title}\n\n"
        content += f"**Source:** https://www.youtube.com/watch?v={video_id}\n\n"
        content += formatted_text + "\n"
        
        if dest_folder is None:
            # Print transcript to stdout
            print(content)
        else:
            # Make sure destination folder exists
            os.makedirs(dest_folder, exist_ok=True)
            
            # Format filename
            filename_slug = slugify_title(title)
            output_path = os.path.join(dest_folder, f"{filename_slug}.md")
            
            if os.path.exists(output_path):
                now = datetime.now()
                # Fallback 1: Add "YYYYMMDD_" prefix, check again
                prefix1 = now.strftime("%Y%m%d_")
                output_path_fallback1 = os.path.join(dest_folder, f"{prefix1}{filename_slug}.md")
                
                if os.path.exists(output_path_fallback1):
                    # Fallback 2: Morph prefix into "YYYYMMDD-HHMM_" prefix, check again
                    prefix2 = now.strftime("%Y%m%d-%H%M_")
                    output_path_fallback2 = os.path.join(dest_folder, f"{prefix2}{filename_slug}.md")
                    
                    if os.path.exists(output_path_fallback2):
                        # STILL EXISTS? Give up, print error
                        print(f"Error: Output file already exists even with datetime prefixes: '{output_path_fallback2}'", file=sys.stderr)
                        sys.exit(1)
                    else:
                        output_path = output_path_fallback2
                else:
                    output_path = output_path_fallback1

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"Success! Transcript saved to: {output_path}", file=sys.stderr)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
