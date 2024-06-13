#
# SCRAPERS/AI_NEWS_SCRAPERS/HACKERNEWS_SCRAPER/SCRAPE_HACKER_NEWS.PY
# 


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import sqlite3
from utils.nlp_utils import generate_article_summary, perform_article_ner, perform_article_ere, perform_article_syntactic_analysis

def scrape_hacker_news():
    """
    Scrape Hacker News posts and comments from the first page and store them in the database.
    
    Returns:
        list: A list of dictionaries containing the article information.
    """
    articles = []

    # Construct the URL for the first page
    url = "https://news.ycombinator.com/news"

    # Send a request to the URL and parse the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the post rows on the page
    post_rows = soup.find_all("tr", class_="athing")
    print(f"Found {len(post_rows)} article links on the Hacker News homepage")

    # Get the current timestamp
    current_timestamp = datetime.now()

    for row in post_rows:
        # Extract the title and link for each post
        title_element = row.find("span", class_="titleline")
        title = title_element.text.strip()
        link = title_element.find("a")["href"]
        print(f"Processing article: {link}")

        # Construct the page URL for the post
        if link.startswith("http"):
            page_url = link
        else:
            page_url = f"https://news.ycombinator.com/{link}"

        # Extract the post ID and construct the comments URL
        post_id = row["id"]
        comments_url = f"https://news.ycombinator.com/item?id={post_id}"

        # Send a request to the comments URL and parse the HTML content
        comments_response = requests.get(comments_url)
        comments_soup = BeautifulSoup(comments_response.content, "html.parser")

        # Find all the comments for the post
        comments = comments_soup.find_all("div", class_="comment")

        # Extract the text content of each comment
        comment_texts = [comment.find("span", class_="commtext").text.strip() for comment in comments if comment.find("span", class_="commtext") is not None]

        # Join the comment texts into a single string
        comments_text = "\n".join(comment_texts)

        # Concatenate the post title and comments
        post_text = f"Title: {title}\nComments:\n{comments_text}\n\n"

        # Generate a unique article ID
        article_id = link

        # Generate a summary of the post and comments
        article_summary = generate_article_summary(post_text.strip())
        print(f"Generated article summary: {article_summary}")

        # Perform NER on the post and comments
        ner_result = perform_article_ner(post_text.strip())

        # Perform ERE on the post and comments
        ere_result = perform_article_ere(post_text.strip())

        # Perform syntactic analysis on the post and comments
        syntactic_result = perform_article_syntactic_analysis(post_text.strip())

        # Create a dictionary containing the article information
        article_info = {
            "Title": title,
            "URL": link,
            "Page URL": page_url,
            "Text": post_text.strip(),
            "Summary": article_summary,
            "NER": ner_result,
            "ERE": ere_result,
            "Syntactic": syntactic_result
        }

        # Append the article information to the articles list
        articles.append(article_info)

    return articles