# Clara AI Voice Agent - Vercel Deployment

A production-ready web application for creating AI voice agents using Retell AI platform. This system allows users to create custom voice assistants with knowledge bases, proper credentials, and phone number integration.

## 🚀 Features

- **Real Agent Creation**: Creates actual Retell AI agents with knowledge bases
- **Demo Mode**: Full preview without API requirements
- **Robust Error Handling**: Comprehensive error handling and validation
- **Responsive Design**: Works on all devices
- **Production Ready**: Optimized for Vercel deployment

## 📋 Prerequisites

- Vercel account
- Retell AI API token (for real agent creation)

## 🔧 Vercel Deployment Setup

### 1. Environment Variables

Add these environment variables in your Vercel dashboard:

**Required for Real Agent Creation:**
- `RETELL_API_TOKEN`: Your Retell AI API token

**Optional:**
- `ORG_ID`: Organization ID (only if required by your Retell account)

### 2. Deploy to Vercel

```bash
# Clone the repository
git clone <your-repo-url>
cd clara-onboarding-website

# Deploy to Vercel
vercel --prod
```

### 3. Configure Environment Variables

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add `RETELL_API_TOKEN` with your API token
5. Redeploy the project

## 🏗️ Project Structure

```
clara-onboarding-website/
├── api/                          # Vercel serverless functions
│   ├── create-agent.py          # Agent creation endpoint
│   └── creation-status/         # Status checking endpoint
│       └── [creation_id].py
├── src/                         # Frontend JavaScript
│   └── main.js                  # Main application logic
├── styles/                      # CSS stylesheets
│   └── main.css
├── assets/                      # Static assets
│   └── clara_black.png
├── index.html                   # Main HTML file
├── vercel.json                  # Vercel configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔄 How It Works

### Demo Mode (Default)
- No API token required
- Shows complete user experience
- Generates realistic demo credentials
- Perfect for showcasing the system

### Real Mode (With API Token)
- Creates actual Retell AI agents
- Generates knowledge bases from websites
- Creates LLMs with custom prompts
- Returns real agent IDs and credentials

## 🛠️ API Endpoints

### POST `/api/create-agent`
Starts agent creation process.

**Request Body:**
```json
{
  "companyName": "Your Company",
  "officeAddress": "123 Main St, City, State",
  "websiteUrl": "https://yourwebsite.com",
  "timeZone": "Eastern",
  "businessHours": "9:00 AM - 5:00 PM",
  "contactNumber": "+1 (555) 123-4567",
  "assistantName": "Clara"
}
```

**Response:**
```json
{
  "success": true,
  "creation_id": "real_1234567890_...",
  "message": "Agent creation started",
  "demo_mode": false
}
```

### GET `/api/creation-status/{creation_id}`
Checks agent creation status.

**Response:**
```json
{
  "success": true,
  "status": "completed",
  "progress": 100,
  "message": "Agent creation completed successfully!",
  "result": {
    "phone_number": "+1 (555) 123-4567",
    "dashboard_credentials": {
      "email": "supportcompany@justclara.ai",
      "password": "company@321"
    },
    "agent_id": "agent_...",
    "llm_id": "llm_...",
    "knowledge_base_id": "kb_..."
  },
  "demo_mode": false
}
```

## 🔒 Security Features

- **Input Validation**: All inputs are validated and sanitized
- **Error Handling**: Comprehensive error handling prevents crashes
- **Rate Limiting**: Built-in protection against abuse
- **CORS Protection**: Proper CORS headers for security
- **Data Sanitization**: All user data is properly sanitized

## 🚨 Error Handling

The system includes robust error handling for:
- Invalid JSON data
- Base64 decoding errors
- API timeout issues
- Network connectivity problems
- Invalid API responses
- Malformed creation IDs

## 📊 Monitoring

### Success Indicators
- ✅ Website loads without errors
- ✅ Form submission works
- ✅ Agent creation completes
- ✅ Credentials are generated correctly

### Common Issues & Solutions

**404 Errors:**
- Check Vercel deployment status
- Verify `vercel.json` configuration
- Ensure all files are properly deployed

**Agent Creation Fails:**
- Verify `RETELL_API_TOKEN` is set correctly
- Check API token permissions
- Ensure website URL is accessible

**Timeout Errors:**
- Knowledge base creation may take time
- System will retry automatically
- Check Retell API status

## 🔧 Development

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run local development server
python -m http.server 8000
```

### File Structure Guidelines
- Keep API functions under 10MB
- Limit encoded data to prevent URL issues
- Use proper error handling in all functions
- Follow Vercel serverless function best practices

## 📈 Performance Optimization

- **Minimal Dependencies**: Only essential packages included
- **Efficient Encoding**: Optimized data encoding for URLs
- **Error Recovery**: Graceful degradation on failures
- **Timeout Handling**: Proper timeout management for API calls

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] API token tested and working
- [ ] All error scenarios handled
- [ ] CORS headers properly set
- [ ] No sensitive data in code
- [ ] Proper logging implemented
- [ ] Performance optimized

## 📞 Support

For issues or questions:
1. Check the troubleshooting tips in error messages
2. Verify environment variable configuration
3. Check Vercel deployment logs
4. Ensure Retell API service is operational

---

**Built for Vercel deployment with production-grade reliability and error handling.**