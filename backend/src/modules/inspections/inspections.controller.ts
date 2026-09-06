import { Controller, Get, Post, Patch, Delete, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { OffenceCalculatorService } from '../offences/offence-calculator.service';

@ApiTags('Inspector Operations & Packaging Scans')
@Controller('api/v1/inspections')
export class InspectionsController {
  private mockInspections: any[] = [
    {
      id: 'insp_001',
      inspectorId: 'usr_inspector_1',
      inspectorName: 'Inspector S. K. Shinde',
      businessId: 'biz_001',
      business: {
        id: 'biz_001',
        name: 'Maharashtrian Pickles & Spices SHG',
        type: 'manufacturer',
        status: 'active',
        ownerName: 'Sunita Patil',
        address: 'Plot 42, MIDC Industrial Area, Pune, Maharashtra 411026',
        location: {
          addressLine: 'Plot 42, MIDC Industrial Area',
          city: 'Pune',
          state: 'Maharashtra',
          pincode: '411026',
          latitude: 18.5204,
          longitude: 73.8567,
        },
        gstin: '27AAAAA0000A1Z5',
        turnoverBand: '< ₹20 Lakhs (SHG)',
        geoLat: 18.5204,
        geoLng: 73.8567,
      },
      complaintId: null,
      type: 'Routine',
      status: 'assigned',
      scheduledAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
      notes: 'Routine packaged food inspection under Rule 6.',
      products: [],
    },
    {
      id: 'insp_002',
      inspectorId: 'usr_inspector_1',
      inspectorName: 'Inspector S. K. Shinde',
      businessId: 'biz_002',
      business: {
        id: 'biz_002',
        name: 'Quality Packaged Commodities Pvt Ltd',
        type: 'packer',
        status: 'active',
        ownerName: 'Rajesh Sharma',
        address: 'Block B, Andheri East, Mumbai, Maharashtra 400069',
        location: {
          addressLine: 'Block B, Andheri East',
          city: 'Mumbai',
          state: 'Maharashtra',
          pincode: '400069',
          latitude: 19.0760,
          longitude: 72.8777,
        },
        gstin: '27BBBCA1111B2Z8',
        turnoverBand: '₹1 Cr - ₹5 Cr',
        geoLat: 19.0760,
        geoLng: 72.8777,
      },
      complaintId: 'CMP-1002',
      type: 'Complaint Based',
      status: 'inProgress',
      scheduledAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
      notes: 'Citizen complaint on underweight edible oil packets.',
      products: [],
    },
  ];

  constructor(private readonly offenceCalculator: OffenceCalculatorService) {}

  @Post()
  @ApiOperation({ summary: 'Start a new on-site inspection for a business' })
  startInspection(@Body() body: any) {
    const inspection = {
      id: `insp_${Date.now()}`,
      inspectorId: body.inspectorId || 'usr_inspector_1',
      inspectorName: body.inspectorName || 'Inspector S. K. Shinde',
      businessId: body.businessId || 'biz_001',
      business: {
        id: body.businessId || 'biz_001',
        name: body.businessName || 'Maharashtrian Pickles & Spices SHG',
        type: 'manufacturer',
        status: 'active',
        ownerName: 'Sunita Patil',
        address: body.businessAddress || 'Plot 42, MIDC Industrial Area, Pune, Maharashtra 411026',
        location: {
          addressLine: body.businessAddress || 'Plot 42, MIDC Industrial Area',
          city: 'Pune',
          state: 'Maharashtra',
          pincode: '411026',
          latitude: 18.5204,
          longitude: 73.8567,
        },
        gstin: body.gstin || '27AAAAA0000A1Z5',
      },
      complaintId: body.complaintId || null,
      type: body.type || 'Routine',
      status: 'assigned',
      scheduledAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
      notes: body.notes,
      products: [],
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
  @ApiOperation({ summary: 'Get details of a specific inspection' })
  getInspectionDetail(@Param('id') id: string) {
    const insp = this.mockInspections.find((i) => i.id === id);
    if (!insp) return this.mockInspections[0];
    return insp;
  }

  @Post(':id/ocr-result')
  @ApiOperation({ summary: 'Process multi-angle packaging OCR scan findings' })
  processOcrResult(@Param('id') id: string, @Body() body: any) {
    const productName = body.productName || 'Mango Pickle 500g';
    const manufacturerName = body.manufacturerName || 'Maharashtrian Spices Factory';
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
      timestamp: new Date().toISOString(),
    };
  }

  @Get(':id/panchanama')
  @ApiOperation({ summary: 'Get Panchanama record for inspection' })
  getPanchanama(@Param('id') id: string) {
    return {
      id: `panch_${id}`,
      inspectionId: id,
      caseId: 'CASE-1001',
      observations: 'Spot inspection revealed non-compliant Consumer Care label declaration.',
      witness1Name: 'Shri R. V. Deshmukh',
      witness2Name: 'Shri P. K. Joshi',
      actSection: 'Section 36(1) & Rule 6(1)(g)',
      seizureDetails: 'Seized 2 sample units of Mango Pickle 500g for verification.',
      noticePeriodDays: 15,
      createdAt: new Date().toISOString(),
    };
  }

  @Post(':id/start')
  @ApiOperation({ summary: 'Start inspection' })
  startInspectionAction(@Param('id') id: string) {
    const insp = this.getInspectionDetail(id);
    insp.status = 'inProgress';
    return insp;
  }

  @Post(':id/complete')
  @ApiOperation({ summary: 'Complete inspection' })
  completeInspectionAction(@Param('id') id: string, @Body() body: any) {
    const insp = this.getInspectionDetail(id);
    insp.status = 'completed';
    insp.completedAt = new Date().toISOString();
    insp.remarks = body.remarks;
    return insp;
  }

  @Patch(':id/observations')
  @ApiOperation({ summary: 'Update inspection observations' })
  updateObservations(@Param('id') id: string, @Body() body: any) {
    const insp = this.getInspectionDetail(id);
    insp.observation = body;
    return insp;
  }

  @Post(':id/evidence')
  @ApiOperation({ summary: 'Upload inspection evidence photo' })
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
  @ApiOperation({ summary: 'List inspection evidence photos' })
  getEvidence(@Param('id') id: string) {
    return [
      {
        id: `ev_1001`,
        ownerId: id,
        filePath: 'https://storage.local/evidence/photo_1.jpg',
        side: 'front',
        capturedAt: new Date().toISOString(),
      },
    ];
  }

  @Post(':id/seizures')
  @ApiOperation({ summary: 'Create seizure sample records' })
  createSeizures(@Param('id') id: string, @Body() body: any) {
    return {
      samples: (body.samples || [
        {
          id: `smp_${Date.now()}`,
          productId: 'prod_001',
          productName: 'Mango Pickle 500g Jar',
          quantity: '2 Units',
          reason: body.reason || 'Seized for evidence under Section 15',
          capturedAt: new Date().toISOString(),
        },
      ]).map((s: any) => ({
        id: s.id || `smp_${Date.now()}`,
        productId: s.productId || 'prod_001',
        productName: s.productName || 'Mango Pickle 500g Jar',
        quantity: s.quantity || '2 Units',
        reason: body.reason || 'Seized for evidence',
        capturedAt: new Date().toISOString(),
      })),
    };
  }

  @Get(':id/seizures')
  @ApiOperation({ summary: 'List seizure samples for inspection' })
  getSeizures(@Param('id') id: string) {
    return {
      samples: [
        {
          id: 'smp_1001',
          productId: 'prod_001',
          productName: 'Mango Pickle 500g Jar',
          quantity: '2 Units',
          reason: 'Seized for verification of declarations',
          capturedAt: new Date().toISOString(),
        },
      ],
    };
  }

  @Get(':id/violations')
  @ApiOperation({ summary: 'List confirmed violations for inspection' })
  getViolations(@Param('id') id: string) {
    return [
      {
        id: 'viol_1001',
        inspectionId: id,
        type: 'missingDeclaration',
        description: 'Missing Consumer Care Helpline Phone & Email on packaging label',
        severity: 'medium',
        ruleSection: 'Rule 6(1)(g)',
        recommendation: 'Add helpline: +91-1800-111-222, email: care@spices.com',
      },
    ];
  }

  @Post(':id/violations')
  @ApiOperation({ summary: 'Add violation to inspection' })
  addViolation(@Param('id') id: string, @Body() body: any) {
    return {
      id: `viol_${Date.now()}`,
      inspectionId: id,
      type: body.type || 'missingDeclaration',
      description: body.description || 'Missing mandatory declaration',
      severity: body.severity || 'medium',
      ruleSection: body.ruleSection || 'Rule 6(1)(g)',
      recommendation: body.recommendation || 'Correct packaging label',
    };
  }

  @Post(':id/supply-chain')
  @ApiOperation({ summary: 'Submit supplier declaration' })
  submitSupplyChain(@Param('id') id: string, @Body() body: any) {
    return { status: 'SUCCESS', message: 'Supplier declaration recorded' };
  }

  @Post(':id/supply-chain/evidence')
  @ApiOperation({ summary: 'Upload purchase evidence invoice' })
  uploadSupplyChainEvidence(@Param('id') id: string, @Body() body: any) {
    return { status: 'SUCCESS', message: 'Purchase invoice evidence uploaded' };
  }
}
