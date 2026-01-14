#!/usr/bin/env python3
"""
Simplified Onboarding Status API Endpoint
GET /api/onboard/{company_id}/status - Get company onboarding status
"""

import os
import sys
import json
import traceback
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from _config import config
    from _onboarding_engine import onboarding_engine, OnboardingError
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Get company onboarding status"""
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Extract company_id from URL path or query parameters
            company_id = None
            
            try:
                # Try to get from query parameters first (Vercel passes it this way)
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)
                
                if 'session_id' in query_params:
                    company_id = query_params['session_id'][0]
                else:
                    # Fallback: extract from path
                    path_parts = parsed_url.path.strip('/').split('/')
                    if len(path_parts) >= 3:  # /api/onboard/COMPANY_ID/status
                        company_id = path_parts[-2]  # Second to last part
                
                if not company_id or len(company_id) > 100:
                    raise ValueError("Invalid company ID")
                    
            except Exception as e:
                if config.diagnostics_enabled:
                    print(f"❌ Error extracting company_id: {str(e)}")
                    print(f"❌ Path: {self.path}")
                raise OnboardingError("Invalid request path - company_id required")
            
            if config.diagnostics_enabled:
                print(f"🔍 GET /api/onboard/{company_id}/status")
            
            # Get company status
            status = onboarding_engine.get_company_status(company_id)
            
            if 'error' in status:
                raise OnboardingError(status['error'])
            
            if config.diagnostics_enabled:
                print(f"🔍 Company status: {status['status']}")
            
            self.wfile.write(json.dumps(status, ensure_ascii=True).encode('utf-8'))
            
        except OnboardingError as e:
            self.send_error_response(str(e), 400)
        except Exception as e:
            if config.diagnostics_enabled:
                print(f"❌ Error in status: {str(e)}")
                print(f"❌ Traceback: {traceback.format_exc()}")
            self.send_error_response(f"Internal server error: {str(e)}", 500)
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
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
                'error': str(message)[:500],
                'status_code': status_code
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=True).encode('utf-8'))
        except Exception:
            self.wfile.write(b'{"success": false, "error": "Internal server error"}')