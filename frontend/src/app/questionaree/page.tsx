"use client"

import { QuestionnaireProvider } from "@/context/questionnaire-context"
import { QuestionnaireLayout } from "@/components/questionaree/questionnaire-layout"
import "./questionnaire.css"

export default function Home() {
  return (
    <div className="questionnaire-root">
      <QuestionnaireProvider>
        <QuestionnaireLayout />
      </QuestionnaireProvider>
    </div>
  )
}
