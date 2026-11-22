/**
 * Roles and granular permissions (pattern borrowed from NomiFlow's
 * granular-permission model — see research/payroll-systems-shortlist.md).
 *
 * Permissions are checked in code AND enforced at the database level by
 * PostgreSQL RLS (supabase/migrations/). A role is a named bundle of
 * permissions; never hard-code `role === "owner"` checks at call sites —
 * check the permission instead.
 */

export type Role =
  | "owner"
  | "administrator"
  | "payroll_manager"
  | "recruiter"
  | "client_manager"
  | "worker"
  | "accountant";

export type Permission =
  | "org.manage"
  | "org.invite"
  | "clients.read"
  | "clients.write"
  | "workers.read"
  | "workers.write"
  | "assignments.read"
  | "assignments.write"
  | "timesheets.read"
  | "timesheets.submit"
  | "timesheets.approve_manager"
  | "timesheets.approve_client"
  | "timesheets.lock"
  | "invoices.read"
  | "invoices.write"
  | "payroll.prepare"
  | "payroll.approve"
  | "reports.read"
  | "audit.read";

export const ROLE_PERMISSIONS: Record<Role, Permission[]> = {
  owner: [
    "org.manage",
    "org.invite",
    "clients.read",
    "clients.write",
    "workers.read",
    "workers.write",
    "assignments.read",
    "assignments.write",
    "timesheets.read",
    "timesheets.submit",
    "timesheets.approve_manager",
    "timesheets.approve_client",
    "timesheets.lock",
    "invoices.read",
    "invoices.write",
    "payroll.prepare",
    "payroll.approve",
    "reports.read",
    "audit.read",
  ],
  administrator: [
    "org.invite",
    "clients.read",
    "clients.write",
    "workers.read",
    "workers.write",
    "assignments.read",
    "assignments.write",
    "timesheets.read",
    "timesheets.submit",
    "timesheets.approve_manager",
    "timesheets.lock",
    "invoices.read",
    "invoices.write",
    "payroll.prepare",
    "reports.read",
    "audit.read",
  ],
  payroll_manager: [
    "workers.read",
    "assignments.read",
    "timesheets.read",
    "timesheets.approve_manager",
    "timesheets.lock",
    "invoices.read",
    "payroll.prepare",
    "payroll.approve",
    "reports.read",
  ],
  recruiter: [
    "clients.read",
    "workers.read",
    "workers.write",
    "assignments.read",
    "assignments.write",
    "timesheets.read",
    "reports.read",
  ],
  client_manager: [
    "clients.read",
    "assignments.read",
    "timesheets.read",
    "timesheets.approve_client",
    "invoices.read",
    "reports.read",
  ],
  worker: ["timesheets.read", "timesheets.submit", "assignments.read"],
  accountant: [
    "clients.read",
    "workers.read",
    "assignments.read",
    "timesheets.read",
    "invoices.read",
    "invoices.write",
    "payroll.prepare",
    "reports.read",
    "audit.read",
  ],
};

export function hasPermission(role: Role, permission: Permission): boolean {
  return ROLE_PERMISSIONS[role].includes(permission);
}

export function hasAnyPermission(role: Role, permissions: Permission[]): boolean {
  return permissions.some((p) => hasPermission(role, p));
}
