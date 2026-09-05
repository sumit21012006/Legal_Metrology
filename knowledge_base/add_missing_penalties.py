import os
import json
import csv

BASE_DIR = r"c:\Users\APURVA\Desktop\Hackathon\legal_metrology_KB_&_RB"
KB_DIR = os.path.join(BASE_DIR, "legal_knowledge_base")

# Load existing files
with open(os.path.join(KB_DIR, "penalty_matrix.json"), "r", encoding="utf-8") as f:
    penalties = json.load(f)

# Add LM-OFF-014 (Section 37 Registration Penalty)
off_014 = {
    "offence_id": "LM-OFF-014",
    "description": "Failure to register as manufacturer, packer, or importer under Rule 27",
    "legal_reference": {
        "act": "Legal Metrology Act, 2009",
        "section": "Section 37",
        "rule": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 27",
        "jurisdiction": "Central / Maharashtra"
    },
    "first_offence": {
        "fine_type": "STATUTORY_MAX",
        "fine_min": 0.0,
        "fine_max": 4000.0,
        "imprisonment": None,
        "description": "Fine which may extend to Rs. 4,000"
    },
    "second_or_subsequent_offence": {
        "fine_type": "STATUTORY_MAX",
        "fine_min": 0.0,
        "fine_max": 10000.0,
        "imprisonment": None,
        "description": "Fine which may extend to Rs. 10,000"
    },
    "compounding": {
        "compoundable": True,
        "authority": "Director of Legal Metrology (Central) / Controller (Maharashtra)",
        "conditions": ["Compoundable under Section 48"]
    },
    "prosecution": {
        "mandatory_court_prosecution_on_subsequent": False,
        "governing_section": "Section 48"
    },
    "notes": ["Verified from Section 37 of LM Act 2009 & Rule 32 of PCR 2011"]
}

# Add LM-OFF-032 (Rule 32 General PCR Penalty)
off_032 = {
    "offence_id": "LM-OFF-032",
    "description": "Fine for contravention of Packaged Commodities Rules where no specific punishment is provided in the Act",
    "legal_reference": {
        "act": "Legal Metrology Act, 2009",
        "section": "Section 52",
        "rule": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 32",
        "jurisdiction": "Central / Maharashtra"
    },
    "first_offence": {
        "fine_type": "STATUTORY_MAX",
        "fine_min": 0.0,
        "fine_max": 5000.0,
        "imprisonment": None,
        "description": "Fine which may extend to Rs. 5,000"
    },
    "second_or_subsequent_offence": {
        "fine_type": "STATUTORY_MAX",
        "fine_min": 0.0,
        "fine_max": 5000.0,
        "imprisonment": None,
        "description": "Fine which may extend to Rs. 5,000"
    },
    "compounding": {
        "compoundable": True,
        "authority": "Controller / Legal Metrology Officer",
        "conditions": ["Compoundable under Rule 32A Table"]
    },
    "prosecution": {
        "mandatory_court_prosecution_on_subsequent": False,
        "governing_section": "Section 48"
    },
    "notes": ["Rule 32 general PCR penalty clause (as amended vide GSR 385(E) 2015)"]
}

if not any(p["offence_id"] == "LM-OFF-014" for p in penalties):
    penalties.append(off_014)

if not any(p["offence_id"] == "LM-OFF-032" for p in penalties):
    penalties.append(off_032)

with open(os.path.join(KB_DIR, "penalty_matrix.json"), "w", encoding="utf-8") as f:
    json.dump(penalties, f, indent=2)

# Update rulebook offences
with open(os.path.join(KB_DIR, "rulebook.json"), "r", encoding="utf-8") as f:
    rb = json.load(f)

rb["offences"] = penalties
rb["penalties"] = penalties

with open(os.path.join(KB_DIR, "rulebook.json"), "w", encoding="utf-8") as f:
    json.dump(rb, f, indent=2)

print("Added LM-OFF-014 and LM-OFF-032 to penalty_matrix.json and rulebook.json.")
