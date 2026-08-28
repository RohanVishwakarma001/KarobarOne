"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Loader2, Plus, Landmark } from "lucide-react";
import { AdminShell } from "@/components/commerce/AdminShell";
import {
  ApiError,
  type GatewaySettlement,
  type GatewaySettlementItem,
  createGatewaySettlement,
  listGatewaySettlements,
  updateGatewaySettlement,
  listGatewaySettlementItems,
} from "@/lib/api/github";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;
const SETTLEMENT_STATUSES = ["PENDING", "PROCESSING", "SETTLED", "FAILED"] as const;

const statusClass = (s: string) =>
  s === "SETTLED" ? "bg-green-50 text-green-700" : s === "FAILED" ? "bg-red-50 text-red-700" : s === "PROCESSING" ? "bg-blue-50 text-blue-700" : "bg-amber-50 text-amber-700";

export default function SettlementsPage() {
  const [settlements, setSettlements] = useState<GatewaySettlement[]>([]);
  const [items, setItems] = useState<GatewaySettlementItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);

  const [reference, setReference] = useState("");
  const [gatewayName, setGatewayName] = useState("");
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState("");

  const load = () => {
    setLoading(true);
    setError(null);
    Promise.all([listGatewaySettlements(), listGatewaySettlementItems()])
      .then(([s, i]) => {
        setSettlements(s.sort((a, b) => b.created_at.localeCompare(a.created_at)));
        setItems(i);
      })
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load settlements."))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!reference.trim() || !gatewayName.trim() || !amount || !date) {
      toast.error("Reference, gateway, amount, and date are required.");
      return;
    }
    setSaving(true);
    try {
      await createGatewaySettlement({ settlement_reference: reference.trim(), gateway_name: gatewayName.trim(), settlement_amount: Number(amount), settlement_date: date });
      toast.success("Settlement created.");
      setReference("");
      setGatewayName("");
      setAmount("");
      setDate("");
      setShowForm(false);
      load();
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not create settlement.");
    } finally {
      setSaving(false);
    }
  }

  async function cycleStatus(settlement: GatewaySettlement) {
    const idx = SETTLEMENT_STATUSES.indexOf(settlement.settlement_status as (typeof SETTLEMENT_STATUSES)[number]);
    const next = SETTLEMENT_STATUSES[(idx + 1) % SETTLEMENT_STATUSES.length];
    setBusyId(settlement.id);
    try {
      const updated = await updateGatewaySettlement(settlement.id, { settlement_status: next });
      setSettlements((prev) => prev.map((s) => (s.id === settlement.id ? updated : s)));
      toast.success(`Settlement marked ${next}.`);
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not update settlement status.");
    } finally {
      setBusyId(null);
    }
  }

  const visibleItems = selected ? items.filter((i) => i.settlement_id === selected) : items;

  return (
    <AdminShell title="Gateway Settlements" badge="ST">
      <div className="mb-5 flex items-center justify-between gap-3">
        <p className="text-sm text-slate-600">Payment-gateway settlement batches and their line items.</p>
        <button onClick={() => setShowForm((v) => !v)} className="inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white hover:bg-[#4a3ee0]">
          <Plus className="h-4 w-4" /> New settlement
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="mb-6 grid gap-3 rounded-2xl border border-slate-200 bg-white p-5 sm:grid-cols-2 lg:grid-cols-4">
          <input className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Settlement reference" value={reference} onChange={(e) => setReference(e.target.value)} />
          <input className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Gateway name (e.g. Razorpay)" value={gatewayName} onChange={(e) => setGatewayName(e.target.value)} />
          <input type="number" step="0.01" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" placeholder="Amount" value={amount} onChange={(e) => setAmount(e.target.value)} />
          <input type="date" className="rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]" value={date} onChange={(e) => setDate(e.target.value)} />
          <div className="flex gap-2 sm:col-span-2 lg:col-span-4">
            <button disabled={saving} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
              {saving ? "Saving…" : "Create settlement"}
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
            <Loader2 className="h-4 w-4 animate-spin" /> Loading settlements…
          </div>
        )}
        {!loading && error && <div className="px-6 py-16 text-center font-medium text-red-600">{error}</div>}
        {!loading && !error && settlements.length === 0 && (
          <div className="px-6 py-16 text-center">
            <Landmark className="mx-auto h-8 w-8 text-slate-300" />
            <p className="mt-4 font-medium">No settlements yet</p>
          </div>
        )}
        {!loading && !error && settlements.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  {["Reference", "Gateway", "Amount", "Date", "Status", ""].map((h) => (
                    <th key={h} className="border-b border-slate-200 px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {settlements.map((s) => (
                  <tr key={s.id} onClick={() => setSelected(s.id === selected ? null : s.id)} className={`cursor-pointer hover:bg-slate-50/70 ${selected === s.id ? "bg-[#5b4ef9]/5" : ""}`}>
                    <td className="px-5 py-3 text-sm font-medium">{s.settlement_reference}</td>
                    <td className="px-5 py-3 text-sm text-slate-600">{s.gateway_name}</td>
                    <td className="px-5 py-3 text-sm font-medium">{money(s.settlement_amount)}</td>
                    <td className="px-5 py-3 text-sm text-slate-600">{new Date(s.settlement_date).toLocaleDateString("en-IN")}</td>
                    <td className="px-5 py-3">
                      <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(s.settlement_status)}`}>{s.settlement_status}</span>
                    </td>
                    <td className="px-5 py-3">
                      <button
                        disabled={busyId === s.id}
                        onClick={(e) => {
                          e.stopPropagation();
                          cycleStatus(s);
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
            <p className="text-sm font-medium text-slate-900">
              Settlement items {selected ? "for selected settlement" : "(all)"}
            </p>
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
                    {["Payment", "Settlement amount", "Fee", "Tax"].map((h) => (
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
                      <td className="px-5 py-3 text-sm">{money(i.settlement_amount)}</td>
                      <td className="px-5 py-3 text-sm text-slate-600">{money(i.fee_amount)}</td>
                      <td className="px-5 py-3 text-sm text-slate-600">{money(i.tax_amount)}</td>
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
