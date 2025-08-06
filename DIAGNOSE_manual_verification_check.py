#!/usr/bin/env python3
"""
Diagnostic script to check why specific records are tagged as MANUAL_VERIFICATION
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import create_engine
from core.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB
from sqlalchemy import text

def check_manual_verification_records():
    """Check why specific records are tagged as MANUAL_VERIFICATION"""
    
    engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')
    
    with engine.connect() as conn:
        # Check the specific records mentioned
        specific_uids = [
            'GeoTex_134fdf5_63a1780_000010',
            'Steel_134fdf5_63a1780_000010'
        ]
        
        print("Checking Specific Records:")
        print("=" * 50)
        
        for uid in specific_uids:
            result = conn.execute(text("""
                SELECT uid, lender, borrower, Particulars, Debit, Credit, 
                       match_status, matched_with, match_method, audit_info,
                       entered_by, Date
                FROM tally_data 
                WHERE uid = :uid
            """), {'uid': uid})
            
            record = result.fetchone()
            if record:
                print(f"\n📋 Record: {record.uid}")
                print(f"   Lender: {record.lender}")
                print(f"   Borrower: {record.borrower}")
                print(f"   Particulars: {record.Particulars}")
                print(f"   Debit: {record.Debit}")
                print(f"   Credit: {record.Credit}")
                print(f"   Match Status: {record.match_status}")
                print(f"   Matched With: {record.matched_with}")
                print(f"   Match Method: {record.match_method}")
                print(f"   Entered By: {record.entered_by}")
                print(f"   Date: {record.Date}")
                
                if record.audit_info:
                    try:
                        import json
                        audit_info = json.loads(record.audit_info)
                        print(f"   Audit Info: {json.dumps(audit_info, indent=2)}")
                    except:
                        print(f"   Audit Info: {record.audit_info}")
            else:
                print(f"\n❌ Record not found: {uid}")
        
        # Check all MANUAL_VERIFICATION records
        print("\n\nAll MANUAL_VERIFICATION Records:")
        print("=" * 50)
        
        result = conn.execute(text("""
            SELECT uid, lender, borrower, Particulars, Debit, Credit, 
                   match_status, matched_with, match_method, audit_info,
                   entered_by, Date
            FROM tally_data 
            WHERE match_method = 'fallback_match' OR match_status = 'pending_verification'
            ORDER BY Date DESC
            LIMIT 10
        """))
        
        manual_records = result.fetchall()
        
        if manual_records:
            print(f"Found {len(manual_records)} MANUAL_VERIFICATION records:")
            for record in manual_records:
                print(f"\n📋 {record.uid}")
                print(f"   Lender: {record.lender} → Borrower: {record.borrower}")
                print(f"   Particulars: {record.Particulars}")
                print(f"   Amount: Debit={record.Debit}, Credit={record.Credit}")
                print(f"   Match Method: {record.match_method}")
                print(f"   Entered By: {record.entered_by}")
        else:
            print("No MANUAL_VERIFICATION records found")

if __name__ == "__main__":
    check_manual_verification_records() 