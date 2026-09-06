import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { OffenceCalculatorService } from '../offences/offence-calculator.service';

@ApiTags('Inspector Operations & Packaging Scans')
@Controller('api/v1/inspections')
export class InspectionsController {
  private mockInspections: any[] = [];

  constructor(private readonly offenceCalculator: OffenceCalculatorService) {}

  @Post()
  @ApiOperation({ summary: 'Start a new on-site inspection for a business' })
  startInspection(@Body() body: any) {
    const inspection = {
      id: `insp_${Date.now()}`,
      inspectorId: body.inspectorId || 'usr_inspector_1',
      businessId: body.businessId,
      complaintId: body.complaintId || null,
      visitDate: new Date(),
      status: 'ASSIGNED',
      createdAt: new Date(),
    };
    this.mockInspections.push(inspection);
    return inspection;
  }

  @Get()
  @ApiOperation({ summary: 'List inspector assigned inspections' })
  listInspections() {
    return this.mockInspections;
  }

  @Post(':id/ocr-result')
  @ApiOperation({ summary: 'Process multi-angle packaging OCR scan findings' })
  processOcrResult(@Param('id') id: string, @Body() body: any) {
    const productName = body.productName || 'Mango Pickle 500g';
    const manufacturerName = body.manufacturerName || 'Maharashtrian Pickles & Spices';
    const legalSection = body.legalSection || 'Section 36(1)';

    const offenceEval = this.offenceCalculator.evaluateOffence({
      productName,
      manufacturerName,
      legalSection,
      businessId: body.businessId || 'biz_001',
    });

    return {
      inspectionId: id,
      ocrResultId: `ocr_${Date.now()}`,
      extractedFields: {
        productName,
        manufacturerName,
        mrp: body.mrp || '150.00',
        netQuantity: body.netQuantity || '500g',
        mfgDate: body.mfgDate || '08/2026',
        consumerCare: body.consumerCare || 'Missing',
      },
      violations: [
        {
          fieldKey: 'consumer_care',
          issue: 'Missing helpline phone number or contact email',
          actSection: 'Rule 6(1)(g)',
          ruleText: 'Consumer care helpline details mandatory on packaging',
        },
      ],
      offenceEvaluation: offenceEval,
    };
  }

  @Post(':id/panchanama')
  @ApiOperation({ summary: 'Record Panchanama spot inspection details and witness signatures' })
  recordPanchanama(@Param('id') id: string, @Body() body: any) {
    const sampleId = `SMP-MH-${Math.floor(100000 + Math.random() * 900000)}`;
    return {
      inspectionId: id,
      panchanamaId: `panch_${Date.now()}`,
      sampleId: sampleId,
      witness1: body.witness1Name || 'Independent Witness 1',
      witness2: body.witness2Name || 'Independent Witness 2',
      seizurePhotoUrl: body.seizurePhotoUrl || 'https://storage.local/seizures/sample_1.jpg',
      status: 'PANCHANAMA_RECORDED',
      timestamp: new Date(),
    };
  }
}
