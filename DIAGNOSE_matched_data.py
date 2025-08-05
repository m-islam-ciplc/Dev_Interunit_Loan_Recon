#!/usr/bin/env python3
"""
Check the actual matched data to see why LEFT JOIN is not working properly.
"""
from core import database

def check_matched_data():
    """Check the actual matched data structure."""
    print("=== CHECKING MATCHED DATA ===")
    
    # Get matched data
    matched_data = database.get_matched_data()
    if not matched_data:
        print("No matched data found")
        return
    
    print(f"Found {len(matched_data)} matched records")
    
    # Check first few records
    for i, record in enumerate(matched_data[:3]):
        print(f"\n--- Record {i+1} ---")
        print(f"Main UID: {record.get('uid', 'N/A')}")
        print(f"Matched UID: {record.get('matched_uid', 'N/A')}")
        print(f"Main Particulars: '{record.get('Particulars', 'N/A')}'")
        print(f"Matched Particulars: '{record.get('matched_particulars', 'N/A')}'")
        print(f"Main Debit: {record.get('Debit', 'N/A')}")
        print(f"Main Credit: {record.get('Credit', 'N/A')}")
        print(f"Matched Debit: {record.get('matched_Debit', 'N/A')}")
        print(f"Matched Credit: {record.get('matched_Credit', 'N/A')}")
        
        # Check if matched_uid exists in database
        if record.get('matched_uid'):
            print(f"✅ Matched UID exists: {record['matched_uid']}")
        else:
            print(f"❌ Matched UID is NULL")
    
    # Check if there are records with NULL matched_with
    print(f"\n=== CHECKING FOR NULL MATCHED_WITH ===")
    try:
        from sqlalchemy import create_engine, text
        from core.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB
        
        engine = create_engine(
            f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
        )
        
        with engine.connect() as conn:
            # Check for records with NULL matched_with
            result = conn.execute(text("""
                SELECT uid, lender, borrower, Particulars, matched_with, match_status
                FROM tally_data 
                WHERE (match_status = 'matched' OR match_status = 'confirmed')
                AND matched_with IS NULL
                LIMIT 5
            """))
            
            null_records = list(result)
            if null_records:
                print(f"Found {len(null_records)} records with NULL matched_with:")
                for record in null_records:
                    print(f"  UID: {record.uid}, Lender: {record.lender}, Borrower: {record.borrower}")
            else:
                print("No records with NULL matched_with found")
                
            # Check for orphaned matched_with references
            result = conn.execute(text("""
                SELECT t1.uid, t1.matched_with, t2.uid as matched_record_exists
                FROM tally_data t1
                LEFT JOIN tally_data t2 ON t1.matched_with = t2.uid
                WHERE (t1.match_status = 'matched' OR t1.match_status = 'confirmed')
                AND t1.matched_with IS NOT NULL
                AND t2.uid IS NULL
                LIMIT 5
            """))
            
            orphaned_records = list(result)
            if orphaned_records:
                print(f"\nFound {len(orphaned_records)} orphaned matched_with references:")
                for record in orphaned_records:
                    print(f"  UID: {record.uid} -> matched_with: {record.matched_with} (doesn't exist)")
            else:
                print("\nNo orphaned matched_with references found")
                
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_matched_data() 