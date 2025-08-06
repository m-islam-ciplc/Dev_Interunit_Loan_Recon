#!/usr/bin/env python3
"""
Test script to verify INTERUNIT_LOAN keywords are stored correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB
from sqlalchemy import create_engine, text
import json

def test_interunit_keywords():
    """Test that INTERUNIT_LOAN keywords are stored correctly"""
    
    engine = create_engine(
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    )
    
    with engine.connect() as conn:
        # Get all INTERUNIT_LOAN matches
        result = conn.execute(text("""
            SELECT uid, lender, borrower, keywords, match_method, audit_info, match_status
            FROM tally_data 
            WHERE match_status = 'confirmed' 
            AND audit_info LIKE '%INTERUNIT_LOAN%'
            LIMIT 5
        """))
        
        matches = list(result)
        
        if not matches:
            print("No INTERUNIT_LOAN matches found in database")
            return
        
        print(f"Found {len(matches)} INTERUNIT_LOAN matches:")
        print("=" * 80)
        
        for i, match in enumerate(matches, 1):
            print(f"\n{i}. UID: {match.uid}")
            print(f"   Lender: {match.lender}")
            print(f"   Borrower: {match.borrower}")
            print(f"   Keywords: '{match.keywords}'")
            print(f"   Match Method: '{match.match_method}'")
            print(f"   Match Status: {match.match_status}")
            
            # Parse audit_info
            try:
                audit_info = json.loads(match.audit_info) if match.audit_info else {}
                print(f"   Audit Info Keys: {list(audit_info.keys())}")
                print(f"   Full Audit Info: {json.dumps(audit_info, indent=2)}")
                
            except json.JSONDecodeError:
                print(f"   Audit Info: Invalid JSON - {match.audit_info}")
            
            print("-" * 40)

if __name__ == "__main__":
    test_interunit_keywords() 