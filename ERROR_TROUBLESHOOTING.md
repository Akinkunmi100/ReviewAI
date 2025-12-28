# 🔍 Product Search Error Troubleshooting Guide

## Quick Diagnosis (3 Steps)

### Step 1: Check for Common Issues
```bash
python check_issues.py
```
This will check:
- ✓ GROQ_API_KEY configuration
- ✓ Required dependencies installed
- ✓ Critical files present
- ✓ .env file properly configured

### Step 2: Diagnose the Specific Error
```bash
# Make sure backend is running first!
python diagnose_error.py
```
This will:
- Test a real product search
- Capture the exact error
- Show detailed error information

### Step 3: Check Backend Logs
Look at the terminal where you started the backend. You should see detailed error messages there.

---

## Common Errors & Solutions

### Error 1: "GROQ_API_KEY environment variable is not set"

**Symptoms:**
- Search fails immediately
- Error message mentions API key

**Solution:**
```bash
# 1. Check if .env file exists
dir .env

# 2. Open .env and verify it contains:
GROQ_API_KEY=gsk_your_actual_key_here

# 3. Get a free key from:
https://console.groq.com/keys

# 4. Restart the backend
```

---

### Error 2: "ModuleNotFoundError: No module named 'groq'"

**Symptoms:**
- Backend fails to start
- Missing import errors

**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Restart backend
start_backend.bat
```

---

### Error 3: Rate Limit Exceeded

**Symptoms:**
- "Rate limit exceeded" in error message
- 429 status code
- Works initially then stops

**Solution:**
```bash
# Wait 1-2 minutes, then try again
# Groq free tier has rate limits:
# - 30 requests per minute
# - 14,400 requests per day

# If needed, upgrade at: https://console.groq.com/settings/limits
```

---

### Error 4: Web Scraping Timeout

**Symptoms:**
- Request takes very long (>60 seconds)
- Times out during review generation
- "Timeout" error

**Solution:**
```bash
# Try with AI-only mode (no web scraping):
# In the frontend, disable "Use Web Search"

# Or test with a simpler product:
python diagnose_error.py
# (uses "iPhone 14" which usually works)
```

---

### Error 5: Database Errors

**Symptoms:**
- "SQLAlchemy" errors
- "Database locked" messages
- "No such table" errors

**Solution:**
```bash
# Stop the backend (Ctrl+C)

# Delete the database
del app.db

# Restart - database will be recreated
start_backend.bat
```

---

### Error 6: CORS Error (Frontend to Backend)

**Symptoms:**
- "CORS policy" error in browser console
- "Access-Control-Allow-Origin" errors
- Network request blocked

**Solution:**
```bash
# Check backend is running on port 8001
# Frontend expects: http://localhost:8001

# Verify in api.py:
FRONTEND_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
]

# Restart backend after changes
```

---

### Error 7: Connection Refused

**Symptoms:**
- "Cannot connect to backend"
- "Connection refused"
- "ECONNREFUSED"

**Solution:**
```bash
# Backend is not running!
# Start it:
start_backend.bat

# Verify it's running:
python quick_check.py
```

---

### Error 8: Invalid JSON Response

**Symptoms:**
- "JSON parse error"
- "Unexpected token"
- Response is HTML instead of JSON

**Solution:**
```bash
# This usually means backend crashed
# Check backend terminal for error details

# Common causes:
# 1. Groq API returned an error
# 2. Web scraping failed
# 3. Python exception occurred

# Look for Python traceback in backend terminal
```

---

## Step-by-Step Debugging Process

### 1. Verify Backend is Running
```bash
# Start backend
start_backend.bat

# You should see:
# ✓ Database initialized successfully
# ✓ GROQ_API_KEY found
# ✅ API ready!
```

### 2. Run Quick Health Check
```bash
python quick_check.py

# Expected:
# ✅ Backend is UP and responding!
```

### 3. Run Common Issues Check
```bash
python check_issues.py

# This checks:
# - Environment variables
# - Dependencies
# - Files
# - Database
```

### 4. Test Actual Search
```bash
python diagnose_error.py

# This performs a real product search
# Shows exactly where it fails
```

### 5. Check Backend Logs
```
Look at the backend terminal window
Search for:
- "ERROR" messages
- Python tracebacks
- Exception details
```

---

## Reading Error Logs

### Example Backend Log - Success:
```
INFO: 127.0.0.1:52847 - "POST /api/review HTTP/1.1" 200 OK
INFO: Generating review for: iPhone 14
INFO: Using web search mode
INFO: Found 8 search results
INFO: Scraped 5 product pages
INFO: Generated review successfully
```

### Example Backend Log - Error:
```
ERROR: Exception in ASGI application
Traceback (most recent call last):
  File "app_update.py", line 543, in generate_review
    review = self._generate_from_groq(...)
  File "app_update.py", line 678, in _generate_from_groq
    raise ProductReviewError(f"Groq API error: {str(e)}")
ProductReviewError: Groq API error: Rate limit exceeded
```

**Key parts to look for:**
1. **Traceback** - Shows where error occurred
2. **Error type** - ProductReviewError, ValueError, etc.
3. **Error message** - Specific reason for failure

---

## Frontend Error Messages

### "Failed to fetch"
- **Cause:** Backend not running or wrong URL
 - **Fix:** Start backend, check it's on port 8001

### "Network Error"
- **Cause:** Connection issues
- **Fix:** Check backend is accessible

### "Request timeout"
- **Cause:** Review taking too long
- **Fix:** Normal for first request, wait or disable web search

### "Internal Server Error" (500)
- **Cause:** Backend crashed or exception
- **Fix:** Check backend logs for traceback

---

## Testing Without Frontend

You can test the backend directly using the FastAPI docs:

1. Start backend: `start_backend.bat`
2. Open browser: `http://localhost:8001/docs`
3. Try the `/api/review` endpoint
4. Click "Try it out"
5. Enter product name: "iPhone 14"
6. Click "Execute"

This shows you the raw API response and any errors.

---

## Getting Help

### Information to Provide:

1. **Error message** from diagnose_error.py
2. **Backend logs** from the terminal
3. **Browser console errors** (F12 → Console tab)
4. **What you searched for** (product name)
5. **When it fails** (immediately, after delay, etc.)

### Run These Commands:
```bash
# Get diagnostic info
python check_issues.py > issues.txt
python diagnose_error.py > diagnosis.txt

# Share the .txt files
```

---

## Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| Backend won't start | Check .env has GROQ_API_KEY |
| "Module not found" | Run `pip install -r requirements.txt` |
| Rate limit error | Wait 2 minutes, try again |
| Search times out | Try simpler product name |
| Database error | Delete app.db, restart backend |
| Can't connect | Backend not running, run start_backend.bat |

---

## Prevention Tips

1. **Always activate venv first:**
   ```bash
   venv\Scripts\activate
   ```

2. **Keep backend running:**
   - Don't close the terminal
   - If it crashes, check logs before restarting

3. **Monitor rate limits:**
   - Don't test too rapidly
   - Wait between searches

4. **Use simple product names:**
   - "iPhone 14" ✅
   - "Apple iPhone 14 Pro Max 256GB Space Black Unlocked" ❌

5. **Check logs regularly:**
   - Backend terminal shows issues early
   - Don't ignore warnings

---

## Next Steps

After fixing errors:
1. ✅ Run `python check_issues.py` - should show no issues
2. ✅ Run `python quick_check.py` - should show backend UP
3. ✅ Run `python diagnose_error.py` - should complete successfully
4. ✅ Try search in frontend - should work!
