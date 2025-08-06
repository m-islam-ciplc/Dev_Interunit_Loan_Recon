#!/usr/bin/env python3
"""
Test to verify the updated Interunit Loan matching logic.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import find_matches, extract_account_number

# Test data with real interunit loan patterns
test_data = [
    # Real interunit loan transaction - different account numbers (as expected)
    {
        'uid': 'lender_001',
        'Company': 'GeoTex',
        'Particulars': 'Midland Bank PLC-CD-A/C-0011-1050011026 Amount paid as Interunit Loan A/C-Steel Unit MDBL # 00331',
        'Debit': 1000000.0,
        'Credit': 0.0,
        'Date': '2025-01-15',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_001',
        'Company': 'Steel',
        'Particulars': 'Midland-CE-0011-1060000331-CI Amount received as Interunit Loan A/C-Geo Textile Unit. MDBL # 11026',
        'Debit': 0.0,
        'Credit': 1000000.0,
        'Date': '2025-01-15',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    
    # Another real interunit loan transaction
    {
        'uid': 'lender_002',
        'Company': 'GeoTex',
        'Particulars': 'Prime Bank Limited-SND-2126318011502 Inter unit fund transfer as Interunit Loan A/C-Steel Unit, PBL#10855',
        'Debit': 500000.0,
        'Credit': 0.0,
        'Date': '2025-01-20',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_002',
        'Company': 'Steel',
        'Particulars': 'Prime Bank-CD-2126117010855 Amount received as Interunit Loan A/C-Geo Textile Unit., PBL#11502',
        'Debit': 0.0,
        'Credit': 500000.0,
        'Date': '2025-01-20',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    }
]

def main():
    print("Testing updated Interunit Loan matching logic:")
    print("=" * 80)
    
    print("Test scenarios:")
    print("1. lender_001 ↔ borrower_001: Different account numbers (00331 vs 11026) → EXPECTED: INTERUNIT_LOAN MATCH")
    print("2. lender_002 ↔ borrower_002: Different account numbers (10855 vs 11502) → EXPECTED: INTERUNIT_LOAN MATCH")
    
    print("\nTest data with account numbers:")
    for record in test_data:
        account_info = extract_account_number(record['Particulars'])
        is_interunit = ('interunit loan' in record['Particulars'].lower() or 
                       'amount paid as interunit loan' in record['Particulars'].lower() or
                       'amount received as interunit loan' in record['Particulars'].lower() or
                       'interunit fund transfer' in record['Particulars'].lower())
        
        if account_info:
            print(f"  {record['uid']}: {record['Company']} - Account: {account_info['account_number']}, Interunit: {is_interunit}")
            print(f"    Text: {record['Particulars']}")
        else:
            print(f"  {record['uid']}: {record['Company']} - No account number, Interunit: {is_interunit}")
            print(f"    Text: {record['Particulars']}")
    
    print("\nRunning matching logic...")
    matches = find_matches(test_data)
    
    print(f"\nFound {len(matches)} matches:")
    for i, match in enumerate(matches, 1):
        print(f"\n{i}. Match Type: {match['match_type']}")
        print(f"   Lender UID: {match['lender_uid']}")
        print(f"   Borrower UID: {match['borrower_uid']}")
        print(f"   Amount: {match['amount']}")
        
        if match['match_type'] == 'INTERUNIT_LOAN':
            print(f"   Account Number: {match.get('account_number', 'N/A')}")
            print(f"   Lender Bank: {match.get('lender_bank', 'N/A')}")
            print(f"   Borrower Bank: {match.get('borrower_bank', 'N/A')}")
            print(f"   Audit Trail: {match['audit_trail']}")
    
    print("\n" + "=" * 80)
    print("Expected: 2 INTERUNIT_LOAN matches (both scenarios)")
    print("         Both should match because they are interunit loan/fund transfer transactions")

if __name__ == "__main__":
    main() 