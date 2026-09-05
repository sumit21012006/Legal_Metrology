import { Injectable, BadRequestException } from '@nestjs/common';
import { AuditLogsService } from '../audit-logs/audit-logs.service';

export type CaseState = 'RECEIVED' | 'ASSIGNED' | 'INSPECTED' | 'NOTICE_ISSUED' | 'COMPOUNDED' | 'PROSECUTION' | 'RESOLVED';

@Injectable()
export class CaseWorkflowService {
  private readonly validTransitions: Record<CaseState, CaseState[]> = {
    RECEIVED: ['ASSIGNED'],
    ASSIGNED: ['INSPECTED'],
    INSPECTED: ['NOTICE_ISSUED', 'RESOLVED'],
    NOTICE_ISSUED: ['COMPOUNDED', 'PROSECUTION', 'RESOLVED'],
    COMPOUNDED: ['RESOLVED'],
    PROSECUTION: ['RESOLVED'],
    RESOLVED: [],
  };

  constructor(private readonly auditService: AuditLogsService) {}

  transitionState(caseId: string, currentState: CaseState, newState: CaseState, actorId: string): CaseState {
    const allowed = this.validTransitions[currentState] || [];
    if (!allowed.includes(newState)) {
      throw new BadRequestException(`Invalid state transition from ${currentState} to ${newState}. Allowed: ${allowed.join(', ')}`);
    }

    this.auditService.logAction(actorId, 'CASE_STATE_TRANSITION', { caseId, state: currentState }, { caseId, state: newState });
    return newState;
  }

  calculateDeadline(
    noticeType: 'IMPROVEMENT' | 'COMPOUNDED' | 'SEIZURE',
    issuedDate: Date = new Date(),
    customDays?: number,
    customDeadlineDate?: Date,
  ): Date {
    if (customDeadlineDate) {
      return new Date(customDeadlineDate);
    }

    const deadline = new Date(issuedDate);
    if (customDays !== undefined && customDays !== null && customDays > 0) {
      deadline.setDate(deadline.getDate() + customDays);
      return deadline;
    }

    // Default fallbacks if inspector does not specify custom days
    if (noticeType === 'IMPROVEMENT') {
      deadline.setDate(deadline.getDate() + 15);
    } else if (noticeType === 'COMPOUNDED') {
      deadline.setDate(deadline.getDate() + 30);
    } else {
      deadline.setDate(deadline.getDate() + 7);
    }
    return deadline;
  }

  calculateDaysRemaining(deadlineDate: Date): number {
    const now = new Date();
    const diffTime = deadlineDate.getTime() - now.getTime();
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  }
}
