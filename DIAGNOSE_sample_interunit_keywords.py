#!/usr/bin/env python3
"""
Sample script to show what INTERUNIT_LOAN keywords should look like
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import find_matches
from core.database import update_matches
import json

def show_sample_interunit_keywords():
    """Show sample INTERUNIT_LOAN keywords"""
    
    # Sample data that would trigger INTERUNIT_LOAN match
    sample_data = [
        {
            'uid': 'GeoTex_sample_001',
            'lender': 'GeoTex',
            'borrower': 'Steel',
            'Debit': 100000,
            'Credit': 0,
            'Particulars': 'MTBL-SND-A/C-1310000003858 Amount paid as Interunit Loan A/C-Steel Unit,MTBL#4355',
            'entered_by': 'user1'
        },
        {
            'uid': 'Steel_sample_001',
            'lender': 'GeoTex',
            'borrower': 'Steel',
            'Debit': 0,
            'Credit': 100000,
            'Particulars': 'Mutual Trust Bank Ltd-SND-002-0320004355 Amount received as Interunit Loan A/C-Geo Textile Unit.,MTBL#3858',
            'entered_by': 'user2'
        }
    ]
    
    print("Sample INTERUNIT_LOAN Match Display in HTML Table:")
    print("=" * 70)
    
    # Find matches using the matching logic
    matches = find_matches(sample_data)
    
    for match in matches:
        if match['match_type'] == 'INTERUNIT_LOAN':
            print(f"\n📋 HTML Table Row Example:")
            print(f"┌─────────────────────────────────────────────────────────────────┐")
            print(f"│ Pair ID: GeoTex_sample_001 ↔ Steel_sample_001                │")
            print(f"│ Amount: 100,000                                              │")
            print(f"│ Type: INTERUNIT_LOAN                                         │")
            print(f"│ Keywords: Lender: amount paid as interunit loan, interunit   │")
            print(f"│           fund transfer, Borrower: amount received as         │")
            print(f"│           interunit loan, interunit fund transfer             │")
            print(f"│ Method: cross_reference                                       │")
            print(f"│ Status: confirmed                                             │")
            print(f"└─────────────────────────────────────────────────────────────────┘")
            
            print(f"\n🔍 Current Problem (What you see now):")
            print(f"┌─────────────────────────────────────────────────────────────────┐")
            print(f"│ Pair ID: GeoTex_sample_001 ↔ Steel_sample_001                │")
            print(f"│ Amount: 100,000                                              │")
            print(f"│ Type: INTERUNIT_LOAN                                         │")
            print(f"│ Keywords: Type: INTERUNIT_LOAN                               │")
            print(f"│ Method: (empty)                                              │")
            print(f"│ Status: confirmed                                             │")
            print(f"└─────────────────────────────────────────────────────────────────┘")
            
            print(f"\n✅ After Fix (What you should see):")
            print(f"┌─────────────────────────────────────────────────────────────────┐")
            print(f"│ Pair ID: GeoTex_sample_001 ↔ Steel_sample_001                │")
            print(f"│ Amount: 100,000                                              │")
            print(f"│ Type: INTERUNIT_LOAN                                         │")
            print(f"│ Keywords: Lender: amount paid as interunit loan, interunit   │")
            print(f"│           fund transfer, Borrower: amount received as         │")
            print(f"│           interunit loan, interunit fund transfer             │")
            print(f"│ Method: cross_reference                                       │")
            print(f"│ Status: confirmed                                             │")
            print(f"└─────────────────────────────────────────────────────────────────┘")
            
            print(f"\n📊 Database Storage:")
            print(f"   keywords column: 'Lender: amount paid as interunit loan, interunit fund transfer, Borrower: amount received as interunit loan, interunit fund transfer'")
            print(f"   match_method column: 'cross_reference'")
            print(f"   match_status column: 'confirmed'")
            
            print(f"\n🔧 To Fix This:")
            print(f"   1. Go to Database Tools tab")
            print(f"   2. Click 'Reset All Matches' button")
            print(f"   3. Run reconciliation again")
            print(f"   4. Check Matched Results - keywords will show actual keywords")

if __name__ == "__main__":
    show_sample_interunit_keywords() 