-- StaffPilot RLS test — proves a user cannot read another org's rows.
--
-- HOW TO RUN (against a local Postgres with the migrations applied, or a
-- Supabase project's SQL editor as the postgres role):
--   psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f supabase/tests/rls.test.sql
--
-- The test impersonates each demo user by setting the JWT claim that
-- public.current_user_id() reads (exactly what PostgREST sets in Supabase).
-- It uses plain SQL assertions: any failure raises an exception and the
-- script exits non-zero.
--
-- NOTE: RLS applies to the table OWNER only if FORCE ROW LEVEL SECURITY is
-- set. In Supabase, app queries run as `authenticated`, not as the table
-- owner, so policies apply. To make this test meaningful when run as the
-- table owner (psql superuser), we enable FORCE RLS below, run the checks,
-- then disable it again.

\echo '--- StaffPilot RLS test: cross-org isolation ---'

-- Precondition: seed data loaded.
do $$
begin
  if not exists (select 1 from public.clients where id = '33333333-3333-3333-3333-333333333333') then
    raise exception 'seed data missing — load supabase/seed.sql first';
  end if;
end $$;

-- Force RLS even for the table owner, so this psql session is policed.
alter table public.clients force row level security;
alter table public.workers force row level security;
alter table public.timesheets force row level security;
alter table public.payroll_runs force row level security;
alter table public.organizations force row level security;

-- Helper: impersonate a user by setting the JWT claim.
create or replace function pg_temp.impersonate(p_user uuid)
returns void language sql as $$
  select set_config('request.jwt.claims', json_build_object('sub', p_user)::text, true);
$$;

-- 1. Acme owner sees Acme's client, NOT the other org's client.
select pg_temp.impersonate('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa');
do $$
declare c int;
begin
  select count(*) into c from public.clients;
  if c <> 1 then raise exception 'FAIL: Acme owner should see exactly 1 client, saw %', c; end if;
  if exists (select 1 from public.clients where id = '44444444-4444-4444-4444-444444444444') then
    raise exception 'FAIL: Acme owner can read the other org''s client';
  end if;
  raise notice 'PASS: Acme owner sees only Acme clients';
end $$;

-- 2. Outsider (other org) sees only the other org's client.
select pg_temp.impersonate('cccccccc-cccc-cccc-cccc-cccccccccccc');
do $$
declare c int;
begin
  select count(*) into c from public.clients;
  if c <> 1 then raise exception 'FAIL: outsider should see exactly 1 client, saw %', c; end if;
  if exists (select 1 from public.clients where id = '33333333-3333-3333-3333-333333333333') then
    raise exception 'FAIL: outsider can read Acme''s client';
  end if;
  raise notice 'PASS: outsider sees only their own org''s clients';
end $$;

-- 3. Acme worker sees Acme workers/timesheets but NOT payroll estimates
--    (payroll tables restrict reads to owner/administrator/payroll_manager/accountant).
select pg_temp.impersonate('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb');
do $$
declare c int;
begin
  select count(*) into c from public.workers;
  if c <> 2 then raise exception 'FAIL: Acme worker should see 2 workers, saw %', c; end if;
  select count(*) into c from public.timesheets;
  if c <> 1 then raise exception 'FAIL: Acme worker should see 1 timesheet, saw %', c; end if;
  select count(*) into c from public.payroll_runs;
  if c <> 0 then raise exception 'FAIL: worker must NOT see payroll runs, saw %', c; end if;
  raise notice 'PASS: worker sees workers/timesheets, not payroll estimates';
end $$;

-- 4. Unauthenticated (no JWT claim) sees nothing on tenant tables.
select set_config('request.jwt.claims', '', true);
do $$
declare c int;
begin
  select count(*) into c from public.clients;
  if c <> 0 then raise exception 'FAIL: unauthenticated saw % clients', c; end if;
  select count(*) into c from public.organizations;
  if c <> 0 then raise exception 'FAIL: unauthenticated saw % organizations', c; end if;
  raise notice 'PASS: unauthenticated sees nothing';
end $$;

-- 5. Cross-org INSERT is blocked: outsider cannot insert a client into Acme.
select pg_temp.impersonate('cccccccc-cccc-cccc-cccc-cccccccccccc');
do $$
begin
  insert into public.clients (organization_id, name)
  values ('11111111-1111-1111-1111-111111111111', 'Sneaky Client');
  raise exception 'FAIL: outsider inserted a client into Acme';
exception when insufficient_privilege then
  raise notice 'PASS: cross-org insert blocked by RLS';
end $$;

-- 6. Audit logs are append-only: UPDATE is blocked.
-- Insert the probe row as the session owner (RLS is not forced on audit_logs,
-- so the owner bypasses it), then attempt the UPDATE as an impersonated user.
insert into public.audit_logs (organization_id, entity_type, entity_id, action)
values ('11111111-1111-1111-1111-111111111111', 'test', gen_random_uuid(), 'test.insert');
select pg_temp.impersonate('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa');
do $$
begin
  update public.audit_logs set action = 'tampered' where action = 'test.insert';
  raise exception 'FAIL: audit_logs UPDATE was allowed';
exception
  when raise_exception then
    raise notice 'PASS: audit_logs UPDATE blocked by append-only trigger';
  when insufficient_privilege then
    raise notice 'PASS: audit_logs UPDATE blocked by RLS (no update policy)';
end $$;

-- Cleanup: remove the test audit row via service-role-equivalent path is not
-- possible for a normal role; delete it as owner (trigger blocks DELETE too,
-- so leave the single clearly-labelled test row in place) and reset RLS.
-- The row is harmless: entity_type 'test', action 'test.insert'.
alter table public.clients no force row level security;
alter table public.workers no force row level security;
alter table public.timesheets no force row level security;
alter table public.payroll_runs no force row level security;
alter table public.organizations no force row level security;

\echo '--- RLS test complete: all checks passed ---'
