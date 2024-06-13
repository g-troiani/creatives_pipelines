#
# API/GOOGLE_API/AI_NEWS_GOOGLE_API/PERFORM_ERE.PY
# 


import google.generativeai as genai
import time

def perform_ere(text):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f"Perform Entity Relation Extraction (ERE) on the following text. Extract all entity-relation-entity triples from the text. Provide the output in the following format:\n\nEntity: [Entity 1]\nRelation: [Relation]\nEntity: [Entity 2]\n\nExample:\nEntity: Apple Inc.\nRelation: founded by\nEntity: Steve Jobs\n\nEntity: Steve Jobs\nRelation: was the CEO of\nEntity: Apple Inc.\n\nText:\n{text}",
            generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
        )
        ere_result = response.text
        print(f"Generated ERE result: {ere_result}")
        return ere_result
    except Exception as e:
        print(f'An error occurred while performing ERE: {e}')
        return None
