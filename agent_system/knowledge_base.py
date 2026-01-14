#!/usr/bin/env python3
"""
Knowledge Base Creation
Handle knowledge base creation from website sitemaps
"""

import requests
import json
from .config import RETELL_API_TOKEN, ORG_ID, RETELL_URLS


def create_knowledge_base(website_url, knowledge_base_name):
    """Create knowledge base from website sitemap"""
    print(f"📚 Step 1: Creating Knowledge Base from {website_url}")
    
    # Validate and truncate knowledge base name if too long
    max_kb_name_length = 50  # Conservative limit
    if len(knowledge_base_name) > max_kb_name_length:
        original_name = knowledge_base_name
        knowledge_base_name = knowledge_base_name[:max_kb_name_length-3] + "..."
        print(f"   ⚠️  Knowledge base name truncated from '{original_name}' to '{knowledge_base_name}'")
    
    print(f"   Knowledge base name: '{knowledge_base_name}' ({len(knowledge_base_name)} chars)")
    
    # List website sitemap
    sitemap_headers = {
        "Authorization": f"Bearer {RETELL_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Add orgid header only if ORG_ID is provided
    if ORG_ID:
        sitemap_headers["orgid"] = ORG_ID
    
    try:
        sitemap_response = requests.post(RETELL_URLS['sitemap'], headers=sitemap_headers, json={"website_url": website_url})
        
        if sitemap_response.status_code not in [200, 201]:
            error_msg = f"Sitemap listing failed: {sitemap_response.status_code}"
            try:
                error_detail = sitemap_response.json().get('message', sitemap_response.text)
                error_msg += f" - {error_detail}"
            except:
                error_msg += f" - {sitemap_response.text}"
            raise Exception(error_msg)
        
        sitemap_data = sitemap_response.json()
        
        # Handle response format
        if isinstance(sitemap_data, list):
            sitemap_urls = sitemap_data
        elif isinstance(sitemap_data, dict) and "urls" in sitemap_data:
            sitemap_urls = sitemap_data["urls"]
        else:
            raise Exception(f"Unexpected sitemap response format: {sitemap_data}")
        
        if not sitemap_urls:
            raise Exception("No URLs found in sitemap - please check if the website has a valid sitemap")
        
        print(f"   Found {len(sitemap_urls)} URLs in sitemap")
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error while fetching sitemap: {str(e)}")
    except Exception as e:
        if "sitemap" in str(e).lower():
            raise e
        else:
            raise Exception(f"Error processing sitemap: {str(e)}")
    
    # Create knowledge base
    kb_headers = {
        "Authorization": f"Bearer {RETELL_API_TOKEN}"
    }
    
    # Add orgid header only if ORG_ID is provided
    if ORG_ID:
        kb_headers["orgid"] = ORG_ID
    
    kb_form_data = {
        "knowledge_base_name": knowledge_base_name,
        "knowledge_base_texts": json.dumps([]),
        "knowledge_base_urls": json.dumps(sitemap_urls),
        "enable_auto_refresh": "false",
        "auto_crawling_paths": json.dumps([])
    }
    
    try:
        kb_response = requests.post(RETELL_URLS['knowledge_base'], headers=kb_headers, data=kb_form_data)
        
        if kb_response.status_code not in [200, 201]:
            error_msg = f"Knowledge base creation failed: {kb_response.status_code}"
            try:
                error_detail = kb_response.json()
                if isinstance(error_detail, dict):
                    if 'message' in error_detail:
                        error_msg += f" - {error_detail['message']}"
                    elif 'error' in error_detail:
                        error_msg += f" - {error_detail['error']}"
                    else:
                        error_msg += f" - {error_detail}"
                else:
                    error_msg += f" - {error_detail}"
            except:
                error_msg += f" - {kb_response.text}"
            
            # Provide specific guidance for common errors
            if "too long" in error_msg.lower():
                error_msg += f" (Try using a shorter company name - current: {len(knowledge_base_name)} chars)"
            elif "unauthorized" in error_msg.lower():
                error_msg += " (Check your Retell API token)"
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                error_msg += " (API quota exceeded - try again later)"
                
            raise Exception(error_msg)
        
        kb_data = kb_response.json()
        knowledge_base_id = kb_data["knowledge_base_id"]
        
        print(f"✅ Knowledge base created: {knowledge_base_id}")
        return knowledge_base_id
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error while creating knowledge base: {str(e)}")
    except Exception as e:
        if "Knowledge base creation failed" in str(e):
            raise e
        else:
            raise Exception(f"Error creating knowledge base: {str(e)}")