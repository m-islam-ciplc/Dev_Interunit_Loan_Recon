#!/usr/bin/env python3
"""
Test script to verify the fixed interunit keywords detection
"""

def test_fixed_interunit_keywords():
    """Test that the fixed interunit keywords detection works"""
    
    print("Testing Fixed INTERUNIT_LOAN Keywords Detection:")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            'name': 'Original Problem Case',
            'lender': "Prime Bank Limited-SND-2126318011502 Inter unit fund transfer as Interunit Loan A/C-Steel Unit, PBL#10855",
            'borrower': "Prime Bank-CD-2126117010855 Amount received as Interunit Loan A/C-Geo Textile Unit., PBL#11502"
        },
        {
            'name': 'Standard Case',
            'lender': "Midland Bank PLC-CD-A/C-0011-1050011026 Amount paid as Interunit Loan A/C-Steel Unit MDBL#00331",
            'borrower': "Midland-CE-0011-1060000331-CI Amount received as Interunit Loan A/C-Geo Textile Unit. MDBL#11026"
        },
        {
            'name': 'Fund Transfer Case',
            'lender': "One Bank-CD/A/C-0011020008826 Interunit fund transfer as Interunit Loan A/C-Steel Unit OBL#8826",
            'borrower': "One Bank-CD/A/C-0011020008826 Amount received as Interunit Loan A/C-Geo Textile Unit. OBL#8826"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        lender_lower = test_case['lender'].lower()
        borrower_lower = test_case['borrower'].lower()
        
        # Old logic (strict)
        old_lender_interunit = ('amount paid as interunit loan' in lender_lower or 
                               'interunit fund transfer' in lender_lower)
        old_borrower_interunit = ('amount received as interunit loan' in borrower_lower or 
                                 'interunit fund transfer' in borrower_lower)
        
        # New logic (flexible)
        new_lender_interunit = (
            'amount paid as interunit loan' in lender_lower or 
            'interunit fund transfer' in lender_lower or
            'inter unit fund transfer' in lender_lower or
            'interunit loan' in lender_lower
        )
        new_borrower_interunit = (
            'amount received as interunit loan' in borrower_lower or 
            'interunit fund transfer' in borrower_lower or
            'inter unit fund transfer' in borrower_lower or
            'interunit loan' in borrower_lower
        )
        
        print(f"   Lender: {test_case['lender'][:60]}...")
        print(f"   Borrower: {test_case['borrower'][:60]}...")
        print(f"   Old Logic - Lender: {old_lender_interunit}, Borrower: {old_borrower_interunit}")
        print(f"   New Logic - Lender: {new_lender_interunit}, Borrower: {new_borrower_interunit}")
        
        if old_lender_interunit and old_borrower_interunit:
            print(f"   ✅ Old Logic: INTERUNIT_LOAN MATCH")
        elif new_lender_interunit and new_borrower_interunit:
            print(f"   ✅ New Logic: INTERUNIT_LOAN MATCH (FIXED!)")
        else:
            print(f"   ❌ Neither Logic: MANUAL_VERIFICATION")
    
    print(f"\n✅ Summary:")
    print(f"   - Added 'inter unit fund transfer' (with space)")
    print(f"   - Added 'interunit loan' (shorter phrase)")
    print(f"   - More flexible keyword matching")
    print(f"   - Should catch more real-world interunit loan transactions")

if __name__ == "__main__":
    test_fixed_interunit_keywords() 