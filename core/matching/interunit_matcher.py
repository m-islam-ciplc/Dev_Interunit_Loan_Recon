"""
Interunit Matcher - Handles interunit loan transaction matching using dictionary lookup.
"""
from typing import Optional, Dict, Any
import os
import sys

# Support both package import and direct execution
if __package__ in (None, ""):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from core.bank_config import get_interunit_account_mapping  # type: ignore
else:
    from ..bank_config import get_interunit_account_mapping


def match_interunit_loans(lender_particulars: str, borrower_particulars: str) -> Optional[Dict[str, Any]]:
    """Dictionary-based interunit loan match with bidirectional short-reference validation.
    
    Logic:
    - If lender contains a full account format from the mapping, check that borrower's text contains the lender's short reference.
    - If borrower contains a full account format from the mapping, check that lender's text contains the borrower's short reference.
    - Both sides must succeed; otherwise return None.
    - Returns minimal info for audit usage by caller.
    """
    account_mapping = get_interunit_account_mapping()

    # Detect full account on lender side
    lender_account = None
    lender_short_ref = None
    for full_account, short_ref in account_mapping.items():
        if full_account in lender_particulars:
            lender_account = full_account
            lender_short_ref = short_ref
            break

    # Detect full account on borrower side
    borrower_account = None
    borrower_short_ref = None
    for full_account, short_ref in account_mapping.items():
        if full_account in borrower_particulars:
            borrower_account = full_account
            borrower_short_ref = short_ref
            break

    # Both accounts must be found
    if not (lender_account and borrower_account):
        return None

    # Bidirectional cross-reference validation
    cross_ref_1 = lender_short_ref in borrower_particulars if lender_short_ref else False
    cross_ref_2 = borrower_short_ref in lender_particulars if borrower_short_ref else False
    if not (cross_ref_1 and cross_ref_2):
        return None

    # Return minimal fields; caller composes final audit info
    return {
        'lender_account': lender_account,
        'borrower_account': borrower_account,
        'lender_short_ref': lender_short_ref,
        'borrower_short_ref': borrower_short_ref
    }
