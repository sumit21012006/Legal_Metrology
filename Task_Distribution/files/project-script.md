# Automated Legal Metrology Compliance & Enforcement System
### SIH Problem Statement 34 — Project Script

---

## 1. The Problem

The Legal Metrology Act, 2011 protects consumers by making sure every packaged product declares things like MRP, net quantity, manufacturing/expiry date, and manufacturer details correctly. But in practice:

- Businesses rarely learn what's wrong with their packaging until an inspector catches them — by then, they've already broken the law and often didn't even know the rule existed.
- Getting proper guidance costs ₹20,000–₹30,000 in consultancy fees, which is completely out of reach for a small home-based business (like a Self-Help Group selling pickles or papad).
- Consumers, especially online shoppers, have no easy way to report packaging violations they notice.
- Offence records are scattered — the same brand can be caught for the same violation in two different cities and get treated as a "first offence" both times, since there's no shared record.
- This lack of transparency also creates room for corruption in how offences and penalties are recorded.

## 2. Our Solution, in One Line

A single digital platform connecting **Citizens**, **Businesses**, **Inspectors**, and the **Controller (government)** — using OCR-based packaging scans and automated, rule-based notice generation to make compliance preventive, consistent, and transparent instead of punitive and inconsistent.

## 3. Who Uses It, and How

### A. Citizen (Consumer) — Web Dashboard
- Signs up with mobile OTP verification (keeps out fake/spam accounts).
- Files a complaint against a product or retailer: selects a clear violation category (Wrong MRP, Missing Net Quantity, No Manufacturing Date, etc.), uploads photos of the packaging and the invoice/bill, and enters the retailer's name and address.
- Can track their complaint step-by-step: **Received → Assigned → Inspected → Notice Issued → Resolved.**
- Receives an incentive only once the case is compounded or the business corrects the issue — this rewards genuine reporting and discourages false complaints.
- Over time, this also builds public awareness of the Act and gives the department a citizen-powered way to discover violators.

### B. Business / Retailer — Mobile App
*(Importers, exporters, home-based businesses, SHGs, small and large companies)*

- Registers their business on the app.
- Can scan their own product packaging (2–3 angles, camera-based, just like the inspector's process) and get an instant self-compliance check — missing fields, wrong formats, anything that violates the Act, along with a suggested fix.
- **This self-check is completely private.** It's never visible to inspectors or the government — the whole point is to give a business a safe space to learn and fix issues on their own, without a consultant, before anyone ever inspects them.
- If a notice is issued against them, they can view it, submit supporting evidence, raise a dispute if they disagree, submit consent where required, re-upload corrected packaging photos to clear an Improvement Notice, and pay any penalty — all inside the same app.
- This is especially built for small businesses who've never had affordable access to this kind of legal guidance before.

### C. Inspector — Mobile App (works offline)
- Selects the registered business being inspected and scans the product packaging from multiple angles.
- The system automatically extracts all required label information (MRP, net quantity, dates, manufacturer details, etc.) using OCR.
- **The inspector reviews and corrects the extracted data before anything is finalized** — this keeps every legal document built on accurate information, not just whatever the OCR happened to read.
- The system checks its database to see if this exact product or manufacturer has already been caught for a violation anywhere else in the country, and automatically applies First Offence or Second Offence rules.
- Notices are auto-drafted using NLP, pulling exact rule references from the legal knowledge base — the inspector reviews and signs digitally before issuing.

**The Notice Ladder:**
1. **Improvement Notice** — first flag; gives the business a chance to correct the issue.
2. **Seizure Notice** — issued whenever evidence or product samples need to be seized (can happen at any stage).
3. **Panchanama** — formal record of the violation with two independent witnesses, the applicable Act section, and the penalty amount.
4. **Compounded Order** — final penalty order, sent to the Controller for approval before the business pays.

- The system tracks how many days are left before a case must escalate to the next stage, so nothing gets missed.
- If a retailer names their supplier during an inspection, the system automatically opens a linked case against that supplier and routes it to the Controller to assign to the right jurisdiction's inspector — gradually building a supply-chain map of violations.

### D. Controller (Government Officer) — Web Dashboard
- Sees the complete statewide picture: total complaints, first vs. second offence counts, region-wise case load, and compounded cases.
- Reviews every Compounded Order — can **approve** it or **reject it with a comment**, sending it back to the inspector for revision.
- Can mark a serious or repeat case for **prosecution instead of compounding**, when the Act doesn't allow compounding.
- Assigns supply-chain-linked inspection cases to the correct inspector.

## 4. The Legal Knowledge Base — What Makes All of This Possible

Underneath all four dashboards sits one critical piece: a structured digital version of the **Legal Metrology Act, 2011** and the **Legal Metrology (Packaged Commodities) Rules, 2011**. Every mandatory label field, the exact Act/Rule section it comes from, and the penalty for violating it is stored here in a queryable format. This is what the OCR engine checks packaging against, what the NLP engine pulls from to write legally accurate notices, and what powers the whole first-offence/second-offence system. Without this, the OCR scan is just a text reader — this is what makes it a compliance engine.

## 5. Why This Reduces Corruption

Every action in the system — every notice issued, every offence recorded, every approval or rejection — is logged and visible to the Controller. Because offence history is centralized and automatic, an inspector can no longer quietly under-record a second offence as a first offence. At the same time, a genuine small business has a full digital record protecting it from being wrongly harassed.

## 6. Business Model

- **Subscription for businesses**, tiered by turnover — gives access to unlimited self-checks, digital record-keeping, and online case management.
- **1–2% commission from the government** on the total penalty amount collected through the platform.

## 7. Technology Snapshot

| Layer | Technology |
|---|---|
| Mobile Apps (Inspector, Business) | Flutter |
| Web Apps (Citizen, Controller) | Next.js |
| API Gateway & Core Backend | NestJS |
| Authentication | Keycloak (role-based access) |
| AI / OCR / NLP Engine | Python + FastAPI |
| Core Database | PostgreSQL + PostGIS (geo/jurisdiction data) |
| Supply Chain Mapping | Neo4j (graph database) |
| Search | Elasticsearch |
| File Storage (evidence, images, PDFs) | S3 / MinIO |
| Async Job Queue (OCR processing) | RabbitMQ |
| Digital Signatures | eMudhra |
| Payments | Razorpay |
| Notifications | WhatsApp + Email |

---

*This document reflects the current, prototype-scoped version of the project — every feature described above is meant to be demonstrable, not aspirational.*
