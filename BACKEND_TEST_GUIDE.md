# Backend Testing Checklist

## Quick Start Guide

### Step 1: Start the Backend
```bash
# Option A: Use the starter script (Windows)
start_backend.bat

# Option B: Manual start
# Activate virtual environment first:
venv\Scripts\activate

# Then start the server:
uvicorn api:app --reload --port 8001
```

### Step 2: Run the Test Suite
```bash
# In a NEW terminal window (keep the backend running)
# Activate virtual environment:
venv\Scripts\activate

# Run tests:
python test_backend.py
```

---

## What the Tests Check

### ✅ Test 1: Environment Configuration
- Verifies GROQ_API_KEY is set
- Checks DATABASE_URL configuration
- **Expected Result:** All environment variables found

### ✅ Test 2: Health Check Endpoint
- Tests: `GET /health`
- Verifies API is running and responding
- **Expected Result:** Status 200, health data returned

### ✅ Test 3: Product Review Generation
- Tests: `POST /api/review`
- Generates a full product review for "iPhone 14 Pro"
- Checks: specs, prices, pros/cons, sentiment
- **Expected Result:** Complete review with all sections
- **Duration:** 30-60 seconds

### ✅ Test 4: Chat Functionality
- Tests: `POST /api/chat`
- Sends a question about the product
- Verifies conversational AI response
- **Expected Result:** Relevant answer about battery life
- **Duration:** 10-20 seconds

### ✅ Test 5: History Summary
- Tests: `POST /api/history/summary`
- Retrieves user's analyzed products and chat sessions
- **Expected Result:** List of previous analyses
- **Duration:** < 5 seconds

### 🔄 Test 6: Product Comparison (Optional)
- Tests: `POST /api/compare`
- Compares multiple products side-by-side
- **Note:** Commented out by default (takes 60-90 seconds)
- Uncomment in `test_backend.py` to run

---

## Expected Output

### If Everything Works:
```
====================================================================
                PRODUCT REVIEW ENGINE - BACKEND TEST SUITE          
====================================================================

Testing: Environment Configuration
✓ GROQ_API_KEY found: gsk_BXBm60...sBUA
✓ DATABASE_URL: sqlite:///./app.db

Testing: Health Check Endpoint
✓ Health check passed: {'status': 'healthy', ...}

Testing: Product Review Endpoint
ℹ Sending review request (this may take 30-60 seconds)...
✓ Review generated in 45.23 seconds
✓ Product: iPhone 14 Pro
✓ Overall Score: 8.5/10
✓ Specs found: 12 items
✓ Nigerian prices found: 3 retailers
✓ Pros found: 8 items
✓ Cons found: 4 items

Testing: Chat Endpoint
ℹ Sending chat message...
✓ Chat response received in 12.34 seconds
✓ Response: The iPhone 14 Pro has excellent battery life...
✓ Session ID: 1

Testing: History Summary
✓ History summary retrieved
✓ Analyzed products: 1
✓ Chat sessions: 1

====================================================================
                         TEST SUMMARY                              
====================================================================
Environment Check              ✓ PASS
Health Endpoint                ✓ PASS
Review Endpoint                ✓ PASS
Chat Endpoint                  ✓ PASS
History Summary                ✓ PASS

Results: 5/5 tests passed

🎉 All tests passed! Backend is working perfectly!
```

---

## Troubleshooting

### Problem: "Cannot connect to the API"
**Solution:**
1. Make sure backend is running: `start_backend.bat` or `uvicorn api:app --reload --port 8001`
2. Check that port 8001 is not in use by another application
3. Verify you see "Uvicorn running on http://127.0.0.1:8001" in the terminal

### Problem: "GROQ_API_KEY not found"
**Solution:**
1. Check that `.env` file exists in the project root
2. Open `.env` and verify it contains: `GROQ_API_KEY=your_actual_key`
3. Get a free key from: https://console.groq.com/keys

### Problem: "ModuleNotFoundError"
**Solution:**
1. Activate virtual environment: `venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Retry the test

### Problem: Review test times out
**Solution:**
1. This is normal if web scraping is slow
2. Check your internet connection
3. The test has a 2-minute timeout - if it fails, the API might be stuck
4. Try restarting the backend server

### Problem: Review test fails with 500 error
**Solution:**
1. Check the backend terminal for detailed error logs
2. Common causes:
   - Invalid GROQ_API_KEY
   - Rate limit exceeded on Groq (wait a few minutes)
   - Web scraping blocked by target site
   - Missing dependencies

### Problem: Database errors
**Solution:**
1. Delete `app.db` file: `del app.db`
2. Restart the backend - database will be recreated automatically

---

## Manual Testing (Alternative)

If you prefer to test manually, you can use the FastAPI interactive docs:

1. Start the backend: `start_backend.bat`
2. Open browser to: `http://localhost:8001/docs`
3. You'll see the Swagger UI with all endpoints
4. Click "Try it out" on any endpoint to test it interactively

### Quick Manual Test:
1. Go to `http://localhost:8001/health` - should see `{"status":"healthy"}`
2. Use the `/docs` page to test `/api/review` with product name "iPhone 14"

---

## What Each Endpoint Does

### GET /health
- Simple health check
- Returns API status and database info

### POST /api/review
**Input:**
```json
{
  "product_name": "iPhone 14 Pro",
  "use_web": true,
  "user_id": "user123"
}
```
**Output:** Complete product review with specs, prices, pros/cons, sentiment, etc.

### POST /api/chat
**Input:**
```json
{
  "product_name": "iPhone 14 Pro",
  "message": "What's the battery life?",
  "conversation_history": [],
  "use_web": false,
  "user_id": "user123"
}
```
**Output:** AI-generated response with session tracking

### POST /api/compare
**Input:**
```json
{
  "products": ["iPhone 14 Pro", "Samsung Galaxy S23"]
}
```
**Output:** Side-by-side comparison with winner determination

### POST /api/history/summary
**Input:**
```json
{
  "user_id": "user123"
}
```
**Output:** User's analyzed products and chat sessions

---

## Database Schema

The backend uses SQLite with these tables:

1. **users** - User profiles
2. **analyzed_products** - Cached product reviews
3. **chat_sessions** - Chat conversation sessions
4. **chat_messages** - Individual chat messages

Database file: `app.db` (created automatically)

---

## Performance Expectations

- **Health Check:** < 1 second
- **Product Review:** 30-60 seconds (includes web scraping)
- **Chat Response:** 10-20 seconds
- **History Retrieval:** < 5 seconds
- **Product Comparison:** 60-90 seconds

---

## Next Steps After Testing

If all tests pass:
1. ✅ Backend is working perfectly!
2. You can now start the frontend: `cd frontend && npm run dev`
3. Or test individual endpoints at: `http://localhost:8001/docs`
4. Check the logs in the backend terminal for detailed information

If some tests fail:
1. Check the error messages in the test output
2. Review the backend terminal logs
3. Consult the troubleshooting section above
4. Check the detailed debug guides in the `docs/` folder
