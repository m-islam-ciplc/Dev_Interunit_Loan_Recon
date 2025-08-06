#!/usr/bin/env python3
"""
Comprehensive test for manual verification matching logic.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import find_matches

# Test data with various scenarios
test_data = [
    # Scenario 1: Manual verification match (same entered_by, same amounts)
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
    
    # Scenario 2: Manual verification match (same entered_by, same amounts)
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
    
    # Scenario 3: NO manual verification match (different entered_by)
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
    },
    
    # Scenario 4: NO manual verification match (different amounts)
    {
        'uid': 'lender_004',
        'Company': 'GeoTex',
        'Particulars': 'Service payment',
        'Debit': 3000.0,
        'Credit': 0.0,
        'Date': '2025-01-30',
        'entered_by': 'same_user',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_004',
        'Company': 'Steel',
        'Particulars': 'Service received',
        'Debit': 0.0,
        'Credit': 2500.0,  # Different amount
        'Date': '2025-01-30',
        'entered_by': 'same_user',  # Same as lender_004
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    
    # Scenario 5: NO manual verification match (missing entered_by)
    {
        'uid': 'lender_005',
        'Company': 'GeoTex',
        'Particulars': 'Utility payment',
        'Debit': 1500.0,
        'Credit': 0.0,
        'Date': '2025-02-01',
        'entered_by': '',  # Empty
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_005',
        'Company': 'Steel',
        'Particulars': 'Utility received',
        'Debit': 0.0,
        'Credit': 1500.0,
        'Date': '2025-02-01',
        'entered_by': '',  # Empty
        'lender': 'GeoTex',
        'borrower': 'Steel'
    }
]

def main():
    print("Comprehensive testing of manual verification matching logic:")
    print("=" * 80)
    
    print("Test scenarios:")
    print("1. lender_001 ↔ borrower_001: Same entered_by (john_doe), same amounts → EXPECTED: MANUAL_VERIFICATION")
    print("2. lender_002 ↔ borrower_002: Same entered_by (jane_smith), same amounts → EXPECTED: MANUAL_VERIFICATION")
    print("3. lender_003 ↔ borrower_003: Different entered_by → EXPECTED: NO MANUAL_VERIFICATION")
    print("4. lender_004 ↔ borrower_004: Same entered_by, different amounts → EXPECTED: NO MANUAL_VERIFICATION")
    print("5. lender_005 ↔ borrower_005: Empty entered_by → EXPECTED: NO MANUAL_VERIFICATION")
    
    print("\nRunning matching logic...")
    matches = find_matches(test_data)
    
    print(f"\nFound {len(matches)} matches:")
    manual_verification_count = 0
    other_match_count = 0
    
    for i, match in enumerate(matches, 1):
        print(f"\n{i}. Match Type: {match['match_type']}")
        print(f"   Lender UID: {match['lender_uid']}")
        print(f"   Borrower UID: {match['borrower_uid']}")
        print(f"   Amount: {match['amount']}")
        
        if match['match_type'] == 'MANUAL_VERIFICATION':
            manual_verification_count += 1
            print(f"   Entered By: {match['entered_by']}")
            print(f"   Requires Verification: {match['audit_trail']['requires_verification']}")
            print(f"   Match Reason: {match['audit_trail']['match_reason']}")
        else:
            other_match_count += 1
            if 'audit_trail' in match:
                print(f"   Audit Trail: {match['audit_trail']}")
    
    print("\n" + "=" * 80)
    print(f"Summary: {manual_verification_count} MANUAL_VERIFICATION matches, {other_match_count} other matches")
    print("Expected: 2 MANUAL_VERIFICATION matches (scenarios 1 and 2)")

if __name__ == "__main__":
    main() 