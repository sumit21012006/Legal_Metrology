from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from db.models import Exemption

SEED_EXEMPTIONS = [
    {
        "exemption_id": "EXM_SMALL_PACK",
        "category": "small_packages",
        "rule_id": "PCR_RULE_26_2",
        "condition": "Net quantity <= 10g or 10ml",
        "description": "Packages containing net quantity 10g or 10ml or less are exempt from declaring individual mandatory details on the small package if displayed on multi-piece package.",
        "authority": "Central Government",
        "legal_source": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 26(2)"
    },
    {
        "exemption_id": "EXM_WHOLESALE",
        "category": "wholesale_packages",
        "rule_id": "PCR_RULE_26_1",
        "condition": "Package intended for wholesale trade or institutional consumer",
        "description": "Wholesale packages are exempt from retail price (MRP) declaration requirements specified for retail packages.",
        "authority": "Central Government",
        "legal_source": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 26(1) & Chapter III"
    },
    {
        "exemption_id": "EXM_INDUSTRIAL",
        "category": "industrial_consumer",
        "rule_id": "PCR_RULE_3",
        "condition": "Package sold directly to industrial consumer for use in manufacturing",
        "description": "Packages sold directly to industrial consumers (e.g. raw material drums) are exempt from Chapter II retail packaging rules.",
        "authority": "Central Government",
        "legal_source": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 3"
    },
    {
        "exemption_id": "EXM_FAST_FOOD",
        "category": "food",
        "rule_id": "PCR_RULE_26_3",
        "condition": "Unpackaged hot food or fast food served at hotels/restaurants",
        "description": "Unpackaged food items prepared for immediate consumption served at hotels/restaurants are exempt.",
        "authority": "Central Government",
        "legal_source": "Legal Metrology (Packaged Commodities) Rules, 2011 Rule 26(3)"
    }
]

def seed_exemptions(db: Session):
    for ex in SEED_EXEMPTIONS:
        entry = Exemption(**ex)
        db.merge(entry)
    db.commit()

def evaluate_compliance_and_exemptions(
    product_category: str,
    package_weight_g_ml: Optional[float] = None,
    is_wholesale: bool = False,
    is_industrial: bool = False,
    declarations_present: Optional[List[str]] = None
) -> Dict:
    """
    Evaluates compliance before declaring a violation.
    Checks applicable exemptions first before marking non-compliance.
    """
    if declarations_present is None:
        declarations_present = []

    exemptions_applied = []
    is_exempt = False

    # Check 1: Small package exemption (<= 10g or 10ml)
    if package_weight_g_ml is not None and package_weight_g_ml <= 10.0:
        exemptions_applied.append("EXM_SMALL_PACK: Net quantity <= 10g/10ml exempt from detailed individual package declaration under Rule 26(2).")
        is_exempt = True

    # Check 2: Wholesale package exemption
    if is_wholesale:
        exemptions_applied.append("EXM_WHOLESALE: Wholesale package exempt from retail MRP declarations under Rule 26(1).")
        is_exempt = True

    # Check 3: Industrial consumer exemption
    if is_industrial:
        exemptions_applied.append("EXM_INDUSTRIAL: Direct industrial supply exempt from Chapter II retail packaging rules under Rule 3.")
        is_exempt = True

    mandatory_declarations = [
        "manufacturer_name_address",
        "generic_name",
        "net_quantity",
        "month_year_packing",
        "mrp",
        "consumer_care"
    ]

    # Category-specific mandatory additions
    if product_category.lower() in ["food", "edible_oils"]:
        mandatory_declarations.append("fssai_license_number")
    if product_category.lower() == "edible_oils":
        mandatory_declarations.append("volume_at_30c")
    if product_category.lower() == "imported_goods":
        mandatory_declarations.append("importer_name_address")
        mandatory_declarations.append("country_of_origin")

    missing_declarations = [dec for dec in mandatory_declarations if dec not in declarations_present]

    if is_exempt:
        status = "COMPLIANT_EXEMPT"
        violation_found = False
        reason = "Exemption conditions met. No violation."
    elif len(missing_declarations) == 0:
        status = "COMPLIANT"
        violation_found = False
        reason = "All mandatory declarations present."
    else:
        status = "POTENTIAL_VIOLATION"
        violation_found = True
        reason = f"Missing mandatory declarations: {', '.join(missing_declarations)}"

    return {
        "product_category": product_category,
        "is_exempt": is_exempt,
        "exemptions_applied": exemptions_applied,
        "declarations_present": declarations_present,
        "missing_declarations": missing_declarations,
        "status": status,
        "violation_found": violation_found,
        "reason": reason
    }
