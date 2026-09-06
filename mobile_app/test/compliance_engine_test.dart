import 'package:flutter_test/flutter_test.dart';
import 'package:legal_metrology/models/ocr_result.dart';
import 'package:legal_metrology/models/violation.dart';
import 'package:legal_metrology/services/compliance_engine.dart';

void main() {
  group('ComplianceEngine statutory rulebook checks', () {
    late ComplianceEngine engine;

    setUp(() {
      engine = ComplianceEngine();
    });

    test('detects missing consumer care under Rule 6(2)', () {
      final fields = [
        const ExtractedField(key: OcrFieldKeys.productName, label: 'Product Name', value: 'Mango Pickle', confidence: 0.95),
        const ExtractedField(key: OcrFieldKeys.mrp, label: 'MRP', value: 'Rs. 150 (inclusive of all taxes)', confidence: 0.96),
        const ExtractedField(key: OcrFieldKeys.netQuantity, label: 'Net Qty', value: '500g', confidence: 0.95),
        const ExtractedField(key: OcrFieldKeys.manufacturingDate, label: 'Mfg Date', value: '08/2026', confidence: 0.94),
        const ExtractedField(key: OcrFieldKeys.consumerCare, label: 'Consumer Care', value: '', confidence: 0.0, isMissing: true),
      ];

      final violations = engine.evaluateDeclarations(fields: fields, inspectionId: 'insp-1');
      expect(violations.any((v) => v.type == ViolationType.consumerCareIssue), isTrue);
      final careViol = violations.firstWhere((v) => v.type == ViolationType.consumerCareIssue);
      expect(careViol.ruleSection, contains('Rule 6(2)'));
      expect(careViol.ruleSection, contains('Section 18'));
    });

    test('detects missing MRP under Rule 6(1)(e)', () {
      final fields = [
        const ExtractedField(key: OcrFieldKeys.productName, label: 'Product Name', value: 'Mango Pickle', confidence: 0.95),
        const ExtractedField(key: OcrFieldKeys.mrp, label: 'MRP', value: '', confidence: 0.0, isMissing: true),
        const ExtractedField(key: OcrFieldKeys.consumerCare, label: 'Consumer Care', value: '1800-111-222', confidence: 0.95),
      ];

      final violations = engine.evaluateDeclarations(fields: fields, inspectionId: 'insp-2');
      expect(violations.any((v) => v.type == ViolationType.missingMrp), isTrue);
      final mrpViol = violations.firstWhere((v) => v.type == ViolationType.missingMrp);
      expect(mrpViol.ruleSection, contains('Rule 6(1)(e)'));
      expect(mrpViol.severity, ViolationSeverity.high);
    });

    test('detects non-compliant MRP formatting without inclusive of all taxes', () {
      final fields = [
        const ExtractedField(key: OcrFieldKeys.productName, label: 'Product Name', value: 'Mango Pickle', confidence: 0.95),
        const ExtractedField(key: OcrFieldKeys.mrp, label: 'MRP', value: 'Rs. 150', confidence: 0.90),
        const ExtractedField(key: OcrFieldKeys.consumerCare, label: 'Consumer Care', value: 'care@pickle.com', confidence: 0.95),
      ];

      final violations = engine.evaluateDeclarations(fields: fields, inspectionId: 'insp-3');
      expect(violations.any((v) => v.type == ViolationType.incorrectMrp), isTrue);
    });

    test('detects missing Country of Origin under Rule 6(1)(aa)', () {
      final fields = [
        const ExtractedField(key: OcrFieldKeys.productName, label: 'Product Name', value: 'Imported Chocolates', confidence: 0.95),
        const ExtractedField(key: OcrFieldKeys.countryOfOrigin, label: 'Country of Origin', value: '', confidence: 0.0, isMissing: true),
      ];

      final violations = engine.evaluateDeclarations(fields: fields, inspectionId: 'insp-4');
      expect(violations.any((v) => v.type == ViolationType.missingOrigin), isTrue);
      final originViol = violations.firstWhere((v) => v.type == ViolationType.missingOrigin);
      expect(originViol.ruleSection, contains('Rule 6(1)(aa)'));
    });

    test('detects expired product relative to current date and assigns critical severity', () {
      final fields = [
        const ExtractedField(key: OcrFieldKeys.productName, label: 'Product Name', value: 'Whole Wheat Pasta', confidence: 0.96),
        const ExtractedField(key: OcrFieldKeys.mrp, label: 'MRP', value: 'Rs. 149.00 (incl. of all taxes)', confidence: 0.98),
        const ExtractedField(key: OcrFieldKeys.expiryOrUseBy, label: 'Expiry Date', value: '14 Oct 2025', confidence: 0.98),
      ];

      final violations = engine.evaluateDeclarations(fields: fields, inspectionId: 'insp-expired');
      expect(violations.any((v) => v.ruleTitle?.contains('Expired') == true), isTrue);
      final expViol = violations.firstWhere((v) => v.ruleTitle?.contains('Expired') == true);
      expect(expViol.severity, ViolationSeverity.critical);
      expect(expViol.description, contains('EXPIRED PRODUCT'));
      expect(expViol.ruleSection, contains('Rule 6(1)(da)'));
    });

    test('detects solid commodity declared in volume units (Pasta in Litre) under Rule 11 & 12', () {
      final fields = [
        const ExtractedField(key: OcrFieldKeys.productName, label: 'Product Name', value: 'Artisan Harvest Whole Wheat Pasta', confidence: 0.96),
        const ExtractedField(key: OcrFieldKeys.netQuantity, label: 'Net Qty', value: '1 Litre', unit: 'Litre', confidence: 0.98),
      ];

      final violations = engine.evaluateDeclarations(fields: fields, inspectionId: 'insp-vol');
      expect(violations.any((v) => v.type == ViolationType.nonStandardUnits), isTrue);
      final volViol = violations.firstWhere((v) => v.type == ViolationType.nonStandardUnits);
      expect(volViol.ruleSection, contains('Rule 11 & Rule 12'));
      expect(volViol.description, contains('Solid commodity'));
    });

    test('OcrResult helper getters resolve parsed packaging declarations accurately', () {
      final ocr = OcrResult(
        jobId: 'job-1',
        status: OcrStatus.completed,
        analyzedAt: DateTime.now(),
        fields: const [
          ExtractedField(key: OcrFieldKeys.productName, label: 'Product Name', value: 'ARTISAN HARVEST WHOLE WHEAT PASTA', confidence: 0.98),
          ExtractedField(key: OcrFieldKeys.genericName, label: 'Generic Name', value: 'Whole Wheat Pasta', confidence: 0.96),
          ExtractedField(key: OcrFieldKeys.netQuantity, label: 'Net Quantity', value: '1 Litre', unit: 'Litre', confidence: 0.99),
          ExtractedField(key: OcrFieldKeys.mrp, label: 'MRP', value: 'Rs. 149.00 (Incl. of all taxes)', confidence: 0.99),
          ExtractedField(key: OcrFieldKeys.batchOrLot, label: 'Batch Number', value: 'AH231015B', confidence: 0.97),
          ExtractedField(key: OcrFieldKeys.manufacturingDate, label: 'Date of Mfg', value: '15 Oct 2023', confidence: 0.96),
          ExtractedField(key: OcrFieldKeys.expiryOrUseBy, label: 'Best Before', value: '14 Oct 2025', confidence: 0.96),
          ExtractedField(key: OcrFieldKeys.manufacturer, label: 'Manufacturer', value: 'ARTISAN FOODS PVT. LTD., Survey No. 45/2, Kelva', confidence: 0.97),
          ExtractedField(key: OcrFieldKeys.consumerCare, label: 'Consumer Care', value: 'care@artisanharvest.com', confidence: 0.95),
        ],
      );

      expect(ocr.productName, 'ARTISAN HARVEST WHOLE WHEAT PASTA');
      expect(ocr.genericName, 'Whole Wheat Pasta');
      expect(ocr.netQuantity, '1 Litre');
      expect(ocr.mrp, 'Rs. 149.00 (Incl. of all taxes)');
      expect(ocr.batchNumber, 'AH231015B');
      expect(ocr.manufacturingDate, '15 Oct 2023');
      expect(ocr.expiryDate, '14 Oct 2025');
      expect(ocr.manufacturerDetails, contains('ARTISAN FOODS'));
      expect(ocr.consumerCare, 'care@artisanharvest.com');
    });
  });
}
