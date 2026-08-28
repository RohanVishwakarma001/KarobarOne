"use client";

import { PreviewHero } from "./PreviewHero";
import { PreviewAbout } from "./PreviewAbout";
import { PreviewProducts } from "./PreviewProducts";
import { PreviewContact } from "./PreviewContact";

export function LiveWebsitePreview() {
  return (
    <div className="sticky top-24 h-[calc(100vh-120px)] overflow-hidden">

      <div className="flex h-full flex-col overflow-hidden rounded-2xl border bg-white shadow-xl">

        {/* Browser */}

        <div className="flex items-center gap-2 border-b bg-slate-100 px-4 py-3">

          <div className="h-3 w-3 rounded-full bg-red-400" />
          <div className="h-3 w-3 rounded-full bg-yellow-400" />
          <div className="h-3 w-3 rounded-full bg-green-400" />

          <div className="ml-4 flex-1 rounded bg-white px-3 py-1 text-xs text-gray-500">
            https://preview.yourbusiness.com
          </div>

        </div>

        {/* Scroll */}

        <div className="flex-1 overflow-y-auto">

          <PreviewHero />

          <PreviewAbout />

          <PreviewProducts />

          <PreviewContact />

        </div>

      </div>

    </div>
  );
}