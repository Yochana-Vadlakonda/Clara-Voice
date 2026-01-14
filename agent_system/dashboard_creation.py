#!/usr/bin/env python3
"""
Dashboard Creation Module
Automatically creates dashboard accounts and registers agents
"""

import requests
import json
import re


def sanitize_company_name(company_name):
    """Remove spaces and convert to lowercase for credential generation"""
    return re.sub(r'\s+', '', company_name.lower())


def generate_credentials(company_name):
    """Generate deterministic email and password based on company name"""
    sanitized_name = sanitize_company_name(company_name)
    
    email = f"support{sanitized_name}@justclara.ai"
    password = f"{sanitized_name}@321"
    
    return email, password


def create_dashboard_account(company_name, agent_id_mr):
    """
    Create dashboard account and register agent
    
    Args:
        company_name (str): Company name (spaces will be removed automatically)
        agent_id_mr (str): Main router agent ID (e.g., agent_76624de15ce0b291c8692c62ea)
    
    Returns:
        dict: Dashboard creation result with credentials
    """
    try:
        print(f"🔧 Creating dashboard account for {company_name}")
        
        # Generate credentials
        email, password = generate_credentials(company_name)
        sanitized_name = sanitize_company_name(company_name)
        
        # API endpoint
        url = "https://clara-answering-services.justclara.ai/api/auth/register"
        
        # Headers
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://voice.justclara.ai",
            "referer": "https://voice.justclara.ai/"
        }
        
        # Request body
        payload = {
            "email": email,
            "password": password,
            "agentId": agent_id_mr,
            "companyName": sanitized_name
        }
        
        print(f"📡 Registering dashboard account...")
        print(f"   Email: {email}")
        print(f"   Agent ID: {agent_id_mr}")
        
        # Make API request
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Dashboard account created successfully!")
            
            # Display credentials
            print("\n" + "="*50)
            print("🎉 DASHBOARD CREATED SUCCESSFULLY")
            print("="*50)
            print(f"Username (Email): {email}")
            print(f"Password: {password}")
            print("="*50)
            
            return {
                "success": True,
                "email": email,
                "password": password,
                "agent_id": agent_id_mr,
                "company_name": sanitized_name,
                "response": response.json() if response.content else {}
            }
            
        else:
            print(f"❌ Dashboard creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "email": email,
                "password": password
            }
            
    except Exception as e:
        print(f"❌ Dashboard creation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "email": email if 'email' in locals() else None,
            "password": password if 'password' in locals() else None
        }


def register_agent_to_dashboard(agent_id, dashboard_credentials):
    """
    Register agent to the created dashboard account
    This function can be extended based on additional API requirements
    """
    try:
        print(f"🔗 Registering agent {agent_id} to dashboard...")
        
        # The agent registration is handled in the main dashboard creation
        # This function is a placeholder for additional registration steps if needed
        
        print("✅ Agent registered to dashboard successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Agent registration error: {e}")
        return False


def display_dashboard_credentials(credentials):
    """Display dashboard login credentials in a clear format"""
    if credentials.get('success'):
        print("\n" + "="*60)
        print("🎉 DASHBOARD CREATED SUCCESSFULLY")
        print("="*60)
        print(f"Username (Email): {credentials['email']}")
        print(f"Password: {credentials['password']}")
        print(f"Agent ID: {credentials['agent_id']}")
        print(f"Company: {credentials['company_name']}")
        print("="*60)
        print("💡 Save these credentials - they will be needed to access the dashboard")
        print("="*60)
    else:
        print("\n❌ Dashboard creation failed!")
        if credentials.get('email') and credentials.get('password'):
            print(f"Generated credentials (for reference):")
            print(f"Email: {credentials['email']}")
            print(f"Password: {credentials['password']}")
        print(f"Error: {credentials.get('error', 'Unknown error')}")