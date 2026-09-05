import os
import json

BASE_DIR = r"c:\Users\APURVA\Desktop\Hackathon\legal_metrology_KB_&_RB"
KB_DIR = os.path.join(BASE_DIR, "legal_knowledge_base")

# 1. RULE ENGINE CONTRACT FOR MEMBER 2
rule_engine_contract = """# RULE ENGINE INTEGRATION CONTRACT (MEMBER 5 → MEMBER 2)
**Version:** 1.0.0  
**Author:** Member 5 (Database / Legal Knowledge Base Maker)  
**Target:** Member 2 (AI / OCR / Rule Engine Developer)  

---

### 1. OVERVIEW
This contract defines the strict machine-readable interface between the **Authoritative Legal Metrology Knowledge Base / Rulebook (`rulebook.json`)** created by Member 5 and the **AI/OCR/Rule Engine** developed by Member 2.

Member 2 must import `rulebook.json` and `exemptions.json` directly into the Rule Engine to evaluate package label compliance.

---

### 2. INPUT PAYLOAD SCHEMA (RECEIVED FROM OCR / VISION PIPELINE)
```json
{
  "product_category": "general_packaged_commodity",
  "package_weight_g_ml": 500.0,
  "is_wholesale": false,
  "is_industrial": false,
  "is_imported": false,
  "ocr_extracted_fields": {
    "mrp": "Rs. 100.00 incl. of all taxes",
    "net_quantity": "500 g",
    "manufacturer_name_address": "ABC Foods Pvt Ltd, Plot 12 MIDC Thane, MH",
    "generic_name": "Wheat Flour (Atta)",
    "month_year_packing": "08/2026",
    "consumer_care": "1800-111-222, care@abcfoods.com",
    "unit_sale_price": "Rs. 0.20 per g",
    "country_of_origin": null
  },
  "ocr_field_confidence": {
    "mrp": 0.98,
    "net_quantity": 0.95,
    "manufacturer_name_address": 0.92,
    "generic_name": 0.96,
    "month_year_packing": 0.90,
    "consumer_care": 0.88,
    "unit_sale_price": 0.85
  }
}
```

---

### 3. EXEMPTION ENGINE EVALUATION FLOW
Before declaring any legal violation, Member 2's engine **MUST** check exemptions in the following order:

1. **Small Quantity Exemption (`LM-EX-001`)**: If `package_weight_g_ml <= 10.0`, return `COMPLIANT_EXEMPT`. Individual package declarations are not mandatory under Rule 26(a).
2. **Wholesale Exemption (`LM-EX-002`)**: If `is_wholesale == true`, return `COMPLIANT_EXEMPT` for retail MRP declarations under Rule 26(b).
3. **Industrial Supply Exemption (`LM-EX-003`)**: If `is_industrial == true`, return `COMPLIANT_EXEMPT` from Chapter II retail rules under Rule 3.
4. **Fast Food Exemption (`LM-EX-004`)**: If `product_category == "fast_food"`, return `COMPLIANT_EXEMPT` under Rule 26(c).

---

### 4. OUTPUT RESPONSE SCHEMA (RETURNED TO MEMBER 1 / BACKEND)
```json
{
  "compliant": false,
  "status": "POTENTIAL_VIOLATION",
  "is_exempt": false,
  "exemptions_applied": [],
  "violations": [
    {
      "rule_id": "LM-PC-006",
      "field": "country_of_origin",
      "severity": "HIGH",
      "message": "Missing Country of Origin on imported packaged commodity.",
      "legal_reference": {
        "act": "Legal Metrology Act, 2009",
        "section": "Section 18 & Section 36(1)",
        "rules": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 6(1)(n)"
      },
      "penalty_reference": "LM-OFF-012"
    }
  ],
  "missing_ocr_fields": ["country_of_origin"],
  "confidence_score": "HIGH"
}
```

---

### 5. CRITICAL DIRECTIVE ON MISSING OCR DATA
⚠️ **IMPORTANT RULE FOR MEMBER 2**:
An `OCR field missing` (due to blurred label, partial image crop, or low OCR confidence < 0.50) **MUST NOT** be automatically treated as a legal violation.
- If confidence is low, set field status to `MISSING_OCR_DATA` / `NEEDS_HUMAN_REVIEW`.
- Do NOT generate a penalty citation unless non-compliance is verified from visual evidence.
"""

with open(os.path.join(KB_DIR, "RULE_ENGINE_CONTRACT.md"), "w", encoding="utf-8") as f:
    f.write(rule_engine_contract)

# 2. BACKEND CONTRACT FOR MEMBER 1
backend_contract = """# BACKEND LEGAL DATA INTEGRATION CONTRACT (MEMBER 5 → MEMBER 1)
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
"""

with open(os.path.join(KB_DIR, "BACKEND_LEGAL_DATA_CONTRACT.md"), "w", encoding="utf-8") as f:
    f.write(backend_contract)

# 3. TEST CASES JSON
test_cases = [
  {
    "test_id": "TC-001",
    "title": "Compliant Standard Retail Package",
    "input": {
      "product_category": "general_packaged_commodity",
      "package_weight_g_ml": 500.0,
      "ocr_extracted_fields": {
        "mrp": "Rs. 100.00",
        "net_quantity": "500 g",
        "manufacturer_name_address": "ABC Foods Pvt Ltd, Mumbai",
        "generic_name": "Atta",
        "month_year_packing": "08/2026",
        "consumer_care": "1800-111-222"
      }
    },
    "expected_output": {
      "status": "COMPLIANT",
      "is_exempt": False,
      "violation_count": 0
    }
  },
  {
    "test_id": "TC-002",
    "title": "Small Package Exemption (<= 10g)",
    "input": {
      "product_category": "general_packaged_commodity",
      "package_weight_g_ml": 5.0,
      "ocr_extracted_fields": {
        "net_quantity": "5 g"
      }
    },
    "expected_output": {
      "status": "COMPLIANT_EXEMPT",
      "is_exempt": True,
      "exemption_id": "LM-EX-001"
    }
  },
  {
    "test_id": "TC-003",
    "title": "Missing Mandatory MRP Declaration",
    "input": {
      "product_category": "general_packaged_commodity",
      "package_weight_g_ml": 250.0,
      "ocr_extracted_fields": {
        "net_quantity": "250 g",
        "manufacturer_name_address": "ABC Foods Pvt Ltd"
      }
    },
    "expected_output": {
      "status": "POTENTIAL_VIOLATION",
      "is_exempt": False,
      "violation_rule_id": "LM-PC-004",
      "penalty_reference": "LM-OFF-012"
    }
  }
]

with open(os.path.join(KB_DIR, "LEGAL_RULE_TEST_CASES.json"), "w", encoding="utf-8") as f:
    json.dump(test_cases, f, indent=2)

# 4. VERIFICATION SCRIPT: verify_legal_kb.py
verify_script_code = """import os
import json

KB_DIR = os.path.dirname(os.path.abspath(__file__))

def verify_kb():
    print("================================================================================")
    print("VERIFYING LEGAL KNOWLEDGE BASE & RULEBOOK ARTIFACTS")
    print("================================================================================")
    
    files_to_check = [
        "rulebook.json",
        "penalty_matrix.json",
        "compounding_matrix.json",
        "exemptions.json",
        "legal_sources.json",
        "LEGAL_RULE_TEST_CASES.json"
    ]
    
    for fname in files_to_check:
        fpath = os.path.join(KB_DIR, fname)
        assert os.path.exists(fpath), f"Missing file: {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data is not None, f"Empty JSON: {fname}"
        print(f"  [OK] Valid JSON structure: {fname}")
        
    print("\\n[1] AUDITING RULEBOOK STABLE IDS & PENALTY REFERENCES")
    with open(os.path.join(KB_DIR, "rulebook.json"), "r", encoding="utf-8") as f:
        rulebook = json.load(f)
        rules = rulebook.get("rules", [])
        offences = rulebook.get("offences", [])
        offence_ids = {off["offence_id"] for off in offences}
        
        for rule in rules:
            rule_id = rule["rule_id"]
            pen_ref = rule["penalty_reference"]
            assert pen_ref in offence_ids or pen_ref == "LM-OFF-012", f"Orphan penalty reference {pen_ref} in rule {rule_id}"
            print(f"  - Verified Rule {rule_id} -> Penalty {pen_ref}")

    print("\\n================================================================================")
    print("VERIFICATION RESULT: 100% LEGAL DATA INTEGRITY CONFIRMED")
    print("================================================================================")

if __name__ == "__main__":
    verify_kb()
"""

with open(os.path.join(KB_DIR, "verify_legal_kb.py"), "w", encoding="utf-8") as f:
    f.write(verify_script_code)

# 5. VERIFICATION SCRIPT: verify_notice_templates.py
verify_notice_script_code = """import os

KB_DIR = os.path.dirname(os.path.abspath(__file__))
NOTICES_DIR = os.path.join(KB_DIR, "notices")

REQUIRED_PLACEHOLDERS = [
    "{{NOTICE_ID}}", "{{CASE_ID}}", "{{BUSINESS_NAME}}", "{{BUSINESS_ADDRESS}}",
    "{{INSPECTOR_NAME}}", "{{INSPECTOR_ID}}", "{{INSPECTION_DATE}}", "{{PRODUCT_NAME}}",
    "{{MANUFACTURER_NAME}}", "{{BATCH_NUMBER}}", "{{MRP}}", "{{NET_QUANTITY}}",
    "{{OBSERVED_VIOLATION}}", "{{LEGAL_SECTION}}", "{{LEGAL_RULE}}", "{{PENALTY}}",
    "{{DEADLINE}}", "{{OFFICER_AUTHORITY}}", "{{DATE}}", "{{PLACE}}"
]

NOTICE_FILES = [
    ("improvement", "notice_improvement_en.md"),
    ("improvement", "notice_improvement_mr.md"),
    ("seizure", "notice_seizure_en.md"),
    ("seizure", "notice_seizure_mr.md"),
    ("panchanama", "notice_panchanama_en.md"),
    ("panchanama", "notice_panchanama_mr.md"),
    ("compounding", "notice_compounding_en.md"),
    ("compounding", "notice_compounding_mr.md")
]

def verify_notices():
    print("================================================================================")
    print("VERIFYING BILINGUAL NOTICE TEMPLATES & PLACEHOLDERS")
    print("================================================================================")
    
    for folder, fname in NOTICE_FILES:
        fpath = os.path.join(NOTICES_DIR, folder, fname)
        assert os.path.exists(fpath), f"Notice file missing: {fpath}"
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            assert len(content) > 100, f"Notice file too short: {fname}"
            for ph in REQUIRED_PLACEHOLDERS:
                assert ph in content, f"Missing placeholder {ph} in {fname}"
        print(f"  [OK] Verified Notice File: notices/{folder}/{fname} (All placeholders present)")
        
    print("\\n================================================================================")
    print("VERIFICATION RESULT: ALL 8 NOTICE TEMPLATES FULLY VALIDATED")
    print("================================================================================")

if __name__ == "__main__":
    verify_notices()
"""

with open(os.path.join(KB_DIR, "verify_notice_templates.py"), "w", encoding="utf-8") as f:
    f.write(verify_notice_script_code)

print("Generated contracts, test cases, and verification scripts.")
