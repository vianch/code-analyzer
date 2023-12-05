from flask import Flask, jsonify, request
from dataclasses import dataclass
from openai import OpenAI
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


api_key=os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

app = Flask(__name__)

# OpenAI Assistant creation and interaction code
@dataclass
class AssistantInfo:
    id: str
    name: str
    model: str

# Create OpenAI Assistant
assistant_info = AssistantInfo(
    id="your_assistant_id",
    name="Storymaker",
    model="gpt-4-1106-preview"
)

# Sample data (in-memory storage)
threads = []

# POST - Start OpenAI Assistant
@app.route('/start_assistant', methods=['POST'])
def start_assistant():
    global assistant_info
    global threads  
    
    assistant = client.beta.assistants.create(
      name = assistant_info.name,
      instructions="You are a personal math tutor, write a run code to answer math questions",
      tools=[{"type": "code_interpreter"}],
      model = assistant_info.model
    )
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image? do you think is human? if so what genre is the human?",
                    },
                ]
            }
        ]
    )
    

    thread = client.beta.threads.create()
    
    message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content="Solve this problem: 3x + 11 = 14"
    )

    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id,
    )
    
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id = run.id
    )
    
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id = run.id
    )

    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id = run.id
    )

    messages = client.beta.threads.messages.list(
      thread_id=thread.id,
    )
    

    chat_history = []
    for message in reversed(messages.data):
        chat_history.append({
            'thread_id': thread.id,
            'assistant_id': assistant.id,
            'role': message.role,
            'content': message.content[0].text.value,
            'message:': message.role + ": " + message.content[0].text.value
        })


    return jsonify({'thread_id': thread.id, 'chat_history': chat_history})

if __name__ == '__main__':
    app.run(debug=True)