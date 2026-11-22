-- StaffPilot seed — SYNTHETIC DEMO DATA ONLY.
-- Every person, company, rate, and figure below is invented for local
-- development and demos. No real people, no real SSNs, no real bank details.
-- Load with the Supabase service role (bypasses RLS) or psql as superuser.
-- Safe to re-run: ON CONFLICT clauses make it idempotent.

begin;

insert into public.organizations (id, name, slug, plan, max_workers) values
  ('11111111-1111-1111-1111-111111111111', 'Acme Staffing (Demo)', 'acme-staffing-demo', 'growth', 100),
  ('22222222-2222-2222-2222-222222222222', 'Other Org (Demo — isolation test)', 'other-org-demo', 'free', 20)
on conflict (id) do nothing;

insert into public.app_users (id, email, full_name) values
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'owner@acme-demo.example', 'Ada Owner (Demo)'),
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'worker@acme-demo.example', 'Walt Worker (Demo)'),
  ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'outsider@other-demo.example', 'Ollie Outsider (Demo)')
on conflict (id) do nothing;

insert into public.organization_members (organization_id, user_id, role) values
  ('11111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'owner'),
  ('11111111-1111-1111-1111-111111111111', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'worker'),
  ('22222222-2222-2222-2222-222222222222', 'cccccccc-cccc-cccc-cccc-cccccccccccc', 'owner')
on conflict (organization_id, user_id) do nothing;

insert into public.clients (id, organization_id, name, contact_name, contact_email, payment_terms_days) values
  ('33333333-3333-3333-3333-333333333333', '11111111-1111-1111-1111-111111111111', 'Globex Corp (Demo)', 'Gina Globex', 'gina@globex-demo.example', 30),
  ('44444444-4444-4444-4444-444444444444', '22222222-2222-2222-2222-222222222222', 'Other Client (Demo)', 'Oscar Other', 'oscar@other-demo.example', 30)
on conflict (id) do nothing;

insert into public.workers (id, organization_id, user_id, full_name, email, engagement_type, classification_source, title) values
  ('55555555-5555-5555-5555-555555555555', '11111111-1111-1111-1111-111111111111', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Walt Worker (Demo)', 'worker@acme-demo.example', 'w2', 'w2_offer_letter', 'Data Analyst'),
  ('66666666-6666-6666-6666-666666666666', '11111111-1111-1111-1111-111111111111', null, 'Vera Vendor (Demo)', 'vera@vendor-demo.example', 'c2c', 'vendor_agreement', 'Software Engineer')
on conflict (id) do nothing;

-- C2C worker needs a vendor name (see CHECK constraint in 0002).
update public.workers set vendor_name = 'VendorCo (Demo)' where id = '66666666-6666-6666-6666-666666666666';

insert into public.assignments (id, organization_id, worker_id, client_id, title, bill_rate, pay_rate, start_date) values
  ('77777777-7777-7777-7777-777777777777', '11111111-1111-1111-1111-111111111111', '55555555-5555-5555-5555-555555555555', '33333333-3333-3333-3333-333333333333', 'Data Analyst — Globex (Demo)', 95.0000, 65.0000, '2026-11-01')
on conflict (id) do nothing;

insert into public.timesheets (id, organization_id, assignment_id, worker_id, week_start_date, status) values
  ('88888888-8888-8888-8888-888888888888', '11111111-1111-1111-1111-111111111111', '77777777-7777-7777-7777-777777777777', '55555555-5555-5555-5555-555555555555', '2026-11-16', 'draft')
on conflict (id) do nothing;

insert into public.timesheet_entries (timesheet_id, organization_id, work_date, hours, description) values
  ('88888888-8888-8888-8888-888888888888', '11111111-1111-1111-1111-111111111111', '2026-11-16', 8.0000, 'Demo work — Monday'),
  ('88888888-8888-8888-8888-888888888888', '11111111-1111-1111-1111-111111111111', '2026-11-17', 8.0000, 'Demo work — Tuesday')
on conflict (timesheet_id, work_date) do nothing;

insert into public.payroll_components (id, organization_id, name, kind, calculation) values
  ('99999999-9999-9999-9999-999999999999', '11111111-1111-1111-1111-111111111111', 'Regular pay', 'earning', 'per_hour')
on conflict (organization_id, name) do nothing;

insert into public.payroll_runs (id, organization_id, name, period_start, period_end, status) values
  ('12121212-1212-1212-1212-121212121212', '11111111-1111-1111-1111-111111111111', '2026-11-16 Biweekly — ESTIMATE', '2026-11-16', '2026-11-29', 'draft')
on conflict (id) do nothing;

commit;
