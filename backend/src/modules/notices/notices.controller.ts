import { Controller, Get, Post, Patch, Body, Param, Query } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { NoticeGeneratorService } from './notice-generator.service';
import { CaseWorkflowService } from '../cases/case-workflow.service';

@ApiTags('Legal Notices & Orders')
@Controller('api/v1')
export class NoticesController {
  private mockNotices: any[] = [
    {
      id: 'NOT-1001',
      caseId: 'CASE-1001',
      inspectionId: 'insp_001',
      businessId: 'biz_001',
      businessName: 'Maharashtrian Pickles & Spices SHG',
      productName: 'Mango Pickle 500g',
      type: 'improvement',
      status: 'issued',
      issuedDate: new Date().toISOString(),
      deadline: new Date(Date.now() + 15 * 86400000).toISOString(),
      daysRemaining: 15,
      sections: [
        {
          id: 'sec_1',
          citation: 'Rule 6(1)(g)',
          title: 'Consumer Care Details Required',
          description: 'Package must bear helpline phone and contact email.',
        },
      ],
      violations: [],
      isAiDraft: true,
      penaltyAmount: 25000.0,
      bodyText: '# IMPROVEMENT NOTICE\n\nNotice Serial: NOT-1001\nIssued To: Maharashtrian Pickles & Spices SHG',
      inspectorRemark: 'Drafted following spot inspection at Pune facility.',
      createdAt: new Date().toISOString(),
    },
  ];

  private mockCases: any[] = [
    {
      id: 'CASE-1001',
      caseNumber: 'CASE-2026-001',
      businessId: 'biz_001',
      businessName: 'Maharashtrian Pickles & Spices SHG',
      status: 'NOTICE_ISSUED',
      noticeType: 'IMPROVEMENT',
      createdAt: new Date().toISOString(),
    },
  ];

  constructor(
    private readonly noticeGenerator: NoticeGeneratorService,
    private readonly workflowService: CaseWorkflowService,
  ) {}

  @Post('notices')
  @ApiOperation({ summary: 'Draft, render bilingual notice text, and issue notice' })
  issueNotice(@Body() body: any) {
    const type = (body.type || 'improvement').toLowerCase() as any;
    const lang = (body.lang || 'en').toLowerCase() as any;

    const issuedDate = new Date();
    const deadlineDate = this.workflowService.calculateDeadline(
      type.toUpperCase(),
      issuedDate,
      body.customDays,
      body.customDeadlineDate,
    );

    const renderedText = this.noticeGenerator.renderNotice(type, lang, {
      NOTICE_ID: `NOT-${Date.now()}`,
      CASE_ID: body.caseId || `CASE-${Date.now()}`,
      BUSINESS_NAME: body.businessName || 'Maharashtrian Pickles & Spices',
      BUSINESS_ADDRESS: body.businessAddress || 'MIDC Industrial Area, Pune',
      INSPECTOR_NAME: body.inspectorName || 'Inspector S. K. Shinde',
      INSPECTOR_ID: body.inspectorId || 'INS-MH-4021',
      INSPECTION_DATE: issuedDate.toISOString().split('T')[0],
      PRODUCT_NAME: body.productName || 'Mango Pickle 500g',
      MANUFACTURER_NAME: body.manufacturerName || 'Maharashtrian Pickles & Spices',
      OBSERVED_VIOLATION: body.observedViolation || 'Missing Consumer Care Helpline details on packaging',
      LEGAL_SECTION: body.legalSection || 'Section 36(1)',
      LEGAL_RULE: body.legalRule || 'Rule 6(1)(g)',
      PENALTY: body.penalty || 'Fine up to Rs. 25,000 under Section 36(1)',
      DEADLINE: deadlineDate.toISOString().split('T')[0],
      DATE: issuedDate.toISOString().split('T')[0],
      PLACE: body.place || 'Pune, Maharashtra',
    });

    const notice = {
      id: `NOT-${Date.now()}`,
      caseId: body.caseId || `CASE-${Date.now()}`,
      inspectionId: body.inspectionId || `insp_${Date.now()}`,
      businessId: body.businessId || 'biz_001',
      businessName: body.businessName || 'Maharashtrian Pickles & Spices SHG',
      productName: body.productName || 'Mango Pickle 500g',
      type: type,
      status: 'issued',
      issuedDate: issuedDate.toISOString(),
      deadline: deadlineDate.toISOString(),
      daysRemaining: this.workflowService.calculateDaysRemaining(deadlineDate),
      sections: [
        {
          id: 'sec_1',
          citation: body.legalRule || 'Rule 6(1)(g)',
          title: 'Mandatory Packaging Declaration',
          description: body.observedViolation || 'Violation of Packaged Commodities Rules',
        },
      ],
      violations: [],
      isAiDraft: true,
      penaltyAmount: 25000.0,
      bodyText: renderedText,
      inspectorRemark: body.remarks || 'Issued by Legal Metrology Officer',
      createdAt: new Date().toISOString(),
    };

    this.mockNotices.push(notice);
    return notice;
  }

  @Get('notices')
  @ApiOperation({ summary: 'List all notices' })
  listNotices() {
    return this.mockNotices;
  }

  @Get('inspector/notices')
  @ApiOperation({ summary: 'List notices assigned to inspector' })
  listInspectorNotices() {
    return this.mockNotices;
  }

  @Get('business/notices')
  @ApiOperation({ summary: 'List notices issued to business' })
  listBusinessNotices() {
    return this.mockNotices;
  }

  @Get('businesses/:id/notices')
  @ApiOperation({ summary: 'List notices issued to a specific business' })
  listNoticesByBusiness(@Param('id') id: string) {
    return this.mockNotices;
  }

  @Get('cases')
  @ApiOperation({ summary: 'List all active compliance cases' })
  listCases(@Query('onlyActive') onlyActive?: boolean) {
    return this.mockCases;
  }

  @Get('notices/:id')
  @ApiOperation({ summary: 'Get details of a specific legal notice' })
  getNoticeDetail(@Param('id') id: string) {
    const notice = this.mockNotices.find((n) => n.id === id);
    if (!notice) return this.mockNotices[0];
    return notice;
  }

  @Patch('notices/:id')
  @ApiOperation({ summary: 'Update notice status' })
  updateNoticeStatus(@Param('id') id: string, @Body() body: { status: string; comments?: string }) {
    const notice = this.mockNotices.find((n) => n.id === id);
    if (notice) {
      notice.status = body.status;
      notice.updatedAt = new Date().toISOString();
    }
    return notice || { id, status: body.status, comments: body.comments };
  }

  @Post('notices/generate')
  @ApiOperation({ summary: 'Generate notice alias endpoint' })
  generateNotice(@Body() body: any) {
    return this.issueNotice(body);
  }

  @Post('notices/:id/sections')
  @ApiOperation({ summary: 'Add section to notice' })
  addSection(@Param('id') id: string, @Body() body: any) {
    const notice = this.getNoticeDetail(id);
    notice.sections = notice.sections || [];
    notice.sections.push({
      id: `sec_${Date.now()}`,
      citation: body.citation || 'Rule 6(1)',
      title: body.title || 'Packaging Requirement',
      description: body.description || '',
    });
    return notice;
  }

  @Post('notices/:id/confirm')
  @ApiOperation({ summary: 'Confirm notice draft by inspector' })
  confirmDraft(@Param('id') id: string, @Body() body: any) {
    const notice = this.getNoticeDetail(id);
    notice.status = 'confirmed';
    if (body.remark) notice.inspectorRemark = body.remark;
    return notice;
  }

  @Post('notices/:id/issue')
  @ApiOperation({ summary: 'Sign and issue notice' })
  signAndIssue(@Param('id') id: string, @Body() body: any) {
    const notice = this.getNoticeDetail(id);
    notice.status = 'issued';
    notice.signedAt = new Date().toISOString();
    notice.signerName = body.signerName || 'Inspector S. K. Shinde';
    return notice;
  }

  @Post('notices/:id/correction')
  @ApiOperation({ summary: 'Submit compliance correction evidence' })
  submitCorrection(@Param('id') id: string, @Body() body: any) {
    const notice = this.getNoticeDetail(id);
    notice.status = 'correctionSubmitted';
    notice.correctionComments = body.comments || 'Corrected packaging image uploaded.';
    return notice;
  }

  @Post('notices/:id/dispute')
  @ApiOperation({ summary: 'Dispute issued notice' })
  submitDispute(@Param('id') id: string, @Body() body: any) {
    const notice = this.getNoticeDetail(id);
    notice.status = 'disputed';
    notice.disputeReason = body.reason;
    notice.disputeComments = body.comments;
    return notice;
  }

  @Post('notices/:id/consent')
  @ApiOperation({ summary: 'Submit compounding consent' })
  submitConsent(@Param('id') id: string, @Body() body: any) {
    const notice = this.getNoticeDetail(id);
    notice.status = 'consentGiven';
    notice.confirmedBy = body.confirmedBy || 'Business Owner';
    return notice;
  }
}
