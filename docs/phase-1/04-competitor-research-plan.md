# StaffPilot — Competitor Research Plan (Phase 1)

**Status:** Research plan — not research results. No competitor fact below is asserted; each is a question to answer.
**Date:** November 22, 2026

## 1. Purpose

Produce a verified, honest picture of the competitive landscape so that StaffPilot's positioning (see `03-value-proposition.md` and `06-positioning.md`) rests on checked facts, not assumptions — and so the website (Phase 2) never publishes a comparative claim that can't be defended.

## 2. Baseline: the open-source shortlist (already verified)

Start from `~/workspace/staffpilot/research/payroll-systems-shortlist.md` (verified live via GitHub, Nov 22, 2026). Do not redo it; build on it.

| System | License | Role for StaffPilot |
|---|---|---|
| PayrollEngine (MIT) | MIT | Regulation-as-config pattern; pure testable payroll engine |
| frappe/hrms (GPL-3.0) | GPL-3.0 | Data-model ideas only — salary components as data. **No code reuse.** |
| NomiFlow (no license) | All rights reserved | Closest functional twin; payroll lifecycle state machine; permission model. **Study only.** |
| euron-open-hrms (MIT) | MIT | Multi-tenant TypeScript reference |
| Hafta (MIT) | MIT | Simple master-data pattern; advance/limit model |
| OrangeHRM (GPL) | GPL | Module boundaries. **No code reuse.** |
| IceHrm (GPL) | GPL | Lightweight employee-record model. **No code reuse.** |
| supabasePayroll (MIT) | MIT | Normalized Supabase payroll schema sketch |
| payrun (MIT) | MIT | PostgreSQL RLS multi-tenant pattern |
| sheet-happens (AGPL) | AGPL | Timesheet approval workflow. **No code reuse.** |

**Rules carried forward from the shortlist:**
- GPL/AGPL code must not enter a proprietary SaaS codebase.
- No-license repos are all-rights-reserved: study patterns only, never copy code.
- None of these repos implements U.S. federal/state payroll tax correctly. StaffPilot's payroll module stays estimates-only; real tax calculation comes only from a validated provider integration in a later phase.
- No mature open-source staffing/VMS exists in the survey — StaffPilot's assignment/bill-rate/pay-rate/margin model is original work.

**Re-check cadence:** star counts, licenses, and last-updated dates move. Re-verify any figure before citing it externally.

## 3. Commercial research targets

The following are named as **research targets only**. Nothing is claimed about their features, pricing, or positioning until verified against a live source.

### Tier A — generic payroll/HR SaaS (the "doesn't fit staffing" hypothesis)
- **Gusto** — Verify: does it model bill rate vs. pay rate, client assignments, or C2C vendors? What is its payroll scope (processing vs. preparation)? Pricing page structure and what is/isn't public. Target customer size.
- **Deel** — Verify: contractor/EOR positioning; does it serve domestic U.S. staffing agencies placing workers at clients, or is its core cross-border employment? What does it charge for, and what is public vs. sales-gated?
- **Rippling** (add if time permits) — Verify: breadth vs. depth; whether staffing assignment economics appear anywhere in its model.
- **ADP / Paychex** (add if time permits) — Verify: small-business payroll positioning; whether they offer any staffing-assignment workflow; pricing transparency.

### Tier B — staffing / VMS platforms (the "too big / too expensive" hypothesis)
- **Bullhorn** — Verify: target customer size; whether it covers timesheet → approval → billing → payroll prep in one flow or needs add-ons; pricing transparency (public vs. sales-gated); implementation/onboarding model.
- **Avionté** — Verify: same questions as Bullhorn; front-office vs. back-office coverage; target firm size.
- **CEIPAL / AkkenCloud** (add if time permits) — Verify: small-agency positioning, if any; pricing transparency.

### Tier C — adjacent / niche
- **Time-tracking & timesheet tools** (e.g., generic timesheet SaaS) — Verify: do they cover client approval and billing, or stop at time capture?
- **Accounting tools used as workarounds** (e.g., QuickBooks-class tools) — Verify: how target firms currently jury-rig billing/payroll-prep in them; this is the real incumbent for many small firms [UNVERIFIED — confirm in discovery].
- **Spreadsheets + email** — the true default incumbent. Research = discovery interviews, not web pages. How firms actually run the workflow today is the most important competitive fact.

## 4. What to verify about each competitor

For every commercial target, record the following in a research log (one entry per competitor, with source URL and date checked):

1. **Target customer:** who is it built for (firm size, industry, direct employer vs. staffing agency)?
2. **Staffing-model fit:** bill rate vs. pay rate; client assignments; margin reporting; C2C vendor tracking — present, partial, or absent?
3. **Timesheet loop:** entry → manager approval → client approval → billing — how much of the loop is native?
4. **Payroll scope:** full processing (funds, deposits, tax filing) vs. preparation/estimates vs. neither? State exactly what the source says.
5. **Pricing:** what is public? If a price is named, record it with **[VERIFY LIVE]** and the date/URL — never assert a competitor price from memory. If pricing is sales-gated, record that fact ("pricing not public as of [date]").
6. **Onboarding:** self-serve signup, demo-gated, or implementation project?
7. **Positioning language:** tagline and homepage claims, quoted briefly with source.
8. **Gaps for small staffing firms:** what would a 20–100-worker agency find missing, overbuilt, or overpriced?
9. **What StaffPilot can learn:** one pattern worth borrowing (as a pattern, not code) and one mistake to avoid.

## 5. Method

1. **Primary sources only for facts.** Competitor homepages, pricing pages, product docs, and help centers. No third-party "review" roundups as a source for feature or price claims.
2. **Screenshot / archive key pages.** Save the pricing and core product pages with the check date; pricing changes without notice.
3. **Free trial / demo where free.** Use a trial to verify the staffing-model questions firsthand where a free tier or trial exists. Never misrepresent identity to obtain a demo.
4. **Discovery interviews as the real competitive research.** The incumbent is usually spreadsheets + email + a generic tool. Interview questions in `09-discovery-questions.md` cover current-tool usage; answers there outrank web research.
5. **No fake accounts, no scraped pricing databases, no "mystery shopping" with false pretenses.** If a price is gated behind a sales call, record it as gated.
6. **Mark everything.** Every competitor fact gets a source URL + date, or the mark [UNVERIFIED]. Every price gets [VERIFY LIVE].

## 6. Deliverable

A competitor research log (one file, e.g., `~/workspace/staffpilot/research/competitor-log.md`) with one section per competitor covering the 9 verification points above, plus a one-page summary:

- Where StaffPilot's differentiation holds after verification.
- Where it doesn't (claims to drop or soften).
- The three strongest verified differentiators to carry into Phase 2 website copy.
- The three closest competitors to watch, and why.

**Deadline:** Complete Tier A + Tier B before Phase 2 website copy is finalized. Tier C can trail but must be done before any public comparative claim.

## 7. What this plan does NOT authorize

- Copying competitor copy, screenshots, or branding into StaffPilot materials.
- Reusing any GPL/AGPL or no-license open-source code.
- Publishing a competitor price without a live check on the check date.
- Claiming a competitor "can't do X" on the basis of not finding X on their homepage — absence from a marketing page is not proof of absence from the product. Phrase findings as "not found on [page] as of [date]" unless a trial or documentation confirms it.
