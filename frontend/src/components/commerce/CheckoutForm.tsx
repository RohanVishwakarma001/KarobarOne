"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Check, MapPin, CreditCard, Truck, Loader2, PackageSearch } from "lucide-react";
import { useCart } from "@/hooks/use-cart";
import { RAZORPAY_KEY_ID } from "@/lib/api/config";
import { openRazorpayCheckout } from "@/lib/razorpay";
import {
  ApiError,
  type PaymentMethod,
  checkServiceability,
  createOrder,
  createOrderItem,
  createPaymentOrder,
  listPaymentMethods,
  updateOrderStatus,
  verifyPayment,
} from "@/lib/api/github";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;

// No store pickup pincode configured anywhere yet — placeholder until shipping-profile
// / store-settings config exists. Real cart weight isn't tracked either; 0.5kg is a stand-in.
const FALLBACK_PICKUP_PINCODE = "110001";
const FALLBACK_PARCEL_WEIGHT_KG = 0.5;

export function CheckoutForm({ guest = false }: { guest?: boolean }) {
  const { customerId, cart, items, subtotal, loading: cartLoading, refresh: refreshCart } = useCart();

  const [methods, setMethods] = useState<PaymentMethod[]>([]);
  const [methodId, setMethodId] = useState<string | null>(null);
  const [billingAddressId, setBillingAddressId] = useState("");
  const [shippingAddressId, setShippingAddressId] = useState("");
  const [sameAsBilling, setSameAsBilling] = useState(true);
  const [contact, setContact] = useState({ name: "", mobile: "", email: "" });
  const [placing, setPlacing] = useState<string | null>(null); // step label while placing
  const [placedOrder, setPlacedOrder] = useState<{ id: string; order_number: string } | null>(null);

  const [deliveryPincode, setDeliveryPincode] = useState("");
  const [checkingServiceability, setCheckingServiceability] = useState(false);
  const [serviceability, setServiceability] = useState<Record<string, unknown> | null>(null);
  const [serviceabilityError, setServiceabilityError] = useState<string | null>(null);

  useEffect(() => {
    listPaymentMethods()
      .then((all) => {
        const active = all.filter((m) => m.is_active);
        setMethods(active);
        setMethodId((prev) => prev ?? active[0]?.id ?? null);
      })
      .catch(() => toast.error("Could not load payment methods."));
  }, []);

  const shipping = subtotal >= 3000 || subtotal === 0 ? 0 : 99;
  const total = subtotal + shipping;
  const selectedMethod = methods.find((m) => m.id === methodId);

  if (placedOrder) {
    return (
      <div className="mx-auto max-w-2xl px-6">
        <div className="rounded-2xl border border-gray-200 bg-white p-10 text-center shadow-sm">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-green-50 text-green-600">
            <Check />
          </div>
          <h2 className="mt-5 text-2xl font-semibold">Order placed successfully</h2>
          <p className="mt-2 text-sm text-gray-500">
            Your order <span className="font-medium text-gray-900">#{placedOrder.order_number}</span> has been created.
          </p>
          <Link href={`/orders/${placedOrder.id}`} className="mt-6 inline-flex rounded-lg bg-[#5b4ef9] px-5 py-3 text-sm font-medium text-white">
            View Order
          </Link>
        </div>
      </div>
    );
  }

  // Best-effort — degrades gracefully since this depends on live Shiprocket credentials
  // that may not be configured in every environment. Never blocks checkout on failure.
  async function handleCheckServiceability() {
    if (!/^\d{6}$/.test(deliveryPincode)) {
      toast.error("Enter a valid 6-digit delivery pincode.");
      return;
    }
    setCheckingServiceability(true);
    setServiceabilityError(null);
    setServiceability(null);
    try {
      const result = await checkServiceability({
        pickup_postcode: FALLBACK_PICKUP_PINCODE,
        delivery_postcode: deliveryPincode,
        weight: FALLBACK_PARCEL_WEIGHT_KG,
      });
      setServiceability(result);
    } catch (e) {
      setServiceabilityError(e instanceof ApiError ? e.message : "Could not check delivery availability right now — you can still place your order.");
    } finally {
      setCheckingServiceability(false);
    }
  }

  async function handlePlaceOrder() {
    if (!customerId || !cart) return;
    if (items.length === 0) {
      toast.error("Your cart is empty.");
      return;
    }
    if (!billingAddressId || (!sameAsBilling && !shippingAddressId)) {
      toast.error("Enter a billing (and shipping) address id.");
      return;
    }
    if (!methodId) {
      toast.error("Select a payment method.");
      return;
    }

    const shipToId = sameAsBilling ? billingAddressId : shippingAddressId;
    const isCod = selectedMethod?.method_code?.toUpperCase().includes("COD") || selectedMethod?.is_online === false;

    try {
      setPlacing("Creating your order…");
      const noteParts = [];
      if (guest && (contact.name || contact.mobile || contact.email)) {
        noteParts.push(`Guest contact: ${[contact.name, contact.mobile, contact.email].filter(Boolean).join(" / ")}`);
      }
      const order = await createOrder({
        customer_id: customerId,
        cart_id: cart.id,
        billing_address_id: billingAddressId,
        shipping_address_id: shipToId,
        subtotal_amount: subtotal,
        shipping_amount: shipping,
        total_amount: total,
        customer_note: noteParts.join(" | ") || undefined,
      });

      setPlacing("Saving order items…");
      await Promise.all(
        items.map((item) =>
          createOrderItem({
            order_id: order.id,
            product_id: item.product_id,
            product_variant_id: item.product_variant_id ?? undefined,
            sku: item.product_id.slice(0, 12),
            product_name: `Product ${item.product_id.slice(0, 8)}`,
            quantity: item.quantity,
            unit_price: item.unit_price,
            discount_amount: item.discount_amount,
            tax_amount: item.tax_amount,
            line_total: item.line_total,
          })
        )
      );

      if (isCod) {
        setPlacing("Confirming order…");
        await updateOrderStatus({ order_id: order.id, order_status: "CONFIRMED", payment_status: "PENDING", fulfillment_status: "PENDING" });
      } else {
        setPlacing("Starting payment…");
        const { razorpay_order: razorpayOrder } = await createPaymentOrder({
          entity_type: "ORDER",
          entity_id: order.id,
          payment_method_id: methodId,
          amount: total,
          receipt: order.order_number,
        });

        if (!RAZORPAY_KEY_ID) throw new Error("Payment gateway is not configured (NEXT_PUBLIC_RAZORPAY_KEY_ID missing).");

        const result = await openRazorpayCheckout({
          key: RAZORPAY_KEY_ID,
          amount: Number(razorpayOrder.amount),
          currency: razorpayOrder.currency,
          order_id: razorpayOrder.id,
          name: "KarobarOne",
          description: `Order ${order.order_number}`,
          prefill: { name: contact.name || undefined, email: contact.email || undefined, contact: contact.mobile || undefined },
          theme: { color: "#5b4ef9" },
        });

        setPlacing("Verifying payment…");
        const verified = await verifyPayment(result);
        if (!verified) throw new Error("Payment verification failed. If money was deducted, contact support with your order number.");

        setPlacing("Confirming order…");
        await updateOrderStatus({ order_id: order.id, order_status: "CONFIRMED", payment_status: "PAID", fulfillment_status: "PENDING" });
      }

      window.localStorage.removeItem("karobar_cart_id");
      refreshCart();
      setPlacedOrder({ id: order.id, order_number: order.order_number });
    } catch (e) {
      toast.error(e instanceof ApiError || e instanceof Error ? e.message : "Could not place your order. Please try again.");
    } finally {
      setPlacing(null);
    }
  }

  return (
    <div className="mx-auto grid max-w-7xl gap-6 px-6 lg:grid-cols-[1fr_380px]">
      <div className="space-y-5">
        {guest && (
          <section className="rounded-2xl border border-gray-200 bg-white p-5">
            <h2 className="font-semibold">Contact details</h2>
            <div className="mt-4 grid gap-4 sm:grid-cols-2">
              <label className="text-sm text-gray-600">
                Full name
                <input
                  className="mt-2 w-full rounded-lg border border-gray-200 px-3 py-2.5 outline-none focus:border-[#5b4ef9]"
                  placeholder="Your name"
                  value={contact.name}
                  onChange={(e) => setContact((c) => ({ ...c, name: e.target.value }))}
                />
              </label>
              <label className="text-sm text-gray-600">
                Mobile number
                <input
                  className="mt-2 w-full rounded-lg border border-gray-200 px-3 py-2.5 outline-none focus:border-[#5b4ef9]"
                  placeholder="+91 98765 43210"
                  value={contact.mobile}
                  onChange={(e) => setContact((c) => ({ ...c, mobile: e.target.value }))}
                />
              </label>
              <label className="text-sm text-gray-600 sm:col-span-2">
                Email address
                <input
                  className="mt-2 w-full rounded-lg border border-gray-200 px-3 py-2.5 outline-none focus:border-[#5b4ef9]"
                  placeholder="you@example.com"
                  value={contact.email}
                  onChange={(e) => setContact((c) => ({ ...c, email: e.target.value }))}
                />
              </label>
            </div>
          </section>
        )}

        <section className="rounded-2xl border border-gray-200 bg-white p-5">
          <div className="flex items-center gap-3">
            <span className="rounded-lg bg-[#5b4ef9]/10 p-2 text-[#5b4ef9]">
              <MapPin className="h-5 w-5" />
            </span>
            <div>
              <h2 className="font-semibold">Delivery address</h2>
              <p className="text-sm text-gray-500">Address management isn&apos;t wired up yet — enter an existing address id.</p>
            </div>
          </div>
          <div className="mt-5 grid gap-4">
            <input
              className="rounded-lg border border-gray-200 px-3 py-2.5"
              placeholder="Billing address ID (UUID)"
              value={billingAddressId}
              onChange={(e) => setBillingAddressId(e.target.value)}
            />
            <label className="flex items-center gap-2 text-sm text-gray-600">
              <input type="checkbox" checked={sameAsBilling} onChange={(e) => setSameAsBilling(e.target.checked)} />
              Shipping address is the same as billing
            </label>
            {!sameAsBilling && (
              <input
                className="rounded-lg border border-gray-200 px-3 py-2.5"
                placeholder="Shipping address ID (UUID)"
                value={shippingAddressId}
                onChange={(e) => setShippingAddressId(e.target.value)}
              />
            )}

            <div className="rounded-xl border border-gray-100 bg-gray-50 p-4">
              <div className="flex items-center gap-2 text-sm font-medium text-gray-700">
                <PackageSearch className="h-4 w-4 text-[#5b4ef9]" /> Check delivery availability
              </div>
              <div className="mt-3 flex gap-2">
                <input
                  className="flex-1 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm outline-none focus:border-[#5b4ef9]"
                  placeholder="Delivery pincode"
                  maxLength={6}
                  value={deliveryPincode}
                  onChange={(e) => setDeliveryPincode(e.target.value.replace(/\D/g, ""))}
                />
                <button
                  type="button"
                  onClick={handleCheckServiceability}
                  disabled={checkingServiceability}
                  className="shrink-0 rounded-lg border border-[#5b4ef9]/30 bg-white px-4 py-2 text-sm font-medium text-[#5b4ef9] hover:bg-[#5b4ef9]/5 disabled:opacity-50"
                >
                  {checkingServiceability ? "Checking…" : "Check"}
                </button>
              </div>
              {serviceability && (
                <p className="mt-2 text-xs text-gray-600">
                  {(() => {
                    const data = serviceability.data as Record<string, unknown> | undefined;
                    const couriers = (data?.available_courier_companies as unknown[] | undefined) ?? [];
                    return couriers.length > 0
                      ? `Deliverable — ${couriers.length} courier option${couriers.length === 1 ? "" : "s"} available.`
                      : "No courier options found for this pincode.";
                  })()}
                </p>
              )}
              {serviceabilityError && <p className="mt-2 text-xs text-amber-600">{serviceabilityError}</p>}
            </div>
          </div>
        </section>

        <section className="rounded-2xl border border-gray-200 bg-white p-5">
          <div className="flex items-center gap-3">
            <span className="rounded-lg bg-[#5b4ef9]/10 p-2 text-[#5b4ef9]">
              <CreditCard className="h-5 w-5" />
            </span>
            <div>
              <h2 className="font-semibold">Payment method</h2>
              <p className="text-sm text-gray-500">Choose how you want to pay.</p>
            </div>
          </div>
          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            {methods.length === 0 && <p className="text-sm text-gray-400">No payment methods available.</p>}
            {methods.map((m) => (
              <button
                key={m.id}
                onClick={() => setMethodId(m.id)}
                className={`rounded-xl border p-4 text-left text-sm ${methodId === m.id ? "border-[#5b4ef9] bg-[#5b4ef9]/5" : "border-gray-200"}`}
              >
                <p className="font-medium">{m.method_name}</p>
                <p className="mt-1 text-xs text-gray-500">{m.is_online ? "Secure online payment" : "Pay at delivery"}</p>
              </button>
            ))}
          </div>
        </section>
      </div>

      <aside className="h-fit rounded-2xl border border-gray-200 bg-white p-5 lg:sticky lg:top-28">
        <h2 className="font-semibold">Order summary</h2>
        {cartLoading ? (
          <p className="mt-5 text-sm text-gray-400">Loading cart…</p>
        ) : (
          <div className="mt-5 space-y-4">
            {items.map((item) => (
              <div key={item.id} className="flex justify-between text-sm text-gray-600">
                <span>
                  Product {item.product_id.slice(0, 8)} × {item.quantity}
                </span>
                <span>{money(item.line_total)}</span>
              </div>
            ))}
            <div className="border-t border-gray-100 pt-4">
              <div className="flex justify-between text-sm text-gray-600">
                <span>Subtotal</span>
                <span>{money(subtotal)}</span>
              </div>
              <div className="mt-2 flex justify-between text-sm text-gray-600">
                <span>Shipping</span>
                <span className={shipping ? "" : "text-green-600"}>{shipping ? money(shipping) : "Free"}</span>
              </div>
              <div className="mt-4 flex justify-between font-semibold">
                <span>Total</span>
                <span>{money(total)}</span>
              </div>
            </div>
          </div>
        )}
        <button
          onClick={handlePlaceOrder}
          disabled={!!placing || cartLoading || items.length === 0}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-lg bg-[#5b4ef9] px-5 py-3 text-sm font-medium text-white hover:bg-[#4a3ee0] disabled:opacity-60"
        >
          {placing && <Loader2 className="h-4 w-4 animate-spin" />}
          {placing ?? "Place Order"}
        </button>
        <div className="mt-4 flex gap-2 text-xs text-gray-500">
          <Truck className="h-4 w-4 shrink-0" />
          Estimated delivery in 3–5 business days.
        </div>
      </aside>
    </div>
  );
}
