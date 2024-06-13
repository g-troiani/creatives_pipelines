#
# AI_NEWS_MAIN.PY
# 


import sqlite3
import logging
import subprocess
import random
from datetime import datetime, timedelta
import time
from scrapers.ai_news_scrapers.hackernews_scraper.scrape_hacker_news import scrape_hacker_news
from scrapers.ai_news_scrapers.hackernews_scraper.store_articles_in_database import store_articles_in_database as store_hackernews_articles_in_database
from scrapers.ai_news_scrapers.techcrunch_scraper.get_techcrunch_articles import get_techcrunch_articles
from scrapers.ai_news_scrapers.techcrunch_scraper.store_articles_in_database import store_articles_in_database as store_techcrunch_articles_in_database
from utils.nlp_utils import generate_article_summary, perform_article_ner, perform_article_ere, perform_article_syntactic_analysis
from ai_news_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, DB_FILE
from utils.database.ai_news_database.create_tables import create_tables
from utils.database.ai_news_database.create_daily_report_table import create_daily_report_table
from utils.database.ai_news_database.create_hacker_news_table import create_hacker_news_table
from utils.database.ai_news_database.create_techcrunch_table import create_techcrunch_table
from utils.ai_news_content_creation import create_social_media_content_table
from utils.report_generator import generate_daily_report
from utils.email_sender import send_email
from youtube_processor import process_youtube_videos
from graph_processor import process_graph_data
from utils.graph.ai_news_graph.store_ner_data import store_ner_data
from utils.graph.ai_news_graph.store_ere_data import store_ere_data
from utils.graph.ai_news_graph.store_syntactic_data import store_syntactic_data




logging.basicConfig(level=logging.INFO)

def main():
    # Boolean variables to control data sources
    include_youtube = True
    include_hacker_news = False
    include_techcrunch = False
    graph_module = False  # Set to False to disable the graph-related code
    perform_analysis = False  # Set to False to disable NER, ERE, and syntactic analysis
    report_generator_email_module = False  # Set to False to disable report generation and email sending
    creatives = True  # Set to False to disable video highlights and social media creatives generation

    create_tables()
    create_hacker_news_table()  # Ensure hacker_news table is created
    create_daily_report_table()
    create_techcrunch_table()  # Create the techcrunch table
    create_social_media_content_table()  # Create the social_media_content table

    if include_youtube:
        process_youtube_videos(perform_analysis, creatives)

    hacker_news_articles = []
    if include_hacker_news:
        # Scrape the latest articles from Hacker News
        hacker_news_articles = scrape_hacker_news()
        store_hackernews_articles_in_database(hacker_news_articles)

    techcrunch_articles = []
    if include_techcrunch:
        # Scrape the latest articles from TechCrunch
        techcrunch_articles = get_techcrunch_articles()
        store_techcrunch_articles_in_database(techcrunch_articles)
        
        for article in techcrunch_articles:
            article_summary = generate_article_summary(article["Text"].strip())
            article["Summary"] = article_summary
            if perform_analysis:
                if graph_module:
                    ner_result = perform_article_ner(article["Text"].strip())
                    ere_result = perform_article_ere(article["Text"].strip())
                    syntactic_result = perform_article_syntactic_analysis(article["Text"].strip())
                    store_ner_data(article["URL"], ner_result, article["Title"], article["Timestamp"])
                    store_ere_data(article["URL"], ere_result, article["Title"], article["Timestamp"])
                    store_syntactic_data(article["URL"], syntactic_result, article["Title"], article["Timestamp"])

    if graph_module:
        process_graph_data()

    if report_generator_email_module:
        # Generate the AI and Technology Executive Briefing
        report_path = generate_daily_report(hacker_news_articles, techcrunch_articles)
        
        # Print the generated formatted summary
        logging.info(f"Generated formatted summary: {report_path}")
        if report_path:
            send_email(report_path)
            logging.info("AI and Technology Executive Briefing generated and sent via email.")
        else:
            logging.warning("Failed to generate the AI and Technology Executive Briefing. Email not sent.")

    if creatives:
        # Generate Instagram creatives
        logging.info("Generating Instagram creatives...")
        try:
            subprocess.run(["python", "generate_instagram_creatives.py"], check=True)
            logging.info("Instagram creatives generated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error generating Instagram creatives: {e}")
        except FileNotFoundError as e:
            logging.error(f"generate_instagram_creatives.py not found: {e}")

    logging.info("Running ig_poster.py...")
    try:
        subprocess.run(["python", "ig_poster.py"], check=True)
        logging.info("ig_poster.py executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running ig_poster.py: {e}")
    except FileNotFoundError as e:
        logging.error(f"ig_poster.py not found: {e}")

if __name__ == '__main__':
    logging.info("Starting the script...")
    main()
    logging.info("Script execution completed.")