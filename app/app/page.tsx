import Link from "next/link";

const FEATURES = [
  {
    title: "Assignments",
    body: "Bill rate, pay rate, and margin on every consultant placement — decimal-safe money math, no floats.",
  },
  {
    title: "Timesheets",
    body: "Draft → submitted → manager-approved → client-approved → locked. Every transition audit-logged.",
  },
  {
    title: "Billing & invoices",
    body: "Invoices generated from approved timesheets. Draft, approved, sent, paid — with overdue tracking.",
  },
  {
    title: "Payroll preparation (estimates only)",
    body: "Payroll runs are clearly-labelled estimates for preparation. StaffPilot never moves real payroll funds, files taxes, or stores real SSNs or bank details.",
  },
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <header className="mb-12">
        <p className="text-sm font-semibold uppercase tracking-widest text-sky-700">
          StaffPilot
        </p>
        <h1 className="mt-2 text-4xl font-bold leading-tight">
          Staffing operations for teams of 20–100 workers.
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-slate-600">
          Staffing workflow, consultant assignments, timesheets, client
          approvals, billing, and payroll preparation — with tenant isolation
          enforced at the database level and every money figure computed in
          exact decimals.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            href="/login"
            className="rounded-lg bg-sky-700 px-5 py-3 font-medium text-white hover:bg-sky-800"
          >
            Sign in
          </Link>
          <Link
            href="/api/health"
            className="rounded-lg border border-slate-300 bg-white px-5 py-3 font-medium hover:bg-slate-100"
          >
            Check API health
          </Link>
        </div>
      </header>

      <section className="grid gap-4 sm:grid-cols-2">
        {FEATURES.map((f) => (
          <article
            key={f.title}
            className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
          >
            <h2 className="text-lg font-semibold">{f.title}</h2>
            <p className="mt-2 text-slate-600">{f.body}</p>
          </article>
        ))}
      </section>

      <footer className="mt-12 rounded-xl border border-amber-200 bg-amber-50 p-6 text-sm text-amber-900">
        <strong>Boundary notice.</strong> StaffPilot is payroll{" "}
        <em>preparation</em> only. All payroll figures shown are estimates.
        StaffPilot never processes real payroll funds, direct deposits, tax
        filings, or tax deposits, never stores real SSNs or bank account
        details, and claims no payroll or tax certification. Demo data in this
        repository is synthetic.
      </footer>
    </main>
  );
}
