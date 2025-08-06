#!/usr/bin/env python3
"""
Diagnostic script to debug why specific transaction isn't being matched as INTERUNIT_LOAN
"""

import re

def debug_interunit_matching():
    """Debug why the specific transaction isn't being matched as INTERUNIT_LOAN"""
    
    print("Debugging INTERUNIT_LOAN Matching:")
    print("=" * 50)
    
    # The specific transaction details
    lender_particulars = "Prime Bank Limited-SND-2126318011502 Inter unit fund transfer as Interunit Loan A/C-Steel Unit, PBL#10855"
    borrower_particulars = "Prime Bank-CD-2126117010855 Amount received as Interunit Loan A/C-Geo Textile Unit., PBL#11502"
    
    print(f"\n📋 Lender Particulars: {lender_particulars}")
    print(f"📋 Borrower Particulars: {borrower_particulars}")
    
    # Check interunit loan keywords
    is_lender_interunit = ('amount paid as interunit loan' in lender_particulars.lower() or 
                          'interunit fund transfer' in lender_particulars.lower())
    is_borrower_interunit = ('amount received as interunit loan' in borrower_particulars.lower() or 
                            'interunit fund transfer' in borrower_particulars.lower())
    
    print(f"\n✅ Interunit Keywords Check:")
    print(f"   Lender interunit: {is_lender_interunit}")
    print(f"   Borrower interunit: {is_borrower_interunit}")
    print(f"   Both interunit: {is_lender_interunit and is_borrower_interunit}")
    
    # Test account number extraction patterns
    print(f"\n🔍 Account Number Extraction:")
    
    # Pattern 1: For lender - extract full account number after bank name
    lender_account_match = re.search(r'([A-Za-z\s-]+[A-Za-z])-?[A-Za-z0-9/-]*(\d{13})', lender_particulars)
    print(f"   Pattern 1 - Lender: {lender_account_match.group() if lender_account_match else 'NOT FOUND'}")
    
    # Pattern 2: For borrower - extract hyphenated account number
    borrower_account_match = re.search(r'([A-Za-z\s-]+[A-Za-z])-?[A-Za-z0-9/-]*(\d{3}-\d{10})', borrower_particulars)
    print(f"   Pattern 2 - Borrower: {borrower_account_match.group() if borrower_account_match else 'NOT FOUND'}")
    
    # Pattern 3: Fallback for any account number format
    if not lender_account_match:
        lender_account_match = re.search(r'([A-Za-z\s-]+[A-Za-z])-?[A-Za-z0-9/-]*(\d{10,})', lender_particulars)
        print(f"   Pattern 3 - Lender: {lender_account_match.group() if lender_account_match else 'NOT FOUND'}")
    
    if not borrower_account_match:
        borrower_account_match = re.search(r'([A-Za-z\s-]+[A-Za-z])-?[A-Za-z0-9/-]*(\d{10,})', borrower_particulars)
        print(f"   Pattern 3 - Borrower: {borrower_account_match.group() if borrower_account_match else 'NOT FOUND'}")
    
    # Manual extraction for specific patterns
    if not lender_account_match:
        lender_account_match = re.search(r'Prime Bank Limited-SND-(\d{13})', lender_particulars)
        print(f"   Manual - Lender: {lender_account_match.group() if lender_account_match else 'NOT FOUND'}")
    
    if not borrower_account_match:
        borrower_account_match = re.search(r'Prime Bank-CD-(\d{13})', borrower_particulars)
        print(f"   Manual - Borrower: {borrower_account_match.group() if borrower_account_match else 'NOT FOUND'}")
    
    # Check if both account numbers were found
    if lender_account_match and borrower_account_match:
        print(f"\n✅ Both Account Numbers Found:")
        lender_account_full = lender_account_match.group(2) if len(lender_account_match.groups()) > 1 else lender_account_match.group(1)
        borrower_account_full = borrower_account_match.group(2) if len(borrower_account_match.groups()) > 1 else borrower_account_match.group(1)
        
        print(f"   Lender Account: {lender_account_full}")
        print(f"   Borrower Account: {borrower_account_full}")
        
        # Extract last 4-5 digits
        lender_last_digits = lender_account_full[-5:] if len(lender_account_full) >= 5 else lender_account_full[-4:]
        borrower_last_digits = borrower_account_full[-5:] if len(borrower_account_full) >= 5 else borrower_account_full[-4:]
        
        print(f"   Lender Last Digits: {lender_last_digits}")
        print(f"   Borrower Last Digits: {borrower_last_digits}")
        
        # Cross-reference check
        cross_ref_1_found = lender_last_digits in borrower_particulars
        cross_ref_2_found = borrower_last_digits in lender_particulars
        
        print(f"\n🔍 Cross-Reference Check:")
        print(f"   Lender digits in borrower: {cross_ref_1_found}")
        print(f"   Borrower digits in lender: {cross_ref_2_found}")
        
        # Alternative: Look for the shortened references in the narrations
        if not cross_ref_1_found:
            borrower_short_ref = re.search(r'#(\d{4,5})', borrower_particulars)
            if borrower_short_ref:
                cross_ref_1_found = borrower_short_ref.group(1) in lender_last_digits
                print(f"   Alternative cross-ref 1: {cross_ref_1_found} (found {borrower_short_ref.group(1)})")
        
        if not cross_ref_2_found:
            lender_short_ref = re.search(r'#(\d{4,5})', lender_particulars)
            if lender_short_ref:
                cross_ref_2_found = lender_short_ref.group(1) in borrower_last_digits
                print(f"   Alternative cross-ref 2: {cross_ref_2_found} (found {lender_short_ref.group(1)})")
        
        # Final result
        if cross_ref_1_found and cross_ref_2_found:
            print(f"\n✅ INTERUNIT_LOAN MATCH - Should be auto-accepted!")
        else:
            print(f"\n❌ NOT INTERUNIT_LOAN MATCH - Cross-reference failed")
            print(f"   This is why it falls back to MANUAL_VERIFICATION")
    else:
        print(f"\n❌ Account Numbers Not Found:")
        print(f"   Lender account match: {lender_account_match}")
        print(f"   Borrower account match: {borrower_account_match}")
        print(f"   This is why it falls back to MANUAL_VERIFICATION")

if __name__ == "__main__":
    debug_interunit_matching() 