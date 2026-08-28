"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"
import { StepWrapper } from "../step-wrapper"
import { NavigationButtons } from "../navigation-buttons"
import { Check } from "lucide-react"

const categories = [
  {
    title: "Value & Pricing",
    phrases: [
      "Unmatched value for money",
      "Flexible payment options",
      "No lock-in contracts",
      "Pay only for what you use",
      "EMI-friendly plans available",
      "Cost-effective, not cheap",
      "Maximum ROI guaranteed",
      "Price-match promise",
    ],
  },
  {
    title: "Customer Experience",
    phrases: [
      "Client-first approach",
      "Personalized solutions",
      "We listen before we build",
      "Relationship over transactions",
      "Satisfaction before payment",
      "Multilingual customer support",
      "Hindi & regional language support",
      "Doorstep service available",
    ],
  },
  {
    title: "Innovation & Technology",
    phrases: [
      "AI-powered solutions",
      "Future-ready technology stack",
      "Automation at the core",
      "Built for scale",
      "Digital-first approach",
      "Cloud-native infrastructure",
      "Real-time dashboards & reporting",
      "Constantly evolving with trends",
    ],
  },
  {
    title: "Expertise & Team",
    phrases: [
      "Certified domain experts",
      "In-house specialized team",
      "No freelancer dependency",
      "Decades of combined experience",
      "Senior-led project execution",
      "Trained and background-checked staff",
      "Continuous team upskilling",
    ],
  },
  {
    title: "Process & Delivery",
    phrases: [
      "End-to-end project ownership",
      "Agile delivery methodology",
      "Weekly progress updates",
      "Hassle-free onboarding",
      "Quick turnaround time",
      "Zero compromise on quality",
      "Documented processes",
      "Post-delivery support included",
    ],
  },
  {
    title: "Results & Growth",
    phrases: [
      "Measurable results, not promises",
      "Data-driven decision making",
      "Growth-focused mindset",
      "Proven track record",
      "Scalable as your business grows",
      "Results visible within 30 days",
    ],
  },
  {
    title: "India-Specific Advantage",
    phrases: [
      "Made for India, built for Bharat",
      "Understands Indian business culture",
      "UPI & Indian payment integrations",
      "Compliant with Indian regulations",
      "Tier 2 & Tier 3 city experience",
      "Festival & seasonal ready",
      "Local market insights built in",
    ],
  },
]

export function Step12AWhyChooseUs() {
  const { data, updateData } = useQuestionnaire()

  const togglePhrase = (phrase: string) => {
    const current = data.whyChooseUs || []
    const updated = current.includes(phrase)
      ? current.filter((p) => p !== phrase)
      : [...current, phrase]
    updateData({ whyChooseUs: updated })
  }

  return (
    <StepWrapper
      title="Why Choose Us"
      description="Select the phrases that best describe why customers should choose your business."
    >
      <div className="grid gap-8">
        {categories.map((category) => (
          <div key={category.title} className="grid gap-3">
            <h3 className="font-medium text-foreground text-sm uppercase tracking-wide text-muted-foreground">
              {category.title}
            </h3>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {category.phrases.map((phrase) => {
                const selected = data.whyChooseUs?.includes(phrase) || false
                return (
                  <button
                    key={phrase}
                    type="button"
                    onClick={() => togglePhrase(phrase)}
                    className={`flex items-center gap-2 px-4 py-3 rounded-xl border-2 text-sm font-medium text-left transition-colors ${
                      selected
                        ? "border-accent bg-accent/10 text-foreground"
                        : "border-border bg-card text-muted-foreground hover:border-muted-foreground/40"
                    }`}
                  >
                    {selected && <Check className="w-4 h-4 text-accent shrink-0" />}
                    <span>{phrase}</span>
                  </button>
                )
              })}
            </div>
          </div>
        ))}
      </div>

      {data.whyChooseUs && data.whyChooseUs.length > 0 && (
        <div className="bg-muted/50 rounded-lg p-4 border border-border mt-6">
          <p className="text-sm text-muted-foreground">
            Selected: <span className="font-medium text-foreground">{data.whyChooseUs.length} phrase(s)</span>
          </p>
        </div>
      )}

      <NavigationButtons />
    </StepWrapper>
  )
}