import { Controller, Post, Get, Body, Param, Query } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { CaseWorkflowService, CaseState } from '../cases/case-workflow.service';

export class FileComplaintDto {
  citizenId: string;
  retailerNameText: string;
  retailerAddressText: string;
  category: string;
  description: string;
  photoUrls: string[];
  invoiceUrl?: string;
}

@ApiTags('Citizen Complaints')
@Controller('api/v1/complaints')
export class ComplaintsController {
  private complaintsStore: any[] = [];

  constructor(private readonly workflowService: CaseWorkflowService) {}

  @Post()
  @ApiOperation({ summary: 'File a new citizen complaint against a product or retailer' })
  fileComplaint(@Body() dto: FileComplaintDto) {
    const newComplaint = {
      id: `CMP-${Date.now()}`,
      ...dto,
      status: 'RECEIVED' as CaseState,
      incentiveStatus: 'PENDING',
      createdAt: new Date(),
    };
    this.complaintsStore.push(newComplaint);
    return {
      message: 'Complaint registered successfully',
      complaintId: newComplaint.id,
      status: newComplaint.status,
    };
  }

  @Get(':id/status')
  @ApiOperation({ summary: 'Get step-by-step status tracker for a complaint' })
  getComplaintStatus(@Param('id') id: string) {
    const cmp = this.complaintsStore.find((c) => c.id === id);
    if (!cmp) {
      return {
        id,
        status: 'RECEIVED',
        stepper: ['RECEIVED', 'ASSIGNED', 'INSPECTED', 'NOTICE_ISSUED', 'RESOLVED'],
        currentStep: 0,
        incentiveStatus: 'PENDING',
      };
    }
    const stepper = ['RECEIVED', 'ASSIGNED', 'INSPECTED', 'NOTICE_ISSUED', 'RESOLVED'];
    return {
      id: cmp.id,
      status: cmp.status,
      stepper,
      currentStep: stepper.indexOf(cmp.status) >= 0 ? stepper.indexOf(cmp.status) : 0,
      incentiveStatus: cmp.incentiveStatus,
      retailer: cmp.retailerNameText,
    };
  }

  @Get()
  @ApiOperation({ summary: 'List complaints for inspector/controller region queue' })
  listComplaints(@Query('region') region?: string) {
    return this.complaintsStore;
  }
}
