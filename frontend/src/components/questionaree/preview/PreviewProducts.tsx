"use client";

import { useQuestionnaire } from "@/context/questionnaire-context";
import { Package } from "lucide-react";

export function PreviewProducts() {
  const { data } = useQuestionnaire();

  return (
    <section className="border-t bg-slate-50 px-8 py-12">

      <div className="mb-8">

        <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">
          {data.businessNature === "service"
            ? "Our Services"
            : "Our Products"}
        </p>

        <h2 className="mt-2 text-3xl font-bold text-slate-900">

          {data.businessNature === "service"
            ? "What We Offer"
            : "Featured Products"}

        </h2>

      </div>

      {data.items.length === 0 ? (

        <div className="rounded-xl border-2 border-dashed border-slate-200 bg-white p-10 text-center">

          <Package className="mx-auto mb-4 h-10 w-10 text-slate-400" />

          <p className="text-slate-500">

            {data.businessNature === "service"
              ? "Your services will appear here."
              : "Your products will appear here."}

          </p>

        </div>

      ) : (

        <div className="grid gap-6 md:grid-cols-2">

          {data.items.map((item) => (

            <div
              key={item.id}
              className="overflow-hidden rounded-2xl border bg-white shadow-sm transition hover:shadow-lg"
            >

              {/* Image */}

              <div className="flex h-48 items-center justify-center bg-slate-100">

                {item.images.length > 0 ? (

                  <img
                    src={URL.createObjectURL(item.images[0])}
                    alt={item.name}
                    className="h-full w-full object-cover"
                  />

                ) : (

                  <Package className="h-14 w-14 text-slate-400" />

                )}

              </div>

              {/* Content */}

              <div className="p-5">

                <h3 className="text-xl font-semibold text-slate-900">

                  {item.name || "Product Name"}

                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-600">

                  {item.shortDescription ||
                    "Short description will appear here."}

                </p>

                {/* Pricing */}

                {(item.salePrice ||
                  item.listPrice ||
                  item.mrp) && (

                  <div className="mt-5 flex items-center gap-3">

                    {item.salePrice && (

                      <span className="text-xl font-bold text-blue-600">

                        ₹{item.salePrice}

                      </span>

                    )}

                    {item.listPrice && (

                      <span className="text-sm text-slate-400 line-through">

                        ₹{item.listPrice}

                      </span>

                    )}

                    {item.discount && (

                      <span className="rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-700">

                        {item.discount}% OFF

                      </span>

                    )}

                  </div>

                )}

              </div>

            </div>

          ))}

        </div>

      )}

    </section>
  );
}