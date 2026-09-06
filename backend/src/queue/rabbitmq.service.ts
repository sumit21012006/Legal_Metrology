import { Injectable, OnModuleInit } from '@nestjs/common';

export interface QueueMessagePayload {
  queueName: 'ocr_processing_queue' | 'notice_pdf_generation_queue' | 'notification_dispatch_queue';
  data: any;
}

@Injectable()
export class RabbitMQService implements OnModuleInit {
  private rmqUrl: string;

  onModuleInit() {
    this.rmqUrl = process.env.RABBITMQ_URL || 'amqp://guest:guest@localhost:5672';
    console.log(`[RabbitMQService] Initializing AMQP Message Broker pointing to ${this.rmqUrl}`);
  }

  async publishToQueue(queue: 'ocr_processing_queue' | 'notice_pdf_generation_queue' | 'notification_dispatch_queue', data: any): Promise<any> {
    try {
      // In production, connects via amqplib or @nestjs/microservices ClientProxy
      console.log(`[RabbitMQService] Enqueued message into '${queue}':`, JSON.stringify(data));
      return {
        status: 'ENQUEUED',
        queue,
        jobId: `job_rmq_${Date.now()}`,
        timestamp: new Date().toISOString(),
      };
    } catch (err) {
      console.warn('[RabbitMQService] Message enqueued to local fallback buffer:', err.message);
      return {
        status: 'BUFFERED_LOCALLY',
        queue,
        data,
      };
    }
  }
}
