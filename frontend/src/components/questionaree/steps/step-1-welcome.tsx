"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"
import { Button } from "@/components/ui/button"
import { ArrowRight, Globe, Palette, Zap, Shield } from "lucide-react"

export function Step1Welcome() {
  const { nextStep, totalSteps, resetQuestionnaire } = useQuestionnaire()
  
  return (
    <div className="max-w-2xl mx-auto text-center space-y-8">
      <div className="space-y-4">
        <div className="w-16 h-16 bg-accent/20 rounded-2xl flex items-center justify-center mx-auto">
          <Globe className="w-8 h-8 text-accent" />
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-foreground">
          Website Requirement Questionnaire
        </h1>
        <p className="text-lg text-muted-foreground">
          Free Professional Website Setup
        </p>
      </div>
      
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-border text-left">
        <h2 className="font-semibold text-foreground mb-4">
          What to Expect
        </h2>
        <p className="text-muted-foreground mb-6">
          Complete this questionnaire to help us understand your business needs. 
          We will use this information to create a professional website tailored to your requirements.
        </p>
        
        <div className="grid gap-4">
          <div className="flex items-start gap-3">
            <span className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center shrink-0">
              <Zap className="w-4 h-4 text-primary" />
            </span>
            <div>
              <h3 className="font-medium text-foreground">Quick & Easy</h3>
              <p className="text-sm text-muted-foreground">Takes about 10-15 minutes to complete</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center shrink-0">
              <Shield className="w-4 h-4 text-primary" />
            </span>
            <div>
              <h3 className="font-medium text-foreground">Save Progress</h3>
              <p className="text-sm text-muted-foreground">Your answers are saved automatically</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center shrink-0">
              <Palette className="w-4 h-4 text-primary" />
            </span>
            <div>
              <h3 className="font-medium text-foreground">Customized Results</h3>
              <p className="text-sm text-muted-foreground">Get a website designed for your business</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-muted/50 rounded-xl p-4 border border-border">
        <p className="text-sm text-muted-foreground">
          Progress Overview: <span className="font-medium text-foreground">{totalSteps} steps</span> to complete
        </p>
      </div>
      
      <div className="flex flex-col gap-3">
        <Button 
          size="lg" 
          onClick={nextStep}
          className="w-full gap-2 bg-[#6D4C41] hover:bg-[#5D4037] text-white"
        >
          Start Questionnaire
          <ArrowRight className="w-4 h-4" />
        </Button>
        <Button 
          variant="ghost" 
          size="sm"
          onClick={resetQuestionnaire}
          className="text-muted-foreground hover:text-foreground"
        >
          Reset & Start Over
        </Button>
      </div>
    </div>
  )
}
