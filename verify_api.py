import requests
import sys

def check_url(url):
    try:
        print(f"Checking {url}...")
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"SUCCESS: {url} is reachable")
            return True
        else:
            print(f"FAILURE: {url} returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILURE: Could not connect to {url}: {e}")
        return False

print("Verifying API connectivity...")
success_localhost = check_url("http://localhost:8001/docs")
success_ip = check_url("http://127.0.0.1:8001/docs")

if success_localhost or success_ip:
    print("OVERALL SUCCESS: API is reachable")
    sys.exit(0)
else:
    print("OVERALL FAILURE: API is not reachable")
    sys.exit(1)
