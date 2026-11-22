"use client";

export default function LoginPage() {
  const supabaseConfigured = Boolean(
    process.env.NEXT_PUBLIC_SUPABASE_URL &&
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  );

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-6 py-16">
      <h1 className="text-3xl font-bold">Sign in to StaffPilot</h1>
      <p className="mt-3 text-slate-600">
        Authentication is provided by Supabase Auth. Sign-in is not yet wired
        to a live Supabase project in this scaffold.
      </p>

      <div
        className={`mt-6 rounded-xl border p-5 text-sm ${
          supabaseConfigured
            ? "border-emerald-200 bg-emerald-50 text-emerald-900"
            : "border-amber-200 bg-amber-50 text-amber-900"
        }`}
      >
        {supabaseConfigured ? (
          <>
            <strong>Supabase env vars detected.</strong> The sign-in form
            (email + magic link / password via Supabase Auth) is the next
            implementation step — see <code>app/login/page.tsx</code> and{" "}
            <code>docs/ARCHITECTURE.md</code>.
          </>
        ) : (
          <>
            <strong>Supabase is not configured yet.</strong> To enable
            sign-in:
            <ol className="mt-2 list-decimal space-y-1 pl-5">
              <li>Create a free project at supabase.com.</li>
              <li>
                Copy <code>.env.example</code> to <code>.env.local</code> and
                fill in <code>NEXT_PUBLIC_SUPABASE_URL</code> and{" "}
                <code>NEXT_PUBLIC_SUPABASE_ANON_KEY</code>.
              </li>
              <li>
                Run the migrations in <code>supabase/migrations/</code>{" "}
                against that project.
              </li>
              <li>Restart the dev server and return to this page.</li>
            </ol>
          </>
        )}
      </div>

      <form
        className="mt-6 space-y-4"
        onSubmit={(e) => e.preventDefault()}
        aria-label="Sign-in form (placeholder)"
      >
        <label className="block">
          <span className="text-sm font-medium">Work email</span>
          <input
            type="email"
            required
            placeholder="you@company.com"
            disabled={!supabaseConfigured}
            className="mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 disabled:bg-slate-100"
          />
        </label>
        <button
          type="submit"
          disabled={!supabaseConfigured}
          className="w-full rounded-lg bg-sky-700 px-5 py-3 font-medium text-white hover:bg-sky-800 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {supabaseConfigured
            ? "Email me a sign-in link (coming soon)"
            : "Sign-in disabled — configure Supabase first"}
        </button>
      </form>
      <p className="mt-4 text-xs text-slate-500">
        No account is created and no credentials are sent anywhere from this
        page until Supabase Auth is configured.
      </p>
    </main>
  );
}
