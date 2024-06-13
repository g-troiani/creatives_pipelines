#
# SCRAPERS/AI_NEWS_SCRAPERS/YOUTUBE_API_SCRAPER/GET_VIDEO_DETAILS.PY
#


import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ai_news_config import YOUTUBE_API_KEY

# Set up the YouTube Data API
api_key = YOUTUBE_API_KEY  # Replace with your actual API key
youtube = build('youtube', 'v3', developerKey=api_key)
youtube_api_call_count = 0

def get_video_details(video_id):
    global youtube_api_call_count
    try:
        video_response = youtube.videos().list(
            id=video_id,
            part='snippet'
        ).execute()
        youtube_api_call_count += 1
        print(f"YouTube API calls made: {youtube_api_call_count}")

        if 'items' in video_response and len(video_response['items']) > 0:
            video = video_response['items'][0]
            video_title = video['snippet']['title']
            channel_title = video['snippet']['channelTitle']
            video_url = f'https://www.youtube.com/watch?v={video_id}'

            print(f"Retrieved details for video: {video_title}")
            return video_title, channel_title, video_url
        else:
            print(f"No video details found for video ID: {video_id}")
            return None, None, None
    except HttpError as e:
        print(f'An error occurred while retrieving video details for video ID {video_id}: {e}')
        return None, None, None