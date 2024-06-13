#
# API/GOOGLE_API/AI_NEWS_GOOGLE_API/PERFORM_SYNTACTIC_ANALYSIS.PY
# 


import google.generativeai as genai
import time

def perform_syntactic_analysis(text):
   try:
       model = genai.GenerativeModel('gemini-pro')
       response = model.generate_content(
           f"Perform syntactic analysis on the following text. Provide the output in the following format:\n\nSentence: [Sentence]\nDependencies: [Dependency Parse]\n\nExample:\nSentence: John hit the ball.\nDependencies: (ROOT (S (NP (NNP John)) (VP (VBD hit) (NP (DT the) (NN ball))) (. .)))\n\nText:\n{text}",
           generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
       )
       syntactic_result = response.text
       print(f"Generated syntactic analysis result: {syntactic_result}")
       return syntactic_result
   except Exception as e:
       print(f'An error occurred while performing syntactic analysis: {e}')
       return None

