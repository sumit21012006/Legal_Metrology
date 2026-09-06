import { Injectable } from '@nestjs/common';
import * as fs from 'fs';
import * as path from 'path';

export interface NoticePlaceholderData {
  NOTICE_ID: string;
  CASE_ID: string;
  BUSINESS_NAME: string;
  BUSINESS_ADDRESS: string;
  INSPECTOR_NAME: string;
  INSPECTOR_ID: string;
  INSPECTION_DATE: string;
  PRODUCT_NAME: string;
  MANUFACTURER_NAME: string;
  BATCH_NUMBER?: string;
  MRP?: string;
  NET_QUANTITY?: string;
  OBSERVED_VIOLATION: string;
  LEGAL_SECTION: string;
  LEGAL_RULE: string;
  PENALTY: string;
  DEADLINE: string;
  EVIDENCE_REFERENCE?: string;
  WITNESS_1?: string;
  WITNESS_2?: string;
  SAMPLE_ID?: string;
  COMPOUNDING_AMOUNT?: string;
  OFFICER_AUTHORITY?: string;
  DATE: string;
  PLACE: string;
}

@Injectable()
export class NoticeGeneratorService {
  private readonly noticePath = path.resolve(__dirname, '../../../../knowledge_base/legal_knowledge_base/notices');
  private readonly officialTemplatesPath = path.resolve(__dirname, '../../../../Notices_Template');

  getOfficialTemplatePath(type: 'improvement' | 'seizure' | 'panchanama' | 'compounding'): string {
    const templateMap: Record<string, string> = {
      improvement: 'Improvement_Notice_Template.docx',
      seizure: 'Seizure_Bill_English_Template.docx',
      panchanama: 'Panchanama_Template.docx',
      compounding: 'Compounding_Order_Template.docx',
    };
    const fileName = templateMap[type] || 'Improvement_Notice_Template.docx';
    return path.join(this.officialTemplatesPath, fileName);
  }

  renderNotice(type: 'improvement' | 'seizure' | 'panchanama' | 'compounding', lang: 'en' | 'mr', data: NoticePlaceholderData): string {
    const filename = `notice_${type}_${lang}.md`;
    const folder = type;
    const filePath = path.join(this.noticePath, folder, filename);

    let template = '';
    if (fs.existsSync(filePath)) {
      template = fs.readFileSync(filePath, 'utf8');
    } else {
      template = `# OFFICIAL NOTICE OF ${type.toUpperCase()}\n\nNotice Serial: {{NOTICE_ID}}\nCase ID: {{CASE_ID}}\nIssued To: {{BUSINESS_NAME}}, {{BUSINESS_ADDRESS}}\nViolation: {{OBSERVED_VIOLATION}}\nUnder Section: {{LEGAL_SECTION}}\nDeadline: {{DEADLINE}}\nIssued By: {{INSPECTOR_NAME}} (ID: {{INSPECTOR_ID}})`;
    }

    // Replace 24 placeholders dynamically
    Object.keys(data).forEach((key) => {
      const val = data[key] || '';
      const regex = new RegExp(`{{${key}}}`, 'g');
      template = template.replace(regex, val);
    });

    return template;
  }
}
