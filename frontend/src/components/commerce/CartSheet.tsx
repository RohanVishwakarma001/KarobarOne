"use client";

import { useState } from "react";
import Link from "next/link";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { AnimatePresence, motion } from "framer-motion";
import { Loader2, Minus, Plus, ShoppingCart, Tag, Trash2, X } from "lucide-react";
import { useCartSheet } from "@/components/providers/cart-sheet-provider";
import {
  useApplyCommerceCoupon,
  useCommerceCart,
  useGuestSessionId,
  useRemoveCommerceCartItem,
  useUpdateCommerceCartItemQuantity,
} from "@/hooks/use-commerce-cart";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { useReducedMotion } from "@/lib/motion";

const money = (value: string | number) => `₹${Number(value).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

/** Small floating trigger — drop this anywhere (e.g. into a layout's header) to open the drawer. */
export function CartTriggerButton() {
  const { open } = useCartSheet();
  const sessionId = useGuestSessionId();
  const { data: cart } = useCommerceCart(sessionId);
  const count = cart?.items.reduce((sum, i) => sum + i.quantity, 0) ?? 0;

  return (
    <motion.button
      type="button"
      onClick={open}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className="fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-[#5b4ef9] text-white shadow-lg shadow-[#5b4ef9]/30 hover:bg-[#4a3ee0]"
    >
      <ShoppingCart className="h-5 w-5" />
      {count > 0 && (
        <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[11px] font-semibold text-white">
          {count > 9 ? "9+" : count}
        </span>
      )}
    </motion.button>
  );
}

function QuantityStepper({ quantity, onChange, disabled }: { quantity: number; onChange: (next: number) => void; disabled: boolean }) {
  return (
    <div className="inline-flex items-center rounded-full border border-slate-200">
      <button
        type="button"
        disabled={disabled || quantity <= 1}
        onClick={() => onChange(quantity - 1)}
        className="flex h-7 w-7 items-center justify-center rounded-full text-slate-500 hover:bg-slate-100 disabled:opacity-30"
      >
        <Minus className="h-3 w-3" />
      </button>
      <span className="w-6 text-center text-sm font-medium">{quantity}</span>
      <button
        type="button"
        disabled={disabled || quantity >= 999}
        onClick={() => onChange(quantity + 1)}
        className="flex h-7 w-7 items-center justify-center rounded-full text-slate-500 hover:bg-slate-100 disabled:opacity-30"
      >
        <Plus className="h-3 w-3" />
      </button>
    </div>
  );
}

export function CartSheet() {
  const { isOpen, close } = useCartSheet();
  const reducedMotion = useReducedMotion();
  const sessionId = useGuestSessionId();
  const { data: cart, isLoading } = useCommerceCart(sessionId);
  const updateQuantity = useUpdateCommerceCartItemQuantity(sessionId);
  const removeItem = useRemoveCommerceCartItem(sessionId);
  const applyCoupon = useApplyCommerceCoupon(sessionId);
  const [couponCode, setCouponCode] = useState("");

  const handleApplyCoupon = () => {
    if (!cart || !couponCode.trim()) return;
    // No customer auth exists in this codebase (see docs/api-mapping/auth.md)
    // — per-customer usage-limit enforcement needs SOME customer identity,
    // so the guest session id doubles as one here rather than skipping the check.
    applyCoupon.mutate({ cartId: cart.id, couponCode: couponCode.trim(), customerId: sessionId });
  };

  return (
    <DialogPrimitive.Root open={isOpen} onOpenChange={(open) => !open && close()}>
      <AnimatePresence>
        {isOpen && (
          <DialogPrimitive.Portal forceMount>
            <DialogPrimitive.Overlay asChild forceMount>
              <motion.div
                className="fixed inset-0 z-50 bg-slate-950/40"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.15 }}
              />
            </DialogPrimitive.Overlay>
            <DialogPrimitive.Content asChild forceMount onOpenAutoFocus={(e) => e.preventDefault()}>
              <motion.div
                className="fixed right-0 top-0 z-50 flex h-full w-full max-w-md flex-col bg-white shadow-2xl"
                initial={reducedMotion ? { opacity: 0 } : { x: "100%" }}
                animate={reducedMotion ? { opacity: 1 } : { x: 0 }}
                exit={reducedMotion ? { opacity: 0 } : { x: "100%" }}
                transition={{ type: "spring", stiffness: 380, damping: 36 }}
              >
                <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
                  <DialogPrimitive.Title className="text-lg font-semibold text-slate-900">
                    Your cart{cart && cart.items.length > 0 ? ` (${cart.items.length})` : ""}
                  </DialogPrimitive.Title>
                  <DialogPrimitive.Close className="rounded-full p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600">
                    <X className="h-4 w-4" />
                  </DialogPrimitive.Close>
                </div>

                <div className="flex-1 overflow-y-auto px-5 py-4">
                  {isLoading && (
                    <div className="space-y-3">
                      {Array.from({ length: 3 }).map((_, i) => (
                        <Skeleton key={i} className="h-20 w-full rounded-xl" />
                      ))}
                    </div>
                  )}

                  {!isLoading && (!cart || cart.items.length === 0) && (
                    <Empty className="border-none py-12">
                      <EmptyHeader>
                        <EmptyMedia variant="icon">
                          <ShoppingCart />
                        </EmptyMedia>
                        <EmptyTitle>Your cart is empty</EmptyTitle>
                        <EmptyDescription>Items you add will show up here.</EmptyDescription>
                      </EmptyHeader>
                      <EmptyContent>
                        <Button variant="outline" onClick={close}>
                          Continue browsing
                        </Button>
                      </EmptyContent>
                    </Empty>
                  )}

                  {!isLoading && cart && cart.items.length > 0 && (
                    <AnimatePresence mode="popLayout" initial={false}>
                      {cart.items.map((item) => (
                        <motion.div
                          key={item.id}
                          layout
                          initial={{ opacity: 0, y: 8 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, x: 24 }}
                          transition={{ duration: 0.2 }}
                          className="mb-3 flex items-center gap-3 rounded-xl border border-slate-100 p-3"
                        >
                          <div className="flex-1 min-w-0">
                            {/* CartItem has no denormalized product name (unlike OrderItem) — see
                                docs/api-mapping/commerce.md. Showing a short id rather than
                                fabricating a product name that isn't actually stored. */}
                            <p className="truncate text-sm font-medium text-slate-800">Item #{item.productId.slice(0, 8)}</p>
                            <p className="text-xs text-slate-400">{money(item.unitPrice)} each</p>
                          </div>
                          <QuantityStepper
                            quantity={item.quantity}
                            disabled={updateQuantity.isPending}
                            onChange={(next) => updateQuantity.mutate({ itemId: item.id, quantity: next })}
                          />
                          <div className="w-16 shrink-0 text-right text-sm font-semibold">{money(item.lineTotal)}</div>
                          <button
                            type="button"
                            onClick={() => removeItem.mutate(item.id)}
                            className="shrink-0 rounded-full p-1.5 text-slate-300 hover:bg-red-50 hover:text-red-500"
                          >
                            <Trash2 className="h-3.5 w-3.5" />
                          </button>
                        </motion.div>
                      ))}
                    </AnimatePresence>
                  )}
                </div>

                {cart && cart.items.length > 0 && (
                  <div className="border-t border-slate-100 px-5 py-4">
                    <div className="mb-3 flex gap-2">
                      <Input
                        placeholder="Coupon code"
                        value={couponCode}
                        onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                        onKeyDown={(e) => e.key === "Enter" && handleApplyCoupon()}
                      />
                      <Button type="button" variant="outline" onClick={handleApplyCoupon} disabled={applyCoupon.isPending || !couponCode.trim()}>
                        {applyCoupon.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Tag className="h-4 w-4" />}
                      </Button>
                    </div>

                    <div className="space-y-1 text-sm">
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
                      <div className="flex justify-between pt-1 text-base font-semibold text-slate-900">
                        <span>Total</span>
                        <span>{money(cart.totalAmount)}</span>
                      </div>
                    </div>

                    <Link href="/checkout/new" onClick={close}>
                      <Button className="mt-4 w-full bg-[#5b4ef9] hover:bg-[#4a3ee0]">Checkout</Button>
                    </Link>
                  </div>
                )}
              </motion.div>
            </DialogPrimitive.Content>
          </DialogPrimitive.Portal>
        )}
      </AnimatePresence>
    </DialogPrimitive.Root>
  );
}
