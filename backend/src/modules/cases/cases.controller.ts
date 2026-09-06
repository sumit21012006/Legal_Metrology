import { Controller, Get, Post, Patch, Delete, Param, Query, Body } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { OffenceCalculatorService } from '../offences/offence-calculator.service';

@ApiTags('Cases Management')
@Controller('api/v1')
export class CasesController {
  private mockCases: any[] = [
    {
      id: 'CASE-1001',
      caseNumber: 'CASE-2026-001',
      productName: 'Mango Pickle 500g',
      status: 'underReview',
      openedAt: new Date().toISOString(),
      violationSummary: 'Missing Consumer Care Helpline Phone & Email on packaging',
      counterpartyName: 'Maharashtrian Pickles & Spices SHG',
      currentStage: 'Notice Issued',
      deadline: new Date(Date.now() + 15 * 86400000).toISOString(),
      requiredAction: 'Submit corrected packaging photo',
      noticeType: 'improvement',
      penaltyAmount: 25000.0,
      timeline: [
        {
          title: 'Citizen Complaint Registered',
          dateTime: new Date(Date.now() - 3 * 86400000).toISOString(),
          isDone: true,
          isCurrent: false,
          details: 'Complaint filed by citizen for missing consumer care info.',
          actor: 'Citizen',
        },
        {
          title: 'Inspection Completed',
          dateTime: new Date(Date.now() - 2 * 86400000).toISOString(),
          isDone: true,
          isCurrent: false,
          details: 'Inspector verified non-compliant packaging at Pune location.',
          actor: 'Inspector S. K. Shinde',
        },
        {
          title: 'Improvement Notice Issued',
          dateTime: new Date(Date.now() - 1 * 86400000).toISOString(),
          isDone: true,
          isCurrent: true,
          details: 'Notice issued giving 15 days to rectify packaging.',
          actor: 'Legal Metrology Office',
        },
      ],
    },
    {
      id: 'CASE-1002',
      caseNumber: 'CASE-2026-002',
      productName: 'Refined Sunflower Oil 1L',
      status: 'noticeIssued',
      openedAt: new Date(Date.now() - 5 * 86400000).toISOString(),
      violationSummary: 'Net quantity declaration font size smaller than Table-I requirement',
      counterpartyName: 'Quality Packaged Commodities Pvt Ltd',
      currentStage: 'Compounding Order Issued',
      deadline: new Date(Date.now() + 30 * 86400000).toISOString(),
      requiredAction: 'Pay compounding penalty',
      noticeType: 'compounded',
      penaltyAmount: 50000.0,
      timeline: [
        {
          title: 'Routine Inspection Conducted',
          dateTime: new Date(Date.now() - 5 * 86400000).toISOString(),
          isDone: true,
          isCurrent: false,
          details: 'Font size mismatch observed on 1L oil Pouch.',
          actor: 'Inspector M. R. Kulkarni',
        },
        {
          title: 'Compounding Order Issued',
          dateTime: new Date(Date.now() - 1 * 86400000).toISOString(),
          isDone: true,
          isCurrent: true,
          details: 'Controller approved compounding order of Rs. 50,000.',
          actor: 'Controller of Legal Metrology',
        },
      ],
    },
  ];

  constructor(private readonly offenceCalculator: OffenceCalculatorService) {}

  @Get('cases')
  @ApiOperation({ summary: 'List all legal compliance cases' })
  listCases(@Query('active') active?: string) {
    if (active === 'true') {
      return this.mockCases.filter((c) => c.status !== 'completed' && c.status !== 'resolved');
    }
    return this.mockCases;
  }

  @Get('cases/:id')
  @ApiOperation({ summary: 'Get case details by ID' })
  getCase(@Param('id') id: string) {
    const c = this.mockCases.find((item) => item.id === id);
    if (!c) return this.mockCases[0];
    return c;
  }

  @Get('cases/:id/timeline')
  @ApiOperation({ summary: 'Get timeline for case' })
  getTimeline(@Param('id') id: string) {
    const c = this.getCase(id);
    return c ? c.timeline : [];
  }

  @Get('business/cases')
  @ApiOperation({ summary: 'List cases for business portal' })
  listBusinessCases() {
    return this.mockCases;
  }

  @Get('products/:productId/offences')
  @ApiOperation({ summary: 'Get repeat offence history for product' })
  getProductOffences(@Param('productId') productId: string, @Query('businessId') businessId?: string) {
    const evalResult = this.offenceCalculator.evaluateOffence({
      productName: 'Mango Pickle 500g Jar',
      manufacturerName: 'Maharashtrian Pickles & Spices SHG',
      legalSection: 'Section 36(1)',
      businessId: businessId || 'biz_001',
    });

    return {
      productId: productId,
      matchedProductName: 'Mango Pickle 500g Jar',
      tier: evalResult.offenceTier.toLowerCase(),
      checkedAt: new Date().toISOString(),
      matchConfidence: 0.95,
      records: [
        {
          caseId: 'CASE-2025-089',
          businessName: 'Maharashtrian Pickles & Spices SHG',
          location: 'Pune, MH',
          date: new Date(Date.now() - 180 * 86400000).toISOString(),
          violationSummary: 'First offence under Section 36(1) for missing contact details',
          caseStatus: 'COMPOUNDED',
        },
      ],
    };
  }

  @Delete('evidence/:id')
  @ApiOperation({ summary: 'Delete evidence photo by ID' })
  deleteEvidence(@Param('id') id: string) {
    return { status: 'SUCCESS', message: `Evidence ${id} deleted` };
  }

  @Post('ocr/analyze')
  @ApiOperation({ summary: 'Submit package images for OCR analysis' })
  analyzeOcr(@Body() body: any) {
    return { jobId: `ocr_job_${Date.now()}` };
  }

  @Get('ocr/jobs/:jobId')
  @ApiOperation({ summary: 'Get status of OCR analysis job' })
  getOcrJobStatus(@Param('jobId') jobId: string) {
    return {
      jobId: jobId,
      status: 'completed',
      progressStep: 'extractingText',
      analyzedAt: new Date().toISOString(),
      fields: [
        { key: 'mrp', value: 'Rs. 100.00', confidence: 0.98 },
        { key: 'net_quantity', value: '500 g', confidence: 0.96 },
        { key: 'consumer_care', value: 'Missing', confidence: 0.99 },
      ],
      rawTextPreview: 'NET WT: 500g MRP Rs. 100 MFG: 08/2026',
    };
  }

  @Patch('violations/:id')
  @ApiOperation({ summary: 'Edit violation details' })
  editViolation(@Param('id') id: string, @Body() body: any) {
    return {
      id: id,
      description: body.description || 'Violation description updated',
      severity: body.severity || 'medium',
      ruleSection: body.ruleSection || 'Rule 6(1)(g)',
      remark: body.remark,
    };
  }

  @Post('violations/:id/confirm')
  @ApiOperation({ summary: 'Confirm violation' })
  confirmViolation(@Param('id') id: string, @Body() body: any) {
    return { id: id, status: 'CONFIRMED', remark: body?.remark };
  }

  @Post('violations/:id/reject')
  @ApiOperation({ summary: 'Reject violation' })
  rejectViolation(@Param('id') id: string, @Body() body: any) {
    return { id: id, status: 'REJECTED', remark: body?.remark };
  }
}
