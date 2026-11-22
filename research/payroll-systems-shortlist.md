# StaffPilot — Payroll Systems Research Shortlist

**Researched:** November 22, 2026 (all repos verified live via the GitHub connector on this date)
**Source:** https://github.com/topics/payroll-management-system (181 public repos) plus adjacent searches (HRMS, multi-tenant payroll SaaS, timesheet, staffing/VMS).

## Headline finding

The topic itself is thin: the two most-starred repos on the topic have ~140 stars each, and most of the 181 are small or school projects. The serious open-source payroll/HR systems live **outside** the topic tag. StaffPilot should borrow **architecture patterns** from the shortlist below — never copy code against its license. GPL/AGPL code must not enter a proprietary SaaS codebase; no-license repos are all-rights-reserved and are study-only.

## Ranked shortlist

### 1. Payroll-Engine / PayrollEngine — ★141 · MIT · .NET · updated Nov 13, 2026
**What it does:** Open-source payroll automation framework. Build multi-country, multi-industry payroll applications with configurable regulation layers. Docker stack, JSON schemas, automated tests, NuGet packages, docs at payrollengine.org.
**Borrow:** Regulation-as-config (payroll rules as data, not hard-coded logic) — this is exactly how StaffPilot should keep tax/payroll logic pluggable and estimates-only. Payroll calculation as a pure, testable engine. API-first design. Test-driven development with a full automated suite.
**Avoid:** Its .NET stack (StaffPilot is Next.js/TypeScript by spec); its multi-country regulation layers are far beyond MVP scope.

### 2. frappe / hrms (ERPNext HR) — ★9,090 · GPL-3.0 · Python/Frappe · updated Nov 21, 2026
**What it does:** The largest open-source HR + payroll system. Salary structures and components, payroll entries, tax slabs, loans/advances, leave, attendance, expenses.
**Borrow:** Data-model ideas only — salary structure → salary components → payroll entry; the separation of earnings/deductions as configurable components; loan/advance handling. Its scale proves the domain model works.
**Avoid:** DO NOT copy code — GPL-3.0 copyleft would infect a proprietary SaaS. Do not adopt its monolithic ERP scope for an MVP.

### 3. Coretech001 / NomiFlow — ★4 · NO LICENSE · .NET 9 + React 19 + TypeScript + PostgreSQL · updated Nov 20, 2026
**What it does:** Multi-tenant payroll and workforce-management SaaS (Panama compliance). Payroll lifecycle Draft → Calculated → Approved → Paid; 29 granular permissions + custom roles; tenant-based data isolation; email invitations; subscription feature limits; B2B API with SHA-256 API keys, rate limiting, quotas, idempotency keys; PDF payslips, Excel exports.
**Borrow:** The closest functional twin to StaffPilot. The payroll lifecycle state machine, the granular-permission model (maps to StaffPilot's 7 roles), the B2B API discipline (idempotency keys, quotas), and the tenant-isolation approach.
**Avoid:** NO LICENSE = all rights reserved — study patterns only, never copy code. Its Panama-specific tax logic is irrelevant to US payroll and must not be adapted as if it were US tax logic.

### 4. euron-sde-team / euron-open-hrms — ★18 · MIT · TypeScript · updated Nov 18, 2026
**What it does:** Open-source multi-tenant HRMS: payroll in 24 countries, leave, attendance, onboarding.
**Borrow:** The modern-TypeScript multi-tenant reference closest to StaffPilot's stack. Multi-country payroll done as configuration, not forks.
**Avoid:** Small and young (18 stars); treat as a reference, not a foundation to build on.

### 5. highoncarbs / Hafta — ★147 · MIT · Flask + Vue.js + Bulma/Buefy + SQLAlchemy + MySQL · updated Oct 1, 2026
**What it does:** The most-starred repo on the topic itself. Simple payroll for Indian manufacturing: employees, advances with per-employee limits, attendance, payroll, performance/incident reports.
**Borrow:** The simple master-data pattern (masters for quick customization); the advance/limit model (maps to StaffPilot's adjustments); proof that a small, focused payroll tool can stay maintainable.
**Avoid:** India-specific payroll assumptions; Flask/Vue stack (not StaffPilot's); single-tenant design.

### 6. orangehrm / orangehrm — ★1,161 · GPL · PHP/Symfony · updated Nov 19, 2026
**What it does:** Mature, comprehensive HRM: PIM, leave, time, attendance, recruitment, performance, payroll module.
**Borrow:** Module boundaries (PIM vs leave vs time vs payroll kept separate); the leave/attendance/time data models; its longevity as a lesson in what to modularize early.
**Avoid:** GPL — patterns only, no code. PHP stack; enterprise breadth far beyond MVP.

### 7. gamonoid / icehrm — ★741 · GPL · JavaScript/PHP · updated Nov 19, 2026
**What it does:** Lightweight, self-hosted HRM: employees, leave, attendance, expenses, documents.
**Borrow:** The lightweight employee-record model and the document-checklist idea (maps to StaffPilot Phase 6).
**Avoid:** GPL — patterns only. Dated stack; no payroll depth.

### 8. onRubik / supabasePayroll — ★8 · MIT · Supabase (PostgreSQL) + Node.js · updated Apr 25, 2025
**What it does:** A simplified, normalized payroll schema on Supabase: event records (vacations, days off), SQL CREATE TABLE scripts, Supabase JS client usage.
**Borrow:** Directly matches StaffPilot's spec stack (Supabase Auth + PostgreSQL). A normalized event-record schema is a good starting sketch for StaffPilot's own migrations — as a pattern to rewrite, not code to copy verbatim. Stale (Apr 2025) but the schema ideas hold.
**Avoid:** Tiny and unmaintained; demo-grade, no RLS, no multi-tenancy, no tests.

### 9. suyanto98 / payrun — ★0 · MIT · Go + PostgreSQL (RLS) + Vue · updated Oct 12, 2026
**What it does:** Multi-tenant payroll SaaS explicitly built on PostgreSQL row-level security.
**Borrow:** The RLS multi-tenant pattern — the single most relevant architectural reference for StaffPilot Phases 4 and 13 (tenant isolation at the database level, not just in application code).
**Avoid:** Zero stars, unproven, Go stack; study the RLS approach, do not depend on the project.

### 10. rolloutit / sheet-happens — ★3 · AGPL · TypeScript · updated Nov 4, 2026
**What it does:** Open-source time tracking and timesheet approval for companies and their contractors.
**Borrow:** The timesheet approval workflow (draft → submitted → approved) for companies *and contractors* — directly maps to StaffPilot Phase 8, including the contractor (C2C) angle.
**Avoid:** AGPL — patterns only, no code. Very small.

## Honorable mentions
- **timetrex / TimeTrex** — mature PHP workforce + payroll/time suite (time, attendance, scheduling, payroll). License could not be verified from the repo root on this date; TimeTrex CE was historically AGPL — verify before using anything from it. Study its time-and-attendance depth.
- **udayasri10435 / NexusVMS-Contingent-Workforce-Platform** (★0, no license) — the only staffing/VMS hit found: enterprise vendor-management / contingent-workforce platform. Study-only domain model for the staffing-agency side; no code reuse.
- **Devnawjesh / hr-payroll** (★302, Laravel/PHP, updated Nov 21, 2026, no license file found) — popular Laravel HRM; study-only.
- **Hamza-code-hub / NexusHR-Multi-Tenant-HR-Payroll-Accounting-SaaS** (Go + Fiber + Postgres, no license) and **Harsha-code-per / rostra** (Next.js + FastAPI + Postgres multi-tenant SaaS, no license) — both mirror StaffPilot's intended architecture; study-only.

## What StaffPilot takes from this research (architecture patterns)
1. **Regulation/rules as configuration** (PayrollEngine): payroll math lives in a pure, tested engine fed by configurable rules — never hard-coded tax logic.
2. **Payroll lifecycle as a state machine** (NomiFlow): Draft → Calculated → Approved → Paid, with audit history at every transition.
3. **Salary components as data** (frappe/hrms): earnings/deductions are configurable components, not code branches.
4. **Tenant isolation at the database level** (payrun): PostgreSQL RLS, every tenant-owned row carries an organization id.
5. **Granular permissions behind roles** (NomiFlow): the 7 roles map to permission sets, not to hard-coded if-statements.
6. **API-first with idempotency** (NomiFlow, PayrollEngine): every money-adjacent operation is idempotent and keyed.
7. **Decimal-safe money math everywhere** (universal lesson): no floats for money, ever.
8. **Timesheets as an approval workflow, not a form** (sheet-happens): draft → submitted → manager-approved → client-approved, locked after approval, audit-logged.

## What StaffPilot must NOT take from these repos
- Any GPL/AGPL code (frappe/hrms, OrangeHRM, IceHrm, sheet-happens) — copyleft would attach to a proprietary SaaS.
- Any code from no-license repos (NomiFlow, NexusVMS, NexusHR, rostra, Devnawjesh/hr-payroll) — all rights reserved.
- Any US tax logic: **none** of these repos implements US federal/state payroll tax correctly. StaffPilot's payroll module is estimates-only by design; real tax calculation comes only from a validated provider integration (Phase 12).
- Staffing-agency depth: no mature open-source staffing/VMS exists in this survey — StaffPilot's assignment/bill-rate/pay-rate/margin model is original work, not borrowed.

## Verification note
Stars, languages, licenses, and last-updated dates above were read live from GitHub on Nov 22, 2026. Star counts move; re-check before citing them externally. License findings are from each repo's LICENSE/LICENSE.md/license.txt file as read on that date; where no license file was found it is recorded as NO-LICENSE-FILE (not "public domain" — no license means no reuse rights).
