import { Controller, Post, Get, Param, Body } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('OCR & Computer Vision')
@Controller('api/v1/ocr')
export class OcrController {
  @Post('analyze')
  @ApiOperation({ summary: 'Submit package images for OCR analysis' })
  analyzePackage(@Body() body: any) {
    const jobId = `job_${Date.now()}`;
    return {
      jobId,
      status: 'completed',
      message: 'OCR analysis initiated',
    };
  }

  @Get('jobs/:jobId')
  @ApiOperation({ summary: 'Get OCR pipeline status and extracted packaging fields' })
  getJobStatus(@Param('jobId') jobId: string) {
    return {
      jobId,
      status: 'completed',
      progressStep: 'completed',
      analyzedAt: new Date().toISOString(),
      rawTextPreview: 'Mango Pickle 500g | Net Qty: 500g | MRP Rs 150.00 | Mfg: 08/2026 | FSSAI Lic 11521034000123',
      fields: [
        {
          key: 'productName',
          label: 'Product Name',
          value: 'Mango Pickle 500g',
          confidence: 0.98,
          isMissing: false,
        },
        {
          key: 'mrp',
          label: 'Maximum Retail Price (MRP)',
          value: '150.00',
          confidence: 0.96,
          isMissing: false,
          unit: 'INR',
        },
        {
          key: 'netQuantity',
          label: 'Net Quantity',
          value: '500',
          confidence: 0.95,
          isMissing: false,
          unit: 'g',
        },
        {
          key: 'mfgDate',
          label: 'Date of Manufacture',
          value: '08/2026',
          confidence: 0.94,
          isMissing: false,
        },
        {
          key: 'manufacturer',
          label: 'Manufacturer / Packer',
          value: 'Maharashtrian Pickles & Spices SHG',
          confidence: 0.93,
          isMissing: false,
        },
        {
          key: 'consumerCare',
          label: 'Consumer Care Helpline',
          value: '',
          confidence: 0.12,
          isMissing: true,
        },
      ],
    };
  }
}
