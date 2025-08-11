"""
Text Matcher - Handles text similarity and common text pattern matching.
"""
import re
from typing import Optional


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


def extract_common_text(text1: str, text2: str) -> Optional[str]:
    """Extract common text patterns between two strings using continuous phrase matching.

    Focuses on substantial matches (minimum 20 words) to ensure meaningful
    text similarity detection for complex documents like insurance certificates.
    """
    if not text1 or not text2:
        return None

    text1_lower = text1.lower()
    text2_lower = text2.lower()

    # Strategy: Look for continuous phrases (20-50+ words) including numbers/punctuation
    # Extract phrases from both texts
    phrases1 = extract_phrases(text1_lower)
    phrases2 = extract_phrases(text2_lower)

    # Find common phrases
    common_phrases = phrases1.intersection(phrases2)

    if not common_phrases:
        return None

    # Sort phrases by length (longest first) and deduplicate overlapping content
    sorted_phrases = sorted(common_phrases, key=len, reverse=True)

    # Deduplicate: keep only the longest unique phrases (no overlapping content)
    unique_phrases = []
    for phrase in sorted_phrases:
        # Check if this phrase significantly overlaps with any already selected phrase
        is_significantly_overlapping = False
        for selected in unique_phrases:
            # Check for significant overlap (more than 70% similarity)
            if len(phrase) > 0 and len(selected) > 0:
                # Calculate overlap percentage
                if phrase in selected or selected in phrase:
                    is_significantly_overlapping = True
                    break
                # Check for partial overlap by comparing word sets
                words1 = set(phrase.split())
                words2 = set(selected.split())
                if len(words1) > 0 and len(words2) > 0:
                    overlap_ratio = len(words1.intersection(words2)) / max(len(words1), len(words2))
                    if overlap_ratio > 0.7:  # More than 70% overlap
                        is_significantly_overlapping = True
                        break

        if not is_significantly_overlapping:
            unique_phrases.append(phrase)
            # Limit to top 2 unique phrases to keep output focused
            if len(unique_phrases) >= 2:
                break

    if unique_phrases:
        # Return common text with word count in clean format
        result = []
        for phrase in unique_phrases:
            word_count = len(phrase.split())
            # Show up to 50 words, add (CONT...) if longer
            words = phrase.split()
            if len(words) > 50:
                display_phrase = ' '.join(words[:50]) + ' (CONT...)'
            else:
                display_phrase = phrase
            result.append(f"{word_count} words: {display_phrase}")

        return ' | '.join(result)

    return None


def extract_phrases(text: str, min_words: int = 20, max_words: int = 50) -> set:
    """Extract phrases of 20-50 words from text, including numbers and punctuation.
    
    This function focuses only on long continuous text matches that include
    mixed text and numbers, such as insurance certificates, vehicle details, etc.
    Minimum 20 words ensures meaningful, substantial matches.
    """
    # Split text into tokens (words, numbers, punctuation)
    # Enhanced pattern to better capture mixed alphanumeric sequences
    tokens = re.findall(r'\b\w+\b|\d+(?:\.\d+)?|\d+[/\-]\d+|[A-Za-z0-9]+[/\-][A-Za-z0-9]+|[A-Za-z0-9]+(?:\-[A-Za-z0-9]+)*|[^\w\s]', text)
    phrases = set()
    
    for i in range(len(tokens) - min_words + 1):
        for length in range(min_words, min(max_words + 1, len(tokens) - i + 1)):
            phrase = ' '.join(tokens[i:i + length])
            if len(phrase) >= 50:  # Minimum phrase length (increased for 20+ words)
                phrases.add(phrase)
    
    return phrases
