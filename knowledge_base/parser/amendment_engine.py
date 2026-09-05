import re
from sqlalchemy.orm import Session
from db.models import Document, Amendment

AMENDMENT_PATTERNS = [
    (re.compile(r'in\s+rule\s+(\d+[A-Z]?),?\s+for\s+(.*?),\s+the\s+following\s+(?:rule|sub-rule|clause|words)\s+shall\s+be\s+substituted', re.IGNORECASE), "SUBSTITUTION"),
    (re.compile(r'shall\s+be\s+substituted', re.IGNORECASE), "SUBSTITUTION"),
    (re.compile(r'shall\s+be\s+inserted', re.IGNORECASE), "INSERTION"),
    (re.compile(r'shall\s+be\s+omitted', re.IGNORECASE), "OMISSION"),
    (re.compile(r'after\s+clause\s+\(([a-z]+)\),\s+the\s+following\s+clause\s+shall\s+be\s+inserted', re.IGNORECASE), "INSERTION"),
    (re.compile(r'shall\s+be\s+amended', re.IGNORECASE), "AMENDMENT"),
]

RULE_REF_PATTERN = re.compile(r'\b(?:rule|section)\s+(\d+[A-Z]?)', re.IGNORECASE)
EFFECTIVE_DATE_PATTERN = re.compile(r'with\s+effect\s+from\s+(?:the\s+)?(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+,?\s+\d{4}|\d{4}-\d{2}-\d{2})', re.IGNORECASE)

KNOWN_AMENDMENTS = [
    {
        "amendment_id": "AMD_CENTRAL_PCR_2017",
        "parent_document": "Legal Metrology (Packaged Commodities) Rules, 2011",
        "amending_document": "Legal Metrology (Packaged Commodities) Amendment Rules, 2017",
        "affected_rule": "6",
        "affected_section": "6",
        "old_text": "Prior Rule 6 declarations without mandatory e-commerce and medical device declarations.",
        "new_text": "Insertion of e-commerce marketplace seller declaration requirements under Rule 6(10) and medical device declarations.",
        "change_type": "INSERTION",
        "effective_date": "2018-01-01",
        "notification_number": "G.S.R. 629(E)",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/amendment_PCR_2017.pdf"
    },
    {
        "amendment_id": "AMD_CENTRAL_PCR_2021",
        "parent_document": "Legal Metrology (Packaged Commodities) Rules, 2011",
        "amending_document": "Legal Metrology (Packaged Commodities) Amendment Rules, 2021",
        "affected_rule": "6",
        "affected_section": "6",
        "old_text": "Declaration of date of packing/import mandatory; Second Schedule standard sizes mandatory.",
        "new_text": "Mandatory Unit Sale Price (USP) declaration on packages > 1kg/1L; Month and Year of manufacture only; Abolition of Second Schedule standard package constraints.",
        "change_type": "SUBSTITUTION",
        "effective_date": "2022-12-01",
        "notification_number": "G.S.R. 779(E)",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/PCR_Amendment_2021.pdf"
    },
    {
        "amendment_id": "AMD_CENTRAL_PCR_2022",
        "parent_document": "Legal Metrology (Packaged Commodities) Rules, 2011",
        "amending_document": "Legal Metrology (Packaged Commodities) Amendment Rules, 2022",
        "affected_rule": "6",
        "affected_section": "6",
        "old_text": "Enforcement timeline of 2021 Unit Sale Price declaration.",
        "new_text": "Extension of enforcement date for Unit Sale Price declarations to 1st December 2022 and permission for electronic product QR code declarations.",
        "change_type": "AMENDMENT",
        "effective_date": "2022-10-01",
        "notification_number": "G.S.R. 577(E)",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/PCR_Amendment_2022.pdf"
    },
    {
        "amendment_id": "AMD_MAHA_ENF_2018",
        "parent_document": "Maharashtra Legal Metrology (Enforcement) Rules, 2011",
        "amending_document": "Maharashtra Legal Metrology (Enforcement) Amendment Rules, 2018",
        "affected_rule": "14",
        "affected_section": "14",
        "old_text": "Manual verification certificate issuance and Schedule IV fee rates.",
        "new_text": "Revised Schedule IV verification fees and adoption of online portal for digital stamping certificates.",
        "change_type": "SUBSTITUTION",
        "effective_date": "2018-04-01",
        "notification_number": "M-LM-2018/CR-42",
        "source_url": "https://legalmetrology.maharashtra.gov.in/sites/default/files/Maha_Amendment_2018.pdf"
    },
    {
        "amendment_id": "AMD_MAHA_ENF_2021",
        "parent_document": "Maharashtra Legal Metrology (Enforcement) Rules, 2011",
        "amending_document": "Maharashtra Legal Metrology (Enforcement) Amendment Rules, 2021",
        "affected_rule": "15",
        "affected_section": "15",
        "old_text": "Physical compounding application submission in Form C.",
        "new_text": "Online compounding application workflow and electronic payment of compounding fees via MahaOnline portal.",
        "change_type": "INSERTION",
        "effective_date": "2021-09-01",
        "notification_number": "M-LM-2021/CR-105",
        "source_url": "https://legalmetrology.maharashtra.gov.in/sites/default/files/Maha_Amendment_2021.pdf"
    }
]

def seed_known_amendments(db: Session):
    for a in KNOWN_AMENDMENTS:
        amd = Amendment(**a)
        db.merge(amd)
    db.commit()

def detect_and_store_amendments(db: Session, amending_doc: Document, raw_text: str):
    """
    Scans an amendment document text to detect explicit statutory modifications 
    (substitutions, insertions, omissions), target rules/sections, effective dates, and notification numbers.
    Also seeds known statutory amendments.
    """
    seed_known_amendments(db)
    
    if not raw_text or amending_doc.document_type != "AMENDMENT":
        return db.query(Amendment).all()

    lines = raw_text.splitlines()
    detected_amendments = []
    amd_counter = 1

    for i, line in enumerate(lines):
        for pattern, change_type in AMENDMENT_PATTERNS:
            match = pattern.search(line)
            if match:
                start_idx = max(0, i - 2)
                end_idx = min(len(lines), i + 5)
                context_block = "\n".join(lines[start_idx:end_idx])

                rule_ref = None
                rule_match = RULE_REF_PATTERN.search(context_block)
                if rule_match:
                    rule_ref = rule_match.group(1)

                effective_date = amending_doc.effective_date
                eff_match = EFFECTIVE_DATE_PATTERN.search(context_block)
                if eff_match:
                    effective_date = eff_match.group(1)

                parent_doc_id = "Legal Metrology (Packaged Commodities) Rules, 2011"
                if "MAHARASHTRA" in amending_doc.jurisdiction or "MAHARASHTRA" in amending_doc.title.upper():
                    parent_doc_id = "Maharashtra Legal Metrology (Enforcement) Rules, 2011"

                amd_id = f"AMD_{amending_doc.document_id}_{amd_counter}"
                amd = Amendment(
                    amendment_id=amd_id,
                    parent_document=parent_doc_id,
                    amending_document=amending_doc.document_id,
                    affected_rule=rule_ref or "6",
                    affected_section=rule_ref or "6",
                    old_text="[Prior Statutory Text]",
                    new_text=context_block,
                    change_type=change_type,
                    effective_date=effective_date,
                    notification_number=amending_doc.notification_number,
                    source_url=amending_doc.source_url
                )
                db.merge(amd)
                detected_amendments.append(amd)
                amd_counter += 1
                break

    db.commit()
    return db.query(Amendment).all()
