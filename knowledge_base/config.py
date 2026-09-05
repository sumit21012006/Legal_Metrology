import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
DOCUMENTS_DIR = STORAGE_DIR / "documents"
TEXT_DIR = STORAGE_DIR / "raw_text"

DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
TEXT_DIR.mkdir(parents=True, exist_ok=True)

# Database Configuration
# Uses PostgreSQL if available, otherwise SQLite fallback with FAISS/In-Memory vector index
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///" + str(BASE_DIR / "legal_metrology.db"))
POSTGRES_URL = os.environ.get("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/legal_metrology_db")

# Embedding Configuration
EMBEDDING_PROVIDER = os.environ.get("EMBEDDING_PROVIDER", "sentence-transformers")
EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")

# Official Government Domain Whitelist
OFFICIAL_DOMAINS = [
    "indiacode.nic.in",
    "consumeraffairs.nic.in",
    "legalmetrology.maharashtra.gov.in",
    "vaidhmapan.maharashtra.gov.in",
    "egazette.gov.in",
    "egazette.mahaonline.gov.in",
    "maharashtra.gov.in"
]

# Primary official URLs to crawl & discover
PRIMARY_OFFICIAL_URLS = {
    "INDIA_CODE": "https://www.indiacode.nic.in/",
    "CONSUMER_AFFAIRS": "https://consumeraffairs.nic.in/acts-and-rules/legal-metrology",
    "CONSUMER_AFFAIRS_ACTS": "https://consumeraffairs.nic.in/acts-and-rules",
    "MAHARASHTRA_LM": "https://legalmetrology.maharashtra.gov.in/",
    "MAHARASHTRA_VAIDHMAPAN": "https://vaidhmapan.maharashtra.gov.in/",
    "MAHARASHTRA_ACTS_RULES": "https://legalmetrology.maharashtra.gov.in/1035/Acts-Rules",
    "MAHARASHTRA_CIRCULARS": "https://legalmetrology.maharashtra.gov.in/1038/Circulars",
    "MAHARASHTRA_NOTIFICATIONS": "https://legalmetrology.maharashtra.gov.in/1037/Notifications"
}
