from openai import OpenAI

from keys import *

client = OpenAI(
    api_key= OPENAI_API_KEY 
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Human-Cyborg Relations droid in the Star Wars universe named B-1, equipped to be a friendly and polite presence to those in need of help"},
        {"role": "user", "content": "Hello, can you tell me the nearest spaceport in Naboo?"}
    ]
)

print(response.choices[0].message)

