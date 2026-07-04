#You want the model to review a product review and always return rating (int) and summary (str). Write the Pydantic class for this, from memory, no looking back at old code.

from pydantic import BaseModel , field_validator
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class Product(BaseModel):
    rating : int
    summary : str

    @field_validator("rating")
    @classmethod
    def validate_rating(cls,value:int) -> int:
        if value < 0 or value > 100:
            raise ValueError("Rating must be between 0 to 100")
        return value

schema = Product.model_json_schema()
schema['additionalProperties'] = False

client = OpenAI(
    api_key = os.getenv("GROQ_API_KEY"),
    base_url = "https://api.groq.com/openai/v1"
)

response = client.responses.create(
    model = "openai/gpt-oss-120b",
    input = [
        {
            "role" : "developer",
            "content" : "You are a Product reviewer. First, think of 2 strengths and 2 weaknesses of this product. Then, based on that thinking, give a rating from 0 to 100. Keep the final response short and clean."
        },
        {
        "role" : "user",
        "content" : "A food delivery app that predicts what a user might want to order based on past orders, weather, and time of day, then offers quick one tap reordering."
        },  
    ],
    text = {
            "format" : {
            "type" : "json_schema",
            "name" : "Product_reviwer",
            "schema" : schema,
            "strict" : True
            }
        }
)

print(response.output_text)