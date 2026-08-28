"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { FileText, ShieldCheck, ClipboardList, Images, Menu, X, ChevronRight } from "lucide-react";
import { useState } from "react";

const links = [
  { href: "/blog", label: "Blog", icon: FileText },
  { href: "/policies", label: "Policies", icon: ShieldCheck },
  { href: "/forms", label: "Forms", icon: ClipboardList },
  { href: "/media-library", label: "Media Library", icon: Images },
];

export function CmsShell({ children, title, eyebrow = "Blog & CMS" }: { children: React.ReactNode; title: string; eyebrow?: string }) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center gap-3">
            <Image src="/Logo.jpeg" alt="KarobarOne" width={44} height={44} className="rounded-md object-contain" />
            <div>
              <p className="text-lg font-semibold tracking-tight">KarobarOne</p>
              <p className="hidden text-[11px] text-gray-500 sm:block">Commerce workspace</p>
            </div>
          </Link>

          <nav className="hidden items-center gap-2 md:flex">
            {links.map(({ href, label, icon: Icon }) => {
              const active = pathname === href;
              return (
                <Link key={href} href={href} className={`inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm transition-colors ${active ? "bg-[#5b4ef9]/10 text-[#5b4ef9]" : "text-gray-600 hover:bg-gray-50 hover:text-[#5b4ef9]"}`}>
                  <Icon className="h-4 w-4" />
                  {label}
                </Link>
              );
            })}
          </nav>

          <div className="hidden items-center gap-3 md:flex">
            <Link href="/" className="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]">Home</Link>
            <Link href="/login" className="rounded-lg bg-[#5b4ef9] px-5 py-2 text-sm font-medium text-white transition hover:bg-[#4a3ee0]">Login</Link>
          </div>

          <button aria-label="Open navigation" onClick={() => setOpen(!open)} className="rounded-lg bg-[#5b4ef9] p-2 md:hidden">
            {open ? <X className="h-5 w-5 text-white" /> : <Menu className="h-5 w-5 text-white" />}
          </button>
        </div>
        {open && (
          <div className="border-t border-gray-200 px-6 pb-5 pt-3 md:hidden">
            <div className="flex flex-col gap-1">
              {links.map(({ href, label, icon: Icon }) => (
                <Link key={href} href={href} onClick={() => setOpen(false)} className="flex items-center gap-3 rounded-lg px-3 py-3 text-sm text-gray-700 hover:bg-gray-50 hover:text-[#5b4ef9]">
                  <Icon className="h-4 w-4" />{label}
                </Link>
              ))}
              <Link href="/login" onClick={() => setOpen(false)} className="mt-2 rounded-lg bg-[#5b4ef9] px-4 py-3 text-center text-sm font-medium text-white">Login</Link>
            </div>
          </div>
        )}
      </header>

      <main>
        <div className="mx-auto max-w-7xl px-6 pt-8 sm:pt-10">
          <div className="mb-8 flex flex-wrap items-center gap-2 text-sm text-gray-500">
            <Link href="/" className="hover:text-[#5b4ef9]">Home</Link>
            <ChevronRight className="h-4 w-4" />
            <span className="text-gray-900">{title}</span>
          </div>
          <div className="mb-8">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#5b4ef9]">{eyebrow}</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">{title}</h1>
          </div>
        </div>
        {children}
      </main>

      <footer className="mt-20 border-t border-gray-200 bg-gray-50">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-8 text-sm text-gray-500 sm:flex-row sm:items-center sm:justify-between">
          <p>© {new Date().getFullYear()} KarobarOne. Built for profitable commerce.</p>
          <div className="flex gap-5"><Link href="/under-maintenance" className="hover:text-[#5b4ef9]">Help Center</Link><Link href="/under-maintenance" className="hover:text-[#5b4ef9]">Privacy</Link><Link href="/under-maintenance" className="hover:text-[#5b4ef9]">Terms</Link></div>
        </div>
      </footer>
    </div>
  );
}
