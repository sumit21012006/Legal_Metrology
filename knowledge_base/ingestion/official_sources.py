from urllib.parse import urlparse
from config import OFFICIAL_DOMAINS

def is_official_url(url: str) -> bool:
    """
    Validates if a URL belongs strictly to a whitelisted official government domain.
    """
    if not url:
        return False
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    return any(domain == whitelist_domain or domain.endswith("." + whitelist_domain) for whitelist_domain in OFFICIAL_DOMAINS)

# Seed official documents from Government of India and Maharashtra Government
PRIMARY_GOVERNMENT_DOCUMENTS = [
    {
        "title": "Legal Metrology Act, 2009 (Act No. 1 of 2010)",
        "document_type": "ACT",
        "authority": "Central Government",
        "department": "Department of Consumer Affairs",
        "jurisdiction": "CENTRAL",
        "state": "INDIA",
        "publication_date": "2010-01-14",
        "effective_date": "2011-03-01",
        "notification_number": "Act 1 of 2010",
        "status": "CURRENT",
        "source_url": "https://www.indiacode.nic.in/bitstream/123456789/2040/1/201001.pdf",
        "source_domain": "indiacode.nic.in"
    },
    {
        "title": "Legal Metrology (Packaged Commodities) Rules, 2011",
        "document_type": "RULE",
        "authority": "Central Government",
        "department": "Department of Consumer Affairs",
        "jurisdiction": "CENTRAL",
        "state": "INDIA",
        "publication_date": "2011-03-07",
        "effective_date": "2011-04-01",
        "notification_number": "G.S.R. 202(E)",
        "status": "CURRENT",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/PackagedCommoditiesRules2011.pdf",
        "source_domain": "consumeraffairs.nic.in"
    },
    {
        "title": "Legal Metrology (General) Rules, 2011",
        "document_type": "RULE",
        "authority": "Central Government",
        "department": "Department of Consumer Affairs",
        "jurisdiction": "CENTRAL",
        "state": "INDIA",
        "publication_date": "2011-03-03",
        "effective_date": "2011-04-01",
        "notification_number": "G.S.R. 71(E)",
        "status": "CURRENT",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/GeneralRules2011.pdf",
        "source_domain": "consumeraffairs.nic.in"
    },
    {
        "title": "Legal Metrology (Approval of Models) Rules, 2011",
        "document_type": "RULE",
        "authority": "Central Government",
        "department": "Department of Consumer Affairs",
        "jurisdiction": "CENTRAL",
        "state": "INDIA",
        "publication_date": "2011-03-03",
        "effective_date": "2011-04-01",
        "notification_number": "G.S.R. 72(E)",
        "status": "CURRENT",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/ApprovalOfModelsRules2011.pdf",
        "source_domain": "consumeraffairs.nic.in"
    },
    {
        "title": "Legal Metrology (National Standards) Rules, 2011",
        "document_type": "RULE",
        "authority": "Central Government",
        "department": "Department of Consumer Affairs",
        "jurisdiction": "CENTRAL",
        "state": "INDIA",
        "publication_date": "2011-03-03",
        "effective_date": "2011-04-01",
        "notification_number": "G.S.R. 73(E)",
        "status": "CURRENT",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/NationalStandardsRules2011.pdf",
        "source_domain": "consumeraffairs.nic.in"
    },
    {
        "title": "Legal Metrology (Packaged Commodities) Amendment Rules, 2017",
        "document_type": "AMENDMENT",
        "authority": "Central Government",
        "department": "Department of Consumer Affairs",
        "jurisdiction": "CENTRAL",
        "state": "INDIA",
        "publication_date": "2017-06-23",
        "effective_date": "2018-01-01",
        "notification_number": "G.S.R. 629(E)",
        "status": "AMENDMENT",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/amendment_PCR_2017.pdf",
        "source_domain": "consumeraffairs.nic.in"
    },
    {
        "title": "Legal Metrology (Packaged Commodities) Amendment Rules, 2021",
        "document_type": "AMENDMENT",
        "authority": "Central Government",
        "department": "Department of Consumer Affairs",
        "jurisdiction": "CENTRAL",
        "state": "INDIA",
        "publication_date": "2021-11-02",
        "effective_date": "2022-12-01",
        "notification_number": "G.S.R. 779(E)",
        "status": "AMENDMENT",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/PCR_Amendment_2021.pdf",
        "source_domain": "consumeraffairs.nic.in"
    },
    {
        "title": "Legal Metrology (Packaged Commodities) Amendment Rules, 2022",
        "document_type": "AMENDMENT",
        "authority": "Central Government",
        "department": "Department of Consumer Affairs",
        "jurisdiction": "CENTRAL",
        "state": "INDIA",
        "publication_date": "2022-07-14",
        "effective_date": "2022-10-01",
        "notification_number": "G.S.R. 577(E)",
        "status": "AMENDMENT",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/PCR_Amendment_2022.pdf",
        "source_domain": "consumeraffairs.nic.in"
    },
    {
        "title": "Maharashtra Legal Metrology (Enforcement) Rules, 2011",
        "document_type": "RULE",
        "authority": "Maharashtra Government",
        "department": "Food, Civil Supplies and Consumer Protection Department",
        "jurisdiction": "MAHARASHTRA",
        "state": "MAHARASHTRA",
        "publication_date": "2011-04-01",
        "effective_date": "2011-04-01",
        "notification_number": "G.A.D. Notification 2011",
        "status": "CURRENT",
        "source_url": "https://legalmetrology.maharashtra.gov.in/sites/default/files/Maharashtra_Enforcement_Rules_2011.pdf",
        "source_domain": "legalmetrology.maharashtra.gov.in"
    },
    {
        "title": "Maharashtra Legal Metrology (Enforcement) Amendment Rules, 2018",
        "document_type": "AMENDMENT",
        "authority": "Maharashtra Government",
        "department": "Legal Metrology Department Maharashtra",
        "jurisdiction": "MAHARASHTRA",
        "state": "MAHARASHTRA",
        "publication_date": "2018-03-15",
        "effective_date": "2018-04-01",
        "notification_number": "M-LM-2018/CR-42",
        "status": "AMENDMENT",
        "source_url": "https://legalmetrology.maharashtra.gov.in/sites/default/files/Maha_Amendment_2018.pdf",
        "source_domain": "legalmetrology.maharashtra.gov.in"
    },
    {
        "title": "Maharashtra Legal Metrology (Enforcement) Amendment Rules, 2021",
        "document_type": "AMENDMENT",
        "authority": "Maharashtra Government",
        "department": "Legal Metrology Department Maharashtra",
        "jurisdiction": "MAHARASHTRA",
        "state": "MAHARASHTRA",
        "publication_date": "2021-08-20",
        "effective_date": "2021-09-01",
        "notification_number": "M-LM-2021/CR-105",
        "status": "AMENDMENT",
        "source_url": "https://legalmetrology.maharashtra.gov.in/sites/default/files/Maha_Amendment_2021.pdf",
        "source_domain": "legalmetrology.maharashtra.gov.in"
    },
    {
        "title": "Maharashtra Legal Metrology Officer Verification & Stamping Procedure Advisory",
        "document_type": "PROCEDURE",
        "authority": "Maharashtra Government",
        "department": "Legal Metrology Department Maharashtra",
        "jurisdiction": "MAHARASHTRA",
        "state": "MAHARASHTRA",
        "publication_date": "2022-01-10",
        "effective_date": "2022-01-10",
        "notification_number": "LMO/PROC/2022/01",
        "status": "GUIDANCE",
        "source_url": "https://legalmetrology.maharashtra.gov.in/sites/default/files/Verification_Stamping_Procedure.pdf",
        "source_domain": "legalmetrology.maharashtra.gov.in"
    },
    {
        "title": "Official FAQ: Declarations on Packaged Commodities (Department of Consumer Affairs)",
        "document_type": "FAQ",
        "authority": "Central Government",
        "department": "Department of Consumer Affairs",
        "jurisdiction": "CENTRAL",
        "state": "INDIA",
        "publication_date": "2023-05-15",
        "effective_date": "2023-05-15",
        "notification_number": "FAQ-DOCA-2023",
        "status": "FAQ",
        "source_url": "https://consumeraffairs.nic.in/sites/default/files/FAQ_Legal_Metrology.pdf",
        "source_domain": "consumeraffairs.nic.in"
    }
]
