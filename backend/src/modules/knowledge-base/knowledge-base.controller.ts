import { Controller, Get, Param } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { KnowledgeBaseService } from './knowledge-base.service';

@ApiTags('Legal Knowledge Base')
@Controller('api/v1/knowledge-base')
export class KnowledgeBaseController {
  constructor(private readonly kbService: KnowledgeBaseService) {}

  @Get('rulebook')
  @ApiOperation({ summary: 'Get full legal rulebook (Rules 1-34 & Schedules)' })
  @ApiResponse({ status: 200, description: 'Returns structured rulebook data' })
  getRulebook() {
    return this.kbService.getRulebook();
  }

  @Get('penalties')
  @ApiOperation({ summary: 'Get penalty matrix (Sections 24-43 & Rule 32)' })
  @ApiResponse({ status: 200, description: 'Returns statutory penalties details' })
  getPenaltyMatrix() {
    return this.kbService.getPenaltyMatrix();
  }

  @Get('penalties/:section')
  @ApiOperation({ summary: 'Get penalty details for a specific legal section' })
  getPenaltyBySection(@Param('section') section: string) {
    return this.kbService.getPenaltyBySection(section);
  }

  @Get('compounding')
  @ApiOperation({ summary: 'Get compounding matrix & Section 48 rules' })
  getCompoundingMatrix() {
    return this.kbService.getCompoundingMatrix();
  }

  @Get('exemptions')
  @ApiOperation({ summary: 'Get statutory exemption rules (Rule 26 & Rule 3)' })
  getExemptions() {
    return this.kbService.getExemptions();
  }
}
