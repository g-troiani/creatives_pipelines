#
# SCRAPERS/AI_NEWS_SCRAPERS/YOUTUBE_API_SCRAPER/GET_VIDEO_TRANSCRIPT.PY
#

from youtube_transcript_api import YouTubeTranscriptApi

def get_video_transcript(video_id):
    try:
        print(f"Retrieving transcript for video: {video_id}")
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([item['text'] for item in transcript_list])
        transcript_timestamps = ','.join([f"{item['start']}-{item['start'] + item['duration']}" for item in transcript_list])
        print(f"Retrieved transcript for video: {video_id}")
        return transcript_list  # Return the list directly
    except Exception as e:
        print(f'An error occurred while retrieving the transcript for video {video_id}: {e}')
        return None
