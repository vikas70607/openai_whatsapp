from openai_handler import push_message_to_thread, response
from dotenv import load_dotenv
import requests
import urllib.parse
import os

load_dotenv(override=True)

# Example Usage:
bearer_token = os.getenv('WATI_BEARER_TOKEN')


def send_session_message(message_text, wa_id):
    # API endpoint
    url = f"https://live-mt-server.wati.io/403483/api/v1/sendSessionMessage/{wa_id}?messageText={urllib.parse.quote(message_text)}"
    print(url)
    # Headers including Bearer Token for Authorization
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    
    # Send the HTTP GET request
    response = requests.post(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Returns the response as a JSON object
    else:
        return {'error': f"Failed to send message. Status code: {response.status_code}"}

    

def send_message(text, threadId):
    push_message_to_thread(threadId, text)
    return response(threadId)

if __name__ == "__main__":
    # Example usage
    wa_id = '917982850447'
    message_text = 'Hello, this is a test message!'
    send_session_message(message_text, wa_id)
    