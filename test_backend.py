"""
Comprehensive Backend Testing Script
Tests all major endpoints and functionality of the Product Review Engine API
"""

import requests
import json
import time
from typing import Dict, Any
import sys

# Configuration
API_BASE_URL = "http://localhost:8001"
TEST_USER_ID = "test_user_123"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_test(test_name: str):
    """Print test name"""
    print(f"{Colors.BOLD}{Colors.BLUE}Testing: {test_name}{Colors.RESET}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.RESET}")

def test_health_endpoint() -> bool:
    """Test the health check endpoint"""
    print_test("Health Check Endpoint")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed: {data}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to the API. Is the server running?")
        print_info(f"Make sure the backend is running: uvicorn api:app --reload --port 8001")
        return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_review_endpoint() -> bool:
    """Test the product review endpoint"""
    print_test("Product Review Endpoint")
    
    payload = {
        "product_name": "iPhone 14 Pro",
        "use_web": True,
        "user_id": TEST_USER_ID
    }
    
    try:
        print_info("Sending review request (this may take 30-60 seconds)...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/api/review",
            json=payload,
            timeout=120  # 2 minutes timeout for review generation
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Review generated in {elapsed:.2f} seconds")
            
            # Check key fields
            if "product_name" in data:
                print_success(f"Product: {data['product_name']}")
            if "overall_score" in data:
                print_success(f"Overall Score: {data['overall_score']}/10")
            if "specs" in data and data["specs"]:
                print_success(f"Specs found: {len(data['specs'])} items")
            if "nigerian_prices" in data and data["nigerian_prices"]:
                print_success(f"Nigerian prices found: {len(data['nigerian_prices'])} retailers")
            if "pros" in data:
                print_success(f"Pros found: {len(data['pros'])} items")
            if "cons" in data:
                print_success(f"Cons found: {len(data['cons'])} items")
            
            return True
        else:
            print_error(f"Review failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Request timed out. The API might be slow or stuck.")
        return False
    except Exception as e:
        print_error(f"Review test error: {e}")
        return False

def test_chat_endpoint() -> bool:
    """Test the chat endpoint"""
    print_test("Chat Endpoint")
    
    payload = {
        "product_name": "iPhone 14 Pro",
        "message": "What's the battery life like?",
        "conversation_history": [],
        "use_web": False,  # Use AI-only mode for faster response
        "user_id": TEST_USER_ID
    }
    
    try:
        print_info("Sending chat message...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json=payload,
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Chat response received in {elapsed:.2f} seconds")
            
            if "reply" in data:
                reply_text = data["reply"][:100] + "..." if len(data["reply"]) > 100 else data["reply"]
                print_success(f"Reply: {reply_text}")
            
            if "session_id" in data:
                print_success(f"Session ID: {data['session_id']}")
            
            return True
        else:
            print_error(f"Chat failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Chat test error: {e}")
        return False

def test_history_summary_endpoint() -> bool:
    """Test the history summary endpoint"""
    print_test("History Summary Endpoint")
    
    payload = {
        "user_id": TEST_USER_ID
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/history/summary",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("History summary retrieved")
            
            if "analyzed_products" in data:
                count = len(data["analyzed_products"])
                print_success(f"Analyzed products: {count}")
            
            if "chat_sessions" in data:
                count = len(data["chat_sessions"])
                print_success(f"Chat sessions: {count}")
            
            return True
        else:
            print_error(f"History summary failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"History summary test error: {e}")
        return False

def test_compare_endpoint() -> bool:
    """Test the compare endpoint"""
    print_test("Product Comparison Endpoint")
    
    payload = {
        "products": ["iPhone 14 Pro", "Samsung Galaxy S23"]
    }
    
    try:
        print_info("Sending comparison request (this may take 60-90 seconds)...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/api/compare",
            json=payload,
            timeout=180  # 3 minutes for comparison
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Comparison generated in {elapsed:.2f} seconds")
            
            if "products" in data:
                print_success(f"Products compared: {len(data['products'])}")
            
            if "winner" in data:
                print_success(f"Winner: {data['winner']}")
            
            return True
        else:
            print_error(f"Comparison failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Request timed out. Comparison might be too complex.")
        return False
    except Exception as e:
        print_error(f"Comparison test error: {e}")
        return False

def check_environment() -> bool:
    """Check if environment is properly configured"""
    print_test("Environment Configuration")
    
    try:
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            masked_key = groq_key[:10] + "..." + groq_key[-4:]
            print_success(f"GROQ_API_KEY found: {masked_key}")
        else:
            print_error("GROQ_API_KEY not found in environment")
            return False
        
        db_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
        print_success(f"DATABASE_URL: {db_url}")
        
        return True
        
    except Exception as e:
        print_error(f"Environment check error: {e}")
        return False

def main():
    """Run all tests"""
    print_header("PRODUCT REVIEW ENGINE - BACKEND TEST SUITE")
    
    print_info("This script will test all major API endpoints")
    print_info(f"API Base URL: {API_BASE_URL}")
    print_info(f"Test User ID: {TEST_USER_ID}\n")
    
    results = {
        "Environment Check": check_environment(),
        "Health Endpoint": test_health_endpoint(),
        "Review Endpoint": test_review_endpoint(),
        "Chat Endpoint": test_chat_endpoint(),
        "History Summary": test_history_summary_endpoint(),
        # "Compare Endpoint": test_compare_endpoint(),  # Uncomment to test comparison
    }
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if result else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"{test_name.ljust(30)} {status}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed! Backend is working perfectly!{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠ Some tests failed. Please check the errors above.{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}\n")
        sys.exit(1)
