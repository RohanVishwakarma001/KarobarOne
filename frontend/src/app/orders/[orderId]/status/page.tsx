"use client";

import { use } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { AlertTriangle, ArrowLeft, Package } from "lucide-react";

import { useOrder, useOrderHistory } from "@/hooks/use-orders";
import { OrderStatusBadge } from "@/components/commerce/OrderStatusBadge";
import { OrderTimeline } from "@/components/commerce/OrderTimeline";
import { InvoiceDownloadButton } from "@/components/commerce/InvoiceDownloadButton";
import { Skeleton } from "@/components/ui/skeleton";
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { Button } from "@/components/ui/button";
import { ApiError } from "@/lib/api/api-client";

const money = (value: string | number) => `₹${Number(value).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

export default function OrderStatusPage({ params }: { params: Promise<{ orderId: string }> }) {
  const { orderId } = use(params);
  const { data: order, isLoading, isError, error } = useOrder(orderId);
  const { data: history } = useOrderHistory(orderId);

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] px-4 py-10 text-slate-900 sm:px-6">
      <div className="mx-auto max-w-3xl">
        <Link href="/orders" className="inline-flex items-center gap-1.5 text-xs font-medium uppercase tracking-[0.24em] text-slate-500 hover:text-[#5b4ef9]">
          <ArrowLeft className="h-3.5 w-3.5" /> Orders
        </Link>

        {isLoading && (
          <div className="mt-6 space-y-4">
            <Skeleton className="h-24 w-full rounded-3xl" />
            <Skeleton className="h-64 w-full rounded-3xl" />
          </div>
        )}

        {!isLoading && isError && (
          <Empty className="mt-6 rounded-3xl border border-slate-200 bg-white py-16 shadow-sm">
            <EmptyHeader>
              <EmptyMedia variant="icon">
                <AlertTriangle />
              </EmptyMedia>
              <EmptyTitle>{error instanceof ApiError && error.status === 404 ? "Order not found" : "Couldn't load this order"}</EmptyTitle>
              <EmptyDescription>{error instanceof ApiError ? error.message : "Something went wrong."}</EmptyDescription>
            </EmptyHeader>
            <EmptyContent>
              <Link href="/orders">
                <Button variant="outline">Back to orders</Button>
              </Link>
            </EmptyContent>
          </Empty>
        )}

        {!isLoading && !isError && order && (
          <>
            <motion.section
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
            >
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-slate-400">{order.orderNumber}</p>
                  <h1 className="mt-1 text-2xl font-semibold tracking-tight">{money(order.totalAmount)}</h1>
                </div>
                <div className="flex items-center gap-3">
                  <OrderStatusBadge status={order.orderStatus} />
                  <InvoiceDownloadButton order={order} />
                </div>
              </div>
            </motion.section>

            <motion.section
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 }}
              className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
            >
              <h2 className="mb-5 text-lg font-semibold">Tracking</h2>
              <OrderTimeline currentStatus={order.orderStatus} history={history ?? []} />
            </motion.section>

            <motion.section
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
            >
              <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold">
                <Package className="h-4 w-4 text-[#5b4ef9]" /> Items
              </h2>
              <ul className="space-y-3">
                {order.items.map((item) => (
                  <li key={item.id} className="flex items-center justify-between border-b border-slate-100 pb-3 last:border-0 last:pb-0">
                    <div>
                      <p className="text-sm font-medium text-slate-800">{item.productName}</p>
                      <p className="text-xs text-slate-400">
                        {item.sku} · Qty {item.quantity}
                      </p>
                    </div>
                    <span className="text-sm font-semibold">{money(item.lineTotal)}</span>
                  </li>
                ))}
              </ul>
            </motion.section>
          </>
        )}
      </div>
    </div>
  );
}
