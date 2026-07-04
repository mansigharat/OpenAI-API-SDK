from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.responses.create(
    model="openai/gpt-oss-120b",
    input="Tell me a short fact about space.",
    stream=True
)

full_text = ""

for event in response:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
        full_text += event.delta

print("\n\n--- SAVED TEXT ---")
print(full_text)