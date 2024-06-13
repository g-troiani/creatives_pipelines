#
# SCRAPERS/AI_NEWS_SCRAPERS/YOUTUBE_API_SCRAPER/GET_VIDEOS_LAST_24_HOURS.PY
#

from googleapiclient.discovery import build
from datetime import datetime, timedelta
from ai_news_config import GOOGLE_API_KEY

youtube = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)
youtube_api_call_count = 0

def get_videos_last_24_hours(channel_id):
    global youtube_api_call_count
    # Calculate the time 24 hours ago
    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
    
    # Convert the datetime to ISO 8601 format
    published_after = twenty_four_hours_ago.isoformat() + 'Z'
    
    video_ids = []
    next_page_token = None
    
    while True:
        # Make the API request to search for videos in the channel uploaded in the last 24 hours
        search_response = youtube.search().list(
            part='id',
            channelId=channel_id,
            type='video',
            publishedAfter=published_after,
            maxResults=50,
            pageToken=next_page_token,
            order='date'
        ).execute()
        youtube_api_call_count += 1
        print(f"YouTube API calls made: {youtube_api_call_count}")
        
        video_ids.extend([item['id']['videoId'] for item in search_response['items']])
        
        next_page_token = search_response.get('nextPageToken')
        
        if not next_page_token:
            break
    
    # Retrieve the details of the videos
    video_details = []
    
    for i in range(0, len(video_ids), 50):
        video_id_batch = video_ids[i:i+50]
        video_response = youtube.videos().list(
            part='snippet,contentDetails',
            id=','.join(video_id_batch)
        ).execute()
        youtube_api_call_count += 1
        print(f"YouTube API calls made: {youtube_api_call_count}")
        
        for video in video_response['items']:
            video_duration = video['contentDetails']['duration']
            
            if 'PT3M' <= video_duration:
                video_details.append(video)
    
    return [video['id'] for video in video_details]