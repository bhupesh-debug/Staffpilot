# StaffPilot — Business Overview (Phase 1)

**Status:** Phase 1 strategy — internal working document, not a public claim.
**Date:** November 22, 2026
**Geography:** United States; New York first.
**Budget envelope:** $0–$100 for Phase 1 validation work.

## 1. What StaffPilot is

StaffPilot is a B2B software-as-a-service (SaaS) platform for staffing companies, consulting firms, and small employers that manage **20–100 workers**. It brings together the four workflows those firms currently run in disconnected spreadsheets, email, and generic tools:

- **Workforces** — worker and consultant records, assignments, and documents.
- **Projects** — client engagements, bill rates, pay rates, and margins.
- **Payroll (preparation only)** — timesheets, approvals, billing, and payroll *estimates*.
- **One platform** — a single tenant-isolated workspace per firm, with role-based access.

Tagline: **"Workforces. Projects. Payroll. One Platform."**

## 2. The problem

Small staffing and consulting firms (20–100 workers) sit in a gap in the market [UNVERIFIED — to confirm in discovery]:

1. **Spreadsheet operations.** Assignments, bill/pay rates, and margins live in spreadsheets that go stale, have no audit trail, and break when more than one person edits them.
2. **Timesheet chaos.** Consultants submit hours by email or chat; client approval is a reply-all thread; disputes surface at invoice time.
3. **Billing and payroll don't connect.** Invoicing is built from one source, payroll preparation from another, and the margin between them is only reconciled at month-end — if at all.
4. **Generic tools don't fit.** General-purpose HR/payroll tools are built for direct employers, not for firms that place workers at clients, track bill vs. pay rates, and manage C2C (corp-to-corp) vendor relationships.
5. **Enterprise staffing systems are out of reach.** Full vendor-management / staffing suites are priced and implemented for firms far larger than 20–100 workers [UNVERIFIED — to confirm in discovery].

The cost of the gap is concrete: billing errors, late invoices, payroll-preparation rework, lost margin visibility, and audit exposure when records are scattered.

## 3. The product (Phase 1 scope)

StaffPilot's Phase 1 product is a **workflow and preparation platform**, not a money-movement or tax platform. Core capabilities:

| Area | What it does |
|---|---|
| Worker records | Consultant/employee profiles, assignments, rates, documents, status |
| Assignments | Worker ↔ client ↔ project linkage, bill rate, pay rate, margin |
| Timesheets | Weekly entry, submit → manager approve → client approve, locked after approval |
| Client approvals | Client-side review and approval of submitted hours |
| Billing | Invoices generated from approved timesheets and rates |
| Payroll preparation | Payroll *estimates* from approved hours and pay rates — figures for review, not payments |
| Reporting | Margin, utilization, billing vs. payroll-prep, aging |

Out of scope for Phase 1 (and for the product until a later, separately validated phase): moving payroll funds, direct deposits, tax filing, tax deposits, and any claimed tax or compliance certification.

## 4. Business model

- **Model:** Subscription SaaS — a monthly fee per customer, composed of a base platform fee plus a per-worker-per-month charge. See `05-pricing-model.md` for the proposed tiers.
- **Customers:** Staffing companies, consulting firms, and small employers managing 20–100 workers. Initial focus: New York.
- **Revenue:** Subscription fees only in Phase 1. No per-transaction payroll fees, no placement fees, no revenue share on client billings.
- **Cost structure (Phase 1):** Near-zero cash cost by design — founder-built product, $0–$100 validation budget, free-tier hosting where available. The real cost is founder time.
- **Growth path:** Land small firms (20–50 workers), prove the timesheet → approval → billing → payroll-prep loop, then expand within the account as headcount grows.

## 5. The three-way separation (non-negotiable)

StaffPilot must keep three things clearly, visibly separated — in the product, in marketing copy, and in contracts/terms:

### A. Subscription software
StaffPilot sells **software access**. The customer pays a subscription to use the platform. StaffPilot is not the customer's employer, not their staffing agency, and not their payroll provider.

### B. Staffing operations
The **customer** runs their staffing business: hiring, placing, managing, and supervising their workers and consultants. StaffPilot provides the workflow tools; it does not recruit, place, employ, or supervise anyone's workers.

### C. Payroll processing
StaffPilot does **payroll preparation only — estimates**. It computes what payroll *would* look like from approved hours and pay rates so the customer can review it and hand it to their actual payroll processor. StaffPilot does NOT:
- move payroll funds or make direct deposits;
- file taxes or make tax deposits;
- calculate or guarantee tax withholdings;
- store real Social Security numbers or bank account details for payroll purposes;
- claim any payroll, tax, or compliance certification.

**Why this matters:** blurring these three lines is the single biggest legal and trust risk for the product. Every screen, email, and sales conversation must keep them distinct. The payroll-preparation screens must label figures as estimates.

## 6. Boundaries and rules

1. **Estimates only.** Every payroll figure in the product is labeled an estimate. No "net pay" presented as final.
2. **No real sensitive payroll data.** No real SSNs, no bank routing/account numbers. The product must not ask for them.
3. **No claimed certifications.** StaffPilot claims no SOC 2, ISO, tax, or payroll certification unless and until one is actually obtained [UNVERIFIED — none held as of Nov 22, 2026].
4. **No auto-classification.** StaffPilot never auto-classifies a C2C consultant as an independent contractor. Classification is the customer's legal determination, made with their own counsel; the product records what the customer enters.
5. **No fabricated proof.** No fake customer logos, testimonials, case studies, or market statistics in any material. Every unverified claim is marked [UNVERIFIED]; every competitor price is marked [VERIFY LIVE].
6. **Tenant isolation.** Each customer's data is isolated; no cross-tenant visibility, ever.
7. **Audit trail.** Timesheet approvals, rate changes, and payroll-preparation runs are logged with who/when.

## 7. What success looks like (Phase 1)

- 10 paying customers in the 20–100-worker segment within 90 days of launch (see `08-90-day-launch-strategy.md`).
- The core loop (timesheet → approval → billing → payroll-prep estimate) demonstrably working for at least one real customer.
- Discovery interviews completed and pricing validated or revised (see `09-discovery-questions.md` and `05-pricing-model.md`).
- Zero boundary violations: no real payroll funds moved, no SSNs collected, no certification claimed.

## 8. Open questions for discovery

- Is the 20–100-worker segment's biggest pain timesheets, billing, or payroll preparation?
- Do target firms already have a payroll processor they are happy with (making "preparation" the right wedge) or are they looking to replace one?
- How do C2C vendor managers currently track vendor consultants, and what breaks first?
- What does a firm currently pay (in software + staff time) for this workflow? [UNVERIFIED — to learn in discovery, not assumed.]

## 9. Sources and consistency

- Competitor/open-source baseline: `~/workspace/staffpilot/research/payroll-systems-shortlist.md` (verified Nov 22, 2026). StaffPilot borrows architecture patterns from that shortlist (regulation-as-config, payroll lifecycle state machine, RLS tenant isolation, decimal-safe money math) — never code, and never GPL/AGPL or no-license code.
- Pricing, personas, and positioning in the sibling Phase 1 documents must stay consistent with this overview. If a later document contradicts it, this overview governs until the team explicitly revises it.
