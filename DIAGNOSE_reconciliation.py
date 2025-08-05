#!/usr/bin/env python3
"""
Debug the reconciliation process to see what data is being processed.
"""
from core.services.reconciliation_service import ReconciliationService
from core import database

def debug_reconciliation():
    """Debug the reconciliation process"""
    print("=== Debugging Reconciliation Process ===")
    
    # Check what data exists for August 2024
    august_data = database.get_unmatched_data_by_companies('GeoTex', 'Steel', 'August', '2024')
    print(f"August 2024 data: {len(august_data)} records")
    
    for record in august_data:
        print(f"  - UID: {record.get('uid')}, Amount: {record.get('Debit') or record.get('Credit')}, Period: {record.get('statement_month')} {record.get('statement_year')}")
    
    # Check what data exists for all periods
    all_data = database.get_unmatched_data_by_companies('GeoTex', 'Steel')
    print(f"\nAll periods data: {len(all_data)} records")
    
    # Group by period
    periods = {}
    for record in all_data:
        period = f"{record.get('statement_month')} {record.get('statement_year')}"
        if period not in periods:
            periods[period] = []
        periods[period].append(record)
    
    for period, records in periods.items():
        print(f"  {period}: {len(records)} records")
    
    # Test reconciliation service
    print("\n=== Testing Reconciliation Service ===")
    service = ReconciliationService()
    matches = service.run_reconciliation('GeoTex', 'Steel', 'August', '2024')
    print(f"Reconciliation found: {matches} matches")

if __name__ == "__main__":
    debug_reconciliation() 