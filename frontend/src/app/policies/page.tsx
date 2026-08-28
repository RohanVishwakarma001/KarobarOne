"use client";
import { useState } from "react";
import { CheckCircle2, Edit3, FileText, Save } from "lucide-react";
import { CmsShell } from "@/components/cms/CmsShell";

const policySeed = [
  { id: "privacy", title: "Privacy Policy", description: "How customer data is collected, used and protected.", updated: "08 Aug 2026", status: "Published" },
  { id: "terms", title: "Terms & Conditions", description: "Rules and conditions for using the storefront.", updated: "05 Aug 2026", status: "Published" },
  { id: "refund", title: "Return & Refund Policy", description: "Returns, cancellations, refunds and eligibility rules.", updated: "01 Aug 2026", status: "Published" },
  { id: "shipping", title: "Shipping Policy", description: "Delivery timelines, charges and serviceable locations.", updated: "29 Jul 2026", status: "Draft" },
];

export default function PoliciesPage() {
  const [selected, setSelected] = useState(policySeed[0].id);
  const policy = policySeed.find((item) => item.id === selected)!;
  const [content, setContent] = useState(`Welcome to KarobarOne. This policy explains the terms that apply to customers using your storefront.\n\nAdd your store-specific policy content here, including responsibilities, customer rights, eligibility and contact information.`);
  const [saved, setSaved] = useState(false);

  return <CmsShell title="Policies">
    <div className="mx-auto grid max-w-7xl gap-6 px-6 pb-12 lg:grid-cols-[330px_1fr]">
      <section className="h-fit rounded-2xl border border-gray-200 bg-white">
        <div className="border-b border-gray-200 p-5"><h2 className="font-semibold">Store policies</h2><p className="mt-1 text-sm text-gray-500">Manage customer-facing legal and service policies.</p></div>
        <div className="p-3">{policySeed.map((item) => <button key={item.id} onClick={() => { setSelected(item.id); setSaved(false); }} className={`mb-1 w-full rounded-xl p-3 text-left transition ${selected === item.id ? "bg-[#5b4ef9]/10" : "hover:bg-gray-50"}`}><div className="flex items-start justify-between gap-3"><div><p className={`font-medium ${selected === item.id ? "text-[#5b4ef9]" : ""}`}>{item.title}</p><p className="mt-1 text-xs leading-5 text-gray-500">{item.description}</p></div><span className={`mt-0.5 shrink-0 rounded-full px-2 py-1 text-[10px] font-medium ${item.status === "Published" ? "bg-emerald-50 text-emerald-700" : "bg-gray-100 text-gray-600"}`}>{item.status}</span></div></button>)}</div>
      </section>
      <section className="rounded-2xl border border-gray-200 bg-white">
        <div className="flex flex-col gap-3 border-b border-gray-200 p-5 sm:flex-row sm:items-center sm:justify-between"><div><div className="flex items-center gap-2"><FileText className="h-5 w-5 text-[#5b4ef9]" /><h2 className="font-semibold">{policy.title}</h2></div><p className="mt-1 text-sm text-gray-500">Last updated {policy.updated}</p></div><button onClick={() => setSaved(true)} className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2.5 text-sm font-medium text-white hover:bg-[#4a3ee0]"><Save className="h-4 w-4" />Save changes</button></div>
        <div className="p-5"><label className="text-sm font-medium">Policy content</label><textarea value={content} onChange={(e) => { setContent(e.target.value); setSaved(false); }} className="mt-2 min-h-[390px] w-full resize-y rounded-xl border border-gray-200 p-4 text-sm leading-7 outline-none focus:border-[#5b4ef9]" /><div className="mt-4 flex items-center gap-2 text-xs text-gray-500"><Edit3 className="h-4 w-4" />Changes are shown on the storefront after publishing.</div>{saved && <div className="mt-4 flex items-center gap-2 rounded-xl bg-emerald-50 p-3 text-sm text-emerald-700"><CheckCircle2 className="h-4 w-4" />Policy changes saved as a frontend demo state.</div>}</div>
      </section>
    </div>
  </CmsShell>;
}
