import { describe, expect, it } from "vitest";
import {
  INVOICE_TRANSITIONS,
  PAYROLL_RUN_TRANSITIONS,
  TIMESHEET_TRANSITIONS,
  canTransition,
} from "../../src/lib/state-machines";
import { hasPermission } from "../../src/lib/permissions";

describe("timesheet state machine", () => {
  it("allows the happy path draft → submitted → manager_approved → client_approved → locked", () => {
    const path = [
      ["draft", "submitted"],
      ["submitted", "manager_approved"],
      ["manager_approved", "client_approved"],
      ["client_approved", "locked"],
    ] as const;
    for (const [from, to] of path) {
      expect(canTransition(TIMESHEET_TRANSITIONS, from, to)).toBe(true);
    }
  });

  it("forbids skipping steps and editing a locked timesheet", () => {
    expect(canTransition(TIMESHEET_TRANSITIONS, "draft", "client_approved")).toBe(false);
    expect(canTransition(TIMESHEET_TRANSITIONS, "locked", "draft")).toBe(false);
  });

  it("allows a rejected timesheet back to draft", () => {
    expect(canTransition(TIMESHEET_TRANSITIONS, "rejected", "draft")).toBe(true);
  });
});

describe("payroll run state machine", () => {
  it("follows draft → calculated → approved → paid, with void exits", () => {
    expect(canTransition(PAYROLL_RUN_TRANSITIONS, "draft", "calculated")).toBe(true);
    expect(canTransition(PAYROLL_RUN_TRANSITIONS, "calculated", "approved")).toBe(true);
    expect(canTransition(PAYROLL_RUN_TRANSITIONS, "approved", "paid")).toBe(true);
    expect(canTransition(PAYROLL_RUN_TRANSITIONS, "draft", "void")).toBe(true);
    expect(canTransition(PAYROLL_RUN_TRANSITIONS, "paid", "draft")).toBe(false);
  });
});

describe("invoice state machine", () => {
  it("allows draft → approved → sent → paid", () => {
    expect(canTransition(INVOICE_TRANSITIONS, "draft", "approved")).toBe(true);
    expect(canTransition(INVOICE_TRANSITIONS, "approved", "sent")).toBe(true);
    expect(canTransition(INVOICE_TRANSITIONS, "sent", "paid")).toBe(true);
  });
});

describe("role permissions", () => {
  it("workers can submit timesheets but cannot approve payroll", () => {
    expect(hasPermission("worker", "timesheets.submit")).toBe(true);
    expect(hasPermission("worker", "payroll.prepare")).toBe(false);
    expect(hasPermission("worker", "payroll.approve")).toBe(false);
  });

  it("client managers approve timesheets as client, not as manager", () => {
    expect(hasPermission("client_manager", "timesheets.approve_client")).toBe(true);
    expect(hasPermission("client_manager", "timesheets.approve_manager")).toBe(false);
  });

  it("owners hold every permission", () => {
    expect(hasPermission("owner", "org.manage")).toBe(true);
    expect(hasPermission("owner", "audit.read")).toBe(true);
    expect(hasPermission("owner", "payroll.approve")).toBe(true);
  });
});
