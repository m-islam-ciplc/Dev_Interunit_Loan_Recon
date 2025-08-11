"""
Main Matcher - Orchestrates all matching algorithms and coordinates the matching process.
"""
from typing import List, Dict, Any
from .po_matcher import extract_po
from .lc_matcher import extract_lc, normalize_lc_number
from .loan_matcher import (
    extract_loan_id, 
    has_time_loan_phrase,
    extract_normalized_loan_id_after_time_loan_phrase
)
from .account_matcher import extract_account_number
from .salary_matcher import extract_salary_details
from .settlement_matcher import extract_final_settlement_details
from .text_matcher import calculate_jaccard_similarity, extract_common_text
from .interunit_matcher import match_interunit_loans


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
                    
                # Final Settlement match
                lender_final_settlement = extract_final_settlement_details(lender.get('Particulars', ''))
                borrower_final_settlement = extract_final_settlement_details(borrower.get('Particulars', ''))
                
                if lender_final_settlement and borrower_final_settlement:
                    # Check if both sides have the same person
                    if lender_final_settlement['person_name'] == borrower_final_settlement['person_name']:
                        matches.append({
                            'lender_uid': lender['uid'],
                            'borrower_uid': borrower['uid'],
                            'amount': lender['Debit'],
                            'match_type': 'FINAL_SETTLEMENT',
                            'person': lender_final_settlement['person_combined'],
                            'audit_trail': {
                                'match_reason': 'Final settlement match',
                                'lender_person': lender_final_settlement['person_combined'],
                                'borrower_person': borrower_final_settlement['person_combined'],
                                'person_name': lender_final_settlement['person_name'],
                                'person_id': lender_final_settlement['person_id']
                            }
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
                            'person': (
                                lender_salary.get('person_combined')
                                if lender_salary and lender_salary.get('person_combined')
                                else lender_salary.get('person_name') if lender_salary else None
                            ),
                            'period': lender_salary['period'] if lender_salary else None,
                            'audit_trail': audit_keywords
                        })
                        # Mark both records as matched
                        matched_lenders.add(lender['uid'])
                        matched_borrowers.add(borrower['uid'])
                        break

                
                # LC match
                if lender_lc and borrower_lc and normalize_lc_number(lender_lc) == normalize_lc_number(borrower_lc):
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
                interunit_match = match_interunit_loans(
                    lender.get('Particulars', ''),
                    borrower.get('Particulars', '')
                )
                if interunit_match:
                    matches.append({
                        'lender_uid': lender['uid'],
                        'borrower_uid': borrower['uid'],
                        'amount': lender['Debit'],
                        'match_type': 'INTERUNIT_LOAN',
                        'audit_trail': {
                            'lender_account': interunit_match['lender_account'],
                            'borrower_account': interunit_match['borrower_account'],
                            'lender_short_ref': interunit_match.get('lender_short_ref'),
                            'borrower_short_ref': interunit_match.get('borrower_short_ref')
                        }
                    })
                    # Mark both records as matched
                    matched_lenders.add(lender['uid'])
                    matched_borrowers.add(borrower['uid'])
                    break
                    
                
                # Loan ID match (redefined condition):
                # If both narrations contain the Time Loan phrase and share the same Loan ID AFTER the phrase
                lender_text_full = lender.get('Particulars', '')
                borrower_text_full = borrower.get('Particulars', '')
                if has_time_loan_phrase(lender_text_full) and has_time_loan_phrase(borrower_text_full):
                    lender_after_id = extract_normalized_loan_id_after_time_loan_phrase(lender_text_full)
                    borrower_after_id = extract_normalized_loan_id_after_time_loan_phrase(borrower_text_full)
                    if lender_after_id and borrower_after_id and lender_after_id == borrower_after_id:
                        matches.append({
                            'lender_uid': lender['uid'],
                            'borrower_uid': borrower['uid'],
                            'amount': lender['Debit'],
                            'match_type': 'LOAN_ID',
                            'loan_id': lender_after_id,
                            'audit_trail': {
                                'match_reason': 'Time Loan phrase + matching Loan ID after phrase',
                                'phrase_detected': True
                            }
                        })
                        # Mark both records as matched
                        matched_lenders.add(lender['uid'])
                        matched_borrowers.add(borrower['uid'])
                        break
                
                # Loan ID match (generic exact token equality)
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
                
                # Final Settlement match
                final_settlement_match = extract_final_settlement_details(lender.get('Particulars', ''))
                if final_settlement_match:
                    matches.append({
                        'lender_uid': lender['uid'],
                        'borrower_uid': borrower['uid'],
                        'amount': lender['Debit'],
                        'match_type': 'FINAL_SETTLEMENT',
                        'person': final_settlement_match['person_combined'],
                        'audit_trail': {
                            'match_reason': 'Final settlement match',
                            'person_name': final_settlement_match['person_name'],
                            'person_id': final_settlement_match['person_id'],
                            'is_final_settlement': final_settlement_match['is_final_settlement']
                        }
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
