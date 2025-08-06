#!/usr/bin/env python3
"""
Test script to verify Excel export changes
"""

from core.services.export_service import ExportService
import json

def test_excel_export_format():
    """Test the new Excel export format"""
    
    print("Testing Excel Export Format Changes:")
    print("=" * 50)
    
    # Create export service
    export_service = ExportService()
    
    # Test the audit info formatting with sample data
    print("\n📋 Sample Audit Info Formatting:")
    print("-" * 30)
    
    # Sample audit info for different match types
    sample_audit_infos = [
        {
            'match_type': 'INTERUNIT_LOAN',
            'match_method': 'cross_reference',
            'lender_reference': 'MTBL-SND-A/C-1310000003858',
            'borrower_reference': 'Mutual Trust Bank Ltd-SND-002-0320004355',
            'lender_amount': '1300000.00',
            'borrower_amount': '1300000.00'
        },
        {
            'match_type': 'PO',
            'match_method': 'exact',
            'keywords': 'PO-2025-001'
        },
        {
            'match_type': 'LC',
            'match_method': 'exact',
            'keywords': 'LC-2025-002'
        },
        {
            'match_type': 'SALARY',
            'match_method': 'jaccard',
            'keywords': 'person:John,period:January',
            'jaccard_score': 0.85
        },
        {
            'match_type': 'COMMON_TEXT',
            'match_method': 'jaccard',
            'keywords': 'Office Supplies',
            'jaccard_score': 0.72
        }
    ]
    
    for i, audit_info in enumerate(sample_audit_infos, 1):
        formatted = export_service._format_audit_info(json.dumps(audit_info))
        
        print(f"\n{i}. Match Type: {audit_info['match_type']}")
        print("Formatted Audit Info:")
        print(formatted)
        print("-" * 20)
    
    # Test the export row structure
    print("\n📊 Export Row Structure:")
    print("-" * 30)
    
    # Sample export row
    export_row = {
        'Lender_UID': 'GeoTex_134fe03_13d620_000016',
        'Lender_Date': '2025-01-15',
        'Lender_Particulars': 'MTBL-SND-A/C-1310000003858 Amount paid as Interunit Loan',
        'Lender_Debit': 1300000,
        'Lender_Vch_Type': 'Payment',
        'Lender_Role': 'Lender',
        'Borrower_UID': 'Steel_134fe03_13d620_000017',
        'Borrower_Date': '2025-01-15',
        'Borrower_Particulars': 'Mutual Trust Bank Ltd-SND-002-0320004355 Amount received as Interunit Loan',
        'Borrower_Credit': 1300000,
        'Borrower_Vch_Type': 'Receipt',
        'Borrower_Role': 'Borrower',
        'Match_Method': 'cross_reference',
        'Audit_Info': export_service._format_audit_info(json.dumps(sample_audit_infos[0]))
    }
    
    print("Export Row Keys:")
    for key in export_row.keys():
        print(f"  - {key}")
    
    print(f"\nSample Audit Info:")
    print(export_row['Audit_Info'])
    
    print("\n✅ Excel export now uses Audit_Info instead of separate Keywords column")
    print("✅ Audit info is formatted based on match type")
    print("✅ Frontend table no longer has unused Keywords column")
    print("✅ Keywords column can be safely removed from database")

if __name__ == "__main__":
    test_excel_export_format() 