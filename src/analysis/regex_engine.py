import re

TYPO_TRANSFORM_MAP = {
    'a': r'[a4]', 'e': r'[e3]', 'i': r'[i1l|]', 'o': r'[o0]',
    's': r'[s5]', 't': r'[t7]', 'b': r'[b8]', 'g': r'[g9]', 'z': r'[z2]'
}

def convert_word_to_typo_regex(word: str) -> str:
    word_lower = word.lower()
    regex_chars = []
    for char in word_lower:
        if char in TYPO_TRANSFORM_MAP:
            regex_chars.append(f"{TYPO_TRANSFORM_MAP[char]}{{0,2}}")
        else:
            regex_chars.append(f"{re.escape(char)}{{0,2}}")
    return "".join(regex_chars)

def compile_dynamic_query_regex(user_query: str):
    clean_query = re.sub(r"[^\w\s]", " ", user_query.strip())
    words = clean_query.split()
    
    typo_tolerant_words = []
    for word in words:
        if word.lower() in ["is", "the", "whether", "as", "in", "of", "to", "or", "and", "identified"]:
            typo_tolerant_words.append(re.escape(word) + r"\s*")
            continue
        typo_tolerant_words.append(convert_word_to_typo_regex(word))
        
    separator_pattern = r"[\s\-_,.:]*"
    return re.compile(separator_pattern.join(typo_tolerant_words) + r"[\s\?]*", re.IGNORECASE | re.DOTALL)

def resolve_interactive_query(document_text: str, user_query: str):
    compiled_pattern = compile_dynamic_query_regex(user_query)
    match = compiled_pattern.search(document_text)
    
    if not match:
        return user_query, "NA"
        
    start_idx = match.end()
    window = " ".join(document_text[start_idx : start_idx + 250].lower().split())
    
    if "yes" in window:
        return user_query, "YES"
    elif "no" in window:
        return user_query, "NO"
    return user_query, "NA"