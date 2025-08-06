#!/usr/bin/env python3
"""
Script to check and fix the match_status column size.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine
from sqlalchemy import text

def check_and_fix_match_status_column():
    """Check the match_status column definition and fix if needed."""
    
    with engine.connect() as conn:
        # Check current column definition
        result = conn.execute(text("""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'interunit_loan_recon_db' 
            AND TABLE_NAME = 'tally_data' 
            AND COLUMN_NAME = 'match_status'
        """))
        
        column_info = result.fetchone()
        if column_info:
            print(f"Current match_status column definition:")
            print(f"  Column Name: {column_info[0]}")
            print(f"  Data Type: {column_info[1]}")
            print(f"  Max Length: {column_info[2]}")
            print(f"  Nullable: {column_info[3]}")
            
            # Check if we need to increase the size
            current_length = column_info[2] or 0
            required_length = len('pending_verification')  # 21 characters
            
            if current_length < required_length:
                print(f"\nColumn size needs to be increased from {current_length} to at least {required_length}")
                print("Attempting to alter the column...")
                
                try:
                    # Alter the column to increase size
                    conn.execute(text(f"""
                        ALTER TABLE tally_data 
                        MODIFY COLUMN match_status VARCHAR({required_length + 5})
                    """))
                    conn.commit()
                    print("✅ Successfully increased match_status column size")
                except Exception as e:
                    print(f"❌ Error altering column: {e}")
                    return False
            else:
                print("✅ Column size is sufficient")
        else:
            print("❌ match_status column not found")
            return False
    
    return True

def test_match_status_values():
    """Test inserting different match_status values."""
    
    test_values = [
        'matched',
        'confirmed', 
        'rejected',
        'pending_verification',
        'unmatched'
    ]
    
    print("\nTesting match_status values:")
    for value in test_values:
        print(f"  '{value}' - Length: {len(value)}")
    
    # Test the longest value
    longest_value = 'pending_verification'
    print(f"\nLongest value: '{longest_value}' (Length: {len(longest_value)})")

def main():
    print("Checking and fixing match_status column...")
    print("=" * 60)
    
    success = check_and_fix_match_status_column()
    
    if success:
        test_match_status_values()
        print("\n✅ Column should now support all match_status values")
    else:
        print("\n❌ Failed to fix column")

if __name__ == "__main__":
    main() 