"""
Loan Matcher - Handles loan ID extraction and matching.
"""
import re
from typing import Optional


def has_time_loan_phrase(particulars: str) -> bool:
    """Detect the specific Time Loan repayment phrase."""
    if not particulars:
        return False
    # Accept both variants:
    # - "... Principal & Interest repayment of Time Loan ..."
    # - "... Principal & Interest of Time Loan ..."
    pattern = (
        r"amount\s+being\s+paid\s+as\s*principal\s*&?\s*interest"  # Principal & Interest
        r"(?:\s+repayment)?"                                           # optional 'repayment'
        r"\s+(?:of\s+)?time\s+loan"                                  # 'of Time Loan' or 'Time Loan'
    )
    return re.search(pattern, particulars, flags=re.IGNORECASE) is not None


def extract_normalized_loan_id(particulars: str) -> Optional[str]:
    """Extract normalized loan id like PREFIX-<digits> (e.g., LD-2435445106)."""
    if not particulars:
        return None
    match = re.search(r"\b(?P<prefix>LD|ID|LOAN)[-\s]?(?P<digits>\d+)\b", particulars.upper())
    if not match:
        return None
    prefix = match.group("prefix")
    digits = match.group("digits")
    return f"{prefix}-{digits}"


def extract_normalized_loan_id_after_time_loan_phrase(particulars: str) -> Optional[str]:
    """Extract the first Loan ID that appears AFTER the time loan phrase.
    Normalizes to LD-<digits> for comparison/storage.
    """
    if not particulars:
        return None
    phrase = re.search(
        (
            r"amount\s+being\s+paid\s+as\s*principal\s*&?\s*interest"  # Principal & Interest
            r"(?:\s+repayment)?"                                           # optional 'repayment'
            r"\s+(?:of\s+)?time\s+loan"                                  # 'of Time Loan' or 'Time Loan'
        ),
        particulars,
        flags=re.IGNORECASE,
    )
    if not phrase:
        return None
    start = phrase.end()
    after = particulars[start:]
    m = re.search(r"\b(?:LD|ID|LOAN)[-\s]?(\d+)\b", after.upper())
    if not m:
        return None
    digits = m.group(1)
    return f"LD-{digits}"


def extract_loan_id(particulars: str) -> Optional[str]:
    """Extract Loan ID from particulars."""
    if not particulars:
        return None
    
    # Pattern for Loan IDs: LD123, ID-456, etc.
    loan_pattern = r'\b(?:LD|ID|LOAN)[-\s]?\d+\b'
    match = re.search(loan_pattern, particulars.upper())
    return match.group() if match else None
