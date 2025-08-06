#!/usr/bin/env python3
"""
Test to verify the cross-reference Interunit Loan matching logic.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import find_matches
import re

# Test data with real interunit loan patterns
test_data = [
    # Real interunit loan transaction with cross-references
    {
        'uid': 'lender_001',
        'Company': 'GeoTex',
        'Particulars': 'MTBL-SND-A/C-1310000003858 Amount paid as Interunit Loan A/C-Steel Unit,MTBL#4355',
        'Debit': 1000000.0,
        'Credit': 0.0,
        'Date': '2025-01-15',
        'lender': 'GeoTex',
        'borrower': 'Steel'
    },
    {
        'uid': 'borrower_001',
        'Company': 'Steel',
        'Particulars': 'Mutual Trust Bank Ltd-SND-002-0320004355 Amount received as Interunit Loan A/C-Geo Textile Unit.,MTBL#3858',
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

def test_account_extraction():
    """Test account number extraction from narrations."""
    print("Testing account number extraction:")
    print("=" * 60)
    
    for record in test_data:
        particulars = record['Particulars']
        account_match = re.search(r'([A-Za-z\s-]+[A-Za-z])-?[A-Za-z0-9/-]*(\d{10,})', particulars)
        
        if account_match:
            bank_name = account_match.group(1)
            account_number = account_match.group(2)
            last_digits = account_number[-5:] if len(account_number) >= 5 else account_number[-4:]
            
            print(f"  {record['uid']}: {record['Company']}")
            print(f"    Bank: {bank_name}")
            print(f"    Account: {account_number}")
            print(f"    Last digits: {last_digits}")
            print(f"    Text: {particulars}")
            print()
        else:
            print(f"  {record['uid']}: No account number found")
            print(f"    Text: {particulars}")
            print()

def main():
    print("Testing cross-reference Interunit Loan matching logic:")
    print("=" * 80)
    
    print("Test scenarios:")
    print("1. lender_001 ↔ borrower_001: Cross-reference match → EXPECTED: INTERUNIT_LOAN MATCH")
    print("2. lender_002 ↔ borrower_002: Cross-reference match → EXPECTED: INTERUNIT_LOAN MATCH")
    
    # Test account extraction first
    test_account_extraction()
    
    print("Running matching logic...")
    matches = find_matches(test_data)
    
    print(f"\nFound {len(matches)} matches:")
    for i, match in enumerate(matches, 1):
        print(f"\n{i}. Match Type: {match['match_type']}")
        print(f"   Lender UID: {match['lender_uid']}")
        print(f"   Borrower UID: {match['borrower_uid']}")
        print(f"   Amount: {match['amount']}")
        
        if match['match_type'] == 'INTERUNIT_LOAN':
            print(f"   Lender Account: {match.get('lender_account', 'N/A')}")
            print(f"   Borrower Account: {match.get('borrower_account', 'N/A')}")
            print(f"   Lender Last Digits: {match.get('lender_last_digits', 'N/A')}")
            print(f"   Borrower Last Digits: {match.get('borrower_last_digits', 'N/A')}")
            print(f"   Audit Trail: {match['audit_trail']}")
    
    print("\n" + "=" * 80)
    print("Expected: 2 INTERUNIT_LOAN matches (both scenarios)")
    print("         Both should match because cross-references are found")

if __name__ == "__main__":
    main() 