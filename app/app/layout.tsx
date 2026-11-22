import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "StaffPilot — Staffing operations, done right",
  description:
    "Staffing workflow, consultant assignments, timesheets, client approvals, billing, and payroll preparation (estimates only) for teams of 20–100 workers.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        {children}
      </body>
    </html>
  );
}
