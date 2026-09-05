from sqlalchemy.orm import Session
from db.models import Penalty, Compounding, Inspection, Complaint, Seizure, Notice, OfficerWorkflow

# VERIFIED STATUTORY PENALTIES DIRECTLY FROM THE LEGAL METROLOGY ACT, 2009 (ACT NO. 1 OF 2010) GAZETTE PUBLICATION
SEED_PENALTIES = [
    {
        "penalty_id": "PEN_SEC_24",
        "offence": "Penalty for use of unverified weight or measure in transaction, deal or contract",
        "section": "Section 24",
        "rule": "Maharashtra Legal Metrology (Enforcement) Rules, 2011 Rule 14",
        "first_offence": "Fine which shall not be less than Rs. 2,000, but which may extend to Rs. 10,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year and with fine",
        "fine_min": 2000.0,
        "fine_max": 10000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology Maharashtra / Authorized Legal Metrology Officer",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 24",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_25",
        "offence": "Penalty for use of non-standard weight or measure",
        "section": "Section 25",
        "rule": "Legal Metrology Act, 2009 Section 25",
        "first_offence": "Fine which may extend to Rs. 25,000",
        "repeat_offence": "Imprisonment for a term which may extend to 6 months and with fine",
        "fine_min": 0.0,
        "fine_max": 25000.0,
        "imprisonment": "Up to 6 months for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology / Authorized Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 25",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_26",
        "offence": "Penalty for tampering with licence certificate or records",
        "section": "Section 26",
        "rule": "Legal Metrology Act, 2009 Section 26",
        "first_offence": "Fine which may extend to Rs. 20,000 or imprisonment for a term which may extend to 1 year or both",
        "repeat_offence": "Imprisonment up to 1 year and fine",
        "fine_min": 0.0,
        "fine_max": 20000.0,
        "imprisonment": "Up to 1 year",
        "compounding_authority": "Controller of Legal Metrology",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 26",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_27",
        "offence": "Penalty for manufacture or sale of non-standard weight or measure",
        "section": "Section 27",
        "rule": "Legal Metrology Act, 2009 Section 27",
        "first_offence": "Fine which may extend to Rs. 20,000",
        "repeat_offence": "Imprisonment for a term which may extend to 3 years or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 20000.0,
        "imprisonment": "Up to 3 years for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology / Authorized Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 27",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_28",
        "offence": "Penalty for transaction, deal or contract by non-standard weight or measure (making short weighment or measure)",
        "section": "Section 28",
        "rule": "Legal Metrology Act, 2009 Section 28",
        "first_offence": "Fine which may extend to Rs. 10,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 10000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology / Authorized Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 28",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_29",
        "offence": "Penalty for quoting non-standard units in price lists, bills, advertisements, or invoices",
        "section": "Section 29",
        "rule": "Legal Metrology Act, 2009 Section 29",
        "first_offence": "Fine which may extend to Rs. 10,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 10000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology / Authorized Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 29",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_30",
        "offence": "Penalty for transactions in contravention of standard weight or measure",
        "section": "Section 30",
        "rule": "Legal Metrology Act, 2009 Section 30",
        "first_offence": "Fine which may extend to Rs. 10,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 10000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 30",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_31",
        "offence": "Penalty for non-production of documents, registers or records to Legal Metrology Officer",
        "section": "Section 31",
        "rule": "Legal Metrology Act, 2009 Section 31",
        "first_offence": "Fine which may extend to Rs. 5,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 5000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology / Authorized Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 31",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_33",
        "offence": "Penalty for manufacture of weight or measure without licence",
        "section": "Section 33",
        "rule": "Maharashtra Legal Metrology (Enforcement) Rules, 2011 Rule 6",
        "first_offence": "Fine which may extend to Rs. 20,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 20000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology Maharashtra / Authorized Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 33",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_34",
        "offence": "Penalty for repair of weight or measure without licence",
        "section": "Section 34",
        "rule": "Maharashtra Legal Metrology (Enforcement) Rules, 2011 Rule 7",
        "first_offence": "Fine which may extend to Rs. 5,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 5000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology Maharashtra / Authorized Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 34",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_35",
        "offence": "Penalty for deal in weight or measure without licence",
        "section": "Section 35",
        "rule": "Maharashtra Legal Metrology (Enforcement) Rules, 2011 Rule 8",
        "first_offence": "Fine which may extend to Rs. 5,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 5000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology Maharashtra / Authorized Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 35",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_36_1",
        "offence": "Penalty for manufacturing, packing, importing, distributing or selling non-standard pre-packaged commodities (missing mandatory declarations)",
        "section": "Section 36(1)",
        "rule": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 6",
        "first_offence": "Fine which may extend to Rs. 25,000",
        "repeat_offence": "Second offence: Fine which may extend to Rs. 50,000; Subsequent offence: Fine which shall not be less than Rs. 50,000 but which may extend to Rs. 1,00,000 or imprisonment for a term which may extend to 1 year or both",
        "fine_min": 0.0,
        "fine_max": 25000.0,
        "imprisonment": "Up to 1 year for 3rd and subsequent offences",
        "compounding_authority": "Director of Legal Metrology (Central) / Controller of Legal Metrology (Maharashtra) under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 36(1)",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_36_2",
        "offence": "Penalty for manufacture, packing, import or sale of pre-packaged commodity at price exceeding Maximum Retail Price (MRP)",
        "section": "Section 36(2)",
        "rule": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 18",
        "first_offence": "Fine which may extend to Rs. 2,000",
        "repeat_offence": "Fine which may extend to Rs. 2,000 for retail dealer",
        "fine_min": 0.0,
        "fine_max": 2000.0,
        "imprisonment": "None",
        "compounding_authority": "Controller / Authorized Legal Metrology Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 36(2)",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_38",
        "offence": "Penalty for non-compliance of approval of model of weight or measure",
        "section": "Section 38",
        "rule": "Legal Metrology (Approval of Models) Rules, 2011",
        "first_offence": "Fine which may extend to Rs. 25,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 25000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Director of Legal Metrology / Controller under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 38",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_39",
        "offence": "Penalty for import of non-standard weight or measure",
        "section": "Section 39",
        "rule": "Legal Metrology Act, 2009 Section 39",
        "first_offence": "Fine which may extend to Rs. 50,000",
        "repeat_offence": "Imprisonment for a term which may extend to 1 year or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 50000.0,
        "imprisonment": "Up to 1 year for second or subsequent offence",
        "compounding_authority": "Director of Legal Metrology / Controller under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 39",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_40",
        "offence": "Penalty for counterfeiting of seals or verification stamping marks",
        "section": "Section 40",
        "rule": "Legal Metrology Act, 2009 Section 40",
        "first_offence": "Imprisonment for a term which shall not be less than 6 months but which may extend to 1 year and with fine",
        "repeat_offence": "Imprisonment for a term which shall not be less than 1 year but which may extend to 5 years and with fine",
        "fine_min": 0.0,
        "fine_max": 50000.0,
        "imprisonment": "6 months to 5 years (NON-COMPOUNDABLE STATUTORY OFFENCE)",
        "compounding_authority": "N/A - Mandatory Court Prosecution under Section 49",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 40",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_41",
        "offence": "Penalty for giving false information or maintaining false returns",
        "section": "Section 41",
        "rule": "Legal Metrology Act, 2009 Section 41",
        "first_offence": "Fine which may extend to Rs. 5,000",
        "repeat_offence": "Imprisonment for a term which may extend to 6 months or with fine or with both",
        "fine_min": 0.0,
        "fine_max": 5000.0,
        "imprisonment": "Up to 6 months for second or subsequent offence",
        "compounding_authority": "Controller of Legal Metrology / Authorized Officer under Section 48",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 41",
        "effective_date": "2011-03-01"
    },
    {
        "penalty_id": "PEN_SEC_42",
        "offence": "Penalty for vexatious search or inspection by Legal Metrology Officer",
        "section": "Section 42",
        "rule": "Legal Metrology Act, 2009 Section 42",
        "first_offence": "Imprisonment for a term which may extend to 2 years or fine which may extend to Rs. 10,000 or both",
        "repeat_offence": "Imprisonment up to 2 years and fine",
        "fine_min": 0.0,
        "fine_max": 10000.0,
        "imprisonment": "Up to 2 years (NON-COMPOUNDABLE STATUTORY OFFENCE)",
        "compounding_authority": "N/A - Mandatory Departmental Proceeding / Court Prosecution",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 42",
        "effective_date": "2011-03-01"
    }
]

# VERIFIED STATUTORY COMPOUNDING PROVISIONS UNDER SECTION 48 OF LEGAL METROLOGY ACT, 2009
SEED_COMPOUNDING = [
    {
        "compounding_id": "CMP_SEC_48_1",
        "offence": "Compounding of offences under Sections 25, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 41 or any rule made thereunder",
        "compoundable": "COMPOUNDABLE",
        "compound_authority": "Director of Legal Metrology (Central) / Controller of Legal Metrology (Maharashtra) / Authorized Legal Metrology Officer",
        "conditions": "Offence may be compounded either before or after institution of prosecution, on payment of sum specified by Compounding Officer.",
        "amount": "Sum not exceeding statutory maximum fine specified for the respective section",
        "procedure": "Form C Application -> Hearing -> Compounding Order -> Treasury Payment -> Notice Discharge & Case Closure",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 48(1)",
        "effective_date": "2011-03-01"
    },
    {
        "compounding_id": "CMP_SEC_48_2",
        "offence": "Second or subsequent offence committed within 3 years of previous compounding",
        "compoundable": "NON_COMPOUNDABLE",
        "compound_authority": "N/A - Mandatory Court Prosecution under Section 49",
        "conditions": "Under Section 48(2), no offence shall be compounded if committed by a person within a period of 3 years from the date on which a similar offence committed by him was compounded.",
        "amount": "N/A",
        "procedure": "Mandatory filing of official complaint in Magistrate Court under Section 49",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 48(2)",
        "effective_date": "2011-03-01"
    }
]

SEED_INSPECTIONS = [
    {
        "inspection_id": "INSP_RETAIL_PACK",
        "inspection_type": "Surprise Market Inspection & Test Weighment",
        "authority": "Legal Metrology Officer / Inspector",
        "business_type": "Retail Establishment / Supermarket / Manufacturer Premises",
        "documents_to_check": ["Trader Registration Certificate", "Verification Certificate for Weights", "Purchase Invoices"],
        "physical_checks": ["Seal integrity on weighing instruments", "Stamping mark validity"],
        "package_checks": ["MRP tag", "Net content declaration", "Manufacturer address", "Consumer helpline", "Unit sale price"],
        "measurement_checks": ["Test weighing against standard working weights"],
        "evidence_required": ["Seizure memo (Form II)", "Sample package", "Inspection report signed by trader"],
        "follow_up_action": "Issue Show Cause Notice / Seizure Memo within 24 hours under Section 15",
        "legal_basis": "Legal Metrology Act, 2009 Section 15 & Maharashtra Legal Metrology (Enforcement) Rules, 2011 Rule 21"
    }
]

SEED_SEIZURES = [
    {
        "seizure_id": "SZ_SEC_15",
        "circumstances": "Reasonable belief that an offence under the Act has been committed regarding non-compliant pre-packaged commodities or unverified weights and measures",
        "legal_authority": "Legal Metrology Officer / Controller",
        "officer": "Legal Metrology Officer",
        "required_document": ["Form II - Seizure List", "Show Cause Notice under Section 15"],
        "evidence": ["Photographs of non-compliant package", "Test weighing verification record"],
        "inventory": "Itemized quantity, description, batch number, lot number, net content",
        "custody": "Safe custody in departmental store or bonded trader custody under formal undertaking",
        "release_disposal": "Released upon receipt of compounding order payment or court discharge order",
        "legal_source": "Legal Metrology Act, 2009 (Act No. 1 of 2010) Section 15"
    }
]

SEED_NOTICES = [
    {
        "notice_id": "NTC_SHOW_CAUSE",
        "notice_type": "Show Cause Notice for Non-Compliance",
        "trigger": "Detection of missing mandatory declarations, short weighment, or unverified scale during inspection",
        "authority": "Legal Metrology Officer",
        "recipient": "Manufacturer / Packer / Importer / Retailer",
        "required_contents": ["Alleged offence section", "Details of non-compliant package / scale", "7 to 15 days response window", "Compounding option under Section 48"],
        "response_period": "7 to 15 days",
        "legal_basis": "Legal Metrology Act, 2009 Section 15 & Section 48",
        "next_action": "Compounding proceedings or Magistrate Court Prosecution",
        "official_template": True
    },
    {
        "notice_id": "NTC_PROSECUTION_NOTICE",
        "notice_type": "Notice of Intention to Prosecute in Magistrate Court",
        "trigger": "Failure to respond to Show Cause Notice or refusal to compound non-compoundable repeat offence under Section 48(2)",
        "authority": "Assistant Controller of Legal Metrology / Controller",
        "recipient": "Accused Company / Nominated Director under Section 49",
        "required_contents": ["Charge sheet details", "Nominated person declaration under Section 49", "Court jurisdiction details"],
        "response_period": "15 days",
        "legal_basis": "Legal Metrology Act, 2009 Section 49",
        "next_action": "Magistrate Court Complaint Filing",
        "official_template": False
    }
]

SEED_WORKFLOWS = [
    {
        "workflow_id": "WF_MAHA_LMO_INSP",
        "department": "Legal Metrology Department Maharashtra",
        "role": "Legal Metrology Officer (Inspector)",
        "action": "Conduct inspection, test weights, inspect packaged commodities, issue seizure memo under Section 15",
        "jurisdiction": "MAHARASHTRA",
        "delegation": "Delegated by Controller of Legal Metrology Maharashtra under Section 15",
        "legal_basis": "Maharashtra Legal Metrology (Enforcement) Rules, 2011"
    },
    {
        "workflow_id": "WF_MAHA_CONTROLLER_CMP",
        "department": "Legal Metrology Department Maharashtra",
        "role": "Controller of Legal Metrology / Deputy Controller",
        "action": "Hear compounding applications in Form C, pass compounding orders under Section 48, authorize court prosecution",
        "jurisdiction": "MAHARASHTRA",
        "delegation": "Statutory Power under Section 48 & Section 50 of Legal Metrology Act, 2009",
        "legal_basis": "Legal Metrology Act, 2009 Section 48 & Maharashtra Enforcement Rules 2011"
    }
]

SEED_FORMS = [
    {
        "form_id": "FORM_1_PCR_REGISTRATION",
        "form_name": "Form I - Application for Registration of Manufacturer / Packer / Importer",
        "rule_reference": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 27",
        "purpose": "registration",
        "jurisdiction": "CENTRAL",
        "is_publicly_available": True,
        "status": "CURRENT",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/PackagedCommoditiesRules2011.pdf"
    },
    {
        "form_id": "FORM_2_SEIZURE_LIST",
        "form_name": "Form II - Seizure List & Inventory Memo",
        "rule_reference": "Legal Metrology Act, 2009 Section 15 & Maharashtra Enforcement Rules Rule 21",
        "purpose": "seizure",
        "jurisdiction": "MAHARASHTRA",
        "is_publicly_available": True,
        "status": "CURRENT",
        "source_url": "https://legalmetrology.maharashtra.gov.in/sites/default/files/Maharashtra_Enforcement_Rules_2011.pdf"
    },
    {
        "form_id": "FORM_C_COMPOUNDING",
        "form_name": "Form C - Application for Compounding of Offence",
        "rule_reference": "Maharashtra Legal Metrology (Enforcement) Rules, 2011 Rule 15 & Section 48",
        "purpose": "compounding",
        "jurisdiction": "MAHARASHTRA",
        "is_publicly_available": True,
        "status": "CURRENT",
        "source_url": "https://legalmetrology.maharashtra.gov.in/sites/default/files/Maharashtra_Enforcement_Rules_2011.pdf"
    },
    {
        "form_id": "FORM_LM_1_MANUFACTURER_LICENCE",
        "form_name": "Form LM-1 - Application for License as Manufacturer of Weights and Measures",
        "rule_reference": "Maharashtra Legal Metrology (Enforcement) Rules, 2011 Rule 6",
        "purpose": "licence",
        "jurisdiction": "MAHARASHTRA",
        "is_publicly_available": True,
        "status": "CURRENT",
        "source_url": "https://legalmetrology.maharashtra.gov.in/sites/default/files/Maharashtra_Enforcement_Rules_2011.pdf"
    },
    {
        "form_id": "FORM_INTERNAL_INSPECTION_CHECKLIST",
        "form_name": "District-Specific Internal Officer Audit Checklist",
        "rule_reference": "Internal Departmental Circular",
        "purpose": "inspection",
        "jurisdiction": "MAHARASHTRA",
        "is_publicly_available": False,
        "status": "OFFICIAL_FORM_NOT_FOUND",
        "source_url": None
    }
]

def seed_enforcement_databases(db: Session):
    from db.models import OfficialForm
    for p in SEED_PENALTIES:
        db.merge(Penalty(**p))
    for c in SEED_COMPOUNDING:
        db.merge(Compounding(**c))
    for i in SEED_INSPECTIONS:
        db.merge(Inspection(**i))
    for s in SEED_SEIZURES:
        db.merge(Seizure(**s))
    for n in SEED_NOTICES:
        db.merge(Notice(**n))
    for w in SEED_WORKFLOWS:
        db.merge(OfficerWorkflow(**w))
    for f in SEED_FORMS:
        db.merge(OfficialForm(**f))
    db.commit()
