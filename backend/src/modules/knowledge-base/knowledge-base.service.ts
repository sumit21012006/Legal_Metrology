import { Injectable, OnModuleInit } from '@nestjs/common';
import * as fs from 'fs';
import * as path from 'path';

@Injectable()
export class KnowledgeBaseService implements OnModuleInit {
  private rulebook: any = null;
  private penaltyMatrix: any = null;
  private compoundingMatrix: any = null;
  private exemptions: any = null;

  private readonly kbPath = path.resolve(__dirname, '../../../../knowledge_base/legal_knowledge_base');

  onModuleInit() {
    this.reloadKnowledgeBase();
  }

  public reloadKnowledgeBase() {
    try {
      const rulebookPath = path.join(this.kbPath, 'rulebook.json');
      if (fs.existsSync(rulebookPath)) {
        this.rulebook = JSON.parse(fs.readFileSync(rulebookPath, 'utf8'));
      }

      const penaltyPath = path.join(this.kbPath, 'penalty_matrix.json');
      if (fs.existsSync(penaltyPath)) {
        this.penaltyMatrix = JSON.parse(fs.readFileSync(penaltyPath, 'utf8'));
      }

      const compoundingPath = path.join(this.kbPath, 'compounding_matrix.json');
      if (fs.existsSync(compoundingPath)) {
        this.compoundingMatrix = JSON.parse(fs.readFileSync(compoundingPath, 'utf8'));
      }

      const exemptionsPath = path.join(this.kbPath, 'exemptions.json');
      if (fs.existsSync(exemptionsPath)) {
        this.exemptions = JSON.parse(fs.readFileSync(exemptionsPath, 'utf8'));
      }
    } catch (error) {
      console.error('[KnowledgeBaseService] Failed to load legal data:', error.message);
    }
  }

  getRulebook() {
    return this.rulebook || [];
  }

  getPenaltyMatrix() {
    return this.penaltyMatrix || [];
  }

  getCompoundingMatrix() {
    return this.compoundingMatrix || [];
  }

  getExemptions() {
    return this.exemptions || [];
  }

  getPenaltyBySection(legalSection: string) {
    if (!this.penaltyMatrix) return null;
    const items = Array.isArray(this.penaltyMatrix) ? this.penaltyMatrix : Object.values(this.penaltyMatrix);
    return items.find((item: any) => item.legal_section === legalSection || item.offence_id === legalSection) || null;
  }
}
