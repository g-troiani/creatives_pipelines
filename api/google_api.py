#
# API/GOOGLE_API.PY
# 

import google.generativeai as genai
import time
from ai_news_config import GENERATE_FORMATTED_SUMMARY_PROMPT, HACKERNEWS_SUMMARY_PROMPT, PERFORM_NER_PROMPT, PERFORM_ERE_PROMPT, PERFORM_SYNTACTIC_ANALYSIS_PROMPT

def generate_summary(transcript):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(
            GENERATE_FORMATTED_SUMMARY_PROMPT,
            generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
        )
        summary = response.text
        print(f"Generated summary: {summary}")
        return summary
    except Exception as e:
        print(f'An error occurred while generating the summary: {e}')
        return None

def generate_hackernews_summary(transcript):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            HACKERNEWS_SUMMARY_PROMPT,
            generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
        )
        summary = response.text
        print(f"Generated summary: {summary}")
        return summary
    except Exception as e:
        print(f'An error occurred while generating the summary: {e}')
        return None

def generate_formatted_summary(concatenated_summary, max_retries=3, retry_delay=60):
    retry_count = 0
    while retry_count < max_retries:
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(
                GENERATE_FORMATTED_SUMMARY_PROMPT,
                generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
            )
            formatted_summary = response.text
            print(f"Generated formatted summary: {formatted_summary}")
            return formatted_summary
        except Exception as e:
            if "rate_limit_error" in str(e) and retry_count < max_retries - 1:
                retry_count += 1
                print(f"Rate limit exceeded. Retrying in {retry_delay} seconds... (Attempt {retry_count}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print(f'An error occurred while generating the formatted summary: {e}')
                return None

def perform_ner(text):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            PERFORM_NER_PROMPT,
            generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
        )
        ner_result = response.text
        print(f"Generated NER result: {ner_result}")
        return ner_result
    except Exception as e:
        print(f'An error occurred while performing NER: {e}')
        return None

def perform_ere(text):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            PERFORM_ERE_PROMPT,
            generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
        )
        ere_result = response.text
        print(f"Generated ERE result: {ere_result}")
        return ere_result
    except Exception as e:
        print(f'An error occurred while performing ERE: {e}')
        return None

def perform_syntactic_analysis(text):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            PERFORM_SYNTACTIC_ANALYSIS_PROMPT,
            generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
        )
        syntactic_result = response.text
        print(f"Generated syntactic analysis result: {syntactic_result}")
        return syntactic_result
    except Exception as e:
        print(f'An error occurred while performing syntactic analysis: {e}')
        return None