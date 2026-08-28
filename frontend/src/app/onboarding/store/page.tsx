"use client"
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Loader2, Store, Zap } from "lucide-react";
import { useRequireAuth } from "@/hooks/use-require-auth";
import { ApiError } from "@/lib/api/coreClient";
import { createStore } from "@/lib/api/stores";

const slugify = (value: string) =>
  value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");

export default function OnboardingStorePage() {
  const router = useRouter();
  const { session, ready } = useRequireAuth();
  const [storeName, setStoreName] = useState("");
  const [storeSlug, setStoreSlug] = useState("");
  const [slugTouched, setSlugTouched] = useState(false);
  const [tagline, setTagline] = useState("");
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (ready && !session?.tenantId) {
      router.replace("/onboarding/business");
    }
  }, [ready, session, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session?.tenantId) return;
    setSubmitting(true);
    try {
      await createStore({
        tenantId: session.tenantId,
        storeName: storeName.trim(),
        storeSlug: storeSlug.trim(),
        tagline: tagline.trim() || undefined,
        email: email.trim() || undefined,
        mobile: mobile.trim() || undefined,
      });
      toast.success("Store created! Welcome to your dashboard.");
      router.push("/store-owner-dashboard");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not create your store.");
    } finally {
      setSubmitting(false);
    }
  };

  if (!ready || !session?.tenantId) return null;

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-2xl items-center gap-3 px-4 py-4 sm:px-6">
          <div className="bg-[#5b4ef9] p-2 rounded-lg">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Step 2 of 2</p>
            <h1 className="text-lg font-semibold text-slate-900">Create your store</h1>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-2xl px-4 py-8 sm:px-6">
        <form onSubmit={handleSubmit} className="space-y-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-500">
            <Store className="h-4 w-4" />
            Store details
          </div>

          <div>
            <label className="mb-1.5 block text-sm text-slate-700">Store name</label>
            <input
              value={storeName}
              onChange={(e) => {
                setStoreName(e.target.value);
                if (!slugTouched) setStoreSlug(slugify(e.target.value));
              }}
              required
              className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
              placeholder="Jack's Boutique"
            />
          </div>

          <div>
            <label className="mb-1.5 block text-sm text-slate-700">Store URL slug</label>
            <div className="flex items-center gap-2">
              <span className="text-sm text-slate-400">karobar.one/</span>
              <input
                value={storeSlug}
                onChange={(e) => {
                  setSlugTouched(true);
                  setStoreSlug(slugify(e.target.value));
                }}
                required
                className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                placeholder="jacks-boutique"
              />
            </div>
          </div>

          <div>
            <label className="mb-1.5 block text-sm text-slate-700">Tagline (optional)</label>
            <input
              value={tagline}
              onChange={(e) => setTagline(e.target.value)}
              className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
              placeholder="Quality products, honest prices"
            />
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            <div>
              <label className="mb-1.5 block text-sm text-slate-700">Support email (optional)</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm text-slate-700">Support mobile (optional)</label>
              <input
                value={mobile}
                onChange={(e) => setMobile(e.target.value)}
                className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full flex items-center justify-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-3 text-sm font-medium text-white hover:bg-[#4a3ee0] disabled:opacity-60"
          >
            {submitting && <Loader2 className="h-4 w-4 animate-spin" />}
            Create store
          </button>
        </form>
      </main>
    </div>
  );
}
