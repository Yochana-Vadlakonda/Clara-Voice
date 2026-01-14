#!/usr/bin/env python3
"""
Configuration and Constants
Centralized configuration for the agent creation system
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retell API Configuration
RETELL_API_TOKEN = os.getenv('RETELL_API_TOKEN')
ORG_ID = os.getenv('ORG_ID')

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# Time Zone Options
TIMEZONE_OPTIONS = {
    "1": ("Chicago", "Central Time"),
    "2": ("New_York", "Eastern Time"), 
    "3": ("Denver", "Mountain Time"),
    "4": ("Los_Angeles", "Pacific Time")
}

# API URLs
RETELL_URLS = {
    'sitemap': "https://api.retellai.com/list-sitemap",
    'knowledge_base': "https://api.retellai.com/create-knowledge-base",
    'llm': "https://api.retellai.com/create-retell-llm",
    'agent': "https://api.retellai.com/create-agent",
    'conversation_flow': "https://api.retellai.com/create-conversation-flow"
}

# Template Files
TEMPLATE_FILES = {
    'global': 'prompts/global_prompt_template.txt',
    'office_hours': 'prompts/office_hours_prompt_template.txt',
    'after_hours': 'prompts/after_hours_prompt_template.txt'
}