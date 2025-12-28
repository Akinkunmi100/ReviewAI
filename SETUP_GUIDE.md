# 📖 Complete Setup Guide - Product Review Engine

> **Step-by-step instructions to get your Product Review Engine up and running**

This guide will walk you through every step needed to set up and run the Product Review Engine on your local machine.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Setup (Windows)](#quick-setup-windows)
3. [Detailed Manual Setup](#detailed-manual-setup)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [First Run](#first-run)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

| Software | Minimum Version | Recommended | Download Link |
|----------|----------------|-------------|---------------|
| Python | 3.9 | 3.10+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 18 | 20+ | [nodejs.org](https://nodejs.org/) |
| npm | 9.0 | 10+ | (comes with Node.js) |
| Git | Any | Latest | [git-scm.com](https://git-scm.com/) |

### API Keys

You'll need a **Groq API key** (free):
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and save it securely

### System Requirements

- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB minimum
- **Internet**: Required for web scraping and AI features

---

## Quick Setup (Windows)

The fastest way to get started on Windows:

### Step 1: Prepare

1. Download/clone the project
2. Have your Groq API key ready
3. Ensure Python and Node.js are installed

### Step 2: Run Quick Start

Double-click or run:
```bash
quick_start.bat
```

This script will:
- ✅ Create a Python virtual environment
- ✅ Install all Python dependencies
- ✅ Run a comprehensive health check
- ✅ Show you what's working and what needs attention

### Step 3: Configure Environment

1. Open the `.env` file in the root directory
2. Add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```
3. Save and close

### Step 4: Start Application

Double-click or run:
```bash
start_app.bat
```

This will:
- ✅ Start the backend server (port 8001)
- ✅ Install frontend dependencies (first time only)
- ✅ Start the frontend server (port 5173)
- ✅ Open your browser automatically

### Step 5: Create Account & Explore!

1. Register a new account at http://localhost:5173/register
2. Login and start analyzing products!

---

## Detailed Manual Setup

If you prefer manual control or are not on Windows:

### Part 1: Backend Setup

#### Step 1: Navigate to Project Directory

```bash
cd path/to/updated_project
```

#### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

#### Step 3: Activate Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your command prompt.

#### Step 4: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install approximately 20-25 packages including:
- FastAPI and Uvicorn
- SQLAlchemy
- Groq
- BeautifulSoup4
- TextBlob and VADER
- PassLib and python-jose
- And more...

**Note**: Installation may take 2-5 minutes depending on your internet speed.

#### Step 5: Configure Backend Environment

1. **Copy the example file:**
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. **Edit the .env file:**
   ```bash
   # Open with your preferred text editor
   # Windows: notepad .env
   # macOS: nano .env or open .env
   # Linux: nano .env or vim .env
   ```

3. **Set required variables:**
   ```env
   # REQUIRED: Get from console.groq.com
   GROQ_API_KEY=your_groq_api_key_here
   
   # REQUIRED: Already generated, keep secure
   JWT_SECRET=WnhOWqPaZr8zN0FtEGVtYw7lh7XxoC9n4VqLd8ieHv8
   
   # Optional: Defaults work for local development
   DATABASE_URL=sqlite:///./app.db
   JWT_ALGORITHM=HS256
   JWT_EXPIRES_MINUTES=10080
   LOG_LEVEL=INFO
   ```

4. **Save and close the file**

#### Step 6: Initialize Database

The database is automatically created on first run, but you can initialize it manually:

```bash
python -c "from database import init_db; init_db()"
```

You should see: `✓ Database initialized successfully`

#### Step 7: Test Backend

Start the backend server:

```bash
uvicorn api:app --reload --port 8001
```

You should see:
```
🚀 Product Review Engine API Starting...
✓ Database initialized successfully
✓ GROQ_API_KEY found
✓ Database: sqlite:///./app.db
✓ CORS enabled for development and production origins
✅ API ready! Listening for requests...
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Test the health endpoint:
- Open browser to: http://localhost:8001/health
- Should see: `{"status":"ok"}`
- Or visit: http://localhost:8001/docs for interactive API documentation

**Keep this terminal window open** - the backend server needs to stay running.

---

### Part 2: Frontend Setup

Open a **NEW terminal window** (keep the backend running in the first one).

#### Step 1: Navigate to Frontend Directory

```bash
cd path/to/updated_project/frontend
```

#### Step 2: Install Node Dependencies

```bash
npm install
```

This will install approximately 200+ packages including:
- React and React DOM
- React Router
- TypeScript
- Vite
- Lucide React
- And many development tools...

**Note**: Installation may take 3-10 minutes and create a large `node_modules` folder (~150MB).

#### Step 3: Configure Frontend Environment

1. **Copy the example file:**
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. **Edit frontend/.env:**
   ```env
   # Point to your backend server
   VITE_API_BASE_URL=http://localhost:8001
   ```

3. **Save and close**

#### Step 4: Start Frontend Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.4.0  ready in 347 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

**Keep this terminal window open** - the frontend server needs to stay running.

#### Step 5: Open Application

Open your browser and navigate to:
```
http://localhost:5173
```

You should see the Product Review Engine homepage!

---

## Configuration

### Backend Configuration Details

#### Environment Variables (.env)

```env
# ============================================================================
# REQUIRED
# ============================================================================

# Groq API Key - Get from https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# JWT Secret - Keep this secure and never commit to git
# Generate a new one: python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET=your_secure_random_string

# ============================================================================
# OPTIONAL (defaults work for local development)
# ============================================================================

# Database URL
# SQLite (default): sqlite:///./app.db
# PostgreSQL: postgresql://user:password@localhost/dbname
DATABASE_URL=sqlite:///./app.db

# JWT Configuration
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=10080  # 7 days

# CORS Origins (comma-separated)
FRONTEND_ORIGINS=http://localhost:5173,http://localhost:5174

# RapidAPI Key (optional, for additional data sources)
RAPIDAPI_KEY=your_rapidapi_key_here

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

#### Application Config (app_update.py)

Advanced users can modify the `AppConfig` class:

```python
@dataclass
class AppConfig:
    # AI Model Settings
    model_name: str = "llama-3.3-70b-versatile"
    max_tokens_review: int = 2500
    max_tokens_chat: int = 1000
    temperature_review: float = 0.3
    temperature_chat: float = 0.7
    
    # Web Scraping Settings
    max_search_results: int = 10
    max_scrape_results: int = 6
    request_timeout: int = 10
    request_delay: float = 0.5
    
    # Cache Settings
    cache_ttl_hours: int = 24
    cache_max_size: int = 100
```

### Frontend Configuration Details

#### Environment Variables (frontend/.env)

```env
# Backend API Base URL
VITE_API_BASE_URL=http://localhost:8001

# For production deployment:
# VITE_API_BASE_URL=https://api.yourdomain.com
```

#### Port Configuration

If ports 8001 or 5173 are already in use:

**Backend (change port):**
```bash
uvicorn api:app --reload --port 8001
```

Then update frontend/.env:
```env
VITE_API_BASE_URL=http://localhost:8001
```

**Frontend (Vite auto-selects next port):**
- Vite will automatically try 5174, 5175, etc.
- Check terminal output for the actual port
- Or manually specify:
  ```bash
  npm run dev -- --port 5174
  ```

---

## Verification

### Run Comprehensive Health Check

From the root directory:

```bash
python comprehensive_check.py
```

This will verify:
- ✅ Python version (3.9+)
- ✅ All required files exist
- ✅ Environment variables configured
- ✅ Python dependencies installed
- ✅ Database initialized
- ✅ Authentication system working
- ✅ API endpoints defined
- ✅ Frontend configured

### Manual Verification Checklist

#### Backend Checks

- [ ] Virtual environment activated (`(venv)` in prompt)
- [ ] Backend server running without errors
- [ ] http://localhost:8001/health returns `{"status":"ok"}`
- [ ] http://localhost:8001/docs loads API documentation
- [ ] `.env` file exists with GROQ_API_KEY
- [ ] `app.db` file created in root directory
- [ ] No error messages in terminal

#### Frontend Checks

- [ ] Node modules installed (frontend/node_modules exists)
- [ ] Frontend server running without errors
- [ ] http://localhost:5173 loads the homepage
- [ ] No red errors in browser console (F12)
- [ ] Frontend/.env exists with correct API URL
- [ ] Navigation works (click links)
- [ ] Theme toggle works (dark/light switch)

#### Integration Checks

- [ ] Can navigate to /register page
- [ ] Can navigate to /login page
- [ ] Homepage loads without errors
- [ ] No CORS errors in browser console
- [ ] Backend logs show no errors

---

## First Run

### Creating Your First Account

1. **Navigate to Registration**
   - Go to http://localhost:5173/register
   - Or click "Get Started" on homepage

2. **Register**
   - Enter a valid email address
   - Create a strong password (min 8 characters)
   - Click "Register"

3. **Login**
   - You'll be automatically logged in
   - Or manually login at /login

### Analyzing Your First Product

1. **Go to Reviews Page**
   - Click "Start Analyzing" or navigate to /reviews
   - You'll need to be logged in

2. **Enter Product Name**
   - Type a product name (e.g., "iPhone 15 Pro")
   - Click "Analyze Product"

3. **Wait for Analysis**
   - Takes 10-30 seconds depending on:
     - Web scraping speed
     - AI processing time
     - Your internet connection

4. **Review Results**
   - Comprehensive product analysis
   - Specs, pros/cons, pricing
   - Sentiment analysis
   - Purchase recommendations

### Using Chat Feature

1. **After analyzing a product**
   - Scroll to the chat panel on the right
   - Or click the chat icon

2. **Ask Questions**
   - "Is this good for gaming?"
   - "How does it compare to [competitor]?"
   - "What are the main issues?"

3. **Get AI Responses**
   - Context-aware answers
   - Based on actual product data
   - Considers your profile preferences

### Setting Up Profile

1. **Open Profile Panel**
   - Click on your profile icon/name
   - Or find in sidebar

2. **Configure Preferences**
   - Budget range (min/max)
   - Use cases (e.g., gaming, photography)
   - Preferred brands

3. **Save Profile**
   - Your preferences will be used for personalized recommendations

---

## Troubleshooting

### Issue: Backend won't start

**Symptom:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

---

**Symptom:**
```
GROQ_API_KEY environment variable is not set
```

**Solution:**
1. Check `.env` file exists in root directory
2. Verify GROQ_API_KEY is set: `GROQ_API_KEY=gsk_...`
3. Restart backend server

---

### Issue: Frontend won't start

**Symptom:**
```
Cannot find module 'react'
```

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json  # Delete and reinstall
npm install
npm run dev
```

---

**Symptom:**
```
Port 5173 is already in use
```

**Solution:**
- Vite will automatically use next available port (5174, 5175, etc.)
- Check terminal output for actual port
- Or manually specify: `npm run dev -- --port 5174`

---

### Issue: Frontend can't connect to backend

**Symptom:**
- Network errors in browser console
- "Failed to fetch" messages
- API calls failing

**Solution:**
1. Verify backend is running: http://localhost:8001/health
2. Check frontend/.env has correct API URL
3. Restart frontend after changing .env:
   ```bash
   # Stop frontend (Ctrl+C)
   npm run dev
   ```

---

### Issue: Database errors

**Symptom:**
```
no such table: users
```

**Solution:**
```bash
# Delete database and recreate
rm app.db
python -c "from database import init_db; init_db()"
```

---

### Issue: Authentication not working

**Symptom:**
- Can't login
- "Invalid token" errors
- Session expires immediately

**Solution:**
1. Check JWT_SECRET is set in .env
2. Clear browser localStorage:
   - F12 → Application → Local Storage
   - Right-click → Clear
3. Try logging in again

---

### Still Having Issues?

1. **Run the health check:**
   ```bash
   python comprehensive_check.py
   ```

2. **Check logs:**
   - Backend: `app.log` file
   - Frontend: Browser console (F12)

3. **Review documentation:**
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
   - [FAQ.md](FAQ.md)

4. **Fresh start:**
   ```bash
   # Backend
   rm -rf venv app.db
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

---

## Next Steps

### Explore Features

- ✅ **Product Analysis** - Analyze different products
- ✅ **Shortlist** - Save products for later
- ✅ **Comparison** - Compare multiple products
- ✅ **Chat** - Ask questions about products
- ✅ **History** - View past analyses
- ✅ **Profile** - Customize preferences

### Learn More

- **API Documentation**: http://localhost:8001/docs
- **Project Documentation**: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **Deployment Guide**: [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md)

### Customize

- Modify `AppConfig` in `app_update.py` for AI behavior
- Edit `frontend/src/styles.css` for UI styling
- Add new retailers in `app_update.py` Constants
- Configure caching and performance settings

### Deploy

Ready for production? Check out:
- [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md)
- Deploy backend to Render/Railway
- Deploy frontend to Vercel/Netlify

---

## Summary

You should now have:
- ✅ Backend running on http://localhost:8001
- ✅ Frontend running on http://localhost:5173
- ✅ Database initialized and ready
- ✅ Authentication working
- ✅ All features accessible

**Congratulations! You're ready to use the Product Review Engine! 🎉**

---

## Quick Reference

### Start Backend
```bash
venv\Scripts\activate
uvicorn api:app --reload --port 8001
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Health Check
```bash
python comprehensive_check.py
```

### Access Points
- Frontend: http://localhost:5173
 - Backend API: http://localhost:8001
 - API Docs: http://localhost:8001/docs
 - Health Check: http://localhost:8001/health

---

**Need help? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [FAQ.md](FAQ.md)**

**Happy analyzing! 🚀**
