# 🛍️ Product Review Engine

> **AI-Powered Product Analysis Platform with Nigerian Market Integration**

A comprehensive full-stack application that leverages artificial intelligence to provide in-depth product reviews, comparisons, and personalized recommendations. Built with FastAPI, React, and Groq AI, with special focus on the Nigerian e-commerce market.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Detailed Setup](#-detailed-setup)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Documentation](#-documentation)
- [License](#-license)

---

## 🌟 Overview

The **Product Review Engine** is an intelligent platform that helps users make informed purchasing decisions by:

- **Analyzing products** using advanced AI (Groq LLM)
- **Scraping real-time data** from web sources
- **Providing Nigerian market pricing** from Jumia, Konga, Slot, and Pointek
- **Performing sentiment analysis** on reviews using TextBlob and VADER
- **Offering personalized recommendations** based on user preferences
- **Enabling product comparisons** side-by-side
- **Supporting interactive chat** about products

### What Makes It Special?

🇳🇬 **Nigerian Market Focus**: Direct integration with local e-commerce platforms for accurate pricing

🤖 **AI-Powered**: Uses Groq's fast LLM inference for intelligent analysis

🔐 **Secure Authentication**: JWT-based auth with password hashing

💾 **Persistent Storage**: Remembers your searches, chats, and preferences

🎨 **Modern UI/UX**: Clean, responsive design with dark/light themes

---

## ✨ Key Features

### 🔍 Product Analysis
- **Comprehensive Reviews**: AI-generated analysis including specs, pros/cons, sentiment
- **Real-time Web Scraping**: Fetches current information from multiple sources
- **Price Comparison**: Aggregates prices from Nigerian retailers
- **Red Flags Detection**: Identifies potential issues and concerns
- **Purchase Timing**: Recommends best time to buy
- **Alternative Suggestions**: Proposes similar products

### 👤 User Management
- **Secure Authentication**: Email/password registration and login
- **User Profiles**: Save preferences, budget, and use cases
- **Product History**: Track all analyzed products
- **Shortlist/Wishlist**: Save favorite products for later
- **Chat History**: Persistent conversation memory

### 💬 AI Chat Assistant
- **Context-Aware**: Grounded in actual product reviews
- **Personalized**: Considers your budget and preferences
- **Multi-turn Conversations**: Natural dialogue flow
- **Session Persistence**: Resume conversations anytime

### 📊 Product Comparison
- **Side-by-Side Analysis**: Compare up to 4 products
- **Visual Comparisons**: Easy-to-read comparison tables
- **Detailed Metrics**: Specs, pricing, ratings, pros/cons

### 🎯 Smart Features
- **Sentiment Analysis**: Aggregates opinions from multiple sources
- **Trust Scoring**: Rates retailer reliability
- **Price Tracking**: Historical pricing data
- **Statistics Dashboard**: Platform usage insights

---

## 🛠️ Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Groq](https://groq.com/)** - Fast LLM inference for AI features
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[SQLite](https://www.sqlite.org/)** - Lightweight database (default)
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** - Web scraping
- **[TextBlob](https://textblob.readthedocs.io/)** - Natural language processing
- **[VADER](https://github.com/cjhutto/vaderSentiment)** - Sentiment analysis
- **[PassLib](https://passlib.readthedocs.io/)** - Password hashing
- **[python-jose](https://github.com/mpdavis/python-jose)** - JWT tokens

### Frontend
- **[React 18](https://reactjs.org/)** - UI library
- **[TypeScript](https://www.typescriptlang.org/)** - Type-safe JavaScript
- **[Vite](https://vitejs.dev/)** - Fast build tool
- **[React Router](https://reactrouter.com/)** - Navigation
- **[Lucide React](https://lucide.dev/)** - Icon library

### Development Tools
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation
- **[ESLint](https://eslint.org/)** - JavaScript linting

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- Groq API key ([Get one free](https://console.groq.com/keys))

### 🎯 One-Click Start (Windows)

The easiest way to get started:

1. **Run Setup & Health Check**
   ```bash
   # Double-click this file or run:
   quick_start.bat
   ```
   This will:
   - Create virtual environment
   - Install Python dependencies
   - Run comprehensive health check
   - Show you what's working and what needs attention

2. **Start the Application**
   ```bash
   # Double-click this file or run:
   start_app.bat
   ```
   This will:
   - Start backend server (port 8001)
   - Start frontend server (port 5173)
   - Open your browser automatically

3. **Access the App**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

That's it! You're ready to go! 🎉

---

## 📦 Detailed Setup

### Step 1: Clone and Navigate

```bash
cd updated_project
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2.3 Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys:
# - GROQ_API_KEY (required)
# - JWT_SECRET (auto-generated, keep secure)
```

**Required Environment Variables:**
```env
GROQ_API_KEY=your_groq_api_key_here
JWT_SECRET=your_secure_random_string
DATABASE_URL=sqlite:///./app.db
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=10080
```

#### 2.4 Initialize Database

```bash
# Database is automatically created on first run
# You can also run:
python -c "from database import init_db; init_db()"
```

#### 2.5 Start Backend Server

```bash
uvicorn api:app --reload --port 8001
```

You should see:
```
🚀 Product Review Engine API Starting...
✓ Database initialized successfully
✓ GROQ_API_KEY found
✅ API ready! Listening for requests...
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend

```bash
cd frontend
```

#### 3.2 Install Dependencies

```bash
npm install
```

#### 3.3 Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Default configuration (for local development):
VITE_API_BASE_URL=http://localhost:8001
```

#### 3.4 Start Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.4.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Step 4: Verify Installation

Run the comprehensive health check:

```bash
# From the root directory
python comprehensive_check.py
```

This will verify:
- ✅ Python version
- ✅ Required files
- ✅ Environment variables
- ✅ Dependencies
- ✅ Database
- ✅ Authentication system
- ✅ API endpoints
- ✅ Frontend configuration

---

## 📁 Project Structure

```
updated_project/
│
├── 📚 Documentation
│   ├── README.md                      # This file
│   ├── PROJECT_STATUS_REPORT.md       # Comprehensive status
│   ├── TROUBLESHOOTING.md             # Problem solving
│   ├── DOCUMENTATION_INDEX.md         # Doc navigation
│   ├── SETUP_GUIDE.md                 # Detailed setup
│   └── [Other guides...]
│
├── 🐍 Backend (Python/FastAPI)
│   ├── api.py                         # FastAPI app & endpoints
│   ├── app_update.py                  # Core business logic
│   ├── auth.py                        # JWT authentication
│   ├── database.py                    # Database config
│   ├── db_models.py                   # SQLAlchemy models
│   ├── requirements.txt               # Python dependencies
│   └── app.log                        # Application logs
│
├── ⚛️ Frontend (React/TypeScript)
│   ├── src/
│   │   ├── api/                       # API client
│   │   │   ├── client.ts              # HTTP client
│   │   │   ├── types.ts               # Type definitions
│   │   │   ├── history.ts             # History API
│   │   │   └── shortlist.ts           # Shortlist API
│   │   ├── auth/                      # Authentication
│   │   │   ├── AuthContext.tsx        # Auth state
│   │   │   ├── token.ts               # Token management
│   │   │   └── RequireAuth.tsx        # Route protection
│   │   ├── components/                # React components
│   │   │   ├── Header.tsx             # Navigation
│   │   │   ├── Footer.tsx             # Footer
│   │   │   ├── ProfilePanel.tsx       # User profile
│   │   │   ├── ChatPanel.tsx          # Chat interface
│   │   │   └── [30+ components...]
│   │   ├── hooks/                     # Custom hooks
│   │   │   ├── useReview.ts           # Review logic
│   │   │   └── useChat.ts             # Chat logic
│   │   ├── pages/                     # Page components
│   │   │   ├── HomePage.tsx           # Landing page
│   │   │   ├── ReviewPage.tsx         # Main app page
│   │   │   ├── LoginPage.tsx          # Login
│   │   │   ├── RegisterPage.tsx       # Registration
│   │   │   ├── AboutPage.tsx          # About
│   │   │   ├── FeaturesPage.tsx       # Features
│   │   │   └── ContactPage.tsx        # Contact
│   │   ├── App.tsx                    # Main app component
│   │   ├── main.tsx                   # Entry point
│   │   └── styles.css                 # Global styles
│   ├── package.json                   # Dependencies
│   ├── tsconfig.json                  # TypeScript config
│   ├── vite.config.ts                 # Vite config
│   └── .env                           # Frontend config
│
├── 🔧 Configuration
│   ├── .env                           # Backend config
│   ├── .env.example                   # Config template
│   ├── .gitignore                     # Git ignore rules
│   └── render.yaml                    # Deployment config
│
├── 🗄️ Database
│   └── app.db                         # SQLite database
│
├── 🚀 Scripts
│   ├── comprehensive_check.py         # Health check
│   ├── quick_start.bat                # Setup script
│   ├── start_app.bat                  # Start servers
│   ├── test_backend.py                # Backend tests
│   └── [Other scripts...]
│
└── 📦 Cache & Logs
    ├── .cache/                        # Web scraping cache
    ├── app.log                        # Application logs
    └── __pycache__/                   # Python cache
```

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/register          # Create new account
POST   /api/auth/login             # Login and get JWT token
GET    /api/auth/me                # Get current user info
```

### Product Analysis
```
POST   /api/review                 # Generate product review
POST   /api/compare                # Compare multiple products
POST   /api/chat                   # Chat about a product
```

### User Data
```
POST   /api/history/summary        # Get user's history
POST   /api/history/chat-session   # Get chat messages
POST   /api/history/latest-session # Get latest chat session
POST   /api/history/review         # Get saved review
```

### Shortlist
```
GET    /api/shortlist              # Get shortlisted products
POST   /api/shortlist/add          # Add to shortlist
POST   /api/shortlist/remove       # Remove from shortlist
```

### Profile
```
POST   /api/profile                # Save user profile
GET    /api/profile/{user_id}      # Get user profile
```

### Statistics
```
GET    /api/stats                  # Get platform statistics
GET    /health                     # Health check
```

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

---

## 💡 Usage Examples

### 1. Register a New User

```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

### 2. Analyze a Product

```bash
curl -X POST http://localhost:8001/api/review \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "product_name": "iPhone 15 Pro",
    "data_mode": "web",
    "use_web": true
  }'
```

### 3. Chat About a Product

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "product_name": "iPhone 15 Pro",
    "message": "Is this phone good for photography?",
    "conversation_history": []
  }'
```

### 4. Compare Products

```bash
curl -X POST http://localhost:8001/api/compare \
  -H "Content-Type: application/json" \
  -d '{
    "products": ["iPhone 15 Pro", "Samsung S24 Ultra", "Google Pixel 8 Pro"]
  }'
```

---

## ⚙️ Configuration

### Backend Configuration (.env)

```env
# API Keys
GROQ_API_KEY=your_groq_api_key_here          # Required
RAPIDAPI_KEY=your_rapidapi_key_here          # Optional

# Database
DATABASE_URL=sqlite:///./app.db              # SQLite (default)
# DATABASE_URL=postgresql://user:pass@host/db  # PostgreSQL

# Authentication
JWT_SECRET=your_secure_random_string         # Required (auto-generated)
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=10080                    # 7 days

# CORS
FRONTEND_ORIGINS=http://localhost:5173,https://yourdomain.com

# Logging
LOG_LEVEL=INFO                               # DEBUG, INFO, WARNING, ERROR
```

### Frontend Configuration (frontend/.env)

```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8001      # Local development
# VITE_API_BASE_URL=https://api.yourdomain.com  # Production
```

### Application Configuration (app_update.py)

```python
@dataclass
class AppConfig:
    # AI Model
    model_name: str = "llama-3.3-70b-versatile"
    max_tokens_review: int = 2500
    max_tokens_chat: int = 1000
    temperature_review: float = 0.3
    temperature_chat: float = 0.7
    
    # Web Scraping
    max_search_results: int = 10
    max_scrape_results: int = 6
    request_timeout: int = 10
    
    # Cache
    cache_ttl_hours: int = 24
    cache_max_size: int = 100
```

---

## 🌐 Deployment

### Deploy to Render.com

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render Account**
   - Sign up at [render.com](https://render.com)

3. **Deploy Using render.yaml**
   - The project includes a `render.yaml` configuration
   - Render will automatically detect and deploy
   - Set environment variables in Render dashboard

4. **Set Environment Variables**
   - `GROQ_API_KEY`
   - `JWT_SECRET`
   - `DATABASE_URL` (if using PostgreSQL)

### Deploy Frontend to Vercel

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

3. **Configure Environment**
   - Set `VITE_API_BASE_URL` to your backend URL

### Environment-Specific Settings

**Development:**
- SQLite database
- Debug logging
- CORS allows localhost
- Short JWT expiry for testing

**Production:**
- PostgreSQL database (recommended)
- INFO logging
- CORS restricted to production domains
- Longer JWT expiry
- HTTPS only
- Strong JWT_SECRET

---

## 🐛 Troubleshooting

### Common Issues

#### Backend Won't Start

**Problem**: "GROQ_API_KEY environment variable is not set"
```bash
# Solution: Check .env file
cat .env | grep GROQ_API_KEY

# If missing, add it:
echo "GROQ_API_KEY=your_key_here" >> .env
```

#### Frontend Can't Connect to Backend

**Problem**: Network errors in browser console
```bash
# Solution: Check frontend .env
cat frontend/.env

# Should have:
VITE_API_BASE_URL=http://localhost:8001
```

#### Database Errors

**Problem**: Table doesn't exist
```bash
# Solution: Reinitialize database
rm app.db
python -c "from database import init_db; init_db()"
```

#### Port Already in Use

**Problem**: "Address already in use"
```bash
# Solution: Use different port
uvicorn api:app --reload --port 8001

# Update frontend/.env:
VITE_API_BASE_URL=http://localhost:8001
```

### Getting Help

1. **Run Health Check**
   ```bash
   python comprehensive_check.py
   ```

2. **Check Logs**
   - Backend: `app.log`
   - Frontend: Browser console (F12)

3. **Read Documentation**
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Complete troubleshooting guide
   - [FAQ.md](FAQ.md) - Frequently asked questions

4. **Verify Setup**
   - Environment variables set correctly
   - All dependencies installed
   - Virtual environment activated

---

## 🤝 Contributing

Contributions are welcome! Here's how:

### 1. Fork the Repository

### 2. Create a Feature Branch
```bash
git checkout -b feature/amazing-feature
```

### 3. Make Your Changes
- Write clean, documented code
- Follow existing code style
- Add tests if applicable

### 4. Test Thoroughly
```bash
# Run tests
python test_backend.py
python comprehensive_check.py

# Test frontend
cd frontend
npm run build
```

### 5. Commit and Push
```bash
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

### 6. Create Pull Request

### Code Style Guidelines

**Python:**
- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Keep functions focused and small

**TypeScript/React:**
- Use functional components
- Follow React best practices
- Use TypeScript types
- Write descriptive variable names

---

## 📚 Documentation

Comprehensive documentation is available:

- **[PROJECT_STATUS_REPORT.md](PROJECT_STATUS_REPORT.md)** - Complete project overview
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Navigation hub
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Problem solving
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions
- **[DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md)** - Deployment guide
- **[BACKEND_TEST_GUIDE.md](BACKEND_TEST_GUIDE.md)** - Testing guide
- **[FAQ.md](FAQ.md)** - Frequently asked questions

### Quick Links

- **API Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health
- **Frontend**: http://localhost:5173

---

## 🔐 Security

### Best Practices

- ✅ Passwords are hashed with bcrypt
- ✅ JWT tokens for stateless authentication
- ✅ Input validation and sanitization
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ XSS prevention
- ✅ CORS protection
- ✅ Environment variables for secrets

### Security Recommendations

1. **Use Strong JWT_SECRET**
   ```bash
   # Generate secure random string
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Enable HTTPS in Production**
   - Use Render/Vercel automatic SSL
   - Or configure SSL certificates

3. **Restrict CORS**
   ```python
   # In production, only allow your domain
   FRONTEND_ORIGINS = ["https://yourdomain.com"]
   ```

4. **Regular Updates**
   ```bash
   pip install --upgrade -r requirements.txt
   npm update
   ```

---

## 📊 Performance

### Optimization Tips

1. **Enable Caching**
   - Web scraping results cached for 24 hours
   - Reduces API calls and improves speed

2. **Database Indexes**
   - All frequently queried columns indexed
   - Composite indexes for complex queries

3. **Async Operations**
   - FastAPI uses async for concurrent requests
   - Non-blocking database queries

4. **Frontend Optimization**
   - Code splitting with React lazy loading
   - Vite for fast builds
   - Minimal bundle size

### Monitoring

```bash
# Check application logs
tail -f app.log

# Monitor API performance
# Visit http://localhost:8001/docs and test endpoints
```

---

## 🎓 Learning Resources

### For Backend Development
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [Groq API Docs](https://console.groq.com/docs)

### For Frontend Development
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)

### For Full Stack
- [REST API Design](https://restfulapi.net/)
- [JWT Authentication](https://jwt.io/introduction)
- [Web Scraping Guide](https://realpython.com/beautiful-soup-web-scraper-python/)

---

## 📈 Roadmap

### Current Features (v1.0)
- ✅ AI-powered product analysis
- ✅ Nigerian market pricing
- ✅ User authentication
- ✅ Chat functionality
- ✅ Product comparison
- ✅ Shortlist management

### Planned Features (v2.0)
- 🔄 Price tracking and alerts
- 🔄 Email notifications
- 🔄 Social sharing
- 🔄 Product reviews export (PDF/Excel)
- 🔄 Advanced analytics dashboard
- 🔄 Mobile app (React Native)
- 🔄 Multi-language support
- 🔄 Browser extension

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** - For providing fast LLM inference
- **FastAPI** - For the excellent web framework
- **React** - For the powerful UI library
- **SQLAlchemy** - For the robust ORM
- **All open-source contributors**

---

## 📞 Support

### Need Help?

1. **Check Documentation**
   - Start with [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
   - Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

2. **Run Health Check**
   ```bash
   python comprehensive_check.py
   ```

3. **Review Logs**
   - Backend: `app.log`
   - Frontend: Browser console

4. **Community**
   - Create an issue on GitHub
   - Check FAQ for common questions

---

## 🎉 Get Started Now!

Ready to dive in? Here's your checklist:

- [ ] Clone the repository
- [ ] Get Groq API key from https://console.groq.com/keys
- [ ] Run `quick_start.bat` (Windows) or follow manual setup
- [ ] Start both servers with `start_app.bat`
- [ ] Open http://localhost:5173 in your browser
- [ ] Register an account
- [ ] Analyze your first product!

**Happy coding! 🚀**

---

<div align="center">

**[⬆ Back to Top](#-product-review-engine)**

Made with ❤️ using FastAPI and React

**Star ⭐ this repo if you find it helpful!**

</div>
