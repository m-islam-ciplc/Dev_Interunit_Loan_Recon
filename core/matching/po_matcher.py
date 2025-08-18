"""
PO Matcher - Handles Purchase Order number extraction and matching.
"""
import re
from typing import Optional


def extract_po(particulars: str) -> Optional[str]:
    """Extract PO number from particulars."""
    if not particulars:
        return None
    
    # Pattern for PO numbers: ABC/PO/123/456 or ABC/PO/2024/10/29964
    # Allow 2 or more numeric segments after /PO
    po_pattern = r'\b[A-Z]{2,4}/PO(?:/\d+){2,}\b'
    try:
        match = re.search(po_pattern, particulars.upper())
        return match.group() if match else None
    except Exception as e:
        print(f"DEBUG: PO regex error: {e} with pattern '{po_pattern}' and text '{particulars}'")
        return None
