# Product Review Engine – Architecture & Internal Documentation

This document describes the overall architecture of the Product Review Engine, including backend services, frontend structure, data models, and operational considerations.

## 0. Requirements

### Backend
- Python 3.10+ (recommended)
- Key Python packages (installed via `pip` or `requirements.txt`):
  - `fastapi` – web framework
  - `uvicorn[standard]` – ASGI server
  - `pydantic` / `pydantic-settings` – data validation and configuration
  - `requests` – HTTP client for web search and scraping
  - `beautifulsoup4` – HTML parsing
  - `groq` – Groq API client
  - `streamlit` – legacy UI (if still used)
  - `textblob`, `vaderSentiment` – sentiment analysis
  - `numpy` – numeric utilities
  - `Pillow` – image handling
  - Any additional libraries referenced in `app_update.py`

### Frontend
- Node.js 18+ (LTS recommended)
- npm 9+ or yarn
- Vite + React + TypeScript stack (installed via `npm install` in `frontend/`):
  - `react`, `react-dom`
  - `vite`
  - `typescript`
  - Supporting dev dependencies as listed in `frontend/package.json`

### Environment
- Environment variables:
  - `GROQ_API_KEY` – required for backend AI features.
  - `VITE_API_BASE_URL` – frontend API base URL (e.g. `http://localhost:8001` in dev).

---

## 1. High-level overview

The Product Review Engine is a full-stack web application that helps users evaluate consumer products (especially for the Nigerian market) using a mix of:
- Live web search and scraping.
- AI-powered analysis (via Groq models).
- Nigerian-specific price comparison from major online retailers.

It consists of:
- **Backend (FastAPI)** – REST API layer that exposes endpoints for generating product reviews, comparing products, and running a product-centric chat.
- **Domain logic (Python)** – In `app_update.py`, containing web search, scraping, sentiment analysis, price comparison, risk detection, purchase timing advice, and comparison logic.
- **Frontend (React + Vite + TypeScript)** – Single-page UI that interacts with the API, visualizes rich review data, and provides chat and comparison tools.

---

## 2. Backend

### 2.1 Entry point: `api.py`

`api.py` defines the FastAPI application and public HTTP interface.

Key responsibilities:
- Configure CORS for the frontend.
- Instantiate the `EnhancedProductReviewService` from `app_update.py` (via `get_review_service`).
- Define request models and API endpoints.

#### 2.1.1 Configuration

- **Environment variables**
  - `GROQ_API_KEY` – Required. API key for the Groq client used by the domain services.

- **CORS**
  - `FRONTEND_ORIGINS` – List of allowed frontend origins.
  - Currently includes:
    - `http://localhost:5173` (Vite dev server).
  - Add your production URLs here before deployment.

#### 2.1.2 Request models

Defined using Pydantic in `api.py`:

- `ReviewRequest`
  - `product_name: str`
  - `use_web: bool = True` – whether to use web search/scraping or fall back to AI training data.

- `CompareRequest`
  - `products: conlist(str, min_items=2, max_items=4)` – between 2 and 4 product names.

- `ChatRequest`
  - `product_name: str`
  - `message: str`
  - `conversation_history: List[Dict[str, str]]` – chat messages with `{role, content}` shape.
  - `use_web: bool = True`
  - `user_profile: Dict[str, Any] | None` – JSON object matching the `UserProfile` model from `app_update.py`.

#### 2.1.3 Response conventions

All endpoints follow a simple convention:
- On success, they return the appropriate Pydantic model serialized to JSON.
- On failure, they return an error object of the form:
  ```json
  { "error": { "message": "..." } }
  ```

The frontend knows how to interpret this via a shared error handler.

#### 2.1.4 Endpoints

- `POST /api/review`
  - Request: `ReviewRequest`.
  - Response: `EnhancedProductReview` (from `app_update.py`).
  - Behavior:
    - Uses `EnhancedProductReviewService.generate_review`.

- `POST /api/compare`
  - Request: `CompareRequest`.
  - Response: `ProductComparison`.
  - Behavior:
    - Uses `EnhancedProductReviewService.generate_comparison`.

- `POST /api/chat`
  - Request: `ChatRequest`.
  - Response: `{ "reply": string }` on success or error object.
  - Behavior:
    - Ensures a review exists for the product (calls `generate_review`).
    - Optionally constructs a `UserProfile` from the JSON payload.
    - Delegates to `service.chat_service.get_chat_response`.

- `GET /health`
  - Simple health check returning `{ "status": "ok" }`.

---

### 2.2 Domain layer: `app_update.py`

This module contains the majority of the business logic. Major components:

#### 2.2.1 Configuration & constants
- `AppConfig` – central config (model name, token limits, web scraping limits, cache TTL, UI settings).
- `Constants` – static constants like:
  - User agent, headers for requests.
  - Nigerian retailers metadata (`Jumia`, `Konga`, `Slot`, `Pointek`).
  - Currency defaults and fallback FX rate.

#### 2.2.2 Currency & price utilities
- `CurrencyFormatter` – parses and formats prices, detects currencies, converts to NGN.
- Handles:
  - Naira formatting (`₦` with thousand separators).
  - Parsing strings like `₦450,000`, `NGN 450000`, ranges, etc.
  - Detecting currency based on symbols and codes.

#### 2.2.3 Core Pydantic models

These models structure the data returned to the UI:

- `SearchResult`, `ScrapedContent` – for search and scraping results.
- `ProductReview` – base review.
- `EnhancedProductReview` – extended review with:
  - Sentiment analysis.
  - Product images and primary image.
  - Nigerian and global pricing info and comparison.
  - Red-flag report.
  - Purchase timing advice.
  - "Best for" tags, budget tier.
  - Alternatives and data quality info.
- Nigerian pricing models:
  - `RetailerPrice`, `PriceComparison`.
- Risk models:
  - `RedFlag`, `RedFlagReport`.
- Timing:
  - `PurchaseTimingAdvice`.
- Recommendation tags:
  - `BestForTag`.
- User personalization:
  - `UserProfile` (min/max budget, use cases, preferred brands).
- Comparison:
  - `ProductComparisonItem`, `ProductComparison`, `AlternativeProduct`.

#### 2.2.4 Exceptions

Custom exceptions derived from `ProductReviewError`:
- `SearchError`
- `ScrapingError`
- `AIGenerationError`
- `ValidationError`

These are caught at the API level and mapped into error responses.

#### 2.2.5 Cache management

- `CacheManager`
  - Backed by a `.cache/` directory using JSON files.
  - TTL-based invalidation.
  - Size-limited (removes oldest entries beyond max size).
  - Used to cache:
    - Search results.
    - Scraped content.
    - Nigerian price comparisons.
    - Product images (metadata).

#### 2.2.6 Web search & scraping

- `WebSearchClient`
  - Uses DuckDuckGo HTML search.
  - Returns `SearchResult` list.
  - Caches results by query.

- `ContentScraper`
  - Fetches pages from search results.
  - Uses BeautifulSoup to strip scripts, navs, etc., and extract main content.
  - Cleans and truncates content to a configurable max length.
  - Caches `ScrapedContent` per URL.

#### 2.2.7 Nigerian price service

- `NigerianPriceService`
  - Responsible for scraping key Nigerian retailers:
    - Jumia, Konga, Slot, Pointek.
  - Uses selectors tailored to each site.
  - Normalizes prices using `CurrencyFormatter`.
  - Aggregates into `PriceComparison` with:
    - Lowest, highest, average price.
    - Best deal retailer.
    - Derived summaries for potential savings / deal quality.

#### 2.2.8 Product images

- `ProductImageFetcher`
  - Builds enhanced image queries (e.g., adds "official product image").
  - First tries DuckDuckGo image search, then Bing Images as fallback.
  - Returns `ProductImage` list and can optionally download/resize/encode images as base64 for display.

#### 2.2.9 Sentiment analysis

- `SentimentAnalyzer`
  - Uses TextBlob and VADER:
    - Overall sentiment.
    - Polarity, subjectivity.
    - Compound/positive/negative/neutral scores.
  - Aspect-level sentiment breakdown (quality, performance, value, design, features, usability).
  - Extracts key positive/negative aspects.
  - Generates a human-readable summary.

#### 2.2.10 Red-flag detection

- `RedFlagDetector`
  - Heuristic detection of:
    - Product defects.
    - Reliability issues.
    - Fake review patterns.
  - Produces a `RedFlagReport` with:
    - Red flags list.
    - Overall risk level and score.
    - Common complaints.
    - Recommendation string.

#### 2.2.11 Purchase timing advisor

- `PurchaseTimingAdvisor`
  - Considers:
    - Product lifecycle (e.g., year in product name, generational terms).
    - Nigerian sale periods (Black Friday, Boxing Day, etc.).
    - Typical release cycles for certain product families (iPhone, Galaxy, etc.).
  - Returns `PurchaseTimingAdvice` with:
    - Recommendation (buy now, wait, consider alternatives).
    - Reasoning.
    - Best sale periods.
    - Simple deal quality & price trend.

#### 2.2.12 Comparison generator

- `ComparisonGenerator`
  - Converts multiple `EnhancedProductReview` objects into a `ProductComparison`:
    - Extracts `ProductComparisonItem` for each product.
    - Determines winners by category (price, rating, features).
    - Picks best-value, best-budget, and best-premium options.
    - Generates a short AI-style recommendation summarizing results.

---

## 3. Frontend

The frontend is a Vite + React + TypeScript application under `frontend/`.

### 3.1 Entry points

- `src/main.tsx`
  - Standard ReactDOM.render entry, renders `<App />` into `#root`.

- `src/App.tsx`
  - Wraps the main `ReviewPage` in an application shell.
  - Renders the app header with:
    - Title and badge.
    - Tagline.
    - Theme toggle button (light/dark).
  - Manages theme state:
    - Reads from `localStorage` and `prefers-color-scheme` on initial load.
    - Writes selection back to `localStorage`.
    - Applies `data-theme="light" | "dark"` on `document.documentElement`.

- `src/pages/ReviewPage.tsx`
  - Core page component containing the layout:
    - Left sidebar: `ProfilePanel`, `HistorySidebar`.
    - Main content: `SearchBar`, review sections, chat, comparison view.
  - Manages page-level state:
    - `productName`, `useWeb` (web search vs AI knowledge).
    - `history: HistoryEntry[]` – previous analyzed products.
    - `shortlist: HistoryEntry[]` – user short-listed products.
    - `userProfile` – from `ProfilePanel`.
  - Hooks:
    - `useReview` – fetches product review via `/api/review`.
    - `useChat` – manages chat state via `/api/chat`.
  - Behavior:
    - `handleAnalyze` trims input, calls `fetchReview`, and, if successful, appends a `HistoryEntry` built from the result.
    - `handleShortlistAdd` adds a `HistoryEntry` to the shortlist if not already present.

### 3.2 API client and types

**File:** `src/api/types.ts`

- TypeScript interfaces mirror the backend Pydantic models:
  - `SentimentScore`, `AspectBreakdownItem`.
  - `ProductImage`, `RetailerPrice`, `PriceComparison`.
  - `RedFlag`, `RedFlagReport`, `PurchaseTimingAdvice`.
  - `BestForTag`, `AlternativeProduct`.
  - `EnhancedProductReview` – main object used by UI.
  - `ProductComparisonItem`, `ProductComparison`.

**File:** `src/api/client.ts`

- `API_BASE` – computed from env:
  - `import.meta.env.VITE_API_BASE_URL || window.location.origin`.
- `handleJson<T>` – shared response handler that:
  - Parses JSON.
  - Normalizes error shapes from backend (`string` or `{ message }`).
  - Throws `Error` with a human-readable message when HTTP status is not OK or when `error` is present.

API functions:
- `apiReview(productName: string, useWeb?: boolean): Promise<EnhancedProductReview>`.
- `apiCompare(products: string[]): Promise<ProductComparison>`.
- `apiChat(params: { productName; message; history; useWeb?; userProfile? }): Promise<{ reply: string }>`.

### 3.3 Hooks

- `useReview`
  - Manages `review`, `loading`, `error`.
  - `fetchReview(productName, useWeb): Promise<EnhancedProductReview | null>`:
    - Calls `apiReview`.
    - Sets state.
    - Returns the fetched review (or `null` on error).

- `useChat(productName, useWeb, userProfile)`
  - Manages `messages: ChatMessage[]`, `loading`, `error`.
  - `sendMessage(text: string)`:
    - Appends user message.
    - Calls `/api/chat` with conversation history and profile.
    - Appends assistant reply as a new message.

### 3.4 Major components

- `SearchBar`
  - Text input + radio toggles for `useWeb` vs `AI knowledge`.
  - Calls `onAnalyze` when user clicks "Analyze".

- `DecisionCard`
  - Shows product name, predicted rating, and primary price.
  - Displays primary image when available.
  - Button to add to shortlist.

- `PricingSection`
  - Uses `EnhancedProductReview.price_comparison` to show Nigerian retailer prices and ranges.

- `ProsConsSection`
  - Displays pros and cons lists from `review.pros` / `review.cons`.

- `SentimentSection`
  - Shows overall sentiment, compound score, confidence, tone.
  - Visualizes aspect sentiment (e.g., quality, performance) with horizontal bars.

- `RiskSection`
  - Displays overall risk pill (low/medium/high) with score.
  - Lists red flags with severity styling.

- `TimingSection`
  - Shows purchase recommendation (buy now, wait, consider alternatives) with icon.
  - Explains reasoning and best sale periods.

- `BestForSection`
  - Renders "best for" use cases as pill chips.
  - Indicates `budget_tier`.

- `AlternativesSection`
  - Lists alternative products with snippet and link (opens in new tab).

- `SourcesSection`
  - Renders list of source URLs used in the review.

- `ChatPanel`
  - Displays chat messages between user and assistant.
  - Shows a "Thinking..." hint while `chat.loading` is true.
  - Input + send button:
    - Disabled while sending.
    - Button label changes to "Sending..." while loading.

- `HistorySidebar`
  - Shows recent analyzed products and shortlist using `HistoryEntry` type.

- `ProfilePanel`
  - Collects user profile:
    - Min/max budget (₦).
    - Use cases (chips + custom input).
    - Preferred brands.
  - Emits `UserProfile` object used by backend to personalize recommendations.

- `ComparisonView`
  - Uses shortlist data to show simple comparison grid.
  - Intended to be wired to `/api/compare` for richer comparisons.

- `GlobalAlert`
  - Simple global error banner.
  - Currently used to show `useReview.error` above main content.

### 3.5 Theming & layout

**File:** `src/styles.css`

- Uses CSS custom properties (`:root`) for design tokens:
  - Backgrounds, text, primary, success, warning, danger colors.
- Dark theme:
  - `:root[data-theme="dark"]` overrides the tokens.
- `App.tsx` sets `data-theme` attribute on `<html>`.
- Layout:
  - `.app-header` – header bar containing title, tagline, theme toggle.
  - `.layout` – main two-column layout.
  - `.sidebar` – profile + history card.
  - `.content` – main review and chat area.

- Components are styled with a coherent card-based aesthetic.
- Skeleton loader classes (`.review-skeleton`, `.skeleton-card`, `.skeleton-row`) provide visual feedback while waiting for initial reviews.

---

## 4. Error handling strategy

### 4.1 Backend

- All domain-specific errors (`ProductReviewError` and descendants) are caught and returned as:
  ```json
  { "error": { "message": "..." } }
  ```
- Unexpected exceptions in `/api/chat` are caught and returned as a generic message to avoid leaking internals.

### 4.2 Frontend

- `handleJson` in `api/client.ts` normalizes error shapes and throws `Error` with a clean `.message` string.
- Hooks (`useReview`, `useChat`) catch these and set `error` state.
- `GlobalAlert` displays review-related errors.
- `ChatPanel` shows chat-related errors under the messages.

---

## 5. Running locally

See the root `README.md` for step-by-step instructions, but at a high level:

1. **Backend**
   - Install dependencies, set `GROQ_API_KEY`.
  - Start FastAPI via Uvicorn, e.g. `uvicorn api:app --reload --port 8001`.

2. **Frontend**
   - `cd frontend && npm install`.
  - Create `.env` from `.env.example` and set `VITE_API_BASE_URL=http://localhost:8001`.
   - Start dev server with `npm run dev`.

Vite will run on `http://localhost:5173`, and the frontend will communicate with the backend via the configured API base URL.

---

## 6. Production considerations

- **CORS** – ensure `FRONTEND_ORIGINS` includes your real domains.
- **Secrets** – use environment variables or a secrets manager for `GROQ_API_KEY` et al.
- **Logging & Monitoring** – integrate FastAPI logs with your logging stack; consider APM for error tracking.
- **Scaling** – run FastAPI behind a process manager and reverse proxy, and tune workers for concurrency.
- **Security** – consider rate limiting, authentication/authorization if exposing to the public.

This document is intended as an internal reference for engineers working on the Product Review Engine. Update it whenever major architectural changes are made.