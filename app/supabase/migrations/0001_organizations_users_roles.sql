-- StaffPilot migration 0001 — organizations (tenants), users, roles, invitations
-- Conventions: every tenant-owned table carries organization_id; money is
-- NUMERIC(19,4); UUID primary keys; created_at/updated_at on all tables.
-- All data in this repo is SYNTHETIC. No real SSNs, bank details, or payroll.

create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------------------
-- Helper: current authenticated user id, read from the PostgREST JWT claim.
-- Works in Supabase (request.jwt.claims is set per request) and in plain
-- Postgres tests (set it manually with set_config). RLS policies use this.
-- ---------------------------------------------------------------------------
create or replace function public.current_user_id()
returns uuid
language sql
stable
as $$
  select nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub'
$$;

-- ---------------------------------------------------------------------------
-- organizations — one row per tenant (staffing company / employer).
-- ---------------------------------------------------------------------------
create table public.organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text not null unique,
  -- Subscription / plan limits (NomiFlow pattern: feature limits per tenant).
  plan text not null default 'free' check (plan in ('free', 'starter', 'growth')),
  max_workers int not null default 100 check (max_workers > 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- app_users — profile row per Supabase Auth user. id IS the auth user id.
-- ---------------------------------------------------------------------------
create table public.app_users (
  id uuid primary key, -- references auth.users(id) in Supabase; not enforced here so migrations run on plain Postgres too
  email text not null unique,
  full_name text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- organization_members — membership + role per tenant.
-- Roles: owner, administrator, payroll_manager, recruiter, client_manager,
-- worker, accountant. Permission sets live in src/lib/permissions.ts and
-- must stay in sync with this enum.
-- ---------------------------------------------------------------------------
create type public.org_role as enum (
  'owner', 'administrator', 'payroll_manager', 'recruiter',
  'client_manager', 'worker', 'accountant'
);

create table public.organization_members (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  user_id uuid not null references public.app_users(id) on delete cascade,
  role public.org_role not null,
  invited_by uuid references public.app_users(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (organization_id, user_id)
);

create index idx_org_members_org on public.organization_members (organization_id);
create index idx_org_members_user on public.organization_members (user_id);

-- ---------------------------------------------------------------------------
-- invitations — email invites to join an organization (NomiFlow pattern).
-- A row is consumed once; acceptance creates an organization_members row.
-- ---------------------------------------------------------------------------
create table public.invitations (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  email text not null,
  role public.org_role not null,
  token text not null unique,
  invited_by uuid references public.app_users(id) on delete set null,
  accepted_at timestamptz,
  expires_at timestamptz not null default (now() + interval '7 days'),
  created_at timestamptz not null default now(),
  unique (organization_id, email)
);

create index idx_invitations_org on public.invitations (organization_id);
create index idx_invitations_token on public.invitations (token);

-- ---------------------------------------------------------------------------
-- audit_logs — append-only. No UPDATE/DELETE allowed (enforced by trigger
-- in migration 0004 and by RLS: no update/delete policies exist).
-- ---------------------------------------------------------------------------
create table public.audit_logs (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  actor_user_id uuid references public.app_users(id) on delete set null,
  entity_type text not null,          -- e.g. 'timesheet', 'payroll_run'
  entity_id uuid not null,
  action text not null,               -- e.g. 'timesheet.submitted'
  details jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index idx_audit_org_entity on public.audit_logs (organization_id, entity_type, entity_id);
create index idx_audit_org_created on public.audit_logs (organization_id, created_at desc);

-- ---------------------------------------------------------------------------
-- idempotency_keys — replay store for money-adjacent POSTs (see docs/API.md).
-- ---------------------------------------------------------------------------
create table public.idempotency_keys (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  endpoint text not null,
  idempotency_key text not null,
  request_hash text not null,
  response_status int not null,
  response_body jsonb not null,
  created_at timestamptz not null default now(),
  unique (organization_id, endpoint, idempotency_key)
);

create index idx_idempotency_lookup on public.idempotency_keys (organization_id, endpoint, idempotency_key);
