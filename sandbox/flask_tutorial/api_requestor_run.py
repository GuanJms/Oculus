import uuid

import requests
import time

class Requester:
    def __init__(self, base_url):
        self.base_url = base_url

    def request_session(self):
        # Generate a unique request_id
        request_id = str(uuid.uuid4())
        response = requests.post(
            f"{self.base_url}/request_session",
            json={"request_id": request_id},
            headers={"Content-Type": "application/json"}  # Ensure correct content type
        )
        if response.status_code == 200:
            print(f"Request submitted successfully. Request ID: {request_id}")
            return request_id
        else:
            print(response.status_code)
            print("Failed to submit request")
            return None

    def get_session_id(self, request_id):
        while True:
            response = requests.get(f"{self.base_url}/get_session", params={"request_id": request_id})
            if response.status_code == 200:
                data = response.json()
                if data['session_id'] != "Processing":
                    print(f"Session ID for request {request_id}: {data['session_id']}")
                    break
                else:
                    print("Session is still processing. Waiting...")
            else:
                print("Failed to retrieve session ID")
                break
            time.sleep(2)  # Polling interval

if __name__ == '__main__':
    base_url = "http://127.0.0.1:5000"
    requester = Requester(base_url)

    # Request a session
    request_id = requester.request_session()
    if request_id:
        # Poll for session ID
        requester.get_session_id(request_id)


