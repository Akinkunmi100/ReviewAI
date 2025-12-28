# Deployment Guide

This guide explains how to deploy the Product Review Engine using:
- **Render** for the backend API
- **Vercel** for the frontend UI (or Render Static Site as an alternative)

The repo already contains some configuration to make this straightforward:
- `render.yaml` – defines a Render Web Service (backend) and Static Site (frontend).
- `api.py` – CORS is configured to allow:
  - `http://localhost:5173` (local dev)
  - `https://*.vercel.app` (Vercel deployments)

---

## 1. Backend on Render (FastAPI)

### 1.1 Prerequisites

- A Render account
- The repository pushed to GitHub, GitLab, or Bitbucket

### 1.2 Deploy via Render Blueprint (recommended)

1. Log in to Render.
2. Go to **Blueprints** → click **New Blueprint Instance**.
3. Select your repository.
4. Render will detect `render.yaml` and show:
   - A **Web Service** called `product-review-api`.
   - A **Static Site** called `product-review-frontend`.
5. Click **Apply** to create services.

Render will now build and deploy both services.

### 1.3 Backend environment variables

1. In Render, open the `product-review-api` service.
2. Go to **Environment**.
3. Add:
   - `GROQ_API_KEY = <your-real-groq-api-key>`
4. Save, then click **Manual Deploy** → **Clear build cache & deploy** if you changed variables.

### 1.4 Confirm backend is running

After deployment, Render will give you a URL, e.g.:

- `https://product-review-api.onrender.com`

Check the health endpoint:

```bash
curl https://product-review-api.onrender.com/health
```

You should see:

```json
{"status": "ok"}
```

---

## 2. Frontend on Vercel

### 2.1 Prerequisites

- Vercel account
- Same repository connected to Vercel

### 2.2 Create a Vercel project

1. Log in to Vercel.
2. Click **New Project**.
3. Import your Git repository.
4. When prompted for the **Project Root**, set it to `frontend`.
5. Vercel will auto-detect a Vite project and suggest:
   - Build Command: `npm run build`
   - Output Directory: `dist`

Click **Deploy** once environment variables are configured (next step).

### 2.3 Configure `VITE_API_BASE_URL` on Vercel

1. In the Vercel project settings, go to **Environment Variables**.
2. Add:
   - `VITE_API_BASE_URL = https://product-review-api.onrender.com`

   Use the exact URL from Render (no trailing slash).

3. Redeploy the Vercel project if necessary.

After deployment, Vercel will provide a URL, e.g.:

- `https://product-review-frontend.vercel.app`

Because `api.py` is configured with:

```python
FRONTEND_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
]

VERCEL_ORIGIN_REGEX = r"https://.*\\.vercel\\.app"
```

CORS will allow all `*.vercel.app` frontends by default, including previews.

### 2.4 Verify end-to-end

1. Visit your Vercel URL in the browser.
2. Open dev tools (Network tab).
3. Perform a product analysis in the UI.
4. You should see API requests to:
   - `https://product-review-api.onrender.com/api/review`
   - `https://product-review-api.onrender.com/api/chat`
   - etc.
5. There should be no CORS errors; responses should appear in the UI.

---

## 3. Alternative: Frontend as Render Static Site

If you prefer to host both backend and frontend on Render (no Vercel):

1. Use the `product-review-frontend` **Static Site** defined in `render.yaml`.
2. In the Static Site settings (Render dashboard):
   - Ensure **Build Command** is `npm install && npm run build`.
   - Ensure **Publish Directory** is `dist`.
   - Set environment variable:
     - `VITE_API_BASE_URL = https://product-review-api.onrender.com`.
3. Deploy the static site.
4. Update `FRONTEND_ORIGINS` in `api.py` to include the Render static site domain, e.g.:

```python
FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "https://product-review-frontend.onrender.com",
]
```

In this configuration, you can remove or ignore the Vercel deployment entirely.

---

## 4. Local development vs production

### 4.1 Local development (VS Code workflow)

#### Step 1 – Open the project in VS Code

1. Launch VS Code.
2. Use **File → Open Folder...** and select the project root (folder containing `api.py`, `app_update.py`, `frontend/`).

#### Step 2 – Backend (FastAPI)

1. Open a terminal in VS Code (PowerShell is fine) at the project root.
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install backend dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Set your dev API key (replace with your key):
   ```powershell
   $env:GROQ_API_KEY = "your_real_groq_key"
   ```
5. Run the FastAPI server:
   ```powershell
   uvicorn api:app --reload --port 8001
   ```
6. Optional: check health in a browser or terminal:
   - `http://localhost:8001/health`

#### Step 3 – Frontend (Vite + React)

1. Open **another** terminal in VS Code.
2. Move into the `frontend` folder and install dependencies:
   ```powershell
   cd frontend
   npm install
   ```
3. Create or edit `frontend/.env` with:
   ```env
   VITE_API_BASE_URL=http://localhost:8001
   ```
4. Start the Vite dev server:
   ```powershell
   npm run dev
   ```
5. Open the app in your browser:
   - `http://localhost:5173`

- You now have the full app running locally:
- Backend: `http://localhost:8001`
- Frontend: `http://localhost:5173`

### 4.2 Production

- Backend: Render Web Service at `https://product-review-api.onrender.com` (or similar).
- Frontend: Vercel at `https://<your-app>.vercel.app` (or Render Static Site if you choose that route).

Make sure `VITE_API_BASE_URL` always points to the correct backend URL for the environment.

### Production

- Backend: Render Web Service at `https://product-review-api.onrender.com` (or similar).
- Frontend: Vercel at `https://<your-app>.vercel.app` (or Render Static Site if you choose that route).

Make sure `VITE_API_BASE_URL` always points to the correct backend URL for the environment.

---

## 5. Checklist

- [ ] Repo connected to Render and Vercel.
- [ ] `GROQ_API_KEY` set in Render Web Service.
- [ ] `VITE_API_BASE_URL` set in Vercel (or Render Static Site) to the Render API URL.
- [ ] `FRONTEND_ORIGINS` / `VERCEL_ORIGIN_REGEX` in `api.py` correctly configured.
- [ ] Health endpoint (`/health`) returns OK in production.
- [ ] Frontend makes successful API calls with no CORS errors.

This document lives at `docs/DEPLOYMENT.md`. Update it if you change hosting providers, add Docker, or split services further.