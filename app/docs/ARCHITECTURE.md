# StaffPilot Architecture

## Overview

StaffPilot is a multi-tenant B2B SaaS for staffing companies, consulting
firms, and employers managing 20–100 workers: staffing workflow, consultant
assignments, timesheets, client approvals, billing, and payroll
**preparation** (estimates only).

```
┌──────────────────────────────────────────────────────────────┐
│  Next.js 14 App Router (Vercel)                              │
│  app/            pages + API routes                          │
│  src/lib/        money.ts · permissions.ts · state-machines  │
│                  · supabase.ts · idempotency.ts              │
└──────────────────────┬───────────────────────────────────────┘
                       │ Supabase JS client (anon key; RLS applies)
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  Supabase — PostgreSQL + Auth (free tier)                    │
│  migrations 0001–0005 · RLS policies · seed (synthetic)      │
└──────────────────────────────────────────────────────────────┘
```

## Decision 1 — Multi-tenancy via PostgreSQL RLS (payrun pattern)

- Every tenant-owned table carries `organization_id`.
- Row-Level Security is enabled on **every** tenant table
  (`supabase/migrations/0005_row_level_security.sql`).
- Policies require membership: `public.is_org_member(organization_id)`,
  which checks `organization_members` for the JWT user id
  (`public.current_user_id()`, read from the PostgREST JWT claim).
- Application code **also** scopes queries by organization, but RLS is the
  guarantee: a bug in app code cannot leak another tenant's rows, because
  the database refuses them.
- Proof: `supabase/tests/rls.test.sql` — a user cannot read another org's
  rows, cannot insert into another org, and an unauthenticated caller sees
  nothing. Payroll estimates are further restricted to
  owner/administrator/payroll_manager/accountant roles.
- Trade-off: RLS policies must be kept in sync with the permission model in
  `src/lib/permissions.ts`. Both live in this repo; change them together.

## Decision 2 — Regulation/rules as configuration (PayrollEngine pattern)

- Payroll math lives in a pure, tested engine fed by configurable rules —
  never hard-coded tax logic. In this scaffold the engine is
  `src/lib/money.ts` (decimal math) plus `payroll_components` rows
  (earnings/deductions/employer costs as data, frappe/hrms pattern).
- **StaffPilot implements no US tax logic.** No federal/state withholding,
  no FICA, no unemployment tax is computed. Payroll runs are labelled
  estimates on the row (`estimate_disclaimer`) and in every API response.
- Real tax calculation comes only from a validated payroll-provider
  integration (Phase 12), which is not built yet.

## Decision 3 — Payroll lifecycle as a state machine (NomiFlow pattern)

```
payroll:  draft → calculated → approved → paid* / void
timesheet: draft → submitted → manager_approved → client_approved → locked
invoice:  draft → approved → sent → partially_paid → paid / overdue / void
```
- Transitions are defined in `src/lib/state-machines.ts` and mirrored by
  enum types in SQL. Invalid transitions return `422 invalid_transition`.
- `*paid` on a payroll run means "marked as paid in the external payroll
  provider" — StaffPilot never moves funds.
- Locked timesheets are immutable: a database trigger blocks any change to
  their entries (`prevent_locked_timesheet_change`).

## Decision 4 — Salary components as data (frappe/hrms pattern)

- `payroll_components` rows (`earning` / `deduction` / `employer_cost`,
  calculation `fixed_amount` | `per_hour` | `percent_of_gross_estimate`)
  are per-organization configuration, not code branches.
- `payroll_run_lines` snapshot the component name/kind/amount at calculation
  time, so a later component edit never rewrites history.

## Decision 5 — Decimal-safe money (universal lesson)

- Money is `NUMERIC(19,4)` in PostgreSQL and `decimal.js` in TypeScript
  (`src/lib/money.ts`). **No floats for money, ever.**
- Amounts travel the API as decimal strings (`"95.0000"`).
- Conversion to integer cents happens only at a payment-provider boundary —
  and no provider is connected, so `toCents`/`fromCents` are currently used
  only in tests.

## Decision 6 — Granular permissions behind roles (NomiFlow pattern)

- 7 roles: owner, administrator, payroll_manager, recruiter,
  client_manager, worker, accountant.
- Roles are bundles of granular permissions (`src/lib/permissions.ts`).
  Call sites check permissions, never role names.
- RLS policies enforce the coarse version of the same model in the
  database (e.g. workers cannot read `payroll_runs` at all).

## Decision 7 — API-first with idempotency

- Every money-adjacent `POST` requires an `Idempotency-Key` header.
  Replays return the stored response; key reuse with a different body is a
  `409`. Store: `idempotency_keys` table. See `docs/API.md`.
- API routes are the contract; the UI is a client of the same API.

## Decision 8 — Audit logging (append-only)

- `audit_logs` records actor, entity, action, and details JSON for every
  state transition and sensitive write.
- Append-only is enforced twice: no UPDATE/DELETE RLS policies exist, and
  database triggers raise on any UPDATE/DELETE attempt.
- Reads are restricted to owner/administrator/accountant/payroll_manager.

## Decision 9 — Worker classification is recorded, never auto-derived

- `workers.engagement_type` (`w2` / `c2c` / `independent_contractor`) is
  stored with a mandatory `classification_source` (e.g. `w2_offer_letter`,
  `vendor_agreement`).
- StaffPilot **never auto-classifies** a C2C consultant as an independent
  contractor. Changing the type requires owner/admin and is audit-logged.
- C2C workers must have a `vendor_name` (enforced by CHECK constraint).

## Integration interfaces — NOT CONNECTED

No external integration is connected in this scaffold. Each interface below
is documented so a future phase can implement it without redesigning the
domain model. Env vars for these are commented out in `.env.example`.

### QuickBooks Online / Xero (accounting sync)
- **Interface shape:** `POST /api/integrations/{qbo|xero}/invoices/:id/sync`
  pushes an approved invoice (lines, client, amounts as decimal strings) to
  the accounting system and stores the external invoice id + sync status on
  the invoice row. `GET /api/integrations/{qbo|xero}/status` reports
  connected/not-connected. OAuth 2.0 tokens are stored encrypted, never in
  code or env files beyond the client id/secret placeholders.
- **Status:** NOT CONNECTED. No credentials exist; no sync code exists.

### Payroll provider (real payroll execution + tax)
- **Interface shape:** `POST /api/integrations/payroll/runs/:id/export`
  sends the approved estimate (worker, hours, component lines) to the
  provider and records the provider's run id + confirmation. The provider
  owns tax calculation, direct deposit, and filing.
- **Status:** NOT CONNECTED. Provider not selected (Phase 12). StaffPilot's
  estimates must never be presented as tax calculations.

### Payment processor (invoice collection)
- **Interface shape:** `POST /api/integrations/payments/invoices/:id/link`
  creates a payment link; webhook `POST /api/integrations/payments/webhook`
  (signature-verified) records payments against the invoice. All amounts in
  integer cents at the provider boundary only.
- **Status:** NOT CONNECTED. Payments are recorded manually today.

## Boundaries (non-negotiable)

1. **Synthetic data only** in this repo. No real SSNs, bank details, or
   employee PII in code, migrations, or seed data.
2. **Payroll preparation only.** No real payroll funds, direct deposits,
   tax filings, or tax deposits — ever, in any phase, without a licensed
   provider integration and explicit user approval.
3. **No claimed certifications.** StaffPilot claims no payroll, tax, or
   accounting certification.
4. **No auto-classification** of workers (see Decision 9).
5. **No secrets in code.** Env vars only; `.env.local` is git-ignored.
6. **No GPL/AGPL code** from the researched repos (frappe/hrms, OrangeHRM,
   IceHrm, sheet-happens, NomiFlow, etc.) — patterns only, per
   `research/payroll-systems-shortlist.md`.
