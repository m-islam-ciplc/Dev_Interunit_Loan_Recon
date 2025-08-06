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


def extract_account_number(particulars: str) -> Optional[Dict[str, Any]]:
    """Extract account number reference from particulars."""
    if not particulars:
        return None
    
    # Pattern for account number references: #11026, MDBL#11026, OBL#8826, etc.
    # Look for 5-digit numbers preceded by # or bank code#
    account_patterns = [
        r'([A-Z]{2,4})#(\d{4,5})\b',  # MDBL#11026, OBL#8826 (4-5 digits)
        r'([A-Za-z\s]+)#(\d{4,5})\b',  # Midland Bank#11026
        r'#(\d{4,5})\b',  # #11026 (fallback, 4-5 digits)
    ]
    
    for pattern in account_patterns:
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
            
            # Normalize bank codes
            bank_mapping = {
                'MDBL': 'MIDLAND BANK',
                'MIDLAND': 'MIDLAND BANK',
                'MIDLAND BANK': 'MIDLAND BANK',
                'OBL': 'ONE BANK',
                'ONE BANK': 'ONE BANK',
                'EBL': 'EASTERN BANK',
                'EASTERN BANK': 'EASTERN BANK',
                'DBL': 'DUTCH BANGLA BANK',
                'DUTCH BANGLA': 'DUTCH BANGLA BANK',
                'BBL': 'BRAC BANK',
                'BRAC': 'BRAC BANK',
                'PBL': 'PRIME BANK',
                'PRIME': 'PRIME BANK',
                'MTBL': 'MUTUAL TRUST BANK',
                'MUTUAL TRUST': 'MUTUAL TRUST BANK',
                'MBL': 'MIDLAND BANK',
                'NBL': 'NATIONAL BANK',
                'SBL': 'STANDARD BANK',
                'UBL': 'UNITED BANK',
                'CBL': 'CITY BANK'
            }
            
            normalized_bank = bank_mapping.get(bank_code.upper(), bank_code) if bank_code else None
            
            return {
                'account_number': account_number,
                'bank_code': bank_code,
                'normalized_bank': normalized_bank,
                'full_reference': match.group()
            }
    
    return None


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
        lender_account = extract_account_number(lender.get('Particulars', ''))
        lender_salary = extract_salary_details(lender.get('Particulars', ''))
        

        
        for borrower in borrowers:
            # Skip if this borrower is already matched
            if borrower['uid'] in matched_borrowers:
                continue
                
            if float(lender['Debit']) == float(borrower['Credit']):
                borrower_po = extract_po(borrower.get('Particulars', ''))
                borrower_lc = extract_lc(borrower.get('Particulars', ''))
                borrower_loan_id = extract_loan_id(borrower.get('Particulars', ''))
                borrower_account = extract_account_number(borrower.get('Particulars', ''))
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
                
                # Interunit Loan match (auto-confirmed, runs after PO and LC)
                # Two-way cross-reference matching for interunit loan transactions
                lender_particulars = lender.get('Particulars', '')
                borrower_particulars = borrower.get('Particulars', '')
                
                # Check for interunit loan keywords (more flexible matching)
                lender_lower = lender_particulars.lower()
                borrower_lower = borrower_particulars.lower()
                
                is_lender_interunit = (
                    'amount paid as interunit loan' in lender_lower or 
                    'interunit fund transfer' in lender_lower or
                    'inter unit fund transfer' in lender_lower or
                    'interunit loan' in lender_lower
                )
                is_borrower_interunit = (
                    'amount received as interunit loan' in borrower_lower or 
                    'interunit fund transfer' in borrower_lower or
                    'inter unit fund transfer' in borrower_lower or
                    'interunit loan' in borrower_lower
                )
                
                if (is_lender_interunit and is_borrower_interunit):
                    # Extract account numbers from both narrations using multiple patterns
                    lender_account_match = None
                    borrower_account_match = None
                    
                    # Pattern 1: For lender - extract full account number after bank name
                    lender_account_match = re.search(r'([A-Za-z\s-]+[A-Za-z])-?[A-Za-z0-9/-]*(\d{13})', lender_particulars)
                    
                    # Pattern 2: For borrower - extract hyphenated account number
                    borrower_account_match = re.search(r'([A-Za-z\s-]+[A-Za-z])-?[A-Za-z0-9/-]*(\d{3}-\d{10})', borrower_particulars)
                    
                    # Pattern 3: Fallback for any account number format
                    if not lender_account_match:
                        lender_account_match = re.search(r'([A-Za-z\s-]+[A-Za-z])-?[A-Za-z0-9/-]*(\d{10,})', lender_particulars)
                    if not borrower_account_match:
                        borrower_account_match = re.search(r'([A-Za-z\s-]+[A-Za-z])-?[A-Za-z0-9/-]*(\d{10,})', borrower_particulars)
                    
                    # Manual extraction for specific patterns
                    if not lender_account_match:
                        # Try to extract from "MTBL-SND-A/C-1310000003858"
                        lender_account_match = re.search(r'MTBL-SND-A/C-(\d{13})', lender_particulars)
                    if not borrower_account_match:
                        # Try to extract from "Mutual Trust Bank Ltd-SND-002-0320004355"
                        borrower_account_match = re.search(r'Mutual Trust Bank Ltd-SND-(\d{3}-\d{10})', borrower_particulars)
                    
                    # If still not found, try more specific patterns
                    if not lender_account_match:
                        # Try to extract from any pattern with 13 digits
                        lender_account_match = re.search(r'(\d{13})', lender_particulars)
                    if not borrower_account_match:
                        # Try to extract from any pattern with hyphenated account
                        borrower_account_match = re.search(r'(\d{3}-\d{10})', borrower_particulars)
                    
                    # Additional patterns for Prime Bank accounts
                    if not lender_account_match:
                        # Try to extract from "Prime Bank Limited-SND-2126318011502"
                        lender_account_match = re.search(r'Prime Bank Limited-SND-(\d{13})', lender_particulars)
                    if not borrower_account_match:
                        # Try to extract from "Prime Bank-CD-2126117010855"
                        borrower_account_match = re.search(r'Prime Bank-CD-(\d{13})', borrower_particulars)
                    
                    if lender_account_match and borrower_account_match:
                        # Extract last 4-5 digits from both account numbers
                        lender_account_full = lender_account_match.group(2)
                        borrower_account_full = borrower_account_match.group(2)
                        
                        lender_last_digits = lender_account_full[-5:] if len(lender_account_full) >= 5 else lender_account_full[-4:]
                        borrower_last_digits = borrower_account_full[-5:] if len(borrower_account_full) >= 5 else borrower_account_full[-4:]
                        
                        # Cross-reference 1: Lender → Borrower
                        # Look for lender's last digits in borrower's narration
                        cross_ref_1_found = lender_last_digits in borrower_particulars
                        
                        # Cross-reference 2: Borrower → Lender
                        # Look for borrower's last digits in lender's narration
                        cross_ref_2_found = borrower_last_digits in lender_particulars
                        
                        # Alternative: Look for the shortened references in the narrations
                        if not cross_ref_1_found:
                            # Look for any 4-5 digit number followed by # in borrower narration
                            borrower_short_ref = re.search(r'#(\d{4,5})', borrower_particulars)
                            if borrower_short_ref:
                                cross_ref_1_found = borrower_short_ref.group(1) in lender_last_digits
                        
                        if not cross_ref_2_found:
                            # Look for any 4-5 digit number followed by # in lender narration
                            lender_short_ref = re.search(r'#(\d{4,5})', lender_particulars)
                            if lender_short_ref:
                                cross_ref_2_found = lender_short_ref.group(1) in borrower_last_digits
                        
                        # Both cross-references must be found
                        if cross_ref_1_found and cross_ref_2_found:
                            matches.append({
                                'lender_uid': lender['uid'],
                                'borrower_uid': borrower['uid'],
                                'amount': lender['Debit'],
                                'match_type': 'INTERUNIT_LOAN',
                                'lender_account': lender_account_full,
                                'borrower_account': borrower_account_full,
                                'lender_last_digits': lender_last_digits,
                                'borrower_last_digits': borrower_last_digits,
                                'audit_trail': {
                                    'lender_reference': f"{lender_account_match.group(1)}-{lender_account_full}",
                                    'borrower_reference': f"{borrower_account_match.group(1)}-{borrower_account_full}",
                                    'match_reason': f"Interunit loan cross-reference match: {lender_last_digits} ↔ {borrower_last_digits}",
                                    'keywords': {
                                        'lender_interunit_keywords': ['amount paid as interunit loan', 'interunit fund transfer'],
                                        'borrower_interunit_keywords': ['amount received as interunit loan', 'interunit fund transfer'],
                                        'lender_account_patterns': ['MTBL-SND-A/C-', 'Prime Bank Limited-SND-', 'Mutual Trust Bank Ltd-SND-'],
                                        'cross_reference_patterns': ['#\\d{4,5}']
                                    },
                                    'validation': {
                                        'lender_interunit': is_lender_interunit,
                                        'borrower_interunit': is_borrower_interunit,
                                        'cross_reference_1': cross_ref_1_found,
                                        'cross_reference_2': cross_ref_2_found,
                                        'interunit_loan_transaction': True
                                    }
                                }
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