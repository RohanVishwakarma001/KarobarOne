"use client";

import { useState } from "react";
import { toast } from "sonner";
import { FileDown, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { CORE_API_BASE_URL } from "@/lib/api/config";
import type { Order } from "@/lib/api/commerce";

/**
 * POST /api/v1/invoice/generate (app/api/v1/endpoints/invoice.py) returns a
 * raw PDF binary, not the {success,data} envelope everything else in this
 * app uses — bypasses api-client.ts's JSON-only request() on purpose here.
 *
 * Known gap: Order carries billingAddressId/shippingAddressId as bare UUIDs,
 * not the address text itself (no denormalized fields — see
 * docs/api-mapping/commerce.md), and there's no frontend address-by-id
 * lookup yet. bill_to/ship_to below are filled from what the order actually
 * has rather than fabricated street addresses.
 */
export function InvoiceDownloadButton({ order }: { order: Order }) {
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownload = async () => {
    setIsDownloading(true);
    try {
      const res = await fetch(`${CORE_API_BASE_URL}/invoice/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          bill_to: { name: `Customer ${order.customerId.slice(0, 8)}`, address: `Billing address on file (id ${order.billingAddressId.slice(0, 8)})` },
          ship_to: { name: `Customer ${order.customerId.slice(0, 8)}`, address: `Shipping address on file (id ${order.shippingAddressId.slice(0, 8)})` },
          invoice: {
            number: order.orderNumber,
            date: (order.placedAt ?? order.createdAt ?? new Date().toISOString()).slice(0, 10),
          },
          items: order.items.map((item, index) => ({
            sr: index + 1,
            description: item.productName,
            hsn: "0000",
            qty: item.quantity,
            unit: "Nos",
            rate: Number(item.unitPrice),
            gst_pct: item.taxAmount && Number(item.unitPrice) > 0 ? Math.round((Number(item.taxAmount) / (Number(item.unitPrice) * item.quantity)) * 100) : 0,
          })),
        }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body?.detail ?? `Invoice generation failed (${res.status})`);
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `invoice_${order.orderNumber}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Couldn't generate the invoice.");
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <Button type="button" variant="outline" onClick={handleDownload} disabled={isDownloading}>
      {isDownloading ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileDown className="h-4 w-4" />}
      Download invoice
    </Button>
  );
}
