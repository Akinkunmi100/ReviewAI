"""
Quick Backend Health Check
Run this before starting full tests to verify basic connectivity
"""

import requests
import sys

API_URL = "http://localhost:8001"

def check():
    print("🔍 Checking backend status...")
    print(f"   API URL: {API_URL}")
    print()
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is UP and responding!")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Database: {data.get('database', 'unknown')}")
            print()
            print("👉 You can now run: python test_backend.py")
            return 0
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return 1
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend!")
        print()
        print("Make sure the backend is running:")
        print("   1. Run: start_backend.bat")
        print("   OR")
        print("   2. Run: venv\\Scripts\\activate")
        print("   3. Run: uvicorn api:app --reload --port 8001")
        return 1
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check())
