import requests

response = requests.post('http://127.0.0.1:5000/test', json={"test": "data"})
print(response.status_code, response.json())
