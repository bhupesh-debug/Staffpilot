#!/usr/bin/env python3
"""Build the StaffPilot static public website.

Generates 16 HTML pages under this directory from one shared template,
so header, footer and navigation are identical on every page.
No build step is needed to view the site; re-run this script after
editing page content:  python3 build.py
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent

NAV = [
    ("index.html", "Home"),
    ("features.html", "Features"),
    ("pricing.html", "Pricing"),
    ("blog.html", "Blog"),
    ("faq.html", "FAQ"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

FOOTER_COLS = [
    ("Product", [
        ("features.html", "Features"),
        ("pricing.html", "Pricing"),
        ("workforce-management.html", "Workforce management"),
        ("payroll-preparation.html", "Payroll preparation"),
        ("security.html", "Security information"),
    ]),
    ("Solutions", [
        ("staffing-firms.html", "Staffing firms"),
        ("c2c-consulting.html", "C2C consulting"),
        ("workforce-management.html", "Workforce management"),
        ("payroll-preparation.html", "Payroll preparation"),
    ]),
    ("Company", [
        ("about.html", "About"),
        ("blog.html", "Blog"),
        ("contact.html", "Contact"),
        ("request-demo.html", "Request a demo"),
        ("faq.html", "FAQ"),
    ]),
    ("Legal", [
        ("privacy.html", "Privacy policy"),
        ("terms.html", "Terms of service"),
        ("security.html", "Security information"),
        ("login.html", "Log in"),
    ]),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | StaffPilot</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">S</span>StaffPilot</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Menu</button>
    <nav class="main-nav" id="main-nav" aria-label="Main navigation">
      <ul>
{nav_items}      </ul>
    </nav>
    <div class="header-cta">
      <a class="btn btn-ghost btn-sm" href="login.html">Log in</a>
      <a class="btn btn-light btn-sm" href="request-demo.html">Request a demo</a>
    </div>
  </div>
</header>
<main id="main">
{body}</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h3>StaffPilot</h3>
        <p>Workforces. Projects. Payroll. One Platform.</p>
        <p>For small staffing companies, consulting firms, and employers managing 20&ndash;100 workers in the U.S.</p>
        <p class="small">StaffPilot prepares payroll estimates only. It never moves payroll funds, files taxes, or claims a payroll or tax certification.</p>
      </div>
{footer_cols}    </div>
    <div class="footer-bottom">
      <p>&copy; <span id="footer-year">2026</span> StaffPilot. All rights reserved.</p>
      <p>Pricing shown is proposed pricing, published for transparency and subject to change. Payroll figures in the product are always labeled estimates.</p>
    </div>
  </div>
</footer>
<script src="assets/js/main.js"></script>
</body>
</html>
"""


def page_hero(eyebrow, title, text):
    return (
        '<section class="page-hero"><div class="wrap">'
        f'<p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{text}</p>'
        "</div></section>\n"
    )


def render(slug, title, description, body):
    nav_items = "".join(
        f'        <li><a href="{href}"'
        + (f' aria-current="page"' if href == slug else "")
        + f">{label}</a></li>\n"
        for href, label in NAV
    )
    cols = ""
    for heading, links in FOOTER_COLS:
        items = "".join(f'          <li><a href="{h}">{l}</a></li>\n' for h, l in links)
        cols += f'      <div>\n        <h3>{heading}</h3>\n        <ul>\n{items}        </ul>\n      </div>\n'
    html = TEMPLATE.format(
        title=title, description=description, nav_items=nav_items,
        footer_cols=cols, body=body,
    )
    (HERE / slug).write_text(html, encoding="utf-8")
    return slug

# ---------------------------------------------------------------- pages ---
PAGES = []


def add(slug, title, description, body):
    PAGES.append((slug, title, description, body))


# --- Home -----------------------------------------------------------------
HOME_BODY = """
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">For staffing &amp; consulting firms with 20&ndash;100 workers</p>
    <h1>Workforces. Projects. Payroll. One Platform.</h1>
    <p class="lede">StaffPilot connects assignments, timesheets, client approvals, billing, and payroll preparation in one workflow &mdash; so a small staffing firm can see its margin, bill on time, and prepare payroll from the same approved hours, without re-typing anything.</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="request-demo.html">Request a demo</a>
      <a class="btn btn-outline" href="pricing.html">See pricing</a>
      <a class="btn btn-outline" href="features.html">Explore features</a>
    </div>
    <p class="hero-note">14-day free trial &middot; No credit card required &middot; Full Growth features during the trial &middot; Payroll preparation is estimates only &mdash; StaffPilot never moves payroll funds or files taxes.</p>

    <div class="dashboard" aria-label="Sample StaffPilot dashboard preview">
      <div class="dashboard-bar"><span><span class="dot"></span> <span class="dot"></span> <span class="dot"></span></span><span>StaffPilot &mdash; Sample dashboard</span><span style="margin-left:auto;font-weight:400;">Week of Nov 16, 2026</span></div>
      <div class="dashboard-body">
        <p class="sample-note">Sample data &mdash; this dashboard shows synthetic demo figures, not a real customer&rsquo;s data.</p>
        <div class="kpis">
          <div class="kpi"><div class="label">Active workers</div><div class="value">45</div><div class="sub">Sample &middot; 38 direct, 7 vendor (C2C)</div></div>
          <div class="kpi"><div class="label">Hours approved</div><div class="value">1,612</div><div class="sub">Sample &middot; of 1,740 submitted</div></div>
          <div class="kpi"><div class="label">Billed this week</div><div class="value">$86,400</div><div class="sub">Sample &middot; from approved timesheets</div></div>
          <div class="kpi"><div class="label">Margin this week</div><div class="value">$21,300</div><div class="sub">Sample &middot; bill minus pay, estimated</div></div>
        </div>
        <div>
          <h3>Timesheets awaiting approval</h3>
          <table class="mini-table">
            <thead><tr><th>Consultant (sample)</th><th>Client (sample)</th><th>Hours</th><th>Status</th></tr></thead>
            <tbody>
              <tr><td>A. Rivera</td><td>Northbridge Financial</td><td>40</td><td><span class="status pending">Client approval</span></td></tr>
              <tr><td>J. Okafor</td><td>Harbor Health Systems</td><td>38</td><td><span class="status pending">Manager approval</span></td></tr>
              <tr><td>M. Chen</td><td>Northbridge Financial</td><td>40</td><td><span class="status ok">Approved</span></td></tr>
              <tr><td>S. Patel</td><td>Beacon Retail Group</td><td>32</td><td><span class="status ok">Approved</span></td></tr>
            </tbody>
          </table>
          <p class="small muted">Names, clients, hours, and amounts above are synthetic sample data for illustration only.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <p class="eyebrow">How it works</p>
    <h2>One approved hour, billed and prepped</h2>
    <p class="lede">The core loop: a timesheet is entered once, approved, invoiced, and used to prepare payroll estimates. No re-typing, no second source of truth.</p>
    <div class="steps">
      <div class="step"><h3>Enter timesheets</h3><p>Consultants log weekly hours against their assignment &mdash; direct or vendor-supplied.</p></div>
      <div class="step"><h3>Approve</h3><p>Manager approval, then client approval. Approved hours lock, with an audit trail of who approved what and when.</p></div>
      <div class="step"><h3>Bill the client</h3><p>Invoices are generated from approved timesheets and bill rates &mdash; not re-keyed from email.</p></div>
      <div class="step"><h3>Prepare payroll</h3><p>Payroll-preparation <em>estimates</em> are built from the same approved hours and pay rates, ready to hand to your payroll processor.</p></div>
      <div class="step"><h3>See your margin</h3><p>Bill minus pay, by client, consultant, and week &mdash; from the same records, not a month-end spreadsheet.</p></div>
    </div>
  </div>
</section>

<section class="block tint">
  <div class="wrap">
    <p class="eyebrow">What StaffPilot does</p>
    <h2>Built for the staffing model, not adapted to it</h2>
    <div class="grid grid-3">
      <div class="card"><div class="card-icon" aria-hidden="true">&#9783;</div><h3>Workforce records</h3><p>Consultant and employee profiles, assignments, bill rates, pay rates, and documents &mdash; with availability and roll-off dates your recruiters can actually see.</p><p><a href="workforce-management.html">Workforce management &rarr;</a></p></div>
      <div class="card"><div class="card-icon" aria-hidden="true">&#9776;</div><h3>Projects &amp; assignments</h3><p>Worker, client, and project linked in one assignment, with bill rate, pay rate, and margin visible before the work starts.</p><p><a href="features.html">See all features &rarr;</a></p></div>
      <div class="card"><div class="card-icon" aria-hidden="true">&#10003;</div><h3>Timesheets &amp; approvals</h3><p>Draft &rarr; submitted &rarr; manager-approved &rarr; client-approved, locked after approval and audit-logged at every step.</p><p><a href="features.html">See all features &rarr;</a></p></div>
      <div class="card"><div class="card-icon" aria-hidden="true">&#36;</div><h3>Billing</h3><p>Invoices generated from approved timesheets and rates, so billing and hours can never drift apart.</p><p><a href="features.html">See all features &rarr;</a></p></div>
      <div class="card"><div class="card-icon" aria-hidden="true">&#9782;</div><h3>Payroll preparation</h3><p>Estimates from approved hours and pay rates &mdash; figures for review, to hand to your actual payroll processor. Never funds movement, never tax filing.</p><p><a href="payroll-preparation.html">What payroll preparation means &rarr;</a></p></div>
      <div class="card"><div class="card-icon" aria-hidden="true">&#9873;</div><h3>C2C vendor tracking</h3><p>Vendor consultants, vendor rates, and vendor invoices in the same workflow as direct consultants &mdash; on Growth and Scale.</p><p><a href="c2c-consulting.html">C2C consulting &rarr;</a></p></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <p class="eyebrow">Who it is for</p>
    <h2>Sized for firms with 20&ndash;100 workers</h2>
    <div class="grid grid-3">
      <div class="card"><h3>Staffing firms</h3><p>Place consultants at clients, track bill vs. pay, and stop reconciling margin in spreadsheets at month-end.</p><p><a href="staffing-firms.html">For staffing firms &rarr;</a></p></div>
      <div class="card"><h3>Consulting firms</h3><p>Staff projects, watch utilization and project margin, and bill approved hours as soon as they are approved.</p><p><a href="workforce-management.html">For consulting firms &rarr;</a></p></div>
      <div class="card"><h3>Small employers</h3><p>One place for worker records, assignments, timesheets, billing, and payroll-preparation estimates.</p><p><a href="features.html">See all features &rarr;</a></p></div>
    </div>
    <div class="callout">
      <p><strong>What StaffPilot is not.</strong> It is not a payroll processor, not a PEO or employer of record, not a tax or compliance advisor, and not a recruiting CRM. It does not employ anyone&rsquo;s workers, classify workers, or run payroll. <a href="faq.html">Read the FAQ</a>.</p>
    </div>
  </div>
</section>

<section class="block tint">
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h2>Transparent pricing, per worker</h2>
    <p class="lede">A base platform fee plus a per-worker monthly charge. No per-payroll-run fees, no per-invoice fees, no hidden payroll-processing fees &mdash; because StaffPilot does not process payroll.</p>
    <div class="grid grid-3">
      <div class="card"><span class="tag">Starter</span><p class="price">$49<span class="per">/mo base + $4/worker/mo</span></p><p>For a small agency replacing spreadsheets with its first real system.</p><p><strong>At 45 workers: $229/mo.</strong></p></div>
      <div class="card"><span class="tag popular">Growth &middot; Most popular</span><p class="price">$99<span class="per">/mo base + $6/worker/mo</span></p><p>For a growing firm that needs vendor tracking and better reporting.</p><p><strong>At 45 workers: $369/mo.</strong></p></div>
      <div class="card"><span class="tag">Scale</span><p class="price">$199<span class="per">/mo base + $8/worker/mo</span></p><p>For firms at the top of the segment running multi-client, multi-vendor operations.</p><p><strong>At 45 workers: $559/mo.</strong></p></div>
    </div>
    <p style="margin-top:1rem;"><a class="btn btn-primary" href="pricing.html">Compare all tiers</a> <a class="btn btn-outline" href="request-demo.html">Request a demo</a></p>
    <p class="small muted">Annual billing: 2 months free (about 17% off). Prices are proposed pricing, published for transparency.</p>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <p class="eyebrow">Frequently asked questions</p>
    <h2>Straight answers, including the limits</h2>
    <details class="faq"><summary>Does StaffPilot run payroll?</summary><p>No. StaffPilot prepares payroll <em>estimates</em> from approved hours and pay rates. It never moves payroll funds, makes direct deposits, files taxes, or makes tax deposits. You hand the estimates to your actual payroll processor.</p></details>
    <details class="faq"><summary>How does the 14-day trial work?</summary><p>Fourteen days, no credit card required, with full Growth-tier features. At the end you can pick a tier or export your data and leave. No card was taken, so there is nothing to cancel and no auto-charge.</p></details>
    <details class="faq"><summary>What does it cost for my firm?</summary><p>A base fee plus a per-worker monthly charge: Starter $49 + $4/worker, Growth $99 + $6/worker, Scale $199 + $8/worker. At 45 workers that is $229, $369, or $559 per month. Use the calculator on the <a href="pricing.html">pricing page</a>.</p></details>
    <details class="faq"><summary>Does StaffPilot store Social Security numbers or bank details?</summary><p>No. StaffPilot does not ask for or store real Social Security numbers or bank account details for payroll purposes.</p></details>
    <p><a href="faq.html">Read all frequently asked questions &rarr;</a></p>
  </div>
</section>

<section class="block navy">
  <div class="wrap">
    <h2>See your margin, every week</h2>
    <p>Start a 14-day free trial &mdash; no credit card &mdash; or book a demo and we will walk your own workflow through the timesheet &rarr; approval &rarr; billing &rarr; payroll-prep loop.</p>
    <p><a class="btn btn-light" href="request-demo.html">Request a demo</a> <a class="btn btn-ghost" href="contact.html">Contact us</a></p>
  </div>
</section>
"""
add("index.html", "Workforces. Projects. Payroll. One Platform.",
    "StaffPilot is the single platform for workforces, projects, and payroll preparation for small staffing and consulting firms managing 20–100 workers.",
    HOME_BODY)


# --- Features ---------------------------------------------------------------
FEATURES_BODY = page_hero("Features", "Everything the weekly loop needs. Nothing it doesn\u2019t.",
    "Worker records, assignments, timesheets, approvals, billing, payroll-preparation estimates, and reporting \u2014 in one tenant-isolated workspace per firm.") + """
<section class="block"><div class="wrap">
<div class="grid grid-3">
<div class="card"><h3>Worker &amp; consultant records</h3><p>Profiles, assignments, rates, documents, and status for every consultant and employee. Availability and roll-off dates visible to the people who place work.</p></div>
<div class="card"><h3>Assignments</h3><p>Worker, client, and project linked in one assignment, with bill rate, pay rate, and margin. Rate changes are audit-logged.</p></div>
<div class="card"><h3>Timesheets</h3><p>Weekly entry against an assignment. Draft &rarr; submitted &rarr; manager-approved &rarr; client-approved, locked after approval.</p></div>
<div class="card"><h3>Client approvals</h3><p>Clients review and approve submitted hours in the platform \u2014 no reply-all approval threads, and a clean record when hours are disputed.</p></div>
<div class="card"><h3>Billing &amp; invoicing</h3><p>Invoices generated from approved timesheets and bill rates. Billing can never drift from approved hours, because it is built from them.</p></div>
<div class="card"><h3>Payroll preparation (estimates)</h3><p>Payroll-preparation estimates from approved hours and pay rates, labeled as estimates on every screen, ready to hand to your payroll processor. <a href="payroll-preparation.html">Learn what this means</a>.</p></div>
<div class="card"><h3>C2C vendor tracking <span class="tag">Growth+</span></h3><p>Vendor records, vendor consultants, vendor rates, and vendor invoices alongside direct consultants. <a href="c2c-consulting.html">C2C consulting</a>.</p></div>
<div class="card"><h3>Margin &amp; utilization reporting</h3><p>Margin by client, consultant, and week; utilization and billing-vs.-payroll-prep reconciliation on Growth and Scale.</p></div>
<div class="card"><h3>Roles &amp; permissions</h3><p>Role-based access for owners, recruiters, payroll managers, and client approvers. Custom roles and permissions on Growth and Scale.</p></div>
<div class="card"><h3>Data export <span class="tag">Growth+</span></h3><p>Export billing and payroll-preparation runs as CSV/Excel, so your data \u2014 and your exit \u2014 are never locked in.</p></div>
<div class="card"><h3>Audit trail</h3><p>Timesheet approvals, rate changes, and payroll-preparation runs are logged with who and when.</p></div>
<div class="card"><h3>API access <span class="tag">Scale</span></h3><p>Read/write API with API keys and rate limits, for firms that need to connect StaffPilot to their other tools.</p></div>
</div>
<div class="callout warn"><p><strong>Planned, not yet available:</strong> QuickBooks and Xero integrations are planned future integrations. They are not available in this version, and no date is promised here. The Scale API is the integration route available today.</p></div>
<h2>What StaffPilot deliberately does not do</h2>
<ul class="xlist">
<li>Move payroll funds or make direct deposits.</li>
<li>File taxes or make tax deposits, or calculate or guarantee tax withholdings.</li>
<li>Store real Social Security numbers or bank account details.</li>
<li>Auto-classify C2C consultants as independent contractors \u2014 classification is your legal determination, made with your own counsel.</li>
<li>Claim any payroll, tax, or compliance certification.</li>
</ul>
<p><a class="btn btn-primary" href="request-demo.html">Request a demo</a> <a class="btn btn-outline" href="pricing.html">See pricing</a></p>
</div></section>
"""
add("features.html", "Features", "Worker records, assignments, timesheets, approvals, billing, payroll-preparation estimates, and reporting — in one platform for staffing firms.", FEATURES_BODY)

# --- Staffing firms ---------------------------------------------------------
STAFFING_BODY = page_hero("For staffing firms", "Built for firms that place workers \u2014 and earn a margin on the difference.",
    "You place consultants at clients, bill one rate, pay another, and live on the margin between them. StaffPilot models that economics as the product, not as an add-on.") + """
<section class="block"><div class="wrap">
<h2>The problems this solves</h2>
<div class="grid grid-2">
<div class="card"><h3>Margin blindness</h3><p>Bill vs. pay rates live in spreadsheets. Nobody can say this week\u2019s true margin without manual work. StaffPilot shows margin by client, consultant, and week from the same assignment records.</p></div>
<div class="card"><h3>Timesheet chasing</h3><p>Hours arrive by email and chat; client approval is a reply-all thread; disputes surface at invoice time. One workflow collects, approves, and locks hours \u2014 with an audit trail.</p></div>
<div class="card"><h3>Billing and payroll prep don\u2019t connect</h3><p>Invoicing is built from one source, payroll preparation from another, and the margin is reconciled at month-end \u2014 if at all. In StaffPilot, one approved hour feeds both billing and the payroll-preparation estimate.</p></div>
<div class="card"><h3>Slow handover after placement</h3><p>Recruiters lose placements when handover to ops is manual and error-prone. A placement becomes an assignment with rates attached \u2014 no re-keying.</p></div>
</div>
<h2>Who uses it in your firm</h2>
<table class="data">
<thead><tr><th>Person</th><th>What they get</th></tr></thead>
<tbody>
<tr><td><strong>Agency owner</strong></td><td>Margin by client, consultant, and week \u2014 without asking ops to build a spreadsheet.</td></tr>
<tr><td><strong>Recruiter</strong></td><td>Who is available, at what rate, and when they roll off.</td></tr>
<tr><td><strong>Payroll &amp; billing lead</strong></td><td>Every timesheet in one place, approved, before the billing deadline; estimates that tie exactly to approved hours.</td></tr>
<tr><td><strong>C2C vendor manager</strong></td><td>Every vendor consultant, assignment, rate, and vendor invoice in one view. <a href="c2c-consulting.html">C2C consulting</a>.</td></tr>
</tbody>
</table>
<div class="callout"><p><strong>Honest limit:</strong> StaffPilot is not a recruiting CRM. It tracks placements and assignments, not candidate sourcing pipelines. And it prepares payroll estimates only \u2014 your payroll processor still runs payroll.</p></div>
<p><a class="btn btn-primary" href="request-demo.html">Request a demo</a> <a class="btn btn-outline" href="pricing.html">See pricing for staffing firms</a></p>
</div></section>
"""
add("staffing-firms.html", "StaffPilot for staffing firms", "StaffPilot for staffing firms: assignments, bill vs. pay rates, margin, timesheets, approvals, billing, and payroll-preparation estimates in one platform.", STAFFING_BODY)

# --- C2C consulting ---------------------------------------------------------
C2C_BODY = page_hero("C2C consulting", "Every vendor consultant, one view.",
    "Corp-to-corp consultants are easy to lose track of: vendor hours, vendor rates, and vendor invoices in separate spreadsheets per vendor. StaffPilot tracks them in the same workflow as your direct consultants.") + """
<section class="block"><div class="wrap">
<div class="grid grid-2">
<div class="card"><h3>Vendor records</h3><p>Vendor companies, contacts, agreements, and rate confirmations kept organized and retrievable \u2014 not scattered across email.</p></div>
<div class="card"><h3>Vendor consultants on assignments</h3><p>Vendor-supplied consultants sit on the same assignments, with the same timesheet and approval workflow as direct consultants.</p></div>
<div class="card"><h3>Vendor rates &amp; margin</h3><p>Bill rate, vendor pay rate, and margin on vendor-supplied consultants \u2014 not just on direct ones.</p></div>
<div class="card"><h3>Vendor invoices</h3><p>Vendor invoices tracked against approved vendor hours, so vendor billing disputes have a shared approval record to check.</p></div>
</div>
<div class="callout warn"><p><strong>Classification is your determination, not ours.</strong> StaffPilot never auto-classifies a C2C consultant as an independent contractor. Classification is the customer\u2019s legal determination, made with their own counsel. StaffPilot records the engagement type you enter and keeps the documentation organized \u2014 it does not advise on classification.</p></div>
<p>C2C vendor management is included on the Growth and Scale tiers. <a href="pricing.html">Compare tiers</a>.</p>
<p><a class="btn btn-primary" href="request-demo.html">Request a demo</a></p>
</div></section>
"""
add("c2c-consulting.html", "C2C consulting vendor management", "StaffPilot tracks C2C vendor consultants, vendor rates, and vendor invoices in the same workflow as direct consultants. No auto-classification, ever.", C2C_BODY)

# --- Workforce management ---------------------------------------------------
WORKFORCE_BODY = page_hero("Workforce management", "Know who is working, where, at what rate \u2014 and when they roll off.",
    "Worker records, assignments, documents, and status in one place, for consulting firms and employers managing 20\u2013100 workers.") + """
<section class="block"><div class="wrap">
<div class="grid grid-3">
<div class="card"><h3>One record per worker</h3><p>Consultant and employee profiles, current and past assignments, rates, documents, and status.</p></div>
<div class="card"><h3>Availability &amp; roll-off</h3><p>See who is free, who is on assignment, and when each assignment ends \u2014 before a client asks.</p></div>
<div class="card"><h3>Project staffing</h3><p>Staff a project from available consultants, with allocation and utilization visible in the same view as project margin.</p></div>
<div class="card"><h3>Documents</h3><p>Assignment documents and rate confirmations stored against the worker and the assignment, retrievable when a client or auditor asks.</p></div>
<div class="card"><h3>Utilization</h3><p>Utilization by consultant and project, so a drop is visible while there is still time to act \u2014 not at quarter-end.</p></div>
<div class="card"><h3>Roles &amp; access</h3><p>Role-based access for owners, recruiters, payroll managers, and client approvers. Each firm\u2019s data is isolated to that firm.</p></div>
</div>
<h2>For consulting-firm ops leads</h2>
<p>Your pain is different from a pure staffing agency&rsquo;s: project staffing, utilization, and billing live in different tools, and nobody sees the whole picture. StaffPilot puts utilization and project margin in one view, bills project hours as soon as they are approved, and runs payroll preparation from the same approved hours you already billed.</p>
<p><a class="btn btn-primary" href="request-demo.html">Request a demo</a> <a class="btn btn-outline" href="features.html">See all features</a></p>
</div></section>
"""
add("workforce-management.html", "Workforce management", "StaffPilot workforce management: worker records, assignments, availability, roll-off dates, documents, utilization, and project margin in one place.", WORKFORCE_BODY)

# --- Payroll preparation ----------------------------------------------------
PAYROLL_BODY = page_hero("Payroll preparation", "Payroll preparation. Estimates only. Said plainly, on purpose.",
    "StaffPilot prepares payroll estimates from approved hours and pay rates \u2014 figures for review, to hand to your actual payroll processor.") + """
<section class="block"><div class="wrap">
<div class="callout warn"><p><strong>Read this first.</strong> StaffPilot does <strong>not</strong> run payroll. It does not move payroll funds, make direct deposits, file taxes, make tax deposits, or calculate or guarantee tax withholdings. It does not store real Social Security numbers or bank account details. It claims no payroll, tax, or compliance certification. Every payroll figure in the product is labeled an estimate.</p></div>
<h2>What payroll preparation is</h2>
<p>After timesheets are approved, StaffPilot computes what payroll <em>would</em> look like from those approved hours and the pay rates on each assignment: gross pay estimates by worker, by client, and by pay cycle. You review every line against approved hours and rates, then hand the figures to your payroll processor \u2014 the company that actually moves funds and files taxes.</p>
<h2>How it works</h2>
<div class="steps">
<div class="step"><h3>Approved hours</h3><p>Only manager- and client-approved, locked hours feed payroll preparation.</p></div>
<div class="step"><h3>Pay rates applied</h3><p>The pay rate on each assignment is applied to its approved hours.</p></div>
<div class="step"><h3>Estimate generated</h3><p>Gross pay estimates by worker and cycle, every figure labeled &ldquo;estimate&rdquo;.</p></div>
<div class="step"><h3>You review</h3><p>Check every line before it leaves StaffPilot. Nothing is final until you say so.</p></div>
<div class="step"><h3>Hand to your processor</h3><p>Export the run (Growth and Scale) and give it to the payroll processor that runs your payroll.</p></div>
</div>
<h2>What it is not</h2>
<ul class="xlist">
<li>Payroll processing &mdash; no funds movement, no direct deposits.</li>
<li>Tax filing or tax deposits &mdash; no tax calculation or guarantee.</li>
<li>A source of tax or compliance advice, or any certification.</li>
<li>A place to store Social Security numbers or bank details &mdash; StaffPilot does not ask for them.</li>
</ul>
<p>Real tax calculation, if it ever comes to StaffPilot, would come only from a validated provider integration in a later phase &mdash; not from StaffPilot itself. That integration does not exist today.</p>
<p><a class="btn btn-primary" href="request-demo.html">Request a demo</a> <a class="btn btn-outline" href="faq.html">Payroll questions in the FAQ</a></p>
</div></section>
"""
add("payroll-preparation.html", "Payroll preparation (estimates only)", "StaffPilot prepares payroll estimates only from approved hours and pay rates. No funds movement, no tax filing, no certifications claimed.", PAYROLL_BODY)

# --- Pricing ----------------------------------------------------------------
PRICING_BODY = page_hero("Pricing", "Transparent pricing you can work out in under a minute.",
    "A base platform fee plus a per-worker monthly charge. No per-payroll-run fees, no per-invoice fees, no hidden payroll-processing fees \u2014 StaffPilot does not process payroll.") + """
<section class="block"><div class="wrap">
<div class="calculator" aria-label="Pricing calculator">
  <h2 style="margin-top:0;">Price it for your firm</h2>
  <label for="calc-workers" style="font-weight:700;">Active workers: <output id="calc-count">45</output></label>
  <input type="range" id="calc-workers" min="20" max="100" value="45" step="1" style="width:100%;" aria-describedby="calc-note">
  <p id="calc-note" class="small muted">A &ldquo;worker&rdquo; is any active consultant/employee record on an assignment in the billing month. Inactive or archived workers don&rsquo;t count.</p>
  <div class="grid grid-3">
    <div><strong>Starter:</strong> <output id="calc-starter">$229/mo</output></div>
    <div><strong>Growth:</strong> <output id="calc-growth">$369/mo</output></div>
    <div><strong>Scale:</strong> <output id="calc-scale">$559/mo</output></div>
  </div>
</div>
<div class="price-cards" style="margin-top:1.5rem;">
  <div class="card price-card">
    <span class="tag">Starter</span>
    <p class="price">$49<span class="per">/mo base + $4/worker/mo</span></p>
    <p>For a small agency replacing spreadsheets with its first real system. Target: 20&ndash;30 workers.</p>
    <ul>
      <li>Core worker records &amp; assignments (bill rate, pay rate, margin)</li>
      <li>Timesheets: entry, submit, manager approval</li>
      <li>Client approval of timesheets</li>
      <li>Invoicing from approved timesheets</li>
      <li>Payroll-preparation estimates (labeled estimates)</li>
      <li>Basic margin reporting (by client, by consultant)</li>
      <li>2 user seats included; extra seats $10/mo each</li>
      <li>Email support</li>
      <li class="no">C2C vendor management module</li>
      <li class="no">Advanced reporting, API access, priority support</li>
    </ul>
    <p><strong>Examples:</strong> 25 workers $149/mo &middot; 45 workers $229/mo &middot; 50 workers $249/mo &middot; 100 workers $449/mo.</p>
    <p><a class="btn btn-outline" href="request-demo.html">Start with Starter</a></p>
  </div>
  <div class="card price-card featured">
    <span class="tag popular">Growth &middot; Most popular</span>
    <p class="price">$99<span class="per">/mo base + $6/worker/mo</span></p>
    <p>For a growing firm that needs vendor tracking and better reporting. Target: 30&ndash;75 workers.</p>
    <ul>
      <li>Everything in Starter, plus:</li>
      <li>C2C vendor consultant tracking (vendor records, rates, invoices)</li>
      <li>Advanced reporting: utilization, margin trends, billing vs. payroll-prep reconciliation</li>
      <li>5 user seats included; extra seats $10/mo each</li>
      <li>Custom roles and permissions</li>
      <li>Data export (CSV/Excel) for billing &amp; payroll-prep runs</li>
      <li>Priority email support (next-business-day target)</li>
      <li class="no">API access, dedicated onboarding, SLA</li>
    </ul>
    <p><strong>Examples:</strong> 25 workers $249/mo &middot; 45 workers $369/mo &middot; 50 workers $399/mo &middot; 100 workers $699/mo.</p>
    <p><a class="btn btn-primary" href="request-demo.html">Start a 14-day trial</a></p>
  </div>
  <div class="card price-card">
    <span class="tag">Scale</span>
    <p class="price">$199<span class="per">/mo base + $8/worker/mo</span></p>
    <p>For firms at the top of the segment running multi-client, multi-vendor operations. Target: 75&ndash;100+ workers.</p>
    <ul>
      <li>Everything in Growth, plus:</li>
      <li>API access (read/write, API keys, rate limits)</li>
      <li>10 user seats included; extra seats $10/mo each</li>
      <li>Dedicated onboarding session (1:1, remote)</li>
      <li>Quarterly business review (margin/utilization walkthrough)</li>
      <li>Priority support, same-business-day target</li>
      <li>Early access to new modules as they ship</li>
      <li class="no">Real payroll funds, tax filing, or tax deposits &mdash; no tier includes those, ever</li>
    </ul>
    <p><strong>Examples:</strong> 25 workers $399/mo &middot; 45 workers $559/mo &middot; 50 workers $599/mo &middot; 100 workers $999/mo.</p>
    <p><a class="btn btn-outline" href="request-demo.html">Talk to us about Scale</a></p>
  </div>
</div>
<h2>Free trial</h2>
<p><strong>14-day free trial, no credit card required.</strong> Full Growth-tier features during the trial, so you evaluate the real product, including vendor tracking. One tenant, up to 100 workers, no API access during the trial. At the end, pick a tier or export your data and leave. No card was taken, so there is no auto-charge.</p>
<h2>What is never charged for</h2>
<ul class="checklist">
<li>Payroll-preparation runs: unlimited, all tiers.</li>
<li>Timesheet submissions and approvals: unlimited.</li>
<li>Invoices generated: unlimited.</li>
<li>Data export on Growth/Scale: unlimited.</li>
</ul>
<h2>What no tier includes</h2>
<ul class="xlist">
<li>Real payroll processing: no funds movement, no direct deposits, no tax filing, no tax deposits.</li>
<li>Storage of real SSNs or bank account details.</li>
<li>Worker classification advice or auto-classification.</li>
<li>Any certification claim.</li>
<li>Custom development.</li>
</ul>
<p class="small muted">Prices are proposed pricing, published for transparency and subject to change. Annual billing: 2 months free (about 17% off). The worker-count bands in the tier descriptions are a soft guide, not a hard cap &mdash; a Starter customer with 28 workers pays the per-worker rate for workers above 25 rather than being forced to upgrade. The tier difference is features, not headcount walls.</p>
<p><a class="btn btn-primary" href="request-demo.html">Request a demo</a> <a class="btn btn-outline" href="faq.html">Pricing questions in the FAQ</a></p>
</div></section>
"""
add("pricing.html", "Pricing", "StaffPilot pricing: Starter $49/mo + $4/worker, Growth $99/mo + $6/worker, Scale $199/mo + $8/worker. 14-day free trial, no credit card.", PRICING_BODY)

# --- About ------------------------------------------------------------------
ABOUT_BODY = page_hero("About", "A small tool for small staffing firms, built honestly.",
    "StaffPilot is a B2B software-as-a-service platform for staffing companies, consulting firms, and small employers managing 20\u2013100 workers in the U.S. \u2014 New York first.") + """
<section class="block"><div class="wrap">
<h2>What we are building</h2>
<p>Small staffing and consulting firms sit in a gap: spreadsheets that go stale, timesheets chased by email, billing and payroll preparation built from different sources, and generic HR/payroll tools built for direct employers &mdash; not for firms that place workers at clients and earn a margin on the difference. Enterprise staffing suites, meanwhile, are priced and implemented for firms far larger than 20&ndash;100 workers.</p>
<p>StaffPilot is the single platform for workforces, projects, and payroll preparation, sized, priced, and built for the way small staffing firms actually run: assignments with bill and pay rates, a timesheet &rarr; approval &rarr; billing &rarr; payroll-prep loop, and C2C vendor tracking.</p>
<h2>Three lines we do not blur</h2>
<table class="data">
<thead><tr><th>Separation</th><th>What it means</th></tr></thead>
<tbody>
<tr><td><strong>Subscription software</strong></td><td>StaffPilot sells software access. It is not the customer&rsquo;s employer, staffing agency, or payroll provider.</td></tr>
<tr><td><strong>Staffing operations</strong></td><td>The customer runs their staffing business: hiring, placing, managing, and supervising workers. StaffPilot provides the workflow tools.</td></tr>
<tr><td><strong>Payroll processing</strong></td><td>StaffPilot prepares estimates only. It never moves payroll funds, files taxes, or claims certifications.</td></tr>
</tbody>
</table>
<h2>How we work</h2>
<ul class="checklist">
<li>Plain, direct language. Specific over grand.</li>
<li>Honest about limits &mdash; saying &ldquo;we prepare payroll estimates; your processor runs payroll&rdquo; builds more trust than implying full payroll.</li>
<li>No fake customer logos, testimonials, case studies, or market statistics. Ever.</li>
<li>Discovery first: pricing and positioning are validated with real firms before they are treated as final.</li>
</ul>
<p>StaffPilot is an early-stage product. The website describes what the product does today and what is planned; planned items are labeled as planned. If you run a 20&ndash;100-worker firm and this workflow sounds like yours, <a href="contact.html">talk to us</a>.</p>
</div></section>
"""
add("about.html", "About StaffPilot", "StaffPilot is a B2B SaaS for staffing companies, consulting firms, and small employers managing 20–100 workers. Workforces, projects, and payroll preparation in one platform.", ABOUT_BODY)

# --- Contact ----------------------------------------------------------------
CONTACT_BODY = page_hero("Contact", "Talk to a person, not a ticket queue.",
    "Questions about fit, pricing, the trial, or the payroll-preparation boundary? Write to us and we will reply.") + """
<section class="block"><div class="wrap">
<div class="grid grid-2">
<div>
<form id="contact-form" class="stacked" novalidate>
<label for="contact-name">Your name</label>
<input type="text" id="contact-name" name="name" data-required autocomplete="name">
<p class="field-error" id="contact-name-error">Please enter your name.</p>
<label for="contact-email">Work email</label>
<input type="email" id="contact-email" name="email" data-required autocomplete="email">
<p class="field-error" id="contact-email-error">Please enter a valid email address.</p>
<label for="contact-company">Company</label>
<input type="text" id="contact-company" name="company" data-required autocomplete="organization">
<p class="field-error" id="contact-company-error">Please enter your company name.</p>
<label for="contact-topic">Topic</label>
<select id="contact-topic" name="topic">
<option>General question</option><option>Pricing and trial</option><option>Fit for my firm</option><option>Payroll preparation boundary</option><option>Security and data</option><option>Something else</option>
</select>
<label for="contact-message">Message</label>
<textarea id="contact-message" name="message" rows="5" data-required></textarea>
<p class="field-error" id="contact-message-error">Please write a short message.</p>
<p><button class="btn btn-primary" type="submit">Send message</button></p>
</form>
<div class="confirmation" id="contact-confirmation" role="status">
<h3>Message recorded</h3>
<p id="contact-summary">Thanks. Your message was recorded locally in this browser.</p>
<p>Please do not include Social Security numbers, bank details, or other sensitive personal data in a contact message &mdash; StaffPilot never asks for them.</p>
</div>
<p class="form-note"><strong>How this form works in this version:</strong> there is no backend API yet, so messages are stored only in this browser&rsquo;s local storage until the API exists (Phase 15). Nothing is sent to a server. If you need an answer now, request a demo instead and we will follow up from there.</p>
</div>
<div>
<h2>Before you write</h2>
<ul class="checklist">
<li><strong>Fit:</strong> StaffPilot is built for firms managing 20&ndash;100 workers. Smaller or much larger? Tell us anyway &mdash; we will say plainly whether it fits.</li>
<li><strong>Trial:</strong> 14 days, no credit card, full Growth features. <a href="request-demo.html">Request a demo</a> to start.</li>
<li><strong>Payroll:</strong> estimates only. <a href="payroll-preparation.html">Read the boundary</a> before you ask us to run payroll &mdash; we can&rsquo;t, and we won&rsquo;t pretend otherwise.</li>
<li><strong>Security:</strong> see the <a href="security.html">security information</a> page for what is implemented and planned.</li>
</ul>
<h2>What not to send</h2>
<p>Never send Social Security numbers, bank routing or account numbers, passwords, or worker tax documents through this form or by email. StaffPilot does not need them and does not store them.</p>
</div>
</div>
</div></section>
"""
add("contact.html", "Contact StaffPilot", "Contact StaffPilot with questions about fit, pricing, the trial, or the payroll-preparation boundary.", CONTACT_BODY)

# --- Request a demo ---------------------------------------------------------
DEMO_BODY = page_hero("Request a demo", "See your own workflow in StaffPilot.",
    "A 30-minute walkthrough of the timesheet &rarr; approval &rarr; billing &rarr; payroll-prep loop, using your firm&rsquo;s workflow &mdash; not a generic slide deck.") + """
<section class="block"><div class="wrap">
<div class="grid grid-2">
<div>
<form id="demo-form" class="stacked" novalidate>
<label for="demo-name">Your name</label>
<input type="text" id="demo-name" name="name" data-required autocomplete="name">
<p class="field-error" id="demo-name-error">Please enter your name.</p>
<label for="demo-email">Work email</label>
<input type="email" id="demo-email" name="email" data-required autocomplete="email">
<p class="field-error" id="demo-email-error">Please enter a valid email address.</p>
<label for="demo-company">Company</label>
<input type="text" id="demo-company" name="company" data-required autocomplete="organization">
<p class="field-error" id="demo-company-error">Please enter your company name.</p>
<label for="demo-workers">How many workers do you manage?</label>
<input type="number" id="demo-workers" name="workers" min="1" max="500" data-required inputmode="numeric" placeholder="e.g. 45">
<p class="field-error" id="demo-workers-error">Please enter a number of workers (1 or more).</p>
<label for="demo-type">What best describes your firm?</label>
<select id="demo-type" name="firm-type">
<option>Staffing company</option><option>Consulting firm</option><option>Small employer (direct hires)</option><option>Other</option>
</select>
<label for="demo-notes">What should the demo focus on? (optional)</label>
<textarea id="demo-notes" name="notes" rows="4" placeholder="e.g. C2C vendor tracking, client approvals, payroll-prep handoff"></textarea>
<p><button class="btn btn-primary" type="submit">Request my demo</button></p>
</form>
<div class="confirmation" id="demo-confirmation" role="status">
<h3>Demo request recorded</h3>
<p id="demo-summary">Thanks. Your request was recorded locally in this browser.</p>
<p>What happens next: in the live product, the team confirms a time by email. In this version, your request is stored only in this browser until the demo-request API exists (Phase 15) &mdash; it has not been sent anywhere yet.</p>
</div>
<p class="form-note"><strong>How this form works in this version:</strong> demo requests are stored locally in this browser (local storage) until the API exists (Phase 15). Nothing is sent to a server and no email is sent. This note is here so the form never pretends to do more than it does.</p>
</div>
<div>
<h2>What the demo covers</h2>
<ul class="checklist">
<li>Worker records and assignments with bill rate, pay rate, and margin.</li>
<li>The full loop: timesheet &rarr; manager approval &rarr; client approval &rarr; invoice &rarr; payroll-preparation estimate.</li>
<li>C2C vendor tracking, if your firm uses vendor consultants.</li>
<li>Margin and utilization reporting for your worker count.</li>
<li>The payroll-preparation boundary, stated plainly: estimates only.</li>
</ul>
<h2>Prefer to try it yourself?</h2>
<p>The 14-day free trial needs no credit card and includes full Growth features. The demo is the guided route; the trial is the self-serve route. Either way, you start with one client, one pay cycle, and a handful of workers &mdash; prove the loop, then roll out the rest of the firm.</p>
<p><a href="pricing.html">See pricing</a> &middot; <a href="faq.html">Read the FAQ</a></p>
</div>
</div>
</div></section>
"""
add("request-demo.html", "Request a demo", "Request a 30-minute StaffPilot demo: the timesheet → approval → billing → payroll-prep loop, using your firm’s workflow.", DEMO_BODY)

# --- Blog -------------------------------------------------------------------
BLOG_BODY = page_hero("Blog", "Notes on running a small staffing firm.",
    "Practical notes on timesheets, billing, margin, and payroll preparation \u2014 written for the ops person who runs the weekly loop.") + """
<section class="block"><div class="wrap"><div class="post-list">
<article class="card post">
<p class="eyebrow">Workflow</p>
<h2>One approved hour, billed and prepped: the loop that replaces five spreadsheets</h2>
<p><time datetime="2026-11-19">November 19, 2026</time> &middot; 5-minute read</p>
<p>Most small staffing firms already run the same loop every week: a consultant logs hours, a manager approves them, a client approves them, someone builds an invoice, and someone prepares payroll. The problem is not the loop &mdash; it is that the loop runs in five places. Hours live in email, approvals in a reply-all thread, rates in a spreadsheet, invoices in an accounting tool, and payroll preparation in a second spreadsheet built from the first.</p>
<p>When one approved hour feeds both billing and payroll preparation, three things change. First, billing and payroll prep cannot drift apart, because they are built from the same hours. Second, a disputed hour has an answer: who approved it and when. Third, margin is visible during the week, not reconstructed at month-end. That is the whole idea behind StaffPilot&rsquo;s core loop &mdash; timesheet &rarr; manager approval &rarr; client approval &rarr; invoice &rarr; payroll-preparation estimate &mdash; and the test of any tool that claims to run it is simple: enter an hour once, and count how many times you have to re-type it.</p>
<p><a href="features.html">See how the loop works in StaffPilot &rarr;</a></p>
</article>
<article class="card post">
<p class="eyebrow">Payroll preparation</p>
<h2>Payroll preparation is not payroll processing &mdash; and why the distinction matters</h2>
<p><time datetime="2026-11-12">November 12, 2026</time> &middot; 4-minute read</p>
<p>&ldquo;Payroll preparation&rdquo; and &ldquo;payroll processing&rdquo; sound like the same thing. They are not, and blurring them is the single biggest trust risk for a staffing firm choosing software.</p>
<p>Preparation means computing what payroll <em>would</em> look like from approved hours and pay rates, so you can review it and hand it to the company that actually runs your payroll. Processing means moving the money: direct deposits, tax filing, tax deposits, withholdings. StaffPilot does the first and is explicit that it never does the second. It does not store Social Security numbers or bank details, and it labels every payroll figure an estimate.</p>
<p>If a vendor ever implies it runs payroll while only preparing estimates &mdash; or asks for bank details it does not need &mdash; treat that as a reason to walk away, whoever the vendor is. Ask any payroll tool three questions before you buy: do you move funds, do you file taxes, and do you store SSNs or bank details? The answers should be short, specific, and in writing.</p>
<p><a href="payroll-preparation.html">Read StaffPilot&rsquo;s payroll boundary in full &rarr;</a></p>
</article>
<article class="card post">
<p class="eyebrow">C2C &amp; vendors</p>
<h2>Managing C2C vendor consultants without losing the margin &mdash; or the paperwork</h2>
<p><time datetime="2026-11-05">November 5, 2026</time> &middot; 4-minute read</p>
<p>Vendor-supplied consultants create a second books problem: their hours, rates, and invoices are tracked per vendor, often in a separate spreadsheet each, while the client is billed from a different one. The margin on a vendor consultant is real money, but it is the last margin a firm can see clearly.</p>
<p>The fix is unglamorous: put vendor consultants on the same assignments, the same timesheet workflow, and the same approval record as direct consultants, with the vendor rate visible next to the bill rate. Then vendor invoices can be checked against approved vendor hours, and a vendor billing dispute has a shared record instead of two competing spreadsheets.</p>
<p>One boundary matters more than the workflow: no software should auto-classify a C2C consultant as an independent contractor. Classification is your legal determination, made with your own counsel. A tool should record the engagement type you enter and keep the documentation organized &mdash; nothing more.</p>
<p><a href="c2c-consulting.html">How StaffPilot tracks C2C vendors &rarr;</a></p>
</article>
</div>
<p class="small muted" style="margin-top:1rem;">Articles are dated November 2026. No customer names, testimonials, or statistics appear on this blog, because none have been gathered yet.</p>
</div></section>
"""
add("blog.html", "Blog", "Practical notes on timesheets, billing, margin, C2C vendors, and payroll preparation for small staffing firms.", BLOG_BODY)

# --- FAQ --------------------------------------------------------------------
FAQ_ITEMS = [
    ("What is StaffPilot?", "StaffPilot is a subscription software platform for small staffing companies, consulting firms, and employers managing 20\u2013100 workers. It brings together worker records, assignments, timesheets, client approvals, billing, and payroll-preparation estimates in one tenant-isolated workspace per firm."),
    ("Does StaffPilot run payroll?", "No. StaffPilot prepares payroll estimates only, from approved hours and pay rates. It never moves payroll funds, makes direct deposits, files taxes, makes tax deposits, or calculates or guarantees tax withholdings. You hand the estimates to your actual payroll processor."),
    ("What does it cost?", "A base fee plus a per-worker monthly charge: Starter $49/mo + $4/worker, Growth $99/mo + $6/worker, Scale $199/mo + $8/worker. At 45 workers that is $229, $369, or $559 per month. Annual billing is 2 months free (about 17% off). See the pricing page for the full comparison and a calculator."),
    ("How does the 14-day free trial work?", "Fourteen days, no credit card required, with full Growth-tier features. One tenant, up to 100 workers, no API access during the trial. At the end you pick a tier or export your data and leave. No card was taken, so there is no auto-charge."),
    ("What counts as a \u201cworker\u201d for billing?", "Any active consultant or employee record on an assignment in the billing month. Inactive or archived workers don\u2019t count."),
    ("What is C2C, and how does StaffPilot handle it?", "C2C (corp-to-corp) means consultants employed by a third-party vendor and placed at your clients. StaffPilot tracks vendor records, vendor consultants, vendor rates, and vendor invoices in the same workflow as direct consultants (Growth and Scale tiers). StaffPilot never auto-classifies a C2C consultant as an independent contractor \u2014 classification is your legal determination, made with your own counsel."),
    ("Does StaffPilot store Social Security numbers or bank details?", "No. StaffPilot does not ask for or store real Social Security numbers or bank account details for payroll purposes."),
    ("Does StaffPilot classify workers or give tax advice?", "No. StaffPilot does not classify workers, advise on classification, calculate taxes, or give tax or compliance advice. It records the engagement type you enter."),
    ("Is my firm\u2019s data kept separate from other firms?", "Yes. Each customer gets a tenant-isolated workspace, and role-based access controls who inside your firm can see and do what. No cross-tenant access. See the security information page for what is implemented and what is planned."),
    ("Is StaffPilot SOC 2 or ISO certified?", "No. StaffPilot holds no SOC 2, ISO, tax, or payroll certification, and claims none. The security page states what is implemented and planned honestly, and will be updated if a certification is ever obtained."),
    ("What happens to my data if I cancel?", "You can export your billing and payroll-preparation data (Growth and Scale) and leave. At the end of a trial, the same applies: pick a tier, or export your data and leave."),
    ("Does StaffPilot integrate with QuickBooks or Xero?", "Not yet. QuickBooks and Xero integrations are planned future integrations, with no date promised. The Scale API is the integration route available today, and data export (CSV/Excel) is available on Growth and Scale."),
    ("What if my firm has fewer than 20 or more than 100 workers?", "StaffPilot is built and priced for 20\u2013100 workers. If you are outside that range, contact us \u2014 we will say plainly whether it fits, rather than sell you a tool built for a different size of firm."),
    ("Can I get a demo before the trial?", "Yes. Request a demo and we will walk your own workflow through the timesheet \u2192 approval \u2192 billing \u2192 payroll-prep loop in about 30 minutes."),
    ("Who do I contact with a question?", "Use the contact page. Do not send Social Security numbers, bank details, passwords, or worker tax documents through the form or by email \u2014 StaffPilot never asks for them."),
]
FAQ_BODY = page_hero("FAQ", "Frequently asked questions.",
    "Straight answers \u2014 including the limits. If your question is not here, contact us.") + """
<section class="block"><div class="wrap">
""" + "\n".join(
    f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ_ITEMS
) + """
<p style="margin-top:1.5rem;"><a class="btn btn-primary" href="request-demo.html">Request a demo</a> <a class="btn btn-outline" href="contact.html">Ask something else</a></p>
</div></section>
"""
add("faq.html", "Frequently asked questions", "StaffPilot FAQ: pricing, the trial, C2C, payroll-preparation boundaries, data, security, and integrations.", FAQ_BODY)

# --- Login ------------------------------------------------------------------
LOGIN_BODY = page_hero("Log in", "Sign in to the StaffPilot application.",
    "StaffPilot accounts sign in through the application itself, not through this website.") + """
<section class="block"><div class="wrap">
<div class="grid grid-2">
<div class="card">
<h2>How sign-in works</h2>
<p>Authentication for the StaffPilot application is provided by <strong>Supabase Auth</strong>. When you sign in to the application, you sign in with the email and password (or other method) set up for your firm&rsquo;s tenant. Your firm&rsquo;s data is isolated to your tenant, and your role determines what you can see and do.</p>
<p>This public website does not have a sign-in form and does not accept passwords. That is deliberate: credentials belong only in the application, never on a marketing page.</p>
<div class="callout"><p><strong>Application sign-in is not yet published.</strong> The StaffPilot application is still being built, and its hosted sign-in page is not live yet. This page will link directly to it as soon as it is. If you are an existing trial or pilot customer, use the sign-in link sent to you by the StaffPilot team.</p></div>
<p><a class="btn btn-primary" href="request-demo.html">Request a demo</a> <a class="btn btn-outline" href="contact.html">Contact us</a></p>
</div>
<div>
<h2>New here?</h2>
<p>If your firm does not have a StaffPilot account yet, start with the <strong>14-day free trial</strong> (no credit card, full Growth features) or <a href="request-demo.html">request a demo</a> first. Signup creates your firm&rsquo;s tenant and your admin user, and confirms in writing that StaffPilot prepares payroll estimates only.</p>
<h2>Locked out?</h2>
<p>Password resets and account recovery are handled inside the application&rsquo;s Supabase Auth flow once it is live. Until then, <a href="contact.html">contact us</a> and we will help. Never share your password by email or through the contact form.</p>
<h2>Security notes</h2>
<p>See the <a href="security.html">security information</a> page for what is implemented and planned, including tenant isolation and role-based access. StaffPilot holds no SOC 2 or ISO certification and claims none.</p>
</div>
</div>
</div></section>
"""
add("login.html", "Log in", "Sign in to the StaffPilot application. Authentication is provided by Supabase Auth; this website has no sign-in form.", LOGIN_BODY)

# --- Privacy ----------------------------------------------------------------
PRIVACY_BODY = page_hero("Privacy policy", "Privacy policy.",
    "Last updated: November 2026. This policy describes what StaffPilot collects on this website and in the product, and what it does not collect.") + """
<section class="block legal"><div class="wrap">
<h2>1. Who we are</h2>
<p>StaffPilot is a B2B software-as-a-service platform for staffing companies, consulting firms, and small employers managing 20&ndash;100 workers. This policy covers the public website (this site) and the StaffPilot application.</p>
<h2>2. What we collect on this website</h2>
<p>When you use the demo-request or contact forms on this site, we collect the information you enter: your name, work email, company, firm type, worker count, and your message. In this version of the site, form submissions are stored only in your browser&rsquo;s local storage until the API exists (Phase 15); they are not sent to a server. Once the API exists, submissions will be sent to StaffPilot so we can respond, and this policy will be updated to say so.</p>
<h2>3. What the product collects</h2>
<p>The application collects the business data your firm enters to run its staffing workflow: worker and consultant records, assignments, rates, timesheets, approvals, invoices, and payroll-preparation estimates. Your firm&rsquo;s data is isolated to your tenant; no other customer can see it.</p>
<h2>4. What we do not collect</h2>
<p>StaffPilot does not ask for or store real Social Security numbers or bank account details for payroll purposes, and you should never enter them into the product or send them through the website forms or by email. StaffPilot does not sell personal data.</p>
<h2>5. How we use information</h2>
<p>We use contact information to respond to demo requests and enquiries, to provide the service, and to operate and secure it. We do not use your firm&rsquo;s business data for advertising, and we do not share it with other customers.</p>
<h2>6. Data retention and deletion</h2>
<p>Contact and demo-request data is kept only as long as needed to respond and to keep a record of the enquiry. Product data is kept while your subscription (or trial) is active. You may request export or deletion of your firm&rsquo;s data by contacting us; Growth and Scale tiers also include self-serve data export.</p>
<h2>7. Cookies and tracking</h2>
<p>This website uses no third-party analytics or advertising trackers. The only browser storage used is local storage for form submissions in this version (see section 2), which stays in your browser.</p>
<h2>8. Changes to this policy</h2>
<p>We will update this page when the product or the website changes how it handles data &mdash; including when the demo-request and contact APIs go live. The &ldquo;last updated&rdquo; date at the top will change with it.</p>
<h2>9. Contact</h2>
<p>Questions about this policy: use the <a href="contact.html">contact page</a>.</p>
</div></section>
"""
add("privacy.html", "Privacy policy", "StaffPilot privacy policy: what the website and product collect, what they do not collect, and how data is used.", PRIVACY_BODY)

# --- Terms ------------------------------------------------------------------
TERMS_BODY = page_hero("Terms of service", "Terms of service.",
    "Last updated: November 2026. These terms cover use of the StaffPilot website and the StaffPilot application.") + """
<section class="block legal"><div class="wrap">
<h2>1. The service</h2>
<p>StaffPilot provides subscription access to software for workforce, project, and payroll-preparation workflows. StaffPilot is not the customer&rsquo;s employer, staffing agency, or payroll provider.</p>
<h2>2. Payroll preparation &mdash; estimates only</h2>
<p>StaffPilot prepares payroll <em>estimates</em> from approved hours and pay rates. It does not move payroll funds, make direct deposits, file taxes, make tax deposits, or calculate or guarantee tax withholdings. Payroll figures in the product are labeled estimates. The customer is responsible for reviewing every estimate and for all actual payroll processing, tax filing, and payments through its own payroll processor.</p>
<h2>3. What the customer is responsible for</h2>
<p>The customer runs its own staffing business: hiring, placing, managing, and supervising its workers and consultants, and all worker classification determinations (made with its own counsel). The customer must not enter real Social Security numbers or bank account details into the product. The customer is responsible for the accuracy of the rates, hours, and records it enters.</p>
<h2>4. Subscriptions, trial, and pricing</h2>
<p>Subscriptions are billed per the published tiers (Starter, Growth, Scale) at a base fee plus a per-worker monthly charge. The 14-day free trial requires no credit card and includes full Growth features; no card is taken, so there is no auto-charge at trial end. Prices are proposed pricing, published for transparency, and may change; existing customers will be told of a price change before it applies to them.</p>
<h2>5. Acceptable use</h2>
<p>You must not use the service to break the law, to misrepresent payroll estimates as final payroll or tax figures, to store Social Security numbers or bank details, or to attempt to access another customer&rsquo;s tenant. We may suspend access for misuse.</p>
<h2>6. Data and confidentiality</h2>
<p>Each customer&rsquo;s data is isolated to its tenant. We do not share one customer&rsquo;s data with another. See the <a href="privacy.html">privacy policy</a> and the <a href="security.html">security information</a> page.</p>
<h2>7. No certifications; no warranties beyond the service</h2>
<p>StaffPilot claims no SOC 2, ISO, tax, or payroll certification. The service is provided as a workflow and preparation tool; payroll figures are estimates, not final pay or tax figures, and StaffPilot gives no tax or legal advice.</p>
<h2>8. Liability</h2>
<p>To the extent permitted by law, StaffPilot&rsquo;s liability is limited to the subscription fees paid for the service in the period in question. StaffPilot is not liable for payroll, tax, or employment decisions the customer makes on the basis of estimates.</p>
<h2>9. Changes</h2>
<p>We may update these terms as the product develops; the &ldquo;last updated&rdquo; date at the top will change, and material changes will be flagged to customers.</p>
</div></section>
"""
add("terms.html", "Terms of service", "StaffPilot terms of service: subscription software, payroll preparation as estimates only, customer responsibilities, and liability.", TERMS_BODY)

# --- Security ---------------------------------------------------------------
SECURITY_BODY = page_hero("Security information", "Security, stated honestly.",
    "What StaffPilot does to protect your firm&rsquo;s data, what is planned, and what we do not claim.") + """
<section class="block"><div class="wrap">
<div class="callout"><p><strong>No certifications held.</strong> StaffPilot holds no SOC 2, ISO 27001, tax, or payroll certification, and claims none. If a certification is ever obtained, this page will be updated to name it, with the date. Do not take any statement on this page as a certification claim.</p></div>
<h2>What is in place or planned</h2>
<table class="data">
<thead><tr><th>Area</th><th>Status</th><th>Detail</th></tr></thead>
<tbody>
<tr><td>Tenant isolation</td><td><strong>Planned architecture</strong></td><td>Each customer&rsquo;s data lives in its own tenant. Isolation is enforced at the database level with PostgreSQL row-level security (RLS) in the application design, so no customer can see another&rsquo;s data.</td></tr>
<tr><td>Authentication</td><td><strong>Planned / in build</strong></td><td>Sign-in is provided by Supabase Auth in the application. Passwords are handled by that provider, not stored by StaffPilot&rsquo;s own code.</td></tr>
<tr><td>Encryption in transit</td><td><strong>Provided by the platform</strong></td><td>Traffic to the application and website is encrypted with TLS (HTTPS) via the hosting platform.</td></tr>
<tr><td>Encryption at rest</td><td><strong>Provided by the platform</strong></td><td>Database storage encryption is provided by the database hosting platform (Supabase/PostgreSQL).</td></tr>
<tr><td>Role-based access</td><td><strong>Planned / in build</strong></td><td>Owner, recruiter, payroll manager, and client-approver roles, with custom roles on Growth and Scale. Permissions gate what each role can see and do.</td></tr>
<tr><td>Audit trail</td><td><strong>Planned / in build</strong></td><td>Timesheet approvals, rate changes, and payroll-preparation runs are logged with who and when.</td></tr>
<tr><td>Backups</td><td><strong>Provided by the platform</strong></td><td>Database backups are provided by the database hosting platform; restore procedures are part of the application&rsquo;s operations plan.</td></tr>
<tr><td>SOC 2 / ISO 27001</td><td><strong>Not held</strong></td><td>No certification has been obtained. Not claimed, not implied.</td></tr>
</tbody>
</table>
<p class="small muted">Status labels are deliberate: &ldquo;planned / in build&rdquo; means designed and being implemented, not yet independently verified in production. This page will be updated as items move from planned to live and verified.</p>
<h2>What StaffPilot never stores</h2>
<ul class="xlist">
<li>Real Social Security numbers.</li>
<li>Bank routing or account numbers for payroll purposes.</li>
<li>Passwords on the public website &mdash; this site has no sign-in form.</li>
</ul>
<h2>Your part</h2>
<ul class="checklist">
<li>Give each user their own account and the smallest role they need.</li>
<li>Never share passwords, and never send SSNs or bank details to us by email or form.</li>
<li>Tell us promptly if you suspect unauthorized access to your tenant, via the <a href="contact.html">contact page</a>.</li>
</ul>
<h2>Questions</h2>
<p>Security questions: use the <a href="contact.html">contact page</a> and choose &ldquo;Security and data&rdquo; as the topic.</p>
</div></section>
"""
add("security.html", "Security information", "StaffPilot security: tenant isolation, Supabase Auth, encryption, role-based access, and audit trail — with no SOC 2 or ISO certification claimed.", SECURITY_BODY)


def main():
    for slug, title, description, body in PAGES:
        render(slug, title, description, body)
        print("wrote", slug)
    print(f"{len(PAGES)} pages")


if __name__ == "__main__":
    main()
