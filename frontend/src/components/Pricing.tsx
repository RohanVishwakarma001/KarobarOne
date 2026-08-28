"use client";

import { useState } from "react";
import { Check } from "lucide-react";
import GlassModal from "@/components/GlassModal";

const plans = [
  {
    name: "Starter",
    price: "₹0",
    period: "Subscription Fee",
    description: "Perfect for getting started",
    features: [
      "Basic website setup",
      "5 products",
      "Payment gateway integration",
      "Email support",
      "2% transaction fee",
    ],
  },
  {
    name: "Growth",
    price: "₹2,999",
    period: "per month",
    description: "For growing businesses",
    features: [
      "Advanced website features",
      "Unlimited products",
      "Marketing tools",
      "WhatsApp integration",
      "Priority support",
      "1.5% transaction fee",
    ],
  },
  {
    name: "Pro",
    price: "₹5,999",
    period: "per month",
    description: "For established brands",
    features: [
      "Custom design & development",
      "Advanced analytics",
      "Dedicated account manager",
      "API access",
      "24/7 phone support",
      "1% transaction fee",
    ],
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "pricing",
    description: "For large-scale operations",
    features: [
      "White-label solution",
      "Custom integrations",
      "Multi-store management",
      "Advanced security",
      "SLA guarantee",
      "Negotiable transaction fee",
    ],
  },
];

export function Pricing() {
  const [selectedPlanIndex, setSelectedPlanIndex] = useState<number | null>(null);

  const selectedPlan = selectedPlanIndex !== null ? plans[selectedPlanIndex] : null;
  const isEnterprise = selectedPlanIndex === 3;

  return (
    <section id="pricing" className="bg-gray-50 py-24">
      <div className="mx-auto max-w-7xl px-6">
        <div className="text-center mb-16">
          <h2 className="mb-4 text-4xl font-bold text-gray-900">Simple, Transparent Pricing</h2>
          <p className="text-xl text-gray-600">Choose the plan that fits your business needs</p>
          <div className="mt-6 inline-block rounded-lg border border-green-300 bg-green-100 px-6 py-3">
            <p className="font-semibold text-green-800">
              🎉 Special Offer: ₹0 subscription fee for first 3 months!
            </p>
          </div>
        </div>

        <div className="grid gap-8 md:grid-cols-2">
          {plans.map((plan, index) => (
            <div
              key={plan.name}
              className={`rounded-2xl border bg-white p-8 ${
                index === 0
                  ? "border-[#5b4ef9] ring-2 ring-[#5b4ef9]/50"
                  : "border-gray-200"
              }`}
            >
              <div className="mb-6">
                <h3 className="mb-2 text-2xl font-bold text-gray-900">{plan.name}</h3>
                <p className="mb-4 text-gray-600">{plan.description}</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-bold text-[#5b4ef9]">{plan.price}</span>
                  <span className="text-gray-600">/ {plan.period}</span>
                </div>
              </div>

              <ul className="mb-8 space-y-3">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3">
                    <div className="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-[#5b4ef9]/10">
                      <Check className="h-3 w-3 text-[#5b4ef9]" />
                    </div>
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={() => setSelectedPlanIndex(index)}
                className={`w-full rounded-lg py-3 transition-colors ${
                  index === 0
                    ? "bg-[#5b4ef9] text-white hover:bg-[#4a3ee0]"
                    : "bg-gray-100 text-gray-900 hover:bg-gray-200"
                }`}
              >
                {index === 3 ? "Contact Sales" : "Get Started"}
              </button>
            </div>
          ))}
        </div>
      </div>

      <GlassModal
        isOpen={selectedPlan !== null}
        onClose={() => setSelectedPlanIndex(null)}
        title={selectedPlan ? `${selectedPlan.name} Plan` : ""}
      >
        {selectedPlan && (
          <div className="space-y-4">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-white">{selectedPlan.price}</span>
              <span className="text-white/70">/ {selectedPlan.period}</span>
            </div>

            <ul className="space-y-2">
              {selectedPlan.features.map((feature) => (
                <li key={feature} className="flex items-start gap-2 text-sm text-white/90">
                  <Check className="mt-0.5 h-4 w-4 flex-shrink-0 text-[#8f87ff]" />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>

            <button
              className="mt-2 w-full rounded-lg bg-[#5b4ef9] py-3 font-medium text-white transition-colors hover:bg-[#4a3ee0]"
              onClick={() => {
                setSelectedPlanIndex(null);
              }}
            >
              {isEnterprise ? "Contact Sales" : "Continue with " + selectedPlan.name}
            </button>
          </div>
        )}
      </GlassModal>
    </section>
  );
}
