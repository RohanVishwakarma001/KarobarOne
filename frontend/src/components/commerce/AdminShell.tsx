import Link from "next/link";

export function AdminShell({ children, title, badge }: { children: React.ReactNode; title: string; badge: string }) {
  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex size-11 items-center justify-center rounded-2xl bg-[#5b4ef9]/10 text-sm font-semibold text-[#5b4ef9]">
              {badge}
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Store owner portal</p>
              <h1 className="text-lg font-semibold text-slate-900">{title}</h1>
            </div>
          </div>

          <Link
            href="/store-owner-dashboard"
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
          >
            <span aria-hidden="true">{"<"}</span>
            Back to dashboard
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">{children}</main>
    </div>
  );
}
