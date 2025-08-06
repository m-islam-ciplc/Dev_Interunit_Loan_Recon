#!/usr/bin/env python3
"""
Diagnostic script to read and display all records where Particulars contains salary-related keywords.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine
import pandas as pd

def get_salary_records():
    """Get all records where Particulars contains salary-related keywords."""
    
    # Query to find records with salary-related keywords
    query = """
    SELECT uid, Company, Particulars, Debit, Credit, Date, match_status
    FROM tally_data 
    WHERE LOWER(Particulars) LIKE '%salary%' 
       OR LOWER(Particulars) LIKE '%sal %' 
       OR LOWER(Particulars) LIKE '%payroll%'
       OR LOWER(Particulars) LIKE '%wage%'
       OR LOWER(Particulars) LIKE '%remuneration%'
       OR LOWER(Particulars) LIKE '%compensation%'
    ORDER BY Company, Date
    """
    
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error querying database: {e}")
        # Try a simpler query to check if table exists
        try:
            simple_query = "SELECT COUNT(*) as count FROM tally_data"
            result = pd.read_sql(simple_query, engine)
            print(f"Total records in database: {result['count'].iloc[0]}")
        except Exception as e2:
            print(f"Database connection error: {e2}")
        return None

def main():
    print("Reading salary-related records from database...")
    print("=" * 80)
    
    df = get_salary_records()
    
    if df is None or df.empty:
        print("No salary-related records found in the database.")
        return
    
    print(f"Found {len(df)} salary-related records:")
    print()
    
    # Group by company for better readability
    for company in df['Company'].unique():
        company_data = df[df['Company'] == company]
        print(f"Company: {company}")
        print("-" * 50)
        
        for _, row in company_data.iterrows():
            print(f"UID: {row['uid']}")
            print(f"Date: {row['Date']}")
            print(f"Particulars: {row['Particulars']}")
            print(f"Debit: {row['Debit']}")
            print(f"Credit: {row['Credit']}")
            print(f"Match Status: {row['match_status']}")
            print()
        
        print()

if __name__ == "__main__":
    main() 