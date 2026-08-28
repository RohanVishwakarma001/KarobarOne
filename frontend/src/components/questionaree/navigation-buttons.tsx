"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight } from "lucide-react"

interface NavigationButtonsProps {
  onNext?: () => boolean | void
  nextLabel?: string
  showPrev?: boolean
  showNext?: boolean
}

export function NavigationButtons({
  onNext,
  nextLabel = "Next",
  showPrev = true,
  showNext = true,
}: NavigationButtonsProps) {
  const { currentStep, nextStep, prevStep, totalSteps } = useQuestionnaire()
  
  const handleNext = () => {
    if (onNext) {
      const canProceed = onNext()
      if (canProceed === false) return
    }
    nextStep()
  }
  
  return (
    <div className="flex justify-between items-center pt-6 border-t border-border mt-8">
      {showPrev && currentStep > 1 ? (
        <Button
          variant="outline"
          onClick={prevStep}
          className="gap-2"
        >
          <ChevronLeft className="w-4 h-4" />
          Previous
        </Button>
      ) : (
        <div />
      )}
      
      {showNext && currentStep < 15 && (
        <Button onClick={handleNext} className="gap-2 bg-primary hover:bg-primary/90">
          {nextLabel}
          <ChevronRight className="w-4 h-4" />
        </Button>
      )}
    </div>
  )
}
