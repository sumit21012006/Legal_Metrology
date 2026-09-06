import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#4B5563"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "SIH PS 34 — Legal Metrology Backend & Integration Specification")
            self.setStrokeColor(colors.HexColor("#E5E7EB"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, footer_text)
        self.drawString(54, 36, "CONFIDENTIAL — Member 1 Technical Deliverable")
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * 72 - 54, 48)
        self.restoreState()

def build_pdf():
    pdf_path = r"c:\Users\NICE\Documents\SIH\Legal_Metrology\Task_Distribution\backend_integration_guide.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#111827'),
        backColor=colors.HexColor('#F3F4F6'),
        spaceAfter=4
    )

    story = []

    # Title Banner
    story.append(Paragraph("Automated Legal Metrology Compliance & Enforcement System", subtitle_style))
    story.append(Paragraph("Backend Architecture, Completed Work & Integration Guide", title_style))
    story.append(Paragraph("<b>Author:</b> Member 1 (Backend & Database Architect) &nbsp;|&nbsp; <b>SIH Problem Statement 34</b> &nbsp;|&nbsp; <b>Version:</b> 1.0.0", body_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=15))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary of Completed Work", h1_style))
    story.append(Paragraph(
        "Member 1 has built, compiled, verified, and committed the entire NestJS API Gateway, Multi-Database Layer, "
        "and Business Logic Engines into the <code>backend/</code> codebase. All 13 sub-part commits have been pushed to GitHub.",
        body_style
    ))

    overview_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Status / Access</b>", body_style)],
        [Paragraph("API Gateway & Backend", body_style), Paragraph("NestJS + TypeScript", body_style), Paragraph("Live at <code>http://localhost:3000/api/docs</code>", body_style)],
        [Paragraph("Relational Database", body_style), Paragraph("PostgreSQL + Prisma ORM", body_style), Paragraph("12 Models defined (Users, Notices, Payments, etc.)", body_style)],
        [Paragraph("Graph Database", body_style), Paragraph("Neo4j", body_style), Paragraph("Retailer &rarr; Distributor &rarr; Manufacturer Traceability", body_style)],
        [Paragraph("Object Storage", body_style), Paragraph("MinIO / AWS S3 SDK", body_style), Paragraph("Presigned URLs for Images, Evidence & PDFs", body_style)],
        [Paragraph("Auth & RBAC", body_style), Paragraph("JWT + Keycloak Guards", body_style), Paragraph("4 Roles (Citizen, Business, Inspector, Controller)", body_style)],
        [Paragraph("Real-Time WebSockets", body_style), Paragraph("Socket.IO Gateway", body_style), Paragraph("Live status push updates for complaints", body_style)],
    ]

    t_overview = Table(overview_data, colWidths=[130, 140, 230])
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EFF6FF')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DBEAFE')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 10))

    # Business Logic Engines Summary
    story.append(Paragraph("2. Core Business Logic Engines Implemented", h1_style))
    story.append(Paragraph("• <b>Case Workflow State Machine:</b> Enforces transitions <code>RECEIVED &rarr; ASSIGNED &rarr; INSPECTED &rarr; NOTICE_ISSUED &rarr; COMPOUNDED/PROSECUTION &rarr; RESOLVED</code> with <i>inspector-configurable custom deadline days/dates</i>.", body_style))
    story.append(Paragraph("• <b>Repeat Offender Calculator:</b> Normalizes product and manufacturer names to automatically assign 1st, 2nd, or 3rd offence statutory fine bounds.", body_style))
    story.append(Paragraph("• <b>Dynamic Notice Renderer:</b> Substitutes 24 legal placeholders across 4 notice types (Improvement, Seizure, Panchanama, Compounded) in English & Marathi.", body_style))
    story.append(Paragraph("• <b>Anti-Corruption Audit Logger:</b> Creates an append-only, tamper-evident SHA-256 hash log for every status change and officer action.", body_style))
    story.append(Paragraph("• <b>Payments Service:</b> Integrates Razorpay with duplicate webhook event protection using <code>razorpay_event_id</code>.", body_style))

    story.append(Spacer(1, 10))

    # Independent Endpoints Table
    story.append(Paragraph("3. Independent REST Endpoints (Available Right Now for Frontends)", h1_style))
    story.append(Paragraph("These endpoints are fully functional and do not depend on external AI services. Frontend developers (Member 3 & Member 4) can build against them immediately:", body_style))

    indep_data = [
        [Paragraph("<b>Endpoint / Method</b>", body_style), Paragraph("<b>Target Role</b>", body_style), Paragraph("<b>Description / Usage</b>", body_style)],
        [Paragraph("<code>POST /api/v1/auth/login</code><br/><code>POST /api/v1/auth/register</code>", body_style), Paragraph("All Users", body_style), Paragraph("User signup & JWT authentication", body_style)],
        [Paragraph("<code>GET /api/v1/knowledge-base/rulebook</code><br/><code>GET /penalties</code>", body_style), Paragraph("All Users", body_style), Paragraph("Query statutory rulebook, penalty matrix, and exemptions", body_style)],
        [Paragraph("<code>POST /api/v1/complaints</code><br/><code>GET /complaints/:id/status</code>", body_style), Paragraph("Citizen / Inspector", body_style), Paragraph("File complaint & get step-by-step status tracker", body_style)],
        [Paragraph("<code>POST /api/v1/businesses</code><br/><code>GET /businesses</code>", body_style), Paragraph("Business / Inspector", body_style), Paragraph("Register business & autocomplete business search", body_style)],
        [Paragraph("<code>GET /api/v1/offences/history</code>", body_style), Paragraph("Inspector", body_style), Paragraph("Query offence history by product & manufacturer", body_style)],
        [Paragraph("<code>GET /api/v1/controller/dashboard/stats</code>", body_style), Paragraph("Controller", body_style), Paragraph("Statewide analytics, 1st vs 2nd offence counts, case load", body_style)],
        [Paragraph("<code>POST /api/v1/controller/compounding/:id/action</code>", body_style), Paragraph("Controller", body_style), Paragraph("Approve, Reject (+comments), or Escalate to Prosecution", body_style)],
        [Paragraph("<code>POST /api/v1/controller/supply-chain/multi-tier</code><br/><code>GET /supply-chain/trace/:gstin</code>", body_style), Paragraph("Controller", body_style), Paragraph("Link & trace Retailer &rarr; Distributor &rarr; Manufacturer graph in Neo4j", body_style)],
        [Paragraph("<code>POST /api/v1/payments/initiate</code>", body_style), Paragraph("Business", body_style), Paragraph("Create Razorpay payment order for notice fines", body_style)],
    ]

    t_indep = Table(indep_data, colWidths=[160, 90, 250])
    t_indep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#DCFCE7')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#86EFAC')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_indep)

    story.append(Spacer(1, 10))

    # Dependent Endpoints Table
    story.append(Paragraph("4. Dependent Endpoints (Interacts with Member 2 AI/OCR & Razorpay)", h1_style))
    story.append(Paragraph("These endpoints interact with Member 2's Python FastAPI AI service or Razorpay payment webhooks:", body_style))

    dep_data = [
        [Paragraph("<b>Endpoint / Method</b>", body_style), Paragraph("<b>Dependent On</b>", body_style), Paragraph("<b>Description & Contract</b>", body_style)],
        [Paragraph("<code>POST /api/v1/inspections/:id/ocr-result</code>", body_style), Paragraph("Member 2<br/>(FastAPI <code>/ocr/scan</code>)", body_style), Paragraph("Backend receives packaging scans, calls FastAPI OCR, saves JSON in DB, returns editable fields to Inspector App.", body_style)],
        [Paragraph("<code>POST /api/v1/businesses/self-check</code>", body_style), Paragraph("Member 2<br/>(FastAPI <code>/ocr/self-check</code>)", body_style), Paragraph("Private self-check. Backend proxies images to FastAPI, saves report in private table isolated from inspectors.", body_style)],
        [Paragraph("<code>POST /api/v1/notices</code>", body_style), Paragraph("Member 2<br/>(FastAPI <code>/notices/generate</code>)", body_style), Paragraph("Calls FastAPI NLP notice text generator, populates 24 placeholders across EN/MR templates, exports PDF to MinIO.", body_style)],
        [Paragraph("<code>POST /api/v1/payments/webhook</code>", body_style), Paragraph("Member 6 & Razorpay", body_style), Paragraph("Razorpay payment webhook callback. Deduplicates using <code>razorpay_event_id</code>, updates payment to PAID, resolves case.", body_style)],
    ]

    t_dep = Table(dep_data, colWidths=[160, 110, 230])
    t_dep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FEF3C7')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#FDE047')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_dep)

    story.append(Spacer(1, 10))

    # Action Items & Integration Steps for Team Members
    story.append(Paragraph("5. Member-by-Member Integration Guide", h1_style))
    story.append(Paragraph("<b>Member 2 (AI/OCR Engineer):</b> Expose FastAPI endpoints at <code>/ocr/scan</code>, <code>/ocr/self-check</code>, and <code>/notices/generate</code> adhering to JSON schemas in <code>RULE_ENGINE_CONTRACT.md</code>.", body_style))
    story.append(Paragraph("<b>Member 3 (Flutter Mobile App):</b> Connect Inspector & Business screens to <code>http://localhost:3000/api/v1/</code>. Refer to Swagger UI at <code>http://localhost:3000/api/docs</code>.", body_style))
    story.append(Paragraph("<b>Member 4 (Next.js Web Developer):</b> Connect Citizen Complaint & Controller Dashboard screens to backend REST APIs. Render Neo4j graph using <code>GET /controller/supply-chain/trace/:gstin</code>.", body_style))
    story.append(Paragraph("<b>Member 6 (Integrations & QA Owner):</b> Use Razorpay test keys with <code>POST /payments/initiate</code> and test webhook callbacks with <code>POST /payments/webhook</code>.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
