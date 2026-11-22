# StaffPilot — Workforces. Projects. Payroll. One Platform.

B2B SaaS for staffing companies, consulting firms, and employers managing 20–100 workers:
staffing workflow, consultant assignments, timesheets, client approvals, billing,
payroll **preparation** (estimates only), and profitability reporting.

## What this repo is

- `research/` — verified open-source payroll-systems shortlist (Step 1 research).
- `docs/phase-1/` — business + product strategy (Phase 1, 11 documents).
- `website/` — public marketing website, 16 pages, static HTML/CSS/JS (Phase 2).
- `app/` — Next.js + TypeScript + Tailwind application with PostgreSQL/Supabase
  migrations, RLS, and tests (Phase 3 scaffold; Phases 4–15 build on it).

## Hard boundaries (non-negotiable)

- Synthetic data only in development and demos.
- No real payroll funds, direct deposits, tax filings, or tax deposits.
- No real SSNs or bank account information.
- Payroll figures are **estimates only** — never presented as official calculations.
- No claimed certifications or regulatory approval.
- C2C consultants are never auto-classified as independent contractors.
- Three things stay separate: (1) software subscription, (2) staffing/employment
  operations, (3) payroll processing and payment services.
- External providers (QuickBooks Online, Xero, payroll providers, payment
  processors) are documented integration interfaces marked NOT CONNECTED until
  a real integration is built.

## Quick start

**Website** (no build step):
```bash
cd website && python3 -m http.server 8137
# open http://localhost:8137/
```

**Application** (needs Node 20+):
```bash
cd app
npm install
cp .env.example .env.local   # fill in Supabase values — see app/docs/DEPLOYMENT.md
npm run dev                  # http://localhost:3000
npm run test                 # Vitest unit tests
npm run typecheck            # tsc --noEmit
```

## Status

See [CHECKLIST.md](CHECKLIST.md) for the milestone-by-milestone record:
what was built, what works, what was tested, what remains, and what the
user needs to configure.

## Suggested GitHub repo name

`staffpilot` under github.com/bhupesh-debug (user creates the empty repo first;
integrations cannot create repos). Push with the GitHub connector snapshot
procedure once the repo exists.
