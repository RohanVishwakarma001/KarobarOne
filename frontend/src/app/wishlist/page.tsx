"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Heart, Loader2, Plus, Trash2 } from "lucide-react";
import { CommerceShell } from "@/components/commerce/CommerceShell";
import { useWishlist } from "@/hooks/use-wishlist";
import { ApiError } from "@/lib/api/github";

export default function WishlistPage() {
  const { items, loading, error, addItem, removeItem, refresh } = useWishlist();
  const [showAddForm, setShowAddForm] = useState(false);
  const [productId, setProductId] = useState("");
  const [adding, setAdding] = useState(false);
  const [busyId, setBusyId] = useState<string | null>(null);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!productId.trim()) {
      toast.error("Enter a product id.");
      return;
    }
    setAdding(true);
    try {
      await addItem(productId.trim());
      setProductId("");
      setShowAddForm(false);
      toast.success("Added to wishlist.");
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not add to wishlist.");
    } finally {
      setAdding(false);
    }
  }

  async function handleRemove(id: string) {
    setBusyId(id);
    try {
      await removeItem(id);
      toast.success("Removed from wishlist.");
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not remove item.");
    } finally {
      setBusyId(null);
    }
  }

  return (
    <CommerceShell title="Wishlist" eyebrow="Orders & Payments">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mb-5 flex items-center justify-between">
          <p className="text-sm text-gray-500">Products you're keeping an eye on.</p>
          <button
            onClick={() => setShowAddForm((v) => !v)}
            className="inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white hover:bg-[#4a3ee0]"
          >
            <Plus className="h-4 w-4" /> Add product
          </button>
        </div>

        {showAddForm && (
          <form onSubmit={handleAdd} className="mb-5 flex flex-col gap-3 rounded-2xl border border-gray-200 bg-white p-5 sm:flex-row sm:items-center">
            <input
              className="flex-1 rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
              placeholder="Product ID (UUID) — no catalog page wired up yet"
              value={productId}
              onChange={(e) => setProductId(e.target.value)}
            />
            <div className="flex gap-2">
              <button disabled={adding} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
                {adding ? "Adding…" : "Add"}
              </button>
              <button type="button" onClick={() => setShowAddForm(false)} className="rounded-lg px-4 py-2 text-sm text-gray-500">
                Cancel
              </button>
            </div>
          </form>
        )}

        <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white">
          {loading && (
            <div className="flex items-center justify-center gap-2 px-6 py-16 text-sm text-gray-500">
              <Loader2 className="h-4 w-4 animate-spin" /> Loading your wishlist…
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
              <Heart className="mx-auto h-8 w-8 text-gray-300" />
              <p className="mt-4 font-medium">Your wishlist is empty</p>
              <p className="mt-1 text-sm text-gray-500">Save products you like to find them here later.</p>
            </div>
          )}
          {!loading &&
            !error &&
            items.map((item) => (
              <div key={item.id} className="flex items-center justify-between gap-4 border-b border-gray-100 p-5 last:border-0">
                <div className="flex items-center gap-4">
                  <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-xl bg-gray-100 text-center text-[10px] font-semibold text-gray-400">
                    {item.product_id.slice(0, 8)}
                  </div>
                  <div>
                    <p className="font-medium">Product {item.product_id.slice(0, 8)}</p>
                    {item.added_at && <p className="mt-1 text-sm text-gray-500">Added {new Date(item.added_at).toLocaleDateString("en-IN")}</p>}
                  </div>
                </div>
                <button
                  disabled={busyId === item.id}
                  onClick={() => handleRemove(item.id)}
                  className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-red-600 disabled:opacity-40"
                >
                  <Trash2 className="h-4 w-4" /> Remove
                </button>
              </div>
            ))}
        </div>
      </div>
    </CommerceShell>
  );
}
