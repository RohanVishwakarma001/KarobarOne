"use client";
import { useMemo, useState } from "react";
import { FileImage, FileText, Grid2X2, ImagePlus, List, MoreHorizontal, Search, Upload, Video } from "lucide-react";
import { CmsShell } from "@/components/cms/CmsShell";

const assets = [
  { id: 1, name: "storefront-hero.jpg", type: "Image", size: "1.8 MB", date: "08 Aug 2026" },
  { id: 2, name: "summer-campaign.png", type: "Image", size: "920 KB", date: "06 Aug 2026" },
  { id: 3, name: "brand-guidelines.pdf", type: "Document", size: "2.4 MB", date: "03 Aug 2026" },
  { id: 4, name: "product-demo.mp4", type: "Video", size: "18.2 MB", date: "29 Jul 2026" },
  { id: 5, name: "checkout-banner.webp", type: "Image", size: "640 KB", date: "27 Jul 2026" },
  { id: 6, name: "logo-primary.png", type: "Image", size: "184 KB", date: "25 Jul 2026" },
];

function iconFor(type: string) { if (type === "Video") return Video; if (type === "Document") return FileText; return FileImage; }

export default function MediaLibraryPage() {
  const [query, setQuery] = useState("");
  const [view, setView] = useState<"grid" | "list">("grid");
  const filtered = useMemo(() => assets.filter((asset) => asset.name.toLowerCase().includes(query.toLowerCase())), [query]);
  return <CmsShell title="Media Library">
    <div className="mx-auto max-w-7xl px-6 pb-12">
      <div className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><p className="text-sm text-gray-500">Store images, documents and media used across your storefront.</p></div><button className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2.5 text-sm font-medium text-white hover:bg-[#4a3ee0]"><Upload className="h-4 w-4" />Upload media</button></div>
      <section className="mb-6 rounded-2xl border border-dashed border-[#5b4ef9]/30 bg-[#5b4ef9]/5 p-6"><div className="flex flex-col items-center justify-center text-center"><div className="flex h-12 w-12 items-center justify-center rounded-full bg-white text-[#5b4ef9] shadow-sm"><ImagePlus className="h-6 w-6" /></div><h2 className="mt-3 font-semibold">Upload files to your media library</h2><p className="mt-1 max-w-md text-sm text-gray-500">Drag and drop files here, or choose files from your computer. This is a frontend-only upload area for now.</p><button className="mt-4 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]">Choose files</button></div></section>
      <section className="rounded-2xl border border-gray-200 bg-white"><div className="flex flex-col gap-4 border-b border-gray-200 p-5 md:flex-row md:items-center md:justify-between"><div><h2 className="font-semibold">All media</h2><p className="mt-1 text-sm text-gray-500">{filtered.length} files shown</p></div><div className="flex items-center gap-3"><div className="relative w-full sm:w-64"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search media" className="w-full rounded-lg border border-gray-200 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-[#5b4ef9]" /></div><div className="hidden rounded-lg border border-gray-200 p-1 sm:flex"><button onClick={() => setView("grid")} className={`rounded-md p-2 ${view === "grid" ? "bg-[#5b4ef9]/10 text-[#5b4ef9]" : "text-gray-500"}`} aria-label="Grid view"><Grid2X2 className="h-4 w-4" /></button><button onClick={() => setView("list")} className={`rounded-md p-2 ${view === "list" ? "bg-[#5b4ef9]/10 text-[#5b4ef9]" : "text-gray-500"}`} aria-label="List view"><List className="h-4 w-4" /></button></div></div></div>
      {view === "grid" ? <div className="grid gap-4 p-5 sm:grid-cols-2 lg:grid-cols-3">{filtered.map((asset) => { const Icon = iconFor(asset.type); return <div key={asset.id} className="group overflow-hidden rounded-xl border border-gray-200"><div className="flex h-36 items-center justify-center bg-gray-50 text-[#5b4ef9]"><Icon className="h-10 w-10" /></div><div className="p-4"><div className="flex items-start justify-between gap-2"><div className="min-w-0"><p className="truncate text-sm font-medium">{asset.name}</p><p className="mt-1 text-xs text-gray-500">{asset.type} · {asset.size}</p></div><button className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-50 hover:text-gray-700" aria-label="More"><MoreHorizontal className="h-4 w-4" /></button></div><p className="mt-3 text-xs text-gray-400">Added {asset.date}</p></div></div> })}</div> : <div className="overflow-x-auto"><table className="w-full min-w-[650px] text-left text-sm"><thead className="bg-gray-50 text-xs uppercase tracking-wide text-gray-500"><tr><th className="px-5 py-3">File</th><th className="px-5 py-3">Type</th><th className="px-5 py-3">Size</th><th className="px-5 py-3">Added</th><th></th></tr></thead><tbody>{filtered.map((asset) => { const Icon = iconFor(asset.type); return <tr key={asset.id} className="border-t border-gray-100"><td className="px-5 py-4"><div className="flex items-center gap-3"><div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#5b4ef9]/10 text-[#5b4ef9]"><Icon className="h-4 w-4" /></div><span className="font-medium">{asset.name}</span></div></td><td className="px-5 py-4 text-gray-600">{asset.type}</td><td className="px-5 py-4 text-gray-600">{asset.size}</td><td className="px-5 py-4 text-gray-600">{asset.date}</td><td className="px-5 py-4 text-right"><button className="rounded-lg p-2 text-gray-400 hover:bg-gray-50 hover:text-gray-700"><MoreHorizontal className="h-4 w-4" /></button></td></tr> })}</tbody></table></div>}
      </section>
    </div>
  </CmsShell>;
}
