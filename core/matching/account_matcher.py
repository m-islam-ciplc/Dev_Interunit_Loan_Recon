"""
Account Matcher - Handles account number reference extraction and matching.
"""
import re
from typing import Optional, Dict, Any
from core.bank_config import get_bank_name, get_account_reference_patterns


def extract_account_number(particulars: str) -> Optional[Dict[str, Any]]:
    """Extract account number reference from particulars."""
    if not particulars:
        return None
    
    # Pattern for account number references: #11026, MDBL#11026, OBL#8826, etc.
    # Look for 4-6 digit numbers preceded by # or bank code#
    account_patterns = get_account_reference_patterns()
    
    for i, pattern in enumerate(account_patterns):
        try:
            match = re.search(pattern, particulars.upper())
            if match:
                if len(match.groups()) == 1:
                    # Pattern: #11026
                    account_number = match.group(1)
                    bank_code = None
                else:
                    # Pattern: MDBL#11026 or Midland Bank#11026
                    bank_code = match.group(1).strip()
                    account_number = match.group(2)
                
                # Normalize bank codes using the bank configuration module
                normalized_bank = get_bank_name(bank_code) if bank_code else None
                
                return {
                    'account_number': account_number,
                    'bank_code': bank_code,
                    'normalized_bank': normalized_bank,
                    'full_reference': match.group()
                }
        except Exception as e:
            print(f"DEBUG: Account regex error pattern {i}: {e} with pattern '{pattern}' and text '{particulars}'")
            continue
    
    return None
