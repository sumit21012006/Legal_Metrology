# RULE ENGINE INTEGRATION CONTRACT (MEMBER 5 → MEMBER 2)
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
