#
# API/GOOGLE_API/AI_NEWS_GOOGLE_API/GENERATE_FORMATTED_SUMMARY.PY
# 

import google.generativeai as genai
import time

def generate_formatted_summary(concatenated_summary, max_retries=3, retry_delay=60):
    retry_count = 0
    while retry_count < max_retries:
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(
                f"Your task is to summarize a long text and break it down into an easily digestible format for a busy reader. The goal is to capture as much of the meaning and insights from the text as possible while keeping the summary concise and structured. The reader will receive the summary via email, so it should be no longer than one single-spaced page in a .docx format.\nBias Level: [Provide one of the following categories that represent the level of bias of the text: 'extremist', 'very bias', 'slightly bias', 'reasonably objective']\nTopics: [Provide a a comma separated list of 3-6 topics that are the main focus of the text or classify the concepts elaborated in the text (1-3 words each; separated by commas)]\n<text>\n{concatenated_summary}\n</text>\nPlease follow these steps:\nCarefully read through the provided text and identify the key points, main ideas, and important details.\nOrganize the information you've gathered into a structured format, such as an outline or bullet points grouped logically. This will make the summary more easily digestible for the reader.\nAs you create the summary, keep in mind that it should be concise. Aim for a maximum of one single-spaced page in a .docx format.\nWhile keeping the summary brief, do your best to capture as much of the meaning and insights from the original text as possible. The goal is to provide the reader with a comprehensive understanding of the text's content.\nRemember, the reader is busy and will be receiving this summary via email, so it's crucial that the information is presented in a clear, concise, and structured manner. Your summary should provide them with a thorough understanding of the text's key points and insights without requiring them to read the entire original document.",
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