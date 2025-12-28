"""
Comprehensive Project Health Check
This script verifies all components are working correctly
"""

import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{text.center(70)}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓{RESET} {text}")

def print_error(text):
    print(f"{RED}✗{RESET} {text}")

def print_warning(text):
    print(f"{YELLOW}⚠{RESET} {text}")

def print_info(text):
    print(f"{BLUE}ℹ{RESET} {text}")

issues_found = []
warnings_found = []
successes = []

def check_python_version():
    """Check if Python version is 3.9+"""
    print_header("CHECKING PYTHON VERSION")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python version {version_str} ✓")
        successes.append("Python version compatible")
    else:
        print_error(f"Python version {version_str} is too old. Need 3.9+")
        issues_found.append("Python version too old (need 3.9+)")

def check_required_files():
    """Check if all required files exist"""
    print_header("CHECKING REQUIRED FILES")
    
    required_files = [
        "api.py",
        "app_update.py",
        "auth.py",
        "database.py",
        "db_models.py",
        "requirements.txt",
        ".env",
        "frontend/package.json",
        "frontend/src/App.tsx",
        "frontend/src/main.tsx",
    ]
    
    for file in required_files:
        file_path = Path(file)
        if file_path.exists():
            print_success(f"Found: {file}")
            successes.append(f"File exists: {file}")
        else:
            print_error(f"Missing: {file}")
            issues_found.append(f"Missing file: {file}")

def check_environment_variables():
    """Check if required environment variables are set"""
    print_header("CHECKING ENVIRONMENT VARIABLES")
    
    # Load .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print_success("Loaded .env file")
        successes.append(".env file loaded")
    except ImportError:
        print_warning("python-dotenv not installed (optional)")
        warnings_found.append("python-dotenv not installed")
    except Exception as e:
        print_error(f"Error loading .env: {e}")
        issues_found.append(f"Error loading .env: {e}")
    
    # Check critical environment variables
    critical_vars = {
        "GROQ_API_KEY": "Required for AI features",
        "JWT_SECRET": "Required for authentication"
    }
    
    for var, description in critical_vars.items():
        value = os.getenv(var)
        if value and value != "your_groq_api_key_here" and value != "change_me_in_production":
            # Mask the key for security
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print_success(f"{var} is set ({masked})")
            successes.append(f"{var} configured")
        else:
            print_error(f"{var} not set properly - {description}")
            issues_found.append(f"{var} not configured")

def check_python_dependencies():
    """Check if all Python dependencies are installed"""
    print_header("CHECKING PYTHON DEPENDENCIES")
    
    required_packages = [
        ("fastapi", "Web framework"),
        ("uvicorn", "ASGI server"),
        ("sqlalchemy", "Database ORM"),
        ("groq", "AI API client"),
        ("requests", "HTTP library"),
        ("beautifulsoup4", "Web scraping"),
        ("textblob", "Sentiment analysis"),
        ("vaderSentiment", "Sentiment analysis"),
        ("passlib", "Password hashing"),
        ("python-jose", "JWT handling"),
        ("pydantic", "Data validation"),
    ]
    
    for package, description in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_success(f"{package} installed - {description}")
            successes.append(f"{package} installed")
        except ImportError:
            print_error(f"{package} not installed - {description}")
            issues_found.append(f"Missing dependency: {package}")

def check_database():
    """Check database configuration and models"""
    print_header("CHECKING DATABASE")
    
    try:
        from database import init_db, engine
        from db_models import Base
        from sqlalchemy import inspect
        
        # Try to initialize database
        init_db()
        print_success("Database initialized successfully")
        successes.append("Database initialized")
        
        # Check tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = ["users", "analyzed_products", "chat_sessions", 
                          "chat_messages", "user_profiles", "shortlisted_products"]
        
        for table in expected_tables:
            if table in tables:
                print_success(f"Table '{table}' exists")
                successes.append(f"Table {table} exists")
            else:
                print_warning(f"Table '{table}' not found (will be created on first run)")
                warnings_found.append(f"Table {table} not found")
        
    except Exception as e:
        print_error(f"Database check failed: {e}")
        issues_found.append(f"Database error: {e}")

def check_frontend():
    """Check frontend configuration"""
    print_header("CHECKING FRONTEND")
    
    # Check package.json
    package_json = Path("frontend/package.json")
    if package_json.exists():
        print_success("frontend/package.json exists")
        successes.append("Frontend package.json exists")
        
        try:
            import json
            with open(package_json) as f:
                data = json.load(f)
                
            # Check dependencies
            deps = data.get("dependencies", {})
            required_deps = ["react", "react-dom", "react-router-dom"]
            
            for dep in required_deps:
                if dep in deps:
                    print_success(f"Frontend dependency: {dep}")
                    successes.append(f"Frontend dep: {dep}")
                else:
                    print_error(f"Missing frontend dependency: {dep}")
                    issues_found.append(f"Missing frontend dep: {dep}")
        except Exception as e:
            print_error(f"Error reading package.json: {e}")
            issues_found.append(f"Error reading package.json: {e}")
    else:
        print_error("frontend/package.json not found")
        issues_found.append("frontend/package.json not found")
    
    # Check frontend .env
    frontend_env = Path("frontend/.env")
    if frontend_env.exists():
        print_success("frontend/.env exists")
        successes.append("Frontend .env exists")
        
        try:
            with open(frontend_env) as f:
                content = f.read()
                if "VITE_API_BASE_URL" in content:
                    print_success("VITE_API_BASE_URL configured")
                    successes.append("VITE_API_BASE_URL configured")
                else:
                    print_warning("VITE_API_BASE_URL not found in frontend/.env")
                    warnings_found.append("VITE_API_BASE_URL not configured")
        except Exception as e:
            print_error(f"Error reading frontend/.env: {e}")
            issues_found.append(f"Error reading frontend/.env: {e}")
    else:
        print_warning("frontend/.env not found (should be created from .env.example)")
        warnings_found.append("frontend/.env not found")
    
    # Check if node_modules exists
    node_modules = Path("frontend/node_modules")
    if node_modules.exists():
        print_success("frontend/node_modules exists (dependencies installed)")
        successes.append("Node modules installed")
    else:
        print_warning("frontend/node_modules not found - run 'npm install' in frontend/")
        warnings_found.append("Node modules not installed")

def check_api_endpoints():
    """Check if API endpoints are properly defined"""
    print_header("CHECKING API ENDPOINTS")
    
    try:
        from api import app
        routes = [route.path for route in app.routes]
        
        expected_endpoints = [
            "/api/auth/register",
            "/api/auth/login",
            "/api/auth/me",
            "/api/review",
            "/api/compare",
            "/api/chat",
            "/api/history/summary",
            "/api/history/chat-session",
            "/api/history/latest-session",
            "/api/history/review",
            "/api/shortlist",
            "/api/shortlist/add",
            "/api/shortlist/remove",
            "/api/profile",
            "/api/stats",
            "/health",
        ]
        
        for endpoint in expected_endpoints:
            if endpoint in routes:
                print_success(f"Endpoint defined: {endpoint}")
                successes.append(f"Endpoint: {endpoint}")
            else:
                print_error(f"Endpoint missing: {endpoint}")
                issues_found.append(f"Missing endpoint: {endpoint}")
                
    except Exception as e:
        print_error(f"Error checking API endpoints: {e}")
        issues_found.append(f"Error checking endpoints: {e}")

def check_auth_system():
    """Check authentication system"""
    print_header("CHECKING AUTHENTICATION SYSTEM")
    
    try:
        from auth import hash_password, verify_password, create_access_token, decode_token
        
        # Test password hashing
        test_password = "test123"
        hashed = hash_password(test_password)
        if verify_password(test_password, hashed):
            print_success("Password hashing/verification works")
            successes.append("Password system works")
        else:
            print_error("Password verification failed")
            issues_found.append("Password system broken")
        
        # Test JWT token creation
        token = create_access_token(user_id=1)
        if token:
            print_success("JWT token creation works")
            successes.append("JWT token creation works")
            
            # Test token decoding
            user_id = decode_token(token)
            if user_id == 1:
                print_success("JWT token decoding works")
                successes.append("JWT token decoding works")
            else:
                print_error("JWT token decoding failed")
                issues_found.append("JWT decoding broken")
        else:
            print_error("JWT token creation failed")
            issues_found.append("JWT creation broken")
            
    except Exception as e:
        print_error(f"Auth system check failed: {e}")
        issues_found.append(f"Auth system error: {e}")

def print_summary():
    """Print summary of all checks"""
    print_header("SUMMARY")
    
    print(f"\n{GREEN}✓ Successes: {len(successes)}{RESET}")
    print(f"{YELLOW}⚠ Warnings: {len(warnings_found)}{RESET}")
    print(f"{RED}✗ Issues: {len(issues_found)}{RESET}\n")
    
    if issues_found:
        print(f"{RED}CRITICAL ISSUES FOUND:{RESET}")
        for i, issue in enumerate(issues_found, 1):
            print(f"  {i}. {issue}")
        print()
    
    if warnings_found:
        print(f"{YELLOW}WARNINGS:{RESET}")
        for i, warning in enumerate(warnings_found, 1):
            print(f"  {i}. {warning}")
        print()
    
    if not issues_found and not warnings_found:
        print(f"{GREEN}{'='*70}{RESET}")
        print(f"{GREEN}🎉 ALL CHECKS PASSED! YOUR PROJECT IS READY TO RUN! 🎉{RESET}")
        print(f"{GREEN}{'='*70}{RESET}\n")
        print_next_steps()
    elif not issues_found:
        print(f"{YELLOW}{'='*70}{RESET}")
        print(f"{YELLOW}⚠ PROJECT IS FUNCTIONAL BUT HAS WARNINGS{RESET}")
        print(f"{YELLOW}{'='*70}{RESET}\n")
        print_next_steps()
    else:
        print(f"{RED}{'='*70}{RESET}")
        print(f"{RED}❌ CRITICAL ISSUES FOUND - PLEASE FIX BEFORE RUNNING{RESET}")
        print(f"{RED}{'='*70}{RESET}\n")
        print_fix_instructions()

def print_next_steps():
    """Print instructions for running the application"""
    print(f"{BLUE}NEXT STEPS:{RESET}\n")
    print("1. Start the backend:")
    print("   uvicorn api:app --reload --port 8001")
    print()
    print("2. In a new terminal, start the frontend:")
    print("   cd frontend")
    print("   npm run dev")
    print()
    print("3. Open your browser to:")
    print("   http://localhost:5173")
    print()

def print_fix_instructions():
    """Print instructions for fixing issues"""
    print(f"{BLUE}HOW TO FIX:{RESET}\n")
    
    if any("dependency" in issue.lower() for issue in issues_found):
        print("Install missing Python dependencies:")
        print("  pip install -r requirements.txt")
        print()
    
    if any("groq_api_key" in issue.lower() for issue in issues_found):
        print("Set GROQ_API_KEY in .env file:")
        print("  1. Get API key from https://console.groq.com/keys")
        print("  2. Add to .env: GROQ_API_KEY=your_key_here")
        print()
    
    if any("jwt_secret" in issue.lower() for issue in issues_found):
        print("Set JWT_SECRET in .env file:")
        print("  Generate a secure random string and add to .env")
        print()
    
    if any("frontend" in issue.lower() for issue in issues_found):
        print("Fix frontend issues:")
        print("  cd frontend")
        print("  npm install")
        print()

def main():
    """Run all checks"""
    print(f"{BLUE}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║     PRODUCT REVIEW ENGINE - COMPREHENSIVE HEALTH CHECK            ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    
    check_python_version()
    check_required_files()
    check_environment_variables()
    check_python_dependencies()
    check_database()
    check_auth_system()
    check_api_endpoints()
    check_frontend()
    
    print_summary()

if __name__ == "__main__":
    main()
