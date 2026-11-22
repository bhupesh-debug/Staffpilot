# StaffPilot — Revenue Assumptions (Phase 1)

**Status:** ASSUMPTIONS ONLY. Every number in this document is an assumption to validate in discovery. There are no revenue guarantees, no market facts, and no forecasts presented as predictions.
**Date:** November 22, 2026

## 1. How to read this document

- **ASSUMPTION** = a number we are choosing in order to plan, which discovery and early sales must confirm or correct.
- If an assumption proves wrong, the model is revised — the model does not revise reality.
- All prices are the proposed tiers from `05-pricing-model.md` (themselves proposals to validate).
- "Worker" = an active worker on assignment in the billing month (see `05-pricing-model.md`).

## 2. Bottom-up assumptions table

| # | Assumption | Value | Basis / note |
|---|---|---|---|
| A1 | Target firm size (workers) | 20–100 | Segment definition (see `01-business-overview.md`) |
| A2 | Average workers per paying customer | **45** (ASSUMPTION) | Midpoint-ish of the segment, weighted toward the smaller end where first customers are likeliest. Validate: first 10 customers' actual headcount. |
| A3 | Tier mix among paying customers | Starter 30% / Growth 50% / Scale 20% (ASSUMPTION) | Growth is the expected most-popular tier [UNVERIFIED]. Validate from actual signups. |
| A4 | Average revenue per customer per month (blended) | **~$365/mo** (ASSUMPTION, derived) | See calculation in §3. Not a price — a derived average from A2 + A3 + tier prices. |
| A5 | Paying customers at end of Month 3 (first 90 days) | **10** (ASSUMPTION — target) | The 90-day goal (see `08-90-day-launch-strategy.md`). A target, not a forecast. |
| A6 | Paying customers at end of Month 6 | **25** (ASSUMPTION — target) | Requires the Month 1–3 motion to keep working plus referrals. Validate after Month 3. |
| A7 | Paying customers at end of Month 12 | **60** (ASSUMPTION — target) | Requires repeatable acquisition; do not treat as a commitment. |
| A8 | Monthly logo churn (customers cancelling) | **3%/mo** (ASSUMPTION) | A planning placeholder. [UNVERIFIED — no data until customers exist.] Small-firm SaaS churn is often higher; if actual churn exceeds this, the model breaks and must be revised. |
| A9 | Months from launch to first paying customer | **1 month** (ASSUMPTION — target) | First revenue inside the first 30 days of the 90-day plan, from a pilot conversion. |
| A10 | Months from launch to first revenue month (MRR > $0) | **Month 1** (ASSUMPTION — target) | Same as A9. |
| A11 | Trial-to-paid conversion rate | **20%** (ASSUMPTION) | Planning placeholder for the 14-day trial. [UNVERIFIED — measure from the first 20 trials.] |
| A12 | Sales cycle (first contact → paying) | **2–4 weeks** (ASSUMPTION) | Small-firm, low-price sale. Validate from the first 10 deals. |
| A13 | Founder time available for sales | **~10 hrs/week** (ASSUMPTION) | Budget is $0–$100 cash; the constraint is time. If less time is available, A5–A7 must come down. |
| A14 | Annual-billing share | **25% of customers** (ASSUMPTION) | Affects cash timing (2 months free), not MRR. Validate from signups. |

## 3. Derived monthly recurring revenue (MRR) — arithmetic only

Tier price at the assumed average of 45 workers (from `05-pricing-model.md`):

| Tier | Price at 45 workers | Share (A3) | Contribution |
|---|---|---|---|
| Starter: $49 + $4×45 | $229/mo | 30% | $68.70 |
| Growth: $99 + $6×45 | $369/mo | 50% | $184.50 |
| Scale: $199 + $8×45 | $559/mo | 20% | $111.80 |
| **Blended ARPU** | | | **~$365/mo** |

Derived MRR at each customer milestone (before churn, for illustration):

| Milestone | Customers | Blended MRR (ASSUMPTION) |
|---|---|---|
| End of Month 3 | 10 | ~$3,650/mo |
| End of Month 6 | 25 | ~$9,125/mo |
| End of Month 12 | 60 | ~$21,900/mo |

**Read these as:** "IF the tier prices hold, IF the average customer has 45 workers, IF the tier mix is 30/50/20, and IF churn is ignored, THEN the arithmetic gives these figures." Every IF is unvalidated. These are planning illustrations, not projections to quote to anyone.

## 4. Sensitivity — what breaks the model

| Change | Effect on Month-12 illustration | What to do |
|---|---|---|
| Average workers per customer is 30, not 45 | Blended ARPU falls to ~$265/mo; Month-12 MRR ~$15,900 | Re-examine whether the segment's real average is lower; pricing may need a higher per-worker rate or lower base |
| Tier mix skews Starter (60/30/10) | Blended ARPU ~$299/mo | Find out why Growth isn't landing — feature gap or price gap? |
| Churn is 6%/mo, not 3% | Roughly doubles the new customers needed to hold any milestone | Fix onboarding and time-to-value before spending more on acquisition |
| Trial-to-paid is 10%, not 20% | Twice as many trials needed per paying customer | Fix trial onboarding; check whether the trial shows the core loop fast enough |
| Sales cycle is 6–8 weeks, not 2–4 | Month-3 target of 10 slips by a month or more | Start outreach earlier; shorten the pilot path |
| Only 5 hrs/week of founder sales time | Outreach volume halves; Month-3 target likely missed | Cut the target or find a referral channel that scales without founder hours |

## 5. Costs (Phase 1, $0–$100 cash budget)

| Cost | Assumption |
|---|---|
| Hosting / tooling | Free tiers where available; stay inside the $0–$100 envelope |
| Founder time | The real cost; ~10 hrs/week assumed (A13) |
| Paid ads | $0 in Phase 1 — outreach is direct (email/LinkedIn) and referral-based |
| Compliance/legal | $0 budgeted; the three-way separation (see `01-business-overview.md`) is a positioning and product decision, not a purchased opinion. If a real legal question arises (e.g., a customer asks StaffPilot to handle something at the boundary), pause and get advice before acting — do not improvise. |

## 6. What would invalidate this model

- Discovery shows target firms won't pay per-worker pricing at all (then the model is rebuilt around flat pricing or another structure).
- Discovery shows the real willingness-to-pay is far below $229–$559/mo for a 45-worker firm (then tiers move or the segment moves).
- The payroll-preparation wedge is wrong — firms want full payroll processing, not preparation (then the product scope, not just the model, must be re-thought; do not drift into processing without a separate decision).
- Churn in the first 10 customers exceeds ~5%/mo (then fix retention before growth).

## 7. Review cadence

Revisit this document at the end of each month during the first 90 days, and revise every assumption with actuals: real headcount per customer, real tier mix, real churn, real trial conversion, real sales-cycle length. The revised document is the record — never silently keep stale assumptions.
