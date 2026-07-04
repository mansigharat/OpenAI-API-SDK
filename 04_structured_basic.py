# We want the model's answer to come back in an exact shape we choose, not just any JSON.

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class Joke(BaseModel):
    setup: str
    punchline: str

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

schema = Joke.model_json_schema() # model_json_schema() is just convert python into json so api can understand that
schema["additionalProperties"] = False

response = client.responses.create(
    model="openai/gpt-oss-120b",
    input="what is capital of india ?",
    text={
        "format": {
            "type": "json_schema",
            "name": "joke",
            "schema": schema,
            "strict": True
        }
    }
)

print(response.output_text)