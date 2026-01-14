#!/usr/bin/env python3
"""
Phone Number Management
Handle phone number purchasing and area code fallback logic
"""

import requests
import json
from .config import RETELL_API_TOKEN

# Area code fallback mapping for US and Canada
AREA_CODE_FALLBACKS = {
    "US": {
        "CA": {
            "213": ["323", "818", "310", "626"],
            "310": ["424", "213", "323", "818"],
            "323": ["213", "818", "310", "626"],
            "408": ["669", "650", "510", "415"],
            "415": ["628", "650", "510", "408"],
            "510": ["341", "415", "925", "408"],
            "530": ["916", "279", "209", "707"],
            "559": ["661", "209", "530"],
            "626": ["213", "323", "818"],
            "650": ["415", "408", "669"],
            "661": ["559", "818", "805"],
            "707": ["415", "628", "530"],
            "714": ["657", "949", "562"],
            "805": ["661", "818", "310"],
            "818": ["747", "213", "323"],
            "916": ["279", "530", "209", "707"],
            "925": ["510", "341", "707"],
            "949": ["714", "657", "562"]
        },
        "TX": {
            "214": ["469", "972", "817"],
            "469": ["214", "972", "817"],
            "972": ["214", "469", "817"],
            "817": ["682", "214", "972"],
            "713": ["281", "832", "346"],
            "281": ["713", "832", "346"],
            "832": ["713", "281", "346"],
            "346": ["713", "281", "832"],
            "512": ["737", "210", "830"],
            "737": ["512", "210", "830"],
            "210": ["830", "512"],
            "915": ["575", "432"]
        },
        "NY": {
            "212": ["646", "332", "917", "718"],
            "646": ["212", "332", "917"],
            "332": ["212", "646", "917"],
            "718": ["347", "929", "917"],
            "347": ["718", "929", "917"],
            "929": ["718", "347", "917"],
            "917": ["212", "718", "646"]
        },
        "FL": {
            "305": ["786", "954", "561"],
            "786": ["305", "954", "561"],
            "407": ["689", "321", "386"],
            "689": ["407", "321", "386"],
            "954": ["305", "786", "561"],
            "813": ["656", "727"],
            "727": ["813", "656"]
        },
        "IL": {
            "312": ["773", "872", "630"],
            "773": ["312", "872", "630"],
            "872": ["312", "773", "630"]
        },
        "WA": {
            "206": ["425", "253", "360"],
            "425": ["206", "253", "360"],
            "253": ["206", "425", "360"]
        },
        "MA": {
            "617": ["857", "781", "508"],
            "857": ["617", "781", "508"]
        },
        "GA": {
            "404": ["470", "678", "770"],
            "470": ["404", "678", "770"],
            "678": ["404", "470", "770"]
        }
    },
    "CANADA": {
        "ON": {
            "416": ["647", "437", "905"],
            "647": ["416", "437", "905"],
            "437": ["416", "647", "905"],
            "905": ["289", "365", "416"],
            "289": ["905", "365", "416"],
            "365": ["905", "289", "416"],
            "613": ["343", "819", "705"],
            "343": ["613", "819", "705"],
            "519": ["226", "548", "905"],
            "226": ["519", "548", "905"]
        },
        "BC": {
            "604": ["778", "236", "672"],
            "778": ["604", "236", "672"],
            "236": ["604", "778", "672"],
            "250": ["778", "236", "604"]
        },
        "AB": {
            "403": ["587", "825", "780"],
            "587": ["403", "825", "780"],
            "825": ["403", "587", "780"],
            "780": ["587", "825", "403"]
        },
        "QC": {
            "514": ["438", "450", "579"],
            "438": ["514", "450", "579"],
            "450": ["514", "438", "579"],
            "418": ["581", "819", "514"],
            "581": ["418", "819", "514"]
        },
        "ATLANTIC": {
            "902": ["782", "506", "709"],
            "782": ["902", "506", "709"],
            "506": ["902", "709"],
            "709": ["506", "902"]
        }
    }
}


def get_area_code_fallbacks(area_code):
    """Get fallback area codes for a given area code"""
    fallbacks = []
    
    # Search through all regions to find the area code
    for country, regions in AREA_CODE_FALLBACKS.items():
        for region, codes in regions.items():
            if area_code in codes:
                fallbacks.extend(codes[area_code])
                break
        if fallbacks:
            break
    
    # If no fallbacks found, return some common area codes
    if not fallbacks:
        fallbacks = ["212", "415", "213", "312", "617"]  # Major US cities
    
    return fallbacks


def purchase_phone_number(company_name, area_code, main_router_agent_id):
    """Purchase a phone number with area code fallback logic and inbound agent assignment (no webhook)"""
    print(f"📞 Step 6: Purchasing Phone Number")
    
    headers = {
        "Authorization": f"Bearer {RETELL_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    nickname = f"{company_name} Number"
    
    # Try primary area code first
    area_codes_to_try = [area_code] + get_area_code_fallbacks(area_code)
    
    print(f"   Trying area codes: {area_codes_to_try}")
    print(f"   Inbound agent ID: {main_router_agent_id}")
    
    for attempt_area_code in area_codes_to_try:
        print(f"   Attempting to purchase number with area code: {attempt_area_code}")
        
        payload = {
            "nickname": nickname,
            "area_code": int(attempt_area_code),
            "country_code": "US",
            "number_provider": "twilio",
            "inbound_allowed_countries": ["US", "CA"],
            "inbound_agent_id": main_router_agent_id,
            "inbound_agent_version": 0
            # Removed inbound_webhook_url
        }
        
        response = requests.post(
            "https://api.retellai.com/create-phone-number",
            headers=headers,
            json=payload
        )
        
        if response.status_code in [200, 201]:
            phone_data = response.json()
            phone_number = phone_data.get("phone_number")
            phone_number_id = phone_data.get("phone_number_id")
            
            print(f"   ✅ Phone number purchased: {phone_number}")
            print(f"   ✅ Phone number ID: {phone_number_id}")
            print(f"   ✅ Area code used: {attempt_area_code}")
            print(f"   ✅ Inbound agent assigned: {main_router_agent_id}")
            
            return {
                "phone_number": phone_number,
                "phone_number_id": phone_number_id,
                "area_code_used": attempt_area_code,
                "nickname": nickname,
                "inbound_agent_id": main_router_agent_id
            }
        else:
            print(f"   ⚠️  Failed with area code {attempt_area_code}: {response.status_code} - {response.text}")
            continue
    
    # If all area codes failed
    print(f"   ❌ Failed to purchase phone number with any area code")
    return None