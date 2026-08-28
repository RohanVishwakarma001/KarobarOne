"use client";

import { useQuestionnaire } from "@/context/questionnaire-context";
import {
  BadgeCheck,
  CheckCircle2,
  ShieldCheck,
  Target,
  Sparkles,
} from "lucide-react";

export function PreviewUSP() {
  const { data } = useQuestionnaire();

  const hasUSP =
    data.businessUSP.length > 0 ||
    data.whyChooseUs.length > 0 ||
    data.problemSolved ||
    data.uniqueSolution ||
    data.trustCredibility ||
    data.missionVision;

  return (
    <section className="border-t bg-gradient-to-b from-slate-50 to-white px-8 py-12">

      <div className="mb-10 text-center">

        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-600">
          Why Customers Trust Us
        </p>

        <h2 className="mt-2 text-3xl font-bold text-slate-900">
          What Makes Us Different
        </h2>

      </div>

      {!hasUSP ? (
        <div className="rounded-2xl border-2 border-dashed border-slate-200 bg-white p-10 text-center">

          <Sparkles className="mx-auto mb-4 h-10 w-10 text-slate-400" />

          <p className="text-slate-500">
            Your USP, Mission and Why Choose Us section
            will automatically appear here.
          </p>

        </div>
      ) : (
        <>
          {/* USP */}

          {data.businessUSP.length > 0 && (

            <div className="mb-10">

              <h3 className="mb-5 flex items-center gap-2 text-xl font-semibold">

                <BadgeCheck className="text-blue-600" />

                Business USP

              </h3>

              <div className="grid gap-4 md:grid-cols-2">

                {data.businessUSP.map((item, index) => (

                  <div
                    key={index}
                    className="flex items-start gap-3 rounded-xl border bg-white p-5 shadow-sm"
                  >

                    <CheckCircle2 className="mt-1 h-5 w-5 text-green-600" />

                    <p>{item}</p>

                  </div>

                ))}

              </div>

            </div>

          )}

          {/* Why Choose Us */}

          {data.whyChooseUs.length > 0 && (

            <div className="mb-10">

              <h3 className="mb-5 flex items-center gap-2 text-xl font-semibold">

                <ShieldCheck className="text-blue-600" />

                Why Choose Us

              </h3>

              <div className="grid gap-4 md:grid-cols-2">

                {data.whyChooseUs.map((item, index) => (

                  <div
                    key={index}
                    className="rounded-xl bg-blue-50 p-5"
                  >

                    <div className="mb-2 font-semibold text-blue-700">

                      Advantage {index + 1}

                    </div>

                    <p>{item}</p>

                  </div>

                ))}

              </div>

            </div>

          )}

          {/* Problem + Solution */}

          {(data.problemSolved || data.uniqueSolution) && (

            <div className="grid gap-6 md:grid-cols-2">

              <div className="rounded-xl border p-6">

                <h4 className="mb-3 flex items-center gap-2 font-semibold">

                  <Target className="text-red-500" />

                  Problem We Solve

                </h4>

                <p className="text-slate-600">

                  {data.problemSolved || "No information"}

                </p>

              </div>

              <div className="rounded-xl border p-6">

                <h4 className="mb-3 flex items-center gap-2 font-semibold">

                  <BadgeCheck className="text-green-600" />

                  Our Solution

                </h4>

                <p className="text-slate-600">

                  {data.uniqueSolution || "No information"}

                </p>

              </div>

            </div>

          )}

          {/* Trust */}

          {data.trustCredibility && (

            <div className="mt-10 rounded-2xl bg-slate-900 p-8 text-white">

              <h3 className="mb-4 text-2xl font-semibold">

                Trusted By Customers

              </h3>

              <p className="leading-8 text-slate-300">

                {data.trustCredibility}

              </p>

            </div>

          )}
        </>
      )}
    </section>
  );
}