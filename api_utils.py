from api.google_api.ai_news_google_api import generate_summary as generate_summary_google
from api.google_api.ai_news_google_api import generate_formatted_summary as generate_formatted_summary_google
from api.google_api.ai_news_google_api import perform_ner as perform_ner_google
from api.google_api.ai_news_google_api import perform_ere as perform_ere_google
from api.google_api.ai_news_google_api import perform_syntactic_analysis as perform_syntactic_analysis_google
from api.openai_api import generate_summary as generate_summary_openai
from api.openai_api import generate_formatted_summary as generate_formatted_summary_openai
from api.openai_api import perform_ner as perform_ner_openai
from api.openai_api import perform_ere as perform_ere_openai
from api.openai_api import perform_syntactic_analysis as perform_syntactic_analysis_openai
from api.anthropic_api import generate_summary as generate_summary_anthropic
from api.anthropic_api import generate_formatted_summary as generate_formatted_summary_anthropic
from api.anthropic_api import perform_ner as perform_ner_anthropic
from api.anthropic_api import perform_ere as perform_ere_anthropic
from api.anthropic_api import perform_syntactic_analysis as perform_syntactic_analysis_anthropic

# Set the API to use: 'google', 'openai', or 'anthropic'
API_TO_USE = 'google'

def generate_summary(transcript):
    if API_TO_USE == 'google':
        return generate_summary_google(transcript)
    elif API_TO_USE == 'openai':
        return generate_summary_openai(transcript)
    elif API_TO_USE == 'anthropic':
        return generate_summary_anthropic(transcript)
    else:
        raise ValueError(f"Invalid API selection: {API_TO_USE}")

def generate_formatted_summary(concatenated_summary, max_retries=3, retry_delay=60):
    if API_TO_USE == 'google':
        return generate_formatted_summary_google(concatenated_summary, max_retries, retry_delay)
    elif API_TO_USE == 'openai':
        return generate_formatted_summary_openai(concatenated_summary, max_retries, retry_delay)
    elif API_TO_USE == 'anthropic':
        return generate_formatted_summary_anthropic(concatenated_summary, max_retries, retry_delay)
    else:
        raise ValueError(f"Invalid API selection: {API_TO_USE}")

def perform_ner(text):
    if API_TO_USE == 'google':
        return perform_ner_google(text)
    elif API_TO_USE == 'openai':
        return perform_ner_openai(text)
    elif API_TO_USE == 'anthropic':
        return perform_ner_anthropic(text)
    else:
        raise ValueError(f"Invalid API selection: {API_TO_USE}")

def perform_ere(text):
    if API_TO_USE == 'google':
        return perform_ere_google(text)
    elif API_TO_USE == 'openai':
        return perform_ere_openai(text)
    elif API_TO_USE == 'anthropic':
        return perform_ere_anthropic(text)
    else:
        raise ValueError(f"Invalid API selection: {API_TO_USE}")

def perform_syntactic_analysis(text):
    if API_TO_USE == 'google':
        return perform_syntactic_analysis_google(text)
    elif API_TO_USE == 'openai':
        return perform_syntactic_analysis_openai(text)
    elif API_TO_USE == 'anthropic':
        return perform_syntactic_analysis_anthropic(text)
    else:
        raise ValueError(f"Invalid API selection: {API_TO_USE}")