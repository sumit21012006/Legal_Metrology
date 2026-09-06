import { Controller, Post, Body } from '@nestjs/common';
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
}
