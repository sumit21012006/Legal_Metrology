import json
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    
    document_id = Column(String(100), primary_key=True)
    title = Column(Text, nullable=False)
    document_type = Column(String(50), nullable=False) # ACT, RULE, AMENDMENT, NOTIFICATION, CIRCULAR, FAQ, GUIDELINE, PROCEDURE, FORM
    authority = Column(String(100), nullable=False)    # Central Government, Maharashtra Government
    department = Column(String(100), default="Legal Metrology")
    jurisdiction = Column(String(50), nullable=False)  # CENTRAL, MAHARASHTRA
    state = Column(String(50), default="INDIA")         # INDIA, MAHARASHTRA
    publication_date = Column(String(20), nullable=True)
    effective_date = Column(String(20), nullable=True)
    notification_number = Column(String(100), nullable=True)
    gazette_number = Column(String(100), nullable=True)
    status = Column(String(30), nullable=False)          # CURRENT, AMENDMENT, SUPERSEDED, REPEALED, DRAFT, PROPOSED, GUIDANCE, FAQ, CIRCULAR, NOTIFICATION, UNKNOWN
    source_url = Column(Text, nullable=False)
    source_domain = Column(String(100), nullable=False)
    sha256 = Column(String(64), nullable=False)
    storage_path = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")
    provisions = relationship("LegalProvision", back_populates="document", cascade="all, delete-orphan")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentVersion(Base):
    __tablename__ = 'document_versions'
    
    version_id = Column(String(100), primary_key=True)
    document_id = Column(String(100), ForeignKey('documents.document_id'), nullable=False)
    version_number = Column(Integer, default=1)
    publication_date = Column(String(20), nullable=True)
    effective_date = Column(String(20), nullable=True)
    raw_text = Column(Text, nullable=True)
    sha256 = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="versions")


class Amendment(Base):
    __tablename__ = 'amendments'
    
    amendment_id = Column(String(100), primary_key=True)
    parent_document = Column(String(100), nullable=False)
    amending_document = Column(String(100), nullable=False)
    affected_rule = Column(String(100), nullable=True)
    affected_section = Column(String(100), nullable=True)
    old_text = Column(Text, nullable=True)
    new_text = Column(Text, nullable=True)
    change_type = Column(String(50), nullable=False) # SUBSTITUTION, INSERTION, OMISSION, AMENDMENT
    effective_date = Column(String(20), nullable=True)
    notification_number = Column(String(100), nullable=True)
    source_url = Column(Text, nullable=True)


class LegalProvision(Base):
    __tablename__ = 'legal_provisions'
    
    provision_id = Column(String(100), primary_key=True)
    document_id = Column(String(100), ForeignKey('documents.document_id'), nullable=False)
    chapter = Column(String(100), nullable=True)
    section = Column(String(100), nullable=True)
    rule = Column(String(100), nullable=True)
    sub_rule = Column(String(100), nullable=True)
    clause = Column(String(100), nullable=True)
    schedule = Column(String(100), nullable=True)
    text = Column(Text, nullable=False)
    page = Column(Integer, default=1)
    effective_date = Column(String(20), nullable=True)
    status = Column(String(30), default="CURRENT")

    document = relationship("Document", back_populates="provisions")


class DocumentChunk(Base):
    __tablename__ = 'document_chunks'
    
    chunk_id = Column(String(100), primary_key=True)
    document_id = Column(String(100), ForeignKey('documents.document_id'), nullable=False)
    provision_id = Column(String(100), nullable=True)
    section = Column(String(100), nullable=True)
    rule = Column(String(100), nullable=True)
    sub_rule = Column(String(100), nullable=True)
    clause = Column(String(100), nullable=True)
    schedule = Column(String(100), nullable=True)
    page = Column(Integer, default=1)
    chunk_text = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    embedding = Column(Text, nullable=True)

    document = relationship("Document", back_populates="chunks")


class RuleBase(Base):
    __tablename__ = 'rules'
    
    rule_id = Column(String(100), primary_key=True)
    jurisdiction = Column(String(50), nullable=False) # CENTRAL, MAHARASHTRA
    legal_source = Column(String(200), nullable=False)
    section = Column(String(100), nullable=True)
    rule = Column(String(100), nullable=True)
    sub_rule = Column(String(100), nullable=True)
    clause = Column(String(100), nullable=True)
    effective_from = Column(String(20), nullable=True)
    effective_to = Column(String(20), nullable=True)
    applicability = Column(JSON, default=list)
    conditions = Column(JSON, default=list)
    requirements = Column(JSON, default=list)
    exceptions = Column(JSON, default=list)
    exemptions = Column(JSON, default=list)
    violation = Column(JSON, default=list)
    evidence_required = Column(JSON, default=list)
    penalty = Column(JSON, default=list)
    compounding = Column(JSON, default=list)
    authority = Column(JSON, default=list)
    source_reference = Column(Text, nullable=True)


class Exemption(Base):
    __tablename__ = 'exemptions'
    
    exemption_id = Column(String(100), primary_key=True)
    category = Column(String(100), nullable=False)
    rule_id = Column(String(100), nullable=True)
    condition = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    authority = Column(String(100), nullable=False)
    legal_source = Column(Text, nullable=False)


class Penalty(Base):
    __tablename__ = 'penalties'
    
    penalty_id = Column(String(100), primary_key=True)
    offence = Column(Text, nullable=False)
    section = Column(String(100), nullable=True)
    rule = Column(String(100), nullable=True)
    first_offence = Column(Text, nullable=False)
    repeat_offence = Column(Text, nullable=True)
    fine_min = Column(Float, default=0.0)
    fine_max = Column(Float, default=0.0)
    imprisonment = Column(Text, nullable=True)
    compounding_authority = Column(String(100), nullable=True)
    legal_source = Column(Text, nullable=False)
    effective_date = Column(String(20), nullable=True)


class Compounding(Base):
    __tablename__ = 'compounding'
    
    compounding_id = Column(String(100), primary_key=True)
    offence = Column(Text, nullable=False)
    compoundable = Column(String(30), nullable=False) # COMPOUNDABLE, NON_COMPOUNDABLE, LEGAL_REVIEW_REQUIRED
    compound_authority = Column(String(100), nullable=False)
    conditions = Column(Text, nullable=True)
    amount = Column(Text, nullable=True)
    procedure = Column(Text, nullable=True)
    legal_source = Column(Text, nullable=False)
    effective_date = Column(String(20), nullable=True)


class Inspection(Base):
    __tablename__ = 'inspections'
    
    inspection_id = Column(String(100), primary_key=True)
    inspection_type = Column(String(100), nullable=False)
    authority = Column(String(100), nullable=False)
    business_type = Column(String(100), nullable=False)
    documents_to_check = Column(JSON, default=list)
    physical_checks = Column(JSON, default=list)
    package_checks = Column(JSON, default=list)
    measurement_checks = Column(JSON, default=list)
    evidence_required = Column(JSON, default=list)
    follow_up_action = Column(Text, nullable=True)
    legal_basis = Column(Text, nullable=False)


class Complaint(Base):
    __tablename__ = 'complaints'
    
    complaint_id = Column(String(100), primary_key=True)
    complaint_type = Column(String(100), nullable=False)
    commodity = Column(String(100), nullable=False)
    alleged_violation = Column(Text, nullable=False)
    jurisdiction = Column(String(50), nullable=False)
    applicable_rule = Column(Text, nullable=False)
    required_evidence = Column(JSON, default=list)
    authority = Column(String(100), nullable=False)
    procedure = Column(Text, nullable=False)
    source = Column(Text, nullable=False)


class Seizure(Base):
    __tablename__ = 'seizures'
    
    seizure_id = Column(String(100), primary_key=True)
    circumstances = Column(Text, nullable=False)
    legal_authority = Column(String(100), nullable=False)
    officer = Column(String(100), nullable=False)
    required_document = Column(JSON, default=list)
    evidence = Column(JSON, default=list)
    inventory = Column(Text, nullable=True)
    custody = Column(Text, nullable=True)
    release_disposal = Column(Text, nullable=True)
    legal_source = Column(Text, nullable=False)


class Notice(Base):
    __tablename__ = 'notices'
    
    notice_id = Column(String(100), primary_key=True)
    notice_type = Column(String(100), nullable=False)
    trigger = Column(Text, nullable=False)
    authority = Column(String(100), nullable=False)
    recipient = Column(String(100), nullable=False)
    required_contents = Column(JSON, default=list)
    response_period = Column(String(50), nullable=False)
    legal_basis = Column(Text, nullable=False)
    next_action = Column(Text, nullable=True)
    official_template = Column(Boolean, default=False)


class OfficialForm(Base):
    __tablename__ = 'official_forms'
    
    form_id = Column(String(100), primary_key=True)
    form_name = Column(String(200), nullable=False)
    rule_reference = Column(String(100), nullable=False)
    purpose = Column(String(100), nullable=False) # registration, licence, seizure, compounding, verification, notice
    jurisdiction = Column(String(50), nullable=False)
    is_publicly_available = Column(Boolean, default=True)
    status = Column(String(50), default="CURRENT") # CURRENT, OFFICIAL_FORM_NOT_FOUND
    source_url = Column(Text, nullable=True)


class OfficerWorkflow(Base):
    __tablename__ = 'officer_workflows'
    
    workflow_id = Column(String(100), primary_key=True)
    department = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    action = Column(Text, nullable=False)
    jurisdiction = Column(String(50), nullable=False)
    delegation = Column(Text, nullable=True)
    legal_basis = Column(Text, nullable=False)


class FailedDocument(Base):
    __tablename__ = 'failed_documents'
    
    failed_id = Column(String(100), primary_key=True)
    source_url = Column(Text, nullable=False)
    document_title = Column(Text, nullable=True)
    stage = Column(String(50), nullable=False)
    error_message = Column(Text, nullable=False)
    retry_count = Column(Integer, default=0)
    last_attempt = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    log_id = Column(String(100), primary_key=True)
    query_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    jurisdiction = Column(String(50), nullable=False)
    date_queried = Column(String(20), nullable=True)
    retrieved_documents = Column(JSON, default=list)
    retrieved_chunks = Column(JSON, default=list)
    rules_evaluated = Column(JSON, default=list)
    final_answer = Column(Text, nullable=False)
    citations = Column(JSON, default=list)
    confidence = Column(String(30), default="HIGH")
