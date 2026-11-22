-- StaffPilot migration 0005 — Row-Level Security (payrun pattern)
-- Tenant isolation is enforced at the DATABASE level, not just in app code.
-- Every tenant-owned row carries organization_id; every policy requires the
-- caller to be a member of that organization (via public.current_user_id(),
-- which reads the JWT claim set by PostgREST / Supabase Auth).
--
-- Membership helper: true when the current user belongs to the org.
create or replace function public.is_org_member(p_org_id uuid)
returns boolean
language sql
stable
security definer
as $$
  select exists (
    select 1 from public.organization_members m
    where m.organization_id = p_org_id
      and m.user_id = public.current_user_id()
  );
$$;

-- Role helper: true when the current user holds one of the given roles in org.
create or replace function public.has_org_role(p_org_id uuid, p_roles public.org_role[])
returns boolean
language sql
stable
security definer
as $$
  select exists (
    select 1 from public.organization_members m
    where m.organization_id = p_org_id
      and m.user_id = public.current_user_id()
      and m.role = any (p_roles)
  );
$$;

-- Enable RLS on every table that holds tenant or user data.
alter table public.organizations enable row level security;
alter table public.app_users enable row level security;
alter table public.organization_members enable row level security;
alter table public.invitations enable row level security;
alter table public.audit_logs enable row level security;
alter table public.idempotency_keys enable row level security;
alter table public.clients enable row level security;
alter table public.workers enable row level security;
alter table public.assignments enable row level security;
alter table public.timesheets enable row level security;
alter table public.timesheet_entries enable row level security;
alter table public.approvals enable row level security;
alter table public.invoices enable row level security;
alter table public.invoice_lines enable row level security;
alter table public.payroll_runs enable row level security;
alter table public.payroll_run_lines enable row level security;
alter table public.payroll_components enable row level security;

-- ---------------------------------------------------------------------------
-- organizations: members can read their own orgs; only owners create orgs
-- (org creation itself is done via the service role in the signup flow).
-- ---------------------------------------------------------------------------
create policy orgs_select on public.organizations
  for select using (public.is_org_member(id));
create policy orgs_update on public.organizations
  for update using (public.has_org_role(id, array['owner', 'administrator']::public.org_role[]))
  with check (public.has_org_role(id, array['owner', 'administrator']::public.org_role[]));

-- ---------------------------------------------------------------------------
-- app_users: a user reads their own profile; org members can read profiles
-- of users who share an organization with them.
-- ---------------------------------------------------------------------------
create policy users_select_self on public.app_users
  for select using (
    id = public.current_user_id()
    or exists (
      select 1 from public.organization_members m1
      join public.organization_members m2
        on m2.organization_id = m1.organization_id
      where m1.user_id = public.current_user_id()
        and m2.user_id = public.app_users.id
    )
  );
create policy users_update_self on public.app_users
  for update using (id = public.current_user_id())
  with check (id = public.current_user_id());

-- ---------------------------------------------------------------------------
-- organization_members: readable by members of the same org; role changes
-- restricted to owner/administrator.
-- ---------------------------------------------------------------------------
create policy members_select on public.organization_members
  for select using (public.is_org_member(organization_id));
create policy members_insert on public.organization_members
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator']::public.org_role[]));
create policy members_update on public.organization_members
  for update using (public.has_org_role(organization_id, array['owner', 'administrator']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator']::public.org_role[]));
create policy members_delete on public.organization_members
  for delete using (public.has_org_role(organization_id, array['owner']::public.org_role[]));

-- ---------------------------------------------------------------------------
-- invitations: owner/administrator only.
-- ---------------------------------------------------------------------------
create policy invitations_all_admin on public.invitations
  for all using (public.has_org_role(organization_id, array['owner', 'administrator']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator']::public.org_role[]));

-- ---------------------------------------------------------------------------
-- audit_logs: read-only for members with audit access (owner, administrator,
-- accountant, payroll_manager); NO insert/update/delete policy for regular
-- users — audit rows are written by server-side functions with the service
-- role. The append-only triggers in 0004 block mutation even for the owner.
-- ---------------------------------------------------------------------------
create policy audit_select on public.audit_logs
  for select using (
    public.has_org_role(organization_id, array['owner', 'administrator', 'accountant', 'payroll_manager']::public.org_role[])
  );

-- ---------------------------------------------------------------------------
-- idempotency_keys: server-side only. No policies for authenticated users —
-- the API layer reads/writes these with the service role.
-- (Intentionally no policy: with RLS enabled and no policy, access is denied.)

-- ---------------------------------------------------------------------------
-- Generic tenant tables: members of the org can read; writes restricted by
-- role. This block is generated per table below (explicit, not dynamic, so
-- the policy set is reviewable in one file).
-- ---------------------------------------------------------------------------

-- clients: read all members; write owner/administrator/recruiter/client_manager
create policy clients_select on public.clients
  for select using (public.is_org_member(organization_id));
create policy clients_write on public.clients
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'recruiter', 'client_manager']::public.org_role[]));
create policy clients_update on public.clients
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'recruiter', 'client_manager']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'recruiter', 'client_manager']::public.org_role[]));
create policy clients_delete on public.clients
  for delete using (public.has_org_role(organization_id, array['owner', 'administrator']::public.org_role[]));

-- workers: read all members; write owner/administrator/recruiter
create policy workers_select on public.workers
  for select using (public.is_org_member(organization_id));
create policy workers_write on public.workers
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'recruiter']::public.org_role[]));
create policy workers_update on public.workers
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'recruiter']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'recruiter']::public.org_role[]));
create policy workers_delete on public.workers
  for delete using (public.has_org_role(organization_id, array['owner', 'administrator']::public.org_role[]));

-- assignments: read all members; write owner/administrator/recruiter
create policy assignments_select on public.assignments
  for select using (public.is_org_member(organization_id));
create policy assignments_write on public.assignments
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'recruiter']::public.org_role[]));
create policy assignments_update on public.assignments
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'recruiter']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'recruiter']::public.org_role[]));
create policy assignments_delete on public.assignments
  for delete using (public.has_org_role(organization_id, array['owner', 'administrator']::public.org_role[]));

-- timesheets: read all members; workers submit their own (insert as worker
-- role); approvals restricted to manager/client roles in app logic + here.
create policy timesheets_select on public.timesheets
  for select using (public.is_org_member(organization_id));
create policy timesheets_insert on public.timesheets
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'recruiter', 'worker']::public.org_role[]));
create policy timesheets_update on public.timesheets
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'client_manager', 'worker']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'client_manager', 'worker']::public.org_role[]));

-- timesheet_entries: same membership rule as their parent timesheet.
create policy timesheet_entries_select on public.timesheet_entries
  for select using (public.is_org_member(organization_id));
create policy timesheet_entries_write on public.timesheet_entries
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'worker']::public.org_role[]));
create policy timesheet_entries_update on public.timesheet_entries
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'worker']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'worker']::public.org_role[]));
create policy timesheet_entries_delete on public.timesheet_entries
  for delete using (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]));

-- approvals: read all members; insert restricted to manager/client approvers.
create policy approvals_select on public.approvals
  for select using (public.is_org_member(organization_id));
create policy approvals_insert on public.approvals
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'client_manager']::public.org_role[]));

-- invoices: read all members; write owner/administrator/accountant.
create policy invoices_select on public.invoices
  for select using (public.is_org_member(organization_id));
create policy invoices_write on public.invoices
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'accountant']::public.org_role[]));
create policy invoices_update on public.invoices
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'accountant']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'accountant']::public.org_role[]));
create policy invoices_delete on public.invoices
  for delete using (public.has_org_role(organization_id, array['owner', 'administrator']::public.org_role[]));

-- invoice_lines: follow the invoice's org.
create policy invoice_lines_select on public.invoice_lines
  for select using (public.is_org_member(organization_id));
create policy invoice_lines_write on public.invoice_lines
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'accountant']::public.org_role[]));
create policy invoice_lines_update on public.invoice_lines
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'accountant']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'accountant']::public.org_role[]));

-- payroll_runs / lines / components: payroll_manager, owner, administrator,
-- accountant. Workers and client managers cannot see payroll estimates.
create policy payroll_runs_select on public.payroll_runs
  for select using (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'accountant']::public.org_role[]));
create policy payroll_runs_write on public.payroll_runs
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]));
create policy payroll_runs_update on public.payroll_runs
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]));

create policy payroll_lines_select on public.payroll_run_lines
  for select using (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'accountant']::public.org_role[]));
create policy payroll_lines_write on public.payroll_run_lines
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]));
create policy payroll_lines_update on public.payroll_run_lines
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]));

create policy payroll_components_select on public.payroll_components
  for select using (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager', 'accountant']::public.org_role[]));
create policy payroll_components_write on public.payroll_components
  for insert with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]));
create policy payroll_components_update on public.payroll_components
  for update using (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]))
  with check (public.has_org_role(organization_id, array['owner', 'administrator', 'payroll_manager']::public.org_role[]));
