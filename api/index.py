from flask import Flask, request, jsonify
from db_handler import upsert_entry, get_entry
from message_handler import send_message, send_session_message
from openai_handler import create_thread

app = Flask(__name__)

@app.route('/input', methods=['POST'])
def receive_json():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received or invalid format"}), 400

    phone_id = data.get('waId')
    name = data.get('senderName')
    text = data.get('text')

    if not phone_id or not name or not text:
        return jsonify({"error": "Missing required fields"}), 400

    print("Received JSON:", phone_id, name, text)

    existing_entry = get_entry(phone_id)

    if existing_entry:
        thread_id = existing_entry[0]['threadId']
        message = send_message(text, thread_id)
        send_session_message(message,phone_id)
        print('Entry exists, message sent to existing thread')
        return jsonify({"message": "Entry updated and message sent"}), 200
    else:
        thread_id = create_thread(name,text)
        upsert_entry(phone_id, name, thread_id)
        message = send_message(text, thread_id)
        send_session_message(message,phone_id)
        print('New entry created and message sent')
        return jsonify({"message": "New entry created and message sent"}), 200

if __name__ == '__main__':
    app.run(debug=True)
