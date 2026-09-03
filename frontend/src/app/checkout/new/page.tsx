"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { toast } from "sonner";
import { Loader2, MapPin, ShoppingBag, User } from "lucide-react";

import { useGuestSessionId, useCommerceCart } from "@/hooks/use-commerce-cart";
import { useCreateOrder } from "@/hooks/use-orders";
import { createAddress } from "@/lib/api/addresses";
import { createCustomer } from "@/lib/api/customers";
import { createRazorpayOrder, verifyRazorpayPayment } from "@/lib/api/commerce";
import { openRazorpayCheckout } from "@/lib/razorpay";
import { ApiError } from "@/lib/api/api-client";
import { TENANT_ID, STORE_ID, RAZORPAY_KEY_ID, assertStoreConfig } from "@/lib/api/config";
import { AnimatedButton } from "@/components/ui/animated-button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const money = (value: string | number) => `₹${Number(value).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

type PlaceOrderStatus = "idle" | "pending" | "success" | "error";

export default function NewCheckoutPage() {
  const router = useRouter();
  const sessionId = useGuestSessionId();
  const { data: cart, isLoading: cartLoading } = useCommerceCart(sessionId);
  const createOrder = useCreateOrder();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");
  const [addressLine1, setAddressLine1] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [postalCode, setPostalCode] = useState("");
  const [status, setStatus] = useState<PlaceOrderStatus>("idle");

  const canSubmit =
    Boolean(cart?.items.length) && fullName.trim() && email.trim() && mobile.trim() && addressLine1.trim() && city.trim() && state.trim() && postalCode.trim();

  const handlePlaceOrder = async () => {
    if (!cart || cart.items.length === 0) return;
    try {
      assertStoreConfig();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Store is not configured.");
      return;
    }

    setStatus("pending");
    try {
      // 1. Real customer record (public registration — see app/api/v1/endpoints/customers.py::createCustomer)
      const customer = await createCustomer({
        tenantId: TENANT_ID,
        storeId: STORE_ID,
        firstName: fullName.trim().split(" ")[0] || fullName.trim(),
        lastName: fullName.trim().split(" ").slice(1).join(" ") || undefined,
        email: email.trim(),
        mobile: mobile.trim(),
        status: "ACTIVE",
        isGuestCustomer: true,
      });

      // 2. Real address record, used for both billing and shipping here for simplicity
      const address = await createAddress({
        customerId: customer.id,
        addressType: "SHIPPING",
        fullName: fullName.trim(),
        mobile: mobile.trim(),
        addressLine1: addressLine1.trim(),
        city: city.trim(),
        state: state.trim(),
        postalCode: postalCode.trim(),
        isDefault: true,
      });

      // 3. Real order from the real cart contents (server recomputes totals from these lines)
      const order = await createOrder.mutateAsync({
        tenantId: TENANT_ID,
        storeId: STORE_ID,
        customerId: customer.id,
        billingAddressId: address.id,
        shippingAddressId: address.id,
        cartId: cart.id,
        shippingAmount: Number(cart.shippingAmount),
        items: cart.items.map((item) => ({
          productId: item.productId,
          productVariantId: item.productVariantId ?? undefined,
          sku: item.productId.slice(0, 8), // CartItem has no sku — see docs/api-mapping/commerce.md
          productName: `Item #${item.productId.slice(0, 8)}`,
          quantity: item.quantity,
          unitPrice: Number(item.unitPrice),
          taxAmount: Number(item.taxAmount),
          discountAmount: Number(item.discountAmount),
        })),
      });

      // 4. Real Razorpay order (fails loudly — 500 PAYMENT_GATEWAY_NOT_CONFIGURED —
      // rather than a fake success, if razorpayKeyId/Secret aren't set server-side)
      const razorpayOrder = await createRazorpayOrder({ tenantId: TENANT_ID, storeId: STORE_ID, orderId: order.id });

      const result = await openRazorpayCheckout({
        key: razorpayOrder.razorpayKeyId || RAZORPAY_KEY_ID,
        amount: razorpayOrder.amount,
        currency: razorpayOrder.currency,
        order_id: razorpayOrder.razorpayOrderId,
        name: "KarobarOne",
        description: `Order ${order.orderNumber}`,
        prefill: { name: fullName, email, contact: mobile },
        theme: { color: "#5b4ef9" },
      });

      // 5. Real signature verification server-side (fail-closed HMAC check)
      await verifyRazorpayPayment({
        razorpayOrderId: result.razorpay_order_id,
        razorpayPaymentId: result.razorpay_payment_id,
        razorpaySignature: result.razorpay_signature,
      });

      setStatus("success");
      toast.success("Payment successful — order confirmed!");
      router.push(`/orders/${order.id}/status`);
    } catch (err) {
      setStatus("error");
      toast.error(err instanceof ApiError ? err.message : err instanceof Error ? err.message : "Checkout failed.");
    }
  };

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] px-4 py-10 text-slate-900 sm:px-6">
      <div className="mx-auto grid max-w-4xl gap-6 lg:grid-cols-[1fr_360px]">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="flex items-center gap-2 text-lg font-semibold">
              <User className="h-4 w-4 text-[#5b4ef9]" /> Your details
            </h2>
            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div className="space-y-1.5 sm:col-span-2">
                <Label>Full name</Label>
                <Input value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Ada Lovelace" />
              </div>
              <div className="space-y-1.5">
                <Label>Email</Label>
                <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="ada@example.com" />
              </div>
              <div className="space-y-1.5">
                <Label>Mobile</Label>
                <Input value={mobile} onChange={(e) => setMobile(e.target.value)} placeholder="9876543210" />
              </div>
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="flex items-center gap-2 text-lg font-semibold">
              <MapPin className="h-4 w-4 text-[#5b4ef9]" /> Delivery address
            </h2>
            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div className="space-y-1.5 sm:col-span-2">
                <Label>Address</Label>
                <Input value={addressLine1} onChange={(e) => setAddressLine1(e.target.value)} placeholder="123 MG Road" />
              </div>
              <div className="space-y-1.5">
                <Label>City</Label>
                <Input value={city} onChange={(e) => setCity(e.target.value)} placeholder="Bengaluru" />
              </div>
              <div className="space-y-1.5">
                <Label>State</Label>
                <Input value={state} onChange={(e) => setState(e.target.value)} placeholder="Karnataka" />
              </div>
              <div className="space-y-1.5">
                <Label>Postal code</Label>
                <Input value={postalCode} onChange={(e) => setPostalCode(e.target.value)} placeholder="560001" />
              </div>
            </div>
          </section>
        </motion.div>

        <motion.aside
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="h-fit rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <h2 className="flex items-center gap-2 text-lg font-semibold">
            <ShoppingBag className="h-4 w-4 text-[#5b4ef9]" /> Order summary
          </h2>

          {cartLoading && <Loader2 className="mt-6 h-5 w-5 animate-spin text-slate-400" />}

          {!cartLoading && cart && cart.items.length > 0 && (
            <>
              <ul className="mt-4 space-y-2 text-sm">
                {cart.items.map((item) => (
                  <li key={item.id} className="flex justify-between text-slate-600">
                    <span>Item #{item.productId.slice(0, 8)} × {item.quantity}</span>
                    <span>{money(item.lineTotal)}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-4 space-y-1 border-t border-slate-100 pt-4 text-sm">
                <div className="flex justify-between text-slate-500">
                  <span>Subtotal</span>
                  <span>{money(cart.subtotalAmount)}</span>
                </div>
                {Number(cart.discountAmount) > 0 && (
                  <div className="flex justify-between text-emerald-600">
                    <span>Discount</span>
                    <span>-{money(cart.discountAmount)}</span>
                  </div>
                )}
                <div className="flex justify-between text-slate-500">
                  <span>Shipping</span>
                  <span>{money(cart.shippingAmount)}</span>
                </div>
                <div className="flex justify-between pt-1 text-base font-semibold text-slate-900">
                  <span>Total</span>
                  <span>{money(cart.totalAmount)}</span>
                </div>
              </div>

              <AnimatedButton
                type="button"
                status={status}
                onClick={handlePlaceOrder}
                disabled={!canSubmit}
                label={`Pay ${money(cart.totalAmount)}`}
                loadingLabel="Processing…"
                successLabel="Paid"
                className="mt-5 w-full bg-[#5b4ef9] hover:bg-[#4a3ee0]"
              />
            </>
          )}

          {!cartLoading && (!cart || cart.items.length === 0) && <p className="mt-4 text-sm text-slate-400">Your cart is empty.</p>}
        </motion.aside>
      </div>
    </div>
  );
}
