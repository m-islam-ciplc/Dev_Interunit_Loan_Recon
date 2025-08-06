#!/usr/bin/env python3
"""
Test script to verify the updated salary matching logic with actual database patterns.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.matching import extract_salary_details

# Test cases based on actual patterns found in the database
test_cases = [
    # Real salary entries (should be identified as salary)
    "Salary of Luxmi Kant for the month of February-2025",
    "Amount paid as Salary of Luxmi Kant for the month of March-2025",
    "Amounts paid to Luxmi Kant Sharma's Salary of April-2025",
    "Amount paid to Factory Non Management Employees Salary, Holiday, Overtime & Tiffin allowance for the month of February-2025",
    "Amount paid to HO & Factory Management Employees Salary, Overtime & Tiffin allowance for the month of May-2025",
    "Salary & Allowance Payable Salary of Geo textile unit paid to Steel unit for the month of April-2025",
    "(as per details) Salary & Allowance-Admin Tax Payable-Mr. Luximi Kant Sharma-ID- Amount paid to Luxmi Kant Sharma - Head of Plant Salary for the month of April-25",
    
    # Non-salary entries (should NOT be identified as salary)
    "Being the amount paid for vendor payment against po no : BPD/PO/2024/9/29536",
    "Amount being paid as Principal & Interest of Time Loan",
    "Amount being paid as L/C Acceptance Commission",
    "Amount being paid as Duty & Taxes agt L/C-147125020063/25",
    "Amount being paid as Loan Payoff & Partial Payoff of Brac Bank-RL",
    "Amount being paid as IPDC Principal & Interest Payment of Term Loan",
    "Amount being paid as Repayment of Time Loan's principal & Interest",
    "Amount being paid as Payoff of Time Loan-ID-7100000046377",
    "Amount being paid as Duty,taxes,port,,shipping,carrying charges",
    "Amount being paid as L/C Retirement value agt L/C-308524990243/24",
    "Amount being paid as LC cash Collatereal agt L/C-141325020063/25",
    "Amount being paid as usance loan interest",
    "Amount being paid as Remuneration of Steel Unit for the month of April",
    "Amount paid as usance loan interest. This amount is paid from sttel unit bank",
    "Amount paid to KM Ideal Engineering agt. FOB/PO/2023/8/5023",
    "Amount paid to Dhaka Tyre Battery Sales. Supply of , Invoice Number: 3090",
    "Amount paid to Magnum Steel Industries Limited. Supply of , Invoice Number: SOINV012202300039",
    "Amount payable to Prime Insurance Company Limited as Certificate of Motor Insurance",
    "Amount payable to Titas Gas Transmission & Distribution Co. Ltd. Gas Bill For the month of march -2025",
    "Being the amount received as interunit loan for Salary Purpose. MDBL-0011106000031",
    "Payable to Md. Jasim Khan-ID : 16004 Being the amount Paid to Md. Jasim Khan-ID : 16004 driver Adminstration Factory agt. Final Settlement",
    "Payable to Md. Jomir Hossain-ID:15296 Being the amount Paid to Md. Jomir Hossain-ID:15296 junior Engineer production against his final settlement"
]

print("Testing updated salary matching logic with actual database patterns:")
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
print("Expected: 7 salary entries, 20 non-salary entries") 