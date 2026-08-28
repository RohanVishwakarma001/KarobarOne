"use client"
import Link from "next/link"
import { useQuestionnaire } from "@/context/questionnaire-context"
import { Button } from "@/components/ui/button"
import { CheckCircle, Download, Mail, Phone, RotateCcw } from "lucide-react"

export function Step15Success() {
  const { data, resetQuestionnaire } = useQuestionnaire()
  
  return (
    <div className="max-w-2xl mx-auto text-center space-y-8">
      <div className="space-y-4">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto">
          <CheckCircle className="w-10 h-10 text-green-600" />
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-foreground">
          Thank You!
        </h1>
        <p className="text-lg text-muted-foreground">
          Your questionnaire has been submitted successfully.
        </p>
      </div>
      
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-border text-left space-y-4">
        <h2 className="font-semibold text-foreground">Submission Confirmed</h2>
        <div className="bg-muted/50 rounded-lg p-4 border border-border">
          <p className="text-sm text-muted-foreground">
            <span className="font-medium text-foreground">Business Name:</span> {data.businessName || "Your Business"}
          </p>
          <p className="text-sm text-muted-foreground mt-1">
            <span className="font-medium text-foreground">Contact Email:</span> {data.email || "your@email.com"}
          </p>
        </div>
        <p className="text-sm text-muted-foreground">
          We have received all your information and our team will begin working on your website design.
        </p>
      </div>
      
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-border text-left space-y-4">
        <h2 className="font-semibold text-foreground">What Happens Next?</h2>
        <ul className="space-y-3">
          <li className="flex items-start gap-3">
            <span className="w-6 h-6 bg-accent/20 rounded-full flex items-center justify-center shrink-0 mt-0.5">
              <span className="text-xs font-medium text-accent-foreground">1</span>
            </span>
            <div>
              <p className="font-medium text-foreground">Review</p>
              <p className="text-sm text-muted-foreground">Our team will review your requirements within 24-48 hours.</p>
            </div>
          </li>
          <li className="flex items-start gap-3">
            <span className="w-6 h-6 bg-accent/20 rounded-full flex items-center justify-center shrink-0 mt-0.5">
              <span className="text-xs font-medium text-accent-foreground">2</span>
            </span>
            <div>
              <p className="font-medium text-foreground">Design</p>
              <p className="text-sm text-muted-foreground">We will create a custom design based on your business needs.</p>
            </div>
          </li>
          <li className="flex items-start gap-3">
            <span className="w-6 h-6 bg-accent/20 rounded-full flex items-center justify-center shrink-0 mt-0.5">
              <span className="text-xs font-medium text-accent-foreground">3</span>
            </span>
            <div>
              <p className="font-medium text-foreground">Delivery</p>
              <p className="text-sm text-muted-foreground">You will receive a preview link to review your website.</p>
            </div>
          </li>
        </ul>
      </div>
      
      <div className="bg-card rounded-2xl p-6 shadow-sm border border-border text-left space-y-4">
        <h2 className="font-semibold text-foreground">Need Help?</h2>
        <p className="text-sm text-muted-foreground">
          If you have any questions or need to make changes, please contact our support team.
        </p>
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Mail className="w-4 h-4" />
            <span>support@example.com</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Phone className="w-4 h-4" />
            <span>+91 98765 43210</span>
          </div>
        </div>
      </div>
      
      <div className="flex flex-col sm:flex-row gap-3 justify-center">
        <Button variant="outline" className="gap-2">
          <Download className="w-4 h-4" />
          Download Summary
        </Button>
        <Button 
          variant="ghost" 
          onClick={resetQuestionnaire}
          className="gap-2 text-muted-foreground hover:text-foreground"
        >
          <RotateCcw className="w-4 h-4" />
          Start New Questionnaire
        </Button>
        <Link 
          href="/dashboard"
          className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-[#6D4C41] hover:bg-[#5D4037] text-white transition-colors"
        >
          View Our Designs →
        </Link>
      </div>
    </div>
  )
}
