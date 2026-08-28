"use client";

import { useQuestionnaire } from "@/context/questionnaire-context";
import { Phone, Mail, User, Clock } from "lucide-react";
import {
  FaFacebookF,
  FaInstagram,
  FaLinkedinIn,
} from "react-icons/fa";
export function PreviewContact() {
  const { data } = useQuestionnaire();

  return (
    <section className="border-t bg-white px-8 py-12">

      <div className="mb-8">

        <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">
          Contact Us
        </p>

        <h2 className="mt-2 text-3xl font-bold text-slate-900">
          Get In Touch
        </h2>

      </div>

      <div className="grid gap-8 lg:grid-cols-2">

        {/* Left */}

        <div className="space-y-5">

          <div className="flex items-center gap-4 rounded-xl border p-4">

            <Phone className="h-5 w-5 text-blue-600" />

            <div>
              <p className="text-xs text-slate-500">
                Phone Number
              </p>

              <p className="font-medium">
                {data.phoneNumber || "+91 XXXXX XXXXX"}
              </p>
            </div>

          </div>

          <div className="flex items-center gap-4 rounded-xl border p-4">

            <Mail className="h-5 w-5 text-blue-600" />

            <div>

              <p className="text-xs text-slate-500">
                Email
              </p>

              <p className="font-medium">
                {data.email || "contact@business.com"}
              </p>

            </div>

          </div>

          <div className="flex items-center gap-4 rounded-xl border p-4">

            <User className="h-5 w-5 text-blue-600" />

            <div>

              <p className="text-xs text-slate-500">
                Contact Person
              </p>

              <p className="font-medium">
                {data.contactPerson || "Business Owner"}
              </p>

              <p className="text-sm text-slate-500">
                {data.designation || "Owner"}
              </p>

            </div>

          </div>

        </div>

        {/* Right */}

        <div>

          <div className="rounded-xl bg-slate-50 p-6">

            <div className="mb-4 flex items-center gap-2">

              <Clock className="h-5 w-5 text-blue-600" />

              <h3 className="font-semibold">
                Business Hours
              </h3>

            </div>

            {data.daysOpen.length === 0 ? (

              <p className="text-slate-500">
                Business timings will appear here.
              </p>

            ) : (

              <div className="space-y-2">

                {data.daysOpen.map((day) => (

                  <div
                    key={day}
                    className="flex justify-between border-b pb-2"
                  >

                    <span>{day}</span>

                    <span>

                      {data.dayTimings[day]?.open || "--:--"} -{" "}
                      {data.dayTimings[day]?.close || "--:--"}

                    </span>

                  </div>

                ))}

              </div>

            )}

          </div>

          {/* Social */}

          <div className="mt-6 flex gap-4">

            <div
              className={`rounded-xl border p-3 ${
                data.facebookUrl
                  ? "text-blue-600"
                  : "text-slate-300"
              }`}
            >
              <FaFacebookF size={20} />
            </div>

            <div
              className={`rounded-xl border p-3 ${
                data.instagramUrl
                  ? "text-pink-500"
                  : "text-slate-300"
              }`}
            >
              <FaInstagram size={20} />
            </div>

            <div
              className={`rounded-xl border p-3 ${
                data.linkedinUrl
                  ? "text-blue-700"
                  : "text-slate-300"
              }`}
            >
              <FaLinkedinIn size={20} />
            </div>

          </div>

        </div>

      </div>

    </section>
  );
}