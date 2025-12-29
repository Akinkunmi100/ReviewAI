"""
Product Review Engine API

This is the main FastAPI application that imports all route modules.
"""

import os
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from dotenv import load_dotenv

from auth import JWT_SECRET
from database import init_db

# Import route modules
from routes.auth import router as auth_router
from routes.review import router as review_router
from routes.chat import router as chat_router
from routes.history import router as history_router
from routes.profile import router as profile_router
from routes.stats import router as stats_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Product Review Engine API")


# =============================================================================
# Error Handlers
# =============================================================================

def _error(message: str, status_code: int = 400):
    return JSONResponse(status_code=status_code, content={"error": {"message": message}})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    msg = detail if isinstance(detail, str) else str(detail)
    return _error(msg, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return _error("Invalid request.", status_code=422)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error")
    return _error("An unexpected error occurred while processing your request.", status_code=500)


# =============================================================================
# Load Environment
# =============================================================================

try:
    load_dotenv()
    logger.info("Loaded .env into environment (if present).")
except Exception:
    pass


# =============================================================================
# Startup Event
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("=" * 60)
    logger.info("🚀 Product Review Engine API Starting...")
    logger.info("=" * 60)
    
    # Initialize database
    try:
        init_db()
        logger.info("✓ Database initialized successfully")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        raise
    
    # Check for required environment variables
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        logger.info("✓ GROQ_API_KEY found")
    else:
        logger.warning("⚠ GROQ_API_KEY not set - API will fail on review requests")

    # Security check
    env = os.getenv("ENV", "").lower()
    if env in ("prod", "production") and JWT_SECRET == "dev-insecure-change-me":
        raise RuntimeError("JWT_SECRET is using the insecure default; set JWT_SECRET in production")
    
    db_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    logger.info(f"✓ Database: {db_url}")
    
    logger.info("✓ CORS enabled for development and production origins")
    logger.info("=" * 60)
    logger.info("✅ API ready! Listening for requests...")
    logger.info("=" * 60)


# =============================================================================
# CORS Configuration
# =============================================================================

FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
    "http://localhost:5176",
    "http://127.0.0.1:5176",
]

VERCEL_ORIGIN_REGEX = r"https://.*\.vercel\.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_origin_regex=VERCEL_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Health Check
# =============================================================================

@app.get("/health")
async def health_check():
    return {"status": "ok"}


# =============================================================================
# Admin Cache Management
# =============================================================================

@app.post("/api/admin/clear-cache")
async def clear_cache():
    """Clear all cached data (images, content, search results)."""
    import shutil
    from pathlib import Path
    
    cache_dir = Path(".cache")
    cleared_count = 0
    
    if cache_dir.exists():
        for cache_file in cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                cleared_count += 1
            except Exception:
                pass
    
    logger.info(f"Cache cleared: {cleared_count} entries removed")
    return {"status": "ok", "message": f"Cleared {cleared_count} cache entries"}


# =============================================================================
# Include Route Modules
# =============================================================================

app.include_router(auth_router)
app.include_router(review_router)
app.include_router(chat_router)
app.include_router(history_router)
app.include_router(profile_router)
app.include_router(stats_router)
