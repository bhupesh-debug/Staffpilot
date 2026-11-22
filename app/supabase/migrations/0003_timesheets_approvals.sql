-- StaffPilot migration 0003 — timesheets, entries, approvals
-- State machine (sheet-happens pattern):
--   draft → submitted → manager_approved → client_approved → locked
--   submitted/manager_approved/client_approved → rejected → draft
-- Locked timesheets are immutable: entries cannot change after lock
-- (enforced by trigger below). Every transition is audit-logged.

create type public.timesheet_status as enum (
  'draft', 'submitted', 'manager_approved', 'client_approved', 'rejected', 'locked'
);

create table public.timesheets (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  assignment_id uuid not null references public.assignments(id) on delete restrict,
  worker_id uuid not null references public.workers(id) on delete restrict,
  week_start_date date not null,
  status public.timesheet_status not null default 'draft',
  submitted_at timestamptz,
  manager_approved_at timestamptz,
  manager_approved_by uuid references public.app_users(id) on delete set null,
  client_approved_at timestamptz,
  client_approved_by uuid references public.app_users(id) on delete set null,
  rejection_reason text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (assignment_id, week_start_date)
);

create index idx_timesheets_org on public.timesheets (organization_id);
create index idx_timesheets_worker on public.timesheets (worker_id);
create index idx_timesheets_status on public.timesheets (organization_id, status);

create table public.timesheet_entries (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  timesheet_id uuid not null references public.timesheets(id) on delete cascade,
  work_date date not null,
  hours numeric(19,4) not null check (hours >= 0 and hours <= 24),
  description text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (timesheet_id, work_date)
);

create index idx_timesheet_entries_timesheet on public.timesheet_entries (timesheet_id);

-- A locked timesheet's entries cannot be inserted, updated, or deleted.
create or replace function public.prevent_locked_timesheet_change()
returns trigger
language plpgsql
as $$
declare
  ts_status public.timesheet_status;
begin
  select status into ts_status from public.timesheets
  where id = coalesce(new.timesheet_id, old.timesheet_id);
  if ts_status = 'locked' then
    raise exception 'timesheet % is locked and cannot be modified', coalesce(new.timesheet_id, old.timesheet_id);
  end if;
  return coalesce(new, old);
end;
$$;

create trigger trg_timesheet_entries_locked
  before insert or update or delete on public.timesheet_entries
  for each row execute function public.prevent_locked_timesheet_change();

-- ---------------------------------------------------------------------------
-- approvals — one row per approval decision (manager + client), so the
-- approval history is queryable independently of the timesheet row.
-- ---------------------------------------------------------------------------
create table public.approvals (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  timesheet_id uuid not null references public.timesheets(id) on delete cascade,
  approver_user_id uuid not null references public.app_users(id) on delete restrict,
  approver_role text not null check (approver_role in ('manager', 'client')),
  decision text not null check (decision in ('approved', 'rejected')),
  note text,
  created_at timestamptz not null default now()
);

create index idx_approvals_timesheet on public.approvals (timesheet_id);
