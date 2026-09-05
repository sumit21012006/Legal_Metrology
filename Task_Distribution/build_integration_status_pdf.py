import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ---------- Colors ----------
NAVY = colors.HexColor("#1B2A4A")
MAIN_BLUE = colors.HexColor("#2C5282")
SMALL_TEAL = colors.HexColor("#0F766E")
PURPLE = colors.HexColor("#553C9A")
LIGHT_BLUE_BG = colors.HexColor("#EAF1F8")
LIGHT_TEAL_BG = colors.HexColor("#E6F4F2")
LIGHT_PURPLE_BG = colors.HexColor("#F1EDFB")
GREY_TEXT = colors.HexColor("#2D3748")
GOLD = colors.HexColor("#B7791F")
DARK_GREEN = colors.HexColor("#22543D")
GREEN_BG = colors.HexColor("#C6F6D5")

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=18, textColor=NAVY, spaceAfter=4, alignment=TA_LEFT
)
subtitle_style = ParagraphStyle(
    "SubtitleStyle", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=11, textColor=MAIN_BLUE, spaceAfter=6
)
intro_style = ParagraphStyle(
    "IntroStyle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9.5, textColor=GREY_TEXT, leading=13.5, spaceAfter=8
)
section_header_style = ParagraphStyle(
    "SectionHeader", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=11.5, textColor=colors.white, leading=14
)
member_title_style = ParagraphStyle(
    "MemberTitle", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=10.5, textColor=NAVY, spaceAfter=2, spaceBefore=4
)
subheading_style = ParagraphStyle(
    "Subheading", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=9.5, textColor=NAVY, spaceBefore=4, spaceAfter=2
)
body_style = ParagraphStyle(
    "BodyStyle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9, textColor=GREY_TEXT, leading=12.5
)
bullet_style = ParagraphStyle(
    "BulletStyle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8.8, textColor=GREY_TEXT, leading=12
)
table_header_style = ParagraphStyle(
    "TableHeader", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=8.5, textColor=colors.white, alignment=TA_CENTER
)
table_cell_style = ParagraphStyle(
    "TableCell", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8, textColor=GREY_TEXT, leading=11
)
table_cell_bold = ParagraphStyle(
    "TableCellBold", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=8, textColor=NAVY, leading=11
)

def section_bar(text, bg_color):
    t = Table([[Paragraph(text, section_header_style)]], colWidths=[175 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm
    )

    story = []

    # Title Banner
    story.append(Paragraph("SIH PS 34 — Legal Metrology Automation", title_style))
    story.append(Paragraph("System Integration Status & Architectural Mapping Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=8))

    story.append(Paragraph(
        "<b>Executive Overview:</b> This report details the current integration status of the system. "
        "The core foundation — consisting of <b>Member 1 (NestJS Backend)</b>, <b>Member 5 (Legal Knowledge Base)</b>, "
        "and <b>Member 3 (Flutter Mobile App)</b> — has been fully connected and verified. The remaining roles "
        "(Members 2, 4, and 6) are architecturally mapped to plug in seamlessly without breaking existing mobile app flows.",
        intro_style
    ))
    story.append(Spacer(1, 4))

    # Section 1: Completed Integrations
    story.append(section_bar("1. COMPLETED INTEGRATIONS — WHO IS CONNECTED & HOW?", MAIN_BLUE))
    story.append(Spacer(1, 6))

    # A: Member 5 -> Member 1
    story.append(Paragraph("A. Member 5 (Legal Knowledge Base) ➔ Member 1 (NestJS Backend)", member_title_style))
    story.append(Paragraph("<b>Status:</b> 100% CONNECTED IN CODE & SEEDED", ParagraphStyle("Done", parent=body_style, fontName="Helvetica-Bold", textColor=DARK_GREEN)))
    story.append(Paragraph(
        "• <b>Legal Rulebook & Penalty Seeder:</b> Member 1's seeder script (<code>backend/src/database/seeders/seed-legal-kb.ts</code>) "
        "directly loads and parses Member 5's <code>rulebook.json</code> (53 KB), <code>penalty_matrix.json</code>, <code>compounding_matrix.json</code>, and <code>exemptions.json</code>.<br/>"
        "• <b>Bilingual Notice Generator:</b> Member 1's notice generator service (<code>backend/src/modules/notices/notice-generator.service.ts</code>) "
        "directly loads Member 5's markdown legal templates (<code>notice_improvement_en.md</code>, <code>notice_seizure_mr.md</code>, etc.) "
        "and dynamically substitutes all 24 legal placeholders (e.g. <code>{{NOTICE_ID}}</code>, <code>{{BUSINESS_NAME}}</code>, <code>{{OBSERVED_VIOLATION}}</code>, <code>{{DEADLINE}}</code>).",
        bullet_style
    ))
    story.append(Spacer(1, 6))

    # B: Member 1 -> Member 3
    story.append(Paragraph("B. Member 1 (NestJS Backend) ➔ Member 3 (Flutter Mobile App)", member_title_style))
    story.append(Paragraph("<b>Status:</b> 100% CONNECTED VIA REST REPOSITORIES & DUAL MODE", ParagraphStyle("Done", parent=body_style, fontName="Helvetica-Bold", textColor=DARK_GREEN)))
    story.append(Paragraph(
        "• <b>Single Base URL Gateway:</b> Flutter <code>ApiClient</code> (<code>lib/core/network/api_client.dart</code>) attaches Keycloak JWT "
        "<code>Bearer &lt;token&gt;</code> headers to every HTTP request. Isolated token refresh prevents infinite 401 interceptor loops.<br/>"
        "• <b>Live Repository Mappers:</b> Flutter <code>RealXxxRepository</code> classes (<code>lib/data/real/real_repositories.dart</code>) target Member 1's NestJS routes "
        "(<code>/auth/login</code>, <code>/businesses</code>, <code>/inspections</code>, <code>/notices</code>, <code>/payments</code>, <code>/self-check</code>, <code>/offences</code>).<br/>"
        "• <b>Dual Mode Architecture:</b> Runs in <b>Demo Mode</b> (<code>USE_MOCK_DATA=true</code>) on-device standalone, or flips to <b>Live Mode</b> (<code>USE_MOCK_DATA=false</code>) "
        "with zero UI code changes.",
        bullet_style
    ))
    story.append(Spacer(1, 6))

    # C: Member 3 Internal Fixes
    story.append(Paragraph("C. Member 3 (Mobile App) State Sync & Rule Alignment", member_title_style))
    story.append(Paragraph("<b>Status:</b> VERIFIED & TESTED (8/8 TESTS PASSED)", ParagraphStyle("Done", parent=body_style, fontName="Helvetica-Bold", textColor=DARK_GREEN)))
    story.append(Paragraph(
        "• <b>Violation Propagation:</b> Connected <code>ViolationsStep</code> state to <code>InspectionFlowScreen</code>. Confirmed violations now properly flow into <code>NoticeStep</code> for AI notice generation.<br/>"
        "• <b>Flutter 3.32/3.33 Deprecations:</b> Replaced deprecated <code>DropdownButtonFormField.value</code> with <code>initialValue</code> and cleaned up static analysis warnings across all screens.",
        bullet_style
    ))
    story.append(Spacer(1, 8))

    # Section 2: Remaining Tasks & Integration Wiring Plan
    story.append(section_bar("2. REMAINING TASKS & FUTURE INTEGRATION WIRING PLAN", PURPLE))
    story.append(Spacer(1, 6))

    # Member 2
    story.append(Paragraph("A. Member 2: AI/OCR + NLP Engineer (FastAPI Service)", member_title_style))
    story.append(Paragraph("<b>Remaining Deliverable:</b> FastAPI endpoints for <code>/ocr/scan</code>, <code>/ocr/self-check</code>, and <code>/notices/generate</code>.", bullet_style))
    story.append(Paragraph("<b>Integration Protocol:</b> Member 1's NestJS backend calls FastAPI internally. The Mobile App calls NestJS — <b>zero mobile app changes required</b> when Member 2 deploys!", bullet_style))
    story.append(Spacer(1, 4))

    # Member 4
    story.append(Paragraph("B. Member 4: Web Frontend Developer (Next.js — Citizen + Controller)", member_title_style))
    story.append(Paragraph("<b>Remaining Deliverable:</b> Citizen complaint filing form & Controller regional analytics/compounding approval web app.", bullet_style))
    story.append(Paragraph("<b>Integration Protocol:</b> Next.js app communicates with Member 1's NestJS backend. When Controller assigns inspections or approves notices on Web, updates sync in PostgreSQL and reflect in the Flutter Mobile App.", bullet_style))
    story.append(Spacer(1, 4))

    # Member 6
    story.append(Paragraph("C. Member 6: Integrations, QA & Presentation Owner (Razorpay & End-to-End QA)", member_title_style))
    story.append(Paragraph("<b>Remaining Deliverable:</b> Razorpay sandbox keys, <code>/payments/webhook</code> verification, end-to-end QA, and pitch deck.", bullet_style))
    story.append(Paragraph("<b>Integration Protocol:</b> Mobile App payment screen initiates Razorpay order via Member 1; Webhook updates payment status in PostgreSQL.", bullet_style))
    story.append(Spacer(1, 8))

    # Section 3: Summary Table
    story.append(section_bar("3. SYSTEM INTEGRATION MATRIX SUMMARY", SMALL_TEAL))
    story.append(Spacer(1, 6))

    table_data = [
        [
            Paragraph("Member / Role", table_header_style),
            Paragraph("Status", table_header_style),
            Paragraph("Connected To", table_header_style),
            Paragraph("Integration Method", table_header_style),
        ],
        [
            Paragraph("<b>Member 1</b><br/>Backend & DB Architect", table_cell_bold),
            Paragraph("<font color='#22543D'><b>COMPLETED</b></font>", table_cell_style),
            Paragraph("Member 5 (KB)<br/>Member 3 (Mobile)", table_cell_style),
            Paragraph("Prisma PostgreSQL, Keycloak JWT, File Seeder, REST Controllers", table_cell_style),
        ],
        [
            Paragraph("<b>Member 5</b><br/>Legal KB Maker", table_cell_bold),
            Paragraph("<font color='#22543D'><b>COMPLETED</b></font>", table_cell_style),
            Paragraph("Member 1 (Backend)", table_cell_style),
            Paragraph("Structured JSON Rulebook, CSV Penalty Matrix, Bilingual Markdown Templates", table_cell_style),
        ],
        [
            Paragraph("<b>Member 3</b><br/>Mobile App (Flutter)", table_cell_bold),
            Paragraph("<font color='#22543D'><b>COMPLETED</b></font>", table_cell_style),
            Paragraph("Member 1 (Backend)", table_cell_style),
            Paragraph("Riverpod, Dio REST Repositories, Dual Mock/Real Switch, Signature Pad", table_cell_style),
        ],
        [
            Paragraph("<b>Member 2</b><br/>AI/OCR + NLP Engineer", table_cell_bold),
            Paragraph("<font color='#B7791F'><b>IN PROGRESS</b></font>", table_cell_style),
            Paragraph("Member 1 (Backend)", table_cell_style),
            Paragraph("FastAPI internal proxy called by NestJS (Zero Mobile UI changes)", table_cell_style),
        ],
        [
            Paragraph("<b>Member 4</b><br/>Web Frontend (Next.js)", table_cell_bold),
            Paragraph("<font color='#B7791F'><b>IN PROGRESS</b></font>", table_cell_style),
            Paragraph("Member 1 (Backend)", table_cell_style),
            Paragraph("REST endpoints for Citizen complaints & Controller compounding approvals", table_cell_style),
        ],
        [
            Paragraph("<b>Member 6</b><br/>Integrations & QA", table_cell_bold),
            Paragraph("<font color='#B7791F'><b>IN PROGRESS</b></font>", table_cell_style),
            Paragraph("Member 1 (Backend)<br/>Member 3 (Mobile)", table_cell_style),
            Paragraph("Razorpay checkout SDK & NestJS <code>/payments/webhook</code>", table_cell_style),
        ],
    ]

    t_summary = Table(table_data, colWidths=[40 * mm, 25 * mm, 38 * mm, 72 * mm])
    t_summary.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BLUE_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_summary)

    doc.build(story)
    print(f"Successfully generated PDF: {filename}")

if __name__ == "__main__":
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "integration-status-report.pdf")
    build_pdf(pdf_path)
