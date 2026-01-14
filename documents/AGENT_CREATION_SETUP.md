# Clara Agent Creation Setup Guide

## 🎯 Overview

This system creates Retell AI agents through a web interface. The web form collects company information and creates agents in Retell with proper configuration.

## 🔧 Setup Instructions

### 1. Configure API Keys

Update your `.env` file with your Retell API token:

```env
# Retell API Configuration
RETELL_API_TOKEN=your_actual_retell_api_token_here
ORG_ID=your_org_id_here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Choose Your Development Method

#### Option A: Local Development (Recommended)

This runs the agent creation locally where it has access to all your files:

```bash
# Start local development environment
python start_local_development.py
```

This will:
- Start the local agent creation server (port 8000)
- Start the web interface (port 3001)
- Open your browser automatically

#### Option B: Production Deployment

Deploy to Vercel for production use:

```bash
cd clara-onboarding-website
vercel --prod
```

**Note:** The Vercel deployment currently shows a demo response. For actual agent creation, use the local development method.

## 🚀 Usage

1. **Fill out the web form** with company details:
   - Company name (keep it short, max 50 characters)
   - Office address
   - Website URL (must have a valid sitemap)
   - Business hours and timezone
   - Contact information

2. **Submit the form** - The system will:
   - Create a knowledge base from your website
   - Generate LLMs with custom prompts
   - Create office hours and after hours agents
   - Set up conversation flows
   - Purchase a phone number
   - Create dashboard credentials

3. **Monitor progress** - The interface shows real-time status updates

4. **Get results** - Upon completion, you'll receive:
   - Phone number for your agent
   - Dashboard login credentials
   - Agent IDs for Retell

## 🔍 Troubleshooting

### Common Issues

**"Company name too long"**
- Use a shorter company name (max 50 characters)
- Remove special characters
- Try abbreviations

**"Sitemap not found"**
- Ensure your website has a sitemap.xml
- Check that the URL is accessible
- Try a different website URL

**"Unauthorized API error"**
- Verify your Retell API token in `.env`
- Check token permissions
- Ensure token is not expired

**"Agent not reflected in Retell"**
- Make sure you're using the local development method
- Check that the local agent server is running
- Verify API token configuration

### Development vs Production

| Feature | Local Development | Vercel Production |
|---------|------------------|-------------------|
| Agent Creation | ✅ Full functionality | ❌ Demo only |
| Web Interface | ✅ Works | ✅ Works |
| Real-time Status | ✅ Works | ❌ Limited |
| File Access | ✅ Full access | ❌ Restricted |

## 📁 File Structure

```
├── agent_system/              # Core agent creation logic
│   ├── __init__.py           # Module initialization
│   ├── main.py               # Main orchestration logic
│   ├── config.py             # Configuration and constants
│   ├── user_input.py         # CLI input collection
│   ├── knowledge_base.py     # Knowledge base creation
│   ├── llm_creation.py       # LLM creation and configuration
│   ├── agent_creation.py     # Agent and conversation flow creation
│   ├── phone_number.py       # Phone number purchasing
│   ├── database.py           # Database operations
│   ├── dashboard_creation.py # Dashboard credential creation
│   └── validators.py         # Input validation utilities
├── clara-onboarding-website/ # Web interface (pure HTML/CSS/JS)
│   ├── api/                  # Vercel API endpoints
│   ├── src/                  # JavaScript source files
│   ├── styles/               # CSS stylesheets
│   ├── assets/               # Images and static files
│   └── index.html            # Main web interface
├── prompts/                  # Prompt templates
│   ├── global_prompt_template.txt
│   ├── office_hours_prompt_template.txt
│   └── after_hours_prompt_template.txt
├── local_agent_server.py     # Local API server
├── start_local_development.py # Development startup script
├── run_agent_creation.py     # CLI entry point
├── database_setup.sql        # Database schema
├── .env                      # Configuration file
└── requirements.txt          # Python dependencies
```

## 🎯 Next Steps

1. **Test the system** with a sample company
2. **Verify agents** are created in your Retell dashboard
3. **Test phone calls** to ensure everything works
4. **Customize prompts** in the prompts/ folder if needed

## 🚀 Production Deployment Checklist

- [ ] Configure `.env` with production API tokens
- [ ] Test local development environment works
- [ ] Verify all prompt templates are customized for your use case
- [ ] Test complete agent creation workflow
- [ ] Verify phone number purchasing works in your region
- [ ] Test dashboard credentials generation
- [ ] Deploy to Vercel for production web interface (optional)
- [ ] Set up monitoring and logging for production use

## 📋 Maintenance

- **Prompt Updates**: Edit files in `prompts/` folder to customize agent behavior
- **Configuration**: Update `.env` file for API tokens and settings
- **Database**: Use `database_setup.sql` for fresh database setup
- **Monitoring**: Check logs in local development for troubleshooting

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your API configuration
3. Ensure all dependencies are installed
4. Contact support with specific error messages