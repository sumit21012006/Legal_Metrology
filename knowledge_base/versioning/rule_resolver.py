from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from db.models import LegalProvision, Amendment, RuleBase

def resolve_current_rule(db: Session, rule_id_or_num: str, target_date: Optional[str] = None) -> dict:
    """
    Determines which legal provision was legally applicable on the specified date.
    Builds the version chain: Original -> Amendment 1 -> Amendment 2 -> Current Version.
    If target_date is None, resolves the currently active rule.
    """
    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")

    # Search in structured RuleBase or LegalProvision
    rule_entry = db.query(RuleBase).filter(
        (RuleBase.rule_id == rule_id_or_num) | 
        (RuleBase.rule == rule_id_or_num) | 
        (RuleBase.section == rule_id_or_num)
    ).first()

    provisions = db.query(LegalProvision).filter(
        (LegalProvision.rule == rule_id_or_num) | 
        (LegalProvision.section == rule_id_or_num)
    ).all()

    # Find amendments affecting this rule
    amendments = db.query(Amendment).filter(
        (Amendment.affected_rule == rule_id_or_num) | 
        (Amendment.affected_section == rule_id_or_num)
    ).all()

    applicable_amendments = []
    for amd in amendments:
        if amd.effective_date and amd.effective_date <= target_date:
            applicable_amendments.append(amd)

    # Sort applicable amendments by effective_date
    applicable_amendments.sort(key=lambda x: x.effective_date or "")

    applicable_text = ""
    source_ref = ""
    effective_from = "2011-04-01"

    if provisions:
        applicable_text = provisions[0].text
        source_ref = f"{provisions[0].document_id} Rule {provisions[0].rule or provisions[0].section}"
        effective_from = provisions[0].effective_date or effective_from

    # Apply amendments chronologically up to target_date
    applied_history = []
    for amd in applicable_amendments:
        applied_history.append({
            "amendment_id": amd.amendment_id,
            "change_type": amd.change_type,
            "effective_date": amd.effective_date,
            "notification_number": amd.notification_number,
            "source_url": amd.source_url
        })
        if amd.new_text:
            applicable_text = f"[AMENDED BY {amd.notification_number} W.E.F. {amd.effective_date}]\n{amd.new_text}"
            effective_from = amd.effective_date

    return {
        "rule_id": rule_id_or_num,
        "target_date": target_date,
        "effective_from": effective_from,
        "effective_to": None,
        "applicable_text": applicable_text or f"Provision text for Rule/Section {rule_id_or_num}",
        "amendment_history": applied_history,
        "total_amendments_applied": len(applied_history),
        "source_reference": source_ref,
        "is_historical": target_date < datetime.now().strftime("%Y-%m-%d")
    }
