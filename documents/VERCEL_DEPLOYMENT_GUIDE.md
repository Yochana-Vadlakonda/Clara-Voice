# Vercel Deployment Guide

## 🚀 Quick Deployment Steps

### 1. **Navigate to Web Interface Folder**
```bash
cd clara-onboarding-website
```

### 2. **Deploy to Vercel**
```bash
# Install Vercel CLI if not already installed
npm install -g vercel

# Deploy to production
vercel --prod
```

### 3. **Follow Vercel Prompts**
- **Set up and deploy**: Yes
- **Which scope**: Choose your account/team
- **Link to existing project**: No (for first deployment)
- **Project name**: `clara-agent-creation` (or your preferred name)
- **Directory**: `.` (current directory)
- **Override settings**: No

## 🔧 **What's Deployed**

### **Web Interface (Demo Mode)**
- ✅ **Complete web form** for company information
- ✅ **Real-time progress updates** during creation
- ✅ **Demo agent creation** with sample credentials
- ✅ **Responsive design** works on all devices

### **API Endpoints**
- ✅ **`/api/create-agent`** - Handles form submissions (demo mode)
- ✅ **`/api/creation-status/[id]`** - Returns creation status (demo)
- ✅ **`/api/test`** - Test endpoint to verify deployment

### **Static Assets**
- ✅ **HTML/CSS/JavaScript** - Pure frontend, no build process
- ✅ **Images and fonts** - All assets properly served
- ✅ **Responsive styling** - Works on desktop and mobile

## 🎯 **Demo vs Production Mode**

### **Vercel Deployment (Demo Mode)**
- **Purpose**: Showcase the web interface and user experience
- **Agent Creation**: Returns demo credentials (not real agents)
- **Database**: No database connection (serverless limitations)
- **Benefits**: 
  - Fast deployment and showcasing
  - No infrastructure setup required
  - Perfect for demonstrations and testing UI

### **Local Development (Production Mode)**
- **Purpose**: Actual agent creation with Retell API
- **Agent Creation**: Creates real agents, LLMs, and phone numbers
- **Database**: Full PostgreSQL integration
- **Benefits**:
  - Complete functionality
  - Real agent creation
  - Database persistence

## 📋 **Vercel Configuration Details**

### **vercel.json Configuration**
```json
{
  "version": 2,
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.9"
    }
  },
  "builds": [
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    },
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/create-agent",
      "dest": "/api/create-agent.py"
    },
    {
      "src": "/api/creation-status/(.*)",
      "dest": "/api/creation-status/[creation_id].py"
    },
    {
      "src": "/",
      "dest": "/index.html"
    }
  ]
}
```

### **Python Dependencies**
```txt
python-dotenv==1.0.0
requests==2.31.0
psycopg2-binary==2.9.7
```

## 🔍 **Testing Your Deployment**

### **1. Test Web Interface**
- Visit your Vercel URL (e.g., `https://your-project.vercel.app`)
- Should load the Clara onboarding form
- Fill out company information and submit

### **2. Test API Endpoints**
```bash
# Test the test endpoint
curl https://your-project.vercel.app/api/test

# Test agent creation (should return demo response)
curl -X POST https://your-project.vercel.app/api/create-agent \
  -H "Content-Type: application/json" \
  -d '{"companyName":"Test Company","officeAddress":"123 Test St"}'
```

### **3. Verify Demo Mode**
- Form submission should work
- Progress updates should show
- Should receive demo credentials:
  - Phone: `+1 (555) 123-DEMO`
  - Email: `demo@company.justclara.ai`
  - Password: `demo@321`

## 🚨 **Troubleshooting**

### **Common Issues**

#### **404 NOT_FOUND Error**
- **Cause**: Incorrect routing or missing files
- **Solution**: Ensure `vercel.json` is properly configured
- **Check**: All API files exist in `api/` folder

#### **Function Timeout**
- **Cause**: Serverless function taking too long
- **Solution**: Simplified API responses (already implemented)
- **Note**: Demo mode returns immediately

#### **Import Errors**
- **Cause**: Missing dependencies or complex imports
- **Solution**: Simplified imports (already fixed)
- **Check**: `requirements.txt` has all needed packages

#### **CORS Issues**
- **Cause**: Missing CORS headers
- **Solution**: All endpoints include proper CORS headers
- **Check**: Browser network tab for CORS errors

### **Debugging Steps**

1. **Check Vercel Function Logs**
   ```bash
   vercel logs your-project-url
   ```

2. **Test Individual Endpoints**
   ```bash
   # Test each API endpoint separately
   curl https://your-project.vercel.app/api/test
   ```

3. **Verify File Structure**
   ```
   clara-onboarding-website/
   ├── api/
   │   ├── create-agent.py
   │   ├── test.py
   │   └── creation-status/
   │       └── [creation_id].py
   ├── index.html
   ├── vercel.json
   └── requirements.txt
   ```

## 🎯 **Production Deployment Strategy**

### **Recommended Approach**
1. **Use Vercel for Demo/Showcase**
   - Deploy web interface to Vercel for demonstrations
   - Perfect for showing UI/UX to stakeholders
   - No infrastructure setup required

2. **Use Local/Server for Production**
   - Deploy complete system to dedicated server
   - Full database and Retell API integration
   - Real agent creation capabilities

### **Hybrid Setup**
- **Frontend**: Vercel (fast, global CDN)
- **Backend**: Dedicated server with full agent creation
- **Database**: PostgreSQL on dedicated server
- **API**: Point frontend to production API server

## 📊 **Deployment Comparison**

| Feature | Vercel (Demo) | Local Development | Production Server |
|---------|---------------|-------------------|-------------------|
| Web Interface | ✅ Full | ✅ Full | ✅ Full |
| Agent Creation | ❌ Demo only | ✅ Real | ✅ Real |
| Database | ❌ None | ✅ PostgreSQL | ✅ PostgreSQL |
| Phone Numbers | ❌ Demo | ✅ Real | ✅ Real |
| Setup Time | 5 minutes | 10 minutes | 30+ minutes |
| Cost | Free | Free | Server costs |
| Use Case | Demo/Showcase | Development | Production |

## 🔄 **Updating Deployment**

### **Automatic Deployment**
- Vercel automatically redeploys on git push to main branch
- Connect your GitHub repository for automatic deployments

### **Manual Deployment**
```bash
cd clara-onboarding-website
vercel --prod
```

### **Environment Variables**
If you need to add environment variables:
```bash
vercel env add RETELL_API_TOKEN
```

## 🎉 **Success Indicators**

Your Vercel deployment is successful when:
- ✅ **Web interface loads** at your Vercel URL
- ✅ **Form submission works** and shows progress
- ✅ **Demo credentials appear** after completion
- ✅ **No 404 errors** on any routes
- ✅ **API endpoints respond** correctly
- ✅ **Mobile responsive** design works

## 📞 **Support**

If you encounter issues:
1. Check Vercel function logs
2. Verify all files are committed to git
3. Test API endpoints individually
4. Compare with working local development setup

The Vercel deployment provides a perfect demo environment while local development handles actual agent creation!