import axios from 'axios';

const BASE_URL = 'http://localhost:3000/api/v1';

async function testEndpoint(name: string, method: 'GET' | 'POST' | 'PATCH', urlPath: string, payload?: any, headers?: any) {
  try {
    const fullUrl = `${BASE_URL}${urlPath}`;
    const start = Date.now();
    let res: any;
    if (method === 'GET') {
      res = await axios.get(fullUrl, { headers });
    } else if (method === 'POST') {
      res = await axios.post(fullUrl, payload || {}, { headers });
    } else if (method === 'PATCH') {
      res = await axios.patch(fullUrl, payload || {}, { headers });
    }
    const elapsed = Date.now() - start;
    console.log(`✅ [${res.status} OK] ${method.padEnd(5)} ${urlPath.padEnd(45)} (${elapsed}ms) - ${name}`);
    return { success: true, status: res.status, data: res.data };
  } catch (err: any) {
    const status = err.response ? err.response.status : 'NETWORK_ERR';
    console.error(`❌ [${status}] ${method.padEnd(5)} ${urlPath.padEnd(45)} - ${name}:`, err.message);
    return { success: false, status, error: err.message };
  }
}

async function runFullSystemAudit() {
  console.log('================================================================================');
  console.log('🚀 STARTING FULL END-TO-END ENDPOINT AUDIT (35 API GATEWAY ROUTES)');
  console.log('================================================================================\n');

  let passed = 0;
  let failed = 0;

  const endpoints = [
    // 1. Health & System Check
    { name: 'System Architecture Health Check', method: 'GET', path: '/health/system-check' },

    // 2. Authentication & Profile
    { name: 'Login Inspector Account', method: 'POST', path: '/auth/login', payload: { username: 'inspector_rajesh' } },
    { name: 'Login Business Account', method: 'POST', path: '/auth/login', payload: { username: 'spices_owner', role: 'BUSINESS' } },
    { name: 'Register Business Account', method: 'POST', path: '/auth/register/business', payload: { email: 'test@biz.com', fullName: 'Test Business' } },
    { name: 'Register Citizen Account', method: 'POST', path: '/auth/register', payload: { email: 'citizen@test.com', name: 'Test Citizen' } },
    { name: 'Refresh Auth Token', method: 'POST', path: '/auth/refresh', payload: { refreshToken: 'mock_token' } },
    { name: 'Get Authenticated User Profile (Inspector)', method: 'GET', path: '/auth/me', headers: { Authorization: 'Bearer mock_inspector_token' } },
    { name: 'Get Authenticated User Profile (Business)', method: 'GET', path: '/auth/me', headers: { Authorization: 'Bearer mock_business_token' } },
    { name: 'User Logout', method: 'POST', path: '/auth/logout' },

    // 3. Knowledge Base & Rules Engine
    { name: 'Get Full Legal Rulebook', method: 'GET', path: '/knowledge-base/rulebook' },
    { name: 'Get Penalty Matrix', method: 'GET', path: '/knowledge-base/penalties' },
    { name: 'Get Penalty by Section', method: 'GET', path: '/knowledge-base/penalties/Section 36(1)' },
    { name: 'Get Compounding Matrix', method: 'GET', path: '/knowledge-base/compounding' },
    { name: 'Get Statutory Exemptions', method: 'GET', path: '/knowledge-base/exemptions' },
    { name: 'Sub-millisecond Search Rules (Elasticsearch)', method: 'POST', path: '/knowledge-base/search', payload: { query: 'Consumer Care' } },

    // 4. Businesses Module
    { name: 'Get All Businesses / Search', method: 'GET', path: '/businesses' },
    { name: 'Get Business Details by ID', method: 'GET', path: '/businesses/biz_001' },
    { name: 'Register New Business Entity', method: 'POST', path: '/businesses', payload: { name: 'New Spice Trader', gstin: '27XYZ1234F1Z5', address: 'Pune MIDC' } },
    { name: 'Get Business Inspections', method: 'GET', path: '/businesses/biz_001/inspections' },

    // 5. Inspections & AI OCR Scan
    { name: 'List All Inspections', method: 'GET', path: '/inspections' },
    { name: 'Get Inspection Details by ID', method: 'GET', path: '/inspections/insp_001' },
    { name: 'Create Inspection Request', method: 'POST', path: '/inspections', payload: { businessId: 'biz_001', inspectorId: 'usr_inspector_001' } },
    { name: 'Process Label OCR Photo Scan', method: 'POST', path: '/ocr/analyze', payload: { imageBase64: 'mock_base64_data' } },
    { name: 'Confirm Violation Record', method: 'POST', path: '/violations/v_001/confirm', payload: { inspectorId: 'usr_inspector_001' } },

    // 6. Notices & Legal Orders
    { name: 'List All Legal Notices', method: 'GET', path: '/notices' },
    { name: 'Get Notice Details by ID', method: 'GET', path: '/notices/NOT-1001' },
    { name: 'Issue & Render Bilingual Notice', method: 'POST', path: '/notices', payload: { type: 'improvement', lang: 'en', businessId: 'biz_001', observedViolation: 'Missing helpline phone number' } },
    { name: 'Confirm Notice Draft', method: 'POST', path: '/notices/NOT-1001/confirm', payload: { remark: 'Confirmed by Officer' } },
    { name: 'Sign & Issue Notice', method: 'POST', path: '/notices/NOT-1001/issue', payload: { signerName: 'Inspector S. K. Shinde' } },

    // 7. Complaints & Cases Module
    { name: 'List All Complaints', method: 'GET', path: '/complaints' },
    { name: 'Create Citizen Complaint', method: 'POST', path: '/complaints', payload: { retailerNameText: 'Supermarket', category: 'Dual MRP', description: 'Overpriced item' } },
    { name: 'List Compliance Cases', method: 'GET', path: '/cases' },

    // 8. Controller HQ & Graph Tracing
    { name: 'Get Controller Statewide Dashboard Stats', method: 'GET', path: '/controller/dashboard/stats' },
    { name: 'Create Multi-Tier Neo4j Graph Trace', method: 'POST', path: '/controller/supply-chain/multi-tier', payload: { retailerGstin: '27RET1', retailerName: 'Retailer A', distributorGstin: '27DIS1', distributorName: 'Dist B', manufacturerGstin: '27MFG1', manufacturerName: 'Mfg C', productName: 'Pickle', inspectionId: 'insp_001', violationCategory: 'Label' } },
    { name: 'Trace Upstream Supply Chain (Neo4j Cypher)', method: 'GET', path: '/controller/supply-chain/trace/27AABCU9603R1ZN' },

    // 9. Payments & Self Checks
    { name: 'Create Razorpay Fine Payment Order', method: 'POST', path: '/payments/initiate', payload: { noticeId: 'NOT-1001', amount: 25000 } },
    { name: 'Submit Self-Check Compliance Audit', method: 'POST', path: '/self-check/analyze', payload: { businessId: 'biz_001', imageBase64: 'mock' } },
  ];

  for (const ep of endpoints) {
    const res = await testEndpoint(ep.name, ep.method as any, ep.path, (ep as any).payload, (ep as any).headers);
    if (res.success) {
      passed++;
    } else {
      failed++;
    }
  }

  console.log('\n================================================================================');
  console.log(`📊 AUDIT SUMMARY RESULTS: ${passed} PASSED | ${failed} FAILED | TOTAL: ${endpoints.length}`);
  console.log('================================================================================');
}

runFullSystemAudit();
