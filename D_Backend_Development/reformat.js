const fs = require('fs');
const path = require('path');

const files = [
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
];

const dir = 'd:\\placement\\LIBRARY\\D_Backend_Development';

function parseMarkdown(content) {
    const sections = {};
    let currentSection = null;
    const lines = content.split('\n');
    
    const sectionMap = {
        "1.": "OVERVIEW",
        "2.": "KEY_TERMINOLOGY",
        "3.": "DIAGRAMS",
        "4.": "DEMO_CODE",
        "5.": "PRODUCTION_CODE",
        "6.": "INTERVIEW_QUESTIONS",
        "7.": "RIDDLES",
        "8.": "WHY_IT_MATTERS",
        "9.": "CROSS_REFERENCES"
    };

    let buffer = [];
    
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        if (line.startsWith('## ')) {
            if (currentSection) {
                sections[currentSection] = buffer.join('\n').trim();
            }
            
            let title = line.substring(3).trim();
            currentSection = null;
            for (const [key, val] of Object.entries(sectionMap)) {
                if (title.startsWith(key)) {
                    currentSection = val;
                    break;
                }
            }
            buffer = [];
        } else {
            if (currentSection) {
                buffer.push(line);
            }
        }
    }
                
    if (currentSection) {
        sections[currentSection] = buffer.join('\n').trim();
    }
        
    return sections;
}

function formatOverview(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, '$1');
    text = text.replace(/_(.*?)_/g, '$1');
    return text.trim();
}

function formatTerminology(text) {
    let out = [];
    let lines = text.split('\n');
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        if (!line) continue;
        if (line.startsWith('-')) {
            line = line.substring(1).trim();
            let m = line.match(/\*\*(.*?)\*\*(.*?):(.*)/);
            if (m) {
                let term = m[1].trim();
                let defn = m[3].trim();
                out.push(`  ${term}\n    ${defn}`);
                continue;
            }
            m = line.match(/\*\*(.*?)\*\*:(.*)/);
            if (m) {
                let term = m[1].trim();
                let defn = m[2].trim();
                out.push(`  ${term}\n    ${defn}`);
                continue;
            }
        }
        out.push("  " + line);
    }
    return out.join('\n\n');
}

function formatDiagrams(text) {
    let parts = text.split('```text');
    let out = [];
    for (let i = 0; i < parts.length; i++) {
        if (i === 0) {
            let desc = parts[i].replace(/###/g, ' ').trim();
            if (desc) out.push("  " + desc);
            continue;
        }
        let subparts = parts[i].split('```');
        let diag = subparts[0].replace(/^\n|\n$/g, '');
        
        let box = [];
        box.push("  ┌─────────────────────────────────────────────────────────────────────────┐");
        let dlines = diag.split('\n');
        for (let j = 0; j < dlines.length; j++) {
            box.push(`  │  ${dlines[j].padEnd(71, ' ')}│`);
        }
        box.push("  └─────────────────────────────────────────────────────────────────────────┘");
        
        out.push(box.join('\n'));
        if (subparts.length > 1 && subparts[1].trim()) {
            out.push(subparts[1].trim());
        }
    }
    return out.join('\n\n');
}

function formatCode(text) {
    let out = [];
    let parts = text.split('```');
    for (let i = 0; i < parts.length; i++) {
        if (i % 2 === 0) {
            let desc = parts[i].replace(/###/g, ' ').trim();
            if (desc) {
                out.push(`  ${desc}`);
            }
        } else {
            let clines = parts[i].split('\n');
            let lang = clines[0].trim();
            let code = clines.slice(1).join('\n').replace(/^\n|\n$/g, '');
            
            if (lang) {
                out.push(`\n  Language: ${lang}\n`);
            }
            
            let box = [];
            box.push("  ┌──────────────────────────────────────────────────────────────────────────┐");
            let lines = code.split('\n');
            for (let j = 0; j < lines.length; j++) {
                box.push(`  │  ${lines[j].padEnd(72, ' ')}│`);
            }
            box.push("  └──────────────────────────────────────────────────────────────────────────┘");
            out.push(box.join('\n'));
        }
    }
    return out.join('\n\n');
}

function formatQA(text) {
    let out = [];
    let qas = text.split(/\d+\.\s+\*\*(.*?)\*\*/);
    if (qas.length > 1) {
        for (let i = 1; i < qas.length; i += 2) {
            let q = qas[i].trim();
            let ans_block = qas[i+1].trim();
            let ans = ans_block.replace(/^\*Answer\*:\s*/, '').trim();
            out.push(`  Q${(i+1)/2}: ${q}\n\n  ANSWER:\n    ${ans}\n\n  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─`);
        }
    }
    let res = out.join('\n\n');
    return res.replace(/\n\n\s*─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─$/, '');
}

function formatRiddles(text) {
    let out = [];
    let challenges = text.split('### Challenge ');
    for (let i = 1; i < challenges.length; i++) {
        let c = challenges[i].trim();
        let lines = c.split('\n');
        let title_line = lines[0].trim();
        let num_title = title_line.split(':');
        let num = num_title[0].trim();
        let title = num_title.slice(1).join(':').trim();
        
        let c_rest = lines.slice(1).join('\n');
        let code_parts = c_rest.split('```');
        let code = "";
        let after_code = c_rest;
        
        if (code_parts.length > 2) {
            let clines = code_parts[1].split('\n');
            code = clines.slice(1).join('\n').replace(/^\n|\n$/g, '');
            after_code = code_parts[2];
        }
        
        let whats_wrong = "";
        let fix = "";
        
        let mw = after_code.match(/\*\*What\'s wrong\?\*\*(.*?)(?=\*\*Fix:\*\*|$)/s);
        if (mw) whats_wrong = mw[1].trim();
        
        let mf = after_code.match(/\*\*Fix:\*\*(.*)/s);
        if (mf) fix = mf[1].trim();
        
        let ch_str = `  CHALLENGE ${num}: ${title}\n\n`;
        if (code) {
            let lines = code.split('\n');
            for (let j = 0; j < lines.length; j++) {
                ch_str += `  ${lines[j]}\n`;
            }
            ch_str += "\n";
        }
        
        ch_str += `  SOLUTION:\n    What's wrong? ${whats_wrong}\n    Fix: ${fix}\n`;
        ch_str += "\n  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n";
        out.push(ch_str);
    }
    return out.join('').replace(/\n  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n$/, '');
}

function formatWhy(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, '$1');
    let lines = text.split('\n');
    let out = [];
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].trim().startsWith('-')) {
            out.push('  ' + lines[i].trim());
        } else if (lines[i].trim()) {
            out.push('  ' + lines[i].trim());
        }
    }
    return out.join('\n');
}

function formatCross(text) {
    let lines = text.split('\n');
    let out = [];
    for (let i = 0; i < lines.length; i++) {
        let m = lines[i].trim().match(/-\s*\[(.*?)\]\((.*?)\)\s*-\s*(.*)/);
        if (m) {
            out.push(`  -> File ${m[1].split('_')[0].replace(/^0+/, '')}: ${m[1].split('_').slice(1).join(' ').replace('.md', '')} (${m[3]})`);
        }
    }
    return out.join('\n');
}

for (let i = 0; i < files.length; i++) {
    let filename = files[i];
    let filepath = path.join(dir, filename);
    let content = fs.readFileSync(filepath, 'utf8');
    
    let sections = parseMarkdown(content);
    let num_str = filename.match(/\d+/)[0];
    let title_str = filename.replace(/\.md$/, '').replace(/^\d+_/, '').replace(/_/g, ' ').toUpperCase();
    
    let out = [];
    out.push("================================================================================");
    out.push(`  FILE ${num_str}: ${title_str}`);
    out.push("  Section: D - Backend Development");
    out.push("================================================================================\n");
    
    if (sections["OVERVIEW"]) {
        out.push("────────────────────────────────────────────────────────────────────────────────");
        out.push("  1. OVERVIEW");
        out.push("────────────────────────────────────────────────────────────────────────────────\n");
        let o = formatOverview(sections["OVERVIEW"]);
        out.push("  " + o.replace(/\n/g, '\n  ') + "\n");
    }
    
    if (sections["KEY_TERMINOLOGY"]) {
        out.push("────────────────────────────────────────────────────────────────────────────────");
        out.push("  2. KEY TERMINOLOGY");
        out.push("────────────────────────────────────────────────────────────────────────────────\n");
        out.push(formatTerminology(sections["KEY_TERMINOLOGY"]) + "\n");
    }
    
    if (sections["DIAGRAMS"]) {
        out.push("────────────────────────────────────────────────────────────────────────────────");
        out.push("  3. DIAGRAMS & VISUAL MODELS");
        out.push("────────────────────────────────────────────────────────────────────────────────\n");
        out.push(formatDiagrams(sections["DIAGRAMS"]) + "\n");
    }
    
    if (sections["DEMO_CODE"]) {
        out.push("────────────────────────────────────────────────────────────────────────────────");
        out.push("  5. DEMO CODE");
        out.push("────────────────────────────────────────────────────────────────────────────────\n");
        out.push(formatCode(sections["DEMO_CODE"]) + "\n");
    }
    
    if (sections["PRODUCTION_CODE"]) {
        out.push("────────────────────────────────────────────────────────────────────────────────");
        out.push("  6. PRODUCTION CODE");
        out.push("────────────────────────────────────────────────────────────────────────────────\n");
        out.push(formatCode(sections["PRODUCTION_CODE"]) + "\n");
    }
    
    if (sections["INTERVIEW_QUESTIONS"]) {
        out.push("────────────────────────────────────────────────────────────────────────────────");
        out.push("  7. INTERVIEW QUESTIONS");
        out.push("────────────────────────────────────────────────────────────────────────────────\n");
        out.push(formatQA(sections["INTERVIEW_QUESTIONS"]) + "\n");
    }
    
    if (sections["RIDDLES"]) {
        out.push("────────────────────────────────────────────────────────────────────────────────");
        out.push("  8. RIDDLES & DEBUGGING CHALLENGES");
        out.push("────────────────────────────────────────────────────────────────────────────────\n");
        out.push(formatRiddles(sections["RIDDLES"]) + "\n");
    }
    
    if (sections["WHY_IT_MATTERS"]) {
        out.push("────────────────────────────────────────────────────────────────────────────────");
        out.push("  9. WHY THIS MATTERS IN PRODUCTION");
        out.push("────────────────────────────────────────────────────────────────────────────────\n");
        out.push(formatWhy(sections["WHY_IT_MATTERS"]) + "\n");
    }
    
    if (sections["CROSS_REFERENCES"]) {
        out.push("────────────────────────────────────────────────────────────────────────────────");
        out.push("  10. CROSS-REFERENCES");
        out.push("────────────────────────────────────────────────────────────────────────────────\n");
        out.push(formatCross(sections["CROSS_REFERENCES"]) + "\n");
    }

    out.push("================================================================================");
    out.push(`  END OF FILE ${num_str}`);
    out.push("================================================================================");
    
    fs.writeFileSync(filepath, out.join('\n') + '\n', 'utf8');
    console.log(`Processed ${filename}`);
}
