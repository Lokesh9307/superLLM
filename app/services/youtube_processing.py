from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import re

def extract_video_id(url):
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?&]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^\/?&]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript_chunks(video_id, max_chunk_length=2000):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except NoTranscriptFound:
        raise Exception("No transcript available for this video.")
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")

    full_text = " ".join([t['text'] for t in transcript])
    words = full_text.split()
    chunks, chunk, length = [], [], 0
    for word in words:
        if length + len(word) + 1 > max_chunk_length:
            chunks.append(" ".join(chunk))
            chunk, length = [], 0
        chunk.append(word)
        length += len(word) + 1
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks
