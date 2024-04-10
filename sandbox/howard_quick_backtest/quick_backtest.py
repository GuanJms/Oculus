import requests
import urllib.request
import json

BASE = 'http://127.0.0.1:8000'


def read_next_line(time, public_token, private_key):
    url = f'{BASE}/timeline/time/next/'
    response = requests.get(url, params={'public_token': public_token, 'key': private_key, 'time': time})
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)


def start_connection(ticker='TSLA', date=20240301):
    url = f'{BASE}/timeline/start/'
    ticker_info = {
        ticker: {
            'DOMAINS': 'EQUITY.STOCK.QUOTE',
            'DATE': date
        }
    }
    data = json.dumps(ticker_info).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        response_data = response.read()
        data = json.loads(response_data)
        return data


time = int(9.5 * 60 * 1000 * 60)
freq = 1000
connection_data_json = start_connection()
public_token = connection_data_json['public_token']
private_key = connection_data_json['private_key']
failed_tickers = connection_data_json['failed_tickers']
errors = connection_data_json['errors']

received_data = []
data = read_next_line(time, public_token, private_key)
received_data.append(data['data'])
while data['status'] != 'DONE':
    data = read_next_line(time, public_token, private_key)
    received_data.append(data['data'])

print(received_data)