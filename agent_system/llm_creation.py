#!/usr/bin/env python3
"""
LLM Creation and Prompt Generation
Handle LLM creation with template-based prompt generation
"""

import requests
from .config import RETELL_API_TOKEN, RETELL_URLS, TEMPLATE_FILES


def generate_global_prompt(company_data):
    """Generate global prompt using the template with company-specific data"""
    # Read the global prompt template with UTF-8 encoding
    with open(TEMPLATE_FILES['global'], 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace template variables with actual data
    global_prompt = template.replace('{{Company_Name}}', company_data['company_name'])
    global_prompt = global_prompt.replace('{{Time_Zone}}', company_data['time_zone'])
    global_prompt = global_prompt.replace('{{Time_Place}}', company_data['time_place'])
    global_prompt = global_prompt.replace('{{Business_Hours}}', company_data['business_hours'])
    global_prompt = global_prompt.replace('{{Office_Address}}', company_data['office_address'])
    
    return global_prompt


def generate_office_hours_prompt(company_data):
    """Generate office hours prompt using the template with company-specific data"""
    # Read the office hours prompt template with UTF-8 encoding
    with open(TEMPLATE_FILES['office_hours'], 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace template variables with actual data
    office_hours_prompt = template.replace('{{Company_Name}}', company_data['company_name'])
    office_hours_prompt = office_hours_prompt.replace('{{Assistant_Name}}', company_data['assistant_name'])
    office_hours_prompt = office_hours_prompt.replace('{{Time_Zone}}', company_data['time_zone'])
    office_hours_prompt = office_hours_prompt.replace('{{Time_Place}}', company_data['time_place'])
    office_hours_prompt = office_hours_prompt.replace('{{Business_Hours}}', company_data['business_hours'])
    office_hours_prompt = office_hours_prompt.replace('{{Office_Address}}', company_data['office_address'])
    
    return office_hours_prompt


def generate_after_hours_prompt(company_data):
    """Generate after hours prompt using the template with company-specific data"""
    # Read the after hours prompt template with UTF-8 encoding
    with open(TEMPLATE_FILES['after_hours'], 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace template variables with actual data
    after_hours_prompt = template.replace('{{Company_Name}}', company_data['company_name'])
    after_hours_prompt = after_hours_prompt.replace('{{Assistant_Name}}', company_data['assistant_name'])
    after_hours_prompt = after_hours_prompt.replace('{{Time_Zone}}', company_data['time_zone'])
    after_hours_prompt = after_hours_prompt.replace('{{Time_Place}}', company_data['time_place'])
    after_hours_prompt = after_hours_prompt.replace('{{Business_Hours}}', company_data['business_hours'])
    after_hours_prompt = after_hours_prompt.replace('{{Office_Address}}', company_data['office_address'])
    
    return after_hours_prompt


def create_llms(company_data, knowledge_base_id):
    """Create Retell LLMs with conversation flow logic"""
    print(f"🤖 Step 2: Creating Retell LLMs")
    
    headers = {
        "Authorization": f"Bearer {RETELL_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    company_name = company_data['company_name']
    
    # Generate prompts from templates
    office_hours_prompt = generate_office_hours_prompt(company_data)
    print(f"   ✅ Generated office hours prompt from template ({len(office_hours_prompt)} chars)")
    
    after_hours_prompt = generate_after_hours_prompt(company_data)
    print(f"   ✅ Generated after hours prompt from template ({len(after_hours_prompt)} chars)")

    # Create Office Hours LLM
    office_llm_payload = {
        "model": "gpt-4.1",
        "model_temperature": 0,
        "model_high_priority": True,
        "tool_call_strict_mode": True,
        "knowledge_base_ids": [knowledge_base_id],
        "kb_config": {
            "top_k": 3,
            "filter_score": 0.6
        },
        "start_speaker": "agent",
        "begin_after_user_silence_ms": 2000,
        # Removed hardcoded begin_message - will be dynamic based on prompt
        "general_prompt": office_hours_prompt,
        "general_tools": [
            {
                "headers": {
                    "Authorization": "Bearer secretvalidateaddress2503",
                    "Content-Type": "application/json"
                },
                "parameter_type": "form",
                "method": "POST",
                "query_params": {
                    "_": "1"
                },
                "description": "Validates and geocodes a user-provided address using Google Maps.",
                "type": "custom",
                "url": "https://clara-validate-address.vercel.app/api/validate-address",
                "args_at_root": True,
                "execution_message_description": "Let me quickly verify that address for you...",
                "timeout_ms": 120000,
                "speak_after_execution": True,
                "name": "validate_address",
                "response_variables": {
                    "address_valid": "$.address_valid",
                    "raw_input": "$.raw_input",
                    "validated_address": "$.validated_address",
                    "place_id": "$.place_id",
                    "latitude": "$.latitude",
                    "longitude": "$.longitude"
                },
                "speak_during_execution": True,
                "parameters": {
                    "type": "object",
                    "required": [
                        "full_address"
                    ],
                    "properties": {
                        "full_address": {
                            "type": "string",
                            "description": "The full address string provided by the user",
                            "required": [
                                "full_address"
                            ]
                        }
                    }
                }
            },
            {
                "name": "end_call",
                "type": "end_call",
                "description": "end the call on bye or conversation ends"
            },
            {
                "name": "caller_details",
                "description": "variable used to store caller details like name, address, email coming from response of call",
                "variables": [
                    {
                        "type": "string",
                        "name": "name",
                        "description": "variable used to store caller name coming from response during the call"
                    },
                    {
                        "type": "string",
                        "name": "email",
                        "description": "variable used to store caller email coming from response during the call"
                    }
                ],
                "type": "extract_dynamic_variable"
            }
        ],
        "tools": [
            {
                "name": "user_details",
                "description": "Extract user details from the data they provide on the call",
                "variables": [
                    {
                        "type": "string",
                        "name": "user_name",
                        "description": "Extract the user's name as mentioned by them on the call."
                    },
                    {
                        "type": "string",
                        "name": "user_email",
                        "description": "Extract the user's email id as mentioned by them on the call. The email id must be in this format: \nxxx@xxx.xxx or xxx.xxx@xxx.xxx"
                    }
                ],
                "type": "extract_dynamic_variable"
            },
            {
                "headers": {
                    "Authorization": "Bearer secretvalidateaddress2503",
                    "Content-Type": "application/json"
                },
                "parameter_type": "json",
                "method": "POST",
                "query_params": {},
                "description": "Validates and geocodes a user-provided address using Google Maps.",
                "type": "custom",
                "url": "https://clara-validate-address.vercel.app/api/validate-address",
                "args_at_root": False,
                "execution_message_description": "Let me quickly verify that address for you...",
                "timeout_ms": 120000,
                "speak_after_execution": True,
                "name": "validate_address",
                "response_variables": {
                    "address_valid": "address_valid",
                    "city": "city",
                    "validated_address": "validated_address",
                    "street": "street",
                    "latitude": "latitude",
                    "postalCode": "postalCode",
                    "raw_input": "raw_input",
                    "state": "state",
                    "place_id": "place_id",
                    "longitude": "longitude"
                },
                "speak_during_execution": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_available_ts": {
                            "type": "string",
                            "description": "The timestamp of the appointment that is available for booking."
                        },
                        "doctor_name": {
                            "type": "string",
                            "description": "An optional field to specify the name of the doctor."
                        }
                    },
                    "required": [
                        "appointment_available_ts"
                    ]
                }
            },
            {
                "type": "transfer_call",
                "name": "transfer_to_support",
                "description": "Transfer to the support team.",
                "transfer_destination": {
                    "type": "predefined",
                    "number": "16175551212",
                    "ignore_e164_validation": False
                },
                "transfer_option": {
                    "type": "cold_transfer",
                    "show_transferee_as_caller": False
                }
            }
        ]
    }

    office_llm_response = requests.post(RETELL_URLS['llm'], headers=headers, json=office_llm_payload)
    
    if office_llm_response.status_code not in [200, 201]:
        print(f"   ❌ Office Hours LLM creation failed:")
        print(f"      Status Code: {office_llm_response.status_code}")
        print(f"      Response: {office_llm_response.text}")
        print(f"      Prompt Length: {len(office_hours_prompt)} chars")
        raise Exception(f"Office Hours LLM creation failed: {office_llm_response.status_code} - {office_llm_response.text}")
    
    office_llm_id = office_llm_response.json()["llm_id"]
    print(f"   ✅ Office Hours LLM created: {office_llm_id}")

    # Create After Hours LLM
    after_llm_payload = {
        "model": "gpt-4.1",
        "model_temperature": 0,
        "model_high_priority": True,
        "tool_call_strict_mode": True,
        "knowledge_base_ids": [knowledge_base_id],
        "kb_config": {
            "top_k": 3,
            "filter_score": 0.6
        },
        "start_speaker": "agent",
        "begin_after_user_silence_ms": 2000,
        # Removed hardcoded begin_message - will be dynamic based on prompt
        "general_prompt": after_hours_prompt,
        "general_tools": [
            {
                "headers": {
                    "Authorization": "Bearer secretvalidateaddress2503",
                    "Content-Type": "application/json"
                },
                "parameter_type": "form",
                "method": "POST",
                "query_params": {
                    "_": "1"
                },
                "description": "Validates and geocodes a user-provided address using Google Maps.",
                "type": "custom",
                "url": "https://clara-validate-address.vercel.app/api/validate-address",
                "args_at_root": True,
                "execution_message_description": "Let me quickly verify that address for you...",
                "timeout_ms": 120000,
                "speak_after_execution": True,
                "name": "validate_address",
                "response_variables": {
                    "address_valid": "$.address_valid",
                    "raw_input": "$.raw_input",
                    "validated_address": "$.validated_address",
                    "place_id": "$.place_id",
                    "latitude": "$.latitude",
                    "longitude": "$.longitude"
                },
                "speak_during_execution": True,
                "parameters": {
                    "type": "object",
                    "required": [
                        "full_address"
                    ],
                    "properties": {
                        "full_address": {
                            "type": "string",
                            "description": "The full address string provided by the user",
                            "required": [
                                "full_address"
                            ]
                        }
                    }
                }
            },
            {
                "name": "end_call",
                "type": "end_call",
                "description": "end the call on bye or conversation ends"
            },
            {
                "name": "caller_details",
                "description": "variable used to store caller details like name, address, email coming from response during the call",
                "variables": [
                    {
                        "type": "string",
                        "name": "name",
                        "description": "variable used to store caller name coming from response during the call"
                    },
                    {
                        "type": "string",
                        "name": "email",
                        "description": "variable used to store caller email coming from response during the call"
                    }
                ],
                "type": "extract_dynamic_variable"
            }
        ],
        "tools": [
            {
                "name": "user_details",
                "description": "Extract user details from the data they provide on the call",
                "variables": [
                    {
                        "type": "string",
                        "name": "user_name",
                        "description": "Extract the user's name as mentioned by them on the call."
                    },
                    {
                        "type": "string",
                        "name": "user_email",
                        "description": "Extract the user's email id as mentioned by them on the call. The email id must be in this format: \nxxx@xxx.xxx or xxx.xxx@xxx.xxx"
                    }
                ],
                "type": "extract_dynamic_variable"
            },
            {
                "headers": {
                    "Authorization": "Bearer secretvalidateaddress2503",
                    "Content-Type": "application/json"
                },
                "parameter_type": "json",
                "method": "POST",
                "query_params": {},
                "description": "Validates and geocodes a user-provided address using Google Maps.",
                "type": "custom",
                "url": "https://clara-validate-address.vercel.app/api/validate-address",
                "args_at_root": False,
                "execution_message_description": "Let me quickly verify that address for you...",
                "timeout_ms": 120000,
                "speak_after_execution": True,
                "name": "validate_address",
                "response_variables": {
                    "address_valid": "address_valid",
                    "city": "city",
                    "validated_address": "validated_address",
                    "street": "street",
                    "latitude": "latitude",
                    "postalCode": "postalCode",
                    "raw_input": "raw_input",
                    "state": "state",
                    "place_id": "place_id",
                    "longitude": "longitude"
                },
                "speak_during_execution": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_available_ts": {
                            "type": "string",
                            "description": "The timestamp of the appointment that is available for booking."
                        },
                        "doctor_name": {
                            "type": "string",
                            "description": "An optional field to specify the name of the doctor."
                        }
                    },
                    "required": [
                        "appointment_available_ts"
                    ]
                }
            },
            {
                "type": "transfer_call",
                "name": "transfer_to_support",
                "description": "Transfer to the support team.",
                "transfer_destination": {
                    "type": "predefined",
                    "number": "16175551212",
                    "ignore_e164_validation": False
                },
                "transfer_option": {
                    "type": "cold_transfer",
                    "show_transferee_as_caller": False
                }
            }
        ]
    }

    after_llm_response = requests.post(RETELL_URLS['llm'], headers=headers, json=after_llm_payload)
    
    if after_llm_response.status_code not in [200, 201]:
        print(f"   ❌ After Hours LLM creation failed:")
        print(f"      Status Code: {after_llm_response.status_code}")
        print(f"      Response: {after_llm_response.text}")
        print(f"      Prompt Length: {len(after_hours_prompt)} chars")
        raise Exception(f"After Hours LLM creation failed: {after_llm_response.status_code} - {after_llm_response.text}")
    
    after_llm_id = after_llm_response.json()["llm_id"]
    print(f"   ✅ After Hours LLM created: {after_llm_id}")

    return {
        "office_hours": {
            "llm_id": office_llm_id,
            "prompt": office_hours_prompt
        },
        "after_hours": {
            "llm_id": after_llm_id,
            "prompt": after_hours_prompt
        }
    }