import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { KnowledgeBaseModule } from './modules/knowledge-base/knowledge-base.module';
import { OffenceCalculatorService } from './modules/offences/offence-calculator.service';
import { NoticeGeneratorService } from './modules/notices/notice-generator.service';
import { CaseWorkflowService } from './modules/cases/case-workflow.service';
import { AuditLogsService } from './modules/audit-logs/audit-logs.service';
import { ComplaintsController } from './modules/complaints/complaints.controller';
import { ControllerDashboardController } from './modules/controller/controller.controller';
import { MinioStorageService } from './storage/minio.service';
import { Neo4jService } from './graph/neo4j.service';
import { PaymentsService } from './modules/payments/payments.service';
import { EventsGateway } from './gateways/events.gateway';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    KnowledgeBaseModule,
  ],
  controllers: [
    ComplaintsController,
    ControllerDashboardController,
  ],
  providers: [
    OffenceCalculatorService,
    NoticeGeneratorService,
    CaseWorkflowService,
    AuditLogsService,
    MinioStorageService,
    Neo4jService,
    PaymentsService,
    EventsGateway,
  ],
})
export class AppModule {}
