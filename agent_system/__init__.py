#!/usr/bin/env python3
"""
Agent System Package
Modular agent creation system for Retell AI
"""

from .main import main, create_agent_automation
from .user_input import collect_user_input
from .knowledge_base import create_knowledge_base
from .llm_creation import create_llms
from .agent_creation import create_agents, create_conversation_flow, create_main_router_agent
from .phone_number import purchase_phone_number
from .database import save_company_data
from .validators import extract_area_code, validate_us_canada_phone, validate_email_format

__version__ = "1.0.0"
__author__ = "Agent Creation System"

__all__ = [
    "main",
    "create_agent_automation",
    "collect_user_input",
    "create_knowledge_base",
    "create_llms",
    "create_agents",
    "create_conversation_flow",
    "create_main_router_agent",
    "purchase_phone_number",
    "save_company_data",
    "extract_area_code",
    "validate_us_canada_phone",
    "validate_email_format"
]