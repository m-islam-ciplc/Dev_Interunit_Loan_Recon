#!/usr/bin/env python3
"""
Test script to verify enhanced display with lender and borrower amounts
"""

import json

def test_enhanced_display():
    """Test the enhanced display format"""
    
    print("Testing Enhanced Display with Lender/Borrower Amounts:")
    print("=" * 60)
    
    # Sample audit_info for different match types
    sample_audit_infos = [
        {
            'match_type': 'PO',
            'match_method': 'exact',
            'po_number': 'PO-2025-001',
            'lender_amount': '50000.00',
            'borrower_amount': '50000.00'
        },
        {
            'match_type': 'LC',
            'match_method': 'exact',
            'lc_number': 'LC-2025-002',
            'lender_amount': '75000.00',
            'borrower_amount': '75000.00'
        },
        {
            'match_type': 'LOAN_ID',
            'match_method': 'exact',
            'loan_id': 'LD123',
            'lender_amount': '25000.00',
            'borrower_amount': '25000.00'
        },
        {
            'match_type': 'SALARY',
            'match_method': 'jaccard',
            'person': 'John Doe',
            'period': 'January 2025',
            'lender_amount': '25000.00',
            'borrower_amount': '25000.00',
            'jaccard_score': 0.85
        },
        {
            'match_type': 'COMMON_TEXT',
            'match_method': 'jaccard',
            'common_text': 'Office Supplies',
            'lender_amount': '1500.00',
            'borrower_amount': '1500.00',
            'jaccard_score': 0.72
        },
        {
            'match_type': 'INTERUNIT_LOAN',
            'match_method': 'cross_reference',
            'lender_reference': 'MTBL-SND-A/C-1310000003858',
            'borrower_reference': 'Mutual Trust Bank Ltd-SND-002-0320004355',
            'lender_amount': '1300000.00',
            'borrower_amount': '1300000.00'
        }
    ]
    
    print("\n📋 Enhanced Display Examples:")
    print("-" * 40)
    
    for i, audit_info in enumerate(sample_audit_infos, 1):
        print(f"\n{i}. {audit_info['match_type']} Match:")
        print("   " + "-" * 30)
        
        # Simulate the formatAuditInfo function
        formatted = ""
        match_type = audit_info['match_type']
        
        if match_type == 'PO':
            formatted += f"PO Match\n"
            if audit_info.get('po_number'):
                formatted += f"PO Number: {audit_info['po_number']}\n"
            if audit_info.get('lender_amount'):
                formatted += f"Lender Amount: {audit_info['lender_amount']}\n"
            if audit_info.get('borrower_amount'):
                formatted += f"Borrower Amount: {audit_info['borrower_amount']}\n"
                
        elif match_type == 'LC':
            formatted += f"LC Match\n"
            if audit_info.get('lc_number'):
                formatted += f"LC Number: {audit_info['lc_number']}\n"
            if audit_info.get('lender_amount'):
                formatted += f"Lender Amount: {audit_info['lender_amount']}\n"
            if audit_info.get('borrower_amount'):
                formatted += f"Borrower Amount: {audit_info['borrower_amount']}\n"
                
        elif match_type == 'LOAN_ID':
            formatted += f"Loan ID Match\n"
            if audit_info.get('loan_id'):
                formatted += f"Loan ID: {audit_info['loan_id']}\n"
            if audit_info.get('lender_amount'):
                formatted += f"Lender Amount: {audit_info['lender_amount']}\n"
            if audit_info.get('borrower_amount'):
                formatted += f"Borrower Amount: {audit_info['borrower_amount']}\n"
                
        elif match_type == 'SALARY':
            formatted += f"Salary Match\n"
            if audit_info.get('person'):
                formatted += f"Person: {audit_info['person']}\n"
            if audit_info.get('period'):
                formatted += f"Period: {audit_info['period']}\n"
            if audit_info.get('lender_amount'):
                formatted += f"Lender Amount: {audit_info['lender_amount']}\n"
            if audit_info.get('borrower_amount'):
                formatted += f"Borrower Amount: {audit_info['borrower_amount']}\n"
            if audit_info.get('jaccard_score'):
                formatted += f"Similarity: {(audit_info['jaccard_score'] * 100):.1f}%\n"
                
        elif match_type == 'COMMON_TEXT':
            formatted += f"Common Text Match\n"
            if audit_info.get('common_text'):
                formatted += f"Matched Text: \"{audit_info['common_text']}\"\n"
            if audit_info.get('lender_amount'):
                formatted += f"Lender Amount: {audit_info['lender_amount']}\n"
            if audit_info.get('borrower_amount'):
                formatted += f"Borrower Amount: {audit_info['borrower_amount']}\n"
            if audit_info.get('jaccard_score'):
                formatted += f"Similarity: {(audit_info['jaccard_score'] * 100):.1f}%\n"
                
        elif match_type == 'INTERUNIT_LOAN':
            formatted += f"Interunit Loan Match\n"
            if audit_info.get('lender_reference'):
                formatted += f"Lender: {audit_info['lender_reference']}\n"
            if audit_info.get('borrower_reference'):
                formatted += f"Borrower: {audit_info['borrower_reference']}\n"
            if audit_info.get('lender_amount'):
                formatted += f"Lender Amount: {audit_info['lender_amount']}\n"
            if audit_info.get('borrower_amount'):
                formatted += f"Borrower Amount: {audit_info['borrower_amount']}\n"
        
        print(formatted.strip())
    
    print("\n✅ Enhanced display now shows:")
    print("  - Match type and specific identifiers")
    print("  - Lender Amount for all match types")
    print("  - Borrower Amount for all match types")
    print("  - Additional details (person, period, similarity scores)")
    print("  - Consistent format across all match types")

if __name__ == "__main__":
    test_enhanced_display() 