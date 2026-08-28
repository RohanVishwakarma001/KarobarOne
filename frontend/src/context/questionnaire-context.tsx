"use client"

import { createContext, useContext, useState, useEffect, ReactNode } from "react"

export interface BusinessItem {
  id: string
  name: string
  images: File[]
  shortDescription: string
  longDescription: string
  mrp: string
  listPrice: string
  discount: string
  salePrice: string
}

export interface DayTiming {
  open: string
  close: string
}

export interface QuestionnaireData {
  // Page 2 - Business Basic Details
  businessName: string
  contactPerson: string
  designation: string
  phoneNumber: string
  email: string
  brandTagline: string
  businessNature: "product" | "service" | ""
  
  // Page 2 - GST & Tax Details (merged in)
  gstNumber: string
  panNumber: string
  businessType: string
  taxDocument: File | null
  
  // Page 5 - Business Operating Details
  daysOpen: string[]
  dayTimings: { [day: string]: DayTiming }
  
  // Page 6 - Products / Services
  planType: "free" | "paid" | ""
  items: BusinessItem[]
  
  // Page 11 - Business USP
  businessUSP: string[]
  
  // Page 12 - About Us
  promoterName: string
  promoterDesignation: string
  promoterBio: string
  promoterPhoto: File | null
  yearFounded: string
  companyHistory: string
  missionVision: string
  certificationStatutory: File | null
  problemSolved: string
  uniqueSolution: string
  trustCredibility: string
  
  // Page 12.5 - Why Choose Us
  whyChooseUs: string[]
  
  // Page 12.7 - Social Media
  facebookUrl: string
  instagramUrl: string
  linkedinUrl: string
  
  // Page 13 - Licenses & Certifications
  businessRegistration: File | null
  taxCompliance: File | null
  tradeAuthorization: File | null
  safetyCompliance: File | null
  qualityCertifications: File | null
  brandIdentity: File | null
  
  // Page 14 - Confirmation
  confirmed: boolean
}

const initialData: QuestionnaireData = {
  businessName: "",
  contactPerson: "",
  designation: "",
  phoneNumber: "",
  email: "",
  brandTagline: "",
  businessNature: "",
  gstNumber: "",
  panNumber: "",
  businessType: "",
  taxDocument: null,
  daysOpen: [],
  dayTimings: {},
  planType: "",
  items: [],
  businessUSP: [],
  promoterName: "",
  promoterDesignation: "",
  promoterBio: "",
  promoterPhoto: null,
  yearFounded: "",
  companyHistory: "",
  missionVision: "",
  certificationStatutory: null,
  problemSolved: "",
  uniqueSolution: "",
  trustCredibility: "",
  whyChooseUs: [],
  facebookUrl: "",
  instagramUrl: "",
  linkedinUrl: "",
  businessRegistration: null,
  taxCompliance: null,
  tradeAuthorization: null,
  safetyCompliance: null,
  qualityCertifications: null,
  brandIdentity: null,
  confirmed: false,
}

// Only these step numbers actually exist in the questionnaire flow
const validSteps = [1, 2, 5, 6, 11, 12, 12.5, 12.7, 13, 14, 15]

interface QuestionnaireContextType {
  data: QuestionnaireData
  updateData: (updates: Partial<QuestionnaireData>) => void
  currentStep: number
  setCurrentStep: (step: number) => void
  totalSteps: number
  nextStep: () => void
  prevStep: () => void
  resetQuestionnaire: () => void
}

const QuestionnaireContext = createContext<QuestionnaireContextType | undefined>(undefined)

export function QuestionnaireProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<QuestionnaireData>(initialData)
  const [currentStep, setCurrentStep] = useState(1)
  const totalSteps = validSteps.length
  
  // Load from localStorage on mount
  useEffect(() => {
    const savedData = localStorage.getItem("questionnaireData")
    const savedStep = localStorage.getItem("questionnaireStep")
    
    if (savedData) {
      try {
        const parsed = JSON.parse(savedData)
        // Files cannot be stored in localStorage, so we exclude them
        setData({ ...initialData, ...parsed })
      } catch (e) {
        console.error("Failed to parse saved data:", e)
      }
    }
    
    if (savedStep) {
      const parsedStep = parseFloat(savedStep)
      // Guard against stale step numbers from removed pages
      setCurrentStep(validSteps.includes(parsedStep) ? parsedStep : 1)
    }
  }, [])
  
  // Save to localStorage on change
  useEffect(() => {
    // Create a copy without File objects for localStorage
    const dataToSave = { ...data }
    Object.keys(dataToSave).forEach((key) => {
      const value = dataToSave[key as keyof QuestionnaireData]
      if (value instanceof File) {
        (dataToSave as Record<string, unknown>)[key] = null
      }
    })
    // Strip File objects out of items array too
    dataToSave.items = dataToSave.items.map((item) => ({ ...item, images: [] }))
    localStorage.setItem("questionnaireData", JSON.stringify(dataToSave))
    localStorage.setItem("questionnaireStep", currentStep.toString())
  }, [data, currentStep])
  
  const updateData = (updates: Partial<QuestionnaireData>) => {
    setData((prev) => ({ ...prev, ...updates }))
  }
  
  const nextStep = () => {
    const idx = validSteps.indexOf(currentStep)
    if (idx !== -1 && idx < validSteps.length - 1) {
      setCurrentStep(validSteps[idx + 1])
    }
  }
  
  const prevStep = () => {
    const idx = validSteps.indexOf(currentStep)
    if (idx > 0) {
      setCurrentStep(validSteps[idx - 1])
    }
  }
  
  const resetQuestionnaire = () => {
    setData(initialData)
    setCurrentStep(1)
    localStorage.removeItem("questionnaireData")
    localStorage.removeItem("questionnaireStep")
  }
  
  return (
    <QuestionnaireContext.Provider
      value={{
        data,
        updateData,
        currentStep,
        setCurrentStep,
        totalSteps,
        nextStep,
        prevStep,
        resetQuestionnaire,
      }}
    >
      {children}
    </QuestionnaireContext.Provider>
  )
}

export function useQuestionnaire() {
  const context = useContext(QuestionnaireContext)
  if (context === undefined) {
    throw new Error("useQuestionnaire must be used within a QuestionnaireProvider")
  }
  return context
}