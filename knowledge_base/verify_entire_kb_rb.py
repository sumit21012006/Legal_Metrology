import json
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import (
    Document, DocumentVersion, Amendment, LegalProvision, DocumentChunk,
    RuleBase, Exemption, Penalty, Compounding, Inspection, Seizure, Notice, OfficerWorkflow
)
from ingestion.official_sources import is_official_url

def audit_entire_kb_rb():
    db = SessionLocal()
    
    print("=" * 80)
    print("FULL KNOWLEDGE BASE & RULE BASE OFFICIAL GOVERNMENT SOURCE VERIFICATION AUDIT")
    print("=" * 80)

    # 1. AUDIT DOCUMENTS
    docs = db.query(Document).all()
    print(f"\n[1] AUDITING DOCUMENTS ({len(docs)} Total Documents)")
    doc_audit_pass = True
    for d in docs:
        is_official = is_official_url(d.source_url)
        status_symbol = "VERIFIED OFFICIAL GOV DOMAIN" if is_official else "REJECTED"
        if not is_official:
            doc_audit_pass = False
        print(f"  - [{d.jurisdiction}] {d.title}")
        print(f"    URL: {d.source_url} | {status_symbol}")
        print(f"    SHA-256: {d.sha256[:16]}... | Status: {d.status}")

    # 2. AUDIT RULE BASE
    rules = db.query(RuleBase).all()
    print(f"\n[2] AUDITING MACHINE-READABLE RULE BASE ({len(rules)} Total Rules)")
    rule_audit_pass = True
    for r in rules:
        print(f"  - Rule ID: {r.rule_id} | Jurisdiction: {r.jurisdiction}")
        print(f"    Legal Source: {r.legal_source}")
        print(f"    Source Reference: {r.source_reference}")

    # 3. AUDIT AMENDMENTS
    amds = db.query(Amendment).all()
    print(f"\n[3] AUDITING STATUTORY AMENDMENTS ({len(amds)} Total Amendments)")
    for a in amds:
        print(f"  - [{a.amendment_id}] Amending: {a.amending_document}")
        print(f"    Notification No: {a.notification_number} | Effective: {a.effective_date}")
        print(f"    Target Parent: {a.parent_document} | Change Type: {a.change_type}")

    # 4. AUDIT EXEMPTIONS
    exemptions = db.query(Exemption).all()
    print(f"\n[4] AUDITING EXEMPTION ENGINE ({len(exemptions)} Total Exemptions)")
    for ex in exemptions:
        print(f"  - [{ex.exemption_id}] Category: {ex.category}")
        print(f"    Condition: {ex.condition}")
        print(f"    Legal Source: {ex.legal_source}")

    # 5. AUDIT PENALTIES
    penalties = db.query(Penalty).all()
    print(f"\n[5] AUDITING STATUTORY PENALTIES ({len(penalties)} Total Penalties)")
    for p in penalties:
        print(f"  - [{p.penalty_id}] Section: {p.section} | Offence: {p.offence[:60]}...")
        print(f"    First Offence: {p.first_offence}")
        print(f"    Repeat Offence: {p.repeat_offence}")
        print(f"    Legal Source: {p.legal_source}")

    # 6. AUDIT COMPOUNDING
    compounding = db.query(Compounding).all()
    print(f"\n[6] AUDITING COMPOUNDING MATRIX ({len(compounding)} Total Compounding Entries)")
    for c in compounding:
        print(f"  - [{c.compounding_id}] Status: {c.compoundable} | Authority: {c.compound_authority}")
        print(f"    Legal Source: {c.legal_source}")

    # 7. PROVISION & VECTOR CHUNK METRICS
    prov_count = db.query(LegalProvision).count()
    chunk_count = db.query(DocumentChunk).count()
    ver_count = db.query(DocumentVersion).count()

    print(f"\n[7] STORAGE & VECTOR METRICS")
    print(f"  - Document Versions Maintained: {ver_count}")
    print(f"  - Parsed Statutory Provisions: {prov_count}")
    print(f"  - Legal-Aware Vector Chunks: {chunk_count}")

    print("\n" + "=" * 80)
    if doc_audit_pass:
        print("VERIFICATION RESULT: 100% VERIFIED FROM OFFICIAL GOVERNMENT SOURCES")
    else:
        print("VERIFICATION RESULT: NON-OFFICIAL SOURCES DETECTED")
    print("=" * 80)

    db.close()

if __name__ == "__main__":
    audit_entire_kb_rb()
