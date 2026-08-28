"use client";
import { useMemo, useState } from "react";
import { Calendar, Edit3, Eye, FileText, Plus, Search, MoreHorizontal } from "lucide-react";
import { CmsShell } from "@/components/cms/CmsShell";

const posts = [
  { id: 1, title: "How to build a profitable D2C storefront", category: "Growth", author: "Harsh", date: "08 Aug 2026", status: "Published", views: 1248 },
  { id: 2, title: "7 ways to improve checkout conversion", category: "Conversion", author: "Harsh", date: "04 Aug 2026", status: "Published", views: 892 },
  { id: 3, title: "WhatsApp commerce playbook for Indian brands", category: "Marketing", author: "Harsh", date: "01 Aug 2026", status: "Draft", views: 0 },
  { id: 4, title: "Shipping strategy for growing stores", category: "Operations", author: "Harsh", date: "27 Jul 2026", status: "Scheduled", views: 0 },
];

const statusClass: Record<string, string> = {
  Published: "bg-emerald-50 text-emerald-700",
  Draft: "bg-gray-100 text-gray-600",
  Scheduled: "bg-amber-50 text-amber-700",
};

export default function BlogPage() {
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("All");
  const filtered = useMemo(() => posts.filter((post) => post.title.toLowerCase().includes(query.toLowerCase()) && (status === "All" || post.status === status)), [query, status]);

  return <CmsShell title="Blog">
    <div className="mx-auto max-w-7xl px-6 pb-12">
      <div className="mb-6 grid gap-4 sm:grid-cols-3">
        {[['Total Posts', '24'], ['Published', '18'], ['Drafts', '4']].map(([label, value]) => <div key={label} className="rounded-2xl border border-gray-200 bg-white p-5"><p className="text-sm text-gray-500">{label}</p><p className="mt-2 text-2xl font-semibold">{value}</p></div>)}
      </div>
      <section className="rounded-2xl border border-gray-200 bg-white">
        <div className="flex flex-col gap-4 border-b border-gray-200 p-5 lg:flex-row lg:items-center lg:justify-between">
          <div><h2 className="font-semibold">Manage posts</h2><p className="mt-1 text-sm text-gray-500">Create, edit and publish content for your storefront.</p></div>
          <button className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2.5 text-sm font-medium text-white hover:bg-[#4a3ee0]"><Plus className="h-4 w-4" />New post</button>
        </div>
        <div className="flex flex-col gap-3 border-b border-gray-100 p-5 sm:flex-row">
          <div className="relative flex-1"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search posts" className="w-full rounded-lg border border-gray-200 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-[#5b4ef9]" /></div>
          <select value={status} onChange={(e) => setStatus(e.target.value)} className="rounded-lg border border-gray-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"><option>All</option><option>Published</option><option>Draft</option><option>Scheduled</option></select>
        </div>
        <div className="overflow-x-auto"><table className="w-full min-w-[760px] text-left text-sm"><thead className="bg-gray-50 text-xs uppercase tracking-wide text-gray-500"><tr><th className="px-5 py-3">Post</th><th className="px-5 py-3">Category</th><th className="px-5 py-3">Date</th><th className="px-5 py-3">Status</th><th className="px-5 py-3">Views</th><th className="px-5 py-3"></th></tr></thead><tbody>{filtered.map((post) => <tr key={post.id} className="border-t border-gray-100"><td className="px-5 py-4"><div className="flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#5b4ef9]/10 text-[#5b4ef9]"><FileText className="h-5 w-5" /></div><div><p className="font-medium">{post.title}</p><p className="text-xs text-gray-500">By {post.author}</p></div></div></td><td className="px-5 py-4 text-gray-600">{post.category}</td><td className="px-5 py-4 text-gray-600">{post.date}</td><td className="px-5 py-4"><span className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusClass[post.status]}`}>{post.status}</span></td><td className="px-5 py-4 text-gray-600">{post.views.toLocaleString()}</td><td className="px-5 py-4"><div className="flex items-center justify-end gap-2"><button className="rounded-lg p-2 text-gray-500 hover:bg-gray-50 hover:text-[#5b4ef9]" aria-label="View"><Eye className="h-4 w-4" /></button><button className="rounded-lg p-2 text-gray-500 hover:bg-gray-50 hover:text-[#5b4ef9]" aria-label="Edit"><Edit3 className="h-4 w-4" /></button><button className="rounded-lg p-2 text-gray-500 hover:bg-gray-50 hover:text-[#5b4ef9]" aria-label="More"><MoreHorizontal className="h-4 w-4" /></button></div></td></tr>)}</tbody></table></div>
      </section>
    </div>
  </CmsShell>;
}
