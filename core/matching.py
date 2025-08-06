"""
Matching Module - Contains all matching algorithms and logic.
Extracted from core/database.py to separate concerns.
"""
import re
from typing import List, Dict, Any, Optional, Tuple


def extract_po(particulars: str) -> Optional[str]:
    """Extract PO number from particulars."""
    if not particulars:
        return None
    
    # Pattern for PO numbers: ABC/PO/123/456 or similar formats
    po_pattern = r'\b[A-Z]{2,4}/PO/\d+/\d+\b'
    match = re.search(po_pattern, particulars.upper())
    return match.group() if match else None


def extract_lc(particulars: str) -> Optional[str]:
    """Extract LC number from particulars."""
    if not particulars:
        return None
    
    # Pattern for LC numbers: L/C-123/456 or similar formats
    lc_pattern = r'\bL/C[-\s]?\d+[/\s]?\d*\b'
    match = re.search(lc_pattern, particulars.upper())
    return match.group() if match else None


def extract_loan_id(particulars: str) -> Optional[str]:
    """Extract Loan ID from particulars."""
    if not particulars:
        return None
    
    # Pattern for Loan IDs: LD123, ID-456, etc.
    loan_pattern = r'\b(?:LD|ID|LOAN)[-\s]?\d+\b'
    match = re.search(loan_pattern, particulars.upper())
    return match.group() if match else None


def calculate_jaccard_similarity(text1: str, text2: str) -> float:
    """Calculate Jaccard similarity between two texts."""
    if not text1 or not text2:
        return 0.0
    
    def preprocess(text: str) -> set:
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        # Remove common stop words and short words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = [word for word in words if len(word) > 2 and word not in stop_words]
        return set(words)
    
    set1 = preprocess(text1)
    set2 = preprocess(text2)
    
    if not set1 and not set2:
        return 0.0
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    return len(intersection) / len(union) if union else 0.0


def extract_salary_details(particulars: str) -> Optional[Dict[str, Any]]:
    """Extract salary-related details from particulars."""
    if not particulars:
        return None
    
    particulars_lower = particulars.lower()
    
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
    has_primary_keyword = any(keyword in particulars_lower for keyword in primary_salary_keywords)
    
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
    if any(indicator in particulars_lower for indicator in non_salary_indicators):
        return None
    
    # Check if this is a salary-related transaction
    is_salary = has_primary_keyword
    
    # Extract person name (look for patterns like "Salary of John Doe" or "John Doe Salary")
    person_patterns = [
        r'salary\s+of\s+([A-Za-z\s]+?)(?:\s+for|\s+month|\s+period|$)',
        r'([A-Za-z\s]+?)\s+salary',
        r'payroll\s+for\s+([A-Za-z\s]+?)(?:\s+for|\s+month|\s+period|$)',
        r'([A-Za-z\s]+?)\s+payroll'
    ]
    
    person_name = None
    for pattern in person_patterns:
        match = re.search(pattern, particulars_lower)
        if match:
            person_name = match.group(1).strip()
            break
    
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
        'period': period,
        'is_salary': is_salary,
        'matched_keywords': matched_keywords
    }


def extract_common_text(text1: str, text2: str) -> Optional[str]:
    """Extract common text patterns between two strings."""
    if not text1 or not text2:
        return None
    
    # Convert to lowercase for comparison
    text1_lower = text1.lower()
    text2_lower = text2.lower()
    
    # Find common words (minimum 3 characters)
    words1 = set(re.findall(r'\b\w{3,}\b', text1_lower))
    words2 = set(re.findall(r'\b\w{3,}\b', text2_lower))
    
    common_words = words1.intersection(words2)
    
    if len(common_words) < 2:  # Need at least 2 common words
        return None
    
    # Find the longest common phrase
    common_phrase = ' '.join(sorted(common_words))
    
    # Check if the phrase appears in both original texts (case-insensitive)
    if common_phrase.lower() in text1_lower and common_phrase.lower() in text2_lower:
        return common_phrase
    
    return None


def find_matches(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Match transactions using a hybrid approach combining exact and Jaccard similarity matching.
    
    Matching Strategy:
    1. Amount match (Debit == Credit) as base requirement
    2. Document reference matches (exact matching):
       - PO numbers (e.g., ABC/PO/123/456)
       - LC numbers (e.g., L/C-123/456)
       - Loan IDs (e.g., LD123, ID-456)
    3. Salary payment matches (hybrid):
       - Exact match: person name and period
       - Jaccard similarity: description comparison (threshold: 0.3)
    4. Common text pattern match (fallback)
       - Uses Jaccard similarity for general descriptions
    
    The hybrid approach ensures:
    - High accuracy for structured identifiers (PO, LC, Loan ID)
    - Flexibility for variations in descriptions (Salary, General text)
    - Complete audit trail in audit_info JSON
    """
    if not data:
        print("No data to match")
        return []
    
    lenders = [r for r in data if r.get('Debit') and r['Debit'] > 0]
    borrowers = [r for r in data if r.get('Credit') and r['Credit'] > 0]
    
    matches = []
    # Track which records have already been matched to prevent duplicates
    matched_lenders = set()
    matched_borrowers = set()
    
    for lender in lenders:
        # Skip if this lender is already matched
        if lender['uid'] in matched_lenders:
            continue
            
        lender_po = extract_po(lender.get('Particulars', ''))
        lender_lc = extract_lc(lender.get('Particulars', ''))
        lender_loan_id = extract_loan_id(lender.get('Particulars', ''))
        lender_salary = extract_salary_details(lender.get('Particulars', ''))
        

        
        for borrower in borrowers:
            # Skip if this borrower is already matched
            if borrower['uid'] in matched_borrowers:
                continue
                
            if float(lender['Debit']) == float(borrower['Credit']):
                borrower_po = extract_po(borrower.get('Particulars', ''))
                borrower_lc = extract_lc(borrower.get('Particulars', ''))
                borrower_loan_id = extract_loan_id(borrower.get('Particulars', ''))
                borrower_salary = extract_salary_details(borrower.get('Particulars', ''))
                
                # PO match
                if lender_po and borrower_po and lender_po == borrower_po:
                    matches.append({
                        'lender_uid': lender['uid'],
                        'borrower_uid': borrower['uid'],
                        'amount': lender['Debit'],
                        'match_type': 'PO',
                        'po': lender_po
                    })
                    # Mark both records as matched
                    matched_lenders.add(lender['uid'])
                    matched_borrowers.add(borrower['uid'])
                    break
                    
                # Salary payment match with both exact and Jaccard matching
                lender_text = lender.get('Particulars', '')
                borrower_text = borrower.get('Particulars', '')
                jaccard_score = calculate_jaccard_similarity(lender_text, borrower_text)
                
                if lender_salary and borrower_salary:
                    # Exact keyword matching
                    exact_match = (lender_salary['person_name'] == borrower_salary['person_name'] and 
                                 lender_salary['period'] == borrower_salary['period'] and
                                 lender_salary['is_salary'] and borrower_salary['is_salary'])
                    
                    # Jaccard similarity threshold for salary descriptions
                    jaccard_threshold = 0.3  # Can be adjusted based on requirements
                    
                    if exact_match or jaccard_score >= jaccard_threshold:
                        # Combine matched keywords and similarity score for audit trail
                        audit_keywords = {
                            'lender_keywords': lender_salary['matched_keywords'] if lender_salary else [],
                            'borrower_keywords': borrower_salary['matched_keywords'] if borrower_salary else [],
                            'jaccard_score': round(jaccard_score, 3),
                            'match_method': 'exact' if exact_match else 'jaccard'
                        }
                        
                        matches.append({
                            'lender_uid': lender['uid'],
                            'borrower_uid': borrower['uid'],
                            'amount': lender['Debit'],
                            'match_type': 'SALARY',
                            'person': lender_salary['person_name'] if lender_salary else None,
                            'period': lender_salary['period'] if lender_salary else None,
                            'audit_trail': audit_keywords
                        })
                        # Mark both records as matched
                        matched_lenders.add(lender['uid'])
                        matched_borrowers.add(borrower['uid'])
                        break
                
                # LC match
                if lender_lc and borrower_lc and lender_lc == borrower_lc:
                    matches.append({
                        'lender_uid': lender['uid'],
                        'borrower_uid': borrower['uid'],
                        'amount': lender['Debit'],
                        'match_type': 'LC',
                        'lc': lender_lc
                    })
                    # Mark both records as matched
                    matched_lenders.add(lender['uid'])
                    matched_borrowers.add(borrower['uid'])
                    break
                
                # Loan ID match
                if lender_loan_id and borrower_loan_id and lender_loan_id == borrower_loan_id:
                    matches.append({
                        'lender_uid': lender['uid'],
                        'borrower_uid': borrower['uid'],
                        'amount': lender['Debit'],
                        'match_type': 'LOAN_ID',
                        'loan_id': lender_loan_id
                    })
                    # Mark both records as matched
                    matched_lenders.add(lender['uid'])
                    matched_borrowers.add(borrower['uid'])
                    break
                
                # Manual verification match (lowest priority - requires user verification)
                # This matches records where debit, credit, and entered_by are exactly the same
                lender_entered_by = lender.get('entered_by', '')
                borrower_entered_by = borrower.get('entered_by', '')
                
                if (lender_entered_by and borrower_entered_by and 
                    lender_entered_by == borrower_entered_by):
                    matches.append({
                        'lender_uid': lender['uid'],
                        'borrower_uid': borrower['uid'],
                        'amount': lender['Debit'],
                        'match_type': 'MANUAL_VERIFICATION',
                        'entered_by': lender_entered_by,
                        'audit_trail': {
                            'match_reason': 'Exact match on debit, credit, and entered_by fields',
                            'requires_verification': True
                        }
                    })
                    # Mark both records as matched
                    matched_lenders.add(lender['uid'])
                    matched_borrowers.add(borrower['uid'])
                    break
                
                # Common text pattern match (fallback - only if no other matches found)
                common_text = extract_common_text(
                    lender.get('Particulars', ''),
                    borrower.get('Particulars', '')
                )
                if common_text and isinstance(common_text, str) and common_text.strip():
                    # Calculate Jaccard score for the overall texts
                    text_similarity = calculate_jaccard_similarity(
                        lender.get('Particulars', ''),
                        borrower.get('Particulars', '')
                    )
                    matches.append({
                        'lender_uid': lender['uid'],
                        'borrower_uid': borrower['uid'],
                        'amount': lender['Debit'],
                        'match_type': 'COMMON_TEXT',
                        'common_text': common_text.strip(),
                        'audit_trail': {
                            'jaccard_score': round(text_similarity, 3),
                            'matched_phrase': common_text.strip()  # Store the actual matching phrase
                        }
                    })
                    # Mark both records as matched
                    matched_lenders.add(lender['uid'])
                    matched_borrowers.add(borrower['uid'])
                    break
    
    return matches 