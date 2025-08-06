#!/usr/bin/env python3
"""
Debug script to test frontend INTERUNIT_LOAN display
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB
from sqlalchemy import create_engine, text
import json

def test_frontend_display():
    """Test how frontend would display INTERUNIT_LOAN matches"""
    
    engine = create_engine(
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    )
    
    with engine.connect() as conn:
        # Get one INTERUNIT_LOAN match
        result = conn.execute(text("""
            SELECT audit_info
            FROM tally_data 
            WHERE match_status = 'confirmed' 
            AND audit_info LIKE '%INTERUNIT_LOAN%'
            LIMIT 1
        """))
        
        match = result.fetchone()
        if not match:
            print("No INTERUNIT_LOAN matches found")
            return
        
        audit_info_str = match.audit_info
        print("Raw audit_info from database:")
        print(audit_info_str)
        print("\n" + "="*50 + "\n")
        
        # Simulate frontend parsing
        try:
            audit_info = json.loads(audit_info_str)
            print("Parsed audit_info:")
            print(f"match_type: {audit_info.get('match_type')}")
            print(f"lender_reference: {audit_info.get('lender_reference')}")
            print(f"borrower_reference: {audit_info.get('borrower_reference')}")
            print(f"lender_amount: {audit_info.get('lender_amount')}")
            print(f"borrower_amount: {audit_info.get('borrower_amount')}")
            print(f"match_reason: {audit_info.get('match_reason')}")
            
            # Simulate frontend formatting
            print("\n" + "="*50 + "\n")
            print("Frontend would display:")
            
            match_type = audit_info.get('match_type')
            if match_type == 'INTERUNIT_LOAN':
                print("Interunit Loan Match")
                if audit_info.get('lender_reference'):
                    print(f"Lender: {audit_info['lender_reference']}")
                if audit_info.get('borrower_reference'):
                    print(f"Borrower: {audit_info['borrower_reference']}")
                if audit_info.get('lender_amount'):
                    print(f"Lender Amount: {audit_info['lender_amount']}")
                if audit_info.get('borrower_amount'):
                    print(f"Borrower Amount: {audit_info['borrower_amount']}")
                if audit_info.get('match_reason'):
                    # Extract cross-reference from match_reason
                    reason = audit_info['match_reason']
                    if '↔' in reason:
                        cross_ref = reason.split('↔')[0].split(':')[-1].strip() + ' ↔ ' + reason.split('↔')[1].strip()
                        print(f"Cross-Reference: {cross_ref}")
            else:
                print(f"Type: {match_type}")
                print(f"Keywords: {audit_info.get('keywords', '')}")
                
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Raw string: {audit_info_str}")

if __name__ == "__main__":
    test_frontend_display() 