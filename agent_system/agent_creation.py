#!/usr/bin/env python3
"""
Agent Creation and Conversation Flow
Handle agent creation and conversation flow setup
"""

import requests
from .config import RETELL_API_TOKEN, RETELL_URLS
from .llm_creation import generate_global_prompt


def create_agents(company_data, llm_data, knowledge_base_id):
    """Create Retell agents and attach LLM IDs with knowledge base"""
    print(f"🎯 Step 3: Creating LLM-based Agents")
    
    headers = {
        "Authorization": f"Bearer {RETELL_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    company_name = company_data['company_name']
    
    # Create Office Hours Agent with enhanced configuration
    office_agent_payload = {
        "response_engine": {
            "type": "retell-llm",
            "llm_id": llm_data['office_hours']['llm_id'],
            "version": 0
        },
        "voice_id": "11labs-Chloe",
        "agent_name": f"{company_name} (Office Hours)",
        "language": "en-US",
        "channel": "voice",
        "data_storage_setting": "everything",
        "opt_in_signed_url": False,
        "end_call_after_silence_ms": 150000,
        "post_call_analysis_model": "gpt-4.1-mini",
        "pii_config": {
            "mode": "post_call",
            "categories": []
        },
        "analysis_successful_prompt": "Evaluate whether the agent seems to have a successful call with the user, where the agent finishes the task, and the call was complete without being cutoff.",
        "analysis_summary_prompt": "Write a 1-3 sentence summary of the call based on the call transcript. Should capture the important information and actions taken during the call.",
        "enable_backchannel": True,
        "backchannel_frequency": 0.4,
        "backchannel_words": [
            "yeah", "mm-hmm", "uh-huh", "okay", "alright", "got it", 
            "perfect", "sounds good", "absolutely", "for sure", "understood", 
            "okay great", "right", "gotcha"
        ],
        "max_call_duration_ms": 963000,
        "knowledge_base_ids": [knowledge_base_id],
        "kb_config": {
            "top_k": 3,
            "filter_score": 0.6
        },
        "boosted_keywords": [
            "fire alarm", "fire sprinkler", "sprinkler inspection", "backflow", 
            "backflow preventer", "standpipe", "extinguisher", "fire extinguisher", 
            "extinguishers", "hydrant", "fire hydrant", "alarm panel", "pull station", 
            "smoke detector", "duct detector", "monitoring", "central station", 
            "NFPA", "NFPA 25", "NFPA 72", "AHJ", "impairment", "inspection", 
            "testing", "maintenance", "ITM", "annual inspection", "quarterly inspection", 
            "five-year", "flow test", "hydrostatic test", "riser", "FDC", 
            "fire department connection", "emergency", "urgent", "after hours", 
            "dispatch", "technician", "service call", "work order", "callback number", 
            "site contact", "access code", "gate code", "lockbox", "landlord", 
            "property manager", "suite", "unit", "building", "floor", "warehouse", 
            "front entrance", "rear entrance", "loading dock", "cross street", 
            "landmark", "zip code", "postal code", "pincode", "HVAC", "thermostat", 
            "compressor", "condenser", "evaporator", "refrigerant", "Freon", 
            "heat pump", "RTU", "rooftop unit", "air handler", "ductwork", 
            "blower motor", "capacitor"
        ],
        "ambient_sound": "coffee-shop",
        "normalize_for_speech": True,
        "stt_mode": "accurate",
        "allow_user_dtmf": False,
        "user_dtmf_options": {},
        "denoising_mode": "noise-and-background-speech-cancellation",
        "interruption_sensitivity": 0.5
    }

    office_agent_response = requests.post(RETELL_URLS['agent'], headers=headers, json=office_agent_payload)
    
    if office_agent_response.status_code not in [200, 201]:
        raise Exception(f"Office Hours Agent creation failed: {office_agent_response.text}")
    
    office_agent_id = office_agent_response.json()["agent_id"]
    print(f"   Office Hours Agent created: {office_agent_id} (version 0)")
    
    # Create After Hours Agent with enhanced configuration
    after_agent_payload = {
        "response_engine": {
            "type": "retell-llm",
            "llm_id": llm_data['after_hours']['llm_id'],
            "version": 0
        },
        "voice_id": "11labs-Chloe",
        "agent_name": f"{company_name} (After Hours)",
        "language": "en-US",
        "channel": "voice",
        "data_storage_setting": "everything",
        "opt_in_signed_url": False,
        "end_call_after_silence_ms": 150000,
        "post_call_analysis_model": "gpt-4.1-mini",
        "pii_config": {
            "mode": "post_call",
            "categories": []
        },
        "analysis_successful_prompt": "Evaluate whether the agent seems to have a successful call with the user, where the agent finishes the task, and the call was complete without being cutoff.",
        "analysis_summary_prompt": "Write a 1-3 sentence summary of the call based on the call transcript. Should capture the important information and actions taken during the call.",
        "enable_backchannel": True,
        "backchannel_frequency": 0.4,
        "backchannel_words": [
            "yeah", "mm-hmm", "uh-huh", "okay", "alright", "got it", 
            "perfect", "sounds good", "absolutely", "for sure", "understood", 
            "okay great", "right", "gotcha"
        ],
        "max_call_duration_ms": 963000,
        "knowledge_base_ids": [knowledge_base_id],
        "kb_config": {
            "top_k": 3,
            "filter_score": 0.6
        },
        "boosted_keywords": [
            "fire alarm", "fire sprinkler", "sprinkler inspection", "backflow", 
            "backflow preventer", "standpipe", "extinguisher", "fire extinguisher", 
            "extinguishers", "hydrant", "fire hydrant", "alarm panel", "pull station", 
            "smoke detector", "duct detector", "monitoring", "central station", 
            "NFPA", "NFPA 25", "NFPA 72", "AHJ", "impairment", "inspection", 
            "testing", "maintenance", "ITM", "annual inspection", "quarterly inspection", 
            "five-year", "flow test", "hydrostatic test", "riser", "FDC", 
            "fire department connection", "emergency", "urgent", "after hours", 
            "dispatch", "technician", "service call", "work order", "callback number", 
            "site contact", "access code", "gate code", "lockbox", "landlord", 
            "property manager", "suite", "unit", "building", "floor", "warehouse", 
            "front entrance", "rear entrance", "loading dock", "cross street", 
            "landmark", "zip code", "postal code", "pincode", "HVAC", "thermostat", 
            "compressor", "condenser", "evaporator", "refrigerant", "Freon", 
            "heat pump", "RTU", "rooftop unit", "air handler", "ductwork", 
            "blower motor", "capacitor"
        ],
        "ambient_sound": "coffee-shop",
        "normalize_for_speech": True,
        "stt_mode": "accurate",
        "allow_user_dtmf": False,
        "user_dtmf_options": {},
        "denoising_mode": "noise-and-background-speech-cancellation",
        "interruption_sensitivity": 0.5
    }

    after_agent_response = requests.post(RETELL_URLS['agent'], headers=headers, json=after_agent_payload)
    
    if after_agent_response.status_code not in [200, 201]:
        raise Exception(f"After Hours Agent creation failed: {after_agent_response.text}")
    
    after_agent_id = after_agent_response.json()["agent_id"]
    print(f"   After Hours Agent created: {after_agent_id} (version 0)")
    
    return {
        "office_hours": {
            "llm_id": llm_data['office_hours']['llm_id'],
            "agent_id": office_agent_id
        },
        "after_hours": {
            "llm_id": llm_data['after_hours']['llm_id'],
            "agent_id": after_agent_id
        }
    }


def create_conversation_flow(company_data, llm_data, office_hours_agent_id, after_hours_agent_id):
    """Create conversation flow with proper branch logic and agent transfers"""
    print(f"🔄 Step 4: Creating Conversation Flow with Branch Logic")
    
    headers = {
        "Authorization": f"Bearer {RETELL_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    company_name = company_data['company_name']
    flow_name = f"{company_name} Flow"
    
    # Generate global prompt from template for conversation flow
    global_prompt = generate_global_prompt(company_data)
    
    print(f"   Flow Name: {flow_name}")
    print(f"   Global Prompt: {len(global_prompt)} chars")
    print(f"   Office Hours Agent: {office_hours_agent_id}")
    print(f"   After Hours Agent: {after_hours_agent_id}")
    
    # Using the exact structure that works with proper branch logic
    payload = {
        "conversation_flow_name": flow_name,
        "start_speaker": "agent",
        "start_node_id": "node-1766415486721",
        "global_prompt": global_prompt,
        "model_choice": {
            "type": "cascading",
            "model": "gpt-4.1"
        },
        "tool_call_strict_mode": True,
        "begin_tag_display_position": {
            "x": 122,
            "y": 333
        },
        "nodes": [
            {
                "id": "node-1766415486721",
                "name": "Logic Split Node",
                "type": "branch",
                "display_position": {
                    "x": 421.15671755908613,
                    "y": 344.8734788282263
                },
                "edges": [
                    {
                        "id": "edge-1766415527234-ad0kd71zb",
                        "destination_node_id": "node-1766415491302",
                        "transition_condition": {
                            "type": "prompt",
                            "prompt": f"If {{{{current_time_America/{company_data['time_place']}}}}} is within office hours"
                        }
                    }
                ],
                "else_edge": {
                    "id": "edge-1766415486721-bwb6k8dtj",
                    "destination_node_id": "node-1766415495993",
                    "transition_condition": {
                        "type": "prompt",
                        "prompt": "Else"
                    }
                }
            },
            {
                "id": "node-1766415491302",
                "name": "Office Hours",
                "type": "agent_swap",
                "agent_id": office_hours_agent_id,
                "agent_version": 0,
                "display_position": {
                    "x": 898.4530878611638,
                    "y": 283.4251215977421
                },
                "edge": {
                    "id": "edge-1766415491302-rd4zvwavp",
                    "transition_condition": {
                        "type": "prompt",
                        "prompt": "Transfer failed"
                    }
                },
                "speak_during_execution": False,
                "post_call_analysis_setting": "only_destination_agent"
                # Removed webhook_setting
            },
            {
                "id": "node-1766415495993",
                "name": "After Hours",
                "type": "agent_swap",
                "agent_id": after_hours_agent_id,
                "agent_version": 0,
                "display_position": {
                    "x": 868.4434303522186,
                    "y": 584.9508043156518
                },
                "edge": {
                    "id": "edge-1766415495993-tninv2dyf",
                    "transition_condition": {
                        "type": "prompt",
                        "prompt": "Transfer failed"
                    }
                },
                "speak_during_execution": False,
                "post_call_analysis_setting": "only_destination_agent"
                # Removed webhook_setting
            }
        ]
    }
    
    response = requests.post(RETELL_URLS['conversation_flow'], headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        response_data = response.json()
        flow_id = response_data.get('conversation_flow_id')
        print(f"   ✅ Conversation Flow created: {flow_id}")
        print(f"   ✅ Branch Logic: Office Hours → {office_hours_agent_id}")
        print(f"   ✅ Branch Logic: After Hours → {after_hours_agent_id}")
        return flow_id
    else:
        print(f"   ⚠️  Conversation Flow creation failed ({response.status_code}): {response.text}")
        print(f"   ⚠️  Continuing without conversation flow...")
        return None


def create_main_router_agent(company_data, conversation_flow_id):
    """Create Main Router Agent that uses the conversation flow and create dashboard account"""
    print(f"🎯 Step 5: Creating Main Router Agent")
    
    if not conversation_flow_id:
        print(f"   ⚠️  No conversation flow available, skipping Main Router Agent")
        return {
            "agent_id": None,
            "conversation_flow_id": None,
            "dashboard_result": None
        }
    
    headers = {
        "Authorization": f"Bearer {RETELL_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    company_name = company_data['company_name']
    agent_name = f"{company_name} (Main Router)"
    
    print(f"   Agent Name: {agent_name}")
    print(f"   Using Conversation Flow: {conversation_flow_id}")
    
    # Create Main Router Agent with enhanced configuration
    router_agent_payload = {
        "response_engine": {
            "type": "conversation-flow",
            "conversation_flow_id": conversation_flow_id,
            "version": 0
        },
        "voice_id": "11labs-Grace",
        "agent_name": agent_name,
        "language": "en-US",
        "channel": "voice",
        "data_storage_setting": "everything",
        "opt_in_signed_url": False,
        "end_call_after_silence_ms": 150000,
        "post_call_analysis_model": "gpt-4.1-mini",
        "pii_config": {
            "mode": "post_call",
            "categories": []
        },
        "analysis_successful_prompt": "Evaluate whether the agent seems to have a successful call with the user, where the agent finishes the task, and the call was complete without being cutoff.",
        "analysis_summary_prompt": "Write a 1-3 sentence summary of the call based on the call transcript. Should capture the important information and actions taken during the call.",
        "enable_backchannel": True,
        "backchannel_frequency": 0.4,
        "backchannel_words": [
            "yeah", "mm-hmm", "uh-huh", "okay", "alright", "got it", 
            "perfect", "sounds good", "absolutely", "for sure", "understood", 
            "okay great", "right", "gotcha"
        ],
        "max_call_duration_ms": 963000,
        "boosted_keywords": [
            "fire alarm", "fire sprinkler", "sprinkler inspection", "backflow", 
            "backflow preventer", "standpipe", "extinguisher", "fire extinguisher", 
            "extinguishers", "hydrant", "fire hydrant", "alarm panel", "pull station", 
            "smoke detector", "duct detector", "monitoring", "central station", 
            "NFPA", "NFPA 25", "NFPA 72", "AHJ", "impairment", "inspection", 
            "testing", "maintenance", "ITM", "annual inspection", "quarterly inspection", 
            "five-year", "flow test", "hydrostatic test", "riser", "FDC", 
            "fire department connection", "emergency", "urgent", "after hours", 
            "dispatch", "technician", "service call", "work order", "callback number", 
            "site contact", "access code", "gate code", "lockbox", "landlord", 
            "property manager", "suite", "unit", "building", "floor", "warehouse", 
            "front entrance", "rear entrance", "loading dock", "cross street", 
            "landmark", "zip code", "postal code", "pincode", "HVAC", "thermostat", 
            "compressor", "condenser", "evaporator", "refrigerant", "Freon", 
            "heat pump", "RTU", "rooftop unit", "air handler", "ductwork", 
            "blower motor", "capacitor"
        ],
        "ambient_sound": "coffee-shop",
        "normalize_for_speech": True,
        "stt_mode": "accurate",
        "allow_user_dtmf": False,
        "user_dtmf_options": {},
        "denoising_mode": "noise-and-background-speech-cancellation",
        "interruption_sensitivity": 0.5
    }

    router_agent_response = requests.post(RETELL_URLS['agent'], headers=headers, json=router_agent_payload)
    
    if router_agent_response.status_code not in [200, 201]:
        print(f"   ⚠️  Main Router Agent creation failed: {router_agent_response.text}")
        print(f"   ⚠️  Continuing without Main Router Agent...")
        return {
            "agent_id": None,
            "conversation_flow_id": conversation_flow_id,
            "dashboard_result": None
        }
    
    router_agent_id = router_agent_response.json()["agent_id"]
    print(f"   ✅ Main Router Agent created: {router_agent_id} (version 0)")
    print(f"   ✅ Agent Name: {agent_name}")
    
    # Immediately create dashboard account after agent creation
    print(f"\n🔧 Creating dashboard account for {company_name}...")
    
    from .dashboard_creation import create_dashboard_account, display_dashboard_credentials
    
    dashboard_result = create_dashboard_account(company_name, router_agent_id)
    
    # Display credentials immediately after creation
    display_dashboard_credentials(dashboard_result)

    return {
        "agent_id": router_agent_id,
        "conversation_flow_id": conversation_flow_id,
        "dashboard_result": dashboard_result
    }