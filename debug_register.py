import requests
import json

url = "http://localhost:8001/api/auth/register"
payload = {
    "email": "reproduce_error@example.com",
    "password": "password123"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Request execution failed: {e}")
