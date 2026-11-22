-- StaffPilot migration 0004 — invoices, payroll runs (ESTIMATES ONLY), audit guard
-- Payroll runs are PREPARATION estimates. Column and status names say so.
-- StaffPilot never moves payroll funds, files taxes, or stores SSNs/bank data.

-- ---------------------------------------------------------------------------
-- invoices — generated from approved timesheets.
-- ---------------------------------------------------------------------------
create type public.invoice_status as enum (
  'draft', 'approved', 'sent', 'partially_paid', 'paid', 'overdue', 'void'
);

create table public.invoices (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  client_id uuid not null references public.clients(id) on delete restrict,
  invoice_number text not null,
  status public.invoice_status not null default 'draft',
  -- Amounts are NUMERIC(19,4). amount_due = subtotal + tax_estimate - paid.
  subtotal numeric(19,4) not null default 0 check (subtotal >= 0),
  tax_estimate numeric(19,4) not null default 0 check (tax_estimate >= 0),
  amount_paid numeric(19,4) not null default 0 check (amount_paid >= 0),
  currency text not null default 'USD',
  issue_date date not null default current_date,
  due_date date,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (organization_id, invoice_number)
);

create index idx_invoices_org on public.invoices (organization_id);
create index idx_invoices_client on public.invoices (client_id);
create index idx_invoices_status on public.invoices (organization_id, status);

create table public.invoice_lines (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  invoice_id uuid not null references public.invoices(id) on delete cascade,
  timesheet_id uuid references public.timesheets(id) on delete set null,
  description text not null,
  hours numeric(19,4) not null default 0 check (hours >= 0),
  rate numeric(19,4) not null check (rate >= 0),
  amount numeric(19,4) not null check (amount >= 0),
  created_at timestamptz not null default now()
);

create index idx_invoice_lines_invoice on public.invoice_lines (invoice_id);

-- ---------------------------------------------------------------------------
-- payroll_runs — ESTIMATES ONLY. Lifecycle (NomiFlow pattern):
--   draft → calculated → approved → paid(marked externally) / void
-- "paid" means "marked as paid in the external payroll provider".
-- ---------------------------------------------------------------------------
create type public.payroll_run_status as enum (
  'draft', 'calculated', 'approved', 'paid', 'void'
);

create table public.payroll_runs (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  name text not null, -- e.g. '2026-11-30 Biweekly — ESTIMATE'
  period_start date not null,
  period_end date not null,
  status public.payroll_run_status not null default 'draft',
  -- The estimate disclaimer is stored on the row so every export carries it.
  estimate_disclaimer text not null default
    'ESTIMATE ONLY — for payroll preparation. Not a tax calculation, not a payment instruction. Verify with a licensed payroll provider before paying anyone.',
  approved_by uuid references public.app_users(id) on delete set null,
  approved_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint payroll_period check (period_end >= period_start)
);

create index idx_payroll_runs_org on public.payroll_runs (organization_id);
create index idx_payroll_runs_status on public.payroll_runs (organization_id, status);

-- Salary components as data (frappe/hrms pattern): earnings/deductions are
-- configurable component rows, not code branches.
create type public.payroll_component_kind as enum ('earning', 'deduction', 'employer_cost');

create table public.payroll_components (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  name text not null,              -- e.g. 'Regular pay', 'Overtime', '401(k) estimate'
  kind public.payroll_component_kind not null,
  -- 'fixed_amount' | 'per_hour' | 'percent_of_gross_estimate'
  calculation text not null default 'per_hour',
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (organization_id, name)
);

create table public.payroll_run_lines (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  payroll_run_id uuid not null references public.payroll_runs(id) on delete cascade,
  worker_id uuid not null references public.workers(id) on delete restrict,
  assignment_id uuid references public.assignments(id) on delete set null,
  component_id uuid references public.payroll_components(id) on delete set null,
  component_name text not null,
  kind public.payroll_component_kind not null,
  hours numeric(19,4) not null default 0 check (hours >= 0),
  rate numeric(19,4) not null default 0 check (rate >= 0),
  amount_estimate numeric(19,4) not null check (amount_estimate >= 0),
  created_at timestamptz not null default now()
);

create index idx_payroll_lines_run on public.payroll_run_lines (payroll_run_id);
create index idx_payroll_lines_worker on public.payroll_run_lines (worker_id);

-- ---------------------------------------------------------------------------
-- audit_logs are append-only: block UPDATE and DELETE at the database level.
-- ---------------------------------------------------------------------------
create or replace function public.block_audit_mutation()
returns trigger
language plpgsql
as $$
begin
  raise exception 'audit_logs is append-only';
end;
$$;

create trigger trg_audit_no_update
  before update on public.audit_logs
  for each row execute function public.block_audit_mutation();

create trigger trg_audit_no_delete
  before delete on public.audit_logs
  for each row execute function public.block_audit_mutation();

-- ---------------------------------------------------------------------------
-- updated_at maintenance trigger (applied to all mutable tables).
-- ---------------------------------------------------------------------------
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

do $$
declare
  t text;
begin
  for t in select unnest(array[
    'organizations','app_users','organization_members','clients','workers',
    'assignments','timesheets','timesheet_entries','invoices','payroll_runs',
    'payroll_components'
  ]) loop
    execute format(
      'create trigger trg_%s_updated_at before update on public.%I for each row execute function public.set_updated_at()',
      t, t
    );
  end loop;
end $$;
