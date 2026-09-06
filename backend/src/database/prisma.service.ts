import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  constructor() {
    super({
      log: ['query', 'info', 'warn', 'error'],
    });
  }

  async onModuleInit() {
    try {
      await this.$connect();
      console.log('[PrismaService] Connected to PostgreSQL Database');
    } catch (err) {
      console.warn('[PrismaService] PostgreSQL connection deferred (database offline or running in mock mode):', err.message);
    }
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}
