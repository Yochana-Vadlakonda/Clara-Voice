#!/usr/bin/env python3
"""
User Input Collection
Collect and validate all user input for agent creation
"""

from .config import TIMEZONE_OPTIONS
from .validators import extract_area_code, validate_us_canada_phone, validate_email_format


def collect_user_input():
    """Collect required user input"""
    print("🏢 Agent Creation Input")
    print("=" * 30)
    
    company_name = input("Company Name: ").strip()
    office_address = input("Office Address: ").strip()
    
    website_url = input("Website URL (for knowledge base): ").strip()
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url
    
    # Time zone selection
    print("\nTime Zones:")
    for key, (place, zone) in TIMEZONE_OPTIONS.items():
        print(f"  {key}. {place.replace('_', ' ')} ({zone})")
    
    while True:
        choice = input("Select time zone (1-4): ").strip()
        if choice in TIMEZONE_OPTIONS:
            time_place, time_zone = TIMEZONE_OPTIONS[choice]
            break
        print("Invalid choice. Please select 1-4.")
    
    business_hours = input("Business Hours: ").strip()
    
    # Contact number with area code extraction
    while True:
        contact_number = input("Contact Number (US/Canada format): ").strip()
        area_code = extract_area_code(contact_number)
        if area_code:
            # Format the contact number in E.164 format
            formatted_number = validate_us_canada_phone(contact_number)
            if formatted_number:
                contact_number = formatted_number
                break
            else:
                print("Invalid phone number format. Please enter a valid US/Canada phone number.")
        else:
            print("Could not extract area code. Please enter a valid US/Canada phone number (e.g., 555-123-4567, (555) 123-4567, or +1-555-123-4567)")
    
    assistant_name = input("Assistant Name (default: Clara): ").strip() or "Clara"
    
    # Post-call summary options
    print("\n📋 Post-Call Summary Options")
    print("=" * 35)
    
    # SMS Summary
    post_call_summary_sms = input("Would you like post-call summaries via SMS? (y/n): ").strip().lower() == 'y'
    summary_sms_number = None
    if post_call_summary_sms:
        while True:
            sms_number = input("Enter SMS number (US/Canada format, e.g., 555-123-4567): ").strip()
            formatted_sms = validate_us_canada_phone(sms_number)
            if formatted_sms:
                summary_sms_number = formatted_sms
                break
            print("Invalid format. Please enter a valid US/Canada phone number.")
    
    # Email Summary
    post_call_summary_email = input("Would you like post-call summaries via Email? (y/n): ").strip().lower() == 'y'
    summary_email_address = None
    if post_call_summary_email:
        while True:
            email = input("Enter email address: ").strip()
            if validate_email_format(email):
                summary_email_address = email
                break
            print("Invalid email format. Please enter a valid email address.")
    
    return {
        'company_name': company_name,
        'office_address': office_address,
        'time_place': time_place,
        'time_zone': time_zone,
        'business_hours': business_hours,
        'contact_number': contact_number,
        'area_code': area_code,
        'website_url': website_url,
        'assistant_name': assistant_name,
        'post_call_summary_sms': post_call_summary_sms,
        'post_call_summary_email': post_call_summary_email,
        'summary_sms_number': summary_sms_number,
        'summary_email_address': summary_email_address
    }