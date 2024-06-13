#
# GENERATE_INSTAGRAM_CREATIVES.PY
#

import os
import sqlite3
import openai
import aiohttp
import asyncio
import logging
from collections import defaultdict
from datetime import datetime
from ai_news_config import OPENAI_API_KEY, CAPTION_PROMPT, IMAGE_GENERATION_FROM_VIDEO_PROMPT, OPENAI_LLM_MODEL, OPENAI_IMAGE_MODEL, UPCOMING_POSTS_PATH

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

openai.api_key = OPENAI_API_KEY
client = openai.OpenAI()

async def download_image(url, output_path):
    logging.info(f"Downloading image from {url} to {output_path}")
    retries = 3
    for attempt in range(retries):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(output_path, "wb") as f:
                        async for chunk in response.content.iter_chunked(1024):
                            f.write(chunk)
                    logging.info(f"Image downloaded successfully: {output_path}")
                    return
                else:
                    logging.error(f"Failed to download image from {url}. Status code: {response.status}")
                    if attempt < retries - 1:
                        wait_time = 2 ** attempt
                        logging.info(f"Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        raise Exception(f"Failed to download image after {retries} attempts.")

async def generate_image(client, image_prompt):
    logging.info(f"Generating image using DALL-E with prompt: {image_prompt}")
    retries = 3
    for attempt in range(retries):
        try:
            response = client.images.generate(
                model=OPENAI_IMAGE_MODEL,
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            return response.data[0].url
        except Exception as e:
            logging.error(f"Image generation failed: {e}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt
                logging.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                raise

async def generate_caption(client, video_title, concatenated_highlights, video_url):
    logging.info("Generating caption using GPT-4o")
    messages = [
        {
            "role": "system",
            "content": "You are a highly intelligent AI capable of generating engaging captions for social media posts based on video highlights. Your task is to create a captivating and descriptive caption that captures the essence of the video and is suitable for an Instagram post. The caption should be engaging and encourage interaction."
        },
        {
            "role": "user",
            "content": CAPTION_PROMPT
        }
    ]

    logging.info("Generating caption using OpenAI ChatCompletion...")
    response = client.chat.completions.create(
        model=OPENAI_LLM_MODEL,
        messages=messages
    )

    caption = response.choices[0].message.content.strip()
    logging.info(f"Generated caption: {caption}")
    return caption

async def process_video(client, video_url, video_title, channel_title, concatenated_highlights, video_date):
    logging.info(f"Processing video: {video_title}")

    # Create sub-folder
    folder_name = f"{video_date}_{video_title.replace(' ', '_')}"
    folder_path = os.path.join("instagram_creatives", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    messages = [
        {
            "role": "system",
            "content": "You are a highly intelligent AI capable of generating creative image prompts based on video highlights. Your task is to create a detailed and imaginative prompt that captures the essence of the video and can be used to generate an engaging image for an Instagram post. Focus on the key elements, emotions, and visual aspects of the video to craft a compelling prompt. Do not include any text in the image."
        },
        {
            "role": "user",
            "content": IMAGE_GENERATION_FROM_VIDEO_PROMPT
        }
    ]

    logging.info("Generating image prompt using OpenAI ChatCompletion...")
    response = client.chat.completions.create(
        model=OPENAI_LLM_MODEL,
        messages=messages
    )

    image_prompt = response.choices[0].message.content.strip()
    logging.info(f"{concatenated_highlights}\t{image_prompt}")

    image_url = await generate_image(client, image_prompt)
    image_path = os.path.join(folder_path, "image.png")
    await download_image(image_url, image_path)

    caption = await generate_caption(client, video_title, concatenated_highlights[:2000], video_url)  # Truncate highlights to fit within context limits
    caption_path = os.path.join(folder_path, "caption.txt")
    with open(caption_path, "w") as f:
        f.write(caption)

    return folder_path  # Return the folder path for further processing

async def generate_instagram_creatives():
    logging.info("Connecting to the database...")
    try:
        conn = sqlite3.connect('data/ai_news.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        logging.error(f"Database connection failed: {e}")
        return

    try:
        logging.info("Verifying the schema and adding the missing column if necessary...")
        cursor.execute("PRAGMA table_info(social_media_content)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        if 'channel_title' not in column_names:
            cursor.execute("ALTER TABLE social_media_content ADD COLUMN channel_title TEXT")
            conn.commit()
            logging.info("Added 'channel_title' column to the 'social_media_content' table.")
        else:
            logging.info("'channel_title' column already exists in the 'social_media_content' table.")

        logging.info("Creating the 'instagram_creatives' folder if it doesn't exist...")
        os.makedirs("instagram_creatives", exist_ok=True)

        logging.info("Creating the 'instagram_creatives/upcoming_posts' folder if it doesn't exist...")
        os.makedirs("instagram_creatives/upcoming_posts", exist_ok=True)

        logging.info("Querying the database for social media content...")

        # Check if 'video_date' column exists
        if 'video_date' in column_names:
            query = "SELECT video_url, video_title, channel_title, english_highlights, video_date FROM social_media_content"
        else:
            query = "SELECT video_url, video_title, channel_title, english_highlights FROM social_media_content"

        cursor.execute(query)
        videos = cursor.fetchall()

        if videos:
            logging.info("Video Highlights\tImage Prompt")
            logging.info("===============\t============")
            highlights_by_video = defaultdict(list)
            for video in videos:
                if len(video) == 5:
                    video_url, video_title, channel_title, english_highlights, video_date = video
                else:
                    video_url, video_title, channel_title, english_highlights = video
                    video_date = datetime.now().strftime('%Y%m%d')

                highlights_by_video[(video_url, video_title, channel_title, video_date)].append(english_highlights)

            tasks = []
            for (video_url, video_title, channel_title, video_date), highlights in highlights_by_video.items():
                filtered_highlights = [h for h in highlights if h is not None]  # Filter out None values
                concatenated_highlights = " ".join(set(filtered_highlights))  # Remove duplicates
                tasks.append(process_video(client, video_url, video_title, channel_title, concatenated_highlights, video_date))
            
            # Collect folder paths from processed videos
            processed_folders = await asyncio.gather(*tasks)

            # Process the upcoming posts
            process_upcoming_posts(processed_folders)
        else:
            logging.info("No social media content found in the database.")
    except sqlite3.Error as e:
        logging.error(f"Database query failed: {e}")
    finally:
        logging.info("Closing the database connection...")
        conn.close()

# Process the upcoming posts
def process_upcoming_posts(processed_folders):
    upcoming_posts_path = UPCOMING_POSTS_PATH
    existing_files = os.listdir(upcoming_posts_path)
    picture_count = len([f for f in existing_files if f.startswith("picture_")])

    for i, folder in enumerate(processed_folders):
        image_path = os.path.join(folder, "image.png")
        caption_path = os.path.join(folder, "caption.txt")

        if os.path.exists(image_path) and os.path.exists(caption_path):
            new_image_path = os.path.join(upcoming_posts_path, f"picture_{picture_count}.png")
            new_caption_path = os.path.join(upcoming_posts_path, f"caption_{picture_count}.txt")

            with open(image_path, "rb") as img_src, open(new_image_path, "wb") as img_dest:
                img_dest.write(img_src.read())

            with open(caption_path, "r") as cap_src, open(new_caption_path, "w") as cap_dest:
                cap_dest.write(cap_src.read())

            logging.info(f"Copied {image_path} to {new_image_path}")
            logging.info(f"Copied {caption_path} to {new_caption_path}")

            picture_count += 1

if __name__ == '__main__':
    logging.info("Starting the script...")
    asyncio.run(generate_instagram_creatives())
    logging.info("Script execution completed.")
