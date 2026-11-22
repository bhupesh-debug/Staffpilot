# StaffPilot

**Staffing operations for teams of 20–100 workers.**

StaffPilot is a B2B SaaS for staffing companies, consulting firms, and
employers: staffing workflow, consultant assignments, timesheets, client
approvals, billing, and payroll **preparation** (estimates only).

> **Boundary — read first.** StaffPilot is payroll *preparation* only. All
> payroll figures are estimates. StaffPilot never processes real payroll
> funds, direct deposits, tax filings, or tax deposits; never stores real
> SSNs or bank account details; and claims no payroll or tax certification.
> All data in this repository is **synthetic demo data**.

## Stack

| Layer | Choice |
|---|---|
| Frontend + API | Next.js 14 (App Router) + TypeScript + Tailwind CSS |
| Database | PostgreSQL (Supabase) with Row-Level Security |
| Auth | Supabase Auth (JWT; RLS enforced per request) |
| Money math | `decimal.js` — no floats for money, ever |
| Unit tests | Vitest |
| E2E tests | Playwright |
| Deployment ($0 path) | Vercel Hobby + Supabase Free — see `docs/DEPLOYMENT.md` |

Architecture patterns borrowed from the research in
`../research/payroll-systems-shortlist.md`: regulation/rules as configuration
(PayrollEngine), payroll lifecycle as a state machine (NomiFlow), salary
components as data (frappe/hrms), tenant isolation via PostgreSQL RLS
(payrun), granular permissions behind roles (NomiFlow), API-first with
idempotency, decimal-safe money, timesheets as an approval workflow.

## Run locally

```bash
cp .env.example .env.local   # fill in your Supabase values (see below)
npm install
npm run dev                  # http://localhost:3000
```

| Command | What it does |
|---|---|
| `npm run dev` | Start the dev server |
| `npm run build` | Production build |
| `npm run start` | Serve the production build |
| `npm run test` | Vitest unit tests |
| `npm run test:e2e` | Playwright smoke tests (starts dev server automatically) |
| `npm run lint` | Next.js lint |
| `npm run typecheck` | `tsc --noEmit` |

## What works today

- Home page (`app/page.tsx`) — real, renders, links to login + health check.
- Health check — `GET /api/health` returns `{ "status": "ok", ... }`.
- Login page (`app/login/page.tsx`) — real page that detects whether Supabase
  env vars are set and explains how to configure auth. The sign-in form is a
  placeholder until Supabase Auth is wired (see below).
- Decimal money library (`src/lib/money.ts`) — margin, line totals, exact
  sums, cents conversion; covered by passing Vitest tests.
- Permissions model (`src/lib/permissions.ts`) — 7 roles → 19 granular
  permissions; covered by tests.
- State machines (`src/lib/state-machines.ts`) — timesheet, payroll-run, and
  invoice transitions; covered by tests.
- Idempotency helper (`src/lib/idempotency.ts`) — key validation + request
  hashing for money-adjacent POSTs.
- Database — full domain model in `supabase/migrations/` (0001–0005):
  organizations, users + roles, invitations, clients, workers/vendors,
  assignments, timesheets + entries, approvals, audit logs (append-only),
  invoices, payroll runs + lines + components (estimates only),
  idempotency keys — with RLS policies on every tenant table and a
  cross-org isolation test (`supabase/tests/rls.test.sql`).
- Docs — `docs/API.md` (route contract + idempotency convention),
  `docs/DEPLOYMENT.md` ($0 Vercel + Supabase path),
  `docs/ARCHITECTURE.md` (decisions + NOT-CONNECTED integration interfaces).

## Not yet implemented

Nothing below is claimed to work. Each item names the file/route that will
implement it.

| Feature | Will live in |
|---|---|
| Supabase Auth sign-in (email magic link / password) | `app/login/page.tsx` + `src/lib/supabase.ts` |
| Auth API: invite / accept-invite / me | `app/api/auth/` |
| Orgs API | `app/api/orgs/` |
| Clients API + UI | `app/api/clients/` |
| Workers API + UI | `app/api/workers/` |
| Assignments API + UI (margin display) | `app/api/assignments/` |
| Timesheets API + UI (submit/approve/lock) | `app/api/timesheets/` |
| Invoices API + UI | `app/api/invoices/` |
| Payroll preparation API + UI (estimates) | `app/api/payroll/` |
| Reports API + UI | `app/api/reports/` |
| Audit log viewer | `app/api/audit/` |
| QuickBooks Online / Xero sync | `app/api/integrations/` — NOT CONNECTED (see `docs/ARCHITECTURE.md`) |
| Payroll provider integration | `app/api/integrations/payroll/` — NOT CONNECTED |
| Payment processor integration | `app/api/integrations/payments/` — NOT CONNECTED |

## Configuration (what you need)

1. **Supabase project** (free): create one at supabase.com, then copy
   `.env.example` → `.env.local` and fill in `NEXT_PUBLIC_SUPABASE_URL`,
   `NEXT_PUBLIC_SUPABASE_ANON_KEY`, and `SUPABASE_SERVICE_ROLE_KEY`.
2. **Migrations:** run `supabase/migrations/0001`–`0005` in order against
   that project (SQL Editor or `supabase db push`), then run
   `supabase/tests/rls.test.sql` to prove cross-org isolation.
3. **Seed (dev only):** `supabase/seed.sql` — synthetic demo data.
4. **Deploy:** Vercel Hobby, import the repo, set the env vars above.
   Full steps in `docs/DEPLOYMENT.md`.

## Project layout

```
app/                  Next.js App Router (pages, API routes, styles)
src/lib/              money, permissions, state-machines, supabase, idempotency
supabase/
  migrations/         0001–0005 (domain model + RLS)
  seed.sql            synthetic demo data
  tests/              rls.test.sql (cross-org isolation proof)
tests/
  unit/               Vitest tests (money, state machines, permissions)
  e2e/                Playwright smoke tests
docs/                 API.md, DEPLOYMENT.md, ARCHITECTURE.md
```

## License / reuse note

Original code in this repository is StaffPilot's own. Architecture patterns
were studied from the repos listed in
`../research/payroll-systems-shortlist.md`; no GPL/AGPL or unlicensed code
was copied into this codebase.
