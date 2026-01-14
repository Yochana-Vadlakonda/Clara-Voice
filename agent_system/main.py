#!/usr/bin/env python3
"""
Main Entry Point - Agent Creation Automation
Complete end-to-end Retell AI agent creation with knowledge base integration
"""

from .user_input import collect_user_input
from .knowledge_base import create_knowledge_base
from .llm_creation import create_llms
from .agent_creation import create_agents, create_conversation_flow, create_main_router_agent
from .phone_number import purchase_phone_number
from .database import save_company_data


def create_agent_automation(company_data):
    """Main orchestration function - Complete agent creation lifecycle"""
    try:
        print("🚀 Starting Complete Agent Creation Automation")
        print("=" * 60)
        
        # Step 1: Create knowledge base from sitemap
        knowledge_base_name = company_data['company_name']  # Use just the company name
        try:
            knowledge_base_id = create_knowledge_base(company_data['website_url'], knowledge_base_name)
        except Exception as e:
            error_msg = str(e)
            if "too long" in error_msg.lower():
                print(f"❌ Knowledge base name is too long. Please use a shorter company name.")
                print(f"   Current name: '{knowledge_base_name}' ({len(knowledge_base_name)} characters)")
                print(f"   Maximum recommended: 50 characters")
            elif "sitemap" in error_msg.lower():
                print(f"❌ Website sitemap error: {error_msg}")
                print(f"   Please check if {company_data['website_url']} has a valid sitemap")
            elif "unauthorized" in error_msg.lower():
                print(f"❌ API Authorization error: {error_msg}")
                print(f"   Please check your Retell API token in the configuration")
            else:
                print(f"❌ Knowledge base creation error: {error_msg}")
            raise Exception(f"Knowledge base creation failed: {error_msg}")
        
        # Step 2: Create LLMs with conversation flows
        try:
            llm_data = create_llms(company_data, knowledge_base_id)
        except Exception as e:
            error_msg = str(e)
            print(f"❌ LLM creation error: {error_msg}")
            if "unauthorized" in error_msg.lower():
                print(f"   Please check your Retell API token")
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                print(f"   API quota exceeded - please try again later")
            raise Exception(f"LLM creation failed: {error_msg}")
        
        # Step 3: Create LLM-based agents (they will be auto-published)
        try:
            agent_data = create_agents(company_data, llm_data, knowledge_base_id)
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Agent creation error: {error_msg}")
            if "llm_id" in error_msg.lower():
                print(f"   LLM ID issue - please check if LLMs were created successfully")
            raise Exception(f"Agent creation failed: {error_msg}")
        
        # Step 4: Create conversation flow with published agent IDs for transfers
        try:
            conversation_flow_id = create_conversation_flow(
                company_data, 
                llm_data, 
                agent_data['office_hours']['agent_id'],
                agent_data['after_hours']['agent_id']
            )
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Conversation flow creation error: {error_msg}")
            print(f"   Continuing without conversation flow...")
            conversation_flow_id = None
        
        # Step 5: Create Main Router Agent (uses conversation flow, will be auto-published)
        # Dashboard account is created immediately after agent creation
        try:
            router_agent_data = create_main_router_agent(company_data, conversation_flow_id)
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Main router agent creation error: {error_msg}")
            print(f"   Continuing without main router agent...")
            router_agent_data = {
                "agent_id": None,
                "conversation_flow_id": conversation_flow_id,
                "dashboard_result": None
            }
        
        # Extract dashboard result from router agent creation
        dashboard_result = router_agent_data.get('dashboard_result')
        
        # Step 6: Purchase phone number with area code fallback and inbound agent assignment
        phone_data = None
        if router_agent_data['agent_id']:
            try:
                phone_data = purchase_phone_number(
                    company_data['company_name'], 
                    company_data['area_code'],
                    router_agent_data['agent_id']  # Pass main router agent ID for inbound calls
                )
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Phone number purchase error: {error_msg}")
                print(f"   Continuing without phone number...")
                phone_data = None
        
        # Step 7: Save to database (including phone number and dashboard data)
        try:
            company_id = save_company_data(
                company_data, 
                knowledge_base_id, 
                agent_data, 
                llm_data, 
                conversation_flow_id, 
                router_agent_data,
                phone_data,
                dashboard_result
            )
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Database save error: {error_msg}")
            print(f"   Agents created successfully but data not saved to database")
            company_id = None
        
        # Return final agent IDs
        final_result = {
            "company_id": company_id,
            "knowledge_base_id": knowledge_base_id,
            "conversation_flow_id": conversation_flow_id,
            "main_router_agent_id": router_agent_data['agent_id'],
            "office_hours_agent_id": agent_data['office_hours']['agent_id'],
            "after_hours_agent_id": agent_data['after_hours']['agent_id'],
            "office_hours_llm_id": agent_data['office_hours']['llm_id'],
            "after_hours_llm_id": agent_data['after_hours']['llm_id'],
            "phone_number": phone_data['phone_number'] if phone_data else None,
            "phone_number_id": phone_data['phone_number_id'] if phone_data else None,
            "dashboard_credentials": dashboard_result
        }
        
        print(f"\n🎉 AGENT CREATION COMPLETE!")
        print(f"Company ID: {company_id}")
        print(f"Knowledge Base ID: {knowledge_base_id}")
        print(f"Conversation Flow ID: {conversation_flow_id or 'Not created'}")
        print(f"Main Router Agent ID: {router_agent_data['agent_id'] or 'Not created'}")
        print(f"Office Hours Agent ID: {agent_data['office_hours']['agent_id']}")
        print(f"After Hours Agent ID: {agent_data['after_hours']['agent_id']}")
        if phone_data:
            print(f"📞 Phone Number: {phone_data['phone_number']}")
            print(f"📞 Phone Number ID: {phone_data['phone_number_id']}")
        if dashboard_result and dashboard_result.get('success'):
            print(f"🎯 Dashboard Account: {dashboard_result['email']}")
            print(f"🔑 Dashboard Password: {dashboard_result['password']}")
        
        return final_result
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        print(f"\n🔍 Troubleshooting Tips:")
        error_msg = str(e).lower()
        if "knowledge base" in error_msg and "too long" in error_msg:
            print(f"   • Use a shorter company name (max 30-40 characters)")
            print(f"   • Current company name: '{company_data.get('company_name', 'Unknown')}'")
        elif "sitemap" in error_msg:
            print(f"   • Check if your website has a valid sitemap.xml")
            print(f"   • Verify the website URL is accessible: {company_data.get('website_url', 'Unknown')}")
        elif "unauthorized" in error_msg or "token" in error_msg:
            print(f"   • Check your Retell API token in agent_system/config.py")
            print(f"   • Ensure the token has proper permissions")
        elif "quota" in error_msg or "limit" in error_msg:
            print(f"   • API quota exceeded - wait and try again later")
            print(f"   • Check your Retell account usage limits")
        else:
            print(f"   • Check your internet connection")
            print(f"   • Verify all configuration settings in agent_system/config.py")
            print(f"   • Check Retell API service status")
        raise


def main():
    """Main entry point"""
    try:
        # Collect input
        company_data = collect_user_input()
        
        # Run complete automation
        result = create_agent_automation(company_data)
        
        print(f"\n✅ Setup completed successfully!")
        
        return result
        
    except Exception as e:
        print(f"❌ Automation failed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()