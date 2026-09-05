# BACKEND LEGAL DATA INTEGRATION CONTRACT (MEMBER 5 → MEMBER 1)
**Version:** 1.0.0  
**Author:** Member 5 (Database / Legal Knowledge Base Maker)  
**Target:** Member 1 (Backend / Offence / Penalty / Workflow Logic Developer)  

---

### 1. OVERVIEW
This contract defines the integration interface for Member 1 to consume:
1. `penalty_matrix.json` & `penalty_matrix.csv` (Statutory Penalties Engine)
2. `compounding_matrix.json` (Compounding & Prosecution Workflow)
3. `notices/` (Bilingual Markdown Notice Generator)

---

### 2. PENALTY LOOKUP API RESPONSE CONTRACT
```json
{
  "offence_id": "LM-OFF-012",
  "legal_section": "Section 36(1)",
  "legal_rule": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 6",
  "offence_description": "Penalty for manufacturing, packing, importing, distributing or selling non-standard pre-packaged commodities",
  "penalty_details": {
    "first_offence": {
      "fine_max": 25000.0,
      "imprisonment": null,
      "summary": "Fine up to Rs. 25,000"
    },
    "second_offence": {
      "fine_max": 50000.0,
      "imprisonment": null,
      "summary": "Fine up to Rs. 50,000"
    },
    "subsequent_offence": {
      "fine_min": 50000.0,
      "fine_max": 100000.0,
      "imprisonment": "Up to 1 year",
      "summary": "Fine Rs. 50,000 to Rs. 1,00,000 or imprisonment up to 1 year or both"
    }
  },
  "compounding": {
    "compoundable": true,
    "authority": "Controller of Legal Metrology Maharashtra / Assistant Controller",
    "governing_section": "Section 48(1)"
  }
}
```

---

### 3. NOTICE PLACEHOLDER REPLACEMENT ENGINE
Member 1 must load templates from `legal_knowledge_base/notices/` and substitute the following 24 placeholders dynamically:

- `{{NOTICE_ID}}`: Generated unique notice serial number
- `{{CASE_ID}}`: Unique inspection case ID
- `{{BUSINESS_NAME}}`: Name of business entity
- `{{BUSINESS_ADDRESS}}`: Official address of business premises
- `{{INSPECTOR_NAME}}`: Legal Metrology Officer Name
- `{{INSPECTOR_ID}}`: Officer Govt Badge/ID
- `{{INSPECTION_DATE}}`: Date of inspection (YYYY-MM-DD)
- `{{PRODUCT_NAME}}`: Pre-packaged commodity name
- `{{MANUFACTURER_NAME}}`: Manufacturer/Packer/Importer name
- `{{BATCH_NUMBER}}`: Batch/Lot reference number
- `{{MRP}}`: Maximum Retail Price printed
- `{{NET_QUANTITY}}`: Net quantity declared
- `{{OBSERVED_VIOLATION}}`: Specific violation description
- `{{LEGAL_SECTION}}`: Statutory Act Section (e.g. Section 36(1))
- `{{LEGAL_RULE}}`: Statutory Rule (e.g. Rule 6(1))
- `{{PENALTY}}`: Statutory penalty clause
- `{{DEADLINE}}`: Rectification deadline (e.g. 15 days)
- `{{EVIDENCE_REFERENCE}}`: Photo/Seizure tag reference
- `{{WITNESS_1}}`: Panch witness 1 name & address
- `{{WITNESS_2}}`: Panch witness 2 name & address
- `{{SAMPLE_ID}}`: Sample package ID
- `{{COMPOUNDING_AMOUNT}}`: Calculated compounding fee
- `{{OFFICER_AUTHORITY}}`: Officer designation & authority
- `{{DATE}}` & `{{PLACE}}`: Issuance date and location
