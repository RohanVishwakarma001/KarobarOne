"use client";

import Link from "next/link";
import { useState } from "react";
import { toast } from "sonner";
import { Loader2, Minus, Plus, Trash2, ShieldCheck, PackageOpen, Tag } from "lucide-react";
import { CommerceShell } from "@/components/commerce/CommerceShell";
import { useCart } from "@/hooks/use-cart";
import { ApiError, type Coupon, applyCartCoupon, getOffer, listCoupons } from "@/lib/api/github";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;

export default function CartPage() {
  const { cart, items, subtotal, loading, error, addItem, setQuantity, removeItem, refresh } = useCart();
  const [showAddForm, setShowAddForm] = useState(false);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [form, setForm] = useState({ product_id: "", unit_price: "", quantity: "1" });
  const [adding, setAdding] = useState(false);

  const [couponCode, setCouponCode] = useState("");
  const [applyingCoupon, setApplyingCoupon] = useState(false);
  const [appliedCoupon, setAppliedCoupon] = useState<{ coupon: Coupon; discount: number } | null>(null);

  const shipping = subtotal >= 3000 || subtotal === 0 ? 0 : 99;
  const total = subtotal + shipping - (appliedCoupon?.discount ?? 0);

  // usage_limit / usage_limit_per_customer / first_time_customer_only are NOT enforced
  // server-side (see coupons.ts) — this is a best-effort client-side apply only.
  async function handleApplyCoupon(e: React.FormEvent) {
    e.preventDefault();
    if (!cart || !couponCode.trim()) return;
    setApplyingCoupon(true);
    try {
      const allCoupons = await listCoupons();
      const match = allCoupons.find((c) => c.coupon_code.toLowerCase() === couponCode.trim().toLowerCase());
      if (!match) {
        toast.error("Coupon code not found.");
        return;
      }
      const offer = await getOffer(match.offer_id);
      let discount = offer.discount_type === "PERCENTAGE" ? (subtotal * offer.discount_value) / 100 : offer.discount_value;
      if (offer.maximum_discount_amount != null) discount = Math.min(discount, offer.maximum_discount_amount);
      discount = Math.min(discount, subtotal);

      await applyCartCoupon({ cart_id: cart.id, coupon_id: match.id, discount_amount: discount });
      setAppliedCoupon({ coupon: match, discount });
      toast.success(`Coupon ${match.coupon_code} applied.`);
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not apply this coupon.");
    } finally {
      setApplyingCoupon(false);
    }
  }

  async function handleQuantity(cartItemId: string, next: number) {
    if (next < 1) return;
    setBusyId(cartItemId);
    try {
      await setQuantity(cartItemId, next);
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not update quantity.");
    } finally {
      setBusyId(null);
    }
  }

  async function handleRemove(cartItemId: string) {
    setBusyId(cartItemId);
    try {
      await removeItem(cartItemId);
      toast.success("Item removed from cart.");
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not remove item.");
    } finally {
      setBusyId(null);
    }
  }

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    const unitPrice = Number(form.unit_price);
    const quantity = Number(form.quantity);
    if (!form.product_id || !Number.isFinite(unitPrice) || unitPrice < 0 || !Number.isFinite(quantity) || quantity < 1) {
      toast.error("Enter a valid product id, price and quantity.");
      return;
    }
    setAdding(true);
    try {
      await addItem({ product_id: form.product_id, unit_price: unitPrice, quantity });
      setForm({ product_id: "", unit_price: "", quantity: "1" });
      setShowAddForm(false);
      toast.success("Added to cart.");
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not add item.");
    } finally {
      setAdding(false);
    }
  }

  return (
    <CommerceShell title="Cart" eyebrow="Orders & Payments">
      <div className="mx-auto grid max-w-7xl gap-6 px-6 lg:grid-cols-[1fr_380px]">
        <section className="rounded-2xl border border-gray-200 bg-white">
          <div className="flex items-center justify-between border-b border-gray-200 px-5 py-4">
            <div>
              <h2 className="font-semibold">Your cart</h2>
              <p className="text-sm text-gray-500">{items.length} products ready for checkout</p>
            </div>
            <span className="rounded-full bg-[#5b4ef9]/10 px-3 py-1 text-xs font-semibold text-[#5b4ef9]">
              {items.reduce((s, i) => s + i.quantity, 0)} items
            </span>
          </div>

          {loading && (
            <div className="flex items-center justify-center gap-2 px-6 py-16 text-sm text-gray-500">
              <Loader2 className="h-4 w-4 animate-spin" /> Loading your cart…
            </div>
          )}

          {!loading && error && (
            <div className="px-6 py-16 text-center">
              <p className="font-medium text-red-600">{error}</p>
              <button onClick={() => refresh()} className="mt-4 rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium hover:border-[#5b4ef9]/40">
                Retry
              </button>
            </div>
          )}

          {!loading && !error && items.length === 0 && (
            <div className="px-6 py-16 text-center">
              <PackageOpen className="mx-auto h-8 w-8 text-gray-300" />
              <p className="mt-4 font-medium">Your cart is empty</p>
              <p className="mt-1 text-sm text-gray-500">Add products to continue.</p>
            </div>
          )}

          {!loading &&
            !error &&
            items.map((item) => (
              <div key={item.id} className="flex gap-4 border-b border-gray-100 p-5 last:border-0">
                <div className="flex h-24 w-24 shrink-0 items-center justify-center rounded-xl bg-gray-100 text-center text-[10px] font-semibold text-gray-400">
                  {item.product_id.slice(0, 8)}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex justify-between gap-3">
                    <div>
                      <h3 className="truncate font-medium">Product {item.product_id.slice(0, 8)}</h3>
                      <p className="mt-1 text-sm text-gray-500">{money(item.unit_price)} each</p>
                    </div>
                    <p className="font-semibold">{money(item.line_total)}</p>
                  </div>
                  <div className="mt-5 flex items-center justify-between">
                    <div className="flex items-center rounded-lg border border-gray-200">
                      <button
                        disabled={busyId === item.id}
                        className="p-2 disabled:opacity-40"
                        onClick={() => handleQuantity(item.id, item.quantity - 1)}
                      >
                        <Minus className="h-4 w-4" />
                      </button>
                      <span className="w-8 text-center text-sm">{item.quantity}</span>
                      <button
                        disabled={busyId === item.id}
                        className="p-2 disabled:opacity-40"
                        onClick={() => handleQuantity(item.id, item.quantity + 1)}
                      >
                        <Plus className="h-4 w-4" />
                      </button>
                    </div>
                    <button
                      disabled={busyId === item.id}
                      onClick={() => handleRemove(item.id)}
                      className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-red-600 disabled:opacity-40"
                    >
                      <Trash2 className="h-4 w-4" />
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            ))}

          <div className="border-t border-gray-100 p-5">
            {!showAddForm ? (
              <button
                onClick={() => setShowAddForm(true)}
                className="inline-flex items-center gap-2 text-sm font-medium text-[#5b4ef9] hover:underline"
              >
                <Plus className="h-4 w-4" /> Add a product to cart
              </button>
            ) : (
              <form onSubmit={handleAdd} className="space-y-3">
                <p className="text-xs text-gray-500">
                  There's no product catalog page wired up yet — enter a product id directly. This form will move onto product pages once
                  that module is connected.
                </p>
                <div className="grid gap-3 sm:grid-cols-3">
                  <input
                    className="rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9] sm:col-span-1"
                    placeholder="Product ID (UUID)"
                    value={form.product_id}
                    onChange={(e) => setForm((f) => ({ ...f, product_id: e.target.value }))}
                  />
                  <input
                    className="rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                    placeholder="Unit price"
                    type="number"
                    min="0"
                    value={form.unit_price}
                    onChange={(e) => setForm((f) => ({ ...f, unit_price: e.target.value }))}
                  />
                  <input
                    className="rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                    placeholder="Quantity"
                    type="number"
                    min="1"
                    value={form.quantity}
                    onChange={(e) => setForm((f) => ({ ...f, quantity: e.target.value }))}
                  />
                </div>
                <div className="flex gap-3">
                  <button
                    disabled={adding}
                    type="submit"
                    className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
                  >
                    {adding ? "Adding…" : "Add"}
                  </button>
                  <button type="button" onClick={() => setShowAddForm(false)} className="rounded-lg px-4 py-2 text-sm text-gray-500">
                    Cancel
                  </button>
                </div>
              </form>
            )}
          </div>
        </section>

        <aside className="h-fit rounded-2xl border border-gray-200 bg-white p-5 lg:sticky lg:top-28">
          <h2 className="font-semibold">Order summary</h2>

          <form onSubmit={handleApplyCoupon} className="mt-5 flex gap-2">
            <div className="relative flex-1">
              <Tag className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
              <input
                className="w-full rounded-lg border border-gray-200 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-[#5b4ef9]"
                placeholder="Coupon code"
                value={couponCode}
                onChange={(e) => setCouponCode(e.target.value)}
                disabled={!!appliedCoupon}
              />
            </div>
            <button
              type="submit"
              disabled={applyingCoupon || !!appliedCoupon || !cart}
              className="shrink-0 rounded-lg border border-[#5b4ef9]/30 px-4 py-2 text-sm font-medium text-[#5b4ef9] hover:bg-[#5b4ef9]/5 disabled:opacity-50"
            >
              {applyingCoupon ? "Applying…" : appliedCoupon ? "Applied" : "Apply"}
            </button>
          </form>

          <div className="mt-5 space-y-3 text-sm">
            <div className="flex justify-between text-gray-600">
              <span>Subtotal</span>
              <span>{money(subtotal)}</span>
            </div>
            {appliedCoupon && (
              <div className="flex justify-between text-green-600">
                <span>Coupon ({appliedCoupon.coupon.coupon_code})</span>
                <span>-{money(appliedCoupon.discount)}</span>
              </div>
            )}
            <div className="flex justify-between text-gray-600">
              <span>Shipping</span>
              <span>{shipping ? money(shipping) : "Free"}</span>
            </div>
            <div className="border-t border-gray-100 pt-3">
              <div className="flex justify-between text-base font-semibold">
                <span>Total</span>
                <span>{money(total)}</span>
              </div>
            </div>
          </div>
          <Link
            href="/checkout"
            aria-disabled={!cart || items.length === 0}
            className={`mt-6 flex w-full items-center justify-center rounded-lg px-5 py-3 text-sm font-medium text-white ${
              !cart || items.length === 0 ? "pointer-events-none bg-gray-300" : "bg-[#5b4ef9] hover:bg-[#4a3ee0]"
            }`}
          >
            Proceed to Checkout
          </Link>
          <div className="mt-5 flex gap-2 rounded-xl bg-gray-50 p-3 text-xs text-gray-600">
            <ShieldCheck className="h-4 w-4 shrink-0 text-[#5b4ef9]" />
            Secure checkout with protected payment processing.
          </div>
        </aside>
      </div>
    </CommerceShell>
  );
}
