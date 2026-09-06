import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  MessageBody,
  ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({ cors: { origin: '*' } })
export class EventsGateway {
  @WebSocketServer()
  server: Server;

  @SubscribeMessage('subscribe_complaint')
  handleSubscribeComplaint(@MessageBody() data: { complaintId: string }, @ConnectedSocket() client: Socket) {
    client.join(`complaint_${data.complaintId}`);
    return { status: 'SUBSCRIBED', room: `complaint_${data.complaintId}` };
  }

  @SubscribeMessage('subscribe_inspector')
  handleSubscribeInspector(@MessageBody() data: { inspectorId: string }, @ConnectedSocket() client: Socket) {
    client.join(`inspector_${data.inspectorId}`);
    return { status: 'SUBSCRIBED', room: `inspector_${data.inspectorId}` };
  }

  @SubscribeMessage('subscribe_business')
  handleSubscribeBusiness(@MessageBody() data: { businessId: string }, @ConnectedSocket() client: Socket) {
    client.join(`business_${data.businessId}`);
    return { status: 'SUBSCRIBED', room: `business_${data.businessId}` };
  }

  notifyComplaintStatusChange(complaintId: string, status: string) {
    if (this.server) {
      this.server.to(`complaint_${complaintId}`).emit('complaint_updated', { complaintId, status, timestamp: new Date() });
    }
  }

  notifyInspectionAssigned(inspectorId: string, inspectionData: any) {
    if (this.server) {
      this.server.to(`inspector_${inspectorId}`).emit('inspection_assigned', { inspectionData, timestamp: new Date() });
    }
  }

  notifyNoticeIssued(businessId: string, noticeData: any) {
    if (this.server) {
      this.server.to(`business_${businessId}`).emit('notice_issued', { noticeData, timestamp: new Date() });
    }
  }

  notifyPaymentReceived(businessId: string, paymentData: any) {
    if (this.server) {
      this.server.to(`business_${businessId}`).emit('payment_received', { paymentData, timestamp: new Date() });
    }
  }
}
