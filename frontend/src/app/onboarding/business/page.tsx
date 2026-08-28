"use client"
import { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Building2, Loader2, Zap } from "lucide-react";
import { useRequireAuth } from "@/hooks/use-require-auth";
import { ApiError } from "@/lib/api/coreClient";
import { registerTenant, type TenantCreate } from "@/lib/api/tenants";
import { saveSession } from "@/lib/auth/session";

type FormState = TenantCreate;

const initialState: FormState = {
  businessName: "",
  legalName: "",
  ownerName: "",
  email: "",
  mobile: "",
  panNumber: "",
  gstNumber: "",
  businessAddressLine1: "",
  businessAddressLine2: "",
  city: "",
  state: "",
  country: "India",
  postalCode: "",
  businessType: "",
  businessDescription: "",
};

export default function OnboardingBusinessPage() {
  const router = useRouter();
  const { ready } = useRequireAuth();
  const [form, setForm] = useState<FormState>(initialState);
  const [submitting, setSubmitting] = useState(false);

  const update = (field: keyof FormState, value: string) => setForm((prev) => ({ ...prev, [field]: value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await registerTenant({
        ...form,
        gstNumber: form.gstNumber?.trim() || undefined,
        businessAddressLine2: form.businessAddressLine2?.trim() || undefined,
      });
      if (res.accessToken && res.refreshToken) {
        saveSession({ accessToken: res.accessToken, refreshToken: res.refreshToken });
      }
      toast.success("Business registered. Now let's set up your store.");
      router.push("/onboarding/store");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not register your business.");
    } finally {
      setSubmitting(false);
    }
  };

  if (!ready) return null;

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-3xl items-center gap-3 px-4 py-4 sm:px-6">
          <div className="bg-[#5b4ef9] p-2 rounded-lg">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Step 1 of 2</p>
            <h1 className="text-lg font-semibold text-slate-900">Tell us about your business</h1>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-8 sm:px-6">
        <form onSubmit={handleSubmit} className="space-y-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <Section title="Business identity" icon={<Building2 className="h-4 w-4" />}>
            <div className="grid gap-3 sm:grid-cols-2">
              <Input label="Business name" value={form.businessName} onChange={(v) => update("businessName", v)} required />
              <Input label="Legal name" value={form.legalName} onChange={(v) => update("legalName", v)} required />
              <Input label="Owner name" value={form.ownerName} onChange={(v) => update("ownerName", v)} required />
              <Input label="Business email" type="email" value={form.email} onChange={(v) => update("email", v)} required />
              <Input label="Mobile" value={form.mobile} onChange={(v) => update("mobile", v)} required placeholder="+919876543210" hint="E.164 format, with country code" />
              <Input label="PAN number" value={form.panNumber} onChange={(v) => update("panNumber", v.toUpperCase())} required placeholder="ABCDE1234F" hint="5 letters, 4 digits, 1 letter" maxLength={10} />
              <Input label="GST number (optional)" value={form.gstNumber ?? ""} onChange={(v) => update("gstNumber", v.toUpperCase())} placeholder="22AAAAA0000A1Z5" />
              <Input label="Business type" value={form.businessType} onChange={(v) => update("businessType", v)} required />
            </div>
          </Section>

          <Section title="Business address">
            <div className="grid gap-3 sm:grid-cols-2">
              <Input label="Address line 1" value={form.businessAddressLine1} onChange={(v) => update("businessAddressLine1", v)} required className="sm:col-span-2" />
              <Input label="Address line 2 (optional)" value={form.businessAddressLine2 ?? ""} onChange={(v) => update("businessAddressLine2", v)} className="sm:col-span-2" />
              <Input label="City" value={form.city} onChange={(v) => update("city", v)} required />
              <Input label="State" value={form.state} onChange={(v) => update("state", v)} required />
              <Input label="Postal code" value={form.postalCode} onChange={(v) => update("postalCode", v)} required />
              <Input label="Country" value={form.country ?? "India"} onChange={(v) => update("country", v)} />
            </div>
          </Section>

          <Section title="About the business">
            <textarea
              placeholder="What does your business sell or offer? (optional)"
              value={form.businessDescription ?? ""}
              onChange={(e) => update("businessDescription", e.target.value)}
              rows={3}
              className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
            />
          </Section>

          <button
            type="submit"
            disabled={submitting}
            className="w-full flex items-center justify-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-3 text-sm font-medium text-white hover:bg-[#4a3ee0] disabled:opacity-60"
          >
            {submitting && <Loader2 className="h-4 w-4 animate-spin" />}
            Continue to store setup
          </button>
        </form>
      </main>
    </div>
  );
}

function Section({ title, icon, children }: { title: string; icon?: React.ReactNode; children: React.ReactNode }) {
  return (
    <div>
      <p className="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-500">
        {icon}
        {title}
      </p>
      {children}
    </div>
  );
}

function Input({
  label,
  value,
  onChange,
  type = "text",
  required = false,
  className = "",
  placeholder,
  hint,
  maxLength,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  type?: string;
  required?: boolean;
  className?: string;
  placeholder?: string;
  hint?: string;
  maxLength?: number;
}) {
  return (
    <div className={className}>
      <label className="mb-1.5 block text-sm text-slate-700">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
        placeholder={placeholder}
        maxLength={maxLength}
        className="w-full rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
      />
      {hint && <p className="mt-1 text-xs text-slate-400">{hint}</p>}
    </div>
  );
}
