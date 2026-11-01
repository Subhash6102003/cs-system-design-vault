import os
import re

files = [
    "037_ExpressJS.md",
    "038_NodeJS_PostgreSQL.md",
    "039_NodeJS_Auth_Security.md",
    "040_NodeJS_Advanced.md",
    "041_Python_Backend_Fundamentals.md",
    "042_Python_FastAPI.md",
    "043_Python_SQLAlchemy.md",
    "044_Python_Asyncio_GIL.md",
    "045_Java_SpringBoot_Fundamentals.md",
    "046_Spring_Data_JPA_Hibernate.md",
    "047_Java_VirtualThreads_Reactive.md",
    "048_API_Design_Patterns.md",
    "049_Apache_Kafka.md",
    "050_Backend_Testing.md",
    "051_Microservices_Architecture.md"
]

def parse_markdown(content):
    sections = {}
    current_section = None
    lines = content.split('\n')
    
    section_map = {
        "1.": "OVERVIEW",
        "2.": "KEY_TERMINOLOGY",
        "3.": "DIAGRAMS",
        "4.": "DEMO_CODE",
        "5.": "PRODUCTION_CODE",
        "6.": "INTERVIEW_QUESTIONS",
        "7.": "RIDDLES",
        "8.": "WHY_IT_MATTERS",
        "9.": "CROSS_REFERENCES"
    }

    buffer = []
    
    for line in lines:
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(buffer).strip()
            
            title = line[3:].strip()
            current_section = None
            for key, val in section_map.items():
                if title.startswith(key):
                    current_section = val
                    break
            buffer = []
        else:
            if current_section:
                buffer.append(line)
                
    if current_section:
        sections[current_section] = '\n'.join(buffer).strip()
        
    return sections

def format_overview(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    text = text.replace('Prerequisites:', 'Prerequisites:')
    text = text.replace('What you\'ll learn:', 'What you\'ll learn:')
    return text.strip()

def format_terminology(text):
    out = []
    # match lists like "- **Term**: Def"
    for line in text.split('\n'):
        line = line.strip()
        if not line: continue
        if line.startswith('-'):
            line = line[1:].strip()
            # extract term
            m = re.match(r'\*\*(.*?)\*\*(.*?):(.*)', line)
            if m:
                term = m.group(1).strip()
                defn = m.group(3).strip()
                out.append(f"  {term}\n    {defn}")
                continue
            m = re.match(r'\*\*(.*?)\*\*:(.*)', line)
            if m:
                term = m.group(1).strip()
                defn = m.group(2).strip()
                out.append(f"  {term}\n    {defn}")
                continue
        out.append("  " + line)
    return '\n\n'.join(out)

def format_diagrams(text):
    # Just wrap the code blocks in ASCII boxes
    parts = text.split('```text')
    out = []
    for i in range(len(parts)):
        if i == 0:
            out.append(parts[i].replace('###', ' ').strip())
            continue
        subparts = parts[i].split('```')
        diag = subparts[0].strip("\n")
        
        box = []
        box.append("  ┌─────────────────────────────────────────────────────────────────────────┐")
        for dline in diag.split('\n'):
            box.append(f"  │  {dline.ljust(71)}│")
        box.append("  └─────────────────────────────────────────────────────────────────────────┘")
        
        out.append('\n'.join(box))
        if len(subparts) > 1:
            out.append(subparts[1].strip())
    return '\n\n'.join(out)

def format_code(text):
    out = []
    
    parts = text.split('```')
    for i in range(len(parts)):
        if i % 2 == 0:
            desc = parts[i].replace('###', ' ').strip()
            if desc:
                out.append(f"  {desc}")
        else:
            lang = parts[i].split('\n')[0].strip()
            code = '\n'.join(parts[i].split('\n')[1:])
            code = code.strip('\n')
            
            if lang:
                out.append(f"\n  Language: {lang}\n")
                
            box = []
            box.append("  ┌──────────────────────────────────────────────────────────────────────────┐")
            for cline in code.split('\n'):
                box.append(f"  │  {cline.ljust(72)}│")
            box.append("  └──────────────────────────────────────────────────────────────────────────┘")
            out.append('\n'.join(box))
            
    return '\n\n'.join(out)

def format_qa(text):
    out = []
    qas = re.split(r'\d+\.\s+\*\*(.*?)\*\*', text)
    if len(qas) > 1:
        for i in range(1, len(qas), 2):
            q = qas[i].strip()
            ans_block = qas[i+1].strip()
            # replace *Answer*: 
            ans = re.sub(r'^\*Answer\*:\s*', '', ans_block)
            out.append(f"  Q{ (i+1)//2 }: {q}\n\n  ANSWER:\n    {ans}\n\n  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─")
    return '\n'.join(out).strip(' \n─')

def format_riddles(text):
    out = []
    challenges = text.split('### Challenge ')
    for c in challenges[1:]:
        lines = c.strip().split('\n')
        title_line = lines[0].strip()
        num_title = title_line.split(':', 1)
        if len(num_title) == 2:
            num = num_title[0].strip()
            title = num_title[1].strip()
        else:
            num = ""
            title = title_line
            
        c_rest = '\n'.join(lines[1:])
        
        code_parts = c_rest.split('```')
        code = ""
        if len(code_parts) > 2:
            code = code_parts[1].split('\n', 1)[-1].strip()
            after_code = code_parts[2]
        else:
            after_code = c_rest
            
        whats_wrong = ""
        fix = ""
        
        mw = re.search(r'\*\*What\'s wrong\?\*\*(.*?)(?=\*\*Fix:\*\*|$)', after_code, re.DOTALL)
        if mw: whats_wrong = mw.group(1).strip()
        
        mf = re.search(r'\*\*Fix:\*\*(.*)', after_code, re.DOTALL)
        if mf: fix = mf.group(1).strip()
        
        ch_str = f"  CHALLENGE {num}: {title}\n\n"
        if code:
            for l in code.split('\n'):
                ch_str += f"  {l}\n"
            ch_str += "\n"
            
        ch_str += f"  SOLUTION:\n    What's wrong? {whats_wrong}\n    Fix: {fix}\n"
        ch_str += "\n  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n"
        out.append(ch_str)
        
    return ''.join(out).strip(' \n─')

def format_why(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    lines = text.split('\n')
    out = []
    for l in lines:
        if l.strip().startswith('-'):
            out.append('  ' + l.strip())
        elif l.strip():
            out.append('  ' + l.strip())
    return '\n'.join(out)

def format_cross(text):
    lines = text.split('\n')
    out = []
    for l in lines:
        m = re.search(r'-\s*\[(.*?)\]\((.*?)\)\s*-\s*(.*)', l.strip())
        if m:
            file_title = m.group(1)
            desc = m.group(3)
            out.append(f"  -> File: {file_title} ({desc})")
    return '\n'.join(out)

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    sections = parse_markdown(content)
    
    num_str = re.search(r'\d+', filename).group(0)
    
    out = []
    out.append("================================================================================")
    out.append(f"  FILE {num_str}: {filename.replace('.md', '').upper()}")
    out.append("  Section: D - Backend Development")
    out.append("================================================================================\n")
    
    if "OVERVIEW" in sections:
        out.append("────────────────────────────────────────────────────────────────────────────────")
        out.append("  1. OVERVIEW")
        out.append("────────────────────────────────────────────────────────────────────────────────\n")
        out.append("  " + format_overview(sections["OVERVIEW"]).replace('\n', '\n  ') + "\n")
        
    if "KEY_TERMINOLOGY" in sections:
        out.append("────────────────────────────────────────────────────────────────────────────────")
        out.append("  2. KEY TERMINOLOGY")
        out.append("────────────────────────────────────────────────────────────────────────────────\n")
        out.append(format_terminology(sections["KEY_TERMINOLOGY"]) + "\n")
        
    if "DIAGRAMS" in sections:
        out.append("────────────────────────────────────────────────────────────────────────────────")
        out.append("  3. DIAGRAMS & VISUAL MODELS")
        out.append("────────────────────────────────────────────────────────────────────────────────\n")
        out.append(format_diagrams(sections["DIAGRAMS"]) + "\n")
        
    if "DEMO_CODE" in sections:
        out.append("────────────────────────────────────────────────────────────────────────────────")
        out.append("  5. DEMO CODE")
        out.append("────────────────────────────────────────────────────────────────────────────────\n")
        out.append(format_code(sections["DEMO_CODE"]) + "\n")
        
    if "PRODUCTION_CODE" in sections:
        out.append("────────────────────────────────────────────────────────────────────────────────")
        out.append("  6. PRODUCTION CODE")
        out.append("────────────────────────────────────────────────────────────────────────────────\n")
        out.append(format_code(sections["PRODUCTION_CODE"]) + "\n")
        
    if "INTERVIEW_QUESTIONS" in sections:
        out.append("────────────────────────────────────────────────────────────────────────────────")
        out.append("  7. INTERVIEW QUESTIONS")
        out.append("────────────────────────────────────────────────────────────────────────────────\n")
        out.append(format_qa(sections["INTERVIEW_QUESTIONS"]) + "\n")
        
    if "RIDDLES" in sections:
        out.append("────────────────────────────────────────────────────────────────────────────────")
        out.append("  8. RIDDLES & DEBUGGING CHALLENGES")
        out.append("────────────────────────────────────────────────────────────────────────────────\n")
        out.append(format_riddles(sections["RIDDLES"]) + "\n")
        
    if "WHY_IT_MATTERS" in sections:
        out.append("────────────────────────────────────────────────────────────────────────────────")
        out.append("  9. WHY THIS MATTERS IN PRODUCTION")
        out.append("────────────────────────────────────────────────────────────────────────────────\n")
        out.append(format_why(sections["WHY_IT_MATTERS"]) + "\n")
        
    if "CROSS_REFERENCES" in sections:
        out.append("────────────────────────────────────────────────────────────────────────────────")
        out.append("  10. CROSS-REFERENCES")
        out.append("────────────────────────────────────────────────────────────────────────────────\n")
        out.append(format_cross(sections["CROSS_REFERENCES"]) + "\n")

    out.append("================================================================================")
    out.append(f"  END OF FILE {num_str}")
    out.append("================================================================================")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
        
for f in files:
    try:
        process_file(f)
        print(f"Processed {f}")
    except Exception as e:
        print(f"Failed {f}: {e}")
