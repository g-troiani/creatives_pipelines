#
# SCRAPERS/AI_NEWS_SCRAPERS/YOUTUBE_API_SCRAPER/FILTER_TITLES_BY_KEYWORDS.PY
#


import re

def filter_titles_by_keywords(title, keywords):
    title_lower = title.lower()
    return any(re.search(r'\b' + re.escape(keyword.lower()) + r'\b', title_lower) for keyword in keywords)

""" def filter_titles_by_keywords(title, keywords):
    title_lower = title.lower()
    for keyword in keywords:
        if keyword.lower() in title_lower:
            return True
    return False """