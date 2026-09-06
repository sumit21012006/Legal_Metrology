import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Private Business Self-Checks')
@Controller('api/v1/self-check')
export class SelfChecksController {
  private mockSelfCheckHistory: any[] = [
    {
      id: 'sc_report_101',
      productName: 'Mango Pickle 500g Jar',
      performedAt: new Date().toISOString(),
      isCompliant: false,
      issues: [
        {
          field: 'consumer_care',
          issue: 'Missing helpline phone or contact email',
          requirement: 'Rule 6(1)(g) mandates consumer care helpline details',
          severity: 'medium',
          recommendedCorrection: 'Add helpline: +91-1800-111-222, email: care@spices.com',
        },
      ],
    },
    {
      id: 'sc_report_102',
      productName: 'Special Papad Pack 250g',
      performedAt: new Date(Date.now() - 2 * 86400000).toISOString(),
      isCompliant: true,
      issues: [],
    },
  ];

  @Get('history')
  @ApiOperation({ summary: 'Get private self-check history for business' })
  getSelfCheckHistory() {
    return this.mockSelfCheckHistory;
  }

  @Post('analyze')
  @ApiOperation({ summary: 'Perform private self-check analysis' })
  performSelfCheck(@Body() body: any) {
    const newReport = {
      id: `sc_report_${Date.now()}`,
      productName: body.productNameHint || 'Pre-packaged Commodity',
      performedAt: new Date().toISOString(),
      isCompliant: false,
      issues: [
        {
          field: 'unit_sale_price',
          issue: 'Unit sale price declaration format missing',
          requirement: 'Rule 6(11) requires USP declaration e.g. Rs 0.30/g',
          severity: 'medium',
          recommendedCorrection: 'Add "Unit Sale Price: Rs 0.30/g" next to MRP',
        },
      ],
    };
    this.mockSelfCheckHistory.push(newReport);
    return newReport;
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get details of a specific self-check report' })
  getSelfCheckDetail(@Param('id') id: string) {
    const item = this.mockSelfCheckHistory.find((s) => s.id === id);
    if (!item) return this.mockSelfCheckHistory[0];
    return item;
  }
}
