import { Controller, Get, Post, Body, Param, Patch } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { CaseWorkflowService } from '../cases/case-workflow.service';
import { Neo4jService, MultiTierSupplyChainPayload } from '../../graph/neo4j.service';

@ApiTags('Controller & Officer Dashboard')
@Controller('api/v1/controller')
export class ControllerDashboardController {
  private compoundingQueue: any[] = [];
  private supplyChainLinksStore: any[] = [];

  constructor(
    private readonly workflowService: CaseWorkflowService,
    private readonly neo4jService: Neo4jService,
  ) {}

  @Get('dashboard/stats')
  @ApiOperation({ summary: 'Get statewide monitoring analytics and case metrics' })
  getDashboardStats() {
    return {
      totalComplaints: 142,
      firstOffencesCount: 89,
      secondOffencesCount: 18,
      compoundedCasesCount: 45,
      totalPenaltiesCollected: 1250000.0,
      activeInspectors: 24,
      regionCaseLoad: [
        { region: 'Mumbai City', activeCases: 42, resolvedCases: 110 },
        { region: 'Pune', activeCases: 28, resolvedCases: 85 },
        { region: 'Nagpur', activeCases: 15, resolvedCases: 40 },
      ],
    };
  }

  @Post('compounding/:id/action')
  @ApiOperation({ summary: 'Approve or Reject compounding order or escalate to prosecution' })
  compoundingAction(
    @Param('id') id: string,
    @Body() body: { action: 'APPROVE' | 'REJECT' | 'PROSECUTION'; comments?: string; officerId: string },
  ) {
    let nextState = 'RESOLVED';
    if (body.action === 'REJECT') nextState = 'INSPECTED';
    if (body.action === 'PROSECUTION') nextState = 'PROSECUTION';

    return {
      noticeId: id,
      actionTaken: body.action,
      newState: nextState,
      comments: body.comments || 'Action processed by Controller',
      timestamp: new Date(),
    };
  }

  @Post('supply-chain-links')
  @ApiOperation({ summary: 'Create a linked supply-chain violation case against a supplier' })
  async createSupplyChainLink(@Body() body: { retailerGstin: string; supplierGstin: string; inspectionId: string }) {
    const link = {
      id: `SCL-${Date.now()}`,
      ...body,
      status: 'LINKED',
      createdAt: new Date(),
    };
    this.supplyChainLinksStore.push(link);
    await this.neo4jService.linkSupplyChain(body.retailerGstin, body.supplierGstin, body.inspectionId);
    return link;
  }

  @Post('supply-chain/multi-tier')
  @ApiOperation({ summary: 'Create multi-tier Neo4j graph trace: Retailer -> Distributor -> Manufacturer' })
  async createMultiTierSupplyChain(@Body() payload: MultiTierSupplyChainPayload) {
    const result = await this.neo4jService.createMultiTierSupplyChain(payload);
    return {
      message: 'Multi-tier supply chain graph linked successfully in Neo4j',
      chain: `${payload.retailerName} (Retailer) -> ${payload.distributorName} (Distributor) -> ${payload.manufacturerName} (Manufacturer)`,
      graphResult: result,
    };
  }

  @Get('supply-chain/trace/:retailerGstin')
  @ApiOperation({ summary: 'Trace complete upstream supply chain from Retailer to Manufacturer in Neo4j' })
  async traceUpstreamSupplyChain(@Param('retailerGstin') retailerGstin: string) {
    const graphData = await this.neo4jService.getFullUpstreamGraph(retailerGstin);
    return {
      retailerGstin,
      traceResult: graphData,
    };
  }

  @Patch('supply-chain-links/:id/assign')
  @ApiOperation({ summary: 'Assign linked supplier case to jurisdiction inspector' })
  assignSupplyChainLink(@Param('id') id: string, @Body() body: { inspectorId: string }) {
    const link = this.supplyChainLinksStore.find((l) => l.id === id);
    if (link) {
      link.assignedInspectorId = body.inspectorId;
      link.status = 'ASSIGNED';
    }
    return link || { id, status: 'ASSIGNED', assignedInspectorId: body.inspectorId };
  }
}
