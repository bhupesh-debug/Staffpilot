/**
 * State machines — payroll lifecycle (NomiFlow pattern) and timesheet
 * approval workflow (sheet-happens pattern). Transitions are enforced in
 * code AND mirrored by CHECK constraints in the SQL migrations; the database
 * is the final authority.
 */

export type TimesheetStatus =
  | "draft"
  | "submitted"
  | "manager_approved"
  | "client_approved"
  | "rejected"
  | "locked";

export const TIMESHEET_TRANSITIONS: Record<TimesheetStatus, TimesheetStatus[]> = {
  draft: ["submitted"],
  submitted: ["manager_approved", "rejected"],
  manager_approved: ["client_approved", "rejected"],
  client_approved: ["locked", "rejected"],
  rejected: ["draft"],
  locked: [],
};

export type PayrollRunStatus =
  | "draft"
  | "calculated"
  | "approved"
  | "paid"
  | "void";

export const PAYROLL_RUN_TRANSITIONS: Record<PayrollRunStatus, PayrollRunStatus[]> = {
  draft: ["calculated", "void"],
  calculated: ["approved", "draft", "void"],
  approved: ["paid", "void"],
  // "paid" here means "marked paid in the external payroll provider" —
  // StaffPilot never moves funds itself. See docs/ARCHITECTURE.md.
  paid: [],
  void: [],
};

export type InvoiceStatus =
  | "draft"
  | "approved"
  | "sent"
  | "partially_paid"
  | "paid"
  | "overdue"
  | "void";

export const INVOICE_TRANSITIONS: Record<InvoiceStatus, InvoiceStatus[]> = {
  draft: ["approved", "void"],
  approved: ["sent", "void"],
  sent: ["partially_paid", "paid", "overdue", "void"],
  partially_paid: ["paid", "overdue", "void"],
  paid: [],
  overdue: ["partially_paid", "paid", "void"],
  void: [],
};

export function canTransition<T extends string>(
  transitions: Record<T, T[]>,
  from: T,
  to: T,
): boolean {
  return (transitions[from] ?? []).includes(to);
}
