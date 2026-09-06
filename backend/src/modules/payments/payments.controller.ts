import { Controller, Post, Get, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { PaymentsService, InitiatePaymentRequest, RazorpayWebhookPayload } from './payments.service';

@ApiTags('Razorpay Penalty Payments')
@Controller('api/v1/payments')
export class PaymentsController {
  constructor(private readonly paymentsService: PaymentsService) {}

  @Post('initiate')
  @ApiOperation({ summary: 'Initiate Razorpay payment order for a notice penalty' })
  initiatePayment(@Body() body: InitiatePaymentRequest) {
    return this.paymentsService.initiatePayment(body);
  }

  @Post('webhook')
  @ApiOperation({ summary: 'Razorpay webhook callback endpoint with deduplication protection' })
  handleWebhook(@Body() payload: RazorpayWebhookPayload) {
    return this.paymentsService.handleWebhook(payload);
  }

  @Get()
  @ApiOperation({ summary: 'List payment history for business' })
  listPayments() {
    return [
      {
        id: 'pay_1001',
        caseId: 'CASE-1001',
        description: 'Compounding penalty payment under Section 36(1)',
        amount: 25000.0,
        status: 'PAID',
        createdAt: new Date().toISOString(),
        completedAt: new Date().toISOString(),
        receiptUrl: 'https://storage.local/receipts/pay_1001.pdf',
      },
    ];
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get details of a specific payment' })
  getPaymentStatus(@Param('id') id: string) {
    return {
      id: id,
      caseId: 'CASE-1001',
      description: 'Compounding penalty payment under Section 36(1)',
      amount: 25000.0,
      status: 'PAID',
      createdAt: new Date().toISOString(),
      completedAt: new Date().toISOString(),
      receiptUrl: `https://storage.local/receipts/${id}.pdf`,
    };
  }
}
