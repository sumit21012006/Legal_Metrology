import { Injectable } from '@nestjs/common';
import { KnowledgeBaseService } from '../knowledge-base/knowledge-base.service';

export interface OffenceEvaluationRequest {
  productName: string;
  manufacturerName: string;
  legalSection: string;
  businessId: string;
}

export interface OffenceEvaluationResult {
  offenceNumber: number;
  offenceTier: 'FIRST_OFFENCE' | 'SECOND_OFFENCE' | 'SUBSEQUENT_OFFENCE';
  fineMin: number;
  fineMax: number;
  imprisonment: string | null;
  legalSection: string;
  governingSection: string;
  compoundable: boolean;
}

@Injectable()
export class OffenceCalculatorService {
  private offenceHistory: { productName: string; manufacturerName: string; date: Date }[] = [];

  constructor(private readonly kbService: KnowledgeBaseService) {}

  evaluateOffence(request: OffenceEvaluationRequest): OffenceEvaluationResult {
    const normProduct = request.productName.toLowerCase().trim();
    const normManufacturer = request.manufacturerName.toLowerCase().trim();

    // Check past violations for identical product + manufacturer
    const pastMatches = this.offenceHistory.filter(
      (item) => item.productName === normProduct && item.manufacturerName === normManufacturer,
    );

    const offenceNumber = pastMatches.length + 1;
    this.offenceHistory.push({ productName: normProduct, manufacturerName: normManufacturer, date: new Date() });

    const penaltyInfo = this.kbService.getPenaltyBySection(request.legalSection) || {
      penalty_details: {
        first_offence: { fine_max: 25000, imprisonment: null },
        second_offence: { fine_max: 50000, imprisonment: null },
        subsequent_offence: { fine_min: 50000, fine_max: 100000, imprisonment: 'Up to 1 year' },
      },
      compounding: { compoundable: true, governing_section: 'Section 48(1)' },
    };

    let tier: 'FIRST_OFFENCE' | 'SECOND_OFFENCE' | 'SUBSEQUENT_OFFENCE' = 'FIRST_OFFENCE';
    let fineMin = 0;
    let fineMax = penaltyInfo.penalty_details?.first_offence?.fine_max || 25000;
    let imprisonment = penaltyInfo.penalty_details?.first_offence?.imprisonment || null;

    if (offenceNumber === 2) {
      tier = 'SECOND_OFFENCE';
      fineMax = penaltyInfo.penalty_details?.second_offence?.fine_max || 50000;
      imprisonment = penaltyInfo.penalty_details?.second_offence?.imprisonment || null;
    } else if (offenceNumber >= 3) {
      tier = 'SUBSEQUENT_OFFENCE';
      fineMin = penaltyInfo.penalty_details?.subsequent_offence?.fine_min || 50000;
      fineMax = penaltyInfo.penalty_details?.subsequent_offence?.fine_max || 100000;
      imprisonment = penaltyInfo.penalty_details?.subsequent_offence?.imprisonment || 'Up to 1 year';
    }

    return {
      offenceNumber,
      offenceTier: tier,
      fineMin,
      fineMax,
      imprisonment,
      legalSection: request.legalSection,
      governingSection: penaltyInfo.compounding?.governing_section || 'Section 48(1)',
      compoundable: penaltyInfo.compounding?.compoundable ?? true,
    };
  }
}
