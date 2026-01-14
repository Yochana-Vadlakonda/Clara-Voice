#!/usr/bin/env python3
"""
Production-Grade Configuration Module
Ensures consistent environment variable loading between local and Vercel
"""

import os
import sys
from typing import Optional, List
import json

class ConfigError(Exception):
    """Configuration validation error"""
    pass

class ProductionConfig:
    """Centralized configuration with validation and diagnostics"""
    
    def __init__(self):
        self.diagnostics_enabled = self._get_bool_env('DIAGNOSTICS', False)
        
        # API Configuration
        self.retell_api_token = self._get_required_env('RETELL_API_TOKEN')
        self.org_id = self._get_optional_env('ORG_ID')
        
        # Database Configuration
        self.db_config = {
            'host': self._get_optional_env('DB_HOST', 'localhost'),
            'port': int(self._get_optional_env('DB_PORT', '5432')),
            'database': self._get_optional_env('DB_NAME', 'self_onb'),
            'user': self._get_optional_env('DB_USER', 'postgres'),
            'password': self._get_optional_env('DB_PASSWORD', 'Admin123')
        }
        
        # API URLs
        self.retell_urls = {
            'sitemap': "https://api.retellai.com/list-sitemap",
            'knowledge_base': "https://api.retellai.com/create-knowledge-base",
            'llm': "https://api.retellai.com/create-retell-llm",
            'agent': "https://api.retellai.com/create-agent",
            'conversation_flow': "https://api.retellai.com/create-conversation-flow",
            'phone_number': "https://api.retellai.com/create-phone-number"
        }
        
        # Voice Configuration Defaults
        self.voice_defaults = {
            'voice_id': '11labs-Rachel',
            'backchanneling_enabled': True,
            'backchannel_frequency': 0.5,
            'backchannel_words': 'mm-hmm, okay, got it, alright, right, sure, I see, understood',
            'speech_normalization': True,
            'interruption_sensitivity': 0.5
        }
        
        # Area Code Fallbacks
        self.area_code_fallbacks = {
            'default': ['212', '415', '213', '312', '617', '404', '206', '303', '702'],
            'east_coast': ['212', '617', '404', '305', '215'],
            'west_coast': ['415', '213', '206', '503', '702'],
            'central': ['312', '214', '713', '816', '314']
        }
        
        # Onboarding Steps
        self.onboarding_steps = [
            'init',
            'validate_input',
            'create_company',
            'create_knowledge_base',
            'generate_prompts',
            'create_llms',
            'create_agents',
            'purchase_phone',
            'create_dashboard',
            'configure_voice',
            'finalize'
        ]
        
        if self.diagnostics_enabled:
            self._log_diagnostics()
    
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable with validation"""
        value = os.environ.get(key)
        if not value or not value.strip():
            raise ConfigError(f"Required environment variable '{key}' is missing or empty")
        return value.strip()
    
    def _get_optional_env(self, key: str, default: str = "") -> str:
        """Get optional environment variable with default"""
        return os.environ.get(key, default).strip()
    
    def _get_bool_env(self, key: str, default: bool = False) -> bool:
        """Get boolean environment variable"""
        value = os.environ.get(key, "").lower()
        return value in ("true", "1", "yes", "on") if value else default
    
    def _log_diagnostics(self):
        """Log safe diagnostic information (no secrets)"""
        print(f"🔍 PRODUCTION CONFIG DIAGNOSTICS")
        print(f"   Python Version: {sys.version}")
        print(f"   Platform: {sys.platform}")
        print(f"   Environment Variables Present:")
        
        # Only log presence of env vars, not values
        env_keys = [
            'RETELL_API_TOKEN',
            'DB_HOST', 'DB_NAME', 'DB_USER',
            'VERCEL', 'VERCEL_ENV', 'VERCEL_REGION'
        ]
        
        for key in env_keys:
            status = "✅ Present" if os.environ.get(key) else "❌ Missing"
            print(f"     {key}: {status}")
        
        print(f"   Working Directory: {os.getcwd()}")
        print(f"   Onboarding Steps: {len(self.onboarding_steps)} configured")

# Global configuration instance
try:
    config = ProductionConfig()
except ConfigError as e:
    print(f"❌ Configuration Error: {e}")
    sys.exit(1)