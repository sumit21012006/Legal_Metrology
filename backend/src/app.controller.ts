import { Controller, Get, Res } from '@nestjs/common';
import { ApiExcludeEndpoint } from '@nestjs/swagger';
import type { Response } from 'express';

@Controller()
export class AppController {
  @Get()
  @ApiExcludeEndpoint()
  getRoot(@Res() res: Response) {
    return res.json({
      service: 'Legal Metrology Automated Compliance & Enforcement API Gateway (SIH PS 34)',
      status: 'ONLINE',
      mode: 'In-Memory Mock Active (PostgreSQL/MinIO deferred for presentation demo)',
      endpoints: {
        swaggerDocs: 'http://localhost:3000/api/docs',
        systemHealth: 'http://localhost:3000/api/v1/health/system-check',
        webFrontend: 'http://localhost:3001',
      },
      message: 'Visit /api/docs in your browser to view and test all interactive REST APIs.',
    });
  }
}
