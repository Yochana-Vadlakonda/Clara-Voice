# 🚀 Vercel Deployment Guide - Complete Steps

## Prerequisites

1. **Vercel Account** - Sign up at https://vercel.com
2. **Git Repository** - Your code should be in a Git repository (GitHub, GitLab, or Bitbucket)
3. **Environment Variables Ready** - Your Retell API token and database credentials

---

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Repository

Make sure all your changes are committed:

```bash
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### Step 2: Install Vercel CLI (Optional but Recommended)

```bash
npm install -g vercel
```

Or use the Vercel web dashboard (easier for first-time deployment).

---

## 🌐 Option A: Deploy via Vercel Dashboard (Recommended)

### 1. **Go to Vercel Dashboard**
- Visit https://vercel.com/dashboard
- Click **"Add New Project"**

### 2. **Import Your Git Repository**
- Click **"Import Git Repository"**
- Select your repository from GitHub/GitLab/Bitbucket
- Click **"Import"**

### 3. **Configure Project Settings**

**Project Name:** `clara-agent-creation` (or your preferred name)

**Root Directory:** `clara-onboarding-website`
- Click **"Edit"** next to Root Directory
- Enter: `clara-onboarding-website`
- This tells Vercel to deploy only the web interface folder

**Framework Preset:** Other (no framework)

**Build Settings:**
- Build Command: (leave empty)
- Output Directory: (leave empty)
- Install Command: (leave empty)

### 4. **Add Environment Variables**

Click **"Environment Variables"** and add these:

```
RETELL_API_TOKEN = key_f179b569899f2ab68c5f875033e0
DB_HOST = localhost
DB_PORT = 5432
DB_NAME = self_onb
DB_USER = postgres
DB_PASSWORD = Admin123
```

**Important:** For production, you'll need a cloud PostgreSQL database (not localhost). Options:
- **Supabase** (recommended, free tier available)
- **Neon** (serverless PostgreSQL)
- **Railway** (easy PostgreSQL hosting)
- **AWS RDS** (enterprise option)

### 5. **Deploy**
- Click **"Deploy"**
- Wait 2-3 minutes for deployment to complete
- You'll get a URL like: `https://clara-agent-creation.vercel.app`

---

## 💻 Option B: Deploy via Vercel CLI

### 1. **Navigate to Web Interface Folder**
```bash
cd clara-onboarding-website
```

### 2. **Login to Vercel**
```bash
vercel login
```

### 3. **Deploy to Production**
```bash
vercel --prod
```

### 4. **Follow the Prompts**
- **Set up and deploy**: Yes
- **Which scope**: Choose your account
- **Link to existing project**: No (first time)
- **Project name**: `clara-agent-creation`
- **Directory**: `.` (current directory)
- **Override settings**: No

### 5. **Add Environment Variables**
```bash
vercel env add RETELL_API_TOKEN
# Enter your token when prompted

vercel env add DB_HOST
# Enter your database host

vercel env add DB_PORT
# Enter 5432

vercel env add DB_NAME
# Enter self_onb

vercel env add DB_USER
# Enter postgres

vercel env add DB_PASSWORD
# Enter your password
```

### 6. **Redeploy with Environment Variables**
```bash
vercel --prod
```

---

## 🗄️ Database Setup for Production

Since Vercel is serverless, you can't use `localhost` for the database. Here are your options:

### Option 1: Supabase (Recommended - Free Tier)

1. **Sign up at** https://supabase.com
2. **Create a new project**
3. **Get connection details:**
   - Go to Project Settings → Database
   - Copy the connection string
4. **Update environment variables in Vercel:**
   ```
   DB_HOST = db.xxxxxxxxxxxxx.supabase.co
   DB_PORT = 5432
   DB_NAME = postgres
   DB_USER = postgres
   DB_PASSWORD = your_supabase_password
   ```
5. **Run database setup:**
   - Use Supabase SQL Editor
   - Copy contents of `database_setup.sql`
   - Execute in SQL Editor

### Option 2: Neon (Serverless PostgreSQL)

1. **Sign up at** https://neon.tech
2. **Create a new project**
3. **Get connection string**
4. **Update Vercel environment variables**

### Option 3: Railway

1. **Sign up at** https://railway.app
2. **Create PostgreSQL database**
3. **Get connection details**
4. **Update Vercel environment variables**

---

## ✅ Verify Deployment

### 1. **Test Web Interface**
Visit your Vercel URL: `https://your-project.vercel.app`

You should see the Clara onboarding form.

### 2. **Test Form Submission**
Fill out the form with test data:
- Company Name: Test Company
- Address: 123 Test St
- Website: https://example.com
- Time Zone: Mountain
- Business Days: Mon-Fri
- Hours: 9:00 AM - 5:00 PM
- Phone: +1234567890

Submit and verify it creates an agent successfully.

### 3. **Check Vercel Logs**
```bash
vercel logs your-project-url
```

Or in the dashboard:
- Go to your project
- Click "Deployments"
- Click on latest deployment
- View "Functions" logs

---

## 🔧 Troubleshooting

### Issue: "404 NOT_FOUND" on API calls

**Solution:**
- Verify `vercel.json` is in `clara-onboarding-website` folder
- Check that root directory is set to `clara-onboarding-website`
- Redeploy: `vercel --prod`

### Issue: "Function Timeout"

**Solution:**
- Vercel free tier has 10-second timeout
- Upgrade to Pro for 60-second timeout
- Or optimize the agent creation process

### Issue: Database Connection Failed

**Solution:**
- Can't use `localhost` on Vercel
- Must use cloud database (Supabase, Neon, Railway)
- Update environment variables with cloud database credentials

### Issue: "Invalid API Key" Error

**Solution:**
- Verify `RETELL_API_TOKEN` is set in Vercel environment variables
- Check the token is correct (no extra spaces)
- Redeploy after adding environment variables

### Issue: CORS Errors

**Solution:**
- Already handled in the code
- If still occurring, check browser console
- Verify API endpoints return proper CORS headers

---

## 🔄 Updating Your Deployment

### Automatic Updates (Recommended)

1. **Connect GitHub to Vercel:**
   - In Vercel dashboard, go to Project Settings
   - Connect your GitHub repository
   - Every push to `main` branch auto-deploys

### Manual Updates

```bash
cd clara-onboarding-website
vercel --prod
```

---

## 📊 Project Structure for Vercel

Your `clara-onboarding-website` folder should have:

```
clara-onboarding-website/
├── api/                          # Serverless API functions
│   ├── _config.py               # Configuration
│   ├── _database.py             # Database operations
│   ├── _onboarding_engine.py   # Main onboarding logic
│   ├── onboard.py               # POST /api/onboard
│   └── create-agent.py          # POST /api/create-agent
├── src/                         # JavaScript files
│   └── main.js
├── styles/                      # CSS files
│   └── main.css
├── assets/                      # Images
│   └── clara_black.png
├── index.html                   # Main page
├── vercel.json                  # Vercel configuration
└── requirements.txt             # Python dependencies
```

---

## 🎯 Environment Variables Summary

Add these in Vercel Dashboard → Project Settings → Environment Variables:

| Variable | Value | Notes |
|----------|-------|-------|
| `RETELL_API_TOKEN` | `key_f179b569899f2ab68c5f875033e0` | Your Retell API key |
| `DB_HOST` | Cloud database host | NOT localhost |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `self_onb` | Database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | Your password | Database password |

---

## 🎉 Success Checklist

- ✅ Project deployed to Vercel
- ✅ Custom domain configured (optional)
- ✅ Environment variables added
- ✅ Cloud database connected
- ✅ Web interface loads correctly
- ✅ Form submission works
- ✅ Agent creation completes successfully
- ✅ Credentials displayed in UI
- ✅ No errors in Vercel logs

---

## 📞 Next Steps

1. **Test thoroughly** with real company data
2. **Set up custom domain** (optional)
3. **Monitor Vercel logs** for any issues
4. **Set up database backups** (important!)
5. **Consider upgrading Vercel plan** if you need longer function timeouts

---

## 💡 Pro Tips

1. **Use Vercel Preview Deployments** - Every branch gets a preview URL
2. **Enable Vercel Analytics** - Track usage and performance
3. **Set up Vercel Monitoring** - Get alerts for errors
4. **Use Environment Variables per Environment** - Different values for production/staging
5. **Enable Vercel Protection** - Add password protection if needed

---

## 🆘 Need Help?

- **Vercel Docs:** https://vercel.com/docs
- **Vercel Support:** https://vercel.com/support
- **Check Logs:** `vercel logs` or dashboard
- **Community:** Vercel Discord server

---

**Your deployment URL will be:** `https://your-project-name.vercel.app`

Good luck with your deployment! 🚀
