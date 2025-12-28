# 🚨 SEARCH ERROR - WHAT TO DO NOW

## Run These 2 Commands (In Order):

### 1. Check for Common Problems
```bash
python check_issues.py
```
**What it does:** Checks your setup for typical issues  
**Takes:** 5 seconds  
**Fixes:** GROQ_API_KEY, missing packages, file problems

### 2. Diagnose the Specific Error  
```bash
# Make sure backend is running first!
start_backend.bat

# Then in a NEW terminal:
python diagnose_error.py
```
**What it does:** Tests actual product search  
**Takes:** 30-60 seconds  
**Shows:** Exact error message and location

---

## Most Common Issue (90% of cases)

### ❌ GROQ_API_KEY Problem

**Check this first:**
```bash
# Open .env file and look for:
GROQ_API_KEY=your_groq_api_key_here
```

**Is it there?** ✅ Continue to Step 2  
**Missing or wrong?** ❌ Fix it:
1. Get free key: https://console.groq.com/keys
2. Add to .env file
3. Restart backend

---

## Top 5 Errors & Quick Fixes

| Error | Fix |
|-------|-----|
| "GROQ_API_KEY not set" | Add key to .env, restart backend |
| "Module not found" | Run: `pip install -r requirements.txt` |
| "Rate limit exceeded" | Wait 2 minutes, try again |
| "Cannot connect" | Backend not running, run: `start_backend.bat` |
| "Timeout" | Normal for first search, or try simpler product name |

---

## Is Backend Running?

Check the backend terminal window. You should see:
```
✅ API ready! Listening for requests...
INFO:     Uvicorn running on http://127.0.0.1:8001
```

**Don't see this?** Run: `start_backend.bat`

---

## Error in Frontend When You Search?

### Quick Test:
```bash
# 1. Start backend
start_backend.bat

# 2. In NEW terminal, run quick check
python quick_check.py
```

**If quick_check.py passes** ✅ → Backend works, might be frontend issue  
**If quick_check.py fails** ❌ → Backend has problem, check logs

---

## Need More Help?

1. Run both diagnostic scripts (above)
2. Copy the error messages
3. Check backend terminal for detailed logs
4. Look in **ERROR_TROUBLESHOOTING.md** for your specific error

---

## Emergency Reset

If nothing works:
```bash
# Stop backend (Ctrl+C)

# Delete database
del app.db

# Reinstall packages
pip install -r requirements.txt

# Restart
start_backend.bat
```

---

## Files Created to Help You:

- ✅ `check_issues.py` - Checks common problems
- ✅ `diagnose_error.py` - Tests actual search
- ✅ `ERROR_TROUBLESHOOTING.md` - Detailed error guide
- ✅ `start_backend.bat` - Easy backend starter
- ✅ `quick_check.py` - Fast health check

**Start here:** Run `check_issues.py` first!
