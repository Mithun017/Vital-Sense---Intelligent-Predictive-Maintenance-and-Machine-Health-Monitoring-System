import requests

url = "http://localhost:8000/assistant/query"
payload = {
    "machine_id": "M-101",
    "text": "What is the current health of this machine?"
}

try:
    print(f"Testing endpoint: {url}")
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {str(e)}")
