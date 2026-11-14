
NIC_OPTIONS = {
    "62011": "Writing, modifying and testing computer programs",
    "62012": "Web-page designing",
    "62013": "Software support and maintenance",
    "62020": "Computer consultancy and facilities management"
}

def suggest_nic_codes(description):
    description = description.lower()
    suggestions = []

    keywords = {
        "62011": ["software development", "programming", "coding", "application development"],
        "62012": ["website design", "web-page designing", "web design"],
        "62013": ["software support", "software maintenance"],
        "62020": ["it consulting", "computer consultancy", "systems consultancy"]
    }

    for code, terms in keywords.items():
        if any(term in description for term in terms):
            suggestions.append({
                "code": code,
                "description": NIC_OPTIONS[code]
            })

    return suggestions
