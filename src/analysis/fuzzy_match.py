# src/analysis/fuzzy_match.py

def calculate_levenshtein(s1, s2):
    """Standard Levenshtein Distance Matrix Calculation."""
    if len(s1) < len(s2):
        return calculate_levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
        
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
        
    return prev_row[-1]

def find_fuzzy_match_in_window(context_tokens, targeted_keywords, threshold=2):
    """
    Scans tokens inside a radial text window using string distances.
    Helps catch values if OCR introduces unexpected characters.
    """
    for token in context_tokens:
        clean_token = token.strip(",:-_[]()\"'").lower()
        for target in targeted_keywords:
            if calculate_levenshtein(clean_token, target) <= threshold:
                return target
    return None