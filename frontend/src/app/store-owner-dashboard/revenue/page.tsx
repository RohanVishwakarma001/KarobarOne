"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Loader2, Plus, TrendingUp, Calculator } from "lucide-react";
import { AdminShell } from "@/components/commerce/AdminShell";
import { ApiError, type RevenueSummary, type CommissionResult, createRevenueSummary, listRevenueSummaries, calculateCommission } from "@/lib/api/github";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;

export default function RevenuePage() {
  const [summaries, setSummaries] = useState<RevenueSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);

  const [reportMonth, setReportMonth] = useState("");
  const [subscriptionRevenue, setSubscriptionRevenue] = useState("0");
  const [commissionRevenue, setCommissionRevenue] = useState("0");
  const [totalRevenue, setTotalRevenue] = useState("0");

  const [commOrderId, setCommOrderId] = useState("");
  const [commAmount, setCommAmount] = useState("");
  const [commPercentage, setCommPercentage] = useState("");
  const [commResult, setCommResult] = useState<CommissionResult | null>(null);
  const [commBusy, setCommBusy] = useState(false);

  const load = () => {
    setLoading(true);
    setError(null);
    listRevenueSummaries()
      .then((all) => setSummaries(all.sort((a, b) => b.report_month.localeCompare(a.report_month))))
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load revenue summaries."))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!reportMonth) {
      toast.error("Report month is required.");
      return;
    }
    setSaving(true);
    try {
      await createRevenueSummary({
        report_month: reportMonth,
        subscription_revenue: Number(subscriptionRevenue) || 0,
        commission_revenue: Number(commissionRevenue) || 0,
        total_revenue: Number(totalRevenue) || 0,
      });
      toast.success("Revenue summary recorded.");
      setReportMonth("");
      setSubscriptionRevenue("0");
      setCommissionRevenue("0");
      setTotalRevenue("0");
      setShowForm(false);
      load();
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not record revenue summary.");
    } finally {
      setSaving(false);
    }
  }

  async function handleCalculate(e: React.FormEvent) {
    e.preventDefault();
    if (!commOrderId.trim() || !commAmount || !commPercentage) {
      toast.error("Order ID, amount, and commission % are required.");
      return;
    }
    setCommBusy(true);
    setCommResult(null);
    try {
      const result = await calculateCommission({ order_id: commOrderId.trim(), order_amount: Number(commAmount), commission_percentage: Number(commPercentage) });
      setCommResult(result);
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not calculate commission.");
    } finally {
      setCommBusy(false);
    }
  }

  const totals = summaries.reduce(
    (acc, s) => ({
      total: acc.total + s.total_revenue,
      subscription: acc.subscription + s.subscription_revenue,
      commission: acc.commission + s.commission_revenue,
    }),
    { total: 0, subscription: 0, commission: 0 }
  );

  return (
    <AdminShell title="Revenue Summary" badge="RV">
      {!loading && !error && (
        <div className="mb-6 grid gap-3 sm:grid-cols-3">
          {[
            { label: "Total revenue", value: totals.total },
            { label: "Subscription revenue", value: totals.subscription },
            { label: "Commission revenue", value: totals.commission },
          ].map((t) => (
            <div key={t.label} className="rounded-2xl border border-slate-200 bg-white p-5">
              <p className="flex items-center gap-2 text-xs uppercase tracking-wider text-slate-500">
                <TrendingUp className="h-3.5 w-3.5" /> {t.label}
              </p>
              <p className="mt-2 text-2xl font-semibold text-slate-900">{money(t.value)}</p>
            </div>
          ))}
        </div>
      )}

      <div className="mb-6 rounded-2xl border border-slate-200 bg-white p-5">
        <p className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-900">
          <Calculator className="h-4 w-4 text-[#5b4ef9]" /> Commission calculator
        </p>
        <p className="mb-3 text-xs text-slate-500">Stateless — computes commission/seller split for an order, does not save anything.</p>
        <form onSubmit={handleCalculate} className="grid gap-3 sm:grid-cols-4">
          <input className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Order ID (UUID)" value={commOrderId} onChange={(e) => setCommOrderId(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Order amount" value={commAmount} onChange={(e) => setCommAmount(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Commission %" value={commPercentage} onChange={(e) => setCommPercentage(e.target.value)} />
          <button disabled={commBusy} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
            {commBusy ? "Calculating…" : "Calculate"}
          </button>
        </form>
        {commResult && (
          <div className="mt-4 grid gap-3 rounded-xl bg-slate-50 p-4 sm:grid-cols-2">
            <p className="text-sm text-slate-700">
              Commission amount: <span className="font-semibold text-slate-900">{money(commResult.commission_amount)}</span>
            </p>
            <p className="text-sm text-slate-700">
              Seller amount: <span className="font-semibold text-slate-900">{money(commResult.seller_amount)}</span>
            </p>
          </div>
        )}
      </div>

      <div className="mb-5 flex items-center justify-between gap-3">
        <p className="text-sm text-slate-600">Monthly revenue summaries (subscription + commission).</p>
        <button onClick={() => setShowForm((v) => !v)} className="inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white hover:bg-[#4a3ee0]">
          <Plus className="h-4 w-4" /> New summary
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="mb-6 grid gap-3 rounded-2xl border border-slate-200 bg-white p-5 sm:grid-cols-2 lg:grid-cols-4">
          <input type="date" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" value={reportMonth} onChange={(e) => setReportMonth(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Subscription revenue" value={subscriptionRevenue} onChange={(e) => setSubscriptionRevenue(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Commission revenue" value={commissionRevenue} onChange={(e) => setCommissionRevenue(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Total revenue" value={totalRevenue} onChange={(e) => setTotalRevenue(e.target.value)} />
          <div className="flex gap-2 sm:col-span-2 lg:col-span-4">
            <button disabled={saving} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
              {saving ? "Saving…" : "Record summary"}
            </button>
            <button type="button" onClick={() => setShowForm(false)} className="rounded-lg px-4 py-2 text-sm text-slate-500">
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
        {loading && (
          <div className="flex items-center justify-center gap-2 px-6 py-16 text-sm text-slate-500">
            <Loader2 className="h-4 w-4 animate-spin" /> Loading revenue summaries…
          </div>
        )}
        {!loading && error && <div className="px-6 py-16 text-center font-medium text-red-600">{error}</div>}
        {!loading && !error && summaries.length === 0 && <div className="px-6 py-16 text-center text-sm text-slate-500">No revenue summaries recorded yet.</div>}
        {!loading && !error && summaries.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  {["Month", "Subscription", "Commission", "Total"].map((h) => (
                    <th key={h} className="border-b border-slate-200 px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {summaries.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-50/70">
                    <td className="px-5 py-3 text-sm font-medium">{new Date(s.report_month).toLocaleDateString("en-IN", { year: "numeric", month: "long" })}</td>
                    <td className="px-5 py-3 text-sm text-slate-600">{money(s.subscription_revenue)}</td>
                    <td className="px-5 py-3 text-sm text-slate-600">{money(s.commission_revenue)}</td>
                    <td className="px-5 py-3 text-sm font-semibold">{money(s.total_revenue)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </AdminShell>
  );
}
