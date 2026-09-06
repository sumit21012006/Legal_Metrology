import 'package:flutter_test/flutter_test.dart';
import 'package:legal_metrology/models/ocr_result.dart';
import 'package:legal_metrology/services/ocr_service.dart';

void main() {
  group('OcrService generalized anchor-keyword extraction', () {
    test('accurately extracts all declarations from Pasta package input', () {
      const pastaText = '''
ARTISAN HARVEST WHOLE WHEAT PASTA
BATCH NO & DATE OF MFG
Net Volume: 1 Litre
Batch Number: AH231015B
Date of Manufacture: 15 Oct 2023
MRP Rs. 149.00
(Incl. of all taxes)
Best Before: 14 Oct 2025
MANUFACTURER DETAILS
For Consumer Feedback, contact Manufacturer
Address or Email: care@artisanharvest.com
Manufactured & Packed By:
ARTISAN FOODS PVT. LTD.
Survey No. 45/2, Village Kelva,
Off Mumbai-Ahmedabad Highway,
Taluka Palghar, Thane District,
Maharashtra - 401 401, India.
FSSAI Lic No. 11518018000123
8 901234 567890
''';

      final fields = OcrService.parsePackagingDeclarations(pastaText);
      final ocr = OcrResult(
        jobId: 'test-pasta',
        status: OcrStatus.completed,
        analyzedAt: DateTime.now(),
        fields: fields,
      );

      // 1. Product Name should be the title, not FSSAI or header
      expect(ocr.productName, 'ARTISAN HARVEST WHOLE WHEAT PASTA');
      expect(ocr.genericName, anyOf(contains('Whole Wheat Pasta'), contains('Pasta')));

      // 2. MRP
      expect(ocr.mrp, contains('149.00'));
      expect(ocr.mrp, contains('incl. of all taxes'));

      // 3. Net Quantity
      expect(ocr.netQuantity, contains('1'));
      expect(ocr.netQuantity, contains('Litre'));

      // 4. Mfg Date
      expect(ocr.manufacturingDate, '15 Oct 2023');

      // 5. Expiry Date (must NOT confuse with Mfg Date)
      expect(ocr.expiryDate, '14 Oct 2025');

      // 6. Batch Number (must NOT be "Number" or "No")
      expect(ocr.batchNumber, 'AH231015B');
      expect(ocr.batchNumber, isNot(equals('Number')));

      // 7. FSSAI Number
      expect(ocr.fssaiNumber, '11518018000123');

      // 8. Manufacturer Details (must NOT be "MANUFACTURER DETAILS")
      expect(ocr.manufacturerDetails, contains('ARTISAN FOODS PVT. LTD.'));
      expect(ocr.manufacturerDetails, contains('Survey No. 45/2'));
      expect(ocr.manufacturerDetails, isNot(equals('MANUFACTURER DETAILS')));

      // 9. Consumer Care
      expect(ocr.consumerCare, contains('care@artisanharvest.com'));

      // 10. Country of Origin
      expect(ocr.getFieldValue(OcrFieldKeys.countryOfOrigin), 'India');
    });

    test('accurately extracts declarations from Pickle package', () {
      const pickleText = '''
Maharashtrian Pickles & Spices SHG
Mango Pickle (Special Recipe)
Net Quantity: 500g
Max Retail Price: Rs. 150.00 (inclusive of all taxes)
Date of Mfg: 08/2026
Best Before: 12 months from manufacture
Country of Origin: India
Batch No: B-2026/08
FSSAI Lic No: 11521034000123
Unit Sale Price: Rs 0.30 / g
Customer Care: 1800-222-333, info@spices.org
Plot 42, MIDC Industrial Area, Pune 411026
''';

      final fields = OcrService.parsePackagingDeclarations(pickleText);
      final ocr = OcrResult(
        jobId: 'test-pickle',
        status: OcrStatus.completed,
        analyzedAt: DateTime.now(),
        fields: fields,
      );

      expect(ocr.productName, contains('Pickle'));
      expect(ocr.mrp, contains('150.00'));
      expect(ocr.mrp, anyOf(contains('inclusive of all taxes'), contains('incl. of all taxes')));
      expect(ocr.netQuantity, contains('500'));
      expect(ocr.manufacturingDate, '08/2026');
      expect(ocr.expiryDate, contains('12 months'));
      expect(ocr.batchNumber, 'B-2026/08');
      expect(ocr.fssaiNumber, '11521034000123');
      expect(ocr.unitSalePrice, contains('0.30'));
      expect(ocr.consumerCare, contains('1800-222-333'));
      expect(ocr.consumerCare, contains('info@spices.org'));
      expect(ocr.getFieldValue(OcrFieldKeys.countryOfOrigin), 'India');
    });

    test('accurately extracts declarations from Detergent Powder (FMCG non-food)', () {
      const detergentText = '''
Surf Excel Easy Wash Detergent Powder
Manufactured by: Hindustan Unilever Limited
Unilever House, B. D. Sawant Marg, Chakala, Andheri (E), Mumbai - 400099, Maharashtra
Net Wt: 1 kg
MRP: ₹ 115.00 (incl. of all taxes)
Pkd Date: 06/2026
Use By: 24 months from pkd
Batch: SE-9941A
Consumer Care: 1800-10-22-222, lever.care@unilever.com
Country of Origin: India
''';

      final fields = OcrService.parsePackagingDeclarations(detergentText);
      final ocr = OcrResult(
        jobId: 'test-surf',
        status: OcrStatus.completed,
        analyzedAt: DateTime.now(),
        fields: fields,
      );

      expect(ocr.productName, 'Surf Excel Easy Wash Detergent Powder');
      expect(ocr.genericName, 'Detergent Powder');
      expect(ocr.mrp, contains('115.00'));
      expect(ocr.netQuantity, contains('1 kg'));
      expect(ocr.manufacturingDate, '06/2026');
      expect(ocr.expiryDate, contains('24 months'));
      expect(ocr.batchNumber, 'SE-9941A');
      expect(ocr.manufacturerDetails, contains('Hindustan Unilever Limited'));
      expect(ocr.consumerCare, contains('1800-10-22-222'));
      expect(ocr.consumerCare, contains('lever.care@unilever.com'));
      expect(ocr.getFieldValue(OcrFieldKeys.countryOfOrigin), 'India');
      expect(ocr.fssaiNumber, isNull);
    });

    test('accurately extracts declarations from Edible Oil package', () {
      const oilText = '''
Fortune Sunlite Refined Sunflower Oil
Net Volume: 1 Litre
MRP Rs. 165.00 (incl. of all taxes)
Packed on: 10/05/2026
Best Before: 9 months from packing
Packed by: Adani Wilmar Limited
Post Box No. 2, Mithakhali, Ahmedabad 380006, Gujarat
Batch No: AWL-SF-4402
Customer Care: 1800-233-9999, care@adaniwilmar.in
Made in India
FSSAI No: 10013021000853
''';

      final fields = OcrService.parsePackagingDeclarations(oilText);
      final ocr = OcrResult(
        jobId: 'test-oil',
        status: OcrStatus.completed,
        analyzedAt: DateTime.now(),
        fields: fields,
      );

      expect(ocr.productName, 'Fortune Sunlite Refined Sunflower Oil');
      expect(ocr.genericName, contains('Sunflower Oil'));
      expect(ocr.mrp, contains('165.00'));
      expect(ocr.netQuantity, '1 Litre');
      expect(ocr.manufacturingDate, '10/05/2026');
      expect(ocr.expiryDate, contains('9 months'));
      expect(ocr.batchNumber, 'AWL-SF-4402');
      expect(ocr.manufacturerDetails, contains('Adani Wilmar Limited'));
      expect(ocr.consumerCare, contains('1800-233-9999'));
      expect(ocr.fssaiNumber, '10013021000853');
      expect(ocr.getFieldValue(OcrFieldKeys.countryOfOrigin), 'India');
    });

    test('accurately extracts declarations from Biscuit package', () {
      const biscuitText = '''
Britannia Marie Gold Biscuits
Net Weight: 250 g
MRP: Rs 40.00
Date of Manufacture: 12/04/2026
Expiry Date: 12/10/2026
Manufactured by: Britannia Industries Ltd.
5/1A Hungerford Street, Kolkata - 700017
Batch: BM-202604
Customer Complaints: 1800-4254449, feedback@britindia.com
FSSAI Lic No: 10015043001129
Country of Origin: India
''';

      final fields = OcrService.parsePackagingDeclarations(biscuitText);
      final ocr = OcrResult(
        jobId: 'test-biscuit',
        status: OcrStatus.completed,
        analyzedAt: DateTime.now(),
        fields: fields,
      );

      expect(ocr.productName, 'Britannia Marie Gold Biscuits');
      expect(ocr.genericName, 'Biscuits');
      expect(ocr.mrp, contains('40.00'));
      expect(ocr.netQuantity, '250 g');
      expect(ocr.manufacturingDate, '12/04/2026');
      expect(ocr.expiryDate, '12/10/2026');
      expect(ocr.batchNumber, 'BM-202604');
      expect(ocr.manufacturerDetails, contains('Britannia Industries Ltd.'));
      expect(ocr.consumerCare, contains('1800-4254449'));
      expect(ocr.consumerCare, contains('feedback@britindia.com'));
      expect(ocr.fssaiNumber, '10015043001129');
      expect(ocr.getFieldValue(OcrFieldKeys.countryOfOrigin), 'India');
    });

    test('accurately extracts declarations from Spices package', () {
      const spiceText = '''
Everest Garam Masala
Net Qty: 100g
MRP: Rs. 85.00 (inclusive of all taxes)
Date of Pkd: 01/2026
Best Before: 12 months from pkd
Mfd by: S.Everest Food Products Pvt. Ltd.
D-221, TTC Industrial Area, MIDC, Shirvane, Navi Mumbai 400706
Lot No: EV-GM-109
Consumer Care: 022-27780000, customercare@everestspices.com
FSSAI No: 11516017000215
Country of Origin: India
''';

      final fields = OcrService.parsePackagingDeclarations(spiceText);
      final ocr = OcrResult(
        jobId: 'test-spice',
        status: OcrStatus.completed,
        analyzedAt: DateTime.now(),
        fields: fields,
      );

      expect(ocr.productName, 'Everest Garam Masala');
      expect(ocr.genericName, contains('Garam Masala'));
      expect(ocr.mrp, contains('85.00'));
      expect(ocr.netQuantity, contains('100'));
      expect(ocr.manufacturingDate, '01/2026');
      expect(ocr.expiryDate, contains('12 months'));
      expect(ocr.batchNumber, 'EV-GM-109');
      expect(ocr.manufacturerDetails, contains('S.Everest Food Products Pvt. Ltd.'));
      expect(ocr.fssaiNumber, '11516017000215');
      expect(ocr.consumerCare, contains('022-27780000'));
      expect(ocr.getFieldValue(OcrFieldKeys.countryOfOrigin), 'India');
    });

    test('handles empty or missing input cleanly without hardcoding to pasta or pickle', () {
      const blankText = '';
      final fields = OcrService.parsePackagingDeclarations(blankText);

      final ocr = OcrResult(
        jobId: 'test-blank',
        status: OcrStatus.completed,
        analyzedAt: DateTime.now(),
        fields: fields,
      );

      expect(ocr.productName, isNull);
      expect(ocr.mrp, isNull);
      expect(ocr.netQuantity, isNull);
      expect(ocr.manufacturingDate, isNull);
      expect(ocr.expiryDate, isNull);
      expect(ocr.batchNumber, isNull);
      expect(ocr.fssaiNumber, isNull);

      for (final f in fields) {
        expect(f.isMissing, isTrue);
        expect(f.value, isEmpty);
      }
    });
  });
}
