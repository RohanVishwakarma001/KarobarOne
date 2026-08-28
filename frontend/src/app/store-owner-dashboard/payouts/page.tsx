"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Loader2, Plus, Wallet } from "lucide-react";
import { AdminShell } from "@/components/commerce/AdminShell";
import { ApiError, type SellerPayout, createSellerPayout, listSellerPayouts, updateSellerPayout } from "@/lib/api/github";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;
const PAYOUT_STATUSES = ["PENDING", "PROCESSING", "PAID", "FAILED"] as const;

const statusClass = (s: string) =>
  s === "PAID" ? "bg-green-50 text-green-700" : s === "FAILED" ? "bg-red-50 text-red-700" : s === "PROCESSING" ? "bg-blue-50 text-blue-700" : "bg-amber-50 text-amber-700";

export default function PayoutsPage() {
  const [payouts, setPayouts] = useState<SellerPayout[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [busyId, setBusyId] = useState<string | null>(null);

  const [paymentId, setPaymentId] = useState("");
  const [payoutReference, setPayoutReference] = useState("");
  const [grossAmount, setGrossAmount] = useState("");
  const [gatewayFee, setGatewayFee] = useState("0");
  const [gatewayTax, setGatewayTax] = useState("0");
  const [platformCommission, setPlatformCommission] = useState("0");
  const [netPayoutAmount, setNetPayoutAmount] = useState("");

  const load = () => {
    setLoading(true);
    setError(null);
    listSellerPayouts()
      .then((all) => setPayouts(all.sort((a, b) => b.created_at.localeCompare(a.created_at))))
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load payouts."))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!paymentId.trim() || !grossAmount || !netPayoutAmount) {
      toast.error("Payment ID, gross amount, and net payout amount are required.");
      return;
    }
    setSaving(true);
    try {
      await createSellerPayout({
        payment_id: paymentId.trim(),
        gross_amount: Number(grossAmount),
        net_payout_amount: Number(netPayoutAmount),
        gateway_fee: Number(gatewayFee) || 0,
        gateway_tax: Number(gatewayTax) || 0,
        platform_commission: Number(platformCommission) || 0,
        payout_reference: payoutReference.trim() || undefined,
      });
      toast.success("Payout record created.");
      setPaymentId("");
      setPayoutReference("");
      setGrossAmount("");
      setGatewayFee("0");
      setGatewayTax("0");
      setPlatformCommission("0");
      setNetPayoutAmount("");
      setShowForm(false);
      load();
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not create payout.");
    } finally {
      setSaving(false);
    }
  }

  async function cycleStatus(payout: SellerPayout) {
    const idx = PAYOUT_STATUSES.indexOf(payout.payout_status as (typeof PAYOUT_STATUSES)[number]);
    const next = PAYOUT_STATUSES[(idx + 1) % PAYOUT_STATUSES.length];
    setBusyId(payout.id);
    try {
      const updated = await updateSellerPayout(payout.id, { payout_status: next, payout_date: next === "PAID" ? new Date().toISOString() : payout.payout_date ?? undefined });
      setPayouts((prev) => prev.map((p) => (p.id === payout.id ? updated : p)));
      toast.success(`Payout marked ${next}.`);
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not update payout status.");
    } finally {
      setBusyId(null);
    }
  }

  return (
    <AdminShell title="Seller Payouts" badge="PY">
      <div className="mb-5 flex items-center justify-between gap-3">
        <p className="text-sm text-slate-600">Track and release payouts to sellers for settled payments.</p>
        <button
          onClick={() => setShowForm((v) => !v)}
          className="inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white hover:bg-[#4a3ee0]"
        >
          <Plus className="h-4 w-4" /> New payout
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="mb-6 grid gap-3 rounded-2xl border border-slate-200 bg-white p-5 sm:grid-cols-2 lg:grid-cols-3">
          <input className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Payment ID (UUID)" value={paymentId} onChange={(e) => setPaymentId(e.target.value)} />
          <input className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Payout reference" value={payoutReference} onChange={(e) => setPayoutReference(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Gross amount" value={grossAmount} onChange={(e) => setGrossAmount(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Gateway fee" value={gatewayFee} onChange={(e) => setGatewayFee(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Gateway tax" value={gatewayTax} onChange={(e) => setGatewayTax(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Platform commission" value={platformCommission} onChange={(e) => setPlatformCommission(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Net payout amount" value={netPayoutAmount} onChange={(e) => setNetPayoutAmount(e.target.value)} />
          <div className="flex gap-2 sm:col-span-2 lg:col-span-3">
            <button disabled={saving} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
              {saving ? "Saving…" : "Create payout"}
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
            <Loader2 className="h-4 w-4 animate-spin" /> Loading payouts…
          </div>
        )}
        {!loading && error && <div className="px-6 py-16 text-center font-medium text-red-600">{error}</div>}
        {!loading && !error && payouts.length === 0 && (
          <div className="px-6 py-16 text-center">
            <Wallet className="mx-auto h-8 w-8 text-slate-300" />
            <p className="mt-4 font-medium">No payouts yet</p>
          </div>
        )}
        {!loading && !error && payouts.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  {["Reference", "Payment", "Gross", "Net payout", "Status", "Payout date", ""].map((h) => (
                    <th key={h} className="border-b border-slate-200 px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {payouts.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50/70">
                    <td className="px-5 py-3 text-sm font-medium">{p.payout_reference ?? "—"}</td>
                    <td className="px-5 py-3 text-sm text-slate-600">{p.payment_id.slice(0, 8)}</td>
                    <td className="px-5 py-3 text-sm">{money(p.gross_amount)}</td>
                    <td className="px-5 py-3 text-sm font-medium">{money(p.net_payout_amount)}</td>
                    <td className="px-5 py-3">
                      <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(p.payout_status)}`}>{p.payout_status}</span>
                    </td>
                    <td className="px-5 py-3 text-sm text-slate-600">{p.payout_date ? new Date(p.payout_date).toLocaleDateString("en-IN") : "—"}</td>
                    <td className="px-5 py-3">
                      <button
                        disabled={busyId === p.id}
                        onClick={() => cycleStatus(p)}
                        className="text-sm font-medium text-[#5b4ef9] hover:underline disabled:opacity-40"
                      >
                        Advance status
                      </button>
                    </td>
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
