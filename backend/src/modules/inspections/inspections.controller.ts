import { Controller, Get, Post, Patch, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { OffenceCalculatorService } from '../offences/offence-calculator.service';

@ApiTags('Inspector Operations & Packaging Scans')
@Controller('api/v1/inspections')
export class InspectionsController {
  private mockInspections: any[] = [
    {
      id: 'insp_001',
      inspectorId: 'INS-MH-4021',
      inspectorName: 'Inspector Rajesh Deshmukh',
      businessId: 'biz_001',
      business: {
        id: 'biz_001',
        name: 'Maharashtrian Pickles & Spices SHG',
        ownerName: 'Sunita Patil',
        address: 'Plot 42, MIDC Industrial Area, Pune, Maharashtra 411026',
        gstin: '27AAAAA0000A1Z5',
        category: 'food',
        status: 'active',
      },
      type: 'routine',
      status: 'assigned',
      scheduledAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
      notes: 'Routine packaged food inspection under Rule 6.',
    },
    {
      id: 'insp_002',
      inspectorId: 'INS-MH-4021',
      inspectorName: 'Inspector Rajesh Deshmukh',
      businessId: 'biz_002',
      business: {
        id: 'biz_002',
        name: 'Quality Packaged Commodities Pvt Ltd',
        ownerName: 'Rajesh Sharma',
        address: 'Block B, Andheri East, Mumbai, Maharashtra 400069',
        gstin: '27BBBCA1111B2Z8',
        category: 'retailer',
        status: 'active',
      },
      type: 'complaint_based',
      status: 'in_progress',
      scheduledAt: new Date().toISOString(),
      createdAt: new Date(Date.now() - 86400000).toISOString(),
      notes: 'Citizen complaint on underweight edible oil packets.',
    },
  ];

  constructor(private readonly offenceCalculator: OffenceCalculatorService) {}

  @Post()
  @ApiOperation({ summary: 'Start a new on-site inspection for a business' })
  startInspection(@Body() body: any) {
    const inspection = {
      id: `insp_${Date.now()}`,
      inspectorId: body.inspectorId || 'INS-MH-4021',
      inspectorName: body.inspectorName || 'Inspector Rajesh Deshmukh',
      businessId: body.businessId || 'biz_001',
      business: {
        id: body.businessId || 'biz_001',
        name: body.businessName || 'Maharashtrian Pickles & Spices SHG',
        address: 'Plot 42, MIDC Industrial Area, Pune, Maharashtra 411026',
        gstin: '27AAAAA0000A1Z5',
        status: 'active',
      },
      type: body.type || 'routine',
      complaintId: body.complaintId || null,
      scheduledAt: new Date().toISOString(),
      status: 'assigned',
      createdAt: new Date().toISOString(),
      notes: body.notes,
    };
    this.mockInspections.push(inspection);
    return inspection;
  }

  @Get()
  @ApiOperation({ summary: 'List inspector assigned inspections' })
  listInspections() {
    return this.mockInspections;
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get inspection by id' })
  getInspection(@Param('id') id: string) {
    const found = this.mockInspections.find(i => i.id === id);
    if (found) return found;
    return {
      id,
      inspectorId: 'INS-MH-4021',
      businessId: 'biz_001',
      business: {
        id: 'biz_001',
        name: 'Maharashtrian Pickles & Spices SHG',
        status: 'active',
      },
      type: 'routine',
      status: 'assigned',
      scheduledAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
    };
  }

  @Get(':id/violations')
  @ApiOperation({ summary: 'Get violations found in inspection' })
  getViolations(@Param('id') id: string) {
    return [
      {
        id: 'viol_001',
        inspectionId: id,
        ruleSection: 'Rule 6(1)(g)',
        description: 'Missing consumer care helpline details on packaging',
        severity: 'medium',
        status: 'confirmed',
      },
    ];
  }

  @Post(':id/violations')
  @ApiOperation({ summary: 'Add a violation to inspection' })
  addViolation(@Param('id') id: string, @Body() body: any) {
    return {
      id: `viol_${Date.now()}`,
      inspectionId: id,
      type: body.type || 'mandatory_declaration_missing',
      description: body.description || 'Observed declaration deficiency',
      severity: body.severity || 'medium',
      ruleSection: body.ruleSection || 'Rule 6(1)(g)',
      status: 'confirmed',
      isAiGenerated: false,
      detectedAt: new Date().toISOString(),
    };
  }

  @Post(':id/start')
  @ApiOperation({ summary: 'Start inspection action' })
  startAction(@Param('id') id: string) {
    const found = this.mockInspections.find(i => i.id === id);
    if (found) {
      found.status = 'in_progress';
      return found;
    }
    return { id, status: 'in_progress' };
  }

  @Post(':id/complete')
  @ApiOperation({ summary: 'Complete inspection action' })
  completeAction(@Param('id') id: string, @Body() body: any) {
    const found = this.mockInspections.find(i => i.id === id);
    if (found) {
      found.status = 'completed';
      found.completedAt = new Date().toISOString();
      return found;
    }
    return { id, status: 'completed', completedAt: new Date().toISOString() };
  }

  @Patch(':id/observations')
  @ApiOperation({ summary: 'Update inspection observations' })
  updateObservations(@Param('id') id: string, @Body() body: any) {
    const found = this.mockInspections.find(i => i.id === id);
    if (found) {
      found.observations = body;
      return found;
    }
    return { id, observations: body };
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

  @Post(':id/evidence')
  @ApiOperation({ summary: 'Upload packaging photo evidence' })
  uploadEvidence(@Param('id') id: string, @Body() body: any) {
    return {
      id: `ev_${Date.now()}`,
      ownerId: id,
      filePath: 'https://storage.local/evidence/photo_1.jpg',
      side: body.side || 'front',
      capturedAt: new Date().toISOString(),
    };
  }

  @Get(':id/evidence')
  @ApiOperation({ summary: 'List evidence for inspection' })
  getEvidence(@Param('id') id: string) {
    return [
      {
        id: `ev_front_${id}`,
        ownerId: id,
        filePath: 'https://storage.local/evidence/front.jpg',
        side: 'front',
        capturedAt: new Date().toISOString(),
      },
    ];
  }

  @Post(':id/seizures')
  @ApiOperation({ summary: 'Record seizure samples' })
  recordSeizures(@Param('id') id: string, @Body() body: any) {
    const samples = (body.samples || []).map((s: any, idx: number) => ({
      id: `smpl_${Date.now()}_${idx}`,
      productId: s.productId || 'prod_001',
      productName: s.productName || 'Mango Pickle 500g',
      quantity: s.quantity || '10 units',
      reason: body.reason || 'Statutory violation Rule 6(1)(g)',
      capturedAt: new Date().toISOString(),
    }));
    return {
      inspectionId: id,
      reason: body.reason,
      samples,
    };
  }

  @Get(':id/seizures')
  @ApiOperation({ summary: 'Get seizure samples for inspection' })
  getSeizures(@Param('id') id: string) {
    return {
      samples: [
        {
          id: `smpl_1`,
          productId: 'prod_001',
          productName: 'Mango Pickle 500g',
          quantity: '5 units',
          reason: 'Absence of mandatory declarations',
          capturedAt: new Date().toISOString(),
        },
      ],
    };
  }
}
