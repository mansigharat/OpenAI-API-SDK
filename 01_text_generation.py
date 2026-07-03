# You send the model two things: instructions (how it should behave) and input (what you're asking it to do). It sends back an answer.
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.responses.create(
    model = "openai/gpt-oss-120b",
    input = [
        {
            "role" : "developer",
            "content" : "You are Zomato's customer support bot. Only answer questions about food orders, delivery, refunds, and the app. If the user asks anything unrelated, such as coding, movies, or general knowledge, respond only with: I can only help with Zomato-related questions. Do not explain why, do not offer alternatives, and do not break character."
        },
        {
            "role" : "user",
            "content" : "what's your favorite movie"
        }
    ]
)

print(response.output_text)