#!/usr/bin/env python3
"""
Sample to show how INTERUNIT_LOAN audit info should be displayed
"""

def show_audit_info_sample():
    """Show sample audit info display for INTERUNIT_LOAN matches"""
    
    print("Sample INTERUNIT_LOAN Match - Audit Info Display:")
    print("=" * 60)
    
    print("\n📋 Sample Data:")
    print("Lender Particulars: MTBL-SND-A/C-1310000003858 Amount paid as Interunit Loan A/C-Steel Unit,MTBL#4355")
    print("Borrower Particulars: Mutual Trust Bank Ltd-SND-002-0320004355 Amount received as Interunit Loan A/C-Geo Textile Unit.,MTBL#3858")
    print("Amount: 100,000")
    
    print("\n🔍 Current Display (What you see now):")
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ Type: INTERUNIT_LOAN                                          │")
    print("│ Keywords: Lender: amount paid as interunit loan, interunit   │")
    print("│           fund transfer, Borrower: amount received as         │")
    print("│           interunit loan, interunit fund transfer             │")
    print("└─────────────────────────────────────────────────────────────────┘")
    
    print("\n❓ How do you want the audit info to be displayed?")
    print("Please tell me the exact format you prefer. For example:")
    print("")
    print("Option 1:")
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ Interunit Loan Match                                          │")
    print("│ Lender: MTBL-SND-A/C-1310000003858                           │")
    print("│ Borrower: Mutual Trust Bank Ltd-SND-002-0320004355           │")
    print("│ Cross-Reference: 03858 ↔ 04355                               │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print("")
    print("Option 2:")
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ Type: INTERUNIT_LOAN                                          │")
    print("│ Method: Cross-Reference                                       │")
    print("│ Lender Account: 1310000003858                                 │")
    print("│ Borrower Account: 0320004355                                  │")
    print("│ Reference: MTBL#4355 ↔ MTBL#3858                             │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print("")
    print("Option 3:")
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ INTERUNIT_LOAN Match                                          │")
    print("│ Keywords: amount paid as interunit loan, amount received as   │")
    print("│           interunit loan                                      │")
    print("│ Account Match: 03858 ↔ 04355                                  │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print("")
    print("Or tell me your preferred format exactly as you want it to appear!")

if __name__ == "__main__":
    show_audit_info_sample() 