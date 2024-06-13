#
# SCRAPERS/AI_NEWS_SCRAPERS/TECHCRUNCH_SCRAPER/GET_TECHCRUNCH_ARTICLES.PY
#

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import sqlite3
from utils.nlp_utils import generate_article_summary, perform_article_ner, perform_article_ere, perform_article_syntactic_analysis

def get_techcrunch_articles():
    """
    Retrieve all articles uploaded on TechCrunch in the past 24 hours.
    
    Returns:
        list: A list of dictionaries containing the article information.
    """
    articles = []

    # Construct the URL for the TechCrunch homepage
    url = "https://techcrunch.com/"

    # Send a request to the URL and parse the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the article links on the homepage
    article_links = soup.find_all("h2", class_="post-block__title")
    print(f"Found {len(article_links)} article links on the TechCrunch homepage")

    # Get the current timestamp
    current_timestamp = datetime.now()

    for link in article_links:
        # Extract the article URL
        article_url = link.find("a")["href"]
        print(f"Processing article: {article_url}")

        # Send a request to the article URL and parse the HTML content
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.content, "html.parser")

        # Extract the article timestamp
        timestamp_element = article_soup.find("time", class_="river-byline__time")
        if timestamp_element:
            timestamp_str = timestamp_element["datetime"]
            timestamp = parser.parse(timestamp_str)
            print(f"Article timestamp: {timestamp}")
        else:
            print("Skipping article: Timestamp element not found")
            continue

        # Check if the article was uploaded within the past 24 hours
        if current_timestamp - timestamp <= timedelta(hours=24):
            print("Article is within the past 24 hours")

            # Extract the article title
            title_element = article_soup.find("h1", class_="article__title")
            if title_element:
                title = title_element.text.strip()
                print(f"Article title: {title}")
            else:
                print("Skipping article: Title element not found")
                continue

            # Extract the full text of the article
            article_text = ""
            article_content = article_soup.find("div", class_="article-content")
            if article_content:
                article_paragraphs = article_content.find_all("p")
                for paragraph in article_paragraphs:
                    article_text += paragraph.text.strip() + "\n\n"
                print(f"Extracted article text: {article_text[:100]}...")
            else:
                print("Skipping article: Article content not found")
                continue

            # Generate a summary of the article text using the generate_article_summary function from nlp_utils
            article_summary = generate_article_summary(article_text.strip())
            print(f"Generated article summary: {article_summary}")

            # Perform NER on the article text
            ner_result = perform_article_ner(article_text.strip())

            # Perform ERE on the article text
            ere_result = perform_article_ere(article_text.strip())

            # Perform syntactic analysis on the article text
            syntactic_result = perform_article_syntactic_analysis(article_text.strip())

            # Create a dictionary containing the article information
            article_info = {
                "Title": title,
                "URL": article_url,
                "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "Text": article_text.strip(),
                "Summary": article_summary,
                "NER": ner_result,
                "ERE": ere_result,
                "Syntactic": syntactic_result
            }

            # Append the article information to the articles list
            articles.append(article_info)
        else:
            print("Skipping article: Not within the past 24 hours")

    return articles
