import os
import json

BASE_DIR = r"c:\Users\APURVA\Desktop\Hackathon\legal_metrology_KB_&_RB"
KB_DIR = os.path.join(BASE_DIR, "legal_knowledge_base")
NOTICES_DIR = os.path.join(KB_DIR, "notices")

os.makedirs(os.path.join(NOTICES_DIR, "improvement"), exist_ok=True)
os.makedirs(os.path.join(NOTICES_DIR, "seizure"), exist_ok=True)
os.makedirs(os.path.join(NOTICES_DIR, "panchanama"), exist_ok=True)
os.makedirs(os.path.join(NOTICES_DIR, "compounding"), exist_ok=True)

# Common placeholder block header/footer so all 20 required placeholders exist in every file

# 1A. IMPROVEMENT NOTICE EN
notice_imp_en = """# NOTICE OF DEMAND FOR RECTIFICATION / IMPROVEMENT NOTICE
**Issued under Section 15 of Legal Metrology Act, 2009 & Legal Metrology (Packaged Commodities) Rules, 2011**

**Notice Ref No:** {{NOTICE_ID}}  
**Case File Ref:** {{CASE_ID}}  
**Date of Issuance:** {{DATE}}  
**Place of Issuance:** {{PLACE}}  

---

### TO:
**Business Entity Name:** {{BUSINESS_NAME}}  
**Registered Office / Premises Address:** {{BUSINESS_ADDRESS}}  

---

### SUBJECT: Statutory Improvement Notice regarding observed non-compliances under the Legal Metrology Act, 2009.

Take notice that on **{{INSPECTION_DATE}}**, an inspection of your business premises/establishment situated at **{{BUSINESS_ADDRESS}}** was conducted by the undersigned Legal Metrology Officer (**{{INSPECTOR_NAME}}**, ID: **{{INSPECTOR_ID}}**).

During the course of inspection, the following pre-packaged commodity / weighing instrument was inspected:
- **Product / Instrument Description:** {{PRODUCT_NAME}}
- **Manufacturer / Packer / Importer:** {{MANUFACTURER_NAME}}
- **Batch / Lot Reference Number:** {{BATCH_NUMBER}}
- **Declared MRP:** {{MRP}}
- **Declared Net Quantity:** {{NET_QUANTITY}}

### OBSERVED STATUTORY VIOLATION:
{{OBSERVED_VIOLATION}}

### APPLICABLE LEGAL PROVISIONS:
- **Statutory Act & Section:** {{LEGAL_SECTION}}
- **Statutory Rule & Sub-rule:** {{LEGAL_RULE}}
- **Statutory Penalty Reference:** {{PENALTY}}

---

### DIRECTIVE & MANDATORY COMPLIANCE DEADLINE:
You are hereby directed to rectify the aforesaid non-compliance(s) within **{{DEADLINE}}** days from the date of receipt of this notice, failing which formal prosecution proceedings shall be instituted under the Legal Metrology Act, 2009 before the jurisdictional Judicial Magistrate Court.

---

**Issued By:**  
**Inspector Name:** {{INSPECTOR_NAME}}  
**Designation / Authority:** {{OFFICER_AUTHORITY}}  
**Inspector ID:** {{INSPECTOR_ID}}  
**Signature & Official Seal:** ________________________  
"""

# 1B. IMPROVEMENT NOTICE MR
notice_imp_mr = """# सुधारणा नोटीस (IMPROVEMENT NOTICE)
**कायदेशीर मापनशास्त्र अधिनियम, २००९ चे कलम १५ व कायदेशीर मापनशास्त्र (वेष्टित वस्तू) नियम, २०११ अन्वये निर्गमित**

**नोटीस क्रमांक:** {{NOTICE_ID}}  
**प्रकरण संदर्भ क्रमांक:** {{CASE_ID}}  
**दिनांक:** {{DATE}}  
**ठिकाण:** {{PLACE}}  

---

### प्रति:
**व्यवसाय/संस्थेचे नाव:** {{BUSINESS_NAME}}  
**पत्ता:** {{BUSINESS_ADDRESS}}  

---

### विषय: कायदेशीर मापनशास्त्र अधिनियम, २००९ अंतर्गत त्रुटी सुधारणेबाबत नोटीस.

आपणास कळविण्यात येते की, दिनांक **{{INSPECTION_DATE}}** रोजी स्वाक्षरीकर्ते कायदेशीर मापनशास्त्र अधिकारी (**{{INSPECTOR_NAME}}**, ओळख क्रमांक: **{{INSPECTOR_ID}}**) यांनी आपल्या **{{BUSINESS_ADDRESS}}** येथील व्यावसायिक आवाराची तपासणी केली.

तपासणीदरम्यान खालील वेष्टित वस्तू / वजन व मापन उपकरणाची पाहणी करण्यात आली:
- **वस्तू / उपकरणाचे नाव:** {{PRODUCT_NAME}}
- **उत्पादक / पॅकर / आयातदाराचे नाव:** {{MANUFACTURER_NAME}}
- **बॅच क्रमांक:** {{BATCH_NUMBER}}
- **छापील विक्री किंमत (MRP):** {{MRP}}
- **निव्वळ प्रमाण (Net Quantity):** {{NET_QUANTITY}}

### आढळलेले कायदेशीर उल्लंघन:
{{OBSERVED_VIOLATION}}

### संबंधित कायदेशीर तरतुदी:
- **अधिनियम व कलम:** {{LEGAL_SECTION}}
- **नियम व उप-नियम:** {{LEGAL_RULE}}
- **दंड तरतूद:** {{PENALTY}}

---

### सुचना व मुदत:
आपणास याद्वारे निर्देशित करण्यात येते की, सदर नोटीस प्राप्त झाल्यापासून **{{DEADLINE}}** दिवसांच्या आत वरील त्रुटींची दुरुस्ती करून पूर्तता अहवाल सादर करावा. अन्यथा कायदेशीर मापनशास्त्र अधिनियम, २००९ अन्वये सक्षम न्यायालयात खटला दाखल करण्यात येईल.

---

**निर्गमित करणारे अधिकारी:**  
**अधिकारी नाव:** {{INSPECTOR_NAME}}  
**पदनाम व प्राधिकरण:** {{OFFICER_AUTHORITY}}  
**अधिकारी ओळख क्रमांक:** {{INSPECTOR_ID}}  
**स्वाक्षरी व अधिकृत शिक्का:** ________________________  
"""

# 2A. SEIZURE NOTICE EN
notice_sei_en = """# SEIZURE MEMORANDUM / SEIZURE NOTICE (FORM ISO-1)
**Issued under Section 15(1)(b) & Section 15(2) of Legal Metrology Act, 2009**

**Seizure Memo No:** {{NOTICE_ID}}  
**Case File Ref:** {{CASE_ID}}  
**Date of Seizure:** {{DATE}}  
**Place of Seizure:** {{PLACE}}  

---

### FROM:
**Inspector / Legal Metrology Officer Name:** {{INSPECTOR_NAME}}  
**Officer ID:** {{INSPECTOR_ID}}  
**Authority / Designation:** {{OFFICER_AUTHORITY}}  

### TO (ESTABLISHMENT / PERSON IN POSSESSION):
**Name:** {{BUSINESS_NAME}}  
**Premises Address:** {{BUSINESS_ADDRESS}}  

---

### SEIZURE ORDER:
Whereas on **{{INSPECTION_DATE}}**, during inspection of premises situated at **{{BUSINESS_ADDRESS}}**, the undersigned Legal Metrology Officer has reason to believe that an offence under the Legal Metrology Act, 2009 has been committed in respect of the articles/packages detailed below:

### SCHEDULE OF SEIZED ARTICLES / PACKAGES:
1. **Article / Commodity Name:** {{PRODUCT_NAME}}
2. **Manufacturer / Packer:** {{MANUFACTURER_NAME}}
3. **Batch Reference:** {{BATCH_NUMBER}}
4. **Declared MRP & Net Quantity:** {{MRP}} | {{NET_QUANTITY}}
5. **Observed Legal Violation:** {{OBSERVED_VIOLATION}}
6. **Statutory Reference:** {{LEGAL_SECTION}} read with {{LEGAL_RULE}}
7. **Statutory Penalty Clause:** {{PENALTY}}
8. **Compliance Deadline:** {{DEADLINE}}

### LEGAL CUSTODY & DIRECTIONS:
The aforesaid seized goods/instruments have been seized and taken into statutory legal custody under Section 15 of Legal Metrology Act, 2009. You are directed not to alter, remove, dispose of, or tamper with any evidence relating to these seized articles.

---

**Seized By (Officer Signature & Seal):** ________________________  
"""

# 2B. SEIZURE NOTICE MR
notice_sei_mr = """# जप्ती पंचनामा व जप्ती नोटीस (FORM ISO-1)
**कायदेशीर मापनशास्त्र अधिनियम, २००९ चे कलम १५(१)(ब) व १५(२) अन्वये निर्गमित**

**जप्ती नोटीस क्रमांक:** {{NOTICE_ID}}  
**प्रकरण संदर्भ क्रमांक:** {{CASE_ID}}  
**जप्ती दिनांक:** {{DATE}}  
**जप्ती ठिकाण:** {{PLACE}}  

---

### अधिकारी तपशील:
**कायदेशीर मापनशास्त्र अधिकारी:** {{INSPECTOR_NAME}}  
**अधिकारी ओळख क्रमांक:** {{INSPECTOR_ID}}  
**पदनाम व प्राधिकरण:** {{OFFICER_AUTHORITY}}  

### ज्यांच्या ताब्यातुन वस्तू जप्त करण्यात आल्या त्या व्यावसायिकाचा तपशील:
**व्यावसायिक/संस्थेचे नाव:** {{BUSINESS_NAME}}  
**पत्ता:** {{BUSINESS_ADDRESS}}  

---

### जप्ती आदेश:
दिनांक **{{INSPECTION_DATE}}** रोजी **{{BUSINESS_ADDRESS}}** येथील तपासणीदरम्यान, खालील नमूद केलेल्या वस्तू/उपकरणांच्या बाबतीत कायदेशीर मापनशास्त्र अधिनियम, २००९ अन्वये गुन्हा घडल्याचे आढळून आल्याने खालील वस्तू जप्त करण्यात येत आहेत:

### जप्त केलेल्या वस्तूंची यादी:
१. **वस्तूचे नाव:** {{PRODUCT_NAME}}
२. **उत्पादक / पॅकर:** {{MANUFACTURER_NAME}}
३. **बॅच क्रमांक:** {{BATCH_NUMBER}}
४. **छापील MRP व निव्वळ प्रमाण:** {{MRP}} | {{NET_QUANTITY}}
५. **आढळलेले कायदेशीर उल्लंघन:** {{OBSERVED_VIOLATION}}
६. **कलम व नियम संदर्भ:** {{LEGAL_SECTION}} व {{LEGAL_RULE}}
७. **दंड तरतूद:** {{PENALTY}}
८. **मुदत:** {{DEADLINE}}

---

**जप्ती करणारे अधिकारी (स्वाक्षरी व शिक्का):** ________________________  
"""

# 3A. PANCHANAMA EN
notice_pan_en = """# SPOT PANCHANAMA (CONTEMPORANEOUS RECORD OF INSPECTION & SEIZURE)
**Prepared under Section 15(4) of Legal Metrology Act, 2009 read with Section 100 of Code of Criminal Procedure, 1973**

**Panchanama Ref No:** {{NOTICE_ID}}  
**Case Ref No:** {{CASE_ID}}  
**Date of Inspection:** {{INSPECTION_DATE}}  
**Time & Date:** {{DATE}}  
**Place of Inspection:** {{PLACE}} (Premises: {{BUSINESS_ADDRESS}})  

---

### BUSINESS & OFFICER DETAILS:
- **Business Entity:** {{BUSINESS_NAME}}
- **Officer Name:** {{INSPECTOR_NAME}} (ID: {{INSPECTOR_ID}}, Designation: {{OFFICER_AUTHORITY}})

---

### PROCEEDINGS & OBSERVATIONS:
In our presence, the officer inspected pre-packaged packages / weighing instruments.
- **Product Name:** {{PRODUCT_NAME}}
- **Manufacturer Details:** {{MANUFACTURER_NAME}}
- **Batch Number:** {{BATCH_NUMBER}}
- **MRP & Net Quantity:** {{MRP}} | {{NET_QUANTITY}}

### OBSERVATIONS & STATUTORY VIOLATION:
The officer demonstrated in our presence that the item violates **{{LEGAL_SECTION}}** and **{{LEGAL_RULE}}** with statutory penalty **{{PENALTY}}** due to:
{{OBSERVED_VIOLATION}}

The business owner has been granted **{{DEADLINE}}** days for statutory compliance response.

This Panchanama has been read over to us in English/Marathi, and we confirm that it is a true account.

---

**Attested By Legal Metrology Officer:**  
**Name:** {{INSPECTOR_NAME}}  
**Authority:** {{OFFICER_AUTHORITY}}  
**Signature & Official Seal:** ________________________  
"""

# 3B. PANCHANAMA MR
notice_pan_mr = """# घटनास्थळ पंचनामा (SPOT PANCHANAMA)
**कायदेशीर मापनशास्त्र अधिनियम, २००९ चे कलम १५(४) व फौजदारी प्रक्रिया संहिता, १९७३ चे कलम १०० अन्वये तयार केलेला पंचनामा**

**पंचनामा क्रमांक:** {{NOTICE_ID}}  
**प्रकरण संदर्भ क्रमांक:** {{CASE_ID}}  
**तपासणी दिनांक:** {{INSPECTION_DATE}}  
**वेळ/दिनांक:** {{DATE}}  
**तपासणीचे ठिकाण:** {{PLACE}} (पत्ता: {{BUSINESS_ADDRESS}})  

---

### व्यावसायिक व अधिकारी तपशील:
- **संस्थेचे नाव:** {{BUSINESS_NAME}}
- **अधिकारी नाव:** {{INSPECTOR_NAME}} (आयडी: {{INSPECTOR_ID}}, पदनाम: {{OFFICER_AUTHORITY}})

---

### पंचनामा तपशील:
आमच्या समक्ष अधिकाऱ्यांनी खालील वेष्टित वस्तूची तपासणी केली:
- **वस्तूचे नाव:** {{PRODUCT_NAME}}
- **उत्पादकाचा तपशील:** {{MANUFACTURER_NAME}}
- **बॅच क्रमांक:** {{BATCH_NUMBER}}
- **MRP व निव्वळ प्रमाण:** {{MRP}} | {{NET_QUANTITY}}

### आढळलेले उल्लंघन:
अधिकाऱ्यांनी आमच्या समक्ष दाखवून दिले की सदर वस्तू **{{LEGAL_SECTION}}** व **{{LEGAL_RULE}}** चे उल्लंघन करते (दंड तरतूद: {{PENALTY}}):
{{OBSERVED_VIOLATION}}

व्यावसायिकाला **{{DEADLINE}}** दिवसांची कायदेशीर मुदत देण्यात आली आहे.

---

**कायदेशीर मापनशास्त्र अधिकारी स्वाक्षरी व शिक्का:** ________________________  
"""

# 4A. COMPOUNDING ORDER EN
notice_cmp_en = """# COMPOUNDING ORDER / COMPOUNDING NOTICE
**Issued under Section 48 of Legal Metrology Act, 2009 & Rule 15 of Maharashtra Legal Metrology (Enforcement) Rules, 2011**

**Compounding Order No:** {{NOTICE_ID}}  
**Case Ref No:** {{CASE_ID}}  
**Date:** {{DATE}}  
**Place:** {{PLACE}}  

---

### BEFORE THE COMPOUNDING AUTHORITY:
**Controller / Authorized Officer:** {{OFFICER_AUTHORITY}}  
**Officer Name:** {{INSPECTOR_NAME}}  
**Officer ID:** {{INSPECTOR_ID}}  

### APPLICANT / OFFENDER DETAILS:
**Name of Business Entity:** {{BUSINESS_NAME}}  
**Address:** {{BUSINESS_ADDRESS}}  

---

### ORDER OF COMPOUNDING:
Whereas an application for compounding of offence was submitted by the applicant in Form C under Section 48(1) of Legal Metrology Act, 2009 in respect of observed violation:
- **Product Name:** {{PRODUCT_NAME}}
- **Manufacturer:** {{MANUFACTURER_NAME}}
- **Batch No:** {{BATCH_NUMBER}}
- **Declared MRP & Net Quantity:** {{MRP}} | {{NET_QUANTITY}}
- **Offence Description:** {{OBSERVED_VIOLATION}}
- **Statutory Section:** {{LEGAL_SECTION}}
- **Statutory Rule:** {{LEGAL_RULE}}
- **Statutory Penalty Clause:** {{PENALTY}}
- **Inspection Date:** {{INSPECTION_DATE}}

Whereas the undersigned Authority has satisfied itself that the present offence is a FIRST OFFENCE, and is compoundable under Section 48(1) of the Act;

NOW THEREFORE, in exercise of powers conferred under Section 48(1) of Legal Metrology Act, 2009, the undersigned Authority hereby orders the compounding of the said offence upon payment of a compounding fee of:
- **Compounding Amount:** ₹{{COMPOUNDING_AMOUNT}}
- **Payment Deadline:** Within {{DEADLINE}} days from date of this order into Government Treasury Account.

Upon full payment of the compounding fee, no further prosecution proceedings shall be instituted against the applicant for the said first offence.

---

**Compounding Authority Signature & Seal:** ________________________  
**Name:** {{INSPECTOR_NAME}}  
**Designation:** {{OFFICER_AUTHORITY}}  
"""

# 4B. COMPOUNDING ORDER MR
notice_cmp_mr = """# तडजोड आदेश (COMPOUNDING ORDER)
**कायदेशीर मापनशास्त्र अधिनियम, २००९ चे कलम ४८ व महाराष्ट्र कायदेशीर मापनशास्त्र (अमलबजावणी) नियम, २०११ चे नियम १५ अन्वये निर्गमित**

**तडजोड आदेश क्रमांक:** {{NOTICE_ID}}  
**प्रकरण संदर्भ क्रमांक:** {{CASE_ID}}  
**दिनांक:** {{DATE}}  
**ठिकाण:** {{PLACE}}  

---

### तडजोड अधिकारी:
**प्राधिकरण:** {{OFFICER_AUTHORITY}}  
**अधिकारी नाव:** {{INSPECTOR_NAME}}  
**अधिकारी ओळख क्रमांक:** {{INSPECTOR_ID}}  

### अर्जदार / व्यावसायिक तपशील:
**संस्थेचे नाव:** {{BUSINESS_NAME}}  
**पत्ता:** {{BUSINESS_ADDRESS}}  

---

### तडजोड आदेश:
अर्जदाराने नमुना सी (Form C) मध्ये कायदेशीर मापनशास्त्र अधिनियम, २००९ च्या कलम ४८(१) अन्वये खालील गुन्ह्याबाबत तडजोडीसाठी अर्ज दाखल केला होता:
- **वस्तूचे नाव:** {{PRODUCT_NAME}}
- **उत्पादकाचे नाव:** {{MANUFACTURER_NAME}}
- **बॅच क्रमांक:** {{BATCH_NUMBER}}
- **MRP व निव्वळ प्रमाण:** {{MRP}} | {{NET_QUANTITY}}
- **गुन्ह्याचे वर्णन:** {{OBSERVED_VIOLATION}}
- **कायदेशीर कलम:** {{LEGAL_SECTION}}
- **नियम संदर्भ:** {{LEGAL_RULE}}
- **दंड तरतूद:** {{PENALTY}}
- **तपासणी दिनांक:** {{INSPECTION_DATE}}

सदर गुन्हा हा प्रथम गुन्हा असून कलम ४८(१) अन्वये तडजोडयोग्य असल्याचे प्राधिकरणाची खात्री झाली आहे;

त्याअर्थी, कलम ४८(१) अन्वये प्राप्त अधिकारांचा वापर करून, खालील तडजोड शुल्क भरण्याच्या अटीवर गुन्हा तडजोड करण्यात येत आहे:
- **तडजोड रक्कम:** ₹{{COMPOUNDING_AMOUNT}}
- **रक्कम भरण्याची मुदत:** सदर आदेशाच्या दिनांकापासून {{DEADLINE}} दिवसांच्या आत शासकीय कोषागारात जमा करावी.

---

**तडजोड अधिकारी स्वाक्षरी व शिक्का:** ________________________  
**अधिकारी नाव:** {{INSPECTOR_NAME}}  
**पदनाम:** {{OFFICER_AUTHORITY}}  
"""

# Write all 8 notice files
with open(os.path.join(NOTICES_DIR, "improvement", "notice_improvement_en.md"), "w", encoding="utf-8") as f:
    f.write(notice_imp_en)
with open(os.path.join(NOTICES_DIR, "improvement", "notice_improvement_mr.md"), "w", encoding="utf-8") as f:
    f.write(notice_imp_mr)

with open(os.path.join(NOTICES_DIR, "seizure", "notice_seizure_en.md"), "w", encoding="utf-8") as f:
    f.write(notice_sei_en)
with open(os.path.join(NOTICES_DIR, "seizure", "notice_seizure_mr.md"), "w", encoding="utf-8") as f:
    f.write(notice_sei_mr)

with open(os.path.join(NOTICES_DIR, "panchanama", "notice_panchanama_en.md"), "w", encoding="utf-8") as f:
    f.write(notice_pan_en)
with open(os.path.join(NOTICES_DIR, "panchanama", "notice_panchanama_mr.md"), "w", encoding="utf-8") as f:
    f.write(notice_pan_mr)

with open(os.path.join(NOTICES_DIR, "compounding", "notice_compounding_en.md"), "w", encoding="utf-8") as f:
    f.write(notice_cmp_en)
with open(os.path.join(NOTICES_DIR, "compounding", "notice_compounding_mr.md"), "w", encoding="utf-8") as f:
    f.write(notice_cmp_mr)

print("Successfully created all 8 notice templates with complete placeholder coverage.")
