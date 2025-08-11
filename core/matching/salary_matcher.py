"""
Salary Matcher - Handles salary payment extraction and matching.
"""
import re
from typing import Optional, Dict, Any


def extract_salary_details(particulars: str) -> Optional[Dict[str, Any]]:
    """Extract salary-related details from particulars."""
    if not particulars:
        return None
    
    particulars_lower = particulars.lower()
    
    # Pre-check for the two explicit patterns provided by requirements
    # 1) Lender pattern: "* Amount paid as Inter Unit Loan * (*-ID: *)"
    lender_person_match = re.search(
        r"\(\s*(?P<name>[^()]+?)\s*-\s*ID\s*[:：]\s*(?P<id>\d+)\s*\)",
        particulars,
        flags=re.IGNORECASE,
    ) if ('amount paid as inter unit loan' in particulars_lower) else None
    
    # 2) Borrower pattern: "Payable to *-ID:* * final settlement*"
    borrower_person_match = re.search(
        r"payable\s+to\s+(?P<name>[^\r\n\-]+?)\s*-\s*ID\s*[:：]\s*(?P<id>\d+)",
        particulars,
        flags=re.IGNORECASE | re.DOTALL,
    ) if ('payable to' in particulars_lower and 'final settlement' in particulars_lower) else None
    
    forced_salary = bool(lender_person_match or borrower_person_match)
    
    # Primary salary keywords found in actual data
    primary_salary_keywords = [
        'salary', 'sal', 'wage', 'payroll', 'remuneration', 'compensation'
    ]
    
    # Secondary keywords (context-dependent)
    secondary_keywords = [
        'monthly', 'month', 'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december',
        'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
    ]
    
    # Check for primary salary keywords first
    # Allow additional real-world triggers to qualify as salary-like
    has_primary_keyword = any(keyword in particulars_lower for keyword in primary_salary_keywords) or (
        'final settlement' in particulars_lower
    )
    
    if not has_primary_keyword:
        return None
    
    # Additional validation: must not contain non-salary indicators
    non_salary_indicators = [
        'payment for', 'purchase of', 'rent', 'electricity', 'transportation', 'marketing',
        'maintenance', 'equipment', 'insurance', 'legal', 'consulting', 'training',
        'travel', 'software', 'security', 'cleaning', 'bank charges', 'interest',
        'loan repayment', 'tax payment', 'bill payment', 'expenses for', 'fees for',
        'vendor payment', 'po no', 'work order', 'invoice', 'challan', 'tds deduction',
        'vds deduction', 'duty', 'taxes', 'port', 'shipping', 'carrying charges',
        'l/c', 'letter of credit', 'margin', 'collateral', 'acceptance commission',
        'retirement value', 'principal', 'time loan', 'usance loan'
    ]
    
    # If any non-salary indicator is present, it's not a salary transaction
    if any(indicator in particulars_lower for indicator in non_salary_indicators) and not forced_salary:
        return None
    
    # Check if this is a salary-related transaction
    is_salary = has_primary_keyword
    
    # Extract person
    # Handle patterns with titles and employee IDs
    person_patterns = [
        # Traditional salary patterns
        r'salary\s+of\s+([A-Za-z\s]+?)(?:\s+for|\s+month|\s+period|$)',
        r'([A-Za-z\s]+?)\s+salary',
        r'payroll\s+for\s+([A-Za-z\s]+?)(?:\s+for|\s+month|\s+period|$)',
        r'([A-Za-z\s]+?)\s+payroll',
        
        # Real-world patterns with titles and employee IDs
        r'\(([A-Za-z]+\.\s+[A-Za-z\s]+?)-ID\s*:\s*\d+\)',  # "(Name-ID : Number)"
        r'([A-Za-z]+\.\s+[A-Za-z\s]+?)-ID\s*:\s*\d+',  # "Name-ID : Number" (without parentheses)
        r'payable\s+to\s+([A-Za-z]+\.\s+[A-Za-z\s]+?)-ID\s*:\s*\d+',  # "Payable to Name-ID:Number"
        r'amount\s+paid\s+to\s+([A-Za-z]+\.\s+[A-Za-z\s]+?)(?:\s*,|\s+for|\s+employee|\s+office|\s+human|\s+resources|\s+administration|\s+final|\s+settlement|\s+employee\s+id|\s*$)',  # "Amount paid to Name"
        r'([A-Za-z]+\.\s+[A-Za-z\s]+?)(?:\s+for|\s+month|\s+period|\s+employee|\s+id|\s*,|\s*$)',  # General pattern for titles
        # Additional pattern for names with titles in parentheses
        r'\(([A-Za-z]+\.\s+[A-Za-z\s]+?)\)',  # "(Name)" - just the name in parentheses
    ]
    
    person_name = None
    person_id = None
    person_combined = None
    
    # Priority: use the explicit lender/borrower patterns first
    if lender_person_match:
        person_name = lender_person_match.group('name').strip()
        person_id = lender_person_match.group('id').strip()
        person_combined = f"{person_name}-ID : {person_id}"
    elif borrower_person_match:
        person_name = borrower_person_match.group('name').strip()
        person_id = borrower_person_match.group('id').strip()
        person_combined = f"{person_name}-ID : {person_id}"
    
    # If not found, fallback to legacy name extraction heuristics
    for pattern in person_patterns:
        if person_combined:
            break
        match = re.search(pattern, particulars_lower)
        if match:
            person_name = match.group(1).strip()
            break
    
    # Fallback: Manual extraction for names in parentheses with employee IDs
    if not person_name:
        # Look for pattern like "(Name-ID : Number)"
        start = particulars_lower.find("(")
        if start != -1:
            end = particulars_lower.find("-id :", start)
            if end != -1:
                # Extract the name part (remove the opening parenthesis)
                name_part = particulars_lower[start+1:end].strip()
                # Check if it looks like a name with title (e.g., "md. name")
                if "." in name_part and len(name_part.split()) >= 2:
                    person_name = name_part
    
    # Extract period (month/year)
    period_patterns = [
        r'(\w+\s+\d{4})',  # "January 2024"
        r'(\d{1,2}/\d{4})',  # "01/2024"
        r'(\d{4}-\d{2})',  # "2024-01"
    ]
    
    period = None
    for pattern in period_patterns:
        match = re.search(pattern, particulars)
        if match:
            period = match.group(1)
            break
    
    # Extract matched keywords for audit trail
    all_keywords = primary_salary_keywords + secondary_keywords
    matched_keywords = [keyword for keyword in all_keywords if keyword in particulars_lower]
    
    return {
        'person_name': person_name,
        'person_id': person_id,
        'person_combined': person_combined,
        'period': period,
        'is_salary': is_salary,
        'matched_keywords': matched_keywords
    }
