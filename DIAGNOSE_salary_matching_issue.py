#!/usr/bin/env python3
"""
Diagnostic script to test salary matching logic and identify incorrect matches.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import extract_salary_details

# Test cases - some salary, some non-salary
test_cases = [
    "Salary of John Doe for January 2024",
    "John Doe Salary Payment",
    "Payroll for Jane Smith",
    "Monthly salary transfer",
    "Payment for office supplies",
    "Purchase of raw materials",
    "Rent payment for office",
    "Electricity bill payment",
    "Transportation expenses",
    "Marketing expenses for January",
    "Office maintenance for February",
    "Equipment purchase for March",
    "Insurance payment for April",
    "Legal fees for May",
    "Consulting fees for June",
    "Training expenses for July",
    "Travel expenses for August",
    "Software license for September",
    "Maintenance contract for October",
    "Security services for November",
    "Cleaning services for December",
    "Bank charges for January 2024",
    "Interest payment for February 2024",
    "Loan repayment for March 2024",
    "Tax payment for April 2024"
]

print("Testing salary matching logic:")
print("=" * 50)

for i, test_case in enumerate(test_cases, 1):
    result = extract_salary_details(test_case)
    status = "✅ SALARY" if result else "❌ NOT SALARY"
    print(f"{i:2d}. {status}: {test_case}")
    if result:
        print(f"     Keywords: {result.get('matched_keywords', [])}")
        print(f"     Person: {result.get('person_name', 'N/A')}")
        print(f"     Period: {result.get('period', 'N/A')}")
        print()

print("\n" + "=" * 50)
print("Analysis: Any non-salary transactions marked as salary are FALSE POSITIVES") 