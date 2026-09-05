import { Injectable } from '@nestjs/common';

export interface InitiatePaymentRequest {
  noticeId: string;
  businessId: string;
  amount: number;
}

@Injectable()
export class PaymentsService {
  private paymentsStore: any[] = [];

  initiatePayment(req: InitiatePaymentRequest) {
    const razorpayOrderId = `order_${Math.random().toString(36).substring(2, 12)}`;
    const payment = {
      id: `PAY-${Date.now()}`,
      noticeId: req.noticeId,
      businessId: req.businessId,
      amount: req.amount,
      razorpayOrderId,
      status: 'INITIATED',
      createdAt: new Date(),
    };
    this.paymentsStore.push(payment);
    return {
      paymentId: payment.id,
      razorpayOrderId,
      amount: req.amount,
      currency: 'INR',
      key: process.env.RAZORPAY_KEY_ID || 'rzp_test_mock_key_123',
    };
  }

  handleWebhook(payload: any) {
    const orderId = payload.razorpay_order_id;
    const payment = this.paymentsStore.find((p) => p.razorpayOrderId === orderId);
    if (payment) {
      payment.status = 'PAID';
    }
    return { status: 'SUCCESS', razorpayOrderId: orderId, caseStatus: 'RESOLVED' };
  }
}
