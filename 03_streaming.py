from pydantic import BaseModel , field_validator ,ConfigDict
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class ResumeReview(BaseModel):
    model_config = {"extra": "forbid"}
    score: int
    feedback: str

    @field_validator("score")
    @classmethod
    def validate_score(cls, value: int) -> int:
        if value < 0 or value > 100:
            raise ValueError("Score must be between 0 and 100")
        return value

schema = ResumeReview.model_json_schema()
schema["additionalProperties"] = False


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.responses.create(
    model = "openai/gpt-oss-120b",
    input = "Tell me a short story about a cat.",
    stream = True
    
)
full_text = ""

for event in response:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
        full_text += event.delta

print("\n\n--- FULL SAVED TEXT ---")
print(full_text)
