const sections = [
  {
    title: "Website Builder",
    description: "Simple builder for homepage and marketing pages.",
    items: ["Hero", "About", "Selling section", "Contact", "CMS editor", "Live preview", "Publish workflow"],
  },
];

export function WebsiteBuilder() {
  return (
    <section id="website-builder" className="bg-white px-6 py-24">
      <div className="mx-auto max-w-7xl">
        <div className="mb-10 text-center">
          <p className="text-xs uppercase tracking-[0.24em] text-gray-500">Website Builder</p>
          <h2 className="mt-2 text-3xl font-semibold tracking-tight text-gray-900 sm:text-4xl">
            Website Builder
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm text-gray-600 sm:text-base">
            A simple website builder for editing pages, previewing changes, and publishing updates.
          </p>
        </div>

        <div className="grid gap-6">
          {sections.map((section) => (
            <article
              key={section.title}
              className="rounded-3xl border border-gray-200 bg-gray-50 p-6 shadow-sm transition hover:-translate-y-1 hover:border-[#5b4ef9]/25 hover:bg-[#5b4ef9]/5 hover:shadow-md"
            >
              <p className="text-xs uppercase tracking-[0.24em] text-gray-500">{section.title}</p>
              <h3 className="mt-2 text-2xl font-semibold text-gray-900">{section.title}</h3>
              <p className="mt-3 text-sm leading-6 text-gray-600">{section.description}</p>

              <div className="mt-5 flex flex-wrap gap-2">
                {section.items.map((item) => (
                  <span
                    key={item}
                    className="rounded-full border border-gray-200 bg-white px-3 py-1.5 text-xs font-medium text-gray-600 transition hover:border-[#5b4ef9]/25 hover:bg-[#5b4ef9] hover:text-white"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
