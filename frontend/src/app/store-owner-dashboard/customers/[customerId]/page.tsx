"use client";

import { use, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { AlertTriangle, ArrowLeft, Mail, Pencil, Phone, ShieldCheck, ShieldX, Trash2 } from "lucide-react";

import { useRequireAuth } from "@/hooks/use-require-auth";
import { useCustomer } from "@/hooks/use-customers";
import { CustomerStatusBadge } from "@/components/customers/status-badge";
import { EditCustomerDialog } from "@/components/customers/edit-customer-dialog";
import { DeleteCustomerDialog } from "@/components/customers/delete-customer-dialog";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { ApiError } from "@/lib/api/coreClient";

function formatDateTime(value: string | null): string {
  if (!value) return "—";
  return new Date(value).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" });
}

function VerificationRow({ label, verified }: { label: string; verified: boolean }) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50/60 px-4 py-3">
      <span className="text-sm text-slate-600">{label}</span>
      {verified ? (
        <span className="inline-flex items-center gap-1.5 text-sm font-medium text-emerald-600">
          <ShieldCheck className="h-4 w-4" /> Verified
        </span>
      ) : (
        <span className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-400">
          <ShieldX className="h-4 w-4" /> Not verified
        </span>
      )}
    </div>
  );
}

function DetailSkeleton() {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <div className="flex items-start gap-4">
        <Skeleton className="h-16 w-16 shrink-0 rounded-full" />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-4 w-32" />
        </div>
      </div>
      <div className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-14 w-full rounded-xl" />
        ))}
      </div>
    </div>
  );
}

export default function CustomerDetailPage({ params }: { params: Promise<{ customerId: string }> }) {
  const { customerId } = use(params);
  const router = useRouter();
  const { session, ready } = useRequireAuth();
  const tenantId = session?.tenantId ?? "";
  const [editOpen, setEditOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);

  const { data: customer, isLoading, isError, error } = useCustomer(tenantId, ready ? customerId : null);

  if (!ready) return null;

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-4xl items-center gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <Link
            href="/store-owner-dashboard/customers"
            className="inline-flex items-center gap-1.5 text-xs font-medium uppercase tracking-[0.24em] text-slate-500 hover:text-[#5b4ef9]"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Customers
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        {isLoading && <DetailSkeleton />}

        {!isLoading && isError && (
          <Empty className="rounded-3xl border border-slate-200 bg-white py-16 shadow-sm">
            <EmptyHeader>
              <EmptyMedia variant="icon">
                <AlertTriangle />
              </EmptyMedia>
              <EmptyTitle>
                {error instanceof ApiError && error.status === 404 ? "Customer not found" : "Couldn't load this customer"}
              </EmptyTitle>
              <EmptyDescription>
                {error instanceof ApiError ? error.message : "Something went wrong. Try again in a moment."}
              </EmptyDescription>
            </EmptyHeader>
            <EmptyContent>
              <Link href="/store-owner-dashboard/customers">
                <Button variant="outline">Back to customers</Button>
              </Link>
            </EmptyContent>
          </Empty>
        )}

        {!isLoading && !isError && customer && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
            className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8"
          >
            <div className="flex flex-col justify-between gap-6 sm:flex-row sm:items-start">
              <div className="flex items-start gap-4">
                <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-[#5b4ef9]/10 text-2xl font-semibold text-[#5b4ef9]">
                  {customer.firstName.charAt(0).toUpperCase()}
                </div>
                <div>
                  <h1 className="text-2xl font-semibold tracking-tight">
                    {customer.firstName} {customer.lastName ?? ""}
                  </h1>
                  <p className="mt-1 text-sm text-slate-500">{customer.customerCode}</p>
                  <div className="mt-3 flex flex-wrap items-center gap-2">
                    <CustomerStatusBadge status={customer.status} />
                    {customer.isGuestCustomer ? (
                      <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-600">
                        Guest
                      </span>
                    ) : (
                      <span className="inline-flex items-center rounded-full bg-[#5b4ef9]/10 px-2.5 py-0.5 text-xs font-medium text-[#5b4ef9]">
                        Registered
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex shrink-0 gap-2">
                <Button variant="outline" onClick={() => setEditOpen(true)}>
                  <Pencil className="h-4 w-4" />
                  Edit
                </Button>
                <Button variant="destructive" onClick={() => setDeleteOpen(true)}>
                  <Trash2 className="h-4 w-4" />
                  Delete
                </Button>
              </div>
            </div>

            <div className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div className="flex items-center gap-3 rounded-xl border border-slate-100 bg-slate-50/60 px-4 py-3">
                <Mail className="h-4 w-4 text-slate-400" />
                <span className="text-sm text-slate-700">{customer.email}</span>
              </div>
              <div className="flex items-center gap-3 rounded-xl border border-slate-100 bg-slate-50/60 px-4 py-3">
                <Phone className="h-4 w-4 text-slate-400" />
                <span className="text-sm text-slate-700">{customer.mobile}</span>
              </div>
              <VerificationRow label="Email" verified={customer.isEmailVerified} />
              <VerificationRow label="Mobile" verified={customer.isMobileVerified} />
            </div>

            <div className="mt-6 grid grid-cols-2 gap-3 border-t border-slate-100 pt-6 text-sm sm:grid-cols-4">
              <div>
                <p className="text-xs uppercase tracking-[0.14em] text-slate-400">Registered</p>
                <p className="mt-1 text-slate-700">{formatDateTime(customer.registeredAt)}</p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.14em] text-slate-400">Last login</p>
                <p className="mt-1 text-slate-700">{formatDateTime(customer.lastLoginAt)}</p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.14em] text-slate-400">Created</p>
                <p className="mt-1 text-slate-700">{formatDateTime(customer.createdAt)}</p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.14em] text-slate-400">Updated</p>
                <p className="mt-1 text-slate-700">{formatDateTime(customer.updatedAt)}</p>
              </div>
            </div>
          </motion.div>
        )}
      </main>

      {customer && (
        <>
          <EditCustomerDialog open={editOpen} onOpenChange={setEditOpen} tenantId={tenantId} customer={customer} />
          <DeleteCustomerDialog
            open={deleteOpen}
            onOpenChange={setDeleteOpen}
            tenantId={tenantId}
            customer={customer}
            onDeleted={() => router.push("/store-owner-dashboard/customers")}
          />
        </>
      )}
    </div>
  );
}
