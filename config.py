import re

PRIMARY_KEYWORDS = [
    "EWS", "Early Warning Systems", "Red Flagged", "Misappropriation", 
    "Fraud", "Manipulation", "Cheating", "Concealment", "Impersonation", 
    "Forgery", "Falsification", "Alteration", "Cash Shortage"
]

REJECS_PATTERNS = {
    "ews": re.compile(r"\bews\b", re.IGNORECASE),
    "early_warning_systems": re.compile(r"e[a4]rly\s?w[a4]rn[i1]?ng\s?syst[e3]ms?", re.IGNORECASE),
    "red_flagged": re.compile(r"red[-|\s]?fl[a4]g{1,2}[e3]d?", re.IGNORECASE),
    "misappropriation": re.compile(r"m[i1s]s[-|\s]?app?r[o0]p?r[i1]at[i1][o0]n", re.IGNORECASE),
    "fraud": re.compile(r"fr[a4u]{1,2}d", re.IGNORECASE),
    "manipulation": re.compile(r"m[a4]n[i1]p[u1]?l[a4]t[i1][o0]n", re.IGNORECASE),
    "cheating": re.compile(r"ch[e3][a4]t[i1]ng", re.IGNORECASE),
    "concealment": re.compile(r"conc[e3][a4]nl?m[e3]nt", re.IGNORECASE),
    "impersonation": re.compile(r"[i1]mp[e3]rs[o0]n[a4][i1]?t[i1][o0]n", re.IGNORECASE),
    "forgery": re.compile(r"f[o0]rg[e3]r{1,2}y", re.IGNORECASE),
    "falsification": re.compile(r"f[a4]ls[i1]?f[i1]c[a4]t[i1][o0]n", re.IGNORECASE),
    "alteration": re.compile(r"[a4]lt[e3]r[a4]t[i1][o0]n", re.IGNORECASE),
    "cash_shortage": re.compile(r"c[a4]sh\s?sh[o0]rt[a4e]g[e3]?", re.IGNORECASE)
}

STOP_WORDS = {
    "the", "and", "is", "of", "to", "in", "with", "for", "on", "at", "by", 
    "an", "be", "this", "which", "from", "that", "it", "was", "are", "as",
    "has", "their", "were", "not", "also", "can", "will", "should", "per", 
    "had", "have", "been", "they", "but", "about", "more", "his"
}

INTERNAL_STOP_WORDS = STOP_WORDS.union({word.lower() for word in PRIMARY_KEYWORDS})
FUZZY_THRESHOLD = 2

TEMPLATE_BIAS = {
    "fraud": 2,      
    "ews": 1,        
    "forgery": 1,
    "manipulation": 1,
    "red_flagged": 1,
    "misappropriation": 1,
    "cheating": 1,
    "concealment": 1,
    "impersonation": 1,
    "falsification": 1,
    "alteration": 1,
    "cash_shortage": 1,
    "early_warning_systems": 1
}

AFFIRMATIVE_RESPONSES = {"yes", "true", "confirmed", "identified", "flagged", "positive", "y"}
NEGATIVE_RESPONSES = {"no", "false", "clear", "clean", "unidentified", "negative", "n", "none"}