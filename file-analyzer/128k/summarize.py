import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

with open("summary.txt") as f:
    book_text = f.read()
    
response = openai.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
        {
            "role": "user",
            "content": book_text + "\n\n####\n\n What delivery rate does the book recommend?"
        }
    ]
)

print(response.choices[0].message.content)
print(f"\nTotal tokens: {response.usage.total_tokens}")