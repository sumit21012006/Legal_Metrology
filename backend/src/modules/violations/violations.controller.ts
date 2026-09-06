import { Controller, Post, Patch, Get, Param, Body, Query } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Violations & Product Offences')
@Controller('api/v1')
export class ViolationsController {
  @Post('violations/:id/confirm')
  @ApiOperation({ summary: 'Confirm detected packaging violation' })
  confirmViolation(@Param('id') id: string, @Body() body: any) {
    return {
      id,
      type: 'mandatory_declaration_missing',
      description: 'Missing Consumer Care Helpline details on packaging',
      severity: 'medium',
      status: 'confirmed',
      ruleSection: 'Rule 6(1)(g)',
      ruleTitle: 'Consumer Care Helpline',
      confidence: 0.95,
      inspectorRemark: body.remark || 'Confirmed by Legal Metrology Officer',
      isAiGenerated: true,
      detectedAt: new Date().toISOString(),
    };
  }

  @Post('violations/:id/reject')
  @ApiOperation({ summary: 'Reject detected packaging violation' })
  rejectViolation(@Param('id') id: string, @Body() body: any) {
    return {
      id,
      type: 'mandatory_declaration_missing',
      description: 'Rejected packaging violation',
      severity: 'low',
      status: 'rejected',
      inspectorRemark: body.remark || 'False positive confirmed by officer',
      detectedAt: new Date().toISOString(),
    };
  }

  @Patch('violations/:id')
  @ApiOperation({ summary: 'Edit packaging violation details' })
  editViolation(@Param('id') id: string, @Body() body: any) {
    return {
      id,
      type: body.type || 'mandatory_declaration_missing',
      description: body.description || 'Packaging declaration non-compliance',
      severity: body.severity || 'medium',
      ruleSection: body.ruleSection || 'Rule 6(1)(g)',
      status: 'confirmed',
      inspectorRemark: body.remark,
      detectedAt: new Date().toISOString(),
    };
  }

  @Get('products/:productId/offences')
  @ApiOperation({ summary: 'Get offence history tier for product/business' })
  getProductOffences(@Param('productId') productId: string, @Query('businessId') businessId?: string) {
    return {
      productId,
      matchedProductName: 'Mango Pickle 500g',
      tier: 'first',
      checkedAt: new Date().toISOString(),
      matchConfidence: 0.96,
      records: [
        {
          caseId: 'CASE-2025-098',
          businessName: 'Maharashtrian Pickles & Spices SHG',
          location: 'Pune, Maharashtra',
          date: new Date(Date.now() - 180 * 86400000).toISOString(),
          violationSummary: 'Minor net quantity font size deficiency (Compounded)',
          caseStatus: 'resolved',
        },
      ],
    };
  }
}
