#!/usr/bin/env python3
"""
Validation Utilities
Phone number, email, and other input validation functions
"""

import re


def extract_area_code(phone_number):
    """Extract 3-digit area code from US/Canada phone number"""
    # Remove all non-digit characters
    digits_only = re.sub(r'[^\d]', '', phone_number)
    
    # Handle different formats:
    # +1234567890 -> 234567890 (after removing +1)
    # 1234567890 -> 234567890 (after removing leading 1)
    # 234567890 -> 234567890 (already correct)
    
    if len(digits_only) == 11 and digits_only.startswith('1'):
        # Remove leading 1 (US/Canada country code)
        digits_only = digits_only[1:]
    elif len(digits_only) == 10:
        # Already in correct format
        pass
    else:
        # Invalid format, return None to trigger re-entry
        return None
    
    if len(digits_only) == 10:
        # Extract first 3 digits as area code
        return digits_only[:3]
    
    return None


def validate_us_canada_phone(phone_number):
    """Validate US/Canada phone number and return in E.164 format"""
    # Remove all non-digit characters
    digits_only = re.sub(r'[^\d]', '', phone_number)
    
    # Handle different input formats
    if len(digits_only) == 11 and digits_only.startswith('1'):
        # Remove leading 1
        digits_only = digits_only[1:]
    elif len(digits_only) == 10:
        # Already correct
        pass
    else:
        return None
    
    if len(digits_only) == 10:
        # Return in E.164 format (+1 + 10 digits)
        return f"+1{digits_only}"
    
    return None


def validate_e164_format(phone_number):
    """Validate E.164 phone number format for US/Canada"""
    # E.164 format for US/Canada: +1 followed by 10 digits
    pattern = r'^\+1[2-9]\d{2}[2-9]\d{6}$'
    return bool(re.match(pattern, phone_number))


def validate_email_format(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))