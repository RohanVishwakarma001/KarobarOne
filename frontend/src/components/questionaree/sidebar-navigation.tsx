"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"
import { cn } from "@/lib/utils"
import { Check } from "lucide-react"

const steps = [
  { number: 1, title: "Welcome" },
  { number: 2, title: "Basic Details" },
  { number: 5, title: "Operating Hours" },
  { number: 6, title: "Products/Services" },
  { number: 11, title: "Business USP" },
  { number: 12, title: "About Us" },
  { number: 12.5, title: "Why Choose Us" },
  { number: 13, title: "Licenses" },
  { number: 14, title: "Review" },
  { number: 15, title: "Success" },
]

export function SidebarNavigation() {
  const { currentStep, setCurrentStep } = useQuestionnaire()
  
  return (
    <nav className="hidden xl:block w-full">
      <div className="sticky top-24 w-full rounded-2xl border bg-card p-5 shadow-sm">
        <h3 className="font-semibold text-foreground mb-4">Progress</h3>
        <ul className="space-y-1">
          {steps.map((step) => {
            const isCompleted = step.number < currentStep
            const isCurrent = step.number === currentStep
            const isClickable = step.number <= currentStep
            
            return (
              <li key={step.number}>
                <button
                  onClick={() => isClickable && setCurrentStep(step.number)}
                  disabled={!isClickable}
                  className={cn(
                    "w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors text-left",
                    isCurrent && "bg-primary text-primary-foreground",
                    isCompleted && "text-foreground hover:bg-muted",
                    !isClickable && "text-muted-foreground cursor-not-allowed opacity-50"
                  )}
                >
                  <span
                    className={cn(
                      "w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium shrink-0",
                      isCurrent && "bg-primary-foreground text-primary",
                      isCompleted && "bg-accent text-accent-foreground",
                      !isCurrent && !isCompleted && "bg-muted text-muted-foreground"
                    )}
                  >
                    {isCompleted ? <Check className="w-3.5 h-3.5" /> : step.number}
                  </span>
                  <span className="truncate">{step.title}</span>
                </button>
              </li>
            )
          })}
        </ul>
      </div>
    </nav>
  )
}