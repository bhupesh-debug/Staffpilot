# StaffPilot Deployment — the $0 path

StaffPilot is designed to run at **$0/month** on free tiers for a small
staffing firm (20–100 workers), and to grow into paid tiers only when usage
demands it.

## The $0 path

| Layer | Service | Free tier |
|---|---|---|
| Frontend + API | **Vercel** (Hobby) | Free: 100 GB bandwidth/mo, serverless functions, automatic HTTPS, preview deploys |
| Database + Auth | **Supabase** (Free) | Free: 500 MB database, 1 GB file storage, 50,000 monthly active users, 500K Edge Function invocations |
| Source control | **GitHub** (Free) | Free: unlimited public/private repos |

## 1. Create the Supabase project

1. Go to https://supabase.com/dashboard → **New project**.
2. Pick a name (e.g. `staffpilot`), a strong database password, and the
   region closest to your users.
3. Wait for provisioning (~2 minutes).
4. In **Project Settings → API**, copy:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **anon / public key** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **service_role key** → `SUPABASE_SERVICE_ROLE_KEY` (server-only, never
     expose in the browser)

## 2. Apply the migrations

In the Supabase dashboard, open the **SQL Editor** and run, in order:

1. `supabase/migrations/0001_organizations_users_roles.sql`
2. `supabase/migrations/0002_clients_workers_assignments.sql`
3. `supabase/migrations/0003_timesheets_approvals.sql`
4. `supabase/migrations/0004_invoices_payroll.sql`
5. `supabase/migrations/0005_row_level_security.sql`

Or with the Supabase CLI (recommended once installed):

```bash
supabase link --project-ref <your-project-ref>
supabase db push
```

Verify RLS is on: every tenant table must show `Row Level Security:
Enabled` in **Table Editor**, and the policies from migration 0005 must be
listed. Then run the isolation proof:

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f supabase/tests/rls.test.sql
```

(The `DATABASE_URL` connection string is in **Project Settings → Database**.
Use the **service_role / postgres** connection for the test — it enables
`FORCE ROW LEVEL SECURITY` so the checks are meaningful.)

## 3. Load demo data (optional, local/dev only)

```bash
psql "$DATABASE_URL" -f supabase/seed.sql
```

Seed data is **synthetic** (fake people, fake companies). Never load it into
a production project, and never replace it with real employee data outside
the app's own onboarding flow.

## 4. Configure Supabase Auth

1. **Authentication → Providers → Email**: enable email sign-in.
2. **Authentication → URL Configuration**: set **Site URL** to your Vercel
   URL (e.g. `https://staffpilot.vercel.app`) and add
   `http://localhost:3000` to **Redirect URLs** for local dev.
3. No other providers are needed for MVP.

## 5. Deploy to Vercel

1. Push the repo to GitHub (the coordinator owns git; see repo README).
2. Go to https://vercel.com/new → **Import** the repo.
3. Framework preset: **Next.js**. Leave build settings as detected
   (`npm run build`).
4. In **Environment Variables**, add:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY` (server-only)
   - `NEXT_PUBLIC_APP_URL` = your Vercel URL
   - `APP_SECRET` = a random 32-byte hex string (`openssl rand -hex 32`)
5. **Deploy.** Vercel builds and gives you a `https://<app>.vercel.app` URL.
6. Smoke-check: visit `/api/health` — it must return `{"status":"ok",...}`.

## 6. Local development

```bash
cp .env.example .env.local   # fill in your Supabase values
npm install
npm run dev                  # http://localhost:3000
```

## What costs money if usage grows

| Trigger | What changes |
|---|---|
| Database > 500 MB | Supabase Pro ($25/mo) — more storage, daily backups, no pausing after inactivity |
| > 50,000 monthly active users | Supabase Pro (auth MAU overage) |
| Vercel bandwidth > 100 GB/mo or team features | Vercel Pro ($20/user/mo) |
| Supabase project paused after 7 days of inactivity (free tier) | Upgrade to Pro, or accept a cold start on first use after a pause |
| Real payroll/tax processing | A licensed payroll provider (Phase 12 integration) — priced by that provider, not by StaffPilot |
| QuickBooks Online / Xero sync | Those products' own subscription costs; the integration itself is just API calls |

## What is NOT configured by this deployment

- **No payment processor** is connected. Invoices record payments manually;
  online payment collection is a future integration.
- **No payroll provider** is connected. Payroll runs are estimates only.
- **No QuickBooks/Xero sync** is connected. Exports are CSV until an
  integration is deliberately configured (see `docs/ARCHITECTURE.md`).
- **No email provider beyond Supabase Auth emails.** Transactional email
  for invoices/approvals is a future step.
