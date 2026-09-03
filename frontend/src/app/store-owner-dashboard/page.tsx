"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Loader2, LogOut, Store as StoreIcon, Zap } from "lucide-react";
import { useRequireAuth } from "@/hooks/use-require-auth";
import { clearSession } from "@/lib/auth/session";
import { ApiError } from "@/lib/api/coreClient";
import { listStores, type StoreResponse } from "@/lib/api/stores";
import { useRouter } from "next/navigation";

const financeLinks = [
  { href: "/store-owner-dashboard/payouts", label: "Seller payouts" },
  { href: "/store-owner-dashboard/settlements", label: "Gateway settlements" },
  { href: "/store-owner-dashboard/reconciliation", label: "Payment reconciliation" },
  { href: "/store-owner-dashboard/revenue", label: "Revenue summary" },
  { href: "/store-owner-dashboard/payment-audit-logs", label: "Payment audit logs" },
  { href: "/store-owner-dashboard/shipping", label: "Shipping" },
];

const comingSoon = [
  "Website theme",
  "Bank accounts",
  "Homepage sections",
  "Website settings",
  "Domains",
  "Media library",
];

export default function StoreOwnerDashboardPage() {
  const router = useRouter();
  const { session, ready } = useRequireAuth();
  const [stores, setStores] = useState<StoreResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!ready || !session) return;
    listStores(session.tenantId ?? undefined)
      .then(setStores)
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load your store."))
      .finally(() => setLoading(false));
  }, [ready, session]);

  const handleLogout = () => {
    clearSession();
    toast.success("Logged out.");
    router.push("/login");
  };

  if (!ready) return null;

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex size-11 items-center justify-center rounded-2xl bg-[#5b4ef9]/10 text-sm font-semibold text-[#5b4ef9]">
              <Zap className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Store owner portal</p>
              <h1 className="text-lg font-semibold text-slate-900">Store Owner Dashboard</h1>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
          >
            <LogOut className="h-4 w-4" />
            Log out
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          {loading && (
            <div className="flex items-center justify-center gap-2 py-16 text-sm text-slate-500">
              <Loader2 className="h-4 w-4 animate-spin" /> Loading your store…
            </div>
          )}

          {!loading && error && <div className="py-16 text-center font-medium text-red-600">{error}</div>}

          {!loading && !error && stores.length === 0 && (
            <div className="py-16 text-center">
              <StoreIcon className="mx-auto h-8 w-8 text-slate-300" />
              <p className="mt-4 font-medium">You haven't created a store yet</p>
              <Link
                href="/onboarding/store"
                className="mt-4 inline-flex items-center gap-2 rounded-full bg-[#5b4ef9] px-5 py-2.5 text-sm font-medium text-white hover:bg-[#4a3ee0]"
              >
                Create your store
              </Link>
            </div>
          )}

          {!loading && !error && stores.length > 0 && (
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Your store</p>
                <h2 className="mt-2 text-3xl font-semibold tracking-tight">{stores[0].storeName}</h2>
                <p className="mt-1 text-sm text-slate-500">karobar.one/{stores[0].storeSlug}</p>
                {stores[0].tagline && <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">{stores[0].tagline}</p>}
              </div>
              <span className="rounded-full bg-[#5b4ef9]/10 px-4 py-2 text-sm font-medium text-[#5b4ef9]">
                {stores[0].approvalStatus}
              </span>
            </div>
          )}
        </section>

        <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Customers</p>
          <h2 className="mt-2 text-2xl font-semibold">Manage your customers</h2>
          <div className="mt-5">
            <Link
              href="/store-owner-dashboard/customers"
              className="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-800 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
            >
              View all customers
            </Link>
          </div>
        </section>

        <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Finance & operations</p>
          <h2 className="mt-2 text-2xl font-semibold">Manage your store</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {financeLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="rounded-2xl border border-slate-200 bg-white p-4 text-sm font-medium text-slate-800 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
              >
                {link.label}
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Coming next</p>
          <h2 className="mt-2 text-2xl font-semibold">Store setup</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {comingSoon.map((label) => (
              <div key={label} className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-4 text-sm font-medium text-slate-400">
                {label}
                <span className="mt-1 block text-xs font-normal text-slate-400">Coming soon</span>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
