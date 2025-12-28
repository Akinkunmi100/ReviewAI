"""
Error Diagnosis Tool
Run this to capture the exact error when searching for a product
"""

import requests
import json
import traceback
import sys

API_URL = "http://localhost:8001"

def test_search_with_error_capture():
    """Test product search and capture detailed error information"""
    
    print("="*70)
    print("ERROR DIAGNOSIS - Product Search Test")
    print("="*70)
    print()
    
    # Test with a simple product
    test_product = "iPhone 14"
    
    print(f"🔍 Testing search for: {test_product}")
    print(f"   API URL: {API_URL}/api/review")
    print()
    
    payload = {
        "product_name": test_product,
        "use_web": True,
        "user_id": "test_diagnosis_user"
    }
    
    print("📤 Sending request...")
    print(f"   Payload: {json.dumps(payload, indent=2)}")
    print()
    
    try:
        response = requests.post(
            f"{API_URL}/api/review",
            json=payload,
            timeout=120
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print()
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Check if there's an error in the response
                if "error" in data:
                    print("❌ ERROR IN RESPONSE:")
                    print(f"   Message: {data['error'].get('message', 'Unknown error')}")
                    print()
                    return False
                    
                # Success case
                print("✅ SUCCESS! Product review generated")
                print(f"   Product: {data.get('product_name', 'N/A')}")
                print(f"   Score: {data.get('overall_score', 'N/A')}/10")
                return True
                
            except json.JSONDecodeError as e:
                print("❌ RESPONSE IS NOT VALID JSON")
                print(f"   Error: {e}")
                print(f"   Raw response: {response.text[:500]}")
                return False
                
        else:
            print(f"❌ HTTP ERROR: Status {response.status_code}")
            print()
            print("Response Body:")
            print(response.text[:1000])
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR")
        print("   Cannot connect to the backend API")
        print()
        print("Solutions:")
        print("   1. Make sure the backend is running")
        print("   2. Run: start_backend.bat")
        print("   3. Check if port 8001 is available")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT ERROR")
        print("   Request took too long (>120 seconds)")
        print()
        print("Possible causes:")
        print("   1. Web scraping is very slow")
        print("   2. GROQ API is not responding")
        print("   3. Network issues")
        return False
        
    except Exception as e:
        print("❌ UNEXPECTED ERROR")
        print(f"   Type: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        print()
        print("Full traceback:")
        traceback.print_exc()
        return False

def check_backend_logs():
    """Instructions for checking backend logs"""
    print()
    print("="*70)
    print("NEXT STEPS: Check Backend Logs")
    print("="*70)
    print()
    print("To see detailed error logs:")
    print("1. Look at the terminal where you started the backend")
    print("2. You should see error messages with full stack traces")
    print("3. Common errors to look for:")
    print("   - GROQ_API_KEY issues")
    print("   - Web scraping failures")
    print("   - Database errors")
    print("   - Module import errors")
    print()
    print("If you see error logs, copy them and I can help diagnose!")

def main():
    result = test_search_with_error_capture()
    
    print()
    print("="*70)
    print("DIAGNOSIS SUMMARY")
    print("="*70)
    
    if result:
        print("✅ Search is working! No errors found.")
    else:
        print("❌ Search failed - see error details above")
        check_backend_logs()
    
    print()
    print("="*70)
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())
