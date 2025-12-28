# Deployment Quick Start Guide
**Last Updated**: December 5, 2025

This is a quick reference for deploying to Render (backend) and Vercel (frontend).  
For detailed instructions, see `docs/DEPLOYMENT.md`.

---

## ✅ Prerequisites

- [ ] GitHub/GitLab/Bitbucket repository with your code
- [ ] Render account (free tier available)
- [ ] Vercel account (free tier available)
- [ ] Groq API key from https://console.groq.com/keys

---

## 🚀 Quick Deploy: Render (Backend) + Vercel (Frontend)

### Step 1: Deploy Backend to Render (5 minutes)

1. **Connect Repository to Render**
   - Go to https://dashboard.render.com
   - Click **New** → **Blueprint**
   - Select your repository
   - Render detects `render.yaml` automatically

2. **Configure Environment**
   - Select the `product-review-api` service
   - Go to **Environment** tab
   - Add: `GROQ_API_KEY` = `your_actual_groq_api_key`
   - Click **Save Changes**

3. **Deploy**
   - Click **Manual Deploy** → **Deploy**
   - Wait 2-5 minutes for build
   - Note your backend URL: `https://product-review-api-xxxx.onrender.com`

4. **Verify**
   ```bash
   curl https://your-api-url.onrender.com/health
   # Should return: {"status":"ok"}
   ```

### Step 2: Deploy Frontend to Vercel (3 minutes)

1. **Connect Repository to Vercel**
   - Go to https://vercel.com
   - Click **New Project**
   - Import your Git repository
   - Set **Root Directory**: `frontend`

2. **Configure Build Settings** (auto-detected)
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Set Environment Variable**
   - Add: `VITE_API_BASE_URL` = `https://your-api-url.onrender.com`
   - (Use the URL from Render, no trailing slash)

4. **Deploy**
   - Click **Deploy**
   - Wait 1-2 minutes
   - Visit your app: `https://your-app.vercel.app`

### Step 3: Verify Everything Works

1. Open your Vercel URL in browser
2. Try analyzing a product (e.g., "iPhone 15 Pro")
3. Check browser console - should have no CORS errors
4. Chat should work
5. Check Render logs if issues occur

---

## 🔧 Alternative: Deploy Both to Render

If you prefer hosting both on Render (no Vercel):

1. **Deploy Backend** (same as above)

2. **Deploy Frontend Static Site**
   - Render detects `product-review-frontend` from `render.yaml`
   - Set environment: `VITE_API_BASE_URL` = `https://your-api-url.onrender.com`
   - Deploy

3. **Update CORS in api.py**
   ```python
   FRONTEND_ORIGINS = [
       "http://localhost:5173",
       "https://product-review-frontend.onrender.com",  # Add this
   ]
   ```
   - Commit and redeploy backend

---

## 🐛 Troubleshooting

### Backend Issues

**"Application failed to respond"**
- Check Render logs for errors
- Verify `GROQ_API_KEY` is set correctly
- Check `requirements.txt` installed successfully

**"GROQ_API_KEY environment variable is not set"**
- Go to Render → Environment
- Add `GROQ_API_KEY` = your key
- Redeploy

### Frontend Issues

**"Network Error" when searching**
- Check `VITE_API_BASE_URL` in Vercel
- Make sure it points to Render backend URL
- No trailing slash in URL

**CORS errors in browser console**
- Backend should allow `*.vercel.app` automatically
- Check `api.py` lines 79-95
- If using Render static site, add to `FRONTEND_ORIGINS`

**Blank page / white screen**
- Check Vercel build logs
- Verify Root Directory is set to `frontend`
- Check Output Directory is `dist`

### Database Issues

**"Database locked" errors**
- SQLite doesn't support concurrent writes well
- For production, consider PostgreSQL on Render
- Add to `render.yaml`:
  ```yaml
  databases:
    - name: product-review-db
      databaseName: productreview
      user: productreview
  ```
- Update `DATABASE_URL` environment variable

---

## 📋 Deployment Checklist

### Pre-Deployment
- [x] All code pushed to Git repository
- [x] No syntax errors (verified via debug)
- [x] Environment variables documented
- [ ] Have Groq API key ready

### Render Backend
- [ ] Repository connected
- [ ] Blueprint deployed
- [ ] `GROQ_API_KEY` set
- [ ] Backend URL noted
- [ ] Health endpoint returns OK

### Vercel Frontend
- [ ] Repository connected
- [ ] Root Directory set to `frontend`
- [ ] `VITE_API_BASE_URL` configured
- [ ] Deployment successful
- [ ] App loads in browser

### Verification
- [ ] Can search for products
- [ ] Product reviews display
- [ ] Chat functionality works
- [ ] No CORS errors in console
- [ ] Images load (if any)
- [ ] Theme toggle works

---

## 📊 Current Configuration

### CORS Settings (api.py)
```python
FRONTEND_ORIGINS = [
    "http://localhost:5173",  # Local dev
]
VERCEL_ORIGIN_REGEX = r"https://.*\.vercel\.app"  # All Vercel deployments
```

This automatically allows:
- All Vercel deployments (production + preview)
- Local development
- You can add more specific origins as needed

### Environment Variables

**Backend (Render)**:
- `GROQ_API_KEY` (required) - Your Groq API key
- `DATABASE_URL` (optional) - Defaults to SQLite

**Frontend (Vercel)**:
- `VITE_API_BASE_URL` (required) - Backend API URL

---

## 🚦 Deployment Status

After following this guide, you should have:

| Component | Platform | URL Format | Status |
|-----------|----------|------------|--------|
| Backend API | Render | `https://product-review-api-xxxx.onrender.com` | ✅ |
| Frontend | Vercel | `https://your-app.vercel.app` | ✅ |
| Database | Render (SQLite) | N/A | ✅ |

---

## 🔗 Useful Links

- **Render Dashboard**: https://dashboard.render.com
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Groq Console**: https://console.groq.com
- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs

---

## 💡 Pro Tips

1. **Free Tier Limitations**
   - Render free tier: Spins down after inactivity (first request takes ~30s)
   - Vercel free tier: Unlimited deployments, 100GB bandwidth/month
   - Groq free tier: Rate limits apply

2. **Preview Deployments**
   - Vercel automatically creates preview URLs for pull requests
   - CORS already configured to allow all `*.vercel.app` domains

3. **Environment Variables**
   - Vercel: Can set per environment (Production, Preview, Development)
   - Render: Can set per service

4. **Custom Domains**
   - Both Render and Vercel support custom domains
   - Free SSL certificates included
   - Update CORS settings if using custom domain

5. **Monitoring**
   - Render provides logs and metrics
   - Vercel provides analytics and real-time logs
   - Consider adding Sentry for error tracking

---

## 🎯 Next Steps After Deployment

1. **Test Thoroughly**
   - Try multiple product searches
   - Test chat functionality
   - Check different use cases
   - Test on mobile devices

2. **Add Custom Domain** (optional)
   - Vercel: Settings → Domains
   - Render: Settings → Custom Domain
   - Update DNS records as instructed

3. **Set Up Monitoring**
   - Add Sentry for error tracking
   - Monitor Groq API usage
   - Check Render/Vercel logs regularly

4. **Consider Upgrading** (when ready)
   - Render: Upgrade for no cold starts
   - Consider PostgreSQL for production
   - More concurrent connections

---

**Need Help?**

- Detailed guide: See `docs/DEPLOYMENT.md`
- Setup issues: See `QUICK_DEBUG_GUIDE.md`
- Architecture: See `docs/ARCHITECTURE.md`
- General setup: See `README.md`
