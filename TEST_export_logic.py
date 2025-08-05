#!/usr/bin/env python3
"""
Test the export logic to identify why Particulars columns are blank.
"""
from core import database
from core.services.export_service import ExportService

def test_export_logic():
    """Test the export logic step by step."""
    print("=== TESTING EXPORT LOGIC ===")
    
    # Get some matched data
    matched_data = database.get_matched_data()
    if not matched_data:
        print("No matched data found")
        return
    
    print(f"Testing with {len(matched_data)} matched records")
    
    # Test the first record
    first_record = matched_data[0]
    print(f"\nFirst record structure:")
    print(f"Keys: {list(first_record.keys())}")
    
    # Check the debit/credit values
    main_debit = first_record.get('Debit', 0)
    main_credit = first_record.get('Credit', 0)
    matched_debit = first_record.get('matched_Debit', 0)
    matched_credit = first_record.get('matched_Credit', 0)
    
    print(f"\nAmount values:")
    print(f"Main record - Debit: {main_debit}, Credit: {main_credit}")
    print(f"Matched record - Debit: {matched_debit}, Credit: {matched_credit}")
    
    # Check which record is lender/borrower
    main_record_debit = float(main_debit or 0)
    matched_record_debit = float(matched_debit or 0)
    
    print(f"\nDetermining lender/borrower:")
    print(f"Main record debit: {main_record_debit}")
    print(f"Matched record debit: {matched_record_debit}")
    
    if main_record_debit > 0:
        print("✅ Main record is lender (has debit)")
        lender_record_type = 'main'
        borrower_record_type = 'matched'
    elif matched_record_debit > 0:
        print("✅ Matched record is lender (has debit)")
        lender_record_type = 'matched'
        borrower_record_type = 'main'
    else:
        print("❌ Neither record has debit - using fallback")
        lender_record_type = 'main'
        borrower_record_type = 'matched'
    
    # Test the extraction logic
    print(f"\nTesting extraction logic:")
    print(f"Lender record type: {lender_record_type}")
    print(f"Borrower record type: {borrower_record_type}")
    
    # Test lender data extraction
    prefix = '' if lender_record_type == 'main' else 'matched_'
    lender_particulars_key = f'{prefix}Particulars' if prefix else 'Particulars'
    lender_particulars_value = first_record.get(lender_particulars_key, '')
    
    print(f"Lender particulars key: '{lender_particulars_key}'")
    print(f"Lender particulars value: '{lender_particulars_value}'")
    
    # Test borrower data extraction
    prefix = '' if borrower_record_type == 'main' else 'matched_'
    borrower_particulars_key = f'{prefix}Particulars' if prefix else 'Particulars'
    borrower_particulars_value = first_record.get(borrower_particulars_key, '')
    
    print(f"Borrower particulars key: '{borrower_particulars_key}'")
    print(f"Borrower particulars value: '{borrower_particulars_value}'")
    
    # Test the actual export service methods
    print(f"\nTesting ExportService methods:")
    export_service = ExportService()
    
    # Test lender data extraction
    lender_data = export_service._extract_lender_data(first_record, lender_record_type)
    print(f"Lender data: {lender_data}")
    
    # Test borrower data extraction
    borrower_data = export_service._extract_borrower_data(first_record, borrower_record_type)
    print(f"Borrower data: {borrower_data}")
    
    # Check if the issue is in the logic
    if not lender_data.get('Lender_Particulars'):
        print("❌ ISSUE: Lender_Particulars is empty!")
    else:
        print("✅ Lender_Particulars has data")
        
    if not borrower_data.get('Borrower_Particulars'):
        print("❌ ISSUE: Borrower_Particulars is empty!")
    else:
        print("✅ Borrower_Particulars has data")

if __name__ == "__main__":
    test_export_logic() 