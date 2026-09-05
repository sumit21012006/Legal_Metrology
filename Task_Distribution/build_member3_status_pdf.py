# Generates: member3-flutter-status-report.pdf
# Brief summary of completed / remaining tasks for the Flutter mobile app (Member 3)
# and the integration plan with Members 1-6. Style matches build_detailed_pdf.py.

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    ListFlowable, ListItem, HRFlowable,
)
from reportlab.lib.enums import TA_LEFT

# ---------- Colors (match team's build_detailed_pdf.py) ----------
NAVY = colors.HexColor("#1B2A4A")
MAIN_BLUE = colors.HexColor("#2C5282")
SMALL_TEAL = colors.HexColor("#0F766E")
PURPLE = colors.HexColor("#553C9A")
LIGHT_BLUE_BG = colors.HexColor("#EAF1F8")
LIGHT_TEAL_BG = colors.HexColor("#E6F4F2")
LIGHT_PURPLE_BG = colors.HexColor("#F1EDFB")
LIGHT_AMBER_BG = colors.HexColor("#FFF7E6")
GREY_TEXT = colors.HexColor("#3A3A3A")
GOLD = colors.HexColor("#B7791F")
GREEN = colors.HexColor("#1B7F5A")

styles = getSampleStyleSheet()

title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold",
                             fontSize=18, textColor=NAVY, spaceAfter=3, alignment=TA_LEFT)
subtitle_style = ParagraphStyle("SubtitleStyle", parent=styles["Normal"], fontName="Helvetica",
                                fontSize=10.5, textColor=GREY_TEXT, spaceAfter=2)
intro_style = ParagraphStyle("IntroStyle", parent=styles["Normal"], fontName="Helvetica",
                             fontSize=9.5, textColor=GREY_TEXT, leading=13.5, spaceAfter=8)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=13, textColor=MAIN_BLUE, spaceBefore=12, spaceAfter=5)
h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Helvetica-Bold",
                    fontSize=10.8, textColor=NAVY, spaceBefore=8, spaceAfter=3)
body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=9.3,
                      textColor=GREY_TEXT, leading=13)
bullet = ParagraphStyle("Bullet", parent=body, leftIndent=10)
small = ParagraphStyle("Small", parent=body, fontSize=8.3, leading=11.5)
status_done = ParagraphStyle("StatusDone", parent=body, textColor=GREEN, fontSize=9)
status_open = ParagraphStyle("StatusOpen", parent=body, textColor=GOLD, fontSize=9)

# ---------- Document ----------
doc = SimpleDocTemplate(
    "member3-flutter-status-report.pdf",
    pagesize=A4,
    leftMargin=16 * mm, rightMargin=16 * mm,
    topMargin=14 * mm, bottomMargin=14 * mm,
    title="Member 3 - Flutter App Status Report",
    author="Member 3 (Flutter)",
)

story = []

# ---------- Header ----------
story.append(Paragraph("Legal Metrology — Member 3 Status Report", title_style))
story.append(Paragraph("Flutter Android App (Inspector + Business) · Smart India Hackathon 2026", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.2, color=MAIN_BLUE, spaceBefore=4, spaceAfter=10))

# ---------- Summary box ----------
summary_data = [[
    Paragraph("<b>DELIVERABLE</b><br/>Flutter APK — Inspector + "
              "Business/Retailer roles, fully working in Demo Mode "
              "(mock backend).<br/><br/>"
              "<b>STATUS</b><br/>"
              '<font color="#1B7F5A"><b>100% of the Flutter app build is '
              'complete</b></font> — analyze 0 errors, 8/8 tests passing, '
              "debug APK builds. Remaining work is <b>integration</b>, not "
              "app development.", body),
]]
summary_tbl = Table(summary_data, colWidths=[178 * mm])
summary_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE_BG),
    ("BOX", (0, 0), (-1, -1), 0.8, MAIN_BLUE),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(summary_tbl)
story.append(Spacer(1, 6))

story.append(Paragraph(
    "Location: <b>E:\\SIH_2026\\Legal_Metrology\\mobile_app</b> (inside the team GitHub repo, "
    "own .gitignore so build artifacts stay out of team commits). "
    "Stack: Flutter 3.44 / Dart 3.12, Riverpod, go_router, Dio, flutter_secure_storage, "
    "camera + image_picker, signature pad. Material 3 light GovTech theme.", intro_style))

# ---------- 1. Completed ----------
story.append(Paragraph("1. Completed — App Foundation", h2))
story.append(ListFlowable([
    ListItem(Paragraph("Complete project scaffold: pubspec, Android config (minSdk 23, "
                       "compileSdk 36, camera permissions), Material 3 light GovTech theme.", bullet)),
    ListItem(Paragraph("Clean architecture: UI → controllers → repository interfaces → "
                       "Mock/Real implementations. UI never imports mock data or Dio directly.", bullet)),
    ListItem(Paragraph("13 domain models mapped to the shared PostgreSQL entities "
                       "(users, businesses, products, inspections, evidence, ocr_results, "
                       "violations, notices, cases, payments, supply chain…).", bullet)),
    ListItem(Paragraph("11 repository interfaces = the API contract for Member 1 "
                       "(auth, business, inspection, evidence, OCR, violation, offence, "
                       "notice, seizure+case, self-check, payment, supply chain).", bullet)),
    ListItem(Paragraph("Typed error layer — every failure surfaces a friendly message with "
                       "Retry (401/403/404/timeout/offline/upload/OCR/notice/payment). "
                       "No stack traces ever reach the UI.", bullet)),
    ListItem(Paragraph("Auth: secure token storage (Keystore), JWT bearer interceptor with "
                       "single-attempt refresh on 401, session restore at splash, role-based "
                       "route guards + unauthorized screen. Inspector self-registration is "
                       "impossible by design.", bullet)),
], bulletType="bullet", start="•", leftIndent=14))
story.append(Spacer(1, 4))

story.append(Paragraph("2. Completed — Inspector App (Enforcement Flow)", h2))
story.append(ListFlowable([
    ListItem(Paragraph("<b>Dashboard</b> — assigned inspections, active cases, draft notices, "
                       "pending actions, quick actions, today's inspections.", bullet)),
    ListItem(Paragraph("<b>Business search</b> — name/GSTIN/owner/city; Start Inspection sheet "
                       "(Routine / Complaint-Based / Supply-Chain-Linked + complaint ID).", bullet)),
    ListItem(Paragraph("<b>8-step guided inspection flow:</b> multi-angle evidence capture "
                       "(front/back/side slots, retake/delete/preview) → 5-stage OCR pipeline UI "
                       "with retry → fully editable OCR review (add/remove/correct fields, "
                       "confidence chips) → AI violation review (Accept/Reject/Edit + manual Add, "
                       "POTENTIAL→confirmed human-in-the-loop) → previous product offence history "
                       "(tier badge, case records) → observations + supplier declaration + "
                       "seizure/sample with witnesses → notice generation & review (AI-DRAFT banner, "
                       "editable body, add sections from Legal-KB library) → signature pad → issue.", bullet)),
    ListItem(Paragraph("<b>Case timeline</b> — visual done/current/pending states with actors "
                       "and details; only backend-returned states rendered.", bullet)),
], bulletType="bullet", start="•", leftIndent=14))
story.append(Spacer(1, 4))

story.append(Paragraph("3. Completed — Business App (Prevention Flow)", h2))
story.append(ListFlowable([
    ListItem(Paragraph("<b>Dashboard</b> — PREVENTIVE COMPLIANCE hero (\"Check your packaging "
                       "before you sell\"), stats, quick actions, private-data banner.", bullet)),
    ListItem(Paragraph("<b>Private self-check</b> — capture package photos, pipeline progress, "
                       "COMPLIANT / POTENTIAL ISSUES result with plain-language requirement + "
                       "recommended correction per issue. Clearly labelled PRIVATE throughout.", bullet)),
    ListItem(Paragraph("<b>Self-check history</b> — private reports with result chips.", bullet)),
    ListItem(Paragraph("<b>Notice inbox + detail</b> — status-gated actions: Submit Correction "
                       "(photos + comments), Raise Dispute, Give Consent (explicit confirm), "
                       "Pay Penalty.", bullet)),
    ListItem(Paragraph("<b>Case tracking</b> — Inspection → Notice → Response → Correction → "
                       "Compounding → Payment → Closure timeline.", bullet)),
    ListItem(Paragraph("<b>Payments</b> — pending + history, ₹ en_IN formatting, backend-verified "
                       "status polling (app never marks success locally).", bullet)),
], bulletType="bullet", start="•", leftIndent=14))
story.append(Spacer(1, 4))

story.append(Paragraph("4. Completed — Demo Mode & Quality", h2))
story.append(ListFlowable([
    ListItem(Paragraph("Stateful MockBackend simulating NestJS + FastAPI: realistic Indian seed "
                       "data, RBAC, latency, staged OCR with small failure rate, notice/payment "
                       "status lifecycles — the full judge demo runs with zero backend.", bullet)),
    ListItem(Paragraph("Demo Mode ON/OFF via one flag or dart-defines; per-capability migration "
                       "(REAL_AUTH / REAL_OCR) supported.", bullet)),
    ListItem(Paragraph("Demo credentials: inspector rajesh.deshmukh / inspector123 · "
                       "business anita@abctraders.in / business123.", bullet)),
    ListItem(Paragraph("Reusable widget library (25+ components), loading/error/empty states "
                       "everywhere, 8/8 automated tests passing, flutter analyze 0 errors/0 warnings.", bullet)),
], bulletType="bullet", start="•", leftIndent=14))
story.append(Spacer(1, 6))

# ---------- 5. Remaining ----------
story.append(Paragraph("5. Remaining (Integration-Phase Work)", h2))

remaining_rows = [
    [Paragraph("<b>Task</b>", body), Paragraph("<b>Blocked on</b>", body),
     Paragraph("<b>Owner</b>", body)],
    [Paragraph("Swap Mock Auth → Keycloak OIDC via NestJS", body), Paragraph("Keycloak config + final auth endpoints", body), Paragraph("Member 1", body)],
    [Paragraph("Swap all Mock repos → real NestJS API routes + JSON casing", body), Paragraph("Final REST contract", body), Paragraph("Member 1", body)],
    [Paragraph("Point OCR flow at FastAPI passthrough (job polling)", body), Paragraph("OCR response schema freeze", body), Paragraph("Members 1 + 4", body)],
    [Paragraph("Wire Legal-KB section library API (replace 8 mock sections)", body), Paragraph("Sections API / rule mappings", body), Paragraph("Member 5", body)],
    [Paragraph("eMudhra signature implementation behind SignatureService", body), Paragraph("DSC/eSign integration spec", body), Paragraph("Member 6", body)],
    [Paragraph("Razorpay checkout sheet + order/webhook flow", body), Paragraph("Payment initiate response shape", body), Paragraph("Members 1 + 6", body)],
    [Paragraph("file_picker for document attachments (invoices/dispute docs)", body), Paragraph("Live backend for uploads", body), Paragraph("Member 3 (me)", body)],
    [Paragraph("Offline capture queue (future scope, architecture already allows)", body), Paragraph("Post-integration", body), Paragraph("Member 3 (me)", body)],
]
remaining_tbl = Table(remaining_rows, colWidths=[92 * mm, 56 * mm, 30 * mm])
remaining_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE_BG),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B9C6D6")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(remaining_tbl)
story.append(Spacer(1, 6))

# ---------- 6. Integration plan ----------
story.append(Paragraph("6. How to Integrate With Each Teammate", h2))

def member_block(title, color, bg, lines):
    rows = [[Paragraph(title, ParagraphStyle("mt", parent=body, textColor=color, fontSize=9.6))]]
    rows += [[Paragraph(l, small)] for l in lines]
    t = Table(rows, colWidths=[178 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), bg),
        ("BACKGROUND", (0, 1), (0, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.7, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

story.append(member_block(
    "MEMBER 1 — NestJS + PostgreSQL (Integration Owner)", MAIN_BLUE, LIGHT_BLUE_BG,
    ["<b>They give me:</b> final REST endpoints + JSON schemas, Keycloak realm config, "
     "role claims in JWT, multipart upload contract, ID generation server-side.",
     "<b>I give them:</b> the repo file <b>mobile_app/lib/repositories/*</b> — these interfaces "
     "ARE the contract (11 capability groups). Also mobile_app/DEVELOPMENT_REPORT.md §G "
     "lists every expected route.",
     "<b>Integration steps:</b> (1) share endpoint list → I update only "
     "mobile_app/lib/data/real/real_repositories.dart; (2) they stand up a dev server → "
     "I run the app with --dart-define=API_BASE_URL=http://&lt;host&gt;:3000/api/v1; "
     "(3) migrate capability-by-capability: --dart-define=REAL_AUTH=true first, then the rest; "
     "(4) joint test of 401/403 paths + token refresh.",
     "<b>Rule:</b> Flutter NEVER talks to PostgreSQL directly — all data via their API."]))
story.append(Spacer(1, 5))

story.append(member_block(
    "MEMBER 2 — Next.js Web (Controller + Citizen)", SMALL_TEAL, LIGHT_TEAL_BG,
    ["<b>No direct integration</b> — our apps meet only inside PostgreSQL via NestJS.",
     "<b>Shared-state points to verify together in a joint demo:</b> "
     "Controller assigns inspection → appears in my Inspector app; Citizen complaint → "
     "complaint-based inspection appears with complaint ID; I issue notice → it must render "
     "on their Controller console; business pays → closure shows on Controller web.",
     "<b>Agreement needed:</b> common case/inspection/notice ID formats so every screen "
     "shows the same identifiers (my mocks already use INSP-2026-xxxxx / LM/2026/xxxx / "
     "NOT-xxxxxx — confirm or replace)."]))
story.append(Spacer(1, 5))

story.append(member_block(
    "MEMBER 4 — FastAPI AI (OCR / NER / Compliance / NLP)", PURPLE, LIGHT_PURPLE_BG,
    ["<b>They give me (through Member 1's passthrough, never directly):</b> "
     "OCR job envelope (jobId, status, progressStep, failureReason), "
     "fields[] with keys PRODUCT_NAME, GENERIC_NAME, MANUFACTURER, PACKER, IMPORTER, "
     "NET_QUANTITY, MRP, MANUFACTURING_DATE, EXPIRY_USE_BY, COUNTRY_OF_ORIGIN, "
     "CONSUMER_CARE, BATCH_LOT, OTHER — each with value + confidence (0-1) + isMissing; "
     "violations[] (type, description, severity, status=POTENTIAL, confidence, "
     "ruleSection, ruleTitle, recommendation); self-check issues in plain business language; "
     "offence lookup (matchedProductName, tier, matchConfidence, records[]).",
     "<b>I give them:</b> multi-image JPEG uploads (front/back/side), editable-field "
     "confirmations so corrections can feed their feedback loop, human-in-the-loop "
     "guarantee (AI never finalises — their POTENTIAL status is preserved in UI).",
     "<b>Full field spec:</b> mobile_app/DEVELOPMENT_REPORT.md §H."]))
story.append(Spacer(1, 5))

story.append(member_block(
    "MEMBER 5 — Legal Knowledge Base", GOLD, LIGHT_AMBER_BG,
    ["<b>They give me:</b> sections as {id, citation, title, description} — e.g. "
     "\"Rule 6(3), LM (Packaged Commodities) Rules, 2011\"; violation→section mappings; "
     "compounding amounts by offence tier; notice-period defaults for panchanama/seizure.",
     "<b>I give them:</b> the NoticeSection model my UI consumes "
     "(mock ships 8 representative sections in mobile_app/lib/data/mock_data.dart — "
     "their API output should match that shape).",
     "<b>Used at:</b> Add-Violation section picker, notice draft sections + Add Section, "
     "and self-check REQUIREMENT text."]))
story.append(Spacer(1, 5))

story.append(member_block(
    "MEMBER 6 — Razorpay / eMudhra / WhatsApp / Email / GST", SMALL_TEAL, LIGHT_TEAL_BG,
    ["<b>Razorpay:</b> my initiatePayment call must receive {paymentId, orderId, amount, "
     "currency, note} to open checkout; status polled via getPaymentStatus; webhook on "
     "their side is the ONLY success source — my UI explicitly never marks success locally. "
     "I need their checkout key/flow decision (SDK vs backend-hosted page).",
     "<b>eMudhra:</b> implement my SignatureService interface "
     "(mobile_app/lib/services/signature_service.dart) with DSC/eSign; "
     "verifyDigitalSignature() already exists as the hook. Drawn-signature prototype "
     "is clearly labelled as not legally valid.",
     "<b>WhatsApp/Email:</b> no app work needed — notice delivery notifications fire "
     "server-side after I POST the signed notice.",
     "<b>GSTIN verification:</b> registration flow already routes through backend; "
     "I display pending-verification status they set."]))
story.append(Spacer(1, 6))

# ---------- 7. This week ----------
story.append(Paragraph("7. Proposed Joint Timeline (Next 2 Weeks)", h2))
story.append(ListFlowable([
    ListItem(Paragraph("<b>Week 1:</b> Member 1 finalises auth + 3 core endpoints "
                       "(businesses search, inspections, evidence upload) → I integrate real auth "
                       "and those flows; joint smoke test on a real device.", status_done)),
    ListItem(Paragraph("<b>Week 1:</b> Member 4 freezes OCR JSON schema → I wire REAL_OCR and "
                       "test with real package photos.", status_done)),
    ListItem(Paragraph("<b>Week 2:</b> notices/violations/self-check endpoints; Member 6 "
                       "payment initiate response → Razorpay checkout wired; end-to-end demo "
                       "rehearsal: complaint → inspection → OCR → confirm → notice → business "
                       "response → compounding → payment → closure across all four apps.", status_done)),
], bulletType="bullet", start="•", leftIndent=14))

story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=0.8, color=MAIN_BLUE, spaceBefore=2, spaceAfter=5))
story.append(Paragraph(
    "Hand-off docs in the repo: mobile_app/README.md (run + demo-mode guide) · "
    "mobile_app/DEVELOPMENT_REPORT.md (full integration report §G–N). "
    "App verified: flutter analyze 0 errors · 8/8 tests · debug APK builds.",
    small))

doc.build(story)
print("Generated member3-flutter-status-report.pdf")
