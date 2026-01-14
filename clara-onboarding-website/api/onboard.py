#!/usr/bin/env python3
"""
Simplified Onboarding API Endpoint
POST /api/onboard - Execute complete onboarding workflow
"""

import os
import sys
import json
import traceback
from http.server import BaseHTTPRequestHandler

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

try:
    from _config import config
    from _onboarding_engine import onboarding_engine, OnboardingError
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Execute complete onboarding workflow"""
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            if config.diagnostics_enabled:
                print(f"🔍 POST /api/onboard - Starting onboarding workflow")
            
            # Read and parse request body
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                else:
                    raise ValueError("No request body provided")
            except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as e:
                raise OnboardingError(f"Invalid request data: {str(e)}")
            
            if config.diagnostics_enabled:
                print(f"🔍 Request data keys: {list(data.keys())}")
            
            # Validate required fields
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
            
            # Start onboarding workflow (creates company record)
            company_id = onboarding_engine.start_onboarding(data)
            
            # Execute complete onboarding workflow
            result = onboarding_engine.execute_full_onboarding(company_id, data)
            
            if result['success']:
                response_data = {
                    'success': True,
                    'company_id': company_id,
                    'message': 'Onboarding completed successfully',
                    'duration_ms': result['duration_ms'],
                    'phone_number': result['results']['phone']['phone_number'],
                    'dashboard_email': result['results']['dashboard']['dashboard_email'],
                    'dashboard_password': result['results']['dashboard']['dashboard_password'],
                    'agent_ids': {
                        'office_hours': result['results']['agents']['office_hours'],
                        'after_hours': result['results']['agents']['after_hours'],
                        'main_router': result['results']['agents']['main_router']
                    }
                }
            else:
                response_data = {
                    'success': False,
                    'company_id': company_id,
                    'error': result['error'],
                    'duration_ms': result['duration_ms'],
                    'partial_results': result.get('partial_results', {})
                }
            
            if config.diagnostics_enabled:
                print(f"🔍 Onboarding result: {'SUCCESS' if result['success'] else 'FAILED'}")
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=True).encode('utf-8'))
            
        except OnboardingError as e:
            self.send_error_response(str(e), 400)
        except Exception as e:
            if config.diagnostics_enabled:
                print(f"❌ Error in onboard: {str(e)}")
                print(f"❌ Traceback: {traceback.format_exc()}")
            self.send_error_response(f"Internal server error: {str(e)}", 500)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
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
                'error': str(message)[:500],  # Limit error message length
                'status_code': status_code
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=True).encode('utf-8'))
        except Exception:
            # Last resort error handling
            self.wfile.write(b'{"success": false, "error": "Internal server error"}')