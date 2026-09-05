from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path
from pydantic import BaseModel

from config import BASE_DIR
from db.database import init_db, get_db
from db.models import (
    Document, Amendment, RuleBase, Exemption, Penalty, 
    Compounding, Inspection, Seizure, Notice, FailedDocument, AuditLog
)
from ingestion.crawler import crawl_and_ingest_documents
from rag.query_engine import process_rag_query
from versioning.rule_resolver import resolve_current_rule

app = FastAPI(
    title="Legal Metrology Knowledge Base & Rule Base API",
    version="1.0.0",
    description="Official Government of India & Maharashtra Legal Metrology Regulatory Knowledge API"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB tables on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Models for request body
class RAGQueryRequest(BaseModel):
    query: str
    jurisdiction: Optional[str] = "MAHARASHTRA"
    date: Optional[str] = None
    top_k: Optional[int] = 5

@app.post("/api/rag/query")
def rag_query(req: RAGQueryRequest, db: Session = Depends(get_db)):
    """
    Executes hybrid RAG query returning 10-step cited answer, applicable provisions, 
    exemption checks, and source metadata.
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")
    return process_rag_query(
        db=db,
        query=req.query,
        jurisdiction=req.jurisdiction or "MAHARASHTRA",
        target_date=req.date,
        top_k=req.top_k or 5
    )

@app.get("/api/documents")
def list_documents(jurisdiction: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Document)
    if jurisdiction:
        query = query.filter(Document.jurisdiction == jurisdiction)
    docs = query.all()
    return [
        {
            "document_id": d.document_id,
            "title": d.title,
            "document_type": d.document_type,
            "authority": d.authority,
            "department": d.department,
            "jurisdiction": d.jurisdiction,
            "state": d.state,
            "publication_date": d.publication_date,
            "effective_date": d.effective_date,
            "notification_number": d.notification_number,
            "status": d.status,
            "source_url": d.source_url,
            "sha256": d.sha256
        }
        for d in docs
    ]

@app.get("/api/rules")
def list_rules(db: Session = Depends(get_db)):
    rules = db.query(RuleBase).all()
    return [
        {
            "rule_id": r.rule_id,
            "jurisdiction": r.jurisdiction,
            "legal_source": r.legal_source,
            "section": r.section,
            "rule": r.rule,
            "sub_rule": r.sub_rule,
            "clause": r.clause,
            "effective_from": r.effective_from,
            "applicability": r.applicability,
            "requirements": r.requirements,
            "exemptions": r.exemptions,
            "penalty": r.penalty,
            "authority": r.authority,
            "source_reference": r.source_reference
        }
        for r in rules
    ]

@app.get("/api/amendments")
def list_amendments(db: Session = Depends(get_db)):
    amds = db.query(Amendment).all()
    return [
        {
            "amendment_id": a.amendment_id,
            "parent_document": a.parent_document,
            "amending_document": a.amending_document,
            "affected_rule": a.affected_rule,
            "change_type": a.change_type,
            "effective_date": a.effective_date,
            "notification_number": a.notification_number,
            "source_url": a.source_url
        }
        for a in amds
    ]

@app.get("/api/rule/resolve")
def resolve_rule_endpoint(rule_id: str, date: Optional[str] = None, db: Session = Depends(get_db)):
    return resolve_current_rule(db, rule_id, target_date=date)

@app.get("/api/exemptions")
def list_exemptions(db: Session = Depends(get_db)):
    return db.query(Exemption).all()

@app.get("/api/penalties")
def list_penalties(db: Session = Depends(get_db)):
    return db.query(Penalty).all()

@app.get("/api/compounding")
def list_compounding(db: Session = Depends(get_db)):
    return db.query(Compounding).all()

@app.get("/api/forms")
def list_forms(db: Session = Depends(get_db)):
    from db.models import OfficialForm
    return db.query(OfficialForm).all()

@app.get("/api/failed_documents")
def list_failed_documents(db: Session = Depends(get_db)):
    return db.query(FailedDocument).all()

@app.post("/api/ingest/sync")
def trigger_sync(db: Session = Depends(get_db)):
    ingested = crawl_and_ingest_documents(db)
    return {"status": "SUCCESS", "ingested_count": len(ingested)}

@app.get("/api/audit_logs")
def list_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()

# Mount Dashboard UI Static Directory
dashboard_static_dir = BASE_DIR / "dashboard" / "static"
dashboard_static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/dashboard", StaticFiles(directory=str(dashboard_static_dir), html=True), name="dashboard")
