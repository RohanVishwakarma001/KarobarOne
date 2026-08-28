"use client";
import { useState } from "react";
import { ClipboardList, Eye, MessageSquare, Plus, Search, Settings2 } from "lucide-react";
import { CmsShell } from "@/components/cms/CmsShell";

const forms = [
  { id: 1, name: "Contact Us", submissions: 128, updated: "08 Aug 2026", status: "Active" },
  { id: 2, name: "Newsletter Signup", submissions: 964, updated: "07 Aug 2026", status: "Active" },
  { id: 3, name: "Product Enquiry", submissions: 76, updated: "02 Aug 2026", status: "Active" },
  { id: 4, name: "Customer Feedback", submissions: 41, updated: "25 Jul 2026", status: "Draft" },
];

export default function FormsPage() {
  const [query, setQuery] = useState("");
  const filtered = forms.filter((form) => form.name.toLowerCase().includes(query.toLowerCase()));
  return <CmsShell title="Forms">
    <div className="mx-auto max-w-7xl px-6 pb-12">
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div><p className="text-sm text-gray-500">Collect leads, enquiries and customer feedback from your storefront.</p></div><button className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2.5 text-sm font-medium text-white hover:bg-[#4a3ee0]"><Plus className="h-4 w-4" />Create form</button></div>
      <div className="mb-6 grid gap-4 sm:grid-cols-3">{[['Active Forms','3'],['Total Submissions','1,209'],['New This Week','87']].map(([label,value]) => <div key={label} className="rounded-2xl border border-gray-200 bg-white p-5"><p className="text-sm text-gray-500">{label}</p><p className="mt-2 text-2xl font-semibold">{value}</p></div>)}</div>
      <section className="rounded-2xl border border-gray-200 bg-white"><div className="flex flex-col gap-4 border-b border-gray-200 p-5 sm:flex-row sm:items-center sm:justify-between"><div><h2 className="font-semibold">Your forms</h2><p className="mt-1 text-sm text-gray-500">Manage fields and review incoming responses.</p></div><div className="relative w-full sm:w-72"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search forms" className="w-full rounded-lg border border-gray-200 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-[#5b4ef9]" /></div></div>
      <div className="overflow-x-auto"><table className="w-full min-w-[700px] text-left text-sm"><thead className="bg-gray-50 text-xs uppercase tracking-wide text-gray-500"><tr><th className="px-5 py-3">Form</th><th className="px-5 py-3">Submissions</th><th className="px-5 py-3">Updated</th><th className="px-5 py-3">Status</th><th className="px-5 py-3 text-right">Actions</th></tr></thead><tbody>{filtered.map((form) => <tr key={form.id} className="border-t border-gray-100"><td className="px-5 py-4"><div className="flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#5b4ef9]/10 text-[#5b4ef9]"><ClipboardList className="h-5 w-5" /></div><div><p className="font-medium">{form.name}</p><p className="text-xs text-gray-500">Customer-facing form</p></div></div></td><td className="px-5 py-4 font-medium">{form.submissions.toLocaleString()}</td><td className="px-5 py-4 text-gray-600">{form.updated}</td><td className="px-5 py-4"><span className={`rounded-full px-2.5 py-1 text-xs font-medium ${form.status === "Active" ? "bg-emerald-50 text-emerald-700" : "bg-gray-100 text-gray-600"}`}>{form.status}</span></td><td className="px-5 py-4"><div className="flex justify-end gap-2"><button className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 px-3 py-2 text-xs font-medium text-gray-600 hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"><Eye className="h-3.5 w-3.5" />Preview</button><button className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 px-3 py-2 text-xs font-medium text-gray-600 hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"><Settings2 className="h-3.5 w-3.5" />Edit</button><button className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 px-3 py-2 text-xs font-medium text-gray-600 hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"><MessageSquare className="h-3.5 w-3.5" />Responses</button></div></td></tr>)}</tbody></table></div></section>
    </div>
  </CmsShell>;
}
