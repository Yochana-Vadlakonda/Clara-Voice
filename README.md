# Retell AI Agent Automation System

A comprehensive automation system for creating and managing Retell AI voice agents with PostgreSQL integration, knowledge base creation, and intelligent call routing.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           RETELL AI AGENT AUTOMATION SYSTEM                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │    │  Knowledge Base │    │   PostgreSQL    │
│                 │    │                 │    │    Database     │
│ • Company Info  │    │ • Website Crawl │    │                 │
│ • Business Hrs  │    │ • Sitemap Parse │    │ • companies     │
│ • Contact Info  │    │ • Content Index │    │ • agent_configs │
│ • Preferences   │    │                 │    │ • prompts       │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │                         │
                    │    MAIN ORCHESTRATOR    │
                    │   (agent_system/main)   │
                    │                         │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  LLM Creation │    │Agent Creation │    │ Phone Number  │
│               │    │               │    │  Management   │
│ • Office Hrs  │    │ • Office Hrs  │    │               │
│ • After Hrs   │    │ • After Hrs   │    │ • Purchase    │
│ • Prompts     │    │ • Main Router │    │ • Assignment  │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │                 │
                    │ CONVERSATION    │
                    │     FLOW        │
                    │                 │
                    │ • Time-based    │
                    │   Routing       │
                    │ • Agent Swaps   │
                    │ • Branch Logic  │
                    └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              RETELL AI PLATFORM                                │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│      LLMs       │     Agents      │ Conversation    │     Phone Numbers       │
│                 │                 │     Flows       │                         │
│ • Office Hours  │ • Office Hours  │ • Time Logic    │ • Purchased Numbers     │
│ • After Hours   │ • After Hours   │ • Agent Routing │ • Inbound Assignment    │
│                 │ • Main Router   │ • Branch Rules  │ • Area Code Matching    │
└─────────────────┴─────────────────┴─────────────────┴─────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                CALL FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────────┘

    Incoming Call
         │
         ▼
┌─────────────────┐
│  Main Router    │ ◄─── Uses Conversation Flow
│     Agent       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Time Check     │ ◄─── Current time vs Business Hours
│   (Branch)      │
└─────────┬───────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌─────────┐
│ Office  │ │ After   │
│ Hours   │ │ Hours   │
│ Agent   │ │ Agent   │
└─────────┘ └─────────┘
```

## 📚 Documentation

For detailed information, see the documentation in the `documents/` folder:

- **[Setup Guide](documents/AGENT_CREATION_SETUP.md)** - Complete setup and usage instructions
- **[Database Documentation](documents/DATABASE_DOCUMENTATION.md)** - Database schema, setup, and operations  
- **[Improvements Changelog](documents/IMPROVEMENTS_CHANGELOG.md)** - Recent changes and improvements

## 🚀 Quick Start

### Prerequisites

1. **PostgreSQL Database** - Running locally or remotely
2. **Python 3.8+** with required packages
3. **Retell AI Account** with API access
4. **Environment Configuration**

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd retell-agent-automation
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   # Copy and edit .env file
   cp .env.example .env
   # Edit with your database and API credentials
   ```

3. **Setup Database**
   ```bash
   # Run the consolidated database setup
   psql -h localhost -U postgres -d your_db < database_setup.sql
   ```

4. **Start Development Environment**
   ```bash
   # Start both web interface (port 3001) and API server (port 8000)
   python start_local_development.py
   ```

5. **Open Web Interface**
   - Navigate to `http://localhost:3001`
   - Fill out the company information form
   - Monitor real-time agent creation progress

For detailed setup instructions, see [documents/AGENT_CREATION_SETUP.md](documents/AGENT_CREATION_SETUP.md).

## 📁 Project Structure

```
clara-agent-creation/
├── agent_system/                 # Core automation modules
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Main orchestrator
│   ├── user_input.py            # User input collection
│   ├── knowledge_base.py        # Website crawling & KB creation
│   ├── llm_creation.py          # Retell LLM management
│   ├── agent_creation.py        # Agent & conversation flow
│   ├── phone_number.py          # Phone number management
│   ├── database.py              # PostgreSQL operations
│   ├── dashboard_creation.py    # Dashboard credential creation
│   ├── config.py                # Configuration management
│   └── validators.py            # Input validation
├── clara-onboarding-website/    # Web interface (HTML/CSS/JS)
│   ├── api/                     # Vercel API endpoints
│   ├── src/                     # JavaScript source files
│   ├── styles/                  # CSS stylesheets
│   ├── assets/                  # Images and static files
│   └── index.html               # Main web interface
├── documents/                   # Documentation
│   ├── AGENT_CREATION_SETUP.md  # Setup and usage guide
│   ├── DATABASE_DOCUMENTATION.md # Database schema and operations
│   └── IMPROVEMENTS_CHANGELOG.md # Recent changes and improvements
├── prompts/                     # Prompt templates
│   ├── global_prompt_template.txt
│   ├── office_hours_prompt_template.txt
│   └── after_hours_prompt_template.txt
├── local_agent_server.py        # Local development API server
├── start_local_development.py   # Development startup script
├── database_setup.sql           # Complete database schema
├── run_agent_creation.py        # CLI entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# PostgreSQL Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=self_onb
DB_USER=postgres
DB_PASSWORD=your_password

# Retell AI API (configure in agent_system/config.py)
RETELL_API_TOKEN=your_retell_api_token
```

### Retell AI Configuration

Update `agent_system/config.py` with your Retell AI credentials:

```python
RETELL_API_TOKEN = "your_retell_api_token_here"
```

## 🎯 Core Features

### 1. **Automated Agent Creation**
- Creates Office Hours and After Hours LLMs
- Generates specialized agents for each scenario
- Sets up Main Router agent with conversation flow
- Automatic agent publishing and versioning

### 2. **Intelligent Call Routing**
- Time-based routing using conversation flows
- Business hours detection with timezone support
- Seamless agent transfers based on availability
- Branch logic for complex routing scenarios

### 3. **Knowledge Base Integration**
- Automatic website crawling and sitemap parsing
- Knowledge base creation from company websites
- Content indexing for accurate AI responses
- Integration with Retell LLM knowledge systems

### 4. **Phone Number Management**
- Automatic phone number purchasing
- Area code matching and fallback logic
- Inbound call assignment to router agents
- Phone number lifecycle management

### 5. **Database Persistence**
- Complete configuration storage in PostgreSQL
- Relationship management between entities
- Audit trails with timestamps
- Data integrity with foreign key constraints

## 📊 Database Schema

### Tables Overview

1. **companies** - Core company information
   - Basic details (name, address, contact)
   - Business hours (JSONB format)
   - Timezone and area code information
   - Knowledge base references
   - Post-call summary preferences

2. **company_agent_configs** - Retell AI configurations
   - LLM IDs (office hours, after hours)
   - Agent IDs (office hours, after hours, main router)
   - Conversation flow IDs
   - Phone number assignments
   - Status tracking

3. **company_prompts** - AI assistant prompts
   - Global prompt (base instructions)
   - Office hours specific prompt
   - After hours specific prompt
   - Timestamp tracking

### Key Relationships

```sql
companies (1) ──── (1) company_prompts
    │
    └── (1) ──── (1) company_agent_configs
```

## 🔄 Automation Workflow

### Step-by-Step Process

1. **User Input Collection**
   - Company details and preferences
   - Business hours and timezone
   - Contact information and website
   - Post-call summary preferences

2. **Knowledge Base Creation**
   - Website sitemap crawling
   - Content extraction and indexing
   - Knowledge base generation in Retell AI

3. **LLM Creation**
   - Generate specialized prompts for each scenario
   - Create Office Hours and After Hours LLMs
   - Link knowledge bases to LLMs

4. **Agent Creation**
   - Create Office Hours agent (LLM-based)
   - Create After Hours agent (LLM-based)
   - Auto-publish agents with version 0

5. **Conversation Flow Setup**
   - Create time-based routing logic
   - Configure branch conditions
   - Set up agent transfer rules

6. **Main Router Creation**
   - Create router agent using conversation flow
   - Configure as entry point for all calls
   - Auto-publish with version 0

7. **Phone Number Management**
   - Purchase phone number with area code preference
   - Assign inbound calls to router agent
   - Configure number settings

8. **Database Persistence**
   - Save all configurations to PostgreSQL
   - Maintain relationships between entities
   - Store prompts and metadata

## 🎮 Usage Examples

### Basic Company Setup

```bash
python run_agent_creation.py
```

**Interactive Prompts:**
```
Company Name: Acme Medical Center
Office Address: 123 Healthcare Ave, Medical City, MC 12345
Contact Number: +1-555-MEDICAL
Time Zone: America/New_York
Website URL: https://acme-medical.com
Business Hours: {"monday":{"open":"08:00","close":"17:00"},...}
```

### Advanced Configuration

For custom prompts and specialized scenarios, modify the templates:
- `global_prompt_template.txt` - Base instructions
- `office_hours_prompt_template.txt` - Open hours behavior
- `after_hours_prompt_template.txt` - Closed hours behavior

### Database Operations

```bash
# View recent companies
python -c "from agent_system.database import *; # custom query here"

# Clear all data (use with caution)
psql -h localhost -U postgres -d self_onb < database_setup.sql
```

## 🔍 Monitoring and Debugging

### Database Queries

```sql
-- View all companies with their configurations
SELECT 
    c.company_name,
    c.created_at,
    cac.agent_id_oh,
    cac.agent_id_ah,
    cac.agent_id_mr,
    cac.retell_phone_number
FROM companies c
LEFT JOIN company_agent_configs cac ON c.id = cac.company_id
ORDER BY c.created_at DESC;

-- Check system health
SELECT 
    'companies' as table_name, 
    COUNT(*) as record_count 
FROM companies
UNION ALL
SELECT 'agent_configs', COUNT(*) FROM company_agent_configs
UNION ALL
SELECT 'prompts', COUNT(*) FROM company_prompts;
```

### Common Issues

1. **Database Connection Errors**
   - Verify PostgreSQL is running
   - Check credentials in `.env`
   - Ensure database exists

2. **Retell API Failures**
   - Verify API token in `config.py`
   - Check Retell AI account limits
   - Review API response errors

3. **Knowledge Base Creation Issues**
   - Ensure website is accessible
   - Check sitemap.xml availability
   - Verify content extraction

## 🚀 Deployment

### Production Considerations

1. **Security**
   - Use environment variables for all secrets
   - Implement proper database access controls
   - Secure API token storage

2. **Scalability**
   - Consider connection pooling for database
   - Implement rate limiting for Retell API calls
   - Add monitoring and logging

3. **Backup and Recovery**
   - Regular database backups
   - Configuration export/import
   - Disaster recovery procedures

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run_agent_creation.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:

1. **Database Issues**: Check PostgreSQL logs and connection settings
2. **Retell AI Issues**: Verify API credentials and check Retell documentation
3. **System Issues**: Review logs and error messages
4. **Feature Requests**: Submit an issue with detailed requirements

## 🔮 Roadmap

- [ ] Web-based configuration interface
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Integration with CRM systems
- [ ] Automated testing framework
- [ ] Performance optimization
- [ ] Cloud deployment templates

---

**Built with ❤️ for seamless Retell AI automation**#   P r o d u c t i o n _ V o i c e _ C l a r a  
 