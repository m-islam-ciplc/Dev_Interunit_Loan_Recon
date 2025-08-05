#!/usr/bin/env python3
"""
Check August 2024 data and investigate the 104 matches issue.
"""
from core.database import get_data, get_matched_data_by_companies

def check_august_data():
    """Check what data exists for August 2024"""
    print("=== Checking August 2024 Data ===")
    
    # Get all data
    all_data = get_data()
    print(f"Total records in database: {len(all_data)}")
    
    # Filter for August 2024
    august_data = [d for d in all_data if d.get('statement_month') == 'August' and d.get('statement_year') == '2024']
    print(f"August 2024 records: {len(august_data)}")
    
    if august_data:
        # Show company pairs
        company_pairs = set()
        for record in august_data:
            lender = record.get('lender', 'Unknown')
            borrower = record.get('borrower', 'Unknown')
            company_pairs.add(f"{lender} ↔ {borrower}")
        
        print(f"Company pairs in August 2024: {company_pairs}")
        
        # Check for GeoTex-Steel specifically
        geotex_steel = [d for d in august_data if d.get('lender') == 'GeoTex' and d.get('borrower') == 'Steel']
        steel_geotex = [d for d in august_data if d.get('lender') == 'Steel' and d.get('borrower') == 'GeoTex']
        
        print(f"GeoTex → Steel records: {len(geotex_steel)}")
        print(f"Steel → GeoTex records: {len(steel_geotex)}")
        
        if geotex_steel:
            print("\nSample GeoTex → Steel records:")
            for i, record in enumerate(geotex_steel[:3]):
                print(f"  {i+1}. UID: {record.get('uid')}, Amount: {record.get('Debit') or record.get('Credit')}")
    
    # Check matched data
    print("\n=== Checking Matched Data ===")
    matched_data = get_matched_data_by_companies('GeoTex', 'Steel', 'August', '2024')
    print(f"Matched records for GeoTex-Steel August 2024: {len(matched_data)}")
    
    if matched_data:
        print("Sample matched records:")
        for i, record in enumerate(matched_data[:3]):
            print(f"  {i+1}. UID: {record.get('uid')}, Matched UID: {record.get('matched_uid')}")

if __name__ == "__main__":
    check_august_data() 