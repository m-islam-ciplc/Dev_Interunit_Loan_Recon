#!/usr/bin/env python3
"""
Diagnostic script to show all unique values in the Particulars column.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine
import pandas as pd

def get_all_particulars():
    """Get all unique values in the Particulars column."""
    
    query = """
    SELECT DISTINCT Particulars, COUNT(*) as count
    FROM tally_data 
    WHERE Particulars IS NOT NULL AND Particulars != ''
    GROUP BY Particulars
    ORDER BY count DESC, Particulars
    """
    
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error querying database: {e}")
        return None

def main():
    print("Reading all unique Particulars values from database...")
    print("=" * 80)
    
    df = get_all_particulars()
    
    if df is None or df.empty:
        print("No records found in the database.")
        return
    
    print(f"Found {len(df)} unique Particulars values:")
    print()
    
    # Show first 50 entries
    for i, (_, row) in enumerate(df.head(50).iterrows()):
        print(f"{i+1:3d}. [{row['count']:3d}x] {row['Particulars']}")
    
    if len(df) > 50:
        print(f"\n... and {len(df) - 50} more entries")
    
    print("\n" + "=" * 80)
    print("Looking for any entries that might be salary-related...")
    
    # Search for any entries that might contain salary-related terms
    salary_indicators = ['salary', 'sal', 'payroll', 'wage', 'remuneration', 'compensation', 'pay']
    
    for _, row in df.iterrows():
        particulars_lower = row['Particulars'].lower()
        for indicator in salary_indicators:
            if indicator in particulars_lower:
                print(f"Potential salary entry: [{row['count']:3d}x] {row['Particulars']}")
                break

if __name__ == "__main__":
    main() 