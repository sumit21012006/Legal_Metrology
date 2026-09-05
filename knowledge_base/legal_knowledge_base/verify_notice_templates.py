import os

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
        
    print("\n================================================================================")
    print("VERIFICATION RESULT: ALL 8 NOTICE TEMPLATES FULLY VALIDATED")
    print("================================================================================")

if __name__ == "__main__":
    verify_notices()
