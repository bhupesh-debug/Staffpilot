# StaffPilot — Customer Onboarding Workflow (Phase 1)

**Status:** Working checklist. Revise after each of the first 5 onboardings.
**Date:** November 22, 2026
**Goal:** Take a new customer from signup to their first completed payroll-preparation run — one full cycle of timesheet → approval → billing → payroll-prep estimate — within 14 days (trial) or 30 days (guided pilot).

## 1. Principles

- **Founder-led for the first 10 customers.** No self-serve-only onboarding until the checklist has survived 10 real onboardings.
- **Start small, then expand.** One client, one pay cycle, a handful of workers — prove the loop, then roll out to the rest of the firm.
- **Import, don't re-key.** Take the customer's spreadsheet and import it for them. Re-keying is the #1 onboarding killer [UNVERIFIED — validate in the first onboardings].
- **The boundary, stated twice.** At signup and at the first payroll-prep run, confirm in writing that StaffPilot prepares estimates only and never moves funds or files taxes.
- **Time-to-value is the metric.** Days from signup to first completed loop. If it exceeds 14 days for a trial customer, diagnose why before onboarding the next one.

## 2. Phase A — Signup (Day 0)

- [ ] Customer signs up (14-day trial, no credit card; or guided pilot agreement).
- [ ] Tenant created; admin user set up; role-based access explained (owner/admin, recruiter, payroll manager, client approver).
- [ ] Welcome email sent: what StaffPilot is, what it is not (payroll preparation, estimates only), links to the onboarding checklist, and the founder's direct contact.
- [ ] **Boundary confirmation:** customer acknowledges in the signup flow that StaffPilot does not process payroll, move funds, file taxes, or store SSNs/bank details.
- [ ] Kickoff call booked (30 min, within 2 business days).

## 3. Phase B — Kickoff call (Day 1–2)

- [ ] Confirm the customer's goal for the trial/pilot: which pain are they solving first (timesheets, billing, margin, payroll prep)?
- [ ] Agree the pilot scope: **one client, one pay cycle, 5–10 workers** to start.
- [ ] Identify the people: who enters timesheets, who approves (manager), who approves at the client, who runs billing, who runs payroll prep.
- [ ] Collect the customer's current data: worker list, assignment list (bill/pay rates), client list, current timesheet format. Accept a spreadsheet — do not ask them to re-key.
- [ ] Agree the success criterion for the pilot in their words (e.g., "invoice X goes out on time with no rework" or "payroll prep takes under an hour").
- [ ] Set the date of the first payroll-prep run.

## 4. Phase C — Data setup (Day 2–5)

- [ ] Import workers, clients, and assignments from the customer's spreadsheet. Verify counts with the customer (e.g., "10 workers, 1 client, 10 assignments — does that match?").
- [ ] Enter bill rates and pay rates; show the customer the margin per assignment and ask them to confirm it.
- [ ] Set up user accounts and roles for everyone identified in Phase B.
- [ ] Configure the pay cycle (weekly/biweekly, cycle dates, approval deadlines).
- [ ] Walk the payroll manager through the payroll-preparation estimate screen: what each figure is, why it is labeled an estimate, and how it will be handed to their processor.
- [ ] Confirm: no SSNs or bank details requested or entered. If the customer tries to enter them, stop them and explain why.

## 5. Phase D — First timesheet cycle (Day 5–12)

- [ ] Workers submit their first timesheets in StaffPilot (or the founder enters the first batch with them on a call).
- [ ] Manager approves; client approves (or the customer confirms the client-approval step with a real approver).
- [ ] Founder checks in mid-cycle: any stuck timesheets? Any confusion? Fix within 24 hours.
- [ ] Generate the first invoice from approved timesheets. Customer reviews it against their old method before it goes out.
- [ ] Run the first payroll-preparation estimate. Customer reviews every line against approved hours and rates; founder walks through the estimate labels and the handoff to their processor.
- [ ] Record the time taken: timesheet collection, approval, invoicing, payroll prep — before (their old process, self-reported) vs. after (measured in StaffPilot).

## 6. Phase E — Review and convert (Day 12–14 trial / Day 25–30 pilot)

- [ ] Review call (30 min): did the loop complete? Was the success criterion from Phase B met? What broke, and what was fixed?
- [ ] Present the measured result: hours saved per cycle, loop completed on time (yes/no), invoice accuracy (per the customer).
- [ ] Present the proposed tier (Starter/Growth/Scale per `05-pricing-model.md`) and the price for their actual worker count.
- [ ] If converting: collect payment details, confirm the tier, confirm the billing start date, and confirm the next cycle date.
- [ ] If not converting: ask why, in writing; offer data export; leave the door open. Log the reason — it is product feedback, not a failure to hide.
- [ ] Ask for one referral introduction and (with explicit permission) a short written quote about the result.

## 7. Phase F — Steady state (first 30 days as a paying customer)

- [ ] Second cycle runs without founder hand-holding (founder available, not driving).
- [ ] Expand scope: add the next client and the next batch of workers.
- [ ] Enable the features of their tier (e.g., C2C vendor tracking on Growth; API on Scale).
- [ ] Schedule a 30-day check-in: is the loop running weekly? Any churn signals (missed cycles, silence, complaints)? Act on any signal within 48 hours.
- [ ] Update the onboarding checklist with anything learned from this customer.

## 8. Onboarding tracker (per customer)

| Field | Value |
|---|---|
| Firm / contact / persona | |
| Signup date / trial-or-pilot | |
| Pilot scope (client, cycle, workers) | |
| Success criterion (their words) | |
| Data imported (counts verified?) | |
| First loop completed (date) | |
| Hours saved per cycle (before vs. after) | |
| Tier proposed / tier taken | |
| Converted? (date or reason not) | |
| Referral given? | |
| Churn signals? | |

## 9. Escalations and hard stops

- **Customer asks StaffPilot to move payroll funds, make a deposit, or file taxes:** decline clearly, restate the preparation-only boundary, offer the estimate handoff to their processor. Log it.
- **Customer tries to enter SSNs or bank details:** stop them, explain the product does not store them, and remove any that were entered.
- **Customer asks for worker classification advice or auto-classification:** decline to advise; classification is their legal determination with their own counsel.
- **Customer asks for a feature that violates a boundary:** decline, explain why, log the request for the product roadmap discussion.
- **Onboarding stalls (no data in 7 days):** personal call, not email. Offer to do the import on a screenshare. If still stalled after 14 days, pause the trial clock and ask what would unblock it — don't let a dead trial count as a conversion failure.
