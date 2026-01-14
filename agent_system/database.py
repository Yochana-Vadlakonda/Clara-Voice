#!/usr/bin/env python3
"""
Database Operations
Handle all database connections and operations
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
import json
from datetime import datetime
from .config import DB_CONFIG


def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)


def save_company_data(company_data, knowledge_base_id, agent_data, llm_data, conversation_flow_id, router_agent_data, phone_data=None, dashboard_data=None):
    """Save all configuration to database"""
    print(f"💾 Saving to database")
    
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            company_id = str(uuid.uuid4())
            now = datetime.now()
            
            # Save company with knowledge base ID
            business_hours_json = {
                "description": company_data['business_hours'],
                "timezone": f"America/{company_data['time_place']}",
                "note": "Converted from text input"
            }
            
            cur.execute("""
                INSERT INTO companies (
                    id, company_name, office_address, business_hours, 
                    contact_number, area_code, website_url, time_zone, knowledge_base_id,
                    post_call_summary_sms, post_call_summary_email, 
                    summary_sms_number, summary_email_address,
                    needs_prompt_regeneration, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """, (
                company_id,
                company_data['company_name'],
                company_data['office_address'],
                json.dumps(business_hours_json),
                company_data['contact_number'],
                company_data['area_code'],
                company_data['website_url'],
                f"America/{company_data['time_place']}",
                knowledge_base_id,
                company_data['post_call_summary_sms'],
                company_data['post_call_summary_email'],
                company_data['summary_sms_number'],
                company_data['summary_email_address'],
                False,
                now,
                now
            ))
            
            company = dict(cur.fetchone())
            
            # Save agent configuration with Main Router Agent and phone number
            config_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO company_agent_configs (
                    id, company_id, llm_id_oh, llm_id_ah, 
                    agent_id_oh, agent_id_ah, agent_id_mr,
                    conversation_flow_id, retell_phone_number, retell_phone_number_id,
                    dashboard_email, dashboard_password,
                    status, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                config_id,
                company_id,
                agent_data['office_hours']['llm_id'],
                agent_data['after_hours']['llm_id'],
                agent_data['office_hours']['agent_id'],
                agent_data['after_hours']['agent_id'],
                router_agent_data['agent_id'],
                conversation_flow_id,
                phone_data['phone_number'] if phone_data else None,
                phone_data['phone_number_id'] if phone_data else None,
                dashboard_data['email'] if dashboard_data and dashboard_data.get('success') else None,
                dashboard_data['password'] if dashboard_data and dashboard_data.get('success') else None,
                'active',
                now,
                now
            ))
            
            # Save prompts
            from .llm_creation import generate_global_prompt
            global_prompt = generate_global_prompt(company_data)
            cur.execute("""
                INSERT INTO company_prompts (
                    company_id, global_prompt, office_hours_prompt, 
                    after_hours_prompt, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                company_id,
                global_prompt,
                llm_data['office_hours']['prompt'],
                llm_data['after_hours']['prompt'],
                now,
                now
            ))
            
            conn.commit()
            print(f"✅ All data saved to database")
            if phone_data:
                print(f"✅ Phone number {phone_data['phone_number']} saved to database")
            if dashboard_data and dashboard_data.get('success'):
                print(f"✅ Dashboard credentials saved to database")
            
            return company_id
            
    except Exception as e:
        conn.rollback()
        print(f"❌ Database error: {e}")
        raise
    finally:
        conn.close()