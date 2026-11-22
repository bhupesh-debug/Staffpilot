# StaffPilot — Pricing Model (Phase 1)

**Status:** PROPOSED prices to validate in discovery. These are not market facts, not competitor prices, and not final. Every number below is a proposal that discovery interviews must confirm, correct, or reject before Phase 2.
**Date:** November 22, 2026

## 1. Pricing principles

1. **Transparent and self-serve.** Prices are published on the website. A 20–100-worker firm should be able to price itself in under a minute.
2. **Per-worker pricing that matches the business model.** Staffing firms think in headcount; charging per worker per month aligns StaffPilot's price with the customer's scale.
3. **A base fee so small firms aren't free-riding on infrastructure.** The base covers the platform, tenant, and support; the per-worker charge scales with usage.
4. **No hidden payroll-processing fees.** StaffPilot does not process payroll, so there is no per-payroll-run or per-payment fee. Say so on the pricing page.
5. **Annual discount that rewards commitment without locking small firms in.** 2 months free on annual billing (~17% discount) is simple and standard.
6. **Prices must survive the discovery question:** "What do you pay today for this workflow, in software plus staff time?" If the answer is consistently far below these tiers, the tiers move down. If firms pay more in staff time alone, the tiers hold.

## 2. Proposed tiers

All prices in USD. "Worker" = any active consultant/employee record on an assignment (or with an active assignment) in the billing month. Inactive/archived workers don't count.

| | **Starter** | **Growth** | **Scale** |
|---|---|---|---|
| **Proposed price** | **$49/mo base + $4 per worker/mo** | **$99/mo base + $6 per worker/mo** | **$199/mo base + $8 per worker/mo** |
| **Example: 25 workers** | $149/mo | $249/mo | $399/mo |
| **Example: 50 workers** | $249/mo | $399/mo | $599/mo |
| **Example: 100 workers** | $449/mo | $699/mo | $999/mo |
| **Annual (2 months free)** | ~17% off the above | ~17% off the above | ~17% off the above |
| **Workers included in base** | Up to 25 | Up to 50 | Up to 100 |
| **Target firm** | 20–30 workers, first system | 30–75 workers, growing | 75–100+ workers, multi-client |

*Worker-count note:* the "workers included" band is a soft guide, not a hard cap — a Starter customer with 28 workers pays the per-worker rate for workers above 25 rather than being forced to upgrade. Forced upgrades are a churn trigger; the tier difference is features, not headcount walls.

### Starter — $49/mo + $4/worker/mo
**For:** a small agency replacing spreadsheets with its first real system.
- Core worker records and assignments (bill rate, pay rate, margin)
- Timesheets: entry, submit, manager approval
- Client approval of timesheets
- Invoicing from approved timesheets
- Payroll-preparation estimates (labeled estimates)
- Basic margin reporting (by client, by consultant)
- 2 user seats included; additional seats $10/mo each [PROPOSED]
- Email support

**Excludes:** C2C vendor management module; advanced reporting; API access; priority support; custom roles/permissions beyond the defaults.

### Growth — $99/mo + $6/worker/mo
**For:** a growing firm that needs vendor tracking and better reporting. *Expected to be the most popular tier [UNVERIFIED — validate in discovery].*
- Everything in Starter, plus:
- C2C vendor consultant tracking (vendor records, vendor rates, vendor invoices)
- Advanced reporting: utilization, margin trends, billing vs. payroll-prep reconciliation
- 5 user seats included; additional seats $10/mo each [PROPOSED]
- Custom roles and permissions
- Data export (CSV/Excel) for billing and payroll-prep runs
- Priority email support (next-business-day target)

**Excludes:** API access; dedicated onboarding; SLA.

### Scale — $199/mo + $8/worker/mo
**For:** firms at the top of the segment running multi-client, multi-vendor operations.
- Everything in Growth, plus:
- API access (read/write, API keys, rate limits — see the NomiFlow-inspired discipline in the shortlist)
- 10 user seats included; additional seats $10/mo each [PROPOSED]
- Dedicated onboarding session (1:1, remote)
- Quarterly business review (margin/utilization walkthrough)
- Priority support with a same-business-day target
- Early access to new modules as they ship

**Excludes:** anything involving real payroll funds, tax filing, or tax deposits — no tier includes those, ever. Custom development is not offered in Phase 1.

## 3. Justification for the numbers

- **The per-worker band ($4–$8) is deliberately low.** The target customer's margin is earned per placed worker per week; a tool that costs a small fraction of one worker's weekly margin is an easy yes if it saves hours. The exact band is a guess to validate — discovery must ask what firms currently spend on this workflow (software + staff time) and what they'd pay to fix it.
- **The base fee ($49–$199) keeps tiny accounts viable.** Without it, a 20-worker Starter account at $4/worker would be $80/mo with no floor — thin for support and hosting. The base also signals "real product," which matters against free spreadsheets.
- **The step between tiers is features, not headcount.** Firms upgrade because they need vendor tracking or the API — not because they hired worker #26. That reduces upgrade resentment.
- **$999/mo at 100 workers on Scale is the ceiling for Phase 1.** Above that, the customer is arguably out of segment; revisit pricing if larger firms start asking [UNVERIFIED — to observe].
- **No free tier.** A free tier for a product handling billing and payroll-prep data invites misuse and support load with no revenue. A time-limited trial (below) is the try-before-you-buy route instead.

## 4. Free trial terms

- **14-day free trial, no credit card required.** Full Growth-tier features during the trial (so prospects evaluate the real product, including vendor tracking).
- **Trial data is the customer's real data.** The trial is designed to end with the customer already running a live payroll-prep cycle — switching costs then favor staying.
- **Trial limits:** one tenant, up to 100 workers, no API access during trial.
- **At trial end:** downgrade to Starter, upgrade to Growth/Scale, or export data and leave. No dark patterns, no auto-charge (no card was taken).
- **Pilot exception:** for the first 10 customers (see `08-90-day-launch-strategy.md`), a 30-day guided pilot with founder-led onboarding may be offered instead of the standard 14-day trial, in exchange for a feedback interview.

## 5. What is NOT charged for

- Payroll-preparation runs: unlimited, all tiers. Charging per run would punish the core loop.
- Timesheet submissions and approvals: unlimited.
- Invoices generated: unlimited.
- Data export on Growth/Scale: unlimited.

## 6. What each tier explicitly excludes (all tiers)

- Real payroll processing: no funds movement, no direct deposits, no tax filing, no tax deposits.
- Storage of real SSNs or bank account details.
- Worker classification advice or auto-classification.
- Any certification claim.
- Custom development and integrations beyond the Scale API.

## 7. Validation checklist (before Phase 2)

- [ ] Ask 10+ target firms what they pay today for this workflow (software + staff hours).
- [ ] Ask what they'd pay for a tool that does the timesheet → approval → billing → payroll-prep loop.
- [ ] Test price sensitivity: present the tiers and ask which they'd pick and why — and what would make them pick the tier above.
- [ ] Check whether per-worker pricing confuses firms whose headcount fluctuates monthly (assignment-based billing may need a "peak workers in month" rule — decide from interviews).
- [ ] Re-verify that no competitor price is quoted anywhere in StaffPilot materials without a [VERIFY LIVE] check (see `04-competitor-research-plan.md`).
- [ ] If discovery says the band is wrong, revise this document and re-check consistency in `01-business-overview.md`, `03-value-proposition.md`, and `06-positioning.md` before Phase 2 copy is written.
