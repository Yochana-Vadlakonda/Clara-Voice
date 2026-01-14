# Database Documentation

## 🗄️ Overview

The Clara Agent Creation System uses PostgreSQL as its primary database to store company information, agent configurations, and system metadata. This document provides comprehensive information about the database schema, setup, and operations.

## 📊 Database Schema

### Tables Overview

The system uses three main tables with proper relationships and constraints:

1. **companies** - Core company information
2. **company_agent_configs** - Agent configuration and credentials
3. **company_prompts** - Custom prompts for each company

### Table Structures

#### 1. companies
Stores basic company information and business details.

```sql
CREATE TABLE public.companies (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name text NOT NULL UNIQUE,
    office_address text NOT NULL,
    business_hours jsonb NOT NULL,
    contact_number text NOT NULL,
    area_code text NOT NULL,
    website_url text,
    time_zone text NOT NULL,
    knowledge_base_id text,
    needs_prompt_regeneration boolean DEFAULT true,
    post_call_summary_sms boolean DEFAULT false,
    post_call_summary_email boolean DEFAULT false,
    summary_sms_number text,
    summary_email_address text,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);
```

**Key Fields:**
- `id`: Unique identifier (UUID)
- `company_name`: Must be unique across system
- `business_hours`: JSON structure containing schedule
- `knowledge_base_id`: Links to Retell knowledge base
- `time_zone`: Used for business hours logic

#### 2. company_agent_configs
Stores all Retell AI agent configurations and credentials.

```sql
CREATE TABLE public.company_agent_configs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id uuid NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    llm_id_oh text,           -- Office Hours LLM ID
    llm_id_ah text,           -- After Hours LLM ID
    agent_id_oh text,         -- Office Hours Agent ID
    agent_id_ah text,         -- After Hours Agent ID
    agent_id_mr text,         -- Main Router Agent ID
    conversation_flow_id text,
    retell_phone_number text,
    retell_phone_number_id text,
    dashboard_email text,
    dashboard_password text,
    status text DEFAULT 'active',
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);
```

**Key Fields:**
- `company_id`: Foreign key to companies table
- `llm_id_*`: Retell LLM identifiers for different scenarios
- `agent_id_*`: Retell Agent identifiers
- `retell_phone_number`: Purchased phone number
- `dashboard_*`: Login credentials for company dashboard

#### 3. company_prompts
Stores custom prompts generated for each company.

```sql
CREATE TABLE public.company_prompts (
    company_id uuid PRIMARY KEY REFERENCES companies(id) ON DELETE CASCADE,
    global_prompt text NOT NULL,
    office_hours_prompt text NOT NULL,
    after_hours_prompt text NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);
```

**Key Fields:**
- `company_id`: Primary key and foreign key to companies
- `*_prompt`: Generated prompts for different scenarios

### Indexes

Performance optimization indexes:

```sql
CREATE INDEX idx_companies_name ON companies(company_name);
CREATE INDEX idx_agent_configs_company_id ON company_agent_configs(company_id);
CREATE INDEX idx_agent_configs_status ON company_agent_configs(status);
CREATE INDEX idx_agent_configs_dashboard_email ON company_agent_configs(dashboard_email);
```

## 🔧 Database Setup

### Prerequisites

1. **PostgreSQL 12+** installed and running
2. **Database created** for the application
3. **User with proper permissions** to create tables and indexes

### Setup Steps

1. **Create Database**
   ```bash
   createdb -U postgres clara_agents
   ```

2. **Run Schema Setup**
   ```bash
   psql -h localhost -U postgres -d clara_agents < database_setup.sql
   ```

3. **Verify Setup**
   ```sql
   \dt  -- List tables
   \d companies  -- Describe companies table
   ```

### Environment Configuration

Update your `.env` file with database credentials:

```env
# PostgreSQL Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clara_agents
DB_USER=postgres
DB_PASSWORD=your_password
```

## 🔄 Database Operations

### Connection Management

The system uses `psycopg2` for database connections:

```python
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)
```

### Data Flow

1. **Company Creation**
   - Insert into `companies` table
   - Generate UUID for company_id
   - Store business hours as JSONB

2. **Agent Configuration**
   - Create LLMs in Retell
   - Store LLM IDs in `company_agent_configs`
   - Create agents and conversation flows
   - Store all Retell identifiers

3. **Prompt Storage**
   - Generate custom prompts from templates
   - Store in `company_prompts` table
   - Link to company via company_id

### Common Queries

#### Get Company with All Configurations
```sql
SELECT 
    c.*,
    cac.*,
    cp.global_prompt,
    cp.office_hours_prompt,
    cp.after_hours_prompt
FROM companies c
LEFT JOIN company_agent_configs cac ON c.id = cac.company_id
LEFT JOIN company_prompts cp ON c.id = cp.company_id
WHERE c.company_name = 'Example Company';
```

#### Get Active Agents
```sql
SELECT 
    c.company_name,
    cac.retell_phone_number,
    cac.dashboard_email,
    cac.status
FROM companies c
JOIN company_agent_configs cac ON c.id = cac.company_id
WHERE cac.status = 'active';
```

#### Update Company Status
```sql
UPDATE company_agent_configs 
SET status = 'inactive', updated_at = now()
WHERE company_id = (
    SELECT id FROM companies WHERE company_name = 'Example Company'
);
```

## 🛠️ Maintenance

### Backup Strategy

1. **Regular Backups**
   ```bash
   pg_dump -h localhost -U postgres clara_agents > backup_$(date +%Y%m%d).sql
   ```

2. **Restore from Backup**
   ```bash
   psql -h localhost -U postgres clara_agents < backup_20260110.sql
   ```

### Data Cleanup

1. **Remove Test Data**
   ```sql
   DELETE FROM companies WHERE company_name LIKE 'Test%';
   ```

2. **Archive Old Records**
   ```sql
   UPDATE company_agent_configs 
   SET status = 'archived' 
   WHERE created_at < now() - interval '1 year';
   ```

### Performance Monitoring

1. **Check Table Sizes**
   ```sql
   SELECT 
       schemaname,
       tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
   FROM pg_tables 
   WHERE schemaname = 'public';
   ```

2. **Monitor Query Performance**
   ```sql
   SELECT query, calls, total_time, mean_time 
   FROM pg_stat_statements 
   ORDER BY total_time DESC 
   LIMIT 10;
   ```

## 🔒 Security Considerations

### Access Control

1. **Database User Permissions**
   - Create dedicated user for application
   - Grant only necessary permissions
   - Use connection pooling

2. **Data Encryption**
   - Encrypt sensitive fields (passwords, phone numbers)
   - Use SSL connections in production
   - Regular security audits

### Best Practices

1. **Connection Security**
   ```python
   # Use environment variables for credentials
   DB_CONFIG = {
       'host': os.getenv('DB_HOST'),
       'port': os.getenv('DB_PORT'),
       'database': os.getenv('DB_NAME'),
       'user': os.getenv('DB_USER'),
       'password': os.getenv('DB_PASSWORD'),
       'sslmode': 'require'  # For production
   }
   ```

2. **Input Validation**
   - Sanitize all inputs before database operations
   - Use parameterized queries
   - Validate data types and constraints

## 🚨 Troubleshooting

### Common Issues

1. **Connection Errors**
   - Check PostgreSQL service status
   - Verify credentials in `.env`
   - Test network connectivity

2. **Permission Errors**
   - Ensure user has CREATE, INSERT, UPDATE, DELETE permissions
   - Check table ownership
   - Verify schema access

3. **Performance Issues**
   - Analyze slow queries with EXPLAIN
   - Check index usage
   - Monitor connection pool

### Error Codes

- `23505`: Unique constraint violation (duplicate company name)
- `23503`: Foreign key constraint violation
- `42P01`: Table does not exist
- `28P01`: Authentication failed

## 📈 Scaling Considerations

### Horizontal Scaling

1. **Read Replicas**
   - Set up read-only replicas for reporting
   - Route read queries to replicas
   - Monitor replication lag

2. **Connection Pooling**
   - Use pgBouncer or similar
   - Configure appropriate pool sizes
   - Monitor connection usage

### Vertical Scaling

1. **Hardware Optimization**
   - Increase RAM for better caching
   - Use SSDs for faster I/O
   - Optimize PostgreSQL configuration

2. **Query Optimization**
   - Regular VACUUM and ANALYZE
   - Monitor and optimize slow queries
   - Consider partitioning for large tables

## 📊 Monitoring and Alerts

### Key Metrics

1. **Database Health**
   - Connection count
   - Query response times
   - Disk usage
   - Replication lag

2. **Application Metrics**
   - Agent creation success rate
   - Failed database operations
   - Data consistency checks

### Alerting

Set up alerts for:
- High connection count
- Slow query performance
- Disk space usage > 80%
- Failed backup operations
- Replication issues

## 🔄 Migration Strategy

### Schema Changes

1. **Version Control**
   - Track all schema changes in version control
   - Use migration scripts for updates
   - Test migrations in staging environment

2. **Deployment Process**
   ```bash
   # Backup before migration
   pg_dump clara_agents > pre_migration_backup.sql
   
   # Run migration
   psql clara_agents < migration_v2.sql
   
   # Verify migration
   psql clara_agents -c "SELECT version FROM schema_version;"
   ```

### Data Migration

1. **Large Data Sets**
   - Use COPY for bulk operations
   - Process in batches to avoid locks
   - Monitor progress and performance

2. **Zero-Downtime Migrations**
   - Use blue-green deployment strategy
   - Implement backward-compatible changes
   - Plan rollback procedures