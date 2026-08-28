import Link from "next/link";

type Story = {
  code: string;
  title: string;
  timeline: string;
  description: string;
};

const stories: Story[] = [
  {
    code: "DB",
    title: "Dashboard",
    timeline: "1",
    description: "Sales, orders, alerts, and daily activity in one simple view.",
  },
  {
    code: "SP",
    title: "Store profile",
    timeline: "1",
    description: "Store name, contacts, brand info, and profile settings.",
  },
  {
    code: "WM",
    title: "Website management",
    timeline: "3",
    description: "Homepage blocks, banners, content edits, and publish flow.",
  },
  {
    code: "CM",
    title: "Customer management",
    timeline: "1",
    description: "Customer records, repeat buyers, and follow-up notes.",
  },
  {
    code: "SM",
    title: "Staff management",
    timeline: "1",
    description: "Shift coverage, responsibilities, and active staff tracking.",
  },
  {
    code: "ST",
    title: "Settings",
    timeline: "1",
    description: "Permissions, notifications, and basic security controls.",
  },
];

const stats = [
  { label: "Modules", value: "6", icon: "MD" },
  { label: "Timeline", value: "8", icon: "TL" },
  { label: "Coverage", value: "Store ops", icon: "SO" },
  { label: "Access", value: "Role based", icon: "RB" },
];

const portalChips = [
  "Project Setup & Architecture",
  "Authentication & User Management",
  "Platform Admin Portal",
  "Store Owner Dashboard",
  "Website Builder",
  "Product Management",
  "Service Management",
];

export default function StoreOwnerDashboardPage() {
  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex size-11 items-center justify-center rounded-2xl bg-[#5b4ef9]/10 text-sm font-semibold text-[#5b4ef9]">
              SO
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">
                Store owner portal
              </p>
              <h1 className="text-lg font-semibold text-slate-900">Store Owner Dashboard</h1>
            </div>
          </div>

          <Link
            href="/"
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
          >
            <span aria-hidden="true">{"<"}</span>
            Home
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <section className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Overview</p>
                <h2 className="mt-2 text-3xl font-semibold tracking-tight">
                  Clean dashboard for daily store work
                </h2>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">
                  This page keeps the same store-owner features you shared in the screenshot, but
                  presents them in a simple and normal UI that matches the rest of the website.
                </p>
              </div>

              <div className="rounded-2xl bg-[#5b4ef9]/5 px-4 py-3 text-sm text-slate-700">
                <p className="font-medium text-slate-900">Included sections</p>
                <p className="mt-1">Dashboard, profile, website, customers, staff, settings</p>
              </div>
            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
              {stats.map((item) => (
                <div
                  key={item.label}
                  className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <span className="flex size-9 items-center justify-center rounded-xl bg-white text-xs font-semibold text-[#5b4ef9] shadow-sm">
                        {item.icon}
                      </span>
                      <span className="text-sm text-slate-600">{item.label}</span>
                    </div>
                    <span className="text-lg font-semibold text-slate-900">{item.value}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 rounded-3xl border border-slate-200 bg-white p-5">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-sm font-medium text-slate-900">Quick flow</p>
                  <p className="mt-1 text-sm text-slate-600">
                    Dashboard to profile to settings is kept simple and easy to scan.
                  </p>
                </div>
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <span className="rounded-full border border-slate-200 px-3 py-1">Dashboard</span>
                  <span aria-hidden="true">{"->"}</span>
                  <span className="rounded-full border border-slate-200 px-3 py-1">Profile</span>
                  <span aria-hidden="true">{"->"}</span>
                  <span className="rounded-full border border-slate-200 px-3 py-1">Settings</span>
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Module list</p>
                <h2 className="mt-2 text-2xl font-semibold">Stories included in the dashboard</h2>
              </div>
              <div className="rounded-full bg-[#5b4ef9]/10 px-3 py-1 text-sm font-medium text-[#5b4ef9]">
                Timeline 8
              </div>
            </div>

            <div className="mt-5 space-y-3">
              {stories.map((story, index) => (
                <div
                  key={story.code}
                  className={`rounded-2xl border p-4 transition ${
                    index === 0
                      ? "border-[#5b4ef9]/25 bg-[#5b4ef9]/5"
                      : "border-slate-200 bg-white hover:bg-slate-50"
                  }`}
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3">
                      <span className="flex size-10 items-center justify-center rounded-xl bg-[#5b4ef9]/10 text-sm font-semibold text-[#5b4ef9]">
                        {story.code}
                      </span>
                      <div>
                        <p className="text-sm font-medium text-slate-900">{story.title}</p>
                        <p className="mt-1 text-sm text-slate-600">{story.description}</p>
                      </div>
                    </div>
                    <span className="rounded-full border border-slate-200 bg-white px-2.5 py-1 text-xs text-slate-600">
                      {story.timeline}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="mt-6 rounded-3xl border border-slate-200 bg-white shadow-sm">
          <div className="flex flex-col gap-4 border-b border-slate-200 px-6 py-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Detail view</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-900">
                Same structure as the screenshot
              </h2>
              <p className="mt-2 text-sm text-slate-600">
                Simple row-based layout, no heavy styling, and easy to read on the homepage theme.
              </p>
            </div>
            <div className="flex items-center gap-3 text-sm text-slate-500">
              <span className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1">
                <span className="text-xs font-semibold text-[#5b4ef9]">ST</span>
                Store team
              </span>
              <span className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1">
                <span className="text-xs font-semibold text-[#5b4ef9]">SG</span>
                Settings
              </span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-[760px] w-full border-separate border-spacing-0">
              <thead className="bg-slate-50">
                <tr>
                  <th className="border-b border-slate-200 px-6 py-4 text-left text-sm font-semibold text-slate-700">
                    Code
                  </th>
                  <th className="border-b border-slate-200 px-6 py-4 text-left text-sm font-semibold text-slate-700">
                    Story
                  </th>
                  <th className="border-b border-slate-200 px-6 py-4 text-left text-sm font-semibold text-slate-700">
                    Timeline
                  </th>
                  <th className="border-b border-slate-200 px-6 py-4 text-left text-sm font-semibold text-slate-700">
                    Purpose
                  </th>
                </tr>
              </thead>
              <tbody>
                {stories.map((story, index) => (
                  <tr key={story.code} className="hover:bg-[#5b4ef9]/[0.03]">
                    <td
                      className={`border-b border-slate-100 px-6 py-4 text-sm font-medium ${
                        index === 0 ? "bg-[#5b4ef9]/[0.03]" : ""
                      }`}
                    >
                      {story.code}
                    </td>
                    <td
                      className={`border-b border-slate-100 px-6 py-4 text-sm text-slate-800 ${
                        index === 0 ? "bg-[#5b4ef9]/[0.03]" : ""
                      }`}
                    >
                      {story.title}
                    </td>
                    <td className="border-b border-slate-100 px-6 py-4 text-sm text-slate-600">
                      {story.timeline}
                    </td>
                    <td className="border-b border-slate-100 px-6 py-4 text-sm text-slate-600">
                      {story.description}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="mt-6 rounded-3xl border border-[#5b4ef9]/15 bg-[linear-gradient(180deg,rgba(91,78,249,0.08),#ffffff)] shadow-sm">
          <div className="flex flex-col gap-4 px-6 py-6 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-[#5b4ef9]">Platform portal</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-950">
                Need the admin control room too?
              </h2>
              <p className="mt-2 max-w-2xl text-sm text-slate-600">
                The platform admin portal is now available in its own folder and route, with all
                the modules from the screenshot mapped into a web UI.
              </p>
            </div>

            <Link
              href="/platform-admin-portal"
              className="inline-flex items-center gap-2 rounded-full bg-[#5b4ef9] px-5 py-3 text-sm font-medium text-white transition hover:bg-[#4a3ee0]"
            >
              Open platform admin portal
              <span aria-hidden="true">{"->"}</span>
            </Link>
          </div>

          <div className="border-t border-slate-200 px-6 py-5">
            <div className="flex flex-wrap gap-2">
              {portalChips.map((item) => (
                <span
                  key={item}
                  className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-600"
                >
                  {item}
                </span>
              ))}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
