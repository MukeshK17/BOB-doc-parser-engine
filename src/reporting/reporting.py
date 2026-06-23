import json
import csv
import os
import re
from collections import Counter
from config import REJECS_PATTERNS, INTERNAL_STOP_WORDS, TEMPLATE_BIAS
from src.analysis.regex_engine import resolve_interactive_query

def extract_fraud_status(text):
    """
    Radial Scan Logic:
    1. Finds the Fraud Query.
    2. Captures a 250-character 'Radial Window'.
    3. Normalizes all spacing to catch 'Yes' regardless of column gaps.
    """
    query_str = "Whether the account is identified as fraud?"
    query_pattern = re.compile(
        r"Whether\s*the\s*account\s*(?:is\s*)?identified\s*as\s*fraud\??", 
        re.IGNORECASE | re.DOTALL
    )
    
    match = query_pattern.search(text)
    if match:
        start_index = match.end()
        window = " ".join(text[start_index : start_index + 250].lower().split())
        
        if "yes" in window:
            return query_str, "YES"
        elif "no" in window:
            return query_str, "NO"
        elif "na" in window:
            return query_str, "NA"
            
    return query_str, "NA"

def generate_interactive_report(text, doc_name, user_query, output_dir):
    """
    Processes extracted document text structures using exact pristine legacy counting rules,
    while dynamically adding the fault-tolerant user query engine layer.
    """
    report = {
        "document_name": doc_name,
        "primary_keywords": {},
        "other_significant_words": {},
        "fraud_query": "",
        "fraud_answer": "",
        "interactive_query": user_query,
        "query_answer": "NA"
    }

    # 1. Targeted Horizontal Query Extraction (100% Replicated Old Code)
    q, a = extract_fraud_status(text)
    report["fraud_query"] = q
    report["fraud_answer"] = a

    # 2. Count Primary Keywords with Template Suppression (100% Replicated Old Code over raw string)
    for key, pattern in REJECS_PATTERNS.items():
        total_matches = len(pattern.findall(text))
        bias = TEMPLATE_BIAS.get(key, 0)
        net_count = max(0, total_matches - bias) 
        
        if net_count > 0:
            report["primary_keywords"][key] = net_count

    # 3. Contextual Significant Words (100% Replicated Old Code)
    words = [w.lower() for w in re.findall(r'\b\w+\b', text)]
    filtered = [w for w in words if w not in INTERNAL_STOP_WORDS and len(w) > 2]
    report["other_significant_words"] = dict(Counter(filtered).most_common(15))

    # 4. Interactive User inquiry Layer (Isolated Variable Path Engine)
    q_str, interactive_ans = resolve_interactive_query(text, user_query)
    report["interactive_query"] = q_str
    report["query_answer"] = interactive_ans

    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, f"{os.path.splitext(doc_name)[0]}.json")
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=4)
    
    return report

def generate_interactive_csv_summary(all_reports, summary_path):
    """
    Consolidates results and prepends precise audit statistics using 
    the dynamic query input text as the column header matrix field.
    """
    if not all_reports: 
        return
    
    total_files = len(all_reports)
    flagged_reports = [r for r in all_reports if r['primary_keywords'] or r['fraud_answer'] == "YES"]
    
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    
    user_query_header = all_reports[0].get("interactive_query", "Query Result Status")
    headers = ["File Name", "Status", user_query_header, "Primary Hits"]
    
    with open(summary_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["AUDIT SUMMARY REPORT"])
        writer.writerow(["Total Documents Parsed", total_files])
        writer.writerow(["Total Flagged Documents", len(flagged_reports)])
        writer.writerow(["Total Clean Documents", total_files - len(flagged_reports)])
        writer.writerow([]) 
        
        writer.writerow(headers)
        for r in all_reports:
            is_flagged = r['primary_keywords'] or r['fraud_answer'] == "YES"
            status = "FLAGGED" if is_flagged else "CLEAN"
            hits = "; ".join([f"{k}({v})" for k, v in r['primary_keywords'].items()])
            
            writer.writerow([
                r['document_name'], 
                status, 
                r['query_answer'], 
                hits if hits else "None"
            ])