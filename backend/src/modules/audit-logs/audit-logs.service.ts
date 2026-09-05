import { Injectable } from '@nestjs/common';
import * as crypto from 'crypto';

export interface AuditEntry {
  id: string;
  actorId?: string;
  action: string;
  previousState?: string;
  newState?: string;
  ipAddress?: string;
  hash: string;
  timestamp: Date;
}

@Injectable()
export class AuditLogsService {
  private auditLogs: AuditEntry[] = [];

  logAction(actorId: string, action: string, previousState?: any, newState?: any, ipAddress?: string): AuditEntry {
    const timestamp = new Date();
    const prevStr = previousState ? JSON.stringify(previousState) : '';
    const newStr = newState ? JSON.stringify(newState) : '';
    
    const hashData = `${actorId}:${action}:${prevStr}:${newStr}:${timestamp.toISOString()}`;
    const hash = crypto.createHash('sha256').update(hashData).digest('hex');

    const entry: AuditEntry = {
      id: crypto.randomUUID(),
      actorId,
      action,
      previousState: prevStr,
      newState: newStr,
      ipAddress,
      hash,
      timestamp,
    };

    this.auditLogs.push(entry);
    console.log(`[Anti-Corruption Audit] Action: ${action} | Actor: ${actorId} | Hash: ${hash.substring(0, 12)}...`);
    return entry;
  }

  getAuditLogs(): AuditEntry[] {
    return this.auditLogs;
  }
}
