#!/usr/bin/env python3
"""
Simplified Production Onboarding Engine
Works with existing database schema - no complex session tracking
"""

import time
import json
import re
import requests
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from _config import config
from _database import db, DatabaseError

class OnboardingError(Exception):
    """Onboarding workflow error"""
    pass

class OnboardingEngine:
    """Simplified onboarding engine using existing database schema"""
    
    def __init__(self):
        self.retell_headers = {
            "Authorization": f"Bearer {config.retell_api_token}",
            "Content-Type": "application/json"
        }
    
    def start_onboarding(self, input_data: Dict) -> str:
        """Start new onboarding workflow - returns company_id as session_id"""
        # Validate input data
        self._validate_input_data(input_data)
        
        # Create company record immediately
        company_id = db.create_company(input_data)
        
        if config.diagnostics_enabled:
            print(f"🚀 Started onboarding for company: {company_id}")
        
        return company_id
    
    def execute_full_onboarding(self, company_id: str, input_data: Dict) -> Dict:
        """Execute complete onboarding workflow in one go"""
        start_time = time.time()
        results = {}
        
        try:
            if config.diagnostics_enabled:
                print(f"🔄 Starting full onboarding for company: {company_id}")
            
            # Step 1: Create Knowledge Base
            if config.diagnostics_enabled:
                print("📚 Creating knowledge base...")
            kb_result = self._create_knowledge_base(company_id, input_data)
            results['knowledge_base'] = kb_result
            
            # Step 2: Generate Prompts
            if config.diagnostics_enabled:
                print("📝 Generating prompts...")
            prompts = self._generate_prompts(company_id, input_data)
            results['prompts'] = prompts
            
            # Step 3: Create LLMs
            if config.diagnostics_enabled:
                print("🧠 Creating LLMs...")
            llms = self._create_llms(company_id, input_data, prompts, kb_result['knowledge_base_id'])
            results['llms'] = llms
            
            # Step 4: Create Agents
            if config.diagnostics_enabled:
                print("🤖 Creating agents...")
            agents = self._create_agents(company_id, input_data, llms)
            results['agents'] = agents
            
            # Step 5: Purchase Phone Number
            if config.diagnostics_enabled:
                print("📞 Purchasing phone number...")
            phone_result = self._purchase_phone_number(company_id, input_data, agents['main_router'])
            results['phone'] = phone_result
            
            # Step 6: Create Dashboard Account
            if config.diagnostics_enabled:
                print("🔐 Creating dashboard account...")
            dashboard = self._create_dashboard_account(company_id, input_data)
            results['dashboard'] = dashboard
            
            # Step 7: Save Complete Configuration
            if config.diagnostics_enabled:
                print("💾 Saving configuration...")
            config_data = {
                'llm_id_oh': llms['office_hours'],
                'llm_id_ah': llms['after_hours'],
                'agent_id_oh': agents['office_hours'],
                'agent_id_ah': agents['after_hours'],
                'agent_id_mr': agents['main_router'],
                'retell_phone_number': phone_result['phone_number'],
                'retell_phone_number_id': phone_result['phone_number_id'],
                'dashboard_email': dashboard['dashboard_email'],
                'dashboard_password': dashboard['dashboard_password']
            }
            
            agent_config_id = db.create_agent_config(company_id, config_data)
            results['agent_config_id'] = agent_config_id
            
            # Calculate total duration
            duration_ms = int((time.time() - start_time) * 1000)
            
            if config.diagnostics_enabled:
                print(f"✅ Onboarding completed in {duration_ms}ms")
            
            return {
                'success': True,
                'company_id': company_id,
                'duration_ms': duration_ms,
                'results': results
            }
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_message = str(e)[:500]
            
            if config.diagnostics_enabled:
                print(f"❌ Onboarding failed after {duration_ms}ms: {error_message}")
            
            return {
                'success': False,
                'company_id': company_id,
                'error': error_message,
                'duration_ms': duration_ms,
                'partial_results': results
            }
    
    def _validate_input_data(self, data: Dict) -> Dict:
        """Validate input data structure"""
        required_fields = [
            'company_name', 'assistant_name', 'business_address',
            'timezone', 'business_hours', 'website_url',
            'primary_phone_number', 'preferred_area_code'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not data.get(field, '').strip():
                missing_fields.append(field)
        
        if missing_fields:
            raise OnboardingError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate URL format
        website_url = data['website_url'].strip()
        if not website_url.startswith(('http://', 'https://')):
            data['website_url'] = f"https://{website_url}"
        
        # Validate phone number format
        phone = re.sub(r'[^\d]', '', data['primary_phone_number'])
        if len(phone) != 10 and len(phone) != 11:
            raise OnboardingError("Primary phone number must be 10 or 11 digits")
        
        return {'validation': 'passed', 'normalized_data': data}
    
    def _create_knowledge_base(self, company_id: str, data: Dict) -> Dict:
        """Create knowledge base from website URL"""
        try:
            website_url = data['website_url']
            company_name = data['company_name']
            
            kb_data = {
                "knowledge_base_name": f"{company_name[:30]} KB",
                "website_url": website_url
            }
            
            response = requests.post(
                config.retell_urls['knowledge_base'],
                headers=self.retell_headers,
                json=kb_data,
                timeout=60
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                knowledge_base_id = result.get('knowledge_base_id')
                
                if not knowledge_base_id:
                    raise OnboardingError("No knowledge_base_id returned from API")
                
                # Update company record
                db.update_company_kb(company_id, knowledge_base_id)
                
                return {
                    'knowledge_base_id': knowledge_base_id,
                    'website_url': website_url,
                    'pages_processed': result.get('pages_processed', 0)
                }
            else:
                raise OnboardingError(f"KB API returned {response.status_code}: {response.text[:200]}")
                
        except requests.RequestException as e:
            raise OnboardingError(f"KB creation network error: {str(e)}")
        except Exception as e:
            raise OnboardingError(f"KB creation failed: {str(e)}")
    
    def _generate_prompts(self, company_id: str, data: Dict) -> Dict:
        """Generate standardized voice agent prompts"""
        company_name = data['company_name']
        assistant_name = data['assistant_name']
        timezone = data['timezone']
        business_hours = data['business_hours']
        allow_emergency = data.get('allow_emergency_transfer', False)
        
        # Generate global prompt
        global_prompt = f"""You are {assistant_name}, the professional AI assistant for {company_name}.

GREETING: "Hello, welcome to {company_name}, this is {assistant_name}, how may I assist you today?"

CORE BEHAVIOR:
- Capture caller intent at the beginning and do NOT ask again
- Confirm intent once: "Just to confirm, you're calling about ___ — anything else to add?"
- Handle emergencies: stay calm, collect critical info, offer transfer if available
- Never confirm technician availability; only collect requests
- Speak phone numbers, pin codes, and addresses digit-by-digit
- Use professional tone with light fillers (okay, alright, got it) but not excessive
- Use {timezone} timezone for time-based greetings
- Work within business hours: {business_hours}

EMERGENCY HANDLING: {"Transfer available if needed" if allow_emergency else "Collect details and promise callback"}

Only use information from the knowledge base. Do not make up company offerings."""

        # Generate office hours prompt
        office_hours_prompt = f"""{global_prompt}

OFFICE HOURS MODE:
- Handle normal business calls during {business_hours}
- Schedule appointments and service requests
- Provide information from knowledge base
- Transfer to appropriate department if configured
- Capture complete caller information for follow-up"""

        # Generate after hours prompt  
        after_hours_prompt = f"""{global_prompt}

AFTER HOURS MODE:
- Acknowledge it's after business hours ({business_hours})
- Take detailed messages for next business day callback
- Handle true emergencies with calm professionalism
- {"Offer emergency transfer if critical situation" if allow_emergency else "Advise on emergency procedures"}
- Promise callback during next business hours"""

        prompts = {
            'global_prompt': global_prompt,
            'office_hours_prompt': office_hours_prompt,
            'after_hours_prompt': after_hours_prompt
        }
        
        # Store prompts in database
        db.create_prompts(company_id, prompts)
        
        return prompts
    
    def _create_llms(self, company_id: str, data: Dict, prompts: Dict, knowledge_base_id: str) -> Dict:
        """Create LLMs with generated prompts"""
        try:
            company_name = data['company_name']
            llms = {}
            
            # Office Hours LLM
            office_llm_data = {
                "model": "gpt-4o-mini",
                "model_temperature": 0.1,
                "general_prompt": prompts['office_hours_prompt'],
                "knowledge_base_ids": [knowledge_base_id] if knowledge_base_id else []
            }
            
            response = requests.post(
                config.retell_urls['llm'],
                headers=self.retell_headers,
                json=office_llm_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                llms['office_hours'] = response.json().get('llm_id')
            else:
                raise OnboardingError(f"Office Hours LLM creation failed: {response.status_code}")
            
            # After Hours LLM
            after_llm_data = {
                "model": "gpt-4o-mini",
                "model_temperature": 0.1,
                "general_prompt": prompts['after_hours_prompt'],
                "knowledge_base_ids": [knowledge_base_id] if knowledge_base_id else []
            }
            
            response = requests.post(
                config.retell_urls['llm'],
                headers=self.retell_headers,
                json=after_llm_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                llms['after_hours'] = response.json().get('llm_id')
            else:
                raise OnboardingError(f"After Hours LLM creation failed: {response.status_code}")
            
            # Main Router LLM
            router_llm_data = {
                "model": "gpt-4o-mini",
                "model_temperature": 0.1,
                "general_prompt": prompts['global_prompt'],
                "knowledge_base_ids": [knowledge_base_id] if knowledge_base_id else []
            }
            
            response = requests.post(
                config.retell_urls['llm'],
                headers=self.retell_headers,
                json=router_llm_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                llms['main_router'] = response.json().get('llm_id')
            else:
                raise OnboardingError(f"Main Router LLM creation failed: {response.status_code}")
            
            return llms
            
        except requests.RequestException as e:
            raise OnboardingError(f"LLM creation network error: {str(e)}")
        except Exception as e:
            raise OnboardingError(f"LLM creation failed: {str(e)}")
    
    def _create_agents(self, company_id: str, data: Dict, llms: Dict) -> Dict:
        """Create voice agents with proper configuration"""
        try:
            company_name = data['company_name']
            voice_id = config.voice_defaults['voice_id']
            
            agents = {}
            
            # Office Hours Agent
            office_agent_data = {
                "agent_name": f"{company_name} Office Hours Assistant",
                "voice_id": voice_id,
                "response_engine": {
                    "type": "retell-llm",
                    "llm_id": llms['office_hours']
                }
            }
            
            response = requests.post(
                config.retell_urls['agent'],
                headers=self.retell_headers,
                json=office_agent_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                agents['office_hours'] = response.json().get('agent_id')
            else:
                raise OnboardingError(f"Office Hours Agent creation failed: {response.status_code}")
            
            # After Hours Agent
            after_agent_data = {
                "agent_name": f"{company_name} After Hours Assistant",
                "voice_id": voice_id,
                "response_engine": {
                    "type": "retell-llm",
                    "llm_id": llms['after_hours']
                }
            }
            
            response = requests.post(
                config.retell_urls['agent'],
                headers=self.retell_headers,
                json=after_agent_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                agents['after_hours'] = response.json().get('agent_id')
            else:
                raise OnboardingError(f"After Hours Agent creation failed: {response.status_code}")
            
            # Main Router Agent
            router_agent_data = {
                "agent_name": f"{company_name} Main Router",
                "voice_id": voice_id,
                "response_engine": {
                    "type": "retell-llm",
                    "llm_id": llms['main_router']
                }
            }
            
            response = requests.post(
                config.retell_urls['agent'],
                headers=self.retell_headers,
                json=router_agent_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                agents['main_router'] = response.json().get('agent_id')
            else:
                raise OnboardingError(f"Main Router Agent creation failed: {response.status_code}")
            
            return agents
            
        except requests.RequestException as e:
            raise OnboardingError(f"Agent creation network error: {str(e)}")
        except Exception as e:
            raise OnboardingError(f"Agent creation failed: {str(e)}")
    
    def _purchase_phone_number(self, company_id: str, data: Dict, main_router_id: str) -> Dict:
        """Purchase phone number with fallback logic"""
        try:
            company_name = data['company_name']
            preferred_area_code = data['preferred_area_code']
            fallback_codes = data.get('fallback_area_codes', config.area_code_fallbacks['default'])
            
            # Try area codes in order
            area_codes_to_try = [preferred_area_code] + fallback_codes
            
            for area_code in area_codes_to_try:
                try:
                    payload = {
                        "nickname": f"{company_name} Number",
                        "area_code": int(area_code),
                        "country_code": "US",
                        "number_provider": "twilio",
                        "inbound_allowed_countries": ["US", "CA"],
                        "inbound_agent_id": main_router_id,
                        "inbound_agent_version": 0
                    }
                    
                    response = requests.post(
                        config.retell_urls['phone_number'],
                        headers=self.retell_headers,
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code in [200, 201]:
                        phone_data = response.json()
                        return {
                            'phone_number': phone_data.get('phone_number'),
                            'phone_number_id': phone_data.get('phone_number_id'),
                            'area_code_used': area_code,
                            'agent_id': main_router_id
                        }
                    
                except Exception as e:
                    if config.diagnostics_enabled:
                        print(f"   ⚠️ Failed area code {area_code}: {str(e)}")
                    continue
            
            # All area codes failed
            raise OnboardingError(f"No phone numbers available in any area code: {area_codes_to_try}")
            
        except Exception as e:
            raise OnboardingError(f"Phone number purchase failed: {str(e)}")
    
    def _create_dashboard_account(self, company_id: str, data: Dict) -> Dict:
        """Create dashboard login credentials"""
        try:
            company_name = data['company_name']
            
            # Generate standardized credentials
            sanitized_name = re.sub(r'[^a-zA-Z0-9]', '', company_name.lower())
            dashboard_email = f"support{sanitized_name}@justclara.ai"
            dashboard_password = f"{sanitized_name}@321"
            
            return {
                'dashboard_email': dashboard_email,
                'dashboard_password': dashboard_password,
                'company_name': sanitized_name
            }
            
        except Exception as e:
            raise OnboardingError(f"Dashboard account creation failed: {str(e)}")
    
    def get_company_status(self, company_id: str) -> Dict:
        """Get company onboarding status"""
        try:
            company_config = db.get_company_config(company_id)
            if not company_config:
                return {'error': 'Company not found'}
            
            # Check if onboarding is complete
            is_complete = all([
                company_config.get('llm_id_oh'),
                company_config.get('agent_id_oh'),
                company_config.get('retell_phone_number'),
                company_config.get('dashboard_email')
            ])
            
            return {
                'company_id': company_id,
                'company_name': company_config.get('company_name'),
                'status': 'completed' if is_complete else 'in_progress',
                'phone_number': company_config.get('retell_phone_number'),
                'dashboard_email': company_config.get('dashboard_email'),
                'created_at': company_config.get('created_at').isoformat() if company_config.get('created_at') else None,
                'updated_at': company_config.get('updated_at').isoformat() if company_config.get('updated_at') else None
            }
            
        except Exception as e:
            return {'error': f'Failed to get company status: {str(e)}'}

# Global onboarding engine instance
onboarding_engine = OnboardingEngine()