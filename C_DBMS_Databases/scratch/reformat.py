import os
import re
import glob

TEMPLATE_DIR = r"d:\placement\LIBRARY\C_DBMS_Databases"
files = sorted(glob.glob(os.path.join(TEMPLATE_DIR, "*.md")))

for file_path in files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    filename = os.path.basename(file_path)
    file_num = filename.split("_")[0]
    
    # Extract Title from `# Title`
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename
    
    lines = content.split('\n')
    
    # Simple state machine
    sections = {}
    current_section = None
    current_content = []
    
    for line in lines:
        if line.startswith('## 1.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'OVERVIEW'
            current_content = []
        elif line.startswith('## 2.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'KEY TERMINOLOGY'
            current_content = []
        elif line.startswith('## 3.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'DIAGRAMS'
            current_content = []
        elif line.startswith('## 4.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'DEMO CODE'
            current_content = []
        elif line.startswith('## 5.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'PRODUCTION CODE'
            current_content = []
        elif line.startswith('## 6.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'INTERVIEW QUESTIONS'
            current_content = []
        elif line.startswith('## 7.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'RIDDLES'
            current_content = []
        elif line.startswith('## 8.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'WHY THIS MATTERS'
            current_content = []
        elif line.startswith('## 9.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'CROSS-REFERENCES'
            current_content = []
        elif line.startswith('## 10.'):
            if current_section: sections[current_section] = '\n'.join(current_content)
            current_section = 'CROSS-REFERENCES_10'
            current_content = []
        else:
            if current_section and not line.startswith('# '+title):
                current_content.append(line)
                
    if current_section:
        sections[current_section] = '\n'.join(current_content)
        
    # Now format them
    output = []
    output.append("================================================================================")
    output.append(f"  FILE {file_num}: {title.upper()}")
    output.append(f"  Section: C - DBMS & Databases")
    output.append("================================================================================")
    
    sec_num = 1
    
    # 1. OVERVIEW
    if 'OVERVIEW' in sections:
        output.append("")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append(f"  {sec_num}. OVERVIEW")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append("")
        text = sections['OVERVIEW']
        text = re.sub(r'^\*\*.*?\*\*\s*', '', text, flags=re.MULTILINE) # remove title bold
        for l in text.strip().split('\n'):
            if l.strip():
                output.append("  " + l)
        sec_num += 1

    # 2. KEY TERMINOLOGY
    if 'KEY TERMINOLOGY' in sections:
        output.append("")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append(f"  {sec_num}. KEY TERMINOLOGY")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append("")
        text = sections['KEY TERMINOLOGY']
        # Extract terms: *   **Term**: Definition or * **Term**: Definition
        term_pattern = re.compile(r'^\*\s+\*\*(.*?)\*\*(?:\s*:\s*(.*))?', re.MULTILINE)
        last_idx = 0
        
        lines_t = text.split('\n')
        for l in lines_t:
            m = re.match(r'^\*\s+\*\*(.*?)\*\*(?:\s*:\s*(.*))?', l)
            if m:
                term = m.group(1).upper()
                dfn = m.group(2) if m.group(2) else ""
                output.append(f"  {term}")
                if dfn:
                    output.append(f"    {dfn}")
            else:
                m2 = re.match(r'^\s+\*\s+\*(.*?)\*(?:\s*:\s*(.*))?', l)
                if m2:
                    output.append(f"    - {m2.group(1)}: {m2.group(2)}")
                elif l.strip():
                    output.append(f"    {l.strip()}")
        sec_num += 1
        
    # 3. DIAGRAMS
    if 'DIAGRAMS' in sections:
        output.append("")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append(f"  {sec_num}. DIAGRAMS & VISUAL MODELS")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append("")
        text = sections['DIAGRAMS']
        blocks = text.split('###')
        for b in blocks:
            b = b.strip()
            if not b: continue
            lines_b = b.split('\n')
            d_title = lines_b[0].strip()
            
            box_content = []
            in_code = False
            out_of_box = []
            for l in lines_b[1:]:
                if l.strip().startswith('```'):
                    in_code = not in_code
                    continue
                if in_code:
                    box_content.append(l)
                else:
                    if l.strip():
                        # strip out markdown
                        l = l.replace('*', '')
                        out_of_box.append("  " + l.strip())
            
            output.append("  ┌─────────────────────────────────────────────────────────────────────────┐")
            output.append(f"  │  {d_title.upper():<71}│")
            output.append("  │                                                                         │")
            for bc in box_content:
                # pad or truncate roughly to 71 chars
                bc_padded = bc.ljust(71)
                if len(bc_padded) > 71: bc_padded = bc_padded[:71]
                output.append(f"  │  {bc_padded}│")
            output.append("  │                                                                         │")
            output.append("  └─────────────────────────────────────────────────────────────────────────┘")
            output.append("")
            output.extend(out_of_box)
            output.append("")
        sec_num += 1

    # 4. EXPLANATION & THEORY (skip if empty)
    # 5. DEMO CODE
    if 'DEMO CODE' in sections:
        output.append("")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append(f"  {sec_num}. DEMO CODE")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append("")
        text = sections['DEMO CODE']
        blocks = text.split('###')
        for b in blocks:
            b = b.strip()
            if not b: continue
            lines_b = b.split('\n')
            c_title = lines_b[0].strip()
            
            box_content = []
            lang = ""
            in_code = False
            out_of_box = []
            for l in lines_b[1:]:
                if l.strip().startswith('```'):
                    if not in_code:
                        lang = l.strip()[3:].upper()
                        if lang == "SQL": lang = "SQL"
                        elif lang == "JAVASCRIPT": lang = "JavaScript"
                    in_code = not in_code
                    continue
                if in_code:
                    box_content.append(l)
                else:
                    if l.strip():
                        l = l.replace('*', '')
                        out_of_box.append("  " + l.strip())
            
            if lang:
                output.append(f"  [Language: {lang}]")
            output.append("")
            output.append("  ┌──────────────────────────────────────────────────────────────────────────┐")
            output.append(f"  │  // {c_title:<69}│")
            output.append("  │                                                                          │")
            for bc in box_content:
                # pad to 72 chars
                bc_padded = bc.ljust(72)
                if len(bc_padded) > 72: bc_padded = bc_padded[:72]
                output.append(f"  │  {bc_padded}│")
            output.append("  │                                                                          │")
            output.append("  └──────────────────────────────────────────────────────────────────────────┘")
            output.append("")
            output.extend(out_of_box)
            output.append("")
        sec_num += 1

    # 6. PRODUCTION CODE
    if 'PRODUCTION CODE' in sections:
        output.append("")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append(f"  {sec_num}. PRODUCTION CODE")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append("")
        text = sections['PRODUCTION CODE']
        blocks = text.split('###')
        for b in blocks:
            b = b.strip()
            if not b: continue
            lines_b = b.split('\n')
            c_title = lines_b[0].strip()
            
            box_content = []
            lang = ""
            in_code = False
            out_of_box = []
            for l in lines_b[1:]:
                if l.strip().startswith('```'):
                    if not in_code:
                        lang = l.strip()[3:].upper()
                    in_code = not in_code
                    continue
                if in_code:
                    box_content.append(l)
                else:
                    if l.strip():
                        l = l.replace('*', '')
                        out_of_box.append("  " + l.strip())
                        
            if lang:
                output.append(f"  [Language: {lang}]")
            output.append("")
            output.append("  ┌──────────────────────────────────────────────────────────────────────────┐")
            if c_title and not c_title.startswith("Production"):
                output.append(f"  │  // {c_title:<69}│")
                output.append("  │                                                                          │")
            for bc in box_content:
                bc_padded = bc.ljust(72)
                if len(bc_padded) > 72: bc_padded = bc_padded[:72]
                output.append(f"  │  {bc_padded}│")
            output.append("  │                                                                          │")
            output.append("  └──────────────────────────────────────────────────────────────────────────┘")
            output.append("")
            output.extend(out_of_box)
            output.append("")
        sec_num += 1
        
    # 7. INTERVIEW QUESTIONS
    if 'INTERVIEW QUESTIONS' in sections:
        output.append("")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append(f"  {sec_num}. INTERVIEW QUESTIONS")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append("")
        text = sections['INTERVIEW QUESTIONS']
        # split by digit.
        q_blocks = re.split(r'\n\d+\.\s+\*\*(.*?)\*\*', '\n' + text)
        for i in range(1, len(q_blocks), 2):
            q_text = q_blocks[i]
            ans_block = q_blocks[i+1]
            output.append(f"  Q{(i+1)//2}: {q_text}")
            output.append("")
            output.append("  ANSWER:")
            
            ans_lines = ans_block.split('\n')
            for l in ans_lines:
                if l.strip().startswith('*   *Answer*:'):
                    output.append(f"    {l.strip()[14:].strip()}")
                elif l.strip().startswith('*Answer*:'):
                    output.append(f"    {l.strip()[9:].strip()}")
                elif l.strip():
                    # clean up bullets
                    l = l.replace('*', '')
                    output.append(f"    {l.strip()}")
            
            if i < len(q_blocks) - 2:
                output.append("")
                output.append("  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─")
                output.append("")
        sec_num += 1

    # 8. RIDDLES
    if 'RIDDLES' in sections:
        output.append("")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append(f"  {sec_num}. RIDDLES & DEBUGGING CHALLENGES")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append("")
        text = sections['RIDDLES']
        blocks = text.split('### Challenge')
        for i, b in enumerate(blocks):
            if not b.strip(): continue
            b = b.strip()
            lines_b = b.split('\n')
            
            # Title
            first_line = lines_b[0].strip()
            # usually like " 1: Title"
            m = re.match(r'^\s*\d+:\s*(.*)', first_line)
            title = m.group(1) if m else first_line
            
            output.append(f"  CHALLENGE {i}: {title}")
            output.append("")
            
            in_code = False
            for l in lines_b[1:]:
                l = l.strip()
                if l.startswith('```'):
                    continue
                if l.startswith('*   **Problem**:'):
                    output.append(f"  PROBLEM:")
                    output.append(f"    {l[16:].strip()}")
                elif l.startswith('*   **Solution**:'):
                    output.append("")
                    output.append(f"  SOLUTION:")
                    output.append(f"    {l[17:].strip()}")
                elif l:
                    l = l.replace('*', '')
                    output.append(f"  {l}")
                    
            if i < len(blocks) - 1:
                output.append("")
                output.append("  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─")
                output.append("")
        sec_num += 1
        
    # 9. WHY THIS MATTERS
    if 'WHY THIS MATTERS' in sections:
        output.append("")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append(f"  {sec_num}. WHY THIS MATTERS IN PRODUCTION")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append("")
        text = sections['WHY THIS MATTERS']
        for l in text.split('\n'):
            if l.strip().startswith('*   **'):
                m = re.match(r'^\*\s+\*\*(.*?)\*\*(?:\s*:\s*(.*))?', l)
                if m:
                    output.append(f"  {m.group(1).upper()}: {m.group(2)}")
            elif l.strip():
                output.append("  " + l.strip().replace('*', ''))
        sec_num += 1

    # 10. CROSS-REFERENCES
    cr_sec = 'CROSS-REFERENCES' if 'CROSS-REFERENCES' in sections else 'CROSS-REFERENCES_10' if 'CROSS-REFERENCES_10' in sections else None
    if cr_sec:
        output.append("")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append(f"  {sec_num}. CROSS-REFERENCES")
        output.append("────────────────────────────────────────────────────────────────────────────────")
        output.append("")
        text = sections[cr_sec]
        for l in text.split('\n'):
            if l.strip().startswith('*'):
                m = re.search(r'\[(.*?)\]\(.*?\)[\s-]+(.*)', l)
                if m:
                    output.append(f"  -> File {m.group(1)[:3]}: {m.group(1)[4:].replace('.md','')} ({m.group(2)})")
                else:
                    output.append(f"  -> {l.replace('*','').strip()}")
    
    output.append("")
    output.append("================================================================================")
    output.append(f"  END OF FILE {file_num}")
    output.append("================================================================================")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

print("Done reformating files.")
