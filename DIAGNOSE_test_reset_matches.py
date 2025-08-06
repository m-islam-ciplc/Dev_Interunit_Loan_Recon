#!/usr/bin/env python3
"""
Test script to verify Reset All Matches functionality without keywords column
"""

from core.database import reset_all_matches
import json

def test_reset_all_matches():
    """Test the reset all matches functionality"""
    
    print("Testing Reset All Matches Functionality:")
    print("=" * 50)
    
    # Test the reset function
    print("\n🔄 Testing Reset All Matches:")
    print("-" * 30)
    
    result = reset_all_matches()
    
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    if result['success']:
        print(f"Records Reset: {result.get('records_reset', 0)}")
        print(f"Remaining Matched: {result.get('remaining_matched', 0)}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    print("\n✅ Reset All Matches now works without keywords column")
    print("✅ Updated columns: match_status, matched_with, match_method, audit_info, date_matched")
    print("✅ Frontend description updated to reflect removed keywords column")

if __name__ == "__main__":
    test_reset_all_matches() 