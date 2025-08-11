"""
Settlement Matcher - Handles final settlement extraction and matching.
"""
import re
from typing import Optional, Dict, Any


def extract_final_settlement_details(particulars: str) -> Optional[Dict[str, Any]]:
    """Extract final settlement details from particulars."""
    if not particulars:
        return None
    
    particulars_lower = particulars.lower()
    
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
    
    # Extract person details
    person_name = None
    person_id = None
    person_combined = None
    
    if lender_person_match:
        person_name = lender_person_match.group('name').strip()
        person_id = lender_person_match.group('id').strip()
        person_combined = f"{person_name}-ID : {person_id}"
    elif borrower_person_match:
        person_name = borrower_person_match.group('name').strip()
        person_id = borrower_person_match.group('id').strip()
        person_combined = f"{person_name}-ID : {person_id}"
    
    # Only return if we found a person
    if person_combined:
        return {
            'person_name': person_name,
            'person_id': person_id,
            'person_combined': person_combined,
            'is_final_settlement': True
        }
    
    return None
