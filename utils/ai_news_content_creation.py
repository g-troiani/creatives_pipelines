#
# UTILS/GRAPH/AI_NEWS_GRAPH/AI_NEWS_CONTENT_CREATION.PY
#

import sqlite3
from datetime import datetime
from utils.database.ai_news_database.create_tables import db_file

def create_social_media_content_table():
    """
    Create the social_media_content table in the database.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS social_media_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_url TEXT,
            video_title TEXT,
            channel_title TEXT,
            english_highlights TEXT,
            spanish_highlights TEXT,
            video_date TEXT,
            created_at TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def store_social_media_content(video_url, video_title, channel_title, english_highlights, spanish_highlights):
    """
    Store the social media content in the database.
    
    Args:
        video_url (str): The URL of the video.
        video_title (str): The title of the video.
        channel_title (str): The title of the channel.
        english_highlights (str): The English highlights of the video.
        spanish_highlights (str): The Spanish highlights of the video.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Insert the social media content into the database
    cursor.execute('''
        INSERT INTO social_media_content (video_url, video_title, channel_title, english_highlights, spanish_highlights, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        video_url,
        video_title,
        channel_title,
        english_highlights,
        spanish_highlights,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

def generate_instagram_post_content(video_url, video_title, channel_title, english_highlights):
    """
    Generate the content for an Instagram post based on the video information.
    
    Args:
        video_url (str): The URL of the video.
        video_title (str): The title of the video.
        channel_title (str): The title of the channel.
        english_highlights (str): The English highlights of the video.
        
    Returns:
        str: The generated Instagram post content.
    """
    post_content = f"New video from {channel_title}! 🎥\n\n"
    post_content += f"Title: {video_title}\n\n"
    post_content += f"Highlights:\n{english_highlights}\n\n"
    post_content += f"Watch the full video: {video_url}\n\n"
    post_content += "#AI #MachineLearning #DeepLearning #DataScience #TechNews"
    
    return post_content

def generate_twitter_post_content(video_url, video_title, channel_title, english_highlights):
    """
    Generate the content for a Twitter post based on the video information.
    
    Args:
        video_url (str): The URL of the video.
        video_title (str): The title of the video.
        channel_title (str): The title of the channel.
        english_highlights (str): The English highlights of the video.
        
    Returns:
        str: The generated Twitter post content.
    """
    post_content = f"New video from {channel_title}! 🎥\n\n"
    post_content += f"{video_title}\n\n"
    post_content += f"Highlights:\n{english_highlights}\n\n"
    post_content += f"{video_url}\n\n"
    post_content += "#AI #MachineLearning #DeepLearning #DataScience #TechNews"
    
    return post_content