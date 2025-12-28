"""
Common Issues Checker
Checks for typical problems that cause search errors
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check environment variables"""
    print("🔧 Checking Environment Variables...")
    print()
    
    issues = []
    
    # Check GROQ_API_KEY
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        issues.append("❌ GROQ_API_KEY is not set")
        print("   ❌ GROQ_API_KEY: NOT FOUND")
    elif len(groq_key) < 20:
        issues.append("⚠️  GROQ_API_KEY looks too short (might be invalid)")
        print(f"   ⚠️  GROQ_API_KEY: Found but seems short ({len(groq_key)} chars)")
    else:
        masked = groq_key[:10] + "..." + groq_key[-4:]
        print(f"   ✅ GROQ_API_KEY: {masked}")
    
    print()
    return issues

def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking Dependencies...")
    print()
    
    issues = []
    required_packages = [
        'fastapi',
        'uvicorn',
        'groq',
        'requests',
        'beautifulsoup4',
        'pydantic',
        'sqlalchemy',
        'textblob',
        'vaderSentiment',
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            issues.append(f"❌ Missing package: {package}")
            print(f"   ❌ {package} - NOT INSTALLED")
    
    print()
    return issues

def check_files():
    """Check if critical files exist"""
    print("📁 Checking Critical Files...")
    print()
    
    issues = []
    required_files = [
        '.env',
        'api.py',
        'app_update.py',
        'database.py',
        'db_models.py',
        'requirements.txt',
    ]
    
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            print(f"   ✅ {filename}")
        else:
            issues.append(f"❌ Missing file: {filename}")
            print(f"   ❌ {filename} - NOT FOUND")
    
    print()
    return issues

def check_env_file():
    """Check .env file contents"""
    print("⚙️  Checking .env File...")
    print()
    
    issues = []
    
    if not Path('.env').exists():
        issues.append("❌ .env file does not exist")
        print("   ❌ .env file not found")
        print()
        return issues
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Check for GROQ_API_KEY line
        if 'GROQ_API_KEY=' not in content:
            issues.append("❌ GROQ_API_KEY not defined in .env")
            print("   ❌ GROQ_API_KEY line not found")
        else:
            # Extract the key value
            for line in content.split('\n'):
                if line.startswith('GROQ_API_KEY='):
                    key_value = line.split('=', 1)[1].strip()
                    if not key_value or key_value == 'your_actual_groq_api_key_here':
                        issues.append("❌ GROQ_API_KEY is not set to a real value")
                        print("   ❌ GROQ_API_KEY is empty or placeholder")
                    else:
                        print(f"   ✅ GROQ_API_KEY is set")
                    break
        
        # Check for DATABASE_URL
        if 'DATABASE_URL=' in content:
            print("   ✅ DATABASE_URL is defined")
        else:
            print("   ℹ️  DATABASE_URL not defined (will use default)")
        
    except Exception as e:
        issues.append(f"⚠️  Error reading .env file: {e}")
        print(f"   ⚠️  Error reading .env: {e}")
    
    print()
    return issues

def check_database():
    """Check database file"""
    print("🗄️  Checking Database...")
    print()
    
    issues = []
    db_path = Path('app.db')
    
    if db_path.exists():
        size = db_path.stat().st_size
        print(f"   ✅ app.db exists ({size:,} bytes)")
        if size < 1000:
            print(f"   ⚠️  Database is very small - might be empty")
    else:
        print("   ℹ️  app.db not found (will be created on first run)")
    
    print()
    return issues

def suggest_fixes(all_issues):
    """Suggest fixes for found issues"""
    if not all_issues:
        return
    
    print("="*70)
    print("🔧 SUGGESTED FIXES")
    print("="*70)
    print()
    
    for issue in all_issues:
        print(f"• {issue}")
    
    print()
    print("Common solutions:")
    print()
    
    if any("GROQ_API_KEY" in issue for issue in all_issues):
        print("For GROQ_API_KEY issues:")
        print("  1. Get a free API key from: https://console.groq.com/keys")
        print("  2. Open .env file")
        print("  3. Set: GROQ_API_KEY=your_actual_key_here")
        print("  4. Restart the backend")
        print()
    
    if any("Missing package" in issue for issue in all_issues):
        print("For missing packages:")
        print("  1. Activate virtual environment: venv\\Scripts\\activate")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print()
    
    if any("Missing file" in issue for issue in all_issues):
        print("For missing files:")
        print("  1. Make sure you're in the correct directory")
        print("  2. Check if files were accidentally deleted")
        print("  3. Restore from backup if available")
        print()

def main():
    print("="*70)
    print("COMMON ISSUES CHECKER")
    print("="*70)
    print()
    
    all_issues = []
    
    all_issues.extend(check_environment())
    all_issues.extend(check_dependencies())
    all_issues.extend(check_files())
    all_issues.extend(check_env_file())
    all_issues.extend(check_database())
    
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    
    if not all_issues:
        print("✅ No common issues found!")
        print()
        print("If you're still getting errors:")
        print("  1. Run: python diagnose_error.py")
        print("  2. Check the backend terminal for error logs")
        print("  3. Share the error message for specific help")
    else:
        print(f"⚠️  Found {len(all_issues)} potential issue(s)")
        suggest_fixes(all_issues)
    
    print()
    print("="*70)
    
    return 0 if not all_issues else 1

if __name__ == "__main__":
    # Load .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    sys.exit(main())
