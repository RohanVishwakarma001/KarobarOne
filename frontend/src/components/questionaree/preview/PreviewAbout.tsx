"use client";

import { useQuestionnaire } from "@/context/questionnaire-context";
import { Building2, Calendar, User } from "lucide-react";

export function PreviewAbout() {
  const { data } = useQuestionnaire();

  const hasContent =
    data.companyHistory ||
    data.promoterName ||
    data.promoterDesignation ||
    data.yearFounded ||
    data.missionVision;

  return (
    <section className="border-t bg-white px-8 py-12">

      <div className="mb-8">

        <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">
          About Us
        </p>

        <h2 className="mt-2 text-3xl font-bold text-slate-900">
          Know Our Business
        </h2>

      </div>

      {!hasContent ? (
        <div className="rounded-xl border-2 border-dashed border-slate-200 p-8">

          <p className="text-center text-slate-400">
            About section will automatically appear here when you
            fill Step 12 of the questionnaire.
          </p>

        </div>
      ) : (
        <div className="space-y-8">

          {/* Company History */}

          <div>

            <h3 className="mb-3 text-xl font-semibold text-slate-800">
              Company Story
            </h3>

            <p className="leading-8 text-slate-600">

              {data.companyHistory || "Company history not added."}

            </p>

          </div>

          {/* Founder */}

          <div className="grid gap-6 md:grid-cols-2">

            <div className="rounded-xl border p-5">

              <div className="mb-4 flex items-center gap-3">

                <User className="h-5 w-5 text-blue-600" />

                <h4 className="font-semibold">
                  Founder
                </h4>

              </div>

              <p className="font-medium">

                {data.promoterName || "Founder Name"}

              </p>

              <p className="text-sm text-slate-500">

                {data.promoterDesignation || "Designation"}

              </p>

            </div>

            <div className="rounded-xl border p-5">

              <div className="mb-4 flex items-center gap-3">

                <Calendar className="h-5 w-5 text-blue-600" />

                <h4 className="font-semibold">
                  Established
                </h4>

              </div>

              <p>

                {data.yearFounded || "20XX"}

              </p>

            </div>

          </div>

          {/* Mission */}

          <div className="rounded-xl bg-slate-50 p-6">

            <div className="mb-3 flex items-center gap-2">

              <Building2 className="h-5 w-5 text-blue-600" />

              <h3 className="font-semibold">

                Mission & Vision

              </h3>

            </div>

            <p className="leading-8 text-slate-600">

              {data.missionVision ||
                "Mission & Vision will appear here."}

            </p>

          </div>

        </div>
      )}
    </section>
  );
}