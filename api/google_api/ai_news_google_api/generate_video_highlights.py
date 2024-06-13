#
# API/GOOGLE_API/AI_NEWS_GOOGLE_API/GENERATE_VIDEO_HIGHLIGHTS.PY
# 


import google.generativeai as genai
import time

def generate_video_highlights(transcript):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        prompt = f"""Here is the full transcript of a video:

<transcript>

{transcript}

</transcript>

Please read through the entire video transcript carefully. Based on the full content of the video, identify the most important key points and highlights. For each key point:

1. Select the most relevant 3-5 sentences from the transcript that best capture that point.

2. Find the timestamp range in the video where those sentences occurred. Ensure that each highlight clip does not exceed 15-20 seconds.

Before providing your final answer, do one more thorough review of the full video transcript to make sure you have captured the most critical and essential highlights.

Provide your final answer in the following format:

<result>

1. [00:00 - 00:10] [First key sentence(s)]

2. [00:11 - 00:25] [Second key sentence(s)]

3. [00:26 - 00:40] [Third key sentence(s)]

...

</result>"""

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=4096)
        )
        highlights = response.text
        print(f"Generated video highlights: {highlights}")
        return highlights
    except Exception as e:
        print(f'An error occurred while generating video highlights: {e}')
        return None