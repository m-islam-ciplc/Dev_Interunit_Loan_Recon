#!/usr/bin/env python3
"""
Test to verify interunit loan validation for account number matching.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import find_matches, extract_account_number

# Test data with various scenarios
test_data = [
    # VALID: Both are interunit loan transactions with same account number
    {
        'uid': 'lender_001',
        'Company': 'GeoTex',
        'Particulars': 'Midland Bank PLC-CD-A/C-0011-1050011026 Amount paid as Interunit Loan A/C-Steel Unit OBL#8826',
        'Debit': 1000000.0,
        'Credit': 0.0,
        'Date': '2025-01-15',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_001',
        'Company': 'Steel',
        'Particulars': 'One Bank-CD/A/C-0011020008826 Amount received as Interunit Loan A/C-Geo Textile Unit. MDBL#8826',
        'Debit': 0.0,
        'Credit': 1000000.0,
        'Date': '2025-01-15',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    
    # INVALID: Same account number but NOT interunit loan transactions
    {
        'uid': 'lender_002',
        'Company': 'GeoTex',
        'Particulars': 'Payment for office supplies OBL#8826',
        'Debit': 50000.0,
        'Credit': 0.0,
        'Date': '2025-01-20',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_002',
        'Company': 'Steel',
        'Particulars': 'Office supplies received MDBL#8826',
        'Debit': 0.0,
        'Credit': 50000.0,
        'Date': '2025-01-20',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    
    # VALID: Both are interunit loan transactions with same account number
    {
        'uid': 'lender_003',
        'Company': 'GeoTex',
        'Particulars': 'Eastern Bank Limited-SND-1011060605503 Interunit fund transfer as Interunit Loan A/C-Steel Unit, MDBL#00331',
        'Debit': 500000.0,
        'Credit': 0.0,
        'Date': '2025-01-25',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_003',
        'Company': 'Steel',
        'Particulars': 'Midland-CE-0011-1060000331-CI Interunit Fund Transfer as Interunit Loan A/C-Geo Textile Unit, EBL#00331',
        'Debit': 0.0,
        'Credit': 500000.0,
        'Date': '2025-01-25',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    }
]

def main():
    print("Testing interunit loan validation for account number matching:")
    print("=" * 80)
    
    print("Test scenarios:")
    print("1. lender_001 ↔ borrower_001: Same account (8826), BOTH interunit loan → EXPECTED: MATCH")
    print("2. lender_002 ↔ borrower_002: Same account (8826), NOT interunit loan → EXPECTED: NO MATCH")
    print("3. lender_003 ↔ borrower_003: Same account (00331), BOTH interunit loan → EXPECTED: MATCH")
    
    print("\nTest data with account numbers and interunit validation:")
    for record in test_data:
        account_info = extract_account_number(record['Particulars'])
        is_interunit = 'interunit loan' in record['Particulars'].lower() or 'amount paid as interunit loan' in record['Particulars'].lower() or 'amount received as interunit loan' in record['Particulars'].lower()
        
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
            print(f"   Account Number: {match['account_number']}")
            print(f"   Lender Bank: {match.get('lender_bank', 'N/A')}")
            print(f"   Borrower Bank: {match.get('borrower_bank', 'N/A')}")
            print(f"   Audit Trail: {match['audit_trail']}")
    
    print("\n" + "=" * 80)
    print("Expected: 2 INTERUNIT_LOAN matches (scenarios 1 and 3)")
    print("         Scenario 2 should NOT match because it's not interunit loan")

if __name__ == "__main__":
    main() 