#!/usr/bin/env python3
"""
Test to verify account number matching logic.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import find_matches, extract_account_number

# Test data with various account number patterns
test_data = [
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
    {
        'uid': 'borrower_002',
        'Company': 'Steel',
        'Particulars': 'Midland-CE-0011-1060000331-CI Interunit Fund Transfer as Interunit Loan A/C-Geo Textile Unit, EBL#00331',
        'Debit': 0.0,
        'Credit': 500000.0,
        'Date': '2025-01-20',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_003',
        'Company': 'Steel',
        'Particulars': 'Prime Bank-CD-2126117010855 Amount being paid as Principal & Interest of Time Loan',
        'Debit': 0.0,
        'Credit': 750000.0,
        'Date': '2025-01-25',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    }
]

def test_account_extraction():
    """Test account number extraction from various patterns."""
    print("Testing account number extraction:")
    print("=" * 60)
    
    test_cases = [
        "MDBL#11026",
        "OBL#8826", 
        "EBL#00331",
        "BBL#11026",
        "Midland Bank#11026",
        "One Bank#8826",
        "Eastern Bank#00331",
        "No account number here",
        "Random text #12345 more text"
    ]
    
    for case in test_cases:
        result = extract_account_number(case)
        if result:
            print(f"✅ '{case}' → Account: {result['account_number']}, Bank: {result.get('normalized_bank', 'N/A')}")
        else:
            print(f"❌ '{case}' → No account number found")

def main():
    print("Testing account number matching logic:")
    print("=" * 80)
    
    # Test account extraction first
    test_account_extraction()
    
    print("\n" + "=" * 80)
    print("Testing full matching logic:")
    
    print("Test data with account numbers:")
    for record in test_data:
        account_info = extract_account_number(record['Particulars'])
        if account_info:
            print(f"  {record['uid']}: {record['Company']} - Account: {account_info['account_number']}, Bank: {account_info.get('normalized_bank', 'N/A')}")
        else:
            print(f"  {record['uid']}: {record['Company']} - No account number found")
    
    print("\nRunning matching logic...")
    matches = find_matches(test_data)
    
    print(f"\nFound {len(matches)} matches:")
    account_matches = 0
    other_matches = 0
    
    for i, match in enumerate(matches, 1):
        print(f"\n{i}. Match Type: {match['match_type']}")
        print(f"   Lender UID: {match['lender_uid']}")
        print(f"   Borrower UID: {match['borrower_uid']}")
        print(f"   Amount: {match['amount']}")
        
        if match['match_type'] == 'INTERUNIT_LOAN':
            account_matches += 1
            print(f"   Account Number: {match['account_number']}")
            print(f"   Lender Bank: {match.get('lender_bank', 'N/A')}")
            print(f"   Borrower Bank: {match.get('borrower_bank', 'N/A')}")
            print(f"   Audit Trail: {match['audit_trail']}")
        else:
            other_matches += 1
            if 'audit_trail' in match:
                print(f"   Audit Trail: {match['audit_trail']}")
    
    print("\n" + "=" * 80)
    print(f"Summary: {account_matches} INTERUNIT_LOAN matches, {other_matches} other matches")
    print("Expected: 2 INTERUNIT_LOAN matches (8826 and 00331)")

if __name__ == "__main__":
    main() 