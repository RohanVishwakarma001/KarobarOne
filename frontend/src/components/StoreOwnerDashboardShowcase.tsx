const stories = [
  {
    label: "Dashboard",
    code: "DB",
    title: "Daily store overview",
    description:
      "Sales, orders, stock alerts, and staff status appear together in one clean dashboard view.",
    stats: [
      { label: "Sales today", value: "Rs 1,28,450" },
      { label: "Open orders", value: "42" },
      { label: "Low stock items", value: "6" },
    ],
  },
  {
    label: "Store profile",
    code: "SP",
    title: "Store profile settings",
    description:
      "Store name, contact details, and brand information stay organized in one place.",
    stats: [
      { label: "Outlet count", value: "3" },
      { label: "Rating", value: "4.8/5" },
      { label: "Profile", value: "92%" },
    ],
  },
  {
    label: "Website management",
    code: "WM",
    title: "Website management panel",
    description:
      "Edit homepage blocks, banners, and published content without changing the rest of the site.",
    stats: [
      { label: "Sections", value: "10" },
      { label: "Live updates", value: "4" },
      { label: "Publish queue", value: "2" },
    ],
  },
  {
    label: "Customer management",
    code: "CM",
    title: "Customer management panel",
    description:
      "See customer records, repeat buyers, recent orders, and follow-up actions in one list.",
    stats: [
      { label: "Customers", value: "1,234" },
      { label: "Repeat rate", value: "38%" },
      { label: "Tickets", value: "12" },
    ],
  },
  {
    label: "Staff management",
    code: "SM",
    title: "Staff management panel",
    description:
      "Assign work, track shift coverage, and monitor who is active for smooth operations.",
    stats: [
      { label: "Active staff", value: "14" },
      { label: "On shift", value: "9" },
      { label: "Tasks done", value: "27" },
    ],
  },
  {
    label: "Settings",
    code: "ST",
    title: "System settings panel",
    description:
      "Permissions, notifications, and security settings are grouped for quick control.",
    stats: [
      { label: "Permission groups", value: "5" },
      { label: "Notifications", value: "On" },
      { label: "Security", value: "High" },
    ],
  },
];

export function StoreOwnerDashboardShowcase() {
  return (
    <section id="store-owner-dashboard" className="bg-white px-6 py-24">
      <div className="mx-auto max-w-7xl">
        <div className="mb-10">
          <h2 className="text-3xl font-semibold tracking-tight text-gray-900 sm:text-4xl text-center">
            Store Owner Dashboard
          </h2>
          <p className="mt-3 max-w-2xl text-sm text-gray-600 sm:text-base mx-auto text-center">
            Everything you need to monitor sales, manage products and etc.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {stories.map((story) => (
            <details
              key={story.label}
              className="group rounded-3xl border border-gray-200 bg-gray-50 p-5 shadow-sm open:border-[#5b4ef9]/30 open:bg-[#5b4ef9]/5"
            >
              <summary className="flex cursor-pointer list-none items-center gap-3">
                <span className="flex size-10 items-center justify-center rounded-xl bg-[#5b4ef9]/10 text-sm font-semibold text-[#5b4ef9]">
                  {story.code}
                </span>
                <span className="flex-1">
                  <span className="block text-sm font-medium text-gray-900">{story.label}</span>
                  <span className="block text-xs text-gray-500">Click to open content</span>
                </span>
                <span className="text-[#5b4ef9] transition group-open:rotate-90">›</span>
              </summary>

              <div className="mt-5 rounded-2xl border border-gray-200 bg-white p-4">
                <h3 className="text-xl font-semibold text-gray-900">{story.title}</h3>
                <p className="mt-2 text-sm text-gray-600">{story.description}</p>

                <div className="mt-5 grid gap-3 sm:grid-cols-3">
                  {story.stats.map((item) => (
                    <div
                      key={item.label}
                      className="rounded-2xl border border-gray-200 bg-gray-50 px-4 py-4"
                    >
                      <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
                        {item.label}
                      </p>
                      <p className="mt-2 text-2xl font-semibold text-gray-900">{item.value}</p>
                    </div>
                  ))}
                </div>
              </div>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}