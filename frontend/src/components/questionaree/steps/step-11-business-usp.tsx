"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"
import { StepWrapper } from "../step-wrapper"
import { NavigationButtons } from "../navigation-buttons"
import { Check } from "lucide-react"

const uspPhrases = [
  // Credibility & Verification
  "Trusted by thousands",
  "Government registered company",
  "ISO certified",
  "MSME registered",
  "GST verified business",
  "Legally compliant operations",
  "Audited financials",
  // Reputation & Recognition
  "Award-winning service",
  "Industry recognized brand",
  "Featured in leading media",
  "Recommended by experts",
  "Top-rated on Google",
  "Consistently 5-star reviews",
  // Reliability & Availability
  "24/7 verified customer support",
  "Always available, never offline",
  "Dedicated account manager",
  "Zero missed commitments",
  "On-time delivery, every time",
  "Transparent communication",
  // Scale & Reach
  "Global reach, local understanding",
  "Pan-India presence",
  "10+ years of experience",
  "1000+ successful projects",
  "Serving 20+ industries",
  "Trusted across 15+ states",
  // Security & Privacy
  "100% data security guaranteed",
  "Secure payment gateway",
  "No hidden charges, ever",
]

export function Step11BusinessUSP() {
  const { data, updateData } = useQuestionnaire()

  const toggleUSP = (phrase: string) => {
    const current = data.businessUSP || []
    const updated = current.includes(phrase)
      ? current.filter((u) => u !== phrase)
      : [...current, phrase]
    updateData({ businessUSP: updated })
  }

  // Split phrases into two rows for opposite-direction marquees
  const half = Math.ceil(uspPhrases.length / 2)
  const row1 = uspPhrases.slice(0, half)
  const row2 = uspPhrases.slice(half)

  const renderRow = (phrases: string[], direction: "left" | "right") => (
    <div className="overflow-hidden relative py-2">
      <div
        className={`flex gap-3 w-max ${
          direction === "left" ? "animate-marquee-left" : "animate-marquee-right"
        }`}
      >
        {[...phrases, ...phrases].map((phrase, i) => {
          const selected = data.businessUSP?.includes(phrase) || false
          return (
            <button
              key={`${phrase}-${i}`}
              type="button"
              onClick={() => toggleUSP(phrase)}
              className={`shrink-0 flex items-center gap-2 px-4 py-2.5 rounded-full border-2 text-sm font-medium whitespace-nowrap transition-colors ${
                selected
                  ? "border-accent bg-accent/10 text-foreground"
                  : "border-border bg-card text-muted-foreground hover:border-muted-foreground/40"
              }`}
            >
              {selected && <Check className="w-3.5 h-3.5 text-accent" />}
              {phrase}
            </button>
          )
        })}
      </div>
    </div>
  )

  return (
    <StepWrapper
      title="Business USP Selection"
      description="Tap on the phrases that best describe your business. Selected ones will be highlighted."
    >
      <div className="grid gap-3">
        {renderRow(row1, "left")}
        {renderRow(row2, "right")}
      </div>

      {data.businessUSP && data.businessUSP.length > 0 && (
        <div className="bg-muted/50 rounded-lg p-4 border border-border mt-4">
          <p className="text-sm text-muted-foreground">
            Selected: <span className="font-medium text-foreground">{data.businessUSP.length} USP(s)</span>
          </p>
        </div>
      )}

      <NavigationButtons />
    </StepWrapper>
  )
}