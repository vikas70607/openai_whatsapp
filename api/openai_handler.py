from openai import OpenAI
import time
import os
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'))

ASSISTANT_ID = os.getenv('ASSISTANT_ID')

def push_message_to_thread(thread_id, text):
    print(text)
    message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=text
    )
    return message

def response(thread_id):
    run = client.beta.threads.runs.create_and_poll(
    thread_id= thread_id,
    assistant_id=ASSISTANT_ID,
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id= thread_id, run_id=run.id)
    
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            print("Run completed. Messages:")
            return messages.data[0].content[0].text.value
        else:
            time.sleep(1)

def create_thread(name, text):
    # Create a new thread with the given name and text
    thread = client.beta.threads.create()
    first_message = f'Hi My name is {name}, {text}'
    print("Thread ID:", thread.id, "First message:", first_message)
    push_message_to_thread(thread.id,first_message)
    return thread.id