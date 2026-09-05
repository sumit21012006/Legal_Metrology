import json
import math
import numpy as np
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL_NAME
from db.models import Document, LegalProvision, DocumentChunk

# Initialize embedding model lazily
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        try:
            _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        except Exception as e:
            print(f"Warning: Loading default embedding model {EMBEDDING_MODEL_NAME}: {e}")
            _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def generate_embeddings_for_text(text: str) -> list[float]:
    model = get_embedding_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()

def create_legal_aware_chunks(db: Session, document: Document):
    """
    Chunks documents STRICTLY by legal provision boundaries (Section, Rule, Sub-rule, Clause, Schedule).
    Preserves full legal metadata for every chunk.
    """
    provisions = db.query(LegalProvision).filter(LegalProvision.document_id == document.document_id).all()
    created_chunks = []
    
    chunk_counter = 1
    for prov in provisions:
        chunk_text = f"Document: {document.title}\n"
        if prov.rule:
            chunk_text += f"Rule: {prov.rule} "
        if prov.section:
            chunk_text += f"Section: {prov.section} "
        if prov.sub_rule:
            chunk_text += f"Sub-rule: {prov.sub_rule} "
        if prov.clause:
            chunk_text += f"Clause: {prov.clause} "
        if prov.schedule:
            chunk_text += f"Schedule: {prov.schedule} "
        chunk_text += f"\nJurisdiction: {document.jurisdiction}\nText:\n{prov.text}"

        embedding = generate_embeddings_for_text(chunk_text)
        
        meta = {
            "title": document.title,
            "document_type": document.document_type,
            "jurisdiction": document.jurisdiction,
            "authority": document.authority,
            "status": document.status,
            "effective_date": prov.effective_date or document.effective_date,
            "source_url": document.source_url,
            "page": prov.page
        }

        chunk_id = f"CHK_{document.document_id}_{chunk_counter}"
        chunk_obj = DocumentChunk(
            chunk_id=chunk_id,
            document_id=document.document_id,
            provision_id=prov.provision_id,
            section=prov.section,
            rule=prov.rule,
            sub_rule=prov.sub_rule,
            clause=prov.clause,
            schedule=prov.schedule,
            page=prov.page,
            chunk_text=chunk_text,
            metadata_json=meta,
            embedding=json.dumps(embedding)
        )
        db.merge(chunk_obj)
        created_chunks.append(chunk_obj)
        chunk_counter += 1

    db.commit()
    return created_chunks

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    a = np.array(vec_a)
    b = np.array(vec_b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))

def hybrid_search(
    db: Session,
    query: str,
    jurisdiction: str = "ALL",
    top_k: int = 5
) -> list[dict]:
    """
    Executes hybrid retrieval (Vector Similarity + Keyword Matching + Metadata Filtering).
    """
    query_emb = generate_embeddings_for_text(query)
    query_words = set(query.lower().split())

    chunks = db.query(DocumentChunk).all()
    results = []

    for chunk in chunks:
        meta = chunk.metadata_json or {}
        
        # Jurisdiction Filter
        if jurisdiction != "ALL" and meta.get("jurisdiction") != jurisdiction and meta.get("jurisdiction") != "CENTRAL":
            continue

        # Vector Score
        vec_score = 0.0
        if chunk.embedding:
            try:
                emb_list = json.loads(chunk.embedding)
                vec_score = cosine_similarity(query_emb, emb_list)
            except Exception:
                pass

        # Keyword BM25-like Score
        text_words = set(chunk.chunk_text.lower().split())
        match_count = len(query_words.intersection(text_words))
        keyword_score = match_count / (len(query_words) + 1e-5)

        # Combined Hybrid Score
        hybrid_score = (0.7 * vec_score) + (0.3 * keyword_score)

        results.append({
            "chunk_id": chunk.chunk_id,
            "document_id": chunk.document_id,
            "rule": chunk.rule,
            "section": chunk.section,
            "sub_rule": chunk.sub_rule,
            "clause": chunk.clause,
            "page": chunk.page,
            "chunk_text": chunk.chunk_text,
            "metadata": meta,
            "score": hybrid_score
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
