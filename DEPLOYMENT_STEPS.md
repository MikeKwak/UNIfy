# UNIfy Deployment Steps

## Complete Deployment Guide - deploy UNIfy to production.

---

## Option 1: AWS Amplify (Full-Stack Deployment)

### Prerequisites
- AWS Account
- Git repository on GitHub, GitLab, or Bitbucket

### Frontend Deployment (React)

1. **Push your code to GitHub** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Create Amplify App**
   - Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify/)
   - Click "New app" → "Host web app"
   - Connect your repository
   - Select the main branch
   - The `amplify.yml` file is already configured!

3. **Build Settings** (should auto-detect)
   - Build command: `npm ci && npm run build`
   - Output directory: `dist`

4. **Environment Variables** (Add in Amplify Console)
   - Click "Environment variables"
   - Add: `VITE_API_URL` = your backend URL (set after backend deployment)

5. **Deploy**
   - Click "Save and deploy"
   - Wait for build to complete (~5-10 minutes)

### Backend Deployment (Flask)

**Option A: Railway (Easiest)**
1. Go to [Railway.app](https://railway.app/)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables:
   - `GEMINI_API_KEY` (if using)
   - `FLASK_HOST=0.0.0.0`
   - `FLASK_PORT=5000`
   - `FLASK_DEBUG=False`
6. Railway auto-detects Python and installs dependencies

**Option B: Render**
1. Go to [Render.com](https://render.com/)
2. Create new "Web Service"
3. Connect your GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Add environment variables (same as Railway)

**Option C: AWS Elastic Beanstalk**
1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create app: `eb create unify-app`
4. Configure environment variables in EB console

### After Backend Deployment

1. Update frontend environment variable:
   - Go to Amplify Console → App Settings → Environment variables
   - Update `VITE_API_URL` with your backend URL
   - Redeploy the frontend

2. Update backend CORS:
   - Add your Amplify URL to `FRONTEND_ORIGINS`
   - Example: `https://main.d1234abcde.amplifyapp.com`

---

## Option 2: Vercel (Frontend) + Railway/Render (Backend)

### Frontend: Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   cd UNIfy
   vercel
   ```
   - Follow prompts
   - Add environment variable: `VITE_API_URL` = your backend URL

3. **Or use Vercel Dashboard**
   - Go to [vercel.com](https://vercel.com/)
   - Import your GitHub repository
   - Add environment variables
   - Deploy

### Backend
Follow the same steps as Option 1 (Railway/Render)

---

## Option 3: Manual Deployment (Local Server)

### For Testing Only

```bash
# Terminal 1 - Backend
cd /Users/chevinjeon/Downloads/unify-forked-prod/UNIfy
source .venv/bin/activate  # or python -m venv .venv
pip install -r requirements.txt
python app.py

# Terminal 2 - Frontend
npm install
npm run build
npm run preview  # Preview production build
```

---

## 📝 Required Environment Variables

### Frontend (.env or Amplify Console)
```bash
VITE_API_URL=https://your-backend-url.com
```

### Backend (Railway/Render Console)
```bash
GEMINI_API_KEY=your_gemini_key_here
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
FRONTEND_ORIGINS=https://your-frontend-url.com
```

---

## 🔧 Post-Deployment Steps

### 1. Update API URL
After deploying backend, update frontend environment variable:
```bash
# In Amplify/Vercel console
VITE_API_URL=https://your-backend.com
```

### 2. Test the Deployment
```bash
# Test backend health
curl https://your-backend.com/

# Test recommendations
curl -X POST https://your-backend.com/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "mental_health": "ADHD",
    "physical_health": "None",
    "courses": "Computer Science",
    "gpa": 3.8,
    "severity": "moderate"
  }'
```

### 3. Test Frontend
- Visit your deployed frontend URL
- Fill out the user input form
- Submit and verify recommendations appear

---

## 🎯 Recommended Setup

**Easiest Path to Production:**
1. Frontend: AWS Amplify (uses your existing `amplify.yml`)
2. Backend: Railway (fastest setup, free tier available)
3. Total deployment time: ~30 minutes

---

## 🐛 Troubleshooting

### Backend Won't Start
- Check if all dependencies are in `requirements.txt`
- Verify `gunicorn` is installed for production
- Check logs in Railway/Render dashboard

### CORS Errors
- Update `FRONTEND_ORIGINS` in backend environment variables
- Include your exact frontend URL (no trailing slash)

### 404 Errors
- Verify build outputs are correct
- Check that `dist` folder exists after build
- Ensure `amplify.yml` output directory matches build output

### Models Not Found
- Ensure `models/` directory is included in deployment
- Models are already trained and saved in your repo
- No need to retrain

---

## 📊 Quick Reference

| Component | Service | Cost | Difficulty |
|-----------|---------|------|------------|
| Frontend | AWS Amplify | Free | Easy |
| Frontend | Vercel | Free | Easy |
| Backend | Railway | $5-10/mo | Easy |
| Backend | Render | Free tier | Easy |
| Backend | AWS EB | ~$20/mo | Medium |

---

## 🎓 Next Steps After Deployment

1. **Monitor Performance**: Check logs in your cloud console
2. **Set up Custom Domain**: Configure in Amplify/Vercel settings
3. **Enable Analytics**: Add Google Analytics or similar
4. **Set up CI/CD**: Already configured with `amplify.yml`
5. **Monitor Costs**: Track usage on cloud provider dashboards

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub/GitLab
- [ ] Backend deployed (Railway/Render)
- [ ] Frontend deployed (Amplify/Vercel)
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] API URL updated in frontend
- [ ] Health endpoint tested
- [ ] Recommendation endpoint tested
- [ ] Frontend form tested end-to-end
- [ ] Custom domain configured (optional)
- [ ] SSL/HTTPS enabled

---

## 📞 Need Help?

- Check `DEPLOYMENT.md` for technical details
- Check `INTEGRATION_GUIDE.md` for API information
- Review logs in your cloud provider dashboard
- Test locally first: `python app.py` + `npm run dev`

---

**Current Status:** Your project is ready to deploy! The `amplify.yml` file is configured and all code is production-ready.
