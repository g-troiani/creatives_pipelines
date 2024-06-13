#
# YOUTUBE_PROCESSOR.PY
# 


from datetime import datetime, timedelta
import random
import time
import logging
from scrapers.ai_news_scrapers.youtube_api_scraper.get_videos_last_24_hours import get_videos_last_24_hours, youtube_api_call_count as get_videos_last_24_hours_api_call_count
from scrapers.ai_news_scrapers.youtube_api_scraper.get_video_details import get_video_details, youtube_api_call_count as get_video_details_api_call_count
from scrapers.ai_news_scrapers.youtube_api_scraper.get_video_transcript import get_video_transcript
from scrapers.ai_news_scrapers.youtube_api_scraper.filter_titles_by_keywords import filter_titles_by_keywords
from utils.api_utils import generate_summary, perform_ner, perform_ere, perform_syntactic_analysis
from utils.database.ai_news_database.store_video_data import store_video_data
from api.google_api.ai_news_google_api.generate_video_highlights import generate_video_highlights
from api.google_api.ai_news_google_api.translate_video_highlights import translate_video_highlights
from utils.database.ai_news_database.create_video_highlights_table import create_video_highlights_table
from utils.database.ai_news_database.store_video_highlights import store_video_highlights
from utils.ai_news_neo4j.neo4j_utils import Neo4jUtils
from utils.ai_news_content_creation import store_social_media_content
from ai_news_config import CHANNEL_IDS, KEYWORDS, CHANNELS_FILTERED_FOR_KEYWORDS, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

logging.basicConfig(level=logging.INFO)

def format_timestamp(seconds):
    return str(timedelta(seconds=seconds))

def process_youtube_videos(perform_analysis, creatives):
    channel_ids = CHANNEL_IDS     # Define YouTube channel IDs to scrape videos from

    # Define keywords to filter video titles
    keywords = KEYWORDS

    for channel_id in channel_ids:
        logging.info(f"Processing channel: {channel_id}")
        video_ids = get_videos_last_24_hours(channel_id)
        logging.info(f"Retrieved {len(video_ids)} videos from the YouTube API for channel: {channel_id}")
        for video_id in video_ids:
            process_youtube_video(channel_id, video_id, keywords, perform_analysis, creatives)
            
            logging.info(f"YouTube API calls made in get_videos_last_24_hours: {get_videos_last_24_hours_api_call_count}")
            logging.info(f"YouTube API calls made in get_video_details: {get_video_details_api_call_count}")
            logging.info(f"Total YouTube API calls made: {get_videos_last_24_hours_api_call_count + get_video_details_api_call_count}")
            
            # Add a random delay between API calls to avoid hitting rate limits
            time.sleep(random.uniform(1, 5))

def process_youtube_video(channel_id, video_id, keywords, perform_analysis, creatives):
    logging.info(f"Processing video: {video_id}")
    video_title, channel_title, video_url = get_video_details(video_id)

    # Skip videos that do not contain relevant keywords
    if channel_id in CHANNELS_FILTERED_FOR_KEYWORDS : 
        if video_title and not filter_titles_by_keywords(video_title, keywords):
            logging.info(f"Skipping video: {video_title} (No relevant keywords found)")
            return
    
    if video_title:
        transcript = get_video_transcript(video_id)
        logging.info(f"Video Transcript: {transcript}")
        if transcript:
            if isinstance(transcript, list) and all(isinstance(item, dict) for item in transcript):
                transcript_text_with_timestamps = ' '.join([f"{format_timestamp(item['start'])}-{format_timestamp(item['start'] + item['duration'])}: {item['text']}" for item in transcript])
                logging.info(f"Transcript with Timestamps: {transcript_text_with_timestamps}")

                summary = None
                try:
                    summary = generate_summary(transcript_text_with_timestamps)
                except Exception as e:
                    logging.error(f"An error occurred while generating the summary: {e}")
                
                if summary:
                    store_video_data(video_id, video_title, channel_title, video_url, transcript_text_with_timestamps, summary)
                    logging.info(f"Generated summary for video: {video_title}")
                else:
                    logging.warning(f"Failed to generate summary for video: {video_title}")
                
                if creatives:
                    # Generate video highlights
                    highlights = generate_video_highlights(transcript_text_with_timestamps)
                    
                    # Translate video highlights to Spanish
                    translated_highlights = translate_video_highlights(highlights)
                    
                    store_video_highlights(video_id, highlights, translated_highlights)
                    
                    # Store social media content
                    store_social_media_content(video_url, video_title, channel_title, highlights, translated_highlights)
                
                if perform_analysis:
                    # Perform NER on the video transcript
                    ner_result = perform_ner(transcript_text_with_timestamps)
                    logging.info(f"NER Result: {ner_result}")
                    
                    # Extract entities and their counts from the NER result
                    entities = ner_result.split("\n\n")
                    for entity in entities:
                        if "Entity:" in entity:
                            entity_parts = entity.split("\n")
                            entity_name = entity_parts[0].replace("Entity: ", "")
                            entity_count = int(entity_parts[1].replace("Count: ", ""))
                            
                            # Store the entity, count, title, and date in the ner table
                            neo4j_utils = Neo4jUtils(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
                            neo4j_utils.store_ner_data(video_id, entity_name, entity_count, video_title, datetime.now().strftime("%Y-%m-%d"))
                            
                    # Perform ERE on the video transcript
                    ere_result = perform_ere(transcript_text_with_timestamps)
                    logging.info(f"ERE Result: {ere_result}")
                    
                    # Extract entities, relations, and targets from the ERE result
                    ere_triples = ere_result.split("\n\n")
                    for triple in ere_triples:
                        if "Entity:" in triple:
                            triple_parts = triple.split("\n")
                            entity = triple_parts[0].replace("Entity: ", "")
                            relation = triple_parts[1].replace("Relation: ", "")
                            target = triple_parts[2].replace("Target: ", "")
                            
                            # Store the entity, relation, target, title, and date in the ere table
                            neo4j_utils = Neo4jUtils(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
                            neo4j_utils.store_ere_data(video_id, entity, relation, target, video_title, datetime.now().strftime("%Y-%m-%d"))
                            
                    # Perform syntactic analysis on the video transcript
                    syntactic_result = perform_syntactic_analysis(transcript_text_with_timestamps)
                    logging.info(f"Syntactic Analysis Result: {syntactic_result}")
                    if syntactic_result:
                        syntactic_data = syntactic_result.split("\n\n")
                        for data in syntactic_data:
                            if "Sentence:" in data:
                                data_parts = data.split("\n")
                                sentence = data_parts[0].replace("Sentence: ", "")
                                dependencies = data_parts[1].replace("Dependencies: ", "") if len(data_parts) > 1 else ""
                                
                                # Store the sentence, dependencies, title, and date in the syntactic table
                                neo4j_utils = Neo4jUtils(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
                                neo4j_utils.store_syntactic_data(video_id, sentence, dependencies, video_title, datetime.now().strftime("%Y-%m-%d"))
                    else:
                        logging.warning(f"No syntactic analysis result for video: {video_id}")
            else:
                logging.warning(f"Transcript for video {video_id} is not in the expected format.")
        else:
            logging.warning(f"Failed to retrieve transcript for video: {video_id}")
    else:
        logging.warning(f"Failed to retrieve details for video: {video_id}")