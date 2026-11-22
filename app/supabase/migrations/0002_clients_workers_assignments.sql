-- StaffPilot migration 0002 — clients, workers/vendors, assignments
-- Money: NUMERIC(19,4) everywhere. No floats for money, ever.

-- ---------------------------------------------------------------------------
-- clients — the staffing firm's customers (employers receiving workers).
-- ---------------------------------------------------------------------------
create table public.clients (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  name text not null,
  contact_name text,
  contact_email text,
  billing_email text,
  address text,
  -- Net payment terms in days (e.g. 30 = Net 30).
  payment_terms_days int not null default 30 check (payment_terms_days >= 0),
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index idx_clients_org on public.clients (organization_id);

-- ---------------------------------------------------------------------------
-- workers — consultants / employees placed at clients.
-- engagement_type is RECORDED from source documents, never auto-derived:
-- classification_source names where the classification came from
-- (e.g. 'w2_offer_letter', 'vendor_agreement', 'client_msa').
-- StaffPilot NEVER auto-classifies a C2C consultant as an independent
-- contractor. Any change to engagement_type must be a deliberate,
-- human-entered update and is audit-logged.
-- No SSN / bank account columns exist by design.
-- ---------------------------------------------------------------------------
create type public.engagement_type as enum ('w2', 'c2c', 'independent_contractor');

create table public.workers (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  -- Optional link to the worker's login (app_users) so workers can submit
  -- their own timesheets. Null for vendor-supplied workers with no login.
  user_id uuid references public.app_users(id) on delete set null,
  full_name text not null,
  email text,
  phone text,
  engagement_type public.engagement_type not null,
  classification_source text not null,
  -- Vendor (employer of record) for C2C workers, e.g. the vendor company.
  vendor_name text,
  title text,
  skills text[] not null default '{}',
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint workers_c2c_requires_vendor
    check (engagement_type <> 'c2c' or vendor_name is not null)
);

create index idx_workers_org on public.workers (organization_id);
create index idx_workers_user on public.workers (user_id);

-- ---------------------------------------------------------------------------
-- assignments — a worker placed at a client. Bill rate vs pay rate is the
-- margin model; both NUMERIC(19,4) per hour.
-- ---------------------------------------------------------------------------
create table public.assignments (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  worker_id uuid not null references public.workers(id) on delete restrict,
  client_id uuid not null references public.clients(id) on delete restrict,
  title text not null,
  bill_rate numeric(19,4) not null check (bill_rate >= 0),
  pay_rate numeric(19,4) not null check (pay_rate >= 0),
  currency text not null default 'USD',
  start_date date not null,
  end_date date,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint assignments_dates check (end_date is null or end_date >= start_date),
  constraint assignments_pay_not_above_bill check (pay_rate <= bill_rate)
);

create index idx_assignments_org on public.assignments (organization_id);
create index idx_assignments_worker on public.assignments (worker_id);
create index idx_assignments_client on public.assignments (client_id);
