# 🔧 QUICK TROUBLESHOOTING GUIDE

## Common Issues and Solutions

---

### ❌ **Issue: "GROQ_API_KEY environment variable is not set"**

**Solution:**
1. Open `.env` file in the root directory
2. Verify you have: `GROQ_API_KEY=gsk_...`
3. If missing, get a free API key from: https://console.groq.com/keys
4. Add it to `.env`: `GROQ_API_KEY=your_key_here`
5. Restart the backend server

---

### ❌ **Issue: "ModuleNotFoundError: No module named 'fastapi'"**

**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### ❌ **Issue: Frontend shows "Network Error" or "Failed to fetch"**

**Possible Causes & Solutions:**

**1. Backend not running**
 - Check if backend is running on http://localhost:8001
 - Visit http://localhost:8001/health in your browser
- Should see: `{"status":"ok"}`

**2. Wrong API URL**
- Open `frontend/.env`
- Should have: `VITE_API_BASE_URL=http://localhost:8001`
- Restart frontend after changing: `npm run dev`

**3. CORS Issue**
- Check backend logs for CORS errors
- Verify `api.py` has your frontend origin in CORS settings
- Default should include `http://localhost:5173`

---

### ❌ **Issue: "Port 8001 is already in use"**

**Solution:**
```bash
# Option 1: Kill the process using port 8001
netstat -ano | findstr :8001
taskkill /PID <process_id> /F

# Option 2: Use a different port
uvicorn api:app --reload --port 8001

# Then update frontend/.env:
VITE_API_BASE_URL=http://localhost:8001
```

---

### ❌ **Issue: "Port 5173 is already in use"**

**Solution:**
- Vite will automatically use the next available port (5174, 5175, etc.)
- Check the terminal output for the actual port number
- Or manually specify a port:
```bash
npm run dev -- --port 5174
```

---

### ❌ **Issue: Database errors on startup**

**Solution:**
```bash
# Delete the database and let it recreate
del app.db

# Restart backend - it will create a fresh database
uvicorn api:app --reload
```

---

### ❌ **Issue: "Invalid token" or "User not found" errors**

**Solution:**
1. Clear browser localStorage:
   - Open browser DevTools (F12)
   - Go to Application > Local Storage
   - Clear all data
   - Refresh page

2. Or logout and login again

---

### ❌ **Issue: Frontend not displaying properly / white screen**

**Solutions:**

**1. Check browser console**
- Press F12 to open DevTools
- Look for errors in Console tab
- Most errors will indicate what's wrong

**2. Rebuild frontend**
```bash
cd frontend

# Clear cache and reinstall
rmdir /s /q node_modules
del package-lock.json
npm install

# Start dev server
npm run dev
```

---

### ❌ **Issue: "Cannot find module 'XXX'" in Python**

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

---

### ❌ **Issue: Slow product analysis or timeouts**

**Possible Causes:**
1. **Web scraping timeouts** - Some sites block automated requests
2. **Groq API rate limits** - Free tier has limits
3. **Network issues**

**Solutions:**
- Try a different product name
- Wait a few minutes if rate limited
- Check your internet connection
- Consider upgrading Groq plan for higher limits

---

### ❌ **Issue: Authentication not working**

**Check:**
1. JWT_SECRET is set in `.env`
2. Password is at least 8 characters
3. Email format is valid
4. Backend logs for specific error messages

**Solution:**
```bash
# Test auth manually:
python -c "from auth import hash_password, verify_password; 
pwd='test123'; 
h=hash_password(pwd); 
print('Hash:', h); 
print('Verify:', verify_password(pwd, h))"
```

---

### ❌ **Issue: Frontend build fails**

**Solution:**
```bash
cd frontend

# Clear cache
npm cache clean --force

# Reinstall
rmdir /s /q node_modules
del package-lock.json
npm install

# Try building
npm run build
```

---

### ❌ **Issue: Can't run .bat files**

**Solutions:**

**Option 1: Run manually**
```bash
# For quick_start.bat:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python comprehensive_check.py
```

**Option 2: Check permissions**
- Right-click the .bat file
- Click "Run as administrator"

**Option 3: Use PowerShell**
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🔍 **Diagnostic Commands**

### Check Python Version
```bash
python --version
# Should be 3.9 or higher
```

### Check if Backend is Running
```bash
curl http://localhost:8001/health
# Or visit in browser
```

### Check Environment Variables
```bash
# Windows CMD
echo %GROQ_API_KEY%

# PowerShell
$env:GROQ_API_KEY

# In Python
python -c "import os; print(os.getenv('GROQ_API_KEY'))"
```

### Check Database Tables
```bash
python -c "from database import engine; from sqlalchemy import inspect; 
inspector = inspect(engine); 
print('Tables:', inspector.get_table_names())"
```

### Test API Endpoint
```bash
# Using curl
curl -X POST http://localhost:8001/api/review ^
  -H "Content-Type: application/json" ^
  -d "{\"product_name\":\"iPhone 15\",\"use_web\":true}"

# Or use browser's Network tab to inspect requests
```

---

## 📝 **Log Files to Check**

1. **Backend Logs**
   - File: `app.log`
   - Contains: API errors, database issues, authentication problems

2. **Frontend Console**
   - Press F12 in browser
   - Check Console tab for JavaScript errors
   - Check Network tab for failed API requests

3. **Terminal Output**
   - Backend terminal shows FastAPI logs
   - Frontend terminal shows Vite logs and build errors

---

## 🆘 **Still Having Issues?**

1. **Run the comprehensive health check:**
   ```bash
   python comprehensive_check.py
   ```

2. **Check all logs:**
   - Backend: `app.log`
   - Frontend: Browser console (F12)
   - Terminal output from both servers

3. **Verify environment:**
   - `.env` file exists with proper values
   - `frontend/.env` has correct API URL
   - Virtual environment is activated

4. **Try a fresh start:**
   ```bash
   # Delete database
   del app.db
   
   # Reinstall Python dependencies
   pip install -r requirements.txt --force-reinstall
   
   # Reinstall Node dependencies
   cd frontend
   rmdir /s /q node_modules
   npm install
   ```

---

## ✅ **Prevention Tips**

1. **Always activate virtual environment** before running Python commands
2. **Keep dependencies updated** (but test after updates)
3. **Don't commit `.env` files** to version control
4. **Backup database** before major changes
5. **Clear cache** when things act strange
6. **Check logs first** when debugging

---

## 🔗 **Useful Links**

- **Groq API Docs:** https://console.groq.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Vite Docs:** https://vitejs.dev/
- **SQLAlchemy Docs:** https://www.sqlalchemy.org/

---

**Last Updated:** December 13, 2025
