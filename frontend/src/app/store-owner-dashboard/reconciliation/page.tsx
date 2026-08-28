"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Loader2, Plus, ListChecks } from "lucide-react";
import { AdminShell } from "@/components/commerce/AdminShell";
import {
  ApiError,
  type PaymentReconciliationBatch,
  type PaymentReconciliationItem,
  createReconciliationBatch,
  listReconciliationBatches,
  updateReconciliationBatch,
  listReconciliationItems,
} from "@/lib/api/github";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;
const BATCH_STATUSES = ["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"] as const;

const statusClass = (s: string) =>
  s === "COMPLETED" ? "bg-green-50 text-green-700" : s === "FAILED" ? "bg-red-50 text-red-700" : s === "IN_PROGRESS" ? "bg-blue-50 text-blue-700" : "bg-amber-50 text-amber-700";

export default function ReconciliationPage() {
  const [batches, setBatches] = useState<PaymentReconciliationBatch[]>([]);
  const [items, setItems] = useState<PaymentReconciliationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);

  const [batchNumber, setBatchNumber] = useState("");
  const [reconciliationDate, setReconciliationDate] = useState("");
  const [totalPayments, setTotalPayments] = useState("0");
  const [totalAmount, setTotalAmount] = useState("0");

  const load = () => {
    setLoading(true);
    setError(null);
    Promise.all([listReconciliationBatches(), listReconciliationItems()])
      .then(([b, i]) => {
        setBatches(b.sort((a, b2) => b2.created_at.localeCompare(a.created_at)));
        setItems(i);
      })
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load reconciliation batches."))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!batchNumber.trim() || !reconciliationDate) {
      toast.error("Batch number and date are required.");
      return;
    }
    setSaving(true);
    try {
      await createReconciliationBatch({
        batch_number: batchNumber.trim(),
        reconciliation_date: reconciliationDate,
        total_payments: Number(totalPayments) || 0,
        total_amount: Number(totalAmount) || 0,
      });
      toast.success("Reconciliation batch created.");
      setBatchNumber("");
      setReconciliationDate("");
      setTotalPayments("0");
      setTotalAmount("0");
      setShowForm(false);
      load();
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not create batch.");
    } finally {
      setSaving(false);
    }
  }

  async function cycleStatus(batch: PaymentReconciliationBatch) {
    const idx = BATCH_STATUSES.indexOf(batch.status as (typeof BATCH_STATUSES)[number]);
    const next = BATCH_STATUSES[(idx + 1) % BATCH_STATUSES.length];
    setBusyId(batch.id);
    try {
      const updated = await updateReconciliationBatch(batch.id, { status: next });
      setBatches((prev) => prev.map((b) => (b.id === batch.id ? updated : b)));
      toast.success(`Batch marked ${next}.`);
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not update batch status.");
    } finally {
      setBusyId(null);
    }
  }

  const visibleItems = selected ? items.filter((i) => i.batch_id === selected) : items;

  return (
    <AdminShell title="Payment Reconciliation" badge="RC">
      <div className="mb-5 flex items-center justify-between gap-3">
        <p className="text-sm text-slate-600">Reconciliation batches matching payments against gateway records.</p>
        <button onClick={() => setShowForm((v) => !v)} className="inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white hover:bg-[#4a3ee0]">
          <Plus className="h-4 w-4" /> New batch
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="mb-6 grid gap-3 rounded-2xl border border-slate-200 bg-white p-5 sm:grid-cols-2 lg:grid-cols-4">
          <input className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Batch number" value={batchNumber} onChange={(e) => setBatchNumber(e.target.value)} />
          <input type="date" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" value={reconciliationDate} onChange={(e) => setReconciliationDate(e.target.value)} />
          <input type="number" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Total payments" value={totalPayments} onChange={(e) => setTotalPayments(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Total amount" value={totalAmount} onChange={(e) => setTotalAmount(e.target.value)} />
          <div className="flex gap-2 sm:col-span-2 lg:col-span-4">
            <button disabled={saving} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
              {saving ? "Saving…" : "Create batch"}
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
            <Loader2 className="h-4 w-4 animate-spin" /> Loading batches…
          </div>
        )}
        {!loading && error && <div className="px-6 py-16 text-center font-medium text-red-600">{error}</div>}
        {!loading && !error && batches.length === 0 && (
          <div className="px-6 py-16 text-center">
            <ListChecks className="mx-auto h-8 w-8 text-slate-300" />
            <p className="mt-4 font-medium">No reconciliation batches yet</p>
          </div>
        )}
        {!loading && !error && batches.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  {["Batch", "Date", "Payments", "Amount", "Status", ""].map((h) => (
                    <th key={h} className="border-b border-slate-200 px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {batches.map((b) => (
                  <tr key={b.id} onClick={() => setSelected(b.id === selected ? null : b.id)} className={`cursor-pointer hover:bg-slate-50/70 ${selected === b.id ? "bg-[#5b4ef9]/5" : ""}`}>
                    <td className="px-5 py-3 text-sm font-medium">{b.batch_number}</td>
                    <td className="px-5 py-3 text-sm text-slate-600">{new Date(b.reconciliation_date).toLocaleDateString("en-IN")}</td>
                    <td className="px-5 py-3 text-sm text-slate-600">{b.total_payments}</td>
                    <td className="px-5 py-3 text-sm font-medium">{money(b.total_amount)}</td>
                    <td className="px-5 py-3">
                      <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(b.status)}`}>{b.status}</span>
                    </td>
                    <td className="px-5 py-3">
                      <button
                        disabled={busyId === b.id}
                        onClick={(e) => {
                          e.stopPropagation();
                          cycleStatus(b);
                        }}
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

      {!loading && !error && (
        <div className="mt-6 overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <div className="border-b border-slate-200 px-5 py-3">
            <p className="text-sm font-medium text-slate-900">Reconciliation items {selected ? "for selected batch" : "(all)"}</p>
            {selected && (
              <button onClick={() => setSelected(null)} className="mt-1 text-xs font-medium text-[#5b4ef9] hover:underline">
                Clear filter
              </button>
            )}
          </div>
          {visibleItems.length === 0 ? (
            <div className="px-6 py-10 text-center text-sm text-slate-500">No items to show.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50">
                  <tr>
                    {["Payment", "Gateway payment ID", "Status", "Notes"].map((h) => (
                      <th key={h} className="border-b border-slate-200 px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {visibleItems.map((i) => (
                    <tr key={i.id}>
                      <td className="px-5 py-3 text-sm text-slate-600">{i.payment_id.slice(0, 8)}</td>
                      <td className="px-5 py-3 text-sm text-slate-600">{i.gateway_payment_id ?? "—"}</td>
                      <td className="px-5 py-3 text-sm">{i.reconciliation_status}</td>
                      <td className="px-5 py-3 text-sm text-slate-600">{i.notes ?? "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </AdminShell>
  );
}
