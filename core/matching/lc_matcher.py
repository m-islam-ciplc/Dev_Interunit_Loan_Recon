"""
LC Matcher - Handles Letter of Credit number extraction and matching.
"""
import re
from typing import Optional


def extract_lc(particulars: str) -> Optional[str]:
    """Extract LC number from particulars."""
    if not particulars:
        return None
    
    # Pattern for LC numbers: L/C-123/456, LC-123/456, or similar formats
    lc_pattern = r'\b(?:L/C|LC)[-\s]?\d+[/\s]?\d*\b'
    match = re.search(lc_pattern, particulars.upper())
    return match.group() if match else None


def normalize_lc_number(lc_string: str) -> str:
    """Normalize LC number to consistent format for comparison.
    
    Converts both 'L/C-123/456' and 'LC-123/456' to 'LC-123/456'
    """
    if not lc_string:
        return ""
    
    # Remove any extra spaces and normalize to uppercase
    normalized = lc_string.upper().strip()
    
    # Replace 'L/C' with 'LC' for consistent comparison
    normalized = normalized.replace('L/C', 'LC')
    
    return normalized
