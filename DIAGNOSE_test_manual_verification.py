#!/usr/bin/env python3
"""
Test script to verify the new manual verification matching logic.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import find_matches

# Test data with entered_by field
test_data = [
    # Lender records (Debit > 0)
    {
        'uid': 'lender_001',
        'Company': 'GeoTex',
        'Particulars': 'Payment for office supplies',
        'Debit': 1000.0,
        'Credit': 0.0,
        'Date': '2025-01-15',
        'entered_by': 'john_doe',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'lender_002',
        'Company': 'GeoTex',
        'Particulars': 'Salary payment for January',
        'Debit': 5000.0,
        'Credit': 0.0,
        'Date': '2025-01-20',
        'entered_by': 'jane_smith',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'lender_003',
        'Company': 'GeoTex',
        'Particulars': 'Equipment purchase',
        'Debit': 2000.0,
        'Credit': 0.0,
        'Date': '2025-01-25',
        'entered_by': 'admin_user',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    
    # Borrower records (Credit > 0)
    {
        'uid': 'borrower_001',
        'Company': 'Steel',
        'Particulars': 'Office supplies received',
        'Debit': 0.0,
        'Credit': 1000.0,
        'Date': '2025-01-15',
        'entered_by': 'john_doe',  # Same as lender_001
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_002',
        'Company': 'Steel',
        'Particulars': 'Salary received for January',
        'Debit': 0.0,
        'Credit': 5000.0,
        'Date': '2025-01-20',
        'entered_by': 'jane_smith',  # Same as lender_002
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_003',
        'Company': 'Steel',
        'Particulars': 'Equipment received',
        'Debit': 0.0,
        'Credit': 2000.0,
        'Date': '2025-01-25',
        'entered_by': 'different_user',  # Different from lender_003
        'lender': 'GeoTex',
        'borrower': 'Steel'
    }
]

def main():
    print("Testing manual verification matching logic:")
    print("=" * 80)
    
    print("Test data:")
    for record in test_data:
        print(f"  {record['uid']}: {record['Company']} - {record['Particulars']} - {record['Debit']}/{record['Credit']} - entered_by: {record['entered_by']}")
    
    print("\nRunning matching logic...")
    matches = find_matches(test_data)
    
    print(f"\nFound {len(matches)} matches:")
    for i, match in enumerate(matches, 1):
        print(f"\n{i}. Match Type: {match['match_type']}")
        print(f"   Lender UID: {match['lender_uid']}")
        print(f"   Borrower UID: {match['borrower_uid']}")
        print(f"   Amount: {match['amount']}")
        
        if match['match_type'] == 'MANUAL_VERIFICATION':
            print(f"   Entered By: {match['entered_by']}")
            print(f"   Requires Verification: {match['audit_trail']['requires_verification']}")
            print(f"   Match Reason: {match['audit_trail']['match_reason']}")
        elif 'audit_trail' in match:
            print(f"   Audit Trail: {match['audit_trail']}")
    
    print("\n" + "=" * 80)
    print("Expected: 2 MANUAL_VERIFICATION matches (lender_001-borrower_001 and lender_002-borrower_002)")
    print("         1 other match type (lender_003-borrower_003 should match by other criteria)")

if __name__ == "__main__":
    main() 