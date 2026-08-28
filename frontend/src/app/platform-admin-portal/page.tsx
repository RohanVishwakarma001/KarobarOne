import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export const metadata: Metadata = {
  title: "Platform Admin Portal | KarobarOne",
  description: "Platform admin portal modules, planning, and workflow structure.",
};

export default function PlatformAdminPortalPage() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-200 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">
              KarobarOne portal
            </p>
            <h1 className="mt-1 text-xl font-semibold text-slate-950">Platform Admin Portal</h1>
          </div>

          <Link
            href="/"
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
          >
            <ArrowLeft className="size-4" />
            Home
          </Link>
        </div>
      </header>

      <main>
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
            <p className="text-xs uppercase tracking-[0.24em] text-gray-500">Admin portal</p>
            <h2 className="mt-2 text-3xl font-semibold text-gray-900">Platform Admin Portal</h2>
            <p className="mt-3 text-sm leading-6 text-gray-600">
              Simple admin area for businesses, users, approvals, and payouts.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
