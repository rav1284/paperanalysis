import re

def extract_sections(text):
    sections = {
        "title": "",
        "abstract": "",
        "introduction": "",
        "conclusion": ""
    }

    lines = text.split("\n")

    for line in lines:
        if line.strip():
            sections["title"] = line.strip()
            break

    current_section = None

    for line in lines:
        clean_line = line.strip()
        line_lower = clean_line.lower()

        if re.search(r'\babstract\b', line_lower):
            current_section = "abstract"
            continue

        elif re.search(r'\bintroduction\b', line_lower):
            current_section = "introduction"
            continue

        elif re.search(r'\b(conclusion|conclusions|discussion and conclusions)\b', line_lower):
            current_section = "conclusion"        
            continue

        elif re.search(r'\b(references|bibliography|acknowledgment)\b', line_lower):
            current_section = None
            continue

        if current_section:
            sections[current_section] += " " + clean_line

    return sections
