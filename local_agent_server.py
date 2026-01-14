#!/usr/bin/env python3
"""
Local Agent Creation Server
Runs locally to handle agent creation requests from the web interface
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import os
from agent_system.main import create_agent_automation

class AgentCreationHandler(BaseHTTPRequestHandler):
    # Store creation statuses in memory (in production, use a database)
    creation_statuses = {}
    
    def do_POST(self):
        """Handle agent creation requests"""
        if self.path == '/create-agent':
            self.handle_create_agent()
        elif self.path == '/onboard':
            self.handle_onboard_sync()
        else:
            self.send_error(404, "Not Found")
    
    def do_GET(self):
        """Handle status check requests"""
        if self.path.startswith('/creation-status/'):
            creation_id = self.path.split('/')[-1]
            self.handle_creation_status(creation_id)
        else:
            self.send_error(404, "Not Found")
    
    def handle_create_agent(self):
        """Handle agent creation request"""
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Read request data
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
            else:
                data = {}
            
            # Validate required fields - support both camelCase and snake_case
            company_name = data.get('companyName') or data.get('company_name')
            office_address = data.get('officeAddress') or data.get('business_address')
            time_zone = data.get('timeZone') or data.get('timezone')
            business_hours = data.get('businessHours') or data.get('business_hours')
            contact_number = data.get('contactNumber') or data.get('primary_phone_number')
            
            if not company_name:
                self.send_error_response('Missing required field: company_name', 400)
                return
            if not office_address:
                self.send_error_response('Missing required field: business_address', 400)
                return
            if not time_zone:
                self.send_error_response('Missing required field: timezone', 400)
                return
            if not business_hours:
                self.send_error_response('Missing required field: business_hours', 400)
                return
            if not contact_number:
                self.send_error_response('Missing required field: primary_phone_number', 400)
                return
            
            # Generate creation ID
            creation_id = f"creation_{int(time.time())}"
            
            # Transform data
            company_data = self.transform_form_data(data)
            
            # Start agent creation in background
            threading.Thread(
                target=self.create_agent_async,
                args=(creation_id, company_data),
                daemon=True
            ).start()
            
            # Return immediate response
            response_data = {
                'success': True,
                'creation_id': creation_id,
                'message': 'Agent creation started'
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_error_response(str(e), 500)
    
    def handle_onboard_sync(self):
        """Handle synchronous onboarding request (waits for completion)"""
        try:
            # Read request data
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
            else:
                data = {}
            
            # Validate required fields
            company_name = data.get('companyName') or data.get('company_name')
            office_address = data.get('officeAddress') or data.get('business_address')
            time_zone = data.get('timeZone') or data.get('timezone')
            business_hours = data.get('businessHours') or data.get('business_hours')
            contact_number = data.get('contactNumber') or data.get('primary_phone_number')
            
            if not company_name:
                self.send_error_response('Missing required field: company_name', 400)
                return
            if not office_address:
                self.send_error_response('Missing required field: business_address', 400)
                return
            if not time_zone:
                self.send_error_response('Missing required field: timezone', 400)
                return
            if not business_hours:
                self.send_error_response('Missing required field: business_hours', 400)
                return
            if not contact_number:
                self.send_error_response('Missing required field: primary_phone_number', 400)
                return
            
            # Transform data
            company_data = self.transform_form_data(data)
            
            # Run agent creation synchronously
            result = create_agent_automation(company_data)
            
            # Extract dashboard credentials
            dashboard_creds = result.get('dashboard_credentials', {})
            
            # Format response for frontend
            response_data = {
                'success': True,
                'phone_number': result.get('phone_number', '+1 (555) 000-0000'),
                'dashboard_email': dashboard_creds.get('email', 'support@company.justclara.ai') if dashboard_creds else 'support@company.justclara.ai',
                'dashboard_password': dashboard_creds.get('password', 'company@321') if dashboard_creds else 'company@321',
                'company_id': result.get('company_id'),
                'agent_id': result.get('main_router_agent_id')
            }
            
            # Set CORS headers and send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Onboarding failed: {error_msg}")
            self.send_error_response(error_msg, 500)
    
    def handle_creation_status(self, creation_id):
        """Handle status check request"""
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Get status
            status_data = self.creation_statuses.get(creation_id)
            
            if status_data:
                response_data = {
                    'success': True,
                    'status': status_data['status'],
                    'progress': status_data['progress'],
                    'message': status_data['message'],
                    'result': status_data.get('result'),
                    'error': status_data['message'] if status_data['status'] == 'error' else None,
                    'troubleshooting_tips': status_data.get('troubleshooting_tips')
                }
            else:
                response_data = {
                    'success': False,
                    'error': 'Creation ID not found'
                }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_error_response(str(e), 500)
    
    def transform_form_data(self, form_data):
        """Transform web form data to agent system format"""
        
        # Support both camelCase and snake_case field names
        company_name = form_data.get('companyName') or form_data.get('company_name', '')
        office_address = form_data.get('officeAddress') or form_data.get('business_address', '')
        contact_number = form_data.get('contactNumber') or form_data.get('primary_phone_number', '')
        time_zone = form_data.get('timeZone') or form_data.get('timezone', 'Eastern')
        assistant_name = form_data.get('assistantName') or form_data.get('assistant_name', 'Clara')
        
        # Extract website URL from websites array or use first one
        website_url = form_data.get('websiteUrl') or form_data.get('website_url', '')
        websites = form_data.get('websites', [])
        if not website_url and websites:
            website_url = websites[0]
        
        # Parse area code from contact number
        area_code = form_data.get('preferred_area_code') or self.extract_area_code(contact_number)
        
        # Transform business days and hours
        business_days = form_data.get('businessDays', [])
        if isinstance(business_days, list):
            business_days_str = ', '.join(business_days)
        else:
            business_days_str = str(business_days)
        
        business_hours = form_data.get('businessHours') or form_data.get('business_hours', '')
        
        # Map timezone to time_place for Retell API
        timezone_mapping = {
            'Eastern': 'New_York',
            'Central': 'Chicago', 
            'Mountain': 'Denver',
            'Pacific': 'Los_Angeles',
            'Alaska': 'Anchorage',
            'Hawaii': 'Honolulu'
        }
        
        time_place = timezone_mapping.get(time_zone, 'New_York')
        
        return {
            'company_name': company_name,
            'office_address': office_address,
            'website_url': website_url,
            'websites': websites,
            'time_zone': time_zone,
            'time_place': time_place,
            'business_days': business_days_str,
            'start_time': form_data.get('startTime', '09:00'),
            'end_time': form_data.get('endTime', '17:00'),
            'business_hours': business_hours,
            'contact_number': contact_number,
            'area_code': area_code,
            'assistant_name': assistant_name,
            'post_call_summary_sms': form_data.get('postCallSummarySMS', False),
            'post_call_summary_email': form_data.get('postCallSummaryEmail', False),
            'summary_sms_number': form_data.get('smsNumbers', [None])[0] if form_data.get('smsNumbers') else None,
            'summary_email_address': form_data.get('primaryEmail', ''),
            'primary_email': form_data.get('primaryEmail', ''),
            'cc_emails': form_data.get('ccEmails', []),
            'sms_numbers': form_data.get('smsNumbers', []),
            'uploaded_files': form_data.get('uploadedFiles', [])
        }
    
    def extract_area_code(self, phone_number):
        """Extract area code from phone number"""
        digits = ''.join(filter(str.isdigit, phone_number))
        
        if len(digits) >= 10:
            if len(digits) == 11 and digits.startswith('1'):
                return digits[1:4]
            elif len(digits) == 10:
                return digits[:3]
        
        return '555'
    
    def create_agent_async(self, creation_id, company_data):
        """Create agent asynchronously"""
        try:
            print(f"🚀 Starting agent creation for {creation_id}")
            
            # Store initial status
            self.creation_statuses[creation_id] = {
                'status': 'in_progress',
                'progress': 0,
                'message': 'Starting agent creation...',
                'timestamp': time.time()
            }
            
            # Run agent creation
            result = create_agent_automation(company_data)
            
            # Extract dashboard credentials
            dashboard_creds = result.get('dashboard_credentials', {})
            
            # Format response for frontend
            formatted_result = {
                'success': True,
                'phone_number': result.get('phone_number', '+1 (555) 000-0000'),
                'dashboard_email': dashboard_creds.get('email', 'support@company.justclara.ai') if dashboard_creds else 'support@company.justclara.ai',
                'dashboard_password': dashboard_creds.get('password', 'company@321') if dashboard_creds else 'company@321',
                'company_id': result.get('company_id'),
                'agent_id': result.get('main_router_agent_id')
            }
            
            # Store success result
            self.creation_statuses[creation_id] = {
                'status': 'completed',
                'progress': 100,
                'message': '🎉 Agent creation completed successfully!',
                'result': formatted_result,
                'timestamp': time.time()
            }
            
            print(f"✅ Agent creation completed for {creation_id}")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Agent creation failed for {creation_id}: {error_msg}")
            
            # Provide troubleshooting tips
            troubleshooting_tips = []
            if "too long" in error_msg.lower():
                troubleshooting_tips = [
                    "Use a shorter company name (max 50 characters)",
                    "Remove special characters from company name",
                    "Try using abbreviations or acronyms"
                ]
            elif "sitemap" in error_msg.lower():
                troubleshooting_tips = [
                    "Check if your website has a valid sitemap.xml",
                    "Verify the website URL is accessible",
                    "Try using a different website URL"
                ]
            elif "unauthorized" in error_msg.lower():
                troubleshooting_tips = [
                    "Check Retell API token configuration",
                    "Verify API token has proper permissions",
                    "Contact support for API access issues"
                ]
            else:
                troubleshooting_tips = [
                    "Check your internet connection",
                    "Verify all form fields are filled correctly",
                    "Try again in a few minutes",
                    "Contact support if the problem persists"
                ]
            
            # Store error result
            self.creation_statuses[creation_id] = {
                'status': 'error',
                'progress': 0,
                'message': error_msg,
                'troubleshooting_tips': troubleshooting_tips,
                'timestamp': time.time()
            }
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_error_response(self, message, status_code):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_response = {
            'success': False,
            'error': message
        }
        
        self.wfile.write(json.dumps(error_response).encode())

def main():
    """Start the local agent creation server"""
    port = 8000
    server_address = ('localhost', port)
    
    print(f"🚀 Starting Local Agent Creation Server")
    print(f"📡 Server running at http://localhost:{port}")
    print(f"🔗 Agent creation endpoint: http://localhost:{port}/create-agent")
    print(f"📊 Status check endpoint: http://localhost:{port}/creation-status/{{id}}")
    print(f"⏹️  Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        httpd = HTTPServer(server_address, AgentCreationHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    main()