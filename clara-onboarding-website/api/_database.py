#!/usr/bin/env python3
"""
Simplified Database Connection Module
Works with existing PostgreSQL schema only
"""

import psycopg2
import psycopg2.extras
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from _config import config

class DatabaseError(Exception):
    """Database operation error"""
    pass

class DatabaseManager:
    """Simplified database manager using existing schema only"""
    
    def __init__(self):
        self.db_config = config.db_config
        
    @contextmanager
    def get_connection(self):
        """Get database connection with proper cleanup"""
        conn = None
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.autocommit = False
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise DatabaseError(f"Database connection error: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False) -> Optional[List[Dict]]:
        """Execute query with proper error handling"""
        with self.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    cursor.execute(query, params)
                    
                    if fetch:
                        result = cursor.fetchall()
                        return [dict(row) for row in result]
                    else:
                        conn.commit()
                        return None
                        
            except Exception as e:
                conn.rollback()
                raise DatabaseError(f"Query execution error: {str(e)}")
    
    def create_company(self, company_data: Dict) -> str:
        """Create company record using existing schema"""
        query = """
        INSERT INTO companies (
            company_name, office_address, business_hours, 
            contact_number, area_code, website_url, time_zone
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (company_name) DO UPDATE SET
            updated_at = NOW(),
            office_address = EXCLUDED.office_address,
            business_hours = EXCLUDED.business_hours,
            contact_number = EXCLUDED.contact_number,
            area_code = EXCLUDED.area_code,
            website_url = EXCLUDED.website_url,
            time_zone = EXCLUDED.time_zone
        RETURNING id
        """
        
        # Format business hours as JSON
        business_hours_json = {
            "hours": company_data['business_hours'],
            "timezone": company_data['timezone']
        }
        
        result = self.execute_query(query, (
            company_data['company_name'],
            company_data['business_address'],
            json.dumps(business_hours_json),
            company_data['primary_phone_number'],
            company_data['preferred_area_code'],
            company_data['website_url'],
            company_data['timezone']
        ), fetch=True)
        
        return str(result[0]['id'])
    
    def update_company_kb(self, company_id: str, knowledge_base_id: str):
        """Update company with knowledge base ID"""
        query = """
        UPDATE companies 
        SET knowledge_base_id = %s, updated_at = NOW()
        WHERE id = %s
        """
        
        self.execute_query(query, (knowledge_base_id, company_id))
    
    def create_agent_config(self, company_id: str, config_data: Dict) -> str:
        """Create agent configuration using existing schema"""
        query = """
        INSERT INTO company_agent_configs (
            company_id, llm_id_oh, llm_id_ah, agent_id_oh, agent_id_ah, agent_id_mr,
            conversation_flow_id, retell_phone_number, retell_phone_number_id,
            dashboard_email, dashboard_password
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (company_id) DO UPDATE SET
            llm_id_oh = EXCLUDED.llm_id_oh,
            llm_id_ah = EXCLUDED.llm_id_ah,
            agent_id_oh = EXCLUDED.agent_id_oh,
            agent_id_ah = EXCLUDED.agent_id_ah,
            agent_id_mr = EXCLUDED.agent_id_mr,
            conversation_flow_id = EXCLUDED.conversation_flow_id,
            retell_phone_number = EXCLUDED.retell_phone_number,
            retell_phone_number_id = EXCLUDED.retell_phone_number_id,
            dashboard_email = EXCLUDED.dashboard_email,
            dashboard_password = EXCLUDED.dashboard_password,
            updated_at = NOW()
        RETURNING id
        """
        
        result = self.execute_query(query, (
            company_id,
            config_data.get('llm_id_oh'),
            config_data.get('llm_id_ah'),
            config_data.get('agent_id_oh'),
            config_data.get('agent_id_ah'),
            config_data.get('agent_id_mr'),
            config_data.get('conversation_flow_id'),
            config_data.get('retell_phone_number'),
            config_data.get('retell_phone_number_id'),
            config_data.get('dashboard_email'),
            config_data.get('dashboard_password')
        ), fetch=True)
        
        return str(result[0]['id'])
    
    def create_prompts(self, company_id: str, prompts: Dict):
        """Create prompts using existing schema"""
        query = """
        INSERT INTO company_prompts (
            company_id, global_prompt, office_hours_prompt, after_hours_prompt
        ) VALUES (%s, %s, %s, %s)
        ON CONFLICT (company_id) DO UPDATE SET
            global_prompt = EXCLUDED.global_prompt,
            office_hours_prompt = EXCLUDED.office_hours_prompt,
            after_hours_prompt = EXCLUDED.after_hours_prompt,
            updated_at = NOW()
        """
        
        self.execute_query(query, (
            company_id,
            prompts['global_prompt'],
            prompts['office_hours_prompt'],
            prompts['after_hours_prompt']
        ))
    
    def get_company_by_name(self, company_name: str) -> Optional[Dict]:
        """Get company by name"""
        query = """
        SELECT * FROM companies WHERE company_name = %s
        """
        
        result = self.execute_query(query, (company_name,), fetch=True)
        return result[0] if result else None
    
    def get_company_config(self, company_id: str) -> Optional[Dict]:
        """Get company agent configuration"""
        query = """
        SELECT c.*, ac.*, cp.global_prompt, cp.office_hours_prompt, cp.after_hours_prompt
        FROM companies c
        LEFT JOIN company_agent_configs ac ON c.id = ac.company_id
        LEFT JOIN company_prompts cp ON c.id = cp.company_id
        WHERE c.id = %s
        """
        
        result = self.execute_query(query, (company_id,), fetch=True)
        return result[0] if result else None

# Global database manager instance
db = DatabaseManager()