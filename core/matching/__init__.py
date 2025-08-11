"""
Matching Module - Contains all matching algorithms and logic.
Organized into focused, single-purpose submodules.
"""

from .po_matcher import extract_po
from .lc_matcher import extract_lc, normalize_lc_number
from .loan_matcher import (
    extract_loan_id, 
    extract_normalized_loan_id,
    extract_normalized_loan_id_after_time_loan_phrase,
    has_time_loan_phrase
)
from .account_matcher import extract_account_number
from .salary_matcher import extract_salary_details
from .settlement_matcher import extract_final_settlement_details
from .text_matcher import (
    calculate_jaccard_similarity,
    extract_common_text,
    extract_phrases
)
from .interunit_matcher import match_interunit_loans
from .main_matcher import find_matches

__all__ = [
    'extract_po',
    'extract_lc',
    'normalize_lc_number',
    'extract_loan_id',
    'extract_normalized_loan_id',
    'extract_normalized_loan_id_after_time_loan_phrase',
    'has_time_loan_phrase',
    'extract_account_number',
    'extract_salary_details',
    'extract_final_settlement_details',
    'calculate_jaccard_similarity',
    'extract_common_text',
    'extract_phrases',
    'match_interunit_loans',
    'find_matches'
]
