"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"
import { StepWrapper } from "../step-wrapper"
import { NavigationButtons } from "../navigation-buttons"
import { FileUpload } from "../file-upload"

export function Step13Licenses() {
  const { data, updateData } = useQuestionnaire()
  
  return (
    <StepWrapper
      title="Licenses & Certifications"
      description="Upload any relevant business documents. These help build credibility on your website."
    >
      <div className="grid md:grid-cols-2 gap-6">
        <FileUpload
          label="Business Registration"
          description="Certificate of incorporation or business registration"
          value={data.businessRegistration}
          onChange={(file) => updateData({ businessRegistration: file })}
        />
        
        <FileUpload
          label="Tax Compliance"
          description="GST certificate or tax registration document"
          value={data.taxCompliance}
          onChange={(file) => updateData({ taxCompliance: file })}
        />
        
        <FileUpload
          label="Trade Authorization"
          description="Trade license or business permit"
          value={data.tradeAuthorization}
          onChange={(file) => updateData({ tradeAuthorization: file })}
        />
        
        <FileUpload
          label="Safety Compliance"
          description="Safety certifications or compliance documents"
          value={data.safetyCompliance}
          onChange={(file) => updateData({ safetyCompliance: file })}
        />
        
        <FileUpload
          label="Quality Certifications"
          description="ISO or other quality certifications"
          value={data.qualityCertifications}
          onChange={(file) => updateData({ qualityCertifications: file })}
        />
        
        <FileUpload
          label="Brand Identity"
          description="Logo or brand guidelines document"
          value={data.brandIdentity}
          onChange={(file) => updateData({ brandIdentity: file })}
        />
      </div>
      
      <div className="bg-muted/50 rounded-lg p-4 border border-border">
        <p className="text-sm text-muted-foreground">
          All documents are optional but help establish trust with your website visitors.
        </p>
      </div>
      
      <NavigationButtons />
    </StepWrapper>
  )
}
