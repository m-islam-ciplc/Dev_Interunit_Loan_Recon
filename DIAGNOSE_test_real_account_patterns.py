#!/usr/bin/env python3
"""
Test with real account number patterns from user data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import find_matches, extract_account_number

# Real data patterns from user
test_data = [
    # Lender record
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
    
    # Borrower record - should match lender_001
    {
        'uid': 'borrower_001',
        'Company': 'Steel',
        'Particulars': 'One Bank-CD/A/C-0011020008826 Amount received as Interunit Loan A/C-Geo Textile Unit. MDBL#11026',
        'Debit': 0.0,
        'Credit': 1000000.0,
        'Date': '2025-01-15',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    
    # Another lender record
    {
        'uid': 'lender_002',
        'Company': 'GeoTex',
        'Particulars': 'Eastern Bank Limited-SND-1011060605503 Interunit fund transfer as Interunit Loan A/C-Steel Unit, MDBL#00331',
        'Debit': 500000.0,
        'Credit': 0.0,
        'Date': '2025-01-20',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    
    # Another borrower record - should match lender_002
    {
        'uid': 'borrower_002',
        'Company': 'Steel',
        'Particulars': 'Midland-CE-0011-1060000331-CI Interunit Fund Transfer as Interunit Loan A/C-Geo Textile Unit, EBL#00331',
        'Debit': 0.0,
        'Credit': 500000.0,
        'Date': '2025-01-20',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    }
]

def main():
    print("Testing real account number patterns:")
    print("=" * 80)
    
    print("Test data with account numbers:")
    for record in test_data:
        account_info = extract_account_number(record['Particulars'])
        if account_info:
            print(f"  {record['uid']}: {record['Company']} - Account: {account_info['account_number']}, Bank: {account_info.get('normalized_bank', 'N/A')}")
            print(f"    Text: {record['Particulars']}")
        else:
            print(f"  {record['uid']}: {record['Company']} - No account number found")
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
    print("Expected: 2 INTERUNIT_LOAN matches (8826 and 00331)")

if __name__ == "__main__":
    main() 