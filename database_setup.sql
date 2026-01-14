-- =====================================================
-- RETELL AI AGENT AUTOMATION - DATABASE SCHEMA
-- Table creation script for PostgreSQL
-- =====================================================

-- Create the companies table
CREATE TABLE IF NOT EXISTS public.companies (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
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
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT companies_pkey PRIMARY KEY (id)
);

-- Create the company_agent_configs table
CREATE TABLE IF NOT EXISTS public.company_agent_configs (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    company_id uuid NOT NULL,
    llm_id_oh text,
    llm_id_ah text,
    agent_id_oh text,
    agent_id_ah text,
    agent_id_mr text,
    conversation_flow_id text,
    retell_phone_number text,
    retell_phone_number_id text,
    dashboard_email text,
    dashboard_password text,
    status text DEFAULT 'active'::text,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT company_agent_configs_pkey PRIMARY KEY (id),
    CONSTRAINT company_agent_configs_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE
);

-- Create the company_prompts table
CREATE TABLE IF NOT EXISTS public.company_prompts (
    company_id uuid NOT NULL,
    global_prompt text NOT NULL,
    office_hours_prompt text NOT NULL,
    after_hours_prompt text NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT company_prompts_pkey PRIMARY KEY (company_id),
    CONSTRAINT company_prompts_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE
);

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_companies_name ON public.companies(company_name);
CREATE INDEX IF NOT EXISTS idx_agent_configs_company_id ON public.company_agent_configs(company_id);
CREATE INDEX IF NOT EXISTS idx_agent_configs_status ON public.company_agent_configs(status);
CREATE INDEX IF NOT EXISTS idx_agent_configs_dashboard_email ON public.company_agent_configs(dashboard_email);