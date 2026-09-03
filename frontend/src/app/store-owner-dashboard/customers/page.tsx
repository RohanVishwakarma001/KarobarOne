"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { AnimatePresence, motion } from "framer-motion";
import { AlertTriangle, ChevronLeft, ChevronRight, Loader2, Search, UserPlus, Users } from "lucide-react";

import { useRequireAuth } from "@/hooks/use-require-auth";
import { useCustomers } from "@/hooks/use-customers";
import { listStores } from "@/lib/api/stores";
import type { CustomerResponse } from "@/lib/api/customers";
import { CustomerStatusBadge } from "@/components/customers/status-badge";
import { StatusFilterTabs, type StatusFilterValue } from "@/components/customers/status-filter-tabs";
import { CustomersTableSkeletonRows } from "@/components/customers/customers-table-skeleton";
import { CreateCustomerDialog } from "@/components/customers/create-customer-dialog";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";

const PAGE_SIZE = 20;

function formatDate(value: string | null): string {
  if (!value) return "—";
  return new Date(value).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

function StatCard({ label, value, accent, delay }: { label: string; value: number; accent: string; delay: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.3 }}
      whileHover={{ scale: 1.02, boxShadow: "0 12px 32px -8px rgba(91,78,249,0.25)" }}
      className="rounded-2xl border border-slate-200 bg-white p-4"
    >
      <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">{label}</p>
      <p className={`mt-2 text-2xl font-semibold ${accent}`}>{value.toLocaleString("en-IN")}</p>
    </motion.div>
  );
}

export default function CustomersPage() {
  const { session, ready } = useRequireAuth();
  const [statusFilter, setStatusFilter] = useState<StatusFilterValue>("ALL");
  const [guestOnly, setGuestOnly] = useState(false);
  const [page, setPage] = useState(1);
  const [createOpen, setCreateOpen] = useState(false);

  const tenantId = session?.tenantId ?? "";

  const { data: stores } = useQuery({
    queryKey: ["stores", tenantId],
    queryFn: () => listStores(tenantId),
    enabled: ready && Boolean(tenantId),
  });
  const storeId = stores?.[0]?.id;

  const filters = useMemo(
    () => ({
      page,
      pageSize: PAGE_SIZE,
      status: statusFilter === "ALL" ? undefined : statusFilter,
      isGuestCustomer: guestOnly ? true : undefined,
    }),
    [page, statusFilter, guestOnly],
  );

  const { data, isLoading, isFetching, isError, error, refetch } = useCustomers(tenantId, filters);

  const totalPages = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1;
  const customers = useMemo(() => data?.data ?? [], [data?.data]);
  const statCounts = useMemo(() => {
    const active = customers.filter((c) => c.status === "ACTIVE").length;
    const guests = customers.filter((c) => c.isGuestCustomer).length;
    return { total: data?.total ?? 0, active, guests };
  }, [customers, data?.total]);

  if (!ready) return null;

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <Link
              href="/store-owner-dashboard"
              className="text-xs font-medium uppercase tracking-[0.24em] text-slate-500 hover:text-[#5b4ef9]"
            >
              ← Store owner portal
            </Link>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <div className="flex flex-col gap-1">
          <h1 className="text-3xl font-semibold tracking-tight">Customers</h1>
          <p className="text-sm text-slate-500">Everyone who has an account or has checked out from your store.</p>
        </div>

        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
          <StatCard label="Total customers" value={statCounts.total} accent="text-slate-900" delay={0} />
          <StatCard label="Active (this page)" value={statCounts.active} accent="text-emerald-600" delay={0.05} />
          <StatCard label="Guests (this page)" value={statCounts.guests} accent="text-[#5b4ef9]" delay={0.1} />
        </div>

        <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <StatusFilterTabs
              value={statusFilter}
              onChange={(v) => {
                setStatusFilter(v);
                setPage(1);
              }}
            />
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 text-sm text-slate-600">
                <Switch
                  checked={guestOnly}
                  onCheckedChange={(checked) => {
                    setGuestOnly(checked);
                    setPage(1);
                  }}
                />
                Guests only
              </label>
              <Button
                onClick={() => setCreateOpen(true)}
                disabled={!storeId}
                className="bg-[#5b4ef9] hover:bg-[#4a3ee0]"
              >
                <UserPlus className="h-4 w-4" />
                Add customer
              </Button>
            </div>
          </div>

          <div className="mt-5 overflow-hidden rounded-2xl border border-slate-100">
            <Table>
              <TableHeader>
                <TableRow className="bg-slate-50/80 hover:bg-slate-50/80">
                  <TableHead>Customer</TableHead>
                  <TableHead>Contact</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Registered</TableHead>
                  <TableHead className="text-right">
                    {isFetching && !isLoading && <Loader2 className="ml-auto h-3.5 w-3.5 animate-spin text-slate-400" />}
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading && <CustomersTableSkeletonRows />}

                {!isLoading && !isError && customers.length === 0 && (
                  <TableRow className="hover:bg-transparent">
                    <TableCell colSpan={6} className="p-0">
                      <Empty className="border-none py-14">
                        <EmptyHeader>
                          <EmptyMedia variant="icon">
                            <Users />
                          </EmptyMedia>
                          <EmptyTitle>No customers match these filters</EmptyTitle>
                          <EmptyDescription>
                            {statusFilter !== "ALL" || guestOnly
                              ? "Try clearing the status or guest filter."
                              : "Once someone registers or checks out, they'll show up here."}
                          </EmptyDescription>
                        </EmptyHeader>
                        <EmptyContent>
                          <Button onClick={() => setCreateOpen(true)} disabled={!storeId} className="bg-[#5b4ef9] hover:bg-[#4a3ee0]">
                            <UserPlus className="h-4 w-4" />
                            Add your first customer
                          </Button>
                        </EmptyContent>
                      </Empty>
                    </TableCell>
                  </TableRow>
                )}

                {!isLoading && isError && (
                  <TableRow className="hover:bg-transparent">
                    <TableCell colSpan={6} className="p-0">
                      <div className="flex flex-col items-center gap-3 py-14 text-center">
                        <AlertTriangle className="h-7 w-7 text-red-400" />
                        <p className="text-sm font-medium text-slate-700">
                          {error instanceof Error ? error.message : "Couldn't load customers."}
                        </p>
                        <Button variant="outline" size="sm" onClick={() => refetch()}>
                          Try again
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                )}

                {!isLoading && !isError && (
                  <AnimatePresence mode="popLayout" initial={false}>
                    {customers.map((customer) => (
                      <CustomerRow key={customer.id} customer={customer} />
                    ))}
                  </AnimatePresence>
                )}
              </TableBody>
            </Table>
          </div>

          {data && data.total > 0 && (
            <div className="mt-4 flex items-center justify-between text-sm text-slate-500">
              <span>
                Page {data.page} of {totalPages} · {data.total} total
              </span>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>
                  <ChevronLeft className="h-4 w-4" />
                  Prev
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                >
                  Next
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </section>
      </main>

      {storeId && (
        <CreateCustomerDialog open={createOpen} onOpenChange={setCreateOpen} tenantId={tenantId} storeId={storeId} />
      )}
    </div>
  );
}

function CustomerRow({ customer }: { customer: CustomerResponse }) {
  return (
    <motion.tr
      layout
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.18 }}
      className="border-b border-slate-100 transition-colors last:border-0 hover:bg-slate-50"
    >
      <TableCell>
        <Link href={`/store-owner-dashboard/customers/${customer.id}`} className="flex items-center gap-3 group">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#5b4ef9]/10 text-sm font-semibold text-[#5b4ef9]">
            {customer.firstName.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="font-medium text-slate-900 group-hover:text-[#5b4ef9]">
              {customer.firstName} {customer.lastName ?? ""}
            </p>
            <p className="text-xs text-slate-400">{customer.customerCode}</p>
          </div>
        </Link>
      </TableCell>
      <TableCell>
        <p className="text-sm text-slate-700">{customer.email}</p>
        <p className="text-xs text-slate-400">{customer.mobile}</p>
      </TableCell>
      <TableCell>
        <CustomerStatusBadge status={customer.status} />
      </TableCell>
      <TableCell>
        {customer.isGuestCustomer ? (
          <span className="inline-flex items-center rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">
            Guest
          </span>
        ) : (
          <span className="inline-flex items-center rounded-full bg-[#5b4ef9]/10 px-2 py-0.5 text-xs font-medium text-[#5b4ef9]">
            Registered
          </span>
        )}
      </TableCell>
      <TableCell className="text-sm text-slate-500">{formatDate(customer.registeredAt)}</TableCell>
      <TableCell className="text-right">
        <Link href={`/store-owner-dashboard/customers/${customer.id}`}>
          <Button variant="ghost" size="sm" className="text-slate-500 hover:text-[#5b4ef9]">
            <Search className="h-4 w-4" />
          </Button>
        </Link>
      </TableCell>
    </motion.tr>
  );
}
