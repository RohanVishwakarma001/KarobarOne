"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"

export function ProgressBar() {
  const { currentStep, totalSteps } = useQuestionnaire()
  const progress = ((currentStep - 1) / (totalSteps - 1)) * 100
  
  return (
    <div className="w-full">
      <div className="flex justify-between text-sm text-muted-foreground mb-2">
        <span>Step {currentStep} of {totalSteps}</span>
        <span>{Math.round(progress)}% Complete</span>
      </div>
      <div className="h-2 bg-muted rounded-full overflow-hidden">
        <div 
          className="h-full bg-accent transition-all duration-300 ease-out rounded-full"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  )
}
