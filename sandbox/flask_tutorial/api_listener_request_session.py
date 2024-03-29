from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from threading import Thread
import queue
import uuid
import time

# Queue for communication
message_queue = queue.Queue()

app = Flask(__name__)
# CORS(app)  # Enable CORS for all domains on all routes


# The rest of your Flask app goes here

class Listener(Thread):
    def __init__(self, msg_queue):
        Thread.__init__(self)
        self.msg_queue = msg_queue
        self.session_store = {}

    def run(self):
        while True:
            # Check if there's a message in the queue
            if not self.msg_queue.empty():
                msg = self.msg_queue.get()
                # Process message (generate session ID here)
                session_id = str(uuid.uuid4())
                self.session_store[msg['request_id']] = session_id
                # Simulate processing time
                time.sleep(2)
                print(f"Processed request {msg['request_id']} with session ID: {session_id}")

    def get_session_id(self, request_id):
        # Return the session ID for a given request
        return self.session_store.get(request_id, "Processing")

@app.route('/request_session', methods=['POST'])
def request_session():
    data = request.json
    message_queue.put(data)
    return jsonify({"message": "Request received", "request_id": data['request_id']})

@app.route('/get_session', methods=['GET'])
def get_session():
    request_id = request.args.get('request_id')
    session_id = listener.get_session_id(request_id)
    return jsonify({"session_id": session_id})

if __name__ == '__main__':
    listener = Listener(message_queue)
    listener.start()
    app.run(debug=True, port=5000)
