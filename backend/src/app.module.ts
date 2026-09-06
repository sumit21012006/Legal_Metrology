import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { KnowledgeBaseModule } from './modules/knowledge-base/knowledge-base.module';
import { PrismaModule } from './database/prisma.module';
import { AuthController } from './modules/auth/auth.controller';
import { BusinessesController } from './modules/businesses/businesses.controller';
import { InspectionsController } from './modules/inspections/inspections.controller';
import { NoticesController } from './modules/notices/notices.controller';
import { ComplaintsController } from './modules/complaints/complaints.controller';
import { ControllerDashboardController } from './modules/controller/controller.controller';
import { PaymentsController } from './modules/payments/payments.controller';
import { CasesController } from './modules/cases/cases.controller';
import { SelfChecksController } from './modules/self-checks/self-checks.controller';
import { SystemHealthController } from './modules/health/system-health.controller';
import { OcrController } from './modules/ocr/ocr.controller';
import { ViolationsController } from './modules/violations/violations.controller';
import { OffenceCalculatorService } from './modules/offences/offence-calculator.service';
import { NoticeGeneratorService } from './modules/notices/notice-generator.service';
import { CaseWorkflowService } from './modules/cases/case-workflow.service';
import { AuditLogsService } from './modules/audit-logs/audit-logs.service';
import { MinioStorageService } from './storage/minio.service';
import { Neo4jService } from './graph/neo4j.service';
import { PaymentsService } from './modules/payments/payments.service';
import { EventsGateway } from './gateways/events.gateway';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    KnowledgeBaseModule,
    PrismaModule,
  ],
  controllers: [
    AuthController,
    BusinessesController,
    InspectionsController,
    NoticesController,
    ComplaintsController,
    ControllerDashboardController,
    PaymentsController,
    CasesController,
    SelfChecksController,
    SystemHealthController,
    OcrController,
    ViolationsController,
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
