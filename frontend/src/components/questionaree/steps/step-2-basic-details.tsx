"use client"

import { useState } from "react"
import { useQuestionnaire } from "@/context/questionnaire-context"
import { StepWrapper } from "../step-wrapper"
import { NavigationButtons } from "../navigation-buttons"
import { SelectableCard } from "../selectable-card"
import { FileUpload } from "../file-upload"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Package, Wrench } from "lucide-react"
import { isValidPhone, isValidEmail, isValidGST, isValidPAN, isValidBusinessName } from "@/lib/validation"

export function Step2BasicDetails() {
  const { data, updateData } = useQuestionnaire()
  const [errors, setErrors] = useState<Record<string, string>>({})

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!isValidBusinessName(data.businessName)) {
      newErrors.businessName = data.businessName.trim().length === 0
        ? "Business name is required."
        : "Business name must be 100 characters or less."
    }

    if (!data.contactPerson.trim()) {
      newErrors.contactPerson = "Contact person name is required."
    }

    if (!isValidPhone(data.phoneNumber)) {
      newErrors.phoneNumber = "Enter a valid 10-digit Indian mobile number."
    }

    if (!isValidEmail(data.email)) {
      newErrors.email = "Enter a valid email address."
    }

    if (!data.businessNature) {
      newErrors.businessNature = "Please select whether you offer products or services."
    }

    if (!data.businessType) {
      newErrors.businessType = "Please select GST or PAN."
    } else if (data.businessType === "gst" && !isValidGST(data.gstNumber)) {
      newErrors.gstNumber = "Enter a valid GST number (e.g., 22AAAAA0000A1Z5)."
    } else if (data.businessType === "pan" && !isValidPAN(data.panNumber)) {
      newErrors.panNumber = "Enter a valid PAN number (e.g., ABCDE1234F)."
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  return (
    <StepWrapper
      title="Business Basic Details"
      description="Tell us about your business and how we can contact you."
    >
      <div className="grid gap-6">
        <div className="grid gap-2">
          <Label htmlFor="businessName">Business Name *</Label>
          <Input
            id="businessName"
            placeholder="Enter your business name"
            value={data.businessName}
            maxLength={100}
            onChange={(e) => updateData({ businessName: e.target.value })}
          />
          {errors.businessName && (
            <p className="text-xs text-destructive">{errors.businessName}</p>
          )}
        </div>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="grid gap-2">
            <Label htmlFor="contactPerson">Contact Person Name *</Label>
            <Input
              id="contactPerson"
              placeholder="Enter contact person name"
              value={data.contactPerson}
              onChange={(e) => updateData({ contactPerson: e.target.value })}
            />
            {errors.contactPerson && (
              <p className="text-xs text-destructive">{errors.contactPerson}</p>
            )}
          </div>
          
          <div className="grid gap-2">
            <Label htmlFor="designation">Designation</Label>
            <Input
              id="designation"
              placeholder="e.g., Owner, Manager, Director"
              value={data.designation}
              onChange={(e) => updateData({ designation: e.target.value })}
            />
          </div>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="grid gap-2">
            <Label htmlFor="phoneNumber">Phone Number *</Label>
            <Input
              id="phoneNumber"
              type="tel"
              placeholder="+91 XXXXX XXXXX"
              value={data.phoneNumber}
              onChange={(e) => updateData({ phoneNumber: e.target.value })}
            />
            {errors.phoneNumber && (
              <p className="text-xs text-destructive">{errors.phoneNumber}</p>
            )}
          </div>
          
          <div className="grid gap-2">
            <Label htmlFor="email">Email Address *</Label>
            <Input
              id="email"
              type="email"
              placeholder="you@business.com"
              value={data.email}
              onChange={(e) => updateData({ email: e.target.value })}
            />
            {errors.email && (
              <p className="text-xs text-destructive">{errors.email}</p>
            )}
          </div>
        </div>
        
        <div className="grid gap-2">
          <Label htmlFor="brandTagline">Brand Tagline</Label>
          <Input
            id="brandTagline"
            placeholder="Your catchy brand tagline or slogan"
            value={data.brandTagline}
            onChange={(e) => updateData({ brandTagline: e.target.value })}
          />
          <p className="text-xs text-muted-foreground">
            A short phrase that captures your brand essence
          </p>
        </div>

        {/* Business Nature: Product or Service */}
        <div className="grid gap-3">
          <Label>What does your business offer? *</Label>
          <div className="grid md:grid-cols-2 gap-4">
            <SelectableCard
              title="Product"
              description="I sell physical or digital products"
              icon={<Package className="w-5 h-5" />}
              selected={data.businessNature === "product"}
              onClick={() => updateData({ businessNature: "product" })}
            />
            <SelectableCard
              title="Service"
              description="I offer services or expertise"
              icon={<Wrench className="w-5 h-5" />}
              selected={data.businessNature === "service"}
              onClick={() => updateData({ businessNature: "service" })}
            />
          </div>
          {errors.businessNature && (
            <p className="text-xs text-destructive">{errors.businessNature}</p>
          )}
        </div>

        {/* GST / PAN Details */}
        <div className="grid gap-4 pt-2 border-t border-border">
          <h3 className="font-medium text-foreground pt-4">Business Tax Details</h3>

          <div className="grid gap-3">
            <Label>Registered Under *</Label>
            <div className="grid md:grid-cols-2 gap-4">
              <SelectableCard
                title="GST"
                description="Business has GST registration"
                selected={data.businessType === "gst"}
                onClick={() => updateData({ businessType: "gst" })}
              />
              <SelectableCard
                title="PAN"
                description="Business operates with PAN only"
                selected={data.businessType === "pan"}
                onClick={() => updateData({ businessType: "pan" })}
              />
            </div>
            {errors.businessType && (
              <p className="text-xs text-destructive">{errors.businessType}</p>
            )}
          </div>

          {data.businessType === "gst" && (
            <div className="grid gap-2">
              <Label htmlFor="gstNumber">GST Number *</Label>
              <Input
                id="gstNumber"
                placeholder="22AAAAA0000A1Z5"
                value={data.gstNumber}
                onChange={(e) => updateData({ gstNumber: e.target.value.toUpperCase() })}
              />
              {errors.gstNumber && (
                <p className="text-xs text-destructive">{errors.gstNumber}</p>
              )}
            </div>
          )}

          {data.businessType === "pan" && (
            <div className="grid gap-2">
              <Label htmlFor="panNumber">PAN Number *</Label>
              <Input
                id="panNumber"
                placeholder="ABCDE1234F"
                value={data.panNumber}
                onChange={(e) => updateData({ panNumber: e.target.value.toUpperCase() })}
              />
              {errors.panNumber && (
                <p className="text-xs text-destructive">{errors.panNumber}</p>
              )}
            </div>
          )}

          {data.businessType && (
            <FileUpload
              label={data.businessType === "gst" ? "Upload GST Document" : "Upload PAN Document"}
              description="Upload a clear scan or photo of the document"
              value={data.taxDocument}
              onChange={(file) => updateData({ taxDocument: file })}
            />
          )}
        </div>
      </div>
      
      <NavigationButtons onNext={validate} />
    </StepWrapper>
  )
}