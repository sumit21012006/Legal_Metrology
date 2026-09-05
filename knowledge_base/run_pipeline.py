import sys
from pathlib import Path

from config import BASE_DIR
from db.database import init_db, SessionLocal
from db.models import Document
from ingestion.crawler import crawl_and_ingest_documents
from ingestion.pdf_processor import extract_text_from_pdf
from parser.legal_parser import parse_and_store_legal_structure
from parser.amendment_engine import detect_and_store_amendments
from rag.vector_store import create_legal_aware_chunks
from rulebase.structured_rules import seed_structured_rules
from rulebase.exemption_engine import seed_exemptions
from rulebase.enforcement_db import seed_enforcement_databases
from rag.query_engine import process_rag_query
from reporting.generate_reports import generate_coverage_matrix_csv, generate_kb_report_md

def run_full_pipeline():
    print("=" * 70)
    print("LEGAL METROLOGY RULE BASE + KNOWLEDGE BASE INGESTION PIPELINE")
    print("=" * 70)

    # STEP 1: Initialize Database
    print("\n[STEP 1] Initializing relational database & vector tables...")
    init_db()
    db = SessionLocal()

    # STEP 2 & 3: Ingest Documents & Crawl Official Sources
    print("\n[STEP 2 & 3] Ingesting verified Government of India & Maharashtra documents...")
    documents = crawl_and_ingest_documents(db)
    print(f"-> Successfully ingested/verified {len(documents)} official documents.")

    # STEP 4: Legal Structure Parsing, Amendment Detection & Vector Chunking
    print("\n[STEP 4] Parsing legal structures, detecting amendments & generating vector embeddings...")
    for doc in db.query(Document).all():
        print(f"  - Processing: [{doc.jurisdiction}] {doc.title}")
        
        # Read text
        text_path = BASE_DIR / "storage" / "raw_text" / f"{doc.document_id}.txt"
        raw_text = ""
        if text_path.exists():
            with open(text_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

        # Parse structure
        provisions = parse_and_store_legal_structure(db, doc, raw_text)
        print(f"    - Parsed {len(provisions)} hierarchical provisions.")

        # Detect amendments
        if doc.document_type == "AMENDMENT":
            amds = detect_and_store_amendments(db, doc, raw_text)
            print(f"    - Detected {len(amds)} statutory amendment rules.")

        # Vector chunking
        chunks = create_legal_aware_chunks(db, doc)
        print(f"    - Generated {len(chunks)} legal-aware vector chunks.")

    # STEP 5: Seed Machine-Readable Structured Rule Base
    print("\n[STEP 5] Seeding machine-readable Rule Base...")
    seed_structured_rules(db)
    print("-> Structured rules seeded.")

    # STEP 6: Seed Exemption Engine
    print("\n[STEP 6] Seeding statutory Exemption Engine...")
    seed_exemptions(db)
    print("-> Exemption engine seeded.")

    # STEP 7: Seed Enforcement, Penalty & Compounding Databases
    print("\n[STEP 7] Seeding Penalties, Compounding, Inspections, Seizures & Workflows...")
    seed_enforcement_databases(db)
    print("-> Enforcement databases seeded.")

    # STEP 8: Generate Reports & Matrix CSV
    print("\n[STEP 8] Generating coverage matrix CSV and Knowledge Base report...")
    csv_path = BASE_DIR / "LEGAL_METROLOGY_COVERAGE_MATRIX.csv"
    report_path = BASE_DIR / "LEGAL_METROLOGY_KB_REPORT.md"
    
    generate_coverage_matrix_csv(db, csv_path)
    generate_kb_report_md(db, report_path)
    
    print(f"-> Saved Coverage Matrix: {csv_path}")
    print(f"-> Saved KB Audit Report: {report_path}")

    # STEP 9: Run Verification RAG Queries
    print("\n[STEP 9] Running Legal Retrieval & Citation Verification Queries...")
    test_queries = [
        "What declarations are mandatory on a packaged cosmetic sold in Maharashtra?",
        "What exemptions apply to small packages containing 10g or less?",
        "What penalty applies for selling packaged commodities without MRP declaration?"
    ]

    for q in test_queries:
        print(f"\n--- QUERY: {q} ---")
        res = process_rag_query(db, q, jurisdiction="MAHARASHTRA")
        print(res["answer"][:400] + "\n...")

    db.close()
    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_full_pipeline()
