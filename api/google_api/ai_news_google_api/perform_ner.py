#
# API/GOOGLE_API/AI_NEWS_GOOGLE_API/PERFORM_NER.PY
# 



import google.generativeai as genai
import time

def perform_ner(text):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f"Perform Named Entity Recognition (NER) on the following text. Extract all named entities and count the number of times each entity is mentioned in the text. Provide the output in the following format:\n\nEntity: [Entity Name]\nCount: [Number of mentions]\n\nExample:\nEntity: Apple Inc.\nCount: 5\n\nEntity: Steve Jobs\nCount: 3\n\nText:\n{text}",
            generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
        )
        ner_result = response.text
        print(f"Generated NER result: {ner_result}")
        return ner_result
    except Exception as e:
        print(f'An error occurred while performing NER: {e}')
        return None
