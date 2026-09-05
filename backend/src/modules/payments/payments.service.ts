import { Injectable, BadRequestException } from '@nestjs/common';

export interface InitiatePaymentRequest {
  noticeId: string;
  caseId?: string;
  businessId: string;
  amount: number;
  currency?: string;
}

export interface RazorpayWebhookPayload {
  event: string;
  razorpay_event_id: string;
  payload: {
    payment?: {
      entity: {
        id: string;
        order_id: string;
        amount: number;
        currency: string;
        status: string;
      };
    };
  };
  razorpay_order_id?: string;
  razorpay_payment_id?: string;
  razorpay_signature?: string;
}

@Injectable()
export class PaymentsService {
  private paymentsStore: any[] = [];
  private processedEventsSet: Set<string> = new Set();

  initiatePayment(req: InitiatePaymentRequest) {
    const razorpayOrderId = `order_${Math.random().toString(36).substring(2, 12)}`;
    const payment = {
      id: `PAY-${Date.now()}`,
      noticeId: req.noticeId,
      caseId: req.caseId || null,
      businessId: req.businessId,
      amount: req.amount,
      currency: req.currency || 'INR',
      razorpayOrderId,
      razorpayPaymentId: null,
      razorpaySignature: null,
      razorpayEventId: null,
      status: 'INITIATED',
      createdAt: new Date(),
      paidAt: null,
    };
    this.paymentsStore.push(payment);
    return {
      paymentId: payment.id,
      caseId: payment.caseId,
      noticeId: payment.noticeId,
      razorpayOrderId,
      amount: req.amount,
      currency: payment.currency,
      key: process.env.RAZORPAY_KEY_ID || 'rzp_test_mock_key_123',
    };
  }

  handleWebhook(payload: RazorpayWebhookPayload) {
    const eventId = payload.razorpay_event_id || `event_${Date.now()}`;

    // Duplicate webhook protection
    if (this.processedEventsSet.has(eventId)) {
      console.warn(`[PaymentsService] Duplicate webhook event detected: ${eventId}. Skipping processing.`);
      return { status: 'IGNORED_DUPLICATE', razorpayEventId: eventId };
    }

    const orderId = payload.razorpay_order_id || payload.payload?.payment?.entity?.order_id;
    const paymentId = payload.razorpay_payment_id || payload.payload?.payment?.entity?.id;
    const signature = payload.razorpay_signature || null;

    const payment = this.paymentsStore.find((p) => p.razorpayOrderId === orderId);
    if (payment) {
      payment.status = 'PAID';
      payment.razorpayPaymentId = paymentId;
      payment.razorpaySignature = signature;
      payment.razorpayEventId = eventId;
      payment.paidAt = new Date();
    }

    this.processedEventsSet.add(eventId);

    return {
      status: 'SUCCESS',
      razorpayOrderId: orderId,
      razorpayPaymentId: paymentId,
      razorpayEventId: eventId,
      caseStatus: 'RESOLVED',
      paidAt: payment?.paidAt || new Date(),
    };
  }
}
