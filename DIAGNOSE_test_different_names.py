#!/usr/bin/env python3
"""
Test script to verify salary matching logic works with different person names.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import extract_salary_details

# Test cases with different person names
test_cases = [
    # Different person names (should all be identified as salary)
    "Salary of John Doe for the month of January-2025",
    "Salary of Jane Smith for the month of February-2025",
    "Salary of Ahmed Khan for the month of March-2025",
    "Salary of Maria Garcia for the month of April-2025",
    "Salary of David Chen for the month of May-2025",
    "Amount paid as Salary of Robert Johnson for the month of June-2025",
    "Amounts paid to Sarah Wilson's Salary of July-2025",
    "Amount paid to Factory Non Management Employees Salary, Holiday, Overtime & Tiffin allowance for the month of August-2025",
    "Amount paid to HO & Factory Management Employees Salary, Overtime & Tiffin allowance for the month of September-2025",
    "Salary & Allowance Payable Salary of Textile unit paid to Steel unit for the month of October-2025",
    
    # Original names from your data (should still work)
    "Salary of Luxmi Kant for the month of February-2025",
    "Amount paid as Salary of Luxmi Kant for the month of March-2025",
    "Amounts paid to Luxmi Kant Sharma's Salary of April-2025",
    
    # Non-salary entries (should NOT be identified as salary)
    "Being the amount paid for vendor payment against po no : BPD/PO/2024/9/29536",
    "Amount being paid as Principal & Interest of Time Loan",
    "Amount being paid as L/C Acceptance Commission"
]

print("Testing salary matching logic with different person names:")
print("=" * 80)

salary_count = 0
non_salary_count = 0

for i, test_case in enumerate(test_cases, 1):
    result = extract_salary_details(test_case)
    status = "✅ SALARY" if result else "❌ NOT SALARY"
    print(f"{i:2d}. {status}: {test_case}")
    
    if result:
        salary_count += 1
        print(f"     Keywords: {result.get('matched_keywords', [])}")
        print(f"     Person: {result.get('person_name', 'N/A')}")
        print(f"     Period: {result.get('period', 'N/A')}")
        print()
    else:
        non_salary_count += 1

print("=" * 80)
print(f"Summary: {salary_count} salary entries, {non_salary_count} non-salary entries")
print("Expected: 13 salary entries, 3 non-salary entries") 