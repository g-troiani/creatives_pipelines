
#
# API/GOOGLE_API/AI_NEWS_GOOGLE_API/TRANSLATE_VIDEO_HIGHLIGHTS.PY
# 


import google.generativeai as genai
import time

def translate_video_highlights(highlights):
   try:
       model = genai.GenerativeModel('gemini-1.5-pro-latest')
       prompt = f"""Please translate the following video highlights from the original source language to Spanish, using the necessary technical vocabulary:

<highlights>

{highlights}

</highlights>

Provide your translation in the following format:

<translated_highlights>

[Your Spanish translation here]

</translated_highlights>"""

       response = model.generate_content(
           prompt,
           generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
       )
       translated_highlights = response.text
       print(f"Translated video highlights: {translated_highlights}")
       return translated_highlights
   except Exception as e:
       print(f'An error occurred while translating video highlights: {e}')
       return None
