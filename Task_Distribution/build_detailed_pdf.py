from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    ListFlowable, ListItem, HRFlowable, Preformatted
)
from reportlab.lib.enums import TA_LEFT

# ---------- Colors ----------
NAVY = colors.HexColor("#1B2A4A")
MAIN_BLUE = colors.HexColor("#2C5282")
SMALL_TEAL = colors.HexColor("#0F766E")
PURPLE = colors.HexColor("#553C9A")
LIGHT_BLUE_BG = colors.HexColor("#EAF1F8")
LIGHT_TEAL_BG = colors.HexColor("#E6F4F2")
LIGHT_PURPLE_BG = colors.HexColor("#F1EDFB")
GREY_TEXT = colors.HexColor("#3A3A3A")
GOLD = colors.HexColor("#B7791F")
CODE_BG = colors.HexColor("#F5F5F5")

styles = getSampleStyleSheet()

title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=20, textColor=NAVY, spaceAfter=4, alignment=TA_LEFT)
subtitle_style = ParagraphStyle("SubtitleStyle", parent=styles["Normal"], fontName="Helvetica",
                                 fontSize=11, textColor=GREY_TEXT, spaceAfter=2)
intro_style = ParagraphStyle("IntroStyle", parent=styles["Normal"], fontName="Helvetica",
                              fontSize=9.8, textColor=GREY_TEXT, leading=14, spaceAfter=8)
section_header_style = ParagraphStyle("SectionHeader", parent=styles["Normal"], fontName="Helvetica-Bold",
                                       fontSize=13, textColor=colors.white, leading=15)
member_title_style = ParagraphStyle("MemberTitle", parent=styles["Normal"], fontName="Helvetica-Bold",
                                     fontSize=12.5, textColor=NAVY, spaceAfter=1, spaceBefore=2)
member_title_teal = ParagraphStyle("MemberTitleTeal", parent=member_title_style, textColor=SMALL_TEAL)
subheading_style = ParagraphStyle("Subheading", parent=styles["Normal"], fontName="Helvetica-Bold",
                                   fontSize=10, textColor=NAVY, spaceBefore=8, spaceAfter=3)
subheading_teal = ParagraphStyle("SubheadingTeal", parent=subheading_style, textColor=SMALL_TEAL)
label_style = ParagraphStyle("LabelStyle", parent=styles["Normal"], fontName="Helvetica-BoldOblique",
                              fontSize=9.3, textColor=NAVY, spaceBefore=5, spaceAfter=1)
label_style_teal = ParagraphStyle("LabelStyleTeal", parent=label_style, textColor=SMALL_TEAL)
body_style = ParagraphStyle("BodyStyle", parent=styles["Normal"], fontName="Helvetica",
                             fontSize=9.5, textColor=GREY_TEXT, leading=13.5)
bullet_style = ParagraphStyle("BulletStyle", parent=styles["Normal"], fontName="Helvetica",
                               fontSize=9.5, textColor=GREY_TEXT, leading=13)
note_style = ParagraphStyle("NoteStyle", parent=styles["Normal"], fontName="Helvetica-Oblique",
                             fontSize=9, textColor=GOLD, leading=12.5, spaceBefore=4)
table_header_style = ParagraphStyle("TableHeader", parent=styles["Normal"], fontName="Helvetica-Bold",
                                     fontSize=9.2, textColor=colors.white)
table_cell_style = ParagraphStyle("TableCell", parent=styles["Normal"], fontName="Helvetica",
                                   fontSize=8.8, textColor=GREY_TEXT, leading=12)
code_style = ParagraphStyle("CodeStyle", parent=styles["Normal"], fontName="Courier",
                             fontSize=8, textColor=colors.HexColor("#1A1A1A"), leading=11)


def section_bar(text, bg_color):
    t = Table([[Paragraph(text, section_header_style)]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def bullets(items, style=bullet_style, bullet_type="bullet"):
    return ListFlowable(
        [ListItem(Paragraph(i, style)) for i in items],
        bulletType=bullet_type, start="1" if bullet_type == "1" else "•",
        leftIndent=15, bulletFontSize=9, spaceBefore=2, spaceAfter=6,
    )


def code_block(lines):
    text = "\n".join(lines)
    t = Table([[Preformatted(text, code_style)]], colWidths=[160 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
    ]))
    return t


def member_header(number, name, owns, accent="blue"):
    is_teal = accent == "teal"
    s = []
    s.append(Paragraph(f"{number}. {name}", member_title_teal if is_teal else member_title_style))
    s.append(Paragraph(f"<i>{owns}</i>", body_style))
    return s


def connects_block(needs=None, provides=None, blocks=None, accent="blue"):
    is_teal = accent == "teal"
    lbl = label_style_teal if is_teal else label_style
    s = [Paragraph("Connects With", subheading_teal if is_teal else subheading_style)]
    if needs:
        for head, text in needs:
            s.append(Paragraph(head, lbl))
            s.append(Paragraph(text, body_style))
    if provides:
        for head, text in provides:
            s.append(Paragraph(head, lbl))
            s.append(Paragraph(text, body_style))
    if blocks:
        for head, text in blocks:
            s.append(Paragraph(head, lbl))
            s.append(Paragraph(text, body_style))
    return s


def deliverable_block(text, accent="blue"):
    is_teal = accent == "teal"
    return [
        Paragraph("Demo Deliverable", subheading_teal if is_teal else subheading_style),
        Paragraph(text, body_style),
    ]


def divider():
    return HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#D9D9D9"), spaceBefore=10, spaceAfter=12)


doc = SimpleDocTemplate(
    "/home/claude/detailed-task-distribution.pdf",
    pagesize=A4,
    topMargin=15 * mm, bottomMargin=15 * mm,
    leftMargin=20 * mm, rightMargin=20 * mm,
    title="Detailed Task Distribution & Integration Guide",
)

story = []

# ---------- Header ----------
story.append(Paragraph("Detailed Task Distribution &amp; Integration Guide", title_style))
story.append(Paragraph("SIH Internal Round Prototype  |  PS 34 — Legal Metrology Automation", subtitle_style))
story.append(Spacer(1, 4))
story.append(HRFlowable(width="100%", thickness=1.2, color=NAVY, spaceAfter=10))
story.append(Paragraph(
    "For every member: <b>What to Build</b> (specific, step-by-step), <b>Connects With</b> "
    "(what you need from others, and who's waiting on your output), and <b>Demo Deliverable</b>. "
    "The Integration Guide at the end shows exactly how all six pieces get wired into one working system.",
    intro_style
))
story.append(Spacer(1, 8))

# =========================================================
# MAIN TASKS
# =========================================================
story.append(section_bar("MAIN TASKS", MAIN_BLUE))
story.append(Spacer(1, 10))

# ---- Member 1 ----
story += member_header(1, "Backend &amp; Database Architect", "NestJS API Gateway, PostgreSQL schema, workflow/state logic")
story.append(Paragraph("What to Build", subheading_style))
story.append(Paragraph("1. Database schema (PostgreSQL) — these tables, minimum:", body_style))
story.append(bullets([
    "<b>users</b> (id, role, name, phone, email, keycloak_id)",
    "<b>businesses</b> (id, owner_user_id, name, address, geo_lat, geo_lng, gstin, turnover_band)",
    "<b>complaints</b> (id, citizen_id, business_id [nullable], retailer_name_text, retailer_address_text, category, description, photo_urls[], invoice_url, status)",
    "<b>inspections</b> (id, inspector_id, business_id, complaint_id [nullable], visit_date, status)",
    "<b>ocr_results</b> (id, inspection_id/self_check_id, image_urls[], extracted_fields JSON, violations JSON, offence_tier)",
    "<b>self_check_reports</b> (id, business_id, image_urls[], extracted_fields JSON, violations JSON) — its own table, never joined into inspector/controller queries",
    "<b>notices</b> (id, case_id, type, content_text, section_refs, status, issued_date, deadline_date, pdf_url, signature_url)",
    "<b>offence_records</b> (id, product_name_normalized, manufacturer_normalized, business_id, notice_id, offence_number, date)",
    "<b>disputes</b> (id, notice_id, business_id, comment, status)",
    "<b>payments</b> (id, notice_id, business_id, amount, razorpay_order_id, status)",
    "<b>supply_chain_links</b> (id, source_business_id, named_business_id, inspection_id, status)",
]))
story.append(Paragraph("2. REST API endpoints (NestJS):", body_style))
story.append(bullets([
    "<font face='Courier'>POST /complaints</font> — citizen files a complaint",
    "<font face='Courier'>GET /complaints/:id/status</font> — status tracker",
    "<font face='Courier'>GET /complaints?region=</font> — inspector/controller queue",
    "<font face='Courier'>POST /businesses</font> — register a business",
    "<font face='Courier'>POST /inspections</font> — start an inspection",
    "<font face='Courier'>POST /inspections/:id/ocr-result</font> — receives OCR output",
    "<font face='Courier'>GET /offence-history?product=&amp;manufacturer=</font> — offence tier check",
    "<font face='Courier'>POST /notices</font> — create/store a notice (calls the AI service's NLP endpoint internally)",
    "<font face='Courier'>PATCH /notices/:id</font> — status changes (acknowledged, disputed, approved, rejected, paid)",
    "<font face='Courier'>POST /self-check</font> — business submits packaging photos (private path)",
    "<font face='Courier'>POST /disputes</font>",
    "<font face='Courier'>POST /payments/initiate</font>, <font face='Courier'>POST /payments/webhook</font> (Razorpay callback)",
    "<font face='Courier'>GET /controller/dashboard/stats</font>",
    "<font face='Courier'>POST /supply-chain-links</font>, <font face='Courier'>PATCH /supply-chain-links/:id/assign</font>",
]))
story.append(Paragraph(
    "3. <b>Keycloak setup</b> — 4 roles (Citizen, Business, Inspector, Controller), JWT validation middleware, "
    "route guards per role.<br/>"
    "4. <b>Case workflow logic</b> — a CaseWorkflowService enforcing valid status transitions: Received &rarr; "
    "Assigned &rarr; Inspected &rarr; Notice Issued &rarr; Compounded/Prosecution &rarr; Resolved. Reject any "
    "transition that skips a stage.<br/>"
    "5. <b>Deadline &amp; offence logic</b> — days_remaining = deadline_date minus today, computed per notice "
    "type using the day-counts from the Rulebook; offence-tier lookup either done here or delegated to the AI "
    "service's fuzzy-match function (agree this with Member 2 directly).",
    body_style
))
story += connects_block(
    needs=[
        ("Needs from Member 5 (Rulebook):", "penalty amounts and deadline-day counts per notice type — needed by end of Week 1 to finalize the schema, even in draft form."),
        ("Needs from Member 2 (AI/OCR):", "the exact JSON shape of the OCR result and notice-generation response, agreed on Day 1–2, so the ocr_results and notices tables match what's actually returned."),
    ],
    provides=[
        ("Provides to Member 2:", "the API contract for how their service gets called (base URL, expected input format for images/case data)."),
        ("Provides to Member 3 &amp; 4 (Frontend):", "a Postman collection / Swagger docs with sample requests and responses for every endpoint above — this unblocks them to start building screens before the backend is fully live."),
        ("Provides to Member 6:", "the /payments/webhook endpoint ready to receive and test Razorpay callbacks."),
    ],
)
story += deliverable_block(
    "Swagger/Postman collection showing every endpoint working with sample data — a complaint can be filed, an "
    "inspection opened, a notice issued and moved through its status ladder, and offence history correctly "
    "queried, all testable independent of any frontend."
)
story.append(divider())

# ---- Member 2 ----
story += member_header(2, "AI/OCR + NLP Engineer", "Python + FastAPI AI service")
story.append(Paragraph("What to Build", subheading_style))
story.append(bullets([
    "<b>Image preprocessing</b> — basic OpenCV cleanup (deskew, contrast boost, crop) on each of the 2–3 uploaded angle-photos before OCR.",
    "<b>OCR extraction</b> — Tesseract (pytesseract) or EasyOCR on each image; merge and de-duplicate extracted text across the angles into one combined text block.",
    "<b>Field extraction</b> — pattern/regex rules to pull MRP, net quantity/weight, mfg date, expiry date, manufacturer name &amp; address, consumer care details, country of origin. Build and tune this iteratively against real product photos.",
    "<b>Compliance rule engine</b> — load the Rulebook JSON (Member 5) at startup; for each required field, check presence and format validity; output a structured violations list.",
    "<b>Offence matching</b> — normalize product + manufacturer name, run rapidfuzz fuzzy matching against existing offence records to catch near-duplicates, and determine offence tier.",
    "<b>NLP Notice Generator</b> — take case data + the notice template placeholders (Member 5) and fill them in (Jinja2-style templating) to produce final notice text in English and one regional language.",
]))
story.append(Paragraph("Endpoints to expose (FastAPI):", body_style))
story.append(bullets([
    "<font face='Courier'>POST /ocr/scan</font> — multipart image upload &rarr; extracted fields + violations + offence tier",
    "<font face='Courier'>POST /ocr/self-check</font> — same pipeline, flagged private, skips the offence-tier step",
    "<font face='Courier'>POST /notices/generate</font> — case data JSON &rarr; filled notice text (both languages)",
]))
story += connects_block(
    needs=[
        ("Needs from Member 5 (Rulebook) — hard blocker:", "at least a draft rulebook.json and notice templates by end of Week 1 to start building the rule engine and generator at all."),
        ("Needs from Member 1:", "agreement on the exact request/response JSON shape (Day 1–2), and confirmation that NestJS calls this service internally rather than the mobile app calling it directly."),
    ],
    provides=[
        ("Provides to Member 1:", "the finalized OCR result and notice-generation JSON schemas, which shape the ocr_results and notices tables."),
        ("Provides to Member 3 (via Member 1):", "the field names in the OCR response are what the Flutter review screen renders as editable fields — cross-check this schema directly once stable."),
    ],
)
story += deliverable_block(
    "A working FastAPI service, demoable directly via its own Swagger UI (/docs) — upload real packaging "
    "photos, get back structured violation data and a generated notice, and a working offence-tier check "
    "against a small test dataset of past offences."
)
story.append(divider())

# ---- Member 3 ----
story += member_header(3, "Mobile App Developer (Flutter — Inspector + Business)", "The Flutter app, both Inspector and Business modes")
story.append(Paragraph("What to Build — Inspector mode", subheading_style))
story.append(bullets([
    "Login screen",
    "Business search/select screen (GET /businesses?search=)",
    "New inspection screen — start an inspection against a selected business (optionally linked to a citizen complaint)",
    "Multi-angle camera capture screen (2–3 photos), uploads to the backend",
    "OCR review screen — extracted fields shown in <b>editable</b> form fields so the inspector can correct anything before proceeding",
    "Offence-tier display (first/second offence, shown after backend responds)",
    "Notice screen — review the auto-generated notice text, capture a digital signature (signature-pad widget), submit to issue",
    "Panchanama form — two witness fields (name + contact), seizure sample photo upload, auto-generated Sample ID",
    "Offline mode — local storage (sqflite/Hive) for inspection data with no signal, with a sync manager that pushes queued records once back online",
]))
story.append(Paragraph("What to Build — Business mode", subheading_style))
story.append(bullets([
    "Registration screen (name, address, GSTIN, turnover)",
    "Self-check screen — same multi-angle camera flow, calls /self-check, shows results privately with a clear \"Private — never shared with inspectors\" label",
    "Notice inbox — list + detail view of notices received",
    "Notice detail actions: Submit Correction (re-upload photos), Raise Dispute (text box), Give Consent, Pay Penalty (Razorpay checkout)",
]))
story += connects_block(
    needs=[
        ("Needs from Member 1:", "the full API contract (Postman collection) — can start building UI against mock JSON immediately, without waiting for the live backend."),
        ("Needs from Member 2 (via Member 1):", "the exact OCR response field names, to build the editable review screen correctly."),
        ("Needs from Member 6:", "Razorpay test keys and SDK integration snippet for the payment screen."),
    ],
    provides=[
        ("Provides to Member 6:", "a working app to run end-to-end QA against, and screen recordings for the presentation deck."),
    ],
)
story += deliverable_block(
    "An installable APK (or emulator build) demonstrating the complete inspector flow (select business &rarr; "
    "scan &rarr; review &rarr; generate notice &rarr; sign) and the complete business flow (register &rarr; "
    "self-check &rarr; view private results &rarr; view a notice &rarr; dispute or pay)."
)

# =========================================================
# SMALL TASKS
# =========================================================
story.append(Spacer(1, 6))
story.append(section_bar("SMALL TASKS", SMALL_TEAL))
story.append(Spacer(1, 10))

# ---- Member 4 ----
story += member_header(4, "Web Frontend Developer (Next.js — Citizen + Controller)", "Web dashboards for Citizen and Controller", accent="teal")
story.append(Paragraph("What to Build — Citizen", subheading_teal))
story.append(bullets([
    "Signup with OTP verification",
    "Complaint form — category dropdown, multi-photo + invoice upload, retailer name/address fields with autocomplete against GET /businesses",
    "\"My Complaints\" list + status-tracker detail view",
    "Incentive status badge (Pending / Credited)",
]))
story.append(Paragraph("What to Build — Controller", subheading_teal))
story.append(bullets([
    "Login (Controller role)",
    "Dashboard home — stat cards and region-wise table (GET /controller/dashboard/stats)",
    "Case queue — pending Compounded Orders, with Approve / Reject (+comment) / Escalate to Prosecution actions",
    "Supply-chain assignment screen — pending supply_chain_links, assign to an inspector by jurisdiction",
]))
story += connects_block(
    needs=[
        ("Needs from Member 1:", "full API docs for the endpoints above."),
        ("Needs from Member 5 (nice-to-have, not blocking):", "the violation-category list — start with a hardcoded version, swap in the Rulebook-driven list once ready."),
    ],
    provides=[
        ("Provides to Member 1:", "the Controller's Approve/Reject/Escalate actions trigger backend status transitions — confirm the exact request payload together."),
        ("Provides to Member 6:", "a working web app for end-to-end testing and demo screenshots."),
    ],
    accent="teal",
)
story += deliverable_block(
    "A working web app — file and track a complaint as a citizen, and approve/reject/escalate a case as the "
    "Controller.", accent="teal"
)
story.append(divider())

# ---- Member 5 ----
story += member_header(5, "Database / Legal Knowledge Base Maker", "The Legal Metrology rulebook — the most upstream role", accent="teal")
story.append(Paragraph("What to Build", subheading_teal))
story.append(bullets([
    "Read the Legal Metrology Act, 2011 and the Legal Metrology (Packaged Commodities) Rules, 2011, focusing especially on Rule 6 (mandatory declarations).",
    "Build rulebook.json — one entry per mandatory field (see structure below).",
    "Build the deadline-days config per notice type — use the Rules' actual timelines where explicit; where the Act doesn't specify one, use a clearly-labeled configurable default rather than guessing silently.",
    "Draft the four notice templates (Improvement, Seizure, Panchanama, Compounded Order) with placeholders, in English and one regional language, each citing the correct Act/Rule section.",
    "Hand off to Member 2 and Member 1 — first draft by end of Week 1, refine through Week 2.",
]))
story.append(code_block([
    "{",
    '  "field_key": "mrp",',
    '  "field_label": "Maximum Retail Price",',
    '  "requirement": "Must be printed as \'MRP: Rs. XX inclusive of all taxes\'",',
    '  "act_section": "Rule 6(1)(f)",',
    '  "penalty_first_offence": "...",',
    '  "penalty_second_offence": "..."',
    "}",
]))
story.append(Paragraph(
    "Cover: MRP, net quantity, mfg date, expiry date, manufacturer name &amp; address, consumer care detail, "
    "country of origin, unit sale price, generic name.", body_style
))
story += connects_block(
    needs=[("Needs from anyone:", "nothing — this is the one role that should start on Day 1 with zero dependencies.")],
    blocks=[("Blocks:", "Member 2's entire rule engine and notice generator, Member 1's penalty/deadline schema, and (loosely) Member 4's category dropdown. This is the most upstream dependency in the project — a delay here delays almost everyone else.")],
    accent="teal",
)
story += deliverable_block(
    "rulebook.json (or a spreadsheet the team can convert), the four bilingual notice templates, and a one-page "
    "cheat sheet of the Act's core packaging requirements — genuinely useful to show judges as evidence of real "
    "domain research.", accent="teal"
)
story.append(Paragraph(
    "Note: this is not \"small\" in importance — it's smaller in coding effort, but the entire OCR compliance "
    "engine and notice generator are useless without it.", note_style
))
story.append(divider())

# ---- Member 6 ----
story += member_header(6, "Integrations, QA &amp; Presentation Owner", "Payments, mocked integrations, testing, and the pitch", accent="teal")
story.append(Paragraph("What to Build", subheading_teal))
story.append(bullets([
    "<b>Razorpay</b> — sandbox account, SDK integration into Member 3's payment screen, and the /payments/webhook handler built together with Member 1.",
    "<b>Mocked integrations</b> — GSTIN validation as a format/regex check with a hardcoded pass response; WhatsApp/Email via a free-tier service (Twilio sandbox / SendGrid) triggered at 2–3 key transitions; eMudhra stands in as the signature-pad capture already built in the Flutter app.",
    "<b>End-to-end QA</b> — once pieces are wired together, manually run the full path (Citizen complaint &rarr; Inspection &rarr; Notice ladder &rarr; Compounding &rarr; Controller approval &rarr; Payment) repeatedly, logging bugs to a shared tracker.",
    "<b>Presentation</b> — SIH pitch deck, a written demo script (exact click-by-click sequence), and a backup recorded video of the full demo.",
]))
story += connects_block(
    needs=[
        ("Needs from everyone:", "a mostly-working system before full end-to-end testing can start (realistically Week 3)."),
        ("Needs Razorpay setup done early (Week 1):", "so Member 3 isn't blocked integrating the SDK."),
    ],
    provides=[("Provides to everyone:", "the bug list from QA — the main feedback loop back into the other five members' work during Week 4.")],
    accent="teal",
)
story += deliverable_block(
    "A working payment flow, a resolved bug log, the final pitch deck, and a rehearsed demo script with a "
    "backup video.", accent="teal"
)

# =========================================================
# INTEGRATION GUIDE
# =========================================================
story.append(Spacer(1, 6))
story.append(section_bar("INTEGRATION GUIDE — WIRING IT ALL TOGETHER", PURPLE))
story.append(Spacer(1, 10))

story.append(Paragraph("Step 1 — Agree on contracts before writing feature code (Day 1)", subheading_style))
story.append(Paragraph(
    "Before anyone builds a screen or a business-logic function, get three things written down in one shared "
    "doc, agreed by the relevant people:", body_style
))
story.append(bullets([
    "<b>The REST API contract</b> — every endpoint, method, and request/response JSON shape. Member 1 drafts it, everyone else reviews it.",
    "<b>The OCR result JSON schema</b> — agreed between Member 1 and Member 2.",
    "<b>The notice template placeholder format</b> — agreed between Member 5 and Member 2.",
]))
story.append(Paragraph(
    "This single planning session prevents the most common hackathon integration failure: two people building "
    "against two different assumptions about a field name.", body_style
))

story.append(Paragraph("Step 2 — The connection map: who calls whom", subheading_style))
conn_data = [
    [Paragraph("Caller", table_header_style), Paragraph("Callee", table_header_style), Paragraph("Purpose", table_header_style)],
    [Paragraph("Flutter app (Inspector/Business)", table_cell_style), Paragraph("NestJS backend", table_cell_style), Paragraph("All mobile requests — one single base URL", table_cell_style)],
    [Paragraph("Next.js app (Citizen/Controller)", table_cell_style), Paragraph("NestJS backend", table_cell_style), Paragraph("Same backend, different endpoints/roles", table_cell_style)],
    [Paragraph("NestJS backend", table_cell_style), Paragraph("FastAPI AI service", table_cell_style), Paragraph("Internal call for /ocr/scan, /ocr/self-check, /notices/generate", table_cell_style)],
    [Paragraph("NestJS backend", table_cell_style), Paragraph("PostgreSQL", table_cell_style), Paragraph("All persistent data", table_cell_style)],
    [Paragraph("NestJS backend", table_cell_style), Paragraph("Keycloak", table_cell_style), Paragraph("Auth token validation", table_cell_style)],
    [Paragraph("NestJS backend", table_cell_style), Paragraph("Razorpay", table_cell_style), Paragraph("Payment order creation + webhook", table_cell_style)],
    [Paragraph("FastAPI AI service", table_cell_style), Paragraph("rulebook.json", table_cell_style), Paragraph("Loaded at startup from a shared file, updated via Member 5's commits", table_cell_style)],
]
conn_tbl = Table(conn_data, colWidths=[48 * mm, 42 * mm, 80 * mm])
conn_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_PURPLE_BG]),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(conn_tbl)
story.append(Spacer(1, 8))
story.append(Paragraph(
    "<b>Key decision:</b> the mobile and web apps only ever talk to the NestJS backend — never directly to the "
    "FastAPI service. The backend proxies AI requests internally. This gives Member 3 and Member 4 exactly one "
    "API base URL to configure, instead of two.", body_style
))

story.append(Paragraph("Step 3 — Local dev environment", subheading_style))
story.append(Paragraph(
    "Set up a docker-compose.yml with four services: postgres, keycloak, nestjs-backend, fastapi-ai-service — "
    "anyone on the team should be able to run one command and get the full backend running locally to build "
    "their frontend against. Pair this with a single shared .env.example file listing every required variable "
    "(DB connection string, Keycloak URL, Razorpay keys, AI service base URL).", body_style
))

story.append(Paragraph("Step 4 — Phased integration plan", subheading_style))
phase_data = [
    [Paragraph("Phase", table_header_style), Paragraph("When", table_header_style), Paragraph("What happens", table_header_style)],
    [Paragraph("1", table_cell_style), Paragraph("Week 1", table_cell_style), Paragraph("Everyone builds against mocks. Member 1 gives Member 3 &amp; 4 a Postman collection with fake responses. Member 2 tests OCR standalone via FastAPI's /docs.", table_cell_style)],
    [Paragraph("2", table_cell_style), Paragraph("Week 2", table_cell_style), Paragraph("Member 1 and Member 2 connect for real — NestJS calls the live FastAPI service for the first time. Verify one full round trip.", table_cell_style)],
    [Paragraph("3", table_cell_style), Paragraph("Early Wk 3", table_cell_style), Paragraph("Member 3 &amp; 4 switch from mock data to the real NestJS backend (run locally, tunneled with ngrok for a physical phone).", table_cell_style)],
    [Paragraph("4", table_cell_style), Paragraph("Mid Wk 3", table_cell_style), Paragraph("Swap in Member 5's finalized rulebook data, replacing placeholder rules, and re-test notice generation with real legal text.", table_cell_style)],
    [Paragraph("5", table_cell_style), Paragraph("Late Wk 3–4", table_cell_style), Paragraph("Member 6 plugs in Razorpay and notification stubs, then runs full end-to-end passes, logging bugs back to owners.", table_cell_style)],
    [Paragraph("6", table_cell_style), Paragraph("Week 4", table_cell_style), Paragraph("Final rehearsal. Freeze the build a day or two before submission. Record the backup demo video.", table_cell_style)],
]
phase_tbl = Table(phase_data, colWidths=[16 * mm, 22 * mm, 132 * mm])
phase_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_PURPLE_BG]),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(phase_tbl)

story.append(Paragraph("Step 5 — Demo-day setup tip", subheading_style))
story.append(Paragraph(
    "You don't need real cloud deployment for an internal round. Run the backend, AI service, and Postgres via "
    "docker-compose on one laptop (or a shared free-tier cloud VM), expose it with ngrok, and point both the "
    "Flutter app and the Next.js app at that single ngrok URL for the live demo. This sidesteps DevOps work "
    "that isn't the point of the round, while still giving you a genuinely live, working system on stage.",
    body_style
))

doc.build(story)
print("PDF built successfully")
