from api.google_api.ai_news_google_api.generate_summary import generate_summary
from api.google_api.ai_news_google_api.perform_ner import perform_ner
from api.google_api.ai_news_google_api.perform_ere import perform_ere
from api.google_api.ai_news_google_api.perform_syntactic_analysis import perform_syntactic_analysis

# Rest of the code remains the same
__all__ = [
    'generate_article_summary',
    'perform_article_ner',
    'perform_article_ere',
    'perform_article_syntactic_analysis',
]

def generate_article_summary(article_text):
    return generate_summary(article_text.strip())

def perform_article_ner(article_text):
    return perform_ner(article_text.strip())

def perform_article_ere(article_text):
    return perform_ere(article_text.strip())

def perform_article_syntactic_analysis(article_text):
    return perform_syntactic_analysis(article_text.strip())
