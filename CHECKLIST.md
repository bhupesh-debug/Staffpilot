# StaffPilot — Development Checklist

Updated after each milestone. Status: Phase 1–3 complete (Nov 22, 2026).
Phases 4–15 are scoped in the spec and not yet built.

## Milestone record

### Step 1 — Research (DONE, Nov 22, 2026)
- **Built:** Ranked shortlist of open-source payroll systems from
  https://github.com/topics/payroll-management-system (181 repos) plus adjacent
  searches. File: `research/payroll-systems-shortlist.md`.
- **What works:** Every repo verified live via the GitHub connector on the
  research date (stars, language, license from LICENSE file, last-updated date).
- **Key findings:** The topic itself is thin (top repos ~140 stars, mostly small
  or school projects). Top picks: PayrollEngine (141★, MIT — regulation-as-config,
  API-first), frappe/hrms (9,090★, GPL-3.0 — data-model ideas only), NomiFlow
  (no license — closest functional twin, study-only), euron-open-hrms (18★, MIT,
  TypeScript multi-tenant), Hafta (147★, MIT), OrangeHRM (1,161★, GPL), IceHrm
  (741★, GPL), supabasePayroll (8★, MIT), payrun (MIT, Postgres RLS),
  sheet-happens (AGPL, timesheet approvals).
- **What remains:** Re-check star counts before citing externally; no US tax
  logic exists in any surveyed repo (payroll stays estimates-only by design).
- **How to run:** N/A (research document).

### Phase 1 — Business + product strategy (DONE, Nov 22, 2026)
- **Built:** 11 documents, 13,285 words, under `docs/phase-1/`.
- **What works:** Pricing (Starter $49/mo + $4/worker, Growth $99/mo + $6,
  Scale $199/mo + $8; at 45 workers $229/$369/$559), 5 personas, positioning,
  competitor research plan, revenue assumptions (all labeled ASSUMPTION),
  90-day launch strategy (Prove → Convert → Repeat, 10 paying customers),
  discovery questions, outreach templates, onboarding workflow.
- **What was tested:** Consistency check against the research shortlist;
  every unverified claim marked [UNVERIFIED]; no invented statistics,
  testimonials, or revenue guarantees.
- **What remains:** Validate pricing/personas in discovery interviews
  (Phase 1 doc 09 is the interview script); competitor prices marked
  [VERIFY LIVE].
- **How to run:** Read the Markdown files in `docs/phase-1/`.

### Phase 2 — Public website (DONE, Nov 22, 2026)
- **Built:** Static site, 16 pages + CSS + JS + generator (`website/build.py`),
  under `website/`. No build step, no CDN, renders offline.
- **What works:** All 16 pages real (Home, Features, Staffing firms, C2C
  consulting, Workforce management, Payroll preparation, Pricing, About,
  Contact, Request a demo, Blog, FAQ, Login, Privacy, Terms, Security).
  Pricing calculator, demo/contact forms (client-side validation, local-storage
  only, honestly labeled), dashboard preview with synthetic data labeled as such.
- **What was tested:** 0 dead internal links; all 16 pages + CSS/JS served
  HTTP 200 locally; WCAG contrast ratios all ≥ 6.3:1; zero external URLs.
  No fake testimonials, logos, statistics, or guarantees (verified by scan).
- **What remains:** Fold into the Next.js app as marketing routes (later step);
  demo/contact forms need the Phase 15 API; Login page needs the hosted app
  sign-in URL once published.
- **How to run:** `cd website && python3 -m http.server 8137` → http://localhost:8137/

### Phase 3 — Application architecture (DONE, Nov 22, 2026)
- **Built:** Next.js 14 + TypeScript + Tailwind scaffold under `app/` (36 files):
  home page, `/api/health`, login page (Supabase-aware placeholder),
  `src/lib/` (money with decimal.js, permissions for 7 roles → 19 granular
  permissions, timesheet/payroll/invoice state machines, Supabase client,
  idempotency), 5 SQL migrations (organizations/users/roles, clients/workers/
  assignments, timesheets/approvals, invoices/payroll, RLS on every tenant
  table), synthetic seed data, RLS test file (6 assertions), API/ARCHITECTURE/
  DEPLOYMENT docs, Vitest + Playwright scaffolding.
- **What works:** `npm install` (154 packages), `tsc --noEmit` clean,
  Vitest 15/15 passed (independently re-run by coordinator), `npm run build`
  passed (after one real bug fix: login page needed `"use client"`),
  runtime smoke: `/`, `/login`, `/api/health` all HTTP 200.
- **What was tested:** Unit tests for decimal money math, state machines,
  permissions. Playwright: 1 passed (health endpoint), 2 browser tests failed
  ONLY because no Chromium is installed in this VM (download did not finish);
  run `npx playwright install chromium && npm run test:e2e` elsewhere.
  SQL migrations + RLS test were NOT executed (no PostgreSQL in this VM) —
  they must be run against a real Supabase project.
- **What remains:** Supabase Auth wiring; all API routes (contract in
  `app/docs/API.md`); all CRUD UI; QBO/Xero/payroll-provider/payment
  integrations (NOT CONNECTED by design).
- **How to run:** `cd app && npm install && npm run dev` (see `app/README.md`).
- **What the user needs to configure:** Free Supabase project; copy
  `.env.example` → `.env.local` with Supabase URL/keys; apply migrations
  0001–0005; run `supabase/tests/rls.test.sql`; deploy to Vercel Hobby
  (full steps in `app/docs/DEPLOYMENT.md`).

## Not started (Phases 4–15, in spec order)

- [ ] Phase 4 — Multi-tenant app: org registration, login, password reset, invitations, RBAC, org settings, user management (RLS already scaffolded in Phase 3).
- [ ] Phase 5 — Client management module.
- [ ] Phase 6 — Worker and vendor management (W-2 / C2C / independent contractor, no auto-classification).
- [ ] Phase 7 — Consultant assignments (decimal-safe bill/pay/margin math).
- [ ] Phase 8 — Timesheet workflow (draft → submitted → manager-approved → client-approved → locked; audit logs).
- [ ] Phase 9 — Client billing (invoices, PDF/CSV export; no payment processing).
- [ ] Phase 10 — Payroll preparation (estimates only; W-2 estimates vs C2C vendor payment prep reports).
- [ ] Phase 11 — Profitability dashboard (revenue, margin, outstanding invoices, CSV export).
- [ ] Phase 12 — Accounting integration (CSV in/out, journal-entry export; QBO/Xero/provider interfaces).
- [ ] Phase 13 — Security hardening (rate limiting, secure uploads, backups; RLS + audit logging already scaffolded).
- [ ] Phase 14 — Automated tests (auth, tenancy, permissions, calculations, workflows, exports).
- [ ] Phase 15 — Launch system (landing page, demo form backend, CRM structure, onboarding checklist, demo script, support templates, help center, pilot agreement, feedback/bug workflows) + 90-day plan for first 10 paying customers.

## Standing rules for this build

- Synthetic data only; never real payroll funds, deposits, tax filings, SSNs, or bank details.
- Payroll figures are estimates only; no certifications claimed.
- Never auto-classify C2C consultants as independent contractors.
- Borrow architecture patterns from open source; never copy code against its
  license (no GPL/AGPL code; no code from no-license repos).
- Decimal-safe money math (NUMERIC(19,4) in SQL, decimal.js in TypeScript).
- Every tenant-owned record carries an organization id; RLS enforces isolation.
- Working code only — unfinished features are marked as such, never faked.
