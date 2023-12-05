from openai import OpenAI
import requests
import json
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


def get_flight_detail(flight_number):
    access_key = os.getenv('FLIGHT_API_KEY')
    url = f"http://api.aviationstack.com/v1/flights?access_key={access_key}&flight_iata={flight_number}"
    response = requests.get(url=url)
    flight_data_response = response.json()
    flight_data = flight_data_response['data'][0]
    
    flight_status = flight_data["flight_status"]
    actual_landing_date = flight_data["arrival"]["scheduled"]
    estimated_landing_date = flight_data["arrival"]["estimated"]
    airline = flight_data["airline"]["name"]
    
    return f"""Here is some information about flight {flight_number}:\n
        - The airline name is: {airline}\n
        - The flight status is: {flight_status}\n
        - The flight's estimated landing datetime is: {estimated_landing_date}\n
        - The flight did land at: {actual_landing_date}"""
    
# get_flight_detail("AA733")
"""
assistant = client.beta.assistants.create(
  name = "Flight assistant",
  instructions="You are a helpful assistant. if you are asked about a flight, use flight number with the provided get_flight_detail function to get information about the flight, then answer the user's question with that data exclusively",
  tools=[{"type": "retrieval"}],
  model = "gpt-4-1106-preview"
)
"""
api_key=os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
env_assistant_id = os.getenv('ASSISTANT_ID')

assistant = client.beta.assistants.retrieve(
    assistant_id=env_assistant_id,
)

thread = client.beta.threads.create()

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="When is the the flight AA733 arriving?"
)

run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

print("\nrun.required_action\n",run.required_action)

messages = client.beta.threads.messages.list(
  thread_id=thread.id,
)

print(messages)



#tool_calls = run.required_action.submit_tool_outputs.tool_calls

# print(tool_calls)

# def get_outputs_for_tool_call(tool_call):
  