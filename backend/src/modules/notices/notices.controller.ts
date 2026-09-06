import { Controller, Get, Post, Patch, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { NoticeGeneratorService } from './notice-generator.service';
import { CaseWorkflowService } from '../cases/case-workflow.service';

@ApiTags('Legal Notices & Orders')
@Controller('api/v1/notices')
export class NoticesController {
  private mockNotices: any[] = [];

  constructor(
    private readonly noticeGenerator: NoticeGeneratorService,
    private readonly workflowService: CaseWorkflowService,
  ) {}

  @Post()
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
      type: type.toUpperCase(),
      status: 'ISSUED',
      issuedDate: issuedDate,
      deadlineDate: deadlineDate,
      daysRemaining: this.workflowService.calculateDaysRemaining(deadlineDate),
      contentText: renderedText,
      pdfUrl: `https://storage.local/notices/notice_${Date.now()}.pdf`,
      createdAt: new Date(),
    };

    this.mockNotices.push(notice);
    return notice;
  }

  @Get()
  @ApiOperation({ summary: 'List notices for business or inspector inbox' })
  listNotices() {
    return this.mockNotices;
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get details of a specific legal notice' })
  getNoticeDetail(@Param('id') id: string) {
    const notice = this.mockNotices.find((n) => n.id === id);
    if (!notice) {
      return {
        id,
        type: 'IMPROVEMENT',
        status: 'ISSUED',
        issuedDate: new Date(),
        deadlineDate: new Date(Date.now() + 15 * 86400000),
        daysRemaining: 15,
        contentText: '# IMPROVEMENT NOTICE\n\nMandatory field missing on packaging.',
      };
    }
    return notice;
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update notice status (ACKNOWLEDGED, DISPUTED, APPROVED, REJECTED, PAID)' })
  updateNoticeStatus(@Param('id') id: string, @Body() body: { status: string; comments?: string }) {
    const notice = this.mockNotices.find((n) => n.id === id);
    if (notice) {
      notice.status = body.status;
      notice.updatedAt = new Date();
    }
    return notice || { id, status: body.status, comments: body.comments };
  }
}
