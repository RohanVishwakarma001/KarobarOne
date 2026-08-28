"use client"
import { LiveWebsitePreview } from "./preview/LiveWebsitePreview"
import { useQuestionnaire } from "@/context/questionnaire-context"
import { ProgressBar } from "./progress-bar"
import { SidebarNavigation } from "./sidebar-navigation"
import { Step1Welcome } from "./steps/step-1-welcome"
import { Step2BasicDetails } from "./steps/step-2-basic-details"
import { Step5Operating } from "./steps/step-5-operating"
import { Step6ProductsServices } from "./steps/step-6-products-services"
import { Step11BusinessUSP } from "./steps/step-11-business-usp"
import { Step12AboutUs } from "./steps/step-12-about-us"
import { Step12AWhyChooseUs } from "./steps/Step12-A-WhyChooseUs"
import { Step12BSocialMedia } from "./steps/step-12b-social-media"
import { Step13Licenses } from "./steps/step-13-licenses"
import { Step14Review } from "./steps/step-14-review"
import { Step15Success } from "./steps/step-15-success"

const steps: { [key: number]: React.ComponentType } = {
  1: Step1Welcome,
  2: Step2BasicDetails,
  5: Step5Operating,
  6: Step6ProductsServices,
  11: Step11BusinessUSP,
  12: Step12AboutUs,
  12.5: Step12AWhyChooseUs,
  12.7: Step12BSocialMedia,
  13: Step13Licenses,
  14: Step14Review,
  15: Step15Success,
}

export function QuestionnaireLayout() {
  const { currentStep } = useQuestionnaire()

  const CurrentStepComponent = steps[currentStep] || Step1Welcome
  const showSidebar = currentStep > 1 && currentStep < 15
  const showProgress = currentStep > 1 && currentStep < 15

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-background/95 backdrop-blur border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-sm">W</span>
              </div>
              <span className="font-semibold text-foreground hidden sm:inline">
                Website Requirement Questionnaire
              </span>
            </div>
            {showProgress && (
              <div className="flex-1 max-w-xs ml-4 hidden md:block">
                <ProgressBar />
              </div>
            )}
          </div>
          {showProgress && (
            <div className="mt-3 md:hidden">
              <ProgressBar />
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">

  {showSidebar && (
    <div className="xl:col-span-2">
      <SidebarNavigation />
    </div>
  )}

  <div
    className={
      showSidebar
        ? "xl:col-span-5"
        : "xl:col-span-6 xl:col-start-4"
    }
  >
    <div className="bg-card rounded-2xl shadow-sm border border-border p-6 md:p-8">
      <CurrentStepComponent />
    </div>
  </div>

  {showSidebar && (
    <div className="xl:col-span-5">
      <LiveWebsitePreview />
    </div>
  )}

</div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-6 mt-auto">
        <div className="container mx-auto px-4">
          <p className="text-center text-sm text-muted-foreground">
            Your information is secure and will only be used for website development purposes.
          </p>
        </div>
      </footer>
    </div>
  )
}