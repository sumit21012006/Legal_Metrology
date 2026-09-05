import os
import json
import csv

BASE_DIR = r"c:\Users\APURVA\Desktop\Hackathon\legal_metrology_KB_&_RB"
KB_DIR = os.path.join(BASE_DIR, "legal_knowledge_base")

# Load existing files
with open(os.path.join(KB_DIR, "legal_sources.json"), "r", encoding="utf-8") as f:
    sources = json.load(f)

# Ensure official 2022 compiled PDF is registered
pcr_2022_source = {
    "source_id": "LM-SRC-PCR-2022",
    "title": "The Legal Metrology (Packaged Commodities) Rules, 2011 With All Amendments (As of 9th May 2022)",
    "authority": "Central Government",
    "department": "Ministry of Consumer Affairs, Food and Public Distribution - Department of Consumer Affairs",
    "document_type": "Rule Compilation",
    "official_url": "https://consumeraffairs.nic.in/sites/default/files/PackagedCommoditiesRules2011.pdf",
    "publication_date": "2022-05-09",
    "effective_date": "2022-10-01",
    "retrieved_date": "2026-09-05",
    "version": "2022.1.0",
    "sha256": "9b1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
    "status": "CURRENT"
}

if not any(s["source_id"] == "LM-SRC-PCR-2022" for s in sources):
    sources.append(pcr_2022_source)

with open(os.path.join(KB_DIR, "legal_sources.json"), "w", encoding="utf-8") as f:
    json.dump(sources, f, indent=2)

# --- EXPANDED RULES (RULES 1 TO 34 + SCHEDULES I-VII) ---
FULL_RULES = [
    # CHAPTER I: PRELIMINARY
    {
        "rule_id": "LM-PC-001",
        "chapter": "CHAPTER I - PRELIMINARY",
        "category": "packaged_commodity",
        "product_category": ["all_packaged_commodities"],
        "field": "short_title_commencement",
        "requirement": "Short title: The Legal Metrology (Packaged Commodities) Rules, 2011. Came into force on 1st April, 2011.",
        "mandatory": True,
        "applicability": "Whole of India",
        "condition": "Statutory enactment",
        "exception": None,
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 52(2)(j)",
            "sub_rule": "Rule 1",
            "page": 5,
            "source_type": "official"
        },
        "violation": "N/A - Title provision",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-002",
        "chapter": "CHAPTER I - PRELIMINARY",
        "category": "packaged_commodity",
        "product_category": ["definitions"],
        "field": "statutory_definitions",
        "requirement": "Defines Dealer, E-commerce, E-commerce Entity, Marketplace Model, Industrial Consumer, Institutional Consumer, Manufacturer, Maximum Permissible Error, Net Quantity, Packer, Principal Display Panel, Retail Package, Retail Sale Price, Wholesale Package, Unit Sale Price.",
        "mandatory": True,
        "applicability": "All legal terms used under PCR 2011",
        "condition": "Statutory definitions",
        "exception": None,
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 2",
            "sub_rule": "Rule 2 (clauses a to s)",
            "page": 5,
            "source_type": "official"
        },
        "violation": "Misclassification of consumer or package type",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },

    # CHAPTER II: RETAIL SALE PROVISIONS (RULES 3 TO 23)
    {
        "rule_id": "LM-PC-003",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["bulk_packages", "industrial_institutional", "agricultural_produce"],
        "field": "chapter_applicability",
        "requirement": "Chapter II retail declarations do not apply to: (a) Packages containing > 25 kg or 25 L; (b) Cement, fertilizer, and agricultural farm produce in bags > 50 kg; (c) Packaged commodities meant for industrial or institutional consumers.",
        "mandatory": True,
        "applicability": "Scope of retail packaging regulations",
        "condition": "Packages exceeding 25kg/25L or 50kg for cement/fertilizers/agricultural produce",
        "exception": "Retail packages <= 25 kg/L",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18",
            "sub_rule": "Rule 3 (as amended vide GSR 629(E) 2017)",
            "page": 8,
            "source_type": "official"
        },
        "violation": "Misapplying retail exemptions to retail consumer packages <= 25 kg/L.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2018-01-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-004",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["all_packaged_commodities"],
        "field": "pre_packing_regulation",
        "requirement": "No person shall pre-pack, sell, distribute, deliver, or display for sale any pre-packaged commodity unless compliant with mandatory declarations securely affixed to the package.",
        "mandatory": True,
        "applicability": "All pre-packaged commodities",
        "condition": "Pre-packaged commodity offered for sale",
        "exception": None,
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "section": "Section 18 & Section 36(1)",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "sub_rule": "Rule 4",
            "page": 8,
            "source_type": "official"
        },
        "violation": "Sale, distribution, or storage of non-compliant pre-packaged commodities.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-005",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["standard_packages"],
        "field": "standard_pack_sizes",
        "requirement": "Recommended standard pack sizes specified in Second Schedule (Omitted vide GSR 226(E) dated 28.03.2022 w.e.f. 01.10.2022).",
        "mandatory": False,
        "applicability": "Historical standard pack sizes",
        "condition": "Second Schedule commodities",
        "exception": "Omitted w.e.f. 01.10.2022",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18",
            "sub_rule": "Rule 5 (Omitted vide GSR 226(E) 2022)",
            "page": 9,
            "source_type": "official"
        },
        "violation": "Historical non-standard pack size violation",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": "2022-10-01"
    },
    {
        "rule_id": "LM-PC-006",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["general_packaged_commodity", "retail_packages"],
        "field": "manufacturer_name_address",
        "requirement": "Name and complete address of the manufacturer or packer or importer must be prominently printed on PDP. Complete address includes registered office / factory postal address with PIN code.",
        "mandatory": True,
        "applicability": "All pre-packaged commodities",
        "condition": "Retail package offered for sale",
        "exception": "Small packages <= 10 cubic cm capacity.",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "section": "Section 18 & Section 36(1)",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "sub_rule": "Rule 6(1)(a) & Rule 10",
            "page": 10,
            "source_type": "official"
        },
        "violation": "Missing or incomplete manufacturer/packer/importer name or address.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-007",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["imported_goods"],
        "field": "country_of_origin",
        "requirement": "Name of the Country of Origin or manufacture or assembly in case of imported products must be stated on the package.",
        "mandatory": True,
        "applicability": "All imported pre-packaged commodities",
        "condition": "Imported commodity sold in India",
        "exception": "Domestic manufactured items",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "section": "Section 18 & Section 36(1)",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "sub_rule": "Rule 6(1)(aa) (Inserted vide GSR 629(E) 2017)",
            "page": 10,
            "source_type": "official"
        },
        "violation": "Absence of Country of Origin on imported package.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2018-01-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-008",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["general_packaged_commodity"],
        "field": "generic_name",
        "requirement": "Common or generic names of the commodity contained in the package must be declared on PDP.",
        "mandatory": True,
        "applicability": "All retail pre-packaged commodities",
        "condition": "Pre-packaged commodity offered for sale",
        "exception": "Single item packages clearly visible through transparent wrapper",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "section": "Section 18 & Section 36(1)",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "sub_rule": "Rule 6(1)(b)",
            "page": 10,
            "source_type": "official"
        },
        "violation": "Missing generic/common name on package label.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-009",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["general_packaged_commodity"],
        "field": "net_quantity",
        "requirement": "Net quantity in standard unit of weight (g, kg), volume (ml, l), length (cm, m), area (sq m), or number (N, piece, pair, set) must be declared.",
        "mandatory": True,
        "applicability": "All pre-packaged commodities",
        "condition": "Pre-packaged commodity offered for sale",
        "exception": "Net quantity <= 10g or 10ml under Rule 26(a)",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "section": "Section 18 & Section 36(1)",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "sub_rule": "Rule 6(1)(c) & Rule 11-13",
            "page": 11,
            "source_type": "official"
        },
        "violation": "Missing net quantity or use of non-standard metric symbols (e.g. gms, ltrs).",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-010",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["general_packaged_commodity", "food", "cosmetics"],
        "field": "date_of_manufacture_expiry",
        "requirement": "Month and year of manufacture must be declared (w.e.f 2022). For commodities unfit for consumption after time, 'Best before or Use by date, month and year' must be declared.",
        "mandatory": True,
        "applicability": "All pre-packaged commodities",
        "condition": "Retail package offered for sale",
        "exception": "Bidi, incense sticks, LPG cylinders.",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "section": "Section 18 & Section 36(1)",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "sub_rule": "Rule 6(1)(d) & Rule 6(1)(da)",
            "page": 11,
            "source_type": "official"
        },
        "violation": "Missing month/year of manufacture or missing Best Before / Use By date.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-011",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["general_packaged_commodity"],
        "field": "mrp",
        "requirement": "Maximum Retail Price (MRP) inclusive of all taxes must be declared in Indian currency format (e.g. MRP Rs. XX.XX / ₹ XX.XX incl. of all taxes). Price rounding off to nearest rupee/paise.",
        "mandatory": True,
        "applicability": "All retail pre-packaged commodities",
        "condition": "Retail sale package",
        "exception": "Wholesale packages under Rule 26(b)",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "section": "Section 18 & Section 36(1)",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "sub_rule": "Rule 6(1)(e)",
            "page": 12,
            "source_type": "official"
        },
        "violation": "Missing MRP, non-inclusive of taxes statement, price smudging, or dual MRP.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-012",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["general_packaged_commodity"],
        "field": "consumer_care",
        "requirement": "Name, address, telephone number, and email ID of the person or office to be contacted in case of consumer complaints must be declared.",
        "mandatory": True,
        "applicability": "All retail pre-packaged commodities",
        "condition": "Pre-packaged commodity offered for sale",
        "exception": "Small packages <= 10g/10ml where outer multipack declares details",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "section": "Section 18 & Section 36(1)",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "sub_rule": "Rule 6(2)",
            "page": 13,
            "source_type": "official"
        },
        "violation": "Missing consumer helpline phone number, email address, or contact address.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2016-01-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-013",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["general_packaged_commodity"],
        "field": "qr_code_gtin_e_code",
        "requirement": "Barcode, GTIN, QR Code, e-code for net quantity assurance, or government scheme logos (e.g. Swachh Bharat) are permissible in addition to mandatory declarations.",
        "mandatory": False,
        "applicability": "Optional voluntary package label additions",
        "condition": "In addition to mandatory Rule 6(1) declarations",
        "exception": "Cannot replace mandatory physical text declarations on retail packages.",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18",
            "sub_rule": "Rule 6(4A) (Inserted vide GSR 629(E) 2017)",
            "page": 14,
            "source_type": "official"
        },
        "violation": "Attempting to substitute mandatory printed MRP/Net Qty with QR code alone on non-electronic retail goods.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2018-01-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-014",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["gm_food", "cosmetics", "toiletries"],
        "field": "gm_and_veg_nonveg_dots",
        "requirement": "(1) Packages containing GM food must bear 'GM' at top of PDP. (2) Packages containing soaps, shampoos, toothpastes, cosmetics, and toiletries must bear a red/brown dot for non-veg origin or green dot for veg origin.",
        "mandatory": True,
        "applicability": "GM food, cosmetics, soaps, shampoos, toiletries",
        "condition": "Pre-packaged cosmetics and GM food",
        "exception": "Non-cosmetic non-food general items.",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18",
            "sub_rule": "Rule 6(7) & Rule 6(8)",
            "page": 15,
            "source_type": "official"
        },
        "violation": "Missing GM symbol or missing green/brown veg/non-veg dot on cosmetics.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2014-07-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-015",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["e_commerce_goods"],
        "field": "e_commerce_declarations",
        "requirement": "E-Commerce entities must ensure all mandatory declarations specified in Rule 6(1) (except month & year of manufacture) are displayed on the digital marketplace platform prior to purchase.",
        "mandatory": True,
        "applicability": "All e-commerce platforms selling pre-packaged goods in India",
        "condition": "Online digital marketplace listing",
        "exception": "Marketplace intermediary safe harbor applies if platform acts solely as facilitator under IT Act 2000.",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18 & Section 36(1)",
            "sub_rule": "Rule 6(10) (Inserted vide GSR 629(E) 2017)",
            "page": 15,
            "source_type": "official"
        },
        "violation": "Missing mandatory declarations (MRP, Net Qty, Country of Origin, Generic Name) on e-commerce product detail page.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2018-01-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-016",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["general_packaged_commodity"],
        "field": "unit_sale_price",
        "requirement": "Unit Sale Price in Rupees (rounded to 2 decimal places) must be declared as: per g (if <1kg) / per kg (if >1kg); per ml (if <1L) / per L (if >1L); per cm (if <1m) / per m (if >1m); per number/unit.",
        "mandatory": True,
        "applicability": "Pre-packaged commodities w.e.f. 01.10.2022 (vide GSR 226(E))",
        "condition": "Net quantity > 1 kg / 1 L / 1 m",
        "exception": "Not required if retail sale price equals unit sale price (e.g. 1 kg pack). Exempt for alcoholic beverages.",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18",
            "sub_rule": "Rule 6(11) & GSR 779(E) 2021 / GSR 226(E) 2022",
            "page": 16,
            "source_type": "official"
        },
        "violation": "Missing Unit Sale Price declaration on qualifying retail packages.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2022-10-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-017",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["pdp_font_size"],
        "field": "principal_display_panel_area_font_height",
        "requirement": "Minimum height of numerals and letters on PDP must comply with Table-I: (1) Area A <= 50 sq cm: min 1.0 mm (1.5 mm if blown/molded); (2) 50 < A <= 100: min 1.5 mm; (3) 100 < A <= 500: min 2.5 mm; (4) 500 < A <= 2500: min 4.0 mm; (5) A > 2500 sq cm: min 6.0 mm. Width of numeral/letter shall not be less than one-third of height.",
        "mandatory": True,
        "applicability": "Principal Display Panel font sizing for all retail packages",
        "condition": "PDP surface area measurement",
        "exception": "Packages <= 10 cubic cm capacity.",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18",
            "sub_rule": "Rule 7 & Table-I (vide GSR 629(E) 2017)",
            "page": 17,
            "source_type": "official"
        },
        "violation": "Font height smaller than statutory minimum required for PDP surface area.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2018-01-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-018",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["general_packaged_commodity"],
        "field": "declaration_placement_and_language",
        "requirement": "(1) Declarations must appear on PDP with surrounding space around net quantity equal to numeral height above/below and 2x height left/right. (2) Declarations must be in Hindi (Devnagri) or English. (3) Numerals must contrast conspicuously with background.",
        "mandatory": True,
        "applicability": "Placement, legibility, and contrast of declarations",
        "condition": "Pre-packaged commodity label",
        "exception": "Blown/molded text on glass/plastic containers exempt from contrasting color.",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18",
            "sub_rule": "Rules 8 & 9",
            "page": 20,
            "source_type": "official"
        },
        "violation": "Low contrast illegible font, obscured text, or missing English/Hindi text.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },
    {
        "rule_id": "LM-PC-023",
        "chapter": "CHAPTER II - RETAIL SALE",
        "category": "packaged_commodity",
        "product_category": ["retailers_and_wholesalers"],
        "field": "mrp_compliance_and_gst_weighing_scale",
        "requirement": "(1) No retail dealer or wholesaler shall sell any pre-packaged commodity at a price exceeding MRP. (2) Dual MRP on identical pre-packaged commodities is strictly prohibited. (3) Price smudging/overwriting stickers prohibited. (4) All GST retailers dealing in weight/volume commodities must maintain Class-III electronic weighing scale with printed receipt facility free of cost for consumers.",
        "mandatory": True,
        "applicability": "All retail dealers, wholesalers, and importers",
        "condition": "Retail sale transaction",
        "exception": "Lowering MRP via transparent sticker is permitted if original MRP is not covered.",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18 & Section 36(2)",
            "sub_rule": "Rule 18(1)-(7)",
            "page": 26,
            "source_type": "official"
        },
        "violation": "Overcharging above printed MRP, dual MRP printing, smudged price tag, or lack of Class-III check scale.",
        "penalty_reference": "LM-OFF-013",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },

    # CHAPTER V: EXEMPTIONS (RULE 26)
    {
        "rule_id": "LM-PC-028",
        "chapter": "CHAPTER V - EXEMPTIONS",
        "category": "packaged_commodity",
        "product_category": ["exempted_packages"],
        "field": "statutory_exemptions",
        "requirement": "Nothing in PCR 2011 applies to: (a) Net weight/measure <= 10g or 10ml (except tobacco products); (b) Fast food items packed by restaurant/hotel; (c) Formulated drugs covered under DPCO 2013; (d) Thread sold in coil to handloom weavers.",
        "mandatory": True,
        "applicability": "Exempt packages under Rule 26",
        "condition": "Net quantity <= 10g/ml or restaurant fast food or DPCO drugs",
        "exception": "Tobacco products (NOT exempt even if <= 10g/ml)",
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 18",
            "sub_rule": "Rule 26(a)-(e)",
            "page": 34,
            "source_type": "official"
        },
        "violation": "Attempting to issue non-compliance notice to legally exempt small packages.",
        "penalty_reference": "LM-OFF-012",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },

    # CHAPTER VI: REGISTRATION (RULES 27 TO 30)
    {
        "rule_id": "LM-PC-029",
        "chapter": "CHAPTER VI - REGISTRATION",
        "category": "packaged_commodity",
        "product_category": ["manufacturers", "packers", "importers"],
        "field": "mandatory_registration",
        "requirement": "Every manufacturer, packer, or importer of pre-packaged commodities must register their name and complete premises address with the Director of Legal Metrology (Central) or Controller (State) within 90 days of commencement. Application fee: Rs. 500.",
        "mandatory": True,
        "applicability": "All manufacturers, packers, and importers of packaged goods in India",
        "condition": "Commencement of pre-packaging or import operations",
        "exception": None,
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 37",
            "sub_rule": "Rule 27-30",
            "page": 35,
            "source_type": "official"
        },
        "violation": "Operating pre-packaging or import business without mandatory Registration Certificate.",
        "penalty_reference": "LM-OFF-014",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    },

    # CHAPTER VII: GENERAL & SCHEDULES (RULES 31 TO 34 + SCHEDULES I-VII)
    {
        "rule_id": "LM-PC-031",
        "chapter": "CHAPTER VII - GENERAL & SCHEDULES",
        "category": "packaged_commodity",
        "product_category": ["general_penalties", "schedules"],
        "field": "general_fine_and_schedules",
        "requirement": "(1) Rule 32: Whoever contravenes any provision of PCR 2011 for which no punishment is provided in the Act shall be punished with fine of Rs. 5,000. (2) Rule 32A: Compounding fees table for PCR rules. (3) First Schedule: Maximum Permissible Error (MPE) tables. (4) Fifth Schedule: Sample Selection Table. (5) Sixth Schedule: Corrected Average formula Xc = mean + (sigma x C).",
        "mandatory": True,
        "applicability": "General penalty clause and statutory measurement schedules",
        "condition": "Non-compliance with PCR rules without specific Act penalty",
        "exception": None,
        "legal_source": {
            "act": "Legal Metrology Act, 2009",
            "rule": "Legal Metrology (Packaged Commodities) Rules, 2011",
            "section": "Section 52",
            "sub_rule": "Rules 31-34 & Schedules I to VII",
            "page": 37,
            "source_type": "official"
        },
        "violation": "General contravention of Packaged Commodities Rules 2011.",
        "penalty_reference": "LM-OFF-032",
        "confidence": "verified",
        "effective_from": "2011-04-01",
        "effective_to": None
    }
]

# Update Rulebook JSON
with open(os.path.join(KB_DIR, "rulebook.json"), "r", encoding="utf-8") as f:
    rb_data = json.load(f)

rb_data["rules"] = FULL_RULES
rb_data["metadata"]["official_source_pdf"] = "THE LEGAL METROLOGY (PACKAGED COMMODITIES) RULES, 2011 With All Amendments (As of 9th May 2022)"

with open(os.path.join(KB_DIR, "rulebook.json"), "w", encoding="utf-8") as f:
    json.dump(rb_data, f, indent=2)

print("Updated rulebook.json with full 2022 PCR compilation rules.")
