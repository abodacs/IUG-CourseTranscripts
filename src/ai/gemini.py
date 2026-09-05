import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse
from tenacity import retry, wait_random_exponential
from pydantic import BaseModel, Field
from pydantic_core import from_json
from ..config import GEMINI_API_KEY
from ..utils import save_file, open_file
from time import time

genai.configure(api_key=GEMINI_API_KEY)

class Course(BaseModel):
    name: str | None = Field(..., description="The name of the course.")
    faculty: str | None = Field(..., description="The Faculty that offers the course.")
    topic: str | None = Field(..., description="A brief description of the course's main topic.")
    instructor: str | None = Field(..., description="Information about the instructor, including their background and expertise.")
    target_audience: str | None = Field(..., description="The intended audience for the course. Note: Target audience is ALWAYS Arabic Speaking student Audience.")

class Chapter(BaseModel):
    start_ts: float | None = Field(..., description="The start timestamp indicating when the chapter starts in the video.")
    title: str | None = Field(..., description="A concise, short and descriptive title for the chapter.")

@retry(wait=wait_random_exponential(multiplier=1, max=120))
def genai_completion(prompt, response_schema=None):
    filename = f'{time()}_gemini.txt'
    generation_config = {"temperature": 2}
    if response_schema:
        generation_config["response_mime_type"] = "application/json"
        generation_config["response_schema"] = response_schema
    
    model = genai.GenerativeModel("gemini-1.5-flash-latest", generation_config=generation_config)
    
    try:
        response: GenerateContentResponse = model.generate_content(
            prompt,
            safety_settings={
                'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
            }
        )
        text = response.text
        save_file(f'./gemini_logs/{filename}', prompt + '\n\n==========\n\n' + text)
        if response_schema:
            return from_json(text, allow_partial=False)
        return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def enrich_playlist_details(title, description):
    prompt = open_file('src/ai/prompts/enrich_playlist.txt').replace(
        '<<PLAYLISTTITLE>>', title or "").replace(
        '<<DESCRIPTION>>', description or "")
    course_data = genai_completion(prompt, response_schema=Course)
    if course_data:
        return Course.model_validate(course_data)
    return None

def extract_chapters(transcript_text):
    prompt = open_file('src/ai/prompts/clarify_transcript.txt').replace(
        '<<TRANSCRIPT>>', transcript_text)
    chapters_data = genai_completion(prompt, response_schema=list[Chapter])
    if chapters_data:
        return [Chapter.model_validate(chapter) for chapter in chapters_data]
    return []