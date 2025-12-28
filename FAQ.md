# ❓ Frequently Asked Questions (FAQ)

> **Quick answers to common questions about the Product Review Engine**

---

## 📚 Table of Contents

- [General Questions](#general-questions)
- [Setup & Installation](#setup--installation)
- [Features & Functionality](#features--functionality)
- [API & Integration](#api--integration)
- [Troubleshooting](#troubleshooting)
- [Security & Privacy](#security--privacy)
- [Performance & Optimization](#performance--optimization)
- [Deployment & Production](#deployment--production)
- [Development & Customization](#development--customization)

---

## General Questions

### What is the Product Review Engine?

The Product Review Engine is an AI-powered platform that helps users make informed purchasing decisions by analyzing products using advanced AI (Groq LLM), web scraping, and sentiment analysis. It provides comprehensive reviews, price comparisons from Nigerian retailers, and personalized recommendations.

### Is it free to use?

Yes! The application is open-source and free to use. The only cost is the Groq API usage, which has a generous free tier that's sufficient for personal use.

### What products can I analyze?

You can analyze virtually any consumer product - electronics, appliances, fashion, books, software, services, etc. The AI will adapt its analysis based on the product category.

### How accurate are the reviews?

The reviews are based on:
- Real-time web scraping from multiple sources
- AI analysis using advanced language models
- Sentiment analysis from aggregated opinions
- Actual pricing from Nigerian retailers

Accuracy depends on available web data and source quality.

### What makes this different from other review platforms?

- **🇳🇬 Nigerian Market Focus**: Direct pricing from local retailers (Jumia, Konga, Slot, Pointek)
- **🤖 AI-Powered**: Uses advanced LLM for intelligent analysis
- **💬 Interactive Chat**: Ask questions about products
- **🔐 Personalized**: Considers your budget and preferences
- **🆓 Free & Open Source**: No subscriptions or hidden fees

---

## Setup & Installation

### Do I need programming knowledge to set it up?

Basic familiarity with command line is helpful, but we provide:
- One-click setup scripts for Windows (`quick_start.bat`)
- Comprehensive step-by-step guides
- Automated health checks
- Detailed troubleshooting documentation

### What are the system requirements?

**Minimum:**
- Python 3.9+
- Node.js 18+
- 4GB RAM
- 500MB disk space
- Internet connection

**Recommended:**
- Python 3.10+
- Node.js 20+
- 8GB RAM
- SSD storage
- Fast internet

### How long does setup take?

- **Quick Setup (Windows)**: 5-10 minutes using `quick_start.bat`
- **Manual Setup**: 15-20 minutes following the guide
- First-time npm install takes the longest (3-10 minutes)

### Do I need to pay for anything?

**Free:**
- Application (open source)
- Groq API (generous free tier)
- SQLite database
- All features

**Optional (paid):**
- RapidAPI key for additional data sources
- PostgreSQL database for production
- Hosting services (Render, Vercel, etc.)

### Can I run this on Mac/Linux?

Yes! The application works on:
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)

The batch files (`.bat`) are Windows-only, but you can follow the manual setup instructions for other platforms.

---

## Features & Functionality

### What information does the review include?

Each review provides:
- 📊 **Specifications**: Key product specs
- ✅ **Pros & Cons**: Advantages and disadvantages
- 💰 **Pricing**: Nigerian market prices (Jumia, Konga, Slot, Pointek)
- 😊 **Sentiment Analysis**: Overall user sentiment
- ⚠️ **Red Flags**: Potential issues and concerns
- ⏰ **Purchase Timing**: Best time to buy
- 🏷️ **Best For**: Ideal use cases
- 🔄 **Alternatives**: Similar product suggestions
- 📚 **Sources**: Links to source materials

### How does product comparison work?

You can compare up to 4 products side-by-side:
1. Analyze products individually
2. Add them to your shortlist
3. Select products to compare
4. View detailed comparison table
5. See pros/cons, pricing, ratings side-by-side

### What can I ask the chat assistant?

The AI chat can answer:
- "Is this good for [specific use case]?"
- "How does it compare to [competitor]?"
- "What are the main issues with this product?"
- "Is it worth the price?"
- "What's better: this or [alternative]?"
- "Will this work for [my needs]?"

The chat is grounded in the actual product review data.

### Can I save products for later?

Yes! Features include:
- **Shortlist**: Save favorite products
- **History**: View all analyzed products
- **Chat History**: Resume conversations
- **Profile**: Save your preferences

All data is tied to your account and persists across sessions.

### How often is pricing data updated?

Pricing data is:
- **Web Scraped**: Updated on each analysis
- **Cached**: Stored for 24 hours
- **Real-time**: Reflects current retailer listings

For the most current prices, re-analyze the product.

### Does it support international products?

Yes, but with limitations:
- Works for any product globally
- **Pricing** is optimized for Nigerian retailers
- International prices may not be as comprehensive
- Web scraping works for global sources

---

## API & Integration

### Is there an API I can use?

Yes! The backend exposes a full REST API:
 - Interactive docs: http://localhost:8001/docs
- 16+ endpoints for all features
- JSON responses
- JWT authentication
- Well-documented

### How do I get an API key for Groq?

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Go to "API Keys" section
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)
6. Add to your `.env` file

### What are Groq API rate limits?

**Free Tier:**
- Generous limits for personal use
- Sufficient for testing and development
- May throttle with heavy usage

**Paid Tiers:**
- Higher rate limits
- Priority processing
- See [Groq pricing](https://groq.com/pricing) for details

### Can I use a different AI model?

Yes! Edit `app_update.py`:

```python
@dataclass
class AppConfig:
    model_name: str = "llama-3.3-70b-versatile"  # Change this
```

Available Groq models:
- `llama-3.3-70b-versatile` (default, best quality)
- `llama3-70b-8192`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

### How do I integrate with my own application?

1. **Use the API directly:**
   ```javascript
   fetch('http://localhost:8001/api/review', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ product_name: 'iPhone 15' })
   })
   ```

2. **Import Python modules:**
   ```python
   from app_update import EnhancedProductReviewService
   service = EnhancedProductReviewService(api_key, config)
   review = service.generate_review("iPhone 15")
   ```

3. **Customize frontend:**
   - Modify React components in `frontend/src/`
   - Use the API client in `frontend/src/api/`

---

## Troubleshooting

### Why am I getting "GROQ_API_KEY not set" error?

**Causes:**
- Missing `.env` file
- GROQ_API_KEY not in `.env`
- Virtual environment not activated
- Typo in environment variable name

**Solution:**
1. Check `.env` exists in root directory
2. Verify contents: `GROQ_API_KEY=gsk_...`
3. Ensure virtual environment is activated
4. Restart backend server

### Why is the frontend showing network errors?

**Causes:**
- Backend not running
- Wrong API URL in frontend/.env
- CORS issues
- Firewall blocking connection

**Solution:**
1. Verify backend is running: http://localhost:8001/health
2. Check frontend/.env: `VITE_API_BASE_URL=http://localhost:8001`
3. Restart frontend after changing .env
4. Check browser console for specific errors

### Why are product analyses slow?

**Causes:**
- Web scraping takes time
- Some sites block automated requests
- Groq API rate limiting
- Slow internet connection
- Many sources being scraped

**Normal timing:**
- Simple products: 10-20 seconds
- Complex products: 20-40 seconds
- First analysis (cache miss): Longer

**To speed up:**
- Reduce `max_search_results` in AppConfig
- Use caching (enabled by default)
- Upgrade internet connection
- Consider Groq paid tier for priority

### Authentication isn't working?

**Common issues:**
1. **JWT_SECRET not set** → Check `.env`
2. **Expired token** → Login again
3. **Browser cache** → Clear localStorage (F12 → Application)
4. **Wrong credentials** → Verify email/password
5. **Database issues** → Delete `app.db` and restart

### Database errors on startup?

**Solution:**
```bash
# Delete database and recreate
rm app.db  # or del app.db on Windows
python -c "from database import init_db; init_db()"
```

This creates a fresh database with all tables.

---

## Security & Privacy

### Is my data secure?

**Security Measures:**
- ✅ Passwords hashed with bcrypt
- ✅ JWT token authentication
- ✅ SQL injection protection (ORM)
- ✅ XSS prevention
- ✅ CORS protection
- ✅ Input validation and sanitization

### Where is my data stored?

**Local Installation:**
- Database: `app.db` file in root directory
- Logs: `app.log` file
- Cache: `.cache/` directory

**All data stays on your machine** unless you deploy to a server.

### Can others see my analyzed products?

No, all data is user-specific:
- Each user has their own history
- Shortlists are private
- Chat history is private
- Profiles are private

Only you (when logged in) can see your data.

### What data is sent to external services?

**Groq API:**
- Product names
- Generated prompts
- Chat messages

**Web Scraping:**
- HTTP requests to public websites
- User-agent headers (standard browser identification)

**Nothing else** is sent externally.

### How do I delete my data?

**All data:**
```bash
# Delete database
rm app.db
```

**Specific user:** (requires database access)
```python
from database import SessionLocal
from db_models import User

db = SessionLocal()
user = db.query(User).filter(User.external_id == "email@example.com").first()
if user:
    db.delete(user)  # Cascades to all related data
    db.commit()
```

### Can I use this offline?

**Limited functionality:**
- ✅ View saved reviews
- ✅ View chat history
- ✅ Browse shortlist
- ❌ New product analysis (requires Groq API and web scraping)
- ❌ New chat messages (requires Groq API)

AI features require internet connection.

---

## Performance & Optimization

### How can I make it faster?

**Backend:**
1. **Enable caching** (enabled by default)
2. **Reduce scraping sources:**
   ```python
   max_search_results: int = 5  # Down from 10
   max_scrape_results: int = 3  # Down from 6
   ```
3. **Use PostgreSQL** for better performance with many users
4. **Add Redis** for distributed caching

**Frontend:**
1. **Build for production:**
   ```bash
   cd frontend
   npm run build
   npm run preview
   ```
2. **Use production API** with caching
3. **Enable service workers** for offline caching

### How many users can it handle?

**SQLite (default):**
- 1-10 concurrent users
- Good for personal/small team use
- Handles hundreds of requests per minute

**PostgreSQL (recommended for production):**
- 100+ concurrent users
- Better for high traffic
- Requires separate database server

**Scaling tips:**
- Use production database (PostgreSQL)
- Add Redis for caching
- Deploy on proper hosting (not local machine)
- Use CDN for frontend assets
- Enable horizontal scaling

### How much does it cost to run?

**Free Tier:**
- $0/month for personal use
- Groq free tier is generous
- SQLite is free
- Self-hosted on your machine

**Production Hosting:**
- Backend: $7-25/month (Render, Railway)
- Frontend: $0 (Vercel, Netlify free tier)
- Database: $0-15/month (SQLite included or managed PostgreSQL)
- **Total: $7-40/month** depending on traffic

---

## Deployment & Production

### How do I deploy to production?

See [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md) for detailed guides.

**Quick options:**
1. **Render** (easiest, uses included render.yaml)
2. **Vercel** (frontend only, great free tier)
3. **Railway** (backend, simple setup)
4. **Heroku** (all-in-one, paid)

### Do I need to change anything for production?

**Essential changes:**
1. **Strong JWT_SECRET:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **PostgreSQL database:**
   ```env
   DATABASE_URL=postgresql://user:pass@host/db
   ```

3. **Frontend API URL:**
   ```env
   VITE_API_BASE_URL=https://api.yourdomain.com
   ```

4. **CORS origins:**
   ```python
   FRONTEND_ORIGINS = ["https://yourdomain.com"]
   ```

5. **HTTPS** (automatic with Render/Vercel)

### How do I monitor production?

**Logging:**
- Check `app.log` file
- Configure log level: `LOG_LEVEL=INFO`
- Use log aggregation (Papertrail, Loggly)

**Monitoring:**
- Uptime monitoring (UptimeRobot, Pingdom)
- Error tracking (Sentry)
- Analytics (Google Analytics, Plausible)

**Database:**
- Backup regularly
- Monitor size and performance
- Use managed database for automatic backups

---

## Development & Customization

### How do I add a new retailer?

Edit `app_update.py`:

```python
NIGERIAN_RETAILERS = {
    'new_retailer': {
        'name': 'New Retailer Name',
        'base_url': 'https://example.com',
        'search_url': 'https://example.com/search?q=',
        'logo': '🟢',
        'trust_score': 4,
        'trust_note': 'Description'
    }
}
```

### How do I customize the AI prompts?

Edit prompts in `app_update.py`:

```python
def _build_review_prompt(self, product_name: str, data_snippet: str) -> str:
    return f"""You are a product review expert...
    [Customize this prompt]
    """
```

### Can I change the UI design?

Yes! All frontend code is in `frontend/src/`:

**Styles:**
- Global: `styles.css`
- Component-specific: inline or component CSS

**Components:**
- Modify existing: `components/*.tsx`
- Create new: add to `components/`
- Update pages: `pages/*.tsx`

**Theme:**
- Colors in CSS variables
- Dark/light theme toggle in `App.tsx`

### How do I add a new feature?

**Backend:**
1. Add database model in `db_models.py`
2. Create API endpoint in `api.py`
3. Add business logic in `app_update.py`
4. Test with `test_backend.py`

**Frontend:**
1. Create component in `components/`
2. Add API call in `api/`
3. Create custom hook in `hooks/` (optional)
4. Add route in `App.tsx` (if new page)

### How do I contribute?

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature/my-feature`
7. Create Pull Request

See [README.md](README.md#contributing) for detailed guidelines.

---

## Still Have Questions?

### Where can I find more help?

📚 **Documentation:**
- [README.md](README.md) - Overview and quick start
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solving
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - All docs

🔧 **Tools:**
- `comprehensive_check.py` - Health check
- `quick_start.bat` - Automated setup
- `start_app.bat` - Start servers

📖 **API Documentation:**
- http://localhost:8001/docs (when running)

### How do I report a bug?

1. Run `python comprehensive_check.py`
2. Check logs (`app.log`, browser console)
3. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
4. Create GitHub issue with:
   - Description of problem
   - Steps to reproduce
   - Error messages
   - Environment details

### How do I request a feature?

Create a GitHub issue with:
- Clear description
- Use case/benefit
- Example or mockup (if UI)
- Willingness to contribute (optional)

---

<div align="center">

**Can't find your answer?**

Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for all available documentation

Or review the comprehensive [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide

</div>

---

**Last Updated:** December 13, 2025  
**Version:** 1.0 - Full Stack with Authentication
