import { Controller, Post, Get, Body, UploadedFiles, UseInterceptors } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiConsumes } from '@nestjs/swagger';
import { AnyFilesInterceptor } from '@nestjs/platform-express';

@ApiTags('Self-Check (Private Business Compliance)')
@Controller('api/v1/self-check')
export class SelfCheckController {
  private history = [
    {
      id: 'sc_hist_01',
      productName: 'House Blend Chilli Powder 500g',
      performedAt: new Date(Date.now() - 86400000 * 2).toISOString(),
      isCompliant: false,
      issues: [
        {
          field: 'Consumer Care',
          issue: 'Missing official helpline phone or email on packaging',
          requirement: 'Rule 6(2) of PCR, 2011 mandates clear consumer helpline & email.',
          severity: 'medium',
          recommendedCorrection: 'Print: Consumer Care: +91-1800-233-5566, email: care@brand.com',
        },
        {
          field: 'Unit Sale Price',
          issue: 'Unit sale price (USP per g or kg) not declared on 500g pack',
          requirement: 'Rule 6(11) of PCR, 2011 mandates USP on packages > 100g/ml.',
          severity: 'low',
          recommendedCorrection: 'Print: ₹0.30 per gram (inclusive of all taxes)',
        },
      ],
    },
    {
      id: 'sc_hist_02',
      productName: 'Refined Sunflower Oil 1L',
      performedAt: new Date(Date.now() - 86400000 * 5).toISOString(),
      isCompliant: true,
      issues: [],
    },
  ];

  @Post('analyze')
  @ApiOperation({ summary: 'Analyze packaging images for business self-compliance (Private & Confidential)' })
  @ApiConsumes('multipart/form-data')
  @UseInterceptors(AnyFilesInterceptor())
  analyze(@Body() body: any, @UploadedFiles() files?: any[]) {
    const productName = body?.productNameHint || 'Sample Packaged Commodity';
    const report = {
      id: `sc_${Date.now()}`,
      productName,
      performedAt: new Date().toISOString(),
      isCompliant: false,
      issues: [
        {
          field: 'Consumer Care',
          issue: 'Missing consumer helpline number or email address on the package.',
          requirement: 'Rule 6(2) of Legal Metrology (Packaged Commodities) Rules, 2011 requires name, address, telephone number and email of the grievance officer.',
          severity: 'medium',
          recommendedCorrection: 'Add text: Consumer Care: +91-1800-111-222, email: care@brand.com',
        },
        {
          field: 'MRP Declaration',
          issue: 'MRP missing statutory qualifier "inclusive of all taxes".',
          requirement: 'Rule 6(1)(e) requires retail sale price clearly stating "Maximum Retail Price / MRP Rs. ... incl. of all taxes".',
          severity: 'high',
          recommendedCorrection: 'Ensure price format is: "MRP ₹ ... (inclusive of all taxes)"',
        },
      ],
    };

    this.history.unshift(report);
    return report;
  }

  @Get('history')
  @ApiOperation({ summary: 'Get business private self-check history' })
  getHistory() {
    return this.history;
  }
}
