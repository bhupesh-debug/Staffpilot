# StaffPilot API

Base URL (local): `http://localhost:3000/api`
Production: `https://<your-vercel-app>.vercel.app/api`

**Status: planned, not yet implemented.** The routes below are the contract
the frontend and integrations will be built against. The only live route in
this scaffold is `GET /api/health`. Each route's implementing file is listed
in the README's "Not yet implemented" section.

## Conventions

- **Auth:** Supabase Auth JWT in the `Authorization: Bearer <token>` header
  on every route except `/api/health`. The token's `sub` is the `app_users.id`;
  RLS enforces organization membership — a token for Org A cannot read Org B
  rows even if the caller guesses an ID.
- **Tenant scoping:** every request is scoped to the caller's organization
  via RLS. There is no `organization_id` query parameter to spoof.
- **Money:** all amounts are decimal strings with up to 4 places
  (e.g. `"95.0000"`), matching `NUMERIC(19,4)`. Never send floats.
- **Errors:** `{ "error": { "code": "string", "message": "string" } }` with
  HTTP status codes (400 validation, 401 unauthenticated, 403 forbidden —
  including RLS denials, 404 not found, 409 conflict, 422 invalid state
  transition, 500 server error).
- **Pagination:** `?page=1&per_page=25` (max 100). Responses include
  `{ "data": [...], "meta": { "page": 1, "per_page": 25, "total": 42 } }`.
- **Timestamps:** ISO 8601 UTC.

## Idempotency

Every money-adjacent `POST` **must** send an `Idempotency-Key` header
(a UUID v4 is recommended; any opaque token of 8–128 chars is accepted).
The server stores `(organization_id, endpoint, key, request-hash, response)`
in `idempotency_keys` for 24 hours:

- Same key + same body → the stored response is replayed (same status code),
  the operation is **not** re-executed.
- Same key + different body → `409` with code `idempotency_key_reused`.
- Missing key on a money-adjacent POST → `400` with code
  `idempotency_key_required`.

`GET` requests are safe to retry and take no key. `PUT`/`PATCH`/`DELETE`
are idempotent by construction but still accept a key.

## Routes

### Auth — `app/api/auth/[...]` (to be implemented in `app/api/auth/`)

| Method | Route | Purpose |
|---|---|---|
| POST | `/api/auth/invite` | Invite a user to the org (owner/admin). Body: `{ "email", "role" }`. Creates an `invitations` row and sends a Supabase invite email. |
| POST | `/api/auth/accept-invite` | Accept an invitation token. Body: `{ "token" }`. Creates the `organization_members` row. |
| GET | `/api/auth/me` | Current user + org memberships + role. |

### Organizations — `app/api/orgs/` (to be implemented)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/orgs` | Orgs the caller belongs to. |
| GET | `/api/orgs/:id` | One org (members only). |
| PATCH | `/api/orgs/:id` | Update name/plan (owner/admin). |

### Clients — `app/api/clients/` (to be implemented)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/clients` | List clients (paginated). |
| POST | `/api/clients` | Create a client. Body: `{ "name", "contact_name?", "contact_email?", "billing_email?", "payment_terms_days?" }`. |
| GET | `/api/clients/:id` | One client. |
| PATCH | `/api/clients/:id` | Update a client. |
| DELETE | `/api/clients/:id` | Deactivate (soft-delete via `is_active=false`; rows are never hard-deleted while assignments reference them). |

### Workers — `app/api/workers/` (to be implemented)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/workers` | List workers. Filter: `?engagement_type=w2\|c2c\|independent_contractor&is_active=true`. |
| POST | `/api/workers` | Create a worker. Body: `{ "full_name", "email?", "engagement_type", "classification_source", "vendor_name?", "title?", "skills?": [] }`. `classification_source` is **required** — the classification is recorded, never auto-derived. |
| GET | `/api/workers/:id` | One worker. |
| PATCH | `/api/workers/:id` | Update. Changing `engagement_type` is audit-logged and requires owner/admin. |

### Assignments — `app/api/assignments/` (to be implemented)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/assignments` | List assignments. Filters: `?worker_id=&client_id=&is_active=`. |
| POST | `/api/assignments` | Create. Body: `{ "worker_id", "client_id", "title", "bill_rate": "95.0000", "pay_rate": "65.0000", "start_date", "end_date?" }`. Server validates `pay_rate <= bill_rate` and returns computed `margin_amount` / `margin_percent` in the response. |
| GET | `/api/assignments/:id` | One assignment, with computed margin. |
| PATCH | `/api/assignments/:id` | Update rates/dates (creates an audit entry). |

**Example response:**
```json
{
  "id": "77777777-7777-7777-7777-777777777777",
  "worker_id": "55555555-5555-5555-5555-555555555555",
  "client_id": "33333333-3333-3333-3333-333333333333",
  "title": "Data Analyst — Globex",
  "bill_rate": "95.0000",
  "pay_rate": "65.0000",
  "margin_amount": "30.0000",
  "margin_percent": "31.5789",
  "start_date": "2026-11-01",
  "is_active": true
}
```

### Timesheets — `app/api/timesheets/` (to be implemented)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/timesheets` | List. Filters: `?worker_id=&status=&week_start_date=`. |
| POST | `/api/timesheets` | Create a draft for an assignment + week. Body: `{ "assignment_id", "week_start_date", "entries": [{ "work_date", "hours": "8.0000", "description?" }] }`. |
| GET | `/api/timesheets/:id` | One timesheet with entries and approval history. |
| PATCH | `/api/timesheets/:id` | Edit entries while `draft` or `rejected` only. Locked timesheets reject edits (`422`). |
| POST | `/api/timesheets/:id/submit` | `draft` → `submitted`. Requires `timesheets.submit`. |
| POST | `/api/timesheets/:id/approve-manager` | `submitted` → `manager_approved`. Requires `timesheets.approve_manager`. |
| POST | `/api/timesheets/:id/approve-client` | `manager_approved` → `client_approved`. Requires `timesheets.approve_client`. |
| POST | `/api/timesheets/:id/reject` | → `rejected`. Body: `{ "reason" }`. |
| POST | `/api/timesheets/:id/lock` | `client_approved` → `locked`. Requires `timesheets.lock`. |

Invalid transitions return `422` with code `invalid_transition`.

### Invoices — `app/api/invoices/` (to be implemented)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/invoices` | List. Filters: `?client_id=&status=`. |
| POST | `/api/invoices` | Create from approved timesheets. Body: `{ "client_id", "timesheet_ids": [], "issue_date?", "due_date?" }`. Lines are priced at the assignment bill rate; amounts computed with decimal math. Requires `Idempotency-Key`. |
| GET | `/api/invoices/:id` | One invoice with lines. |
| POST | `/api/invoices/:id/approve` | `draft` → `approved`. |
| POST | `/api/invoices/:id/send` | `approved` → `sent`. |
| POST | `/api/invoices/:id/record-payment` | Record a payment. Body: `{ "amount": "1000.0000", "paid_at?" }`. Moves `sent` → `partially_paid` → `paid`. Requires `Idempotency-Key`. |
| POST | `/api/invoices/:id/void` | → `void`. |

### Payroll preparation — `app/api/payroll/` (to be implemented)

All responses carry `estimate_disclaimer`. Nothing here moves money.

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/payroll/runs` | List payroll runs (estimates). |
| POST | `/api/payroll/runs` | Create a run. Body: `{ "name", "period_start", "period_end" }`. Requires `Idempotency-Key`. |
| GET | `/api/payroll/runs/:id` | One run with lines and totals. |
| POST | `/api/payroll/runs/:id/calculate` | `draft` → `calculated`. Computes line estimates from locked timesheets × pay rates + configured components (`payroll_components`). |
| POST | `/api/payroll/runs/:id/approve` | `calculated` → `approved`. Requires `payroll.approve`. |
| POST | `/api/payroll/runs/:id/mark-paid` | `approved` → `paid`. Records that payment was executed **in the external payroll provider** (provider name + reference required). StaffPilot never pays. |
| POST | `/api/payroll/runs/:id/void` | → `void`. |
| GET/POST | `/api/payroll/components` | List / create salary components (earnings, deductions, employer costs). |

### Reports — `app/api/reports/` (to be implemented)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/reports/margin?from=&to=` | Margin by assignment/client over a period. |
| GET | `/api/reports/utilization?from=&to=` | Billable hours vs capacity per worker. |
| GET | `/api/reports/aging` | Invoice aging (current / 30 / 60 / 90+ days). |
| GET | `/api/reports/payroll-estimate/:run_id` | Printable payroll-run estimate (CSV export). |

### Audit — `app/api/audit/` (to be implemented)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/audit?entity_type=&entity_id=` | Append-only audit log (owner/admin/accountant/payroll_manager). |
