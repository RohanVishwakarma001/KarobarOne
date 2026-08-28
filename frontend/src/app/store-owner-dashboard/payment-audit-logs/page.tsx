"use client";

import { useEffect, useState } from "react";
import { Loader2, ScrollText } from "lucide-react";
import { AdminShell } from "@/components/commerce/AdminShell";
import { ApiError, type PaymentAuditLog, listPaymentAuditLogs } from "@/lib/api/github";

const dateFmt = (iso: string) => new Date(iso).toLocaleString("en-IN");

export default function PaymentAuditLogsPage() {
  const [logs, setLogs] = useState<PaymentAuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    listPaymentAuditLogs()
      .then((all) => setLogs(all.sort((a, b) => b.created_at.localeCompare(a.created_at))))
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load audit logs."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <AdminShell title="Payment Audit Logs" badge="AL">
      <p className="mb-5 text-sm text-slate-600">
        A read-only trail of changes made to payment records — system-generated, not editable here.
      </p>

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
        {loading && (
          <div className="flex items-center justify-center gap-2 px-6 py-16 text-sm text-slate-500">
            <Loader2 className="h-4 w-4 animate-spin" /> Loading audit logs…
          </div>
        )}
        {!loading && error && <div className="px-6 py-16 text-center font-medium text-red-600">{error}</div>}
        {!loading && !error && logs.length === 0 && (
          <div className="px-6 py-16 text-center">
            <ScrollText className="mx-auto h-8 w-8 text-slate-300" />
            <p className="mt-4 font-medium">No audit log entries yet</p>
          </div>
        )}
        {!loading && !error && logs.length > 0 && (
          <div className="divide-y divide-slate-100">
            {logs.map((log) => (
              <div key={log.id} className="p-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p className="text-sm font-medium text-slate-900">{log.action_type}</p>
                    <p className="mt-1 text-xs text-slate-500">
                      Payment {log.payment_id.slice(0, 8)} · performed by {log.performed_by.slice(0, 8)} · {dateFmt(log.created_at)}
                    </p>
                  </div>
                  {(log.old_value || log.new_value) && (
                    <button
                      onClick={() => setExpanded(expanded === log.id ? null : log.id)}
                      className="text-sm font-medium text-[#5b4ef9] hover:underline"
                    >
                      {expanded === log.id ? "Hide details" : "View details"}
                    </button>
                  )}
                </div>
                {expanded === log.id && (
                  <div className="mt-3 grid gap-3 sm:grid-cols-2">
                    {log.old_value && (
                      <pre className="overflow-x-auto rounded-lg bg-slate-50 p-3 text-xs text-slate-700">{JSON.stringify(log.old_value, null, 2)}</pre>
                    )}
                    {log.new_value && (
                      <pre className="overflow-x-auto rounded-lg bg-slate-50 p-3 text-xs text-slate-700">{JSON.stringify(log.new_value, null, 2)}</pre>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </AdminShell>
  );
}
