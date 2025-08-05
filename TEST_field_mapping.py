#!/usr/bin/env python3
"""
Test the field name mapping in export service.
"""
from core import database

def test_field_mapping():
    """Test the field name mapping issue."""
    print("=== TESTING FIELD NAME MAPPING ===")
    
    # Get matched data
    matched_data = database.get_matched_data()
    if not matched_data:
        print("No matched data found")
        return
    
    first_record = matched_data[0]
    print(f"First record keys: {list(first_record.keys())}")
    
    # Check the actual field names
    print(f"\nChecking field names:")
    print(f"'Particulars' in keys: {'Particulars' in first_record}")
    print(f"'matched_particulars' in keys: {'matched_particulars' in first_record}")
    
    # Check the actual values
    print(f"\nChecking values:")
    print(f"Particulars: '{first_record.get('Particulars', 'N/A')}'")
    print(f"matched_particulars: '{first_record.get('matched_particulars', 'N/A')}'")
    
    # Test the export service logic
    print(f"\nTesting export service logic:")
    
    # Simulate the export service logic
    main_record_debit = float(first_record.get('Debit', 0) or 0)
    matched_record_debit = float(first_record.get('matched_Debit', 0) or 0)
    
    print(f"Main record debit: {main_record_debit}")
    print(f"Matched record debit: {matched_record_debit}")
    
    if main_record_debit > 0:
        print("Main record is lender")
        lender_record_type = 'main'
        borrower_record_type = 'matched'
    elif matched_record_debit > 0:
        print("Matched record is lender")
        lender_record_type = 'matched'
        borrower_record_type = 'main'
    else:
        print("Using fallback")
        lender_record_type = 'main'
        borrower_record_type = 'matched'
    
    # Test the field name construction
    print(f"\nTesting field name construction:")
    
    # For lender (matched record type)
    prefix = '' if lender_record_type == 'main' else 'matched_'
    lender_particulars_key = f'{prefix}Particulars' if prefix else 'Particulars'
    print(f"Lender record type: {lender_record_type}")
    print(f"Lender prefix: '{prefix}'")
    print(f"Lender particulars key: '{lender_particulars_key}'")
    print(f"Lender particulars value: '{first_record.get(lender_particulars_key, 'N/A')}'")
    
    # For borrower (main record type)
    prefix = '' if borrower_record_type == 'main' else 'matched_'
    borrower_particulars_key = f'{prefix}Particulars' if prefix else 'Particulars'
    print(f"Borrower record type: {borrower_record_type}")
    print(f"Borrower prefix: '{prefix}'")
    print(f"Borrower particulars key: '{borrower_particulars_key}'")
    print(f"Borrower particulars value: '{first_record.get(borrower_particulars_key, 'N/A')}'")

if __name__ == "__main__":
    test_field_mapping() 