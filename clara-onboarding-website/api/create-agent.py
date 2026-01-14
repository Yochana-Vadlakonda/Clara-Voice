#!/usr/bin/env python3
"""
Agent Creation API Endpoint
Production-grade Vercel serverless function
"""

# Vercel Runtime Configuration
import os
os.environ.setdefault('PYTHONPATH', os.path.dirname(__file__))

from http.server import BaseHTTPRequestHandler
import json
import time
import re
import base64
import sys
import traceback

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

try:
    from _config import config
except ImportError:
    # Fallback if config module fails
    class FallbackConfig:
        def __init__(self):
            self.retell_api_token = os.environ.get('RETELL_API_TOKEN', '')
            self.diagnostics_enabled = os.environ.get('DIAGNOSTICS', '').lower() == 'true'
    config = FallbackConfig()

def sanitize_company_name(company_name):
    """Remove spaces and convert to lowercase for credential generation"""
    if not company_name:
        return 'company'
    return re.sub(r'\s+', '', company_name.lower())

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Set CORS headers first
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            if config.diagnostics_enabled:
                print(f"🔍 POST /api/create-agent - Processing request")
            
            # Read and parse request body with error handling
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                else:
                    data = {}
            except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as e:
                raise Exception(f"Invalid request data: {str(e)}")
            
            # Check if we have Retell API token for real creation
            retell_token = config.retell_api_token
            
            if config.diagnostics_enabled:
                print(f"🔍 Token present: {bool(retell_token and retell_token.strip())}")
                print(f"🔍 Request data keys: {list(data.keys())}")
            
            if not retell_token or not retell_token.strip():
                raise Exception('RETELL_API_TOKEN is required for agent creation. Please configure it in Vercel environment variables.')
            
            # Real agent creation mode
            company_name = data.get('companyName', '').strip()
            
            # Validate required fields
            required_fields = ['companyName', 'officeAddress', 'timeZone', 'contactNumber']
            missing_fields = []
            for field in required_fields:
                if not data.get(field, '').strip():
                    missing_fields.append(field)
            
            if missing_fields:
                raise Exception(f'Missing required fields: {", ".join(missing_fields)}')
            
            # Prepare company data with safe defaults
            company_data = {
                'companyName': company_name,
                'officeAddress': data.get('officeAddress', '').strip(),
                'websiteUrl': data.get('websiteUrl', '').strip() or 'https://example.com',
                'timeZone': data.get('timeZone', 'Eastern').strip(),
                'businessHours': data.get('businessHours', '9:00 AM - 5:00 PM').strip(),
                'contactNumber': data.get('contactNumber', '').strip(),
                'assistantName': data.get('assistantName', 'Clara').strip()
            }
            
            # Create safe creation_id with error handling
            try:
                # Create a simplified data structure for encoding
                safe_data = {
                    'name': company_data['companyName'][:30],  # Limit length
                    'url': company_data['websiteUrl'][:50],
                    'assistant': company_data['assistantName'][:20]
                }
                json_str = json.dumps(safe_data)
                encoded_data = base64.b64encode(json_str.encode('utf-8')).decode('ascii')
                # Limit total length to prevent URL issues
                if len(encoded_data) > 150:
                    encoded_data = encoded_data[:150]
                creation_id = f"real_{int(time.time())}_{encoded_data}"
            except Exception:
                # Fallback to simple creation_id
                creation_id = f"real_{int(time.time())}"
            
            response_data = {
                'success': True,
                'creation_id': creation_id,
                'message': 'Agent creation started - this will take 2-3 minutes',
                'demo_mode': False
            }
            
            if config.diagnostics_enabled:
                print(f"🔍 Response: {response_data}")
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=True).encode('utf-8'))
            
        except Exception as e:
            if config.diagnostics_enabled:
                print(f"❌ Error in create-agent: {str(e)}")
                print(f"❌ Traceback: {traceback.format_exc()}")
            self.send_error_response(str(e), 500)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_error_response(self, message, status_code):
        """Send error response with proper encoding"""
        try:
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'success': False,
                'error': str(message)[:200],  # Limit error message length
                'demo_mode': True
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=True).encode('utf-8'))
        except Exception:
            # Last resort error handling
            self.wfile.write(b'{"success": false, "error": "Internal server error"}')