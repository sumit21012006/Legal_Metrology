import re
from sqlalchemy.orm import Session
from db.models import Document, LegalProvision

# Regex patterns for Indian legal hierarchy (Section, Rule, Sub-rule, Clause, Schedule, Chapter)
SECTION_PATTERN = re.compile(r'^(?:SECTION|Section)\s+(\d+[A-Z]?)\b[:\.]?\s*(.*)', re.IGNORECASE)
RULE_PATTERN = re.compile(r'^(?:RULE|Rule)\s+(\d+[A-Z]?)\b[:\.]?\s*(.*)', re.IGNORECASE)
SUB_RULE_PATTERN = re.compile(r'^\((\d+)\)\s*(.*)')
CLAUSE_PATTERN = re.compile(r'^\(([a-z]{1,2})\)\s*(.*)')
SCHEDULE_PATTERN = re.compile(r'^(?:SCHEDULE|Schedule)\s+([IVXLCDM\d]+)\b[:\.]?\s*(.*)', re.IGNORECASE)
CHAPTER_PATTERN = re.compile(r'^(?:CHAPTER|Chapter)\s+([IVXLCDM\d]+)\b[:\.]?\s*(.*)', re.IGNORECASE)

def parse_and_store_legal_structure(db: Session, document: Document, raw_text: str):
    """
    Parses document raw text into hierarchical LegalProvision entries (Section/Rule/Sub-rule/Clause/Schedule).
    """
    if not raw_text:
        return []

    lines = raw_text.splitlines()
    provisions = []
    
    current_chapter = None
    current_section = None
    current_rule = None
    current_sub_rule = None
    current_clause = None
    current_schedule = None
    
    buf = []
    page_num = 1
    prov_counter = 1

    def flush_buffer():
        nonlocal buf, prov_counter
        if not buf:
            return
        content = "\n".join(buf).strip()
        if len(content) < 10:
            buf = []
            return

        prov_id = f"{document.document_id}_P{prov_counter}"
        prov = LegalProvision(
            provision_id=prov_id,
            document_id=document.document_id,
            chapter=current_chapter,
            section=current_section,
            rule=current_rule,
            sub_rule=current_sub_rule,
            clause=current_clause,
            schedule=current_schedule,
            text=content,
            page=page_num,
            effective_date=document.effective_date,
            status=document.status
        )
        db.merge(prov)
        provisions.append(prov)
        prov_counter += 1
        buf = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Page separator check if present
        if stripped.startswith("--- Page ") or stripped.startswith("[Page "):
            try:
                page_num = int(re.findall(r'\d+', stripped)[0])
            except Exception:
                pass
            continue

        ch_match = CHAPTER_PATTERN.match(stripped)
        if ch_match:
            flush_buffer()
            current_chapter = f"Chapter {ch_match.group(1)}"
            buf.append(stripped)
            continue

        sec_match = SECTION_PATTERN.match(stripped)
        if sec_match:
            flush_buffer()
            current_section = sec_match.group(1)
            current_rule = None
            current_sub_rule = None
            current_clause = None
            buf.append(stripped)
            continue

        rule_match = RULE_PATTERN.match(stripped)
        if rule_match:
            flush_buffer()
            current_rule = rule_match.group(1)
            current_sub_rule = None
            current_clause = None
            buf.append(stripped)
            continue

        sub_rule_match = SUB_RULE_PATTERN.match(stripped)
        if sub_rule_match and (current_rule or current_section):
            flush_buffer()
            current_sub_rule = sub_rule_match.group(1)
            current_clause = None
            buf.append(stripped)
            continue

        clause_match = CLAUSE_PATTERN.match(stripped)
        if clause_match and current_sub_rule:
            flush_buffer()
            current_clause = clause_match.group(1)
            buf.append(stripped)
            continue

        sch_match = SCHEDULE_PATTERN.match(stripped)
        if sch_match:
            flush_buffer()
            current_schedule = f"Schedule {sch_match.group(1)}"
            buf.append(stripped)
            continue

        buf.append(stripped)

    flush_buffer()
    db.commit()
    return provisions
