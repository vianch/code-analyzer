from openai import OpenAI
import base64
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

api_key=os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

assistant = client.beta.assistants.create(
    model="gpt-4-1106-preview",
)

thread = client.beta.threads.create()

print(f"Assistant ID: {assistant.id}")
print(f"Thread ID: {thread.id}\n")

print("GPT: Hello! How can I assist you today?")

while True:
    message = input("You: ")
    print()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while True:
        run = client.beta.threads.runs.retrieve(
            run_id=run.id,
            thread_id=thread.id,
        )

        if run.status not in ["queued", "in_progress", "cancelling"]:
            break

    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        limit=1,
    )
    print("GPT: " + messages.data[0].content[0].text.value)