"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { AlertTriangle, ArrowLeft, Database, Download, Loader2, RefreshCw, Server, ShieldQuestion } from "lucide-react";

import { useRequireAuth } from "@/hooks/use-require-auth";
import { useAuditLogs, useFullHealth, useWebsitePublishLogs } from "@/hooks/use-platform";
import type { SubsystemStatus } from "@/lib/api/platform";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

function formatDateTime(value: string): string {
  return new Date(value).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
}

function statusTone(status: SubsystemStatus["status"]): { badge: "default" | "secondary" | "destructive"; dot: string } {
  if (status === "healthy") return { badge: "default", dot: "bg-emerald-500" };
  if (status === "not_configured") return { badge: "secondary", dot: "bg-slate-400" };
  return { badge: "destructive", dot: "bg-red-500" };
}

function UptimeBadge({ label, icon, subsystem }: { label: string; icon: React.ReactNode; subsystem: SubsystemStatus }) {
  const tone = statusTone(subsystem.status);
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white p-4"
    >
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-600">{icon}</div>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <p className="text-sm font-semibold text-slate-900">{label}</p>
          <span className={`h-1.5 w-1.5 rounded-full ${tone.dot}`} />
        </div>
        <Badge variant={tone.badge} className="mt-1">
          {subsystem.status.replace("_", " ")}
        </Badge>
        {subsystem.latencyMs !== undefined && <p className="mt-1 text-xs text-slate-400">{subsystem.latencyMs}ms</p>}
        {subsystem.pool && (
          <p className="mt-1 text-xs text-slate-400">
            pool {subsystem.pool.checkedOut}/{subsystem.pool.size} in use
          </p>
        )}
        {subsystem.error && <p className="mt-1 truncate text-xs text-red-500" title={subsystem.error}>{subsystem.error}</p>}
      </div>
    </motion.div>
  );
}

function exportAuditLogsToCsv(rows: { createdAt: string; actionType: string; entityType: string; entityId: string; performedBy: string | null; ipAddress: string | null }[]) {
  const header = ["createdAt", "actionType", "entityType", "entityId", "performedBy", "ipAddress"];
  const lines = rows.map((r) =>
    [r.createdAt, r.actionType, r.entityType, r.entityId, r.performedBy ?? "", r.ipAddress ?? ""]
      .map((v) => `"${String(v).replace(/"/g, '""')}"`)
      .join(","),
  );
  const csv = [header.join(","), ...lines].join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `audit-logs-${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export default function SystemHealthPage() {
  const { session, ready } = useRequireAuth();
  const [entityTypeFilter, setEntityTypeFilter] = useState("");
  const [actionTypeFilter, setActionTypeFilter] = useState("");
  const [storeIdLookup, setStoreIdLookup] = useState("");

  const health = useFullHealth();
  const filters = useMemo(
    () => ({ entityType: entityTypeFilter || undefined, actionType: actionTypeFilter || undefined, limit: 50 }),
    [entityTypeFilter, actionTypeFilter],
  );
  const auditLogs = useAuditLogs(filters);
  const publishLogs = useWebsitePublishLogs(storeIdLookup.trim() || null);

  if (!ready) return null;
  const isPlatformRole = session?.role === "platform_owner" || session?.role === "platform_staff";

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">KarobarOne portal</p>
            <h1 className="mt-1 text-xl font-semibold text-slate-950">System Health & Audit</h1>
          </div>
          <Link
            href="/platform-admin-portal"
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
          >
            <ArrowLeft className="size-4" />
            Dashboard
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        {!isPlatformRole ? (
          <div className="flex flex-col items-center gap-3 rounded-3xl border border-amber-200 bg-amber-50 py-16 text-center">
            <AlertTriangle className="h-8 w-8 text-amber-500" />
            <p className="text-sm font-medium text-amber-900">This dashboard is restricted to platform owners and platform staff.</p>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-semibold tracking-tight">Service health</h2>
                <p className="text-sm text-slate-500">Live status, polled every 30 seconds.</p>
              </div>
              <Button variant="outline" size="sm" onClick={() => health.refetch()} disabled={health.isFetching}>
                <RefreshCw className={`h-4 w-4 ${health.isFetching ? "animate-spin" : ""}`} />
                Refresh
              </Button>
            </div>

            {health.isLoading ? (
              <div className="mt-4 grid gap-3 sm:grid-cols-3">
                {[0, 1, 2].map((i) => (
                  <div key={i} className="h-24 animate-pulse rounded-2xl border border-slate-200 bg-slate-100" />
                ))}
              </div>
            ) : health.data ? (
              <div className="mt-4 grid gap-3 sm:grid-cols-3">
                <UptimeBadge label="Database" icon={<Database className="h-5 w-5" />} subsystem={health.data.checks.database} />
                <UptimeBadge label="Redis" icon={<Server className="h-5 w-5" />} subsystem={health.data.checks.redis} />
                <UptimeBadge label="Worker / Celery" icon={<ShieldQuestion className="h-5 w-5" />} subsystem={health.data.checks.worker} />
              </div>
            ) : (
              <p className="mt-4 text-sm text-red-500">Couldn't reach the health endpoint.</p>
            )}

            <section className="mt-8 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
              <h3 className="text-sm font-semibold text-slate-900">Deployment logs</h3>
              <p className="mt-1 text-xs text-slate-500">
                Publish logs are per-store — enter a store ID to view its deployment history.
              </p>
              <div className="mt-3 max-w-sm">
                <Label htmlFor="store-lookup">Store ID (UUID)</Label>
                <Input id="store-lookup" value={storeIdLookup} onChange={(e) => setStoreIdLookup(e.target.value)} className="mt-1.5" />
              </div>

              {storeIdLookup.trim() && (
                <div className="mt-4 overflow-hidden rounded-2xl border border-slate-100">
                  <Table>
                    <TableHeader>
                      <TableRow className="bg-slate-50/80 hover:bg-slate-50/80">
                        <TableHead>Action</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Version</TableHead>
                        <TableHead>When</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {publishLogs.isLoading && (
                        <TableRow>
                          <TableCell colSpan={4} className="py-8 text-center">
                            <Loader2 className="mx-auto h-4 w-4 animate-spin text-slate-400" />
                          </TableCell>
                        </TableRow>
                      )}
                      {!publishLogs.isLoading && (publishLogs.data ?? []).length === 0 && (
                        <TableRow>
                          <TableCell colSpan={4} className="py-8 text-center text-sm text-slate-400">
                            No publish logs for this store yet.
                          </TableCell>
                        </TableRow>
                      )}
                      {(publishLogs.data ?? []).map((log) => (
                        <TableRow key={log.id}>
                          <TableCell className="text-sm text-slate-700">{log.action}</TableCell>
                          <TableCell>
                            <Badge variant={log.status === "SUCCESS" ? "default" : "secondary"}>{log.status}</Badge>
                          </TableCell>
                          <TableCell className="text-sm text-slate-500">{log.version ?? "—"}</TableCell>
                          <TableCell className="text-sm text-slate-500">{formatDateTime(log.createdAt)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}
            </section>

            <section className="mt-8 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <h3 className="text-sm font-semibold text-slate-900">Audit trail</h3>
                <div className="flex flex-wrap items-center gap-2">
                  <Input
                    placeholder="Filter entity type"
                    value={entityTypeFilter}
                    onChange={(e) => setEntityTypeFilter(e.target.value)}
                    className="h-8 w-40"
                  />
                  <Input
                    placeholder="Filter action type"
                    value={actionTypeFilter}
                    onChange={(e) => setActionTypeFilter(e.target.value)}
                    className="h-8 w-40"
                  />
                  <Button
                    size="sm"
                    variant="outline"
                    disabled={!auditLogs.data?.length}
                    onClick={() => auditLogs.data && exportAuditLogsToCsv(auditLogs.data)}
                  >
                    <Download className="h-4 w-4" />
                    Export CSV
                  </Button>
                </div>
              </div>

              <div className="mt-4 overflow-hidden rounded-2xl border border-slate-100">
                <Table>
                  <TableHeader>
                    <TableRow className="bg-slate-50/80 hover:bg-slate-50/80">
                      <TableHead>When</TableHead>
                      <TableHead>Action</TableHead>
                      <TableHead>Entity</TableHead>
                      <TableHead>Performed by</TableHead>
                      <TableHead>IP</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {auditLogs.isLoading && (
                      <TableRow>
                        <TableCell colSpan={5} className="py-10 text-center">
                          <Loader2 className="mx-auto h-4 w-4 animate-spin text-slate-400" />
                        </TableCell>
                      </TableRow>
                    )}
                    {!auditLogs.isLoading && (auditLogs.data ?? []).length === 0 && (
                      <TableRow>
                        <TableCell colSpan={5} className="py-10 text-center text-sm text-slate-400">
                          No audit log entries match these filters.
                        </TableCell>
                      </TableRow>
                    )}
                    {(auditLogs.data ?? []).map((entry, i) => (
                      <motion.tr
                        key={entry.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: Math.min(i, 10) * 0.02 }}
                        className="border-b border-slate-100 last:border-0"
                      >
                        <TableCell className="text-sm text-slate-500">{formatDateTime(entry.createdAt)}</TableCell>
                        <TableCell>
                          <Badge variant="outline">{entry.actionType}</Badge>
                        </TableCell>
                        <TableCell className="text-sm text-slate-700">
                          {entry.entityType}
                          <span className="ml-1 text-xs text-slate-400">{entry.entityId.slice(0, 8)}</span>
                        </TableCell>
                        <TableCell className="text-xs text-slate-500">{entry.performedBy ? entry.performedBy.slice(0, 8) : "—"}</TableCell>
                        <TableCell className="text-xs text-slate-500">{entry.ipAddress ?? "—"}</TableCell>
                      </motion.tr>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}
