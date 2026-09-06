import { PrismaClient, Role, NoticeType, NoticeStatus, CaseStatus } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('[Seeder] Seeding database records into PostgreSQL...');

  // 1. Seed Demo Inspector User
  const inspectorUser = await prisma.user.upsert({
    where: { email: 'officer@legalmetrology.maharashtra.gov.in' },
    update: {},
    create: {
      id: 'usr_inspector_001',
      name: 'Legal Metrology Officer S. K. Shinde',
      email: 'officer@legalmetrology.maharashtra.gov.in',
      phone: '+91-9876543210',
      role: Role.INSPECTOR,
    },
  });

  // 2. Seed Demo Business User
  const businessUser = await prisma.user.upsert({
    where: { email: 'owner@spices.com' },
    update: {},
    create: {
      id: 'usr_business_001',
      name: 'Maharashtrian Pickles & Spices Owner',
      email: 'owner@spices.com',
      phone: '+91-9123456789',
      role: Role.BUSINESS,
    },
  });

  // 3. Seed Demo Citizen User
  const citizenUser = await prisma.user.upsert({
    where: { email: 'citizen.rahul@gmail.com' },
    update: {},
    create: {
      id: 'usr_citizen_001',
      name: 'Rahul Sharma',
      email: 'citizen.rahul@gmail.com',
      phone: '+91-9988776655',
      role: Role.CITIZEN,
    },
  });

  // 4. Seed Demo Business Entity
  const business = await prisma.business.upsert({
    where: { gstin: '27AABCU9603R1ZN' },
    update: {},
    create: {
      id: 'biz_001',
      ownerUserId: businessUser.id,
      name: 'Maharashtrian Pickles & Spices SHG',
      address: 'Plot 45, MIDC Industrial Area, Chakan, Pune, Maharashtra - 410501',
      geoLat: 18.7604,
      geoLng: 73.8636,
      gstin: '27AABCU9603R1ZN',
      turnoverBand: '10L-50L',
    },
  });

  // 5. Seed Demo Citizen Complaint
  const complaint = await prisma.complaint.upsert({
    where: { id: 'cmp_001' },
    update: {},
    create: {
      id: 'cmp_001',
      citizenId: citizenUser.id,
      businessId: business.id,
      retailerNameText: 'Maharashtrian Pickles & Spices SHG',
      retailerAddressText: 'Plot 45, MIDC Industrial Area, Chakan, Pune',
      category: 'Label Declaration Deficiency',
      description: 'Missing Consumer Care Helpline details on Mango Pickle 500g packaging label.',
      photoUrls: ['https://storage.legalmetrology.gov.in/evidence/mango_pickle_label.jpg'],
      status: CaseStatus.INSPECTED,
    },
  });

  // 6. Seed Demo Inspection
  const inspection = await prisma.inspection.upsert({
    where: { id: 'insp_001' },
    update: {},
    create: {
      id: 'insp_001',
      inspectorId: inspectorUser.id,
      businessId: business.id,
      complaintId: complaint.id,
      status: CaseStatus.NOTICE_ISSUED,
    },
  });

  // 7. Seed Demo Notice
  await prisma.notice.upsert({
    where: { id: 'not_001' },
    update: {},
    create: {
      id: 'not_001',
      caseId: 'CASE-MH-2026-0891',
      inspectionId: inspection.id,
      businessId: business.id,
      type: NoticeType.IMPROVEMENT,
      contentText: 'Improvement Notice issued under Section 36(1) of Legal Metrology Act 2009 for non-declaration of Customer Care details under PCR Rule 6(1)(g).',
      sectionRefs: ['Section 36(1)', 'PCR Rule 6(1)(g)'],
      status: NoticeStatus.ISSUED,
      issuedDate: new Date(),
      deadlineDate: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000),
      pdfUrl: 'https://storage.legalmetrology.gov.in/notices/MH-2026-0891.pdf',
    },
  });

  console.log('[Seeder] Database successfully seeded with 7 core entities.');
}

main()
  .catch((e) => {
    console.error('[Seeder] Error seeding database:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
