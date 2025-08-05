#!/usr/bin/env python3
"""
Test API endpoints to see what's causing the 104 matches issue.
"""
import requests
import json

def test_api_endpoints():
    """Test the API endpoints to see what data they return"""
    base_url = "http://127.0.0.1:5000"
    
    print("=== Testing API Endpoints ===")
    
    # Test matches endpoint
    print("\n1. Testing /api/matches endpoint:")
    try:
        response = requests.get(f"{base_url}/api/matches?lender_company=GeoTex&borrower_company=Steel&month=August&year=2024")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            if 'matches' in data:
                print(f"Number of matches: {len(data['matches'])}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test data endpoint
    print("\n2. Testing /api/data endpoint:")
    try:
        response = requests.get(f"{base_url}/api/data")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total records: {len(data.get('data', []))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test unmatched endpoint
    print("\n3. Testing /api/unmatched endpoint:")
    try:
        response = requests.get(f"{base_url}/api/unmatched?lender_company=GeoTex&borrower_company=Steel&month=August&year=2024")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Unmatched records: {len(data.get('unmatched', []))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api_endpoints() 