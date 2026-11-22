# StaffPilot — Value Proposition (Phase 1)

**Status:** Draft for discovery validation. Nothing here is a proven claim until customers confirm it.
**Date:** November 22, 2026

## 1. Value Proposition Canvas

### Customer jobs (from `02-personas.md`)
- Place and manage 20–100 workers at client sites without losing track of assignments, rates, and margins.
- Collect, approve, and bill timesheets on time every cycle.
- Prepare payroll from approved hours without re-keying or rework.
- Manage C2C vendor consultants alongside direct consultants.
- See utilization and margin clearly enough to run the business.

### Pains
- Spreadsheets that go stale and break under multi-user editing.
- Timesheet chasing and approval delays every cycle.
- Billing and payroll preparation built from different sources that don't reconcile.
- No audit trail when a client disputes hours.
- Generic HR/payroll tools that don't model bill rate vs. pay rate, assignments, or C2C vendors.
- Enterprise staffing systems priced and implemented beyond a small firm's reach [UNVERIFIED].

### Gains wanted
- One approved hour flows to invoice and to payroll-prep estimate — no re-typing.
- Margin visible by client, consultant, and week.
- Audit-ready approval records.
- Onboarding a consultant to billing in days.
- A tool sized and priced for 20–100 workers, not for enterprises.

### Products & services (StaffPilot)
- Worker/consultant records, assignments, bill/pay rates, margin.
- Timesheet workflow: draft → submitted → manager-approved → client-approved, locked after approval.
- Invoicing from approved timesheets.
- Payroll-preparation estimates from approved hours and pay rates (estimates only — see boundary below).
- C2C vendor consultant tracking.
- Margin, utilization, and billing-vs.-payroll-prep reporting.
- Role-based access and tenant isolation.

### Pain relievers
- Single source of truth replaces the spreadsheet stack.
- Approval workflow with reminders replaces chasing by email.
- One approved hour feeds both billing and payroll prep — reconciliation is structural, not manual.
- Every approval and rate change is audit-logged.
- Built for the staffing model (bill vs. pay, assignments, vendors) from day one.

### Gain creators
- Weekly margin visibility without manual reporting.
- Faster invoice cycles → faster cash collection [UNVERIFIED — quantify in discovery].
- Payroll-prep estimates that tie exactly to approved hours.
- A system that grows from 20 to 100 workers without re-platforming.

## 2. Positioning statement

> **For** small staffing companies, consulting firms, and employers managing 20–100 workers in the U.S.,
> **StaffPilot is** the single platform for workforces, projects, and payroll preparation
> **that** connects assignments, timesheets, client approvals, billing, and payroll estimates in one workflow —
> **unlike** generic HR/payroll tools that don't model staffing economics, and enterprise staffing suites built for firms ten times larger,
> **StaffPilot** is sized, priced, and built for the way small staffing firms actually run.

## 3. Differentiation vs. researched competitors

The open-source baseline is documented in `~/workspace/staffpilot/research/payroll-systems-shortlist.md` (verified Nov 22, 2026). The commercial research targets are named in `04-competitor-research-plan.md` — the comparisons below are **hypotheses to verify**, not established facts. No competitor price is asserted here; any price found during research must be marked [VERIFY LIVE].

### vs. open-source payroll/HR systems (PayrollEngine, frappe/hrms, OrangeHRM, IceHrm, Hafta, supabasePayroll, payrun, euron-open-hrms, NomiFlow, sheet-happens)
- **They are components or general HR systems; StaffPilot is a staffing workflow.** None of them models the staffing core: assignment + bill rate + pay rate + margin + C2C vendor tracking as a first-class workflow [UNVERIFIED — verify per-repo during Phase 2 research].
- **They require self-hosting, setup, and maintenance; StaffPilot is hosted SaaS.** A 20–100-worker firm with one ops person does not want to run infrastructure.
- **Their payroll depth varies and none implements U.S. payroll tax correctly** (per the shortlist). StaffPilot does not pretend to either — it is explicitly estimates-only, which is an honest, narrower claim.
- **What we borrow from them:** architecture patterns only (regulation-as-config, payroll lifecycle state machine, RLS tenant isolation, decimal-safe money math, timesheet approval workflow). No GPL/AGPL or no-license code enters the product.

### vs. generic payroll/HR SaaS (research targets: Gusto, Deel, and similar — see `04-competitor-research-plan.md`)
- **Hypothesis:** generic tools are built for direct employers: one company, its employees, its payroll. They do not natively model placing workers at clients, tracking bill vs. pay rates, or managing C2C vendors [UNVERIFIED — verify against live product pages].
- **StaffPilot's edge (if verified):** the assignment and margin model is the product, not an add-on.
- **StaffPilot's honest limit:** it does not process payroll or file taxes. If a prospect needs a full payroll processor, StaffPilot prepares the figures for their processor — it does not replace it. Say so plainly.

### vs. enterprise staffing/VMS platforms (research targets: Bullhorn, Avionté, and similar — see `04-competitor-research-plan.md`)
- **Hypothesis:** enterprise staffing suites serve large agencies with implementation projects, per-seat enterprise pricing, and breadth a 20–100-worker firm will never use [UNVERIFIED — verify].
- **StaffPilot's edge (if verified):** built for small firms — self-serve onboarding, transparent per-worker pricing, no implementation project.
- **StaffPilot's honest limit:** it does not have enterprise breadth (CRM depth, large-scale VMS integrations, global compliance). It is not trying to.

### Differentiation summary table

| Dimension | Generic payroll/HR SaaS | Enterprise staffing/VMS | StaffPilot (proposed) |
|---|---|---|---|
| Built for staffing economics (bill vs. pay, margin) | No (hypothesis) | Yes | Yes — core |
| C2C vendor tracking | No (hypothesis) | Yes | Yes |
| Timesheet → client approval → billing loop | Partial | Yes | Yes — core loop |
| Payroll processing (funds/taxes) | Yes | Sometimes | **No — preparation/estimates only** |
| Sized for 20–100 workers | Often yes | No (hypothesis) | Yes — the target |
| Self-serve onboarding | Often yes | Rarely | Yes |
| Price transparency | Varies | Low | Proposed transparent tiers (see `05-pricing-model.md`) |

## 4. What StaffPilot is NOT (differentiation by exclusion)

- Not a payroll processor. It prepares estimates; it never moves money or files taxes.
- Not a PEO or employer of record. It does not employ anyone's workers.
- Not a recruiting CRM. It tracks placements and assignments, not candidate pipelines.
- Not an enterprise VMS. It does not try to serve 1,000-worker agencies.
- Not a tax advisor or compliance advisor. It does not classify workers and does not advise on classification.

## 5. Proof points needed (before any of this is used publicly)

The value proposition above is a hypothesis. Before it appears on the website (Phase 2) or in sales material, each claim needs evidence:

1. At least 5 discovery interviews confirming the timesheet/billing/payroll-prep pain (see `09-discovery-questions.md`).
2. At least 1 pilot customer completing a full cycle: timesheet → approval → invoice → payroll-prep estimate.
3. Time-saved measurement from the pilot (hours per cycle, before vs. after) — measured, not asserted.
4. Competitor verification per `04-competitor-research-plan.md` before any comparative claim is published.

Until then, all external copy uses the positioning in `06-positioning.md` and marks anything unproven as a goal, not a fact.
