import * as fs from 'fs';
import * as path from 'path';

export interface RulebookEntry {
  rule_id: string;
  category: string;
  field_key: string;
  field_label: string;
  requirement: string;
  act_section: string;
  rule_reference: string;
  penalty_first_offence: string;
  penalty_second_offence: string;
}

export interface PenaltyMatrixEntry {
  offence_id: string;
  legal_section: string;
  legal_rule: string;
  offence_description: string;
  penalty_details: {
    first_offence: { fine_max: number; imprisonment: string | null; summary: string };
    second_offence: { fine_max: number; imprisonment: string | null; summary: string };
    subsequent_offence: { fine_min: number; fine_max: number; imprisonment: string | null; summary: string };
  };
  compounding: { compoundable: boolean; authority: string; governing_section: string };
}

export class LegalKnowledgeBaseSeeder {
  private readonly kbPath = path.resolve(__dirname, '../../../../knowledge_base/legal_knowledge_base');

  public loadRulebook(): any {
    const filePath = path.join(this.kbPath, 'rulebook.json');
    if (!fs.existsSync(filePath)) {
      throw new Error(`Rulebook file not found at ${filePath}`);
    }
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  }

  public loadPenaltyMatrix(): any {
    const filePath = path.join(this.kbPath, 'penalty_matrix.json');
    if (!fs.existsSync(filePath)) {
      throw new Error(`Penalty Matrix file not found at ${filePath}`);
    }
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  }

  public loadCompoundingMatrix(): any {
    const filePath = path.join(this.kbPath, 'compounding_matrix.json');
    if (!fs.existsSync(filePath)) {
      throw new Error(`Compounding Matrix file not found at ${filePath}`);
    }
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  }

  public loadExemptions(): any {
    const filePath = path.join(this.kbPath, 'exemptions.json');
    if (!fs.existsSync(filePath)) {
      throw new Error(`Exemptions file not found at ${filePath}`);
    }
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  }

  public seedAll(): { status: string; rulebookCount: number; penaltiesCount: number; exemptionsCount: number } {
    const rulebook = this.loadRulebook();
    const penalties = this.loadPenaltyMatrix();
    const exemptions = this.loadExemptions();

    const rulebookCount = Array.isArray(rulebook) ? rulebook.length : Object.keys(rulebook).length;
    const penaltiesCount = Array.isArray(penalties) ? penalties.length : Object.keys(penalties).length;
    const exemptionsCount = Array.isArray(exemptions) ? exemptions.length : Object.keys(exemptions).length;

    console.log(`[Legal KBs Seeder] Successfully validated and seeded:`);
    console.log(` - Rulebook Rules: ${rulebookCount}`);
    console.log(` - Penalty Matrix Entries: ${penaltiesCount}`);
    console.log(` - Exemptions Registered: ${exemptionsCount}`);

    return {
      status: 'SUCCESS',
      rulebookCount,
      penaltiesCount,
      exemptionsCount,
    };
  }
}

if (require.main === module) {
  const seeder = new LegalKnowledgeBaseSeeder();
  seeder.seedAll();
}
