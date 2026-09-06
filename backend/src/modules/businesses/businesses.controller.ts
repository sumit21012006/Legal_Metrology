import { Controller, Get, Post, Body, Query } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Businesses & Self-Compliance')
@Controller('api/v1/businesses')
export class BusinessesController {
  private mockBusinesses = [
    {
      id: 'biz_001',
      name: 'Maharashtrian Pickles & Spices SHG',
      ownerName: 'Sunita Patil',
      address: 'Plot 42, MIDC Industrial Area, Pune, Maharashtra 411026',
      gstin: '27AAAAA0000A1Z5',
      turnoverBand: '< ₹20 Lakhs (SHG)',
      geoLat: 18.5204,
      geoLng: 73.8567,
    },
    {
      id: 'biz_002',
      name: 'Quality Packaged Commodities Pvt Ltd',
      ownerName: 'Rajesh Sharma',
      address: 'Block B, Andheri East, Mumbai, Maharashtra 400069',
      gstin: '27BBBCA1111B2Z8',
      turnoverBand: '₹1 Cr - ₹5 Cr',
      geoLat: 19.0760,
      geoLng: 72.8777,
    },
    {
      id: 'biz_003',
      name: 'Sahyadri Agro Products',
      ownerName: 'Anand Deshmukh',
      address: 'Gat No 102, Satara Highway, Satara, Maharashtra 415001',
      gstin: '27CCCCD2222C3Z1',
      turnoverBand: '₹20 Lakhs - ₹1 Cr',
      geoLat: 17.6805,
      geoLng: 74.0183,
    },
  ];

  @Get()
  @ApiOperation({ summary: 'Search businesses with autocomplete query' })
  searchBusinesses(@Query('q') query?: string, @Query('limit') limit?: number) {
    if (!query) return this.mockBusinesses;
    const q = query.toLowerCase();
    return this.mockBusinesses.filter(
      (b) =>
        b.name.toLowerCase().includes(q) ||
        b.gstin.toLowerCase().includes(q) ||
        b.address.toLowerCase().includes(q),
    );
  }

  @Post()
  @ApiOperation({ summary: 'Register a new business entity' })
  registerBusiness(@Body() body: any) {
    const newBiz = {
      id: `biz_${Date.now()}`,
      name: body.name || 'New Business Entity',
      ownerName: body.ownerName || 'Business Owner',
      address: body.address || 'Maharashtra Address',
      gstin: body.gstin || `27XX${Math.floor(Math.random() * 8999 + 1000)}Z5`,
      turnoverBand: body.turnoverBand || '< ₹20 Lakhs',
      geoLat: body.geoLat || 18.52,
      geoLng: body.geoLng || 73.85,
    };
    this.mockBusinesses.push(newBiz);
    return newBiz;
  }

  @Post('self-check')
  @ApiOperation({ summary: 'Private Business Packaging Self-Check (Confidential)' })
  privateSelfCheck(@Body() body: any) {
    return {
      selfCheckId: `sc_${Date.now()}`,
      businessId: body.businessId || 'biz_001',
      imageUrls: body.imageUrls || [],
      extractedFields: {
        mrp: 'Rs. 150.00 inclusive of all taxes',
        netQuantity: '500g',
        mfgDate: '08/2026',
        manufacturerAddress: 'Plot 42, MIDC, Pune',
      },
      violations: [
        {
          field_key: 'consumer_care',
          issue: 'Missing helpline phone number or email',
          act_section: 'Rule 6(1)(g)',
          rule_text: 'Consumer care helpline details mandatory on packaging',
          suggested_fix: 'Add text: Consumer Care: +91-1800-111-222, email: care@pickle.com',
        },
      ],
      overallStatus: 'NON_COMPLIANT',
      privacyNotice: 'Private check — this report is confidential and never visible to legal metrology inspectors.',
    };
  }
}
