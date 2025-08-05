#!/usr/bin/env python3
"""
Test the reconcile endpoint to see what's happening.
"""
import requests
import json

def test_reconcile_endpoint():
    """Test the reconcile endpoint"""
    base_url = "http://127.0.0.1:5000"
    
    print("=== Testing /api/reconcile endpoint ===")
    
    # Test reconcile endpoint
    try:
        response = requests.post(f"{base_url}/api/reconcile", 
                               json={
                                   'lender_company': 'GeoTex',
                                   'borrower_company': 'Steel',
                                   'month': 'August',
                                   'year': '2024'
                               })
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print(f"Matches found: {data.get('matches_found', 'N/A')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_reconcile_endpoint() 