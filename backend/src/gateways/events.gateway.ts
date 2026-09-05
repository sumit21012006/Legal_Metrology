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
    return { status: 'SUBSCRIBED', complaintId: data.complaintId };
  }

  notifyComplaintStatusChange(complaintId: string, status: string) {
    if (this.server) {
      this.server.to(`complaint_${complaintId}`).emit('complaint_updated', { complaintId, status, timestamp: new Date() });
    }
  }
}
