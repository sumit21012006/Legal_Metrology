import { Controller, Get, Post, Patch, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { NoticeGeneratorService } from './notice-generator.service';
import { CaseWorkflowService } from '../cases/case-workflow.service';

@ApiTags('Legal Notices & Orders')
@Controller('api/v1')
export class NoticesController {
  private mockNotices: any[] = [
    {
      id: 'NOT-2026-001',
      caseId: 'CASE-2026-001',
      inspectionId: 'insp_001',
      businessId: 'biz_001',
      businessName: 'Maharashtrian Pickles & Spices SHG',
      productName: 'Mango Pickle 500g',
      type: 'improvement',
      status: 'draft',
      issuedDate: new Date(Date.now() - 2 * 86400000).toISOString(),
      deadline: new Date(Date.now() + 13 * 86400000).toISOString(),
      penaltyAmount: 5000,
      bodyText: 'Improvement Notice: Mandated contact details missing on packaging under Rule 6(1)(g).',
      sections: [
        { id: 'SEC-1', citation: 'Rule 6(1)(g)', title: 'Consumer Care Helpline Details', description: 'Mandatory helpline phone or email required.' },
      ],
      violations: [
        { id: 'VIOL-001', fieldKey: 'consumerCare', issue: 'Missing helpline details', actSection: 'Rule 6(1)(g)', ruleText: 'Mandatory declaration missing' },
      ],
      isAiDraft: true,
      createdAt: new Date(Date.now() - 2 * 86400000),
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
    const customDays = body.customDays;
    const customDeadlineDate = body.customDeadlineDate;

    const issuedDate = new Date();
    const deadlineDate = this.workflowService.calculateDeadline(
      type.toUpperCase(),
      issuedDate,
      customDays,
      customDeadlineDate,
    );

    const renderedText = this.noticeGenerator.renderNotice(type, lang, {
      NOTICE_ID: `NOT-${Date.now()}`,
      CASE_ID: body.caseId || `CASE-${Date.now()}`,
      BUSINESS_NAME: body.businessName || 'Maharashtrian Pickles & Spices',
      BUSINESS_ADDRESS: body.businessAddress || 'MIDC Industrial Area, Pune',
      INSPECTOR_NAME: body.inspectorName || 'Inspector Rajesh Deshmukh',
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
      businessName: body.businessName || 'Maharashtrian Pickles & Spices',
      productName: body.productName || 'Mango Pickle 500g',
      type: type,
      status: 'draft',
      issuedDate: issuedDate.toISOString(),
      deadline: deadlineDate.toISOString(),
      daysRemaining: this.workflowService.calculateDaysRemaining(deadlineDate),
      contentText: renderedText,
      bodyText: renderedText,
      sections: [],
      violations: [],
      isAiDraft: false,
      pdfUrl: `https://storage.local/notices/notice_${Date.now()}.pdf`,
      createdAt: new Date(),
    };

    this.mockNotices.push(notice);
    return notice;
  }

  @Get('notices')
  @ApiOperation({ summary: 'List notices' })
  listNotices() {
    return this.mockNotices;
  }

  @Get('inspector/notices')
  @ApiOperation({ summary: 'List notices for inspector inbox' })
  listInspectorNotices() {
    return this.mockNotices;
  }

  @Get('businesses/:businessId/notices')
  @ApiOperation({ summary: 'List notices for business' })
  listBusinessNotices(@Param('businessId') businessId: string) {
    return this.mockNotices.filter(n => n.businessId === businessId || !n.businessId);
  }

  @Get('notices/:id')
  @ApiOperation({ summary: 'Get details of a specific legal notice' })
  getNoticeDetail(@Param('id') id: string) {
    const notice = this.mockNotices.find((n) => n.id === id);
    if (!notice) {
      return {
        id,
        caseId: 'CASE-001',
        type: 'improvement',
        status: 'draft',
        issuedDate: new Date().toISOString(),
        deadline: new Date(Date.now() + 15 * 86400000).toISOString(),
        daysRemaining: 15,
        productName: 'Sample Item',
        sections: [],
        violations: [],
        contentText: '# IMPROVEMENT NOTICE\n\nMandatory field missing on packaging.',
      };
    }
    return notice;
  }

  @Patch('notices/:id')
  @ApiOperation({ summary: 'Update notice status (ACKNOWLEDGED, DISPUTED, APPROVED, REJECTED, PAID)' })
  updateNoticeStatus(@Param('id') id: string, @Body() body: { status: string; comments?: string }) {
    const notice = this.mockNotices.find((n) => n.id === id);
    if (notice) {
      notice.status = body.status;
      notice.updatedAt = new Date();
    }
    return notice || { id, status: body.status, comments: body.comments };
  }

  @Post('notices/generate')
  @ApiOperation({ summary: 'Generate notice draft from inspection findings' })
  generateNoticeDraft(@Body() body: any) {
    const notice = {
      id: `NOT-${Date.now()}`,
      caseId: `CASE-${Date.now()}`,
      inspectionId: body.inspectionId || 'insp_001',
      businessId: 'biz_001',
      businessName: 'Maharashtrian Pickles & Spices SHG',
      productName: 'Mango Pickle 500g',
      type: (body.type || 'improvement').toLowerCase(),
      status: 'draft',
      issuedDate: new Date().toISOString(),
      deadline: new Date(Date.now() + 15 * 86400000).toISOString(),
      daysRemaining: 15,
      penaltyAmount: 5000,
      bodyText: 'Statutory Notice issued under Rule 6(1)(g) of Legal Metrology (Packaged Commodities) Rules, 2011.',
      sections: [
        { id: 'SEC-1', citation: 'Rule 6(1)(g)', title: 'Consumer Helpline', description: 'Mandatory helpline phone or email details missing.' },
      ],
      violations: [
        { id: 'VIOL-001', description: 'Missing Consumer Care Helpline details on packaging', ruleSection: 'Rule 6(1)(g)', severity: 'medium', status: 'confirmed' },
      ],
      isAiDraft: true,
      createdAt: new Date(),
    };
    this.mockNotices.push(notice);
    return notice;
  }

  @Post('notices/:id/confirm')
  @ApiOperation({ summary: 'Confirm notice draft' })
  confirmNotice(@Param('id') id: string, @Body() body: any) {
    const notice = this.mockNotices.find(n => n.id === id);
    if (notice) {
      notice.status = 'pendingSignature';
      notice.inspectorRemark = body.remark || 'Verified by Inspector';
      return notice;
    }
    return { id, status: 'pendingSignature', inspectorRemark: body.remark };
  }

  @Post('notices/:id/issue')
  @ApiOperation({ summary: 'Sign and issue notice' })
  issueConfirmedNotice(@Param('id') id: string, @Body() body: any) {
    const notice = this.mockNotices.find(n => n.id === id);
    if (notice) {
      notice.status = 'issued';
      notice.signedAt = new Date().toISOString();
      return notice;
    }
    return { id, status: 'issued', signedAt: new Date().toISOString() };
  }

  @Post('notices/:id/sections')
  @ApiOperation({ summary: 'Add legal section citation to notice' })
  addSection(@Param('id') id: string, @Body() body: any) {
    const notice = this.mockNotices.find(n => n.id === id);
    const sec = {
      id: `SEC-${Date.now()}`,
      citation: body.citation || 'Section 36(1)',
      title: body.title || 'Penalty Section',
    };
    if (notice) {
      notice.sections = notice.sections || [];
      notice.sections.push(sec);
      return notice;
    }
    return { id, sections: [sec] };
  }
}
