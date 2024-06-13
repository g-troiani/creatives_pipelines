#
# SCRAPERS/AI_NEWS_SCRAPERS/TECHCRUNCH_SCRAPER/MAIN.PY
#

from scrapers.ai_news_scrapers.techcrunch_scraper.get_techcrunch_articles import get_techcrunch_articles
from scrapers.ai_news_scrapers.techcrunch_scraper.store_articles_in_database import store_articles_in_database

def main():
    # Scrape the latest articles from TechCrunch
    techcrunch_articles = get_techcrunch_articles()

    # Store the retrieved articles in the database
    store_articles_in_database(techcrunch_articles)

    print(f"{len(techcrunch_articles)} TechCrunch articles stored in the database")

if __name__ == "__main__":
    main()
