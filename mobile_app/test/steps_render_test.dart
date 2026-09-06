import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:legal_metrology/core/theme/app_theme.dart';
import 'package:legal_metrology/core/widgets/common_widgets.dart';
import 'package:legal_metrology/features/inspector/inspection/flow_complete_screen.dart';
import 'package:legal_metrology/features/inspector/inspection/notice_step.dart';
import 'package:legal_metrology/features/inspector/inspection/signature_step.dart';
import 'package:legal_metrology/models/inspection.dart';
import 'package:legal_metrology/models/notice.dart';
import 'package:legal_metrology/models/signature.dart';
import 'package:legal_metrology/models/violation.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('StepIndicator renders without overflow on narrow screen', (tester) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);

    const steps = [
      'Evidence', 'OCR', 'Fields', 'Violations', 'Offence',
      'Observations', 'Notice', 'Sign', 'Done'
    ];

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: StepIndicator(steps: steps, currentStep: 6),
        ),
      ),
    );

    expect(tester.takeException(), isNull);
  });

  testWidgets('SignatureStep renders without overflow on narrow screen with null draftNotice', (tester) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);

    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: Scaffold(
            body: SignatureStep(
              inspection: null,
              draftNotice: null,
              onSigned: (_, __) {},
              onBack: () {},
            ),
          ),
        ),
      ),
    );
  });

  testWidgets('NoticeStep renders selection view and draft review without throwing', (tester) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);

    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: Scaffold(
            body: NoticeStep(
              inspectionId: 'insp-001',
              inspection: null,
              violations: const [],
              onNoticeIssued: (_) {},
              onBack: () {},
            ),
          ),
        ),
      ),
    );
    await tester.pump(const Duration(seconds: 1));

    expect(tester.takeException(), isNull);
  });

  testWidgets('FlowCompleteScreen renders without errors with null and non-null notice', (tester) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);

    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: Scaffold(
            body: FlowCompleteScreen(
              notice: null,
              signature: null,
            ),
          ),
        ),
      ),
    );

    expect(tester.takeException(), isNull);
  });
}
