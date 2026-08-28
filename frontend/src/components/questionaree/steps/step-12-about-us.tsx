"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"
import { StepWrapper } from "../step-wrapper"
import { NavigationButtons } from "../navigation-buttons"
import { FileUpload } from "../file-upload"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

export function Step12AboutUs() {
  const { data, updateData } = useQuestionnaire()
  
  return (
    <StepWrapper
      title="About Us Information"
      description="Tell us your story. This information will help us craft compelling content for your website."
    >
      <div className="grid gap-8">
        {/* About Promoter */}
        <div className="grid gap-4">
          <h3 className="font-medium text-foreground">About Promoter</h3>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="grid gap-2">
              <Label htmlFor="promoterName">Promoter Name</Label>
              <Input
                id="promoterName"
                placeholder="Full name"
                value={data.promoterName}
                onChange={(e) => updateData({ promoterName: e.target.value })}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="promoterDesignation">Designation</Label>
              <Input
                id="promoterDesignation"
                placeholder="e.g., Founder, CEO, Director"
                value={data.promoterDesignation}
                onChange={(e) => updateData({ promoterDesignation: e.target.value })}
              />
            </div>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="promoterBio">Short Bio</Label>
            <Textarea
              id="promoterBio"
              placeholder="A short background of the promoter — experience, journey, achievements..."
              value={data.promoterBio}
              onChange={(e) => updateData({ promoterBio: e.target.value })}
              rows={4}
              className="resize-none"
            />
          </div>

          <FileUpload
            label="Promoter Photo"
            description="A professional photo of the promoter"
            accept=".jpg,.jpeg,.png,.webp"
            value={data.promoterPhoto}
            onChange={(file) => updateData({ promoterPhoto: file })}
          />
        </div>

        {/* Company History */}
        <div className="grid gap-4 pt-2 border-t border-border">
          <h3 className="font-medium text-foreground pt-4">Company History</h3>

          <div className="grid gap-2">
            <Label htmlFor="yearFounded">Year Founded</Label>
            <Input
              id="yearFounded"
              type="number"
              placeholder="e.g., 2015"
              value={data.yearFounded}
              onChange={(e) => updateData({ yearFounded: e.target.value })}
            />
          </div>

          <div className="grid gap-2">
            <Label htmlFor="companyHistory">Company Story</Label>
            <Textarea
              id="companyHistory"
              placeholder="How did the business start? What is its journey so far?"
              value={data.companyHistory}
              onChange={(e) => updateData({ companyHistory: e.target.value })}
              rows={4}
              className="resize-none"
            />
          </div>
        </div>

        {/* Mission and Vision */}
        <div className="grid gap-4 pt-2 border-t border-border">
          <h3 className="font-medium text-foreground pt-4">Mission & Vision</h3>

          <div className="grid gap-2">
            <Label htmlFor="missionVision">Mission and Vision</Label>
            <Textarea
              id="missionVision"
              placeholder="What is your business's mission and long-term vision?"
              value={data.missionVision}
              onChange={(e) => updateData({ missionVision: e.target.value })}
              rows={4}
              className="resize-none"
            />
          </div>
        </div>

        {/* Certifications & Statutory */}
        <div className="grid gap-4 pt-2 border-t border-border">
          <h3 className="font-medium text-foreground pt-4">Certifications & Statutory</h3>

          <FileUpload
            label="Certification / Statutory Document"
            description="Upload any certification or statutory compliance document you'd like to showcase"
            value={data.certificationStatutory}
            onChange={(file) => updateData({ certificationStatutory: file })}
          />
        </div>

        {/* Existing brand-story questions */}
        <div className="grid gap-4 pt-2 border-t border-border">
          <h3 className="font-medium text-foreground pt-4">Brand Story</h3>

          <div className="grid gap-3">
            <Label htmlFor="problemSolved">What problem does your business solve?</Label>
            <Textarea
              id="problemSolved"
              placeholder="Describe the main problem or pain point that your business addresses for customers..."
              value={data.problemSolved}
              onChange={(e) => updateData({ problemSolved: e.target.value })}
              rows={4}
              className="resize-none"
            />
            <p className="text-xs text-muted-foreground">
              Example: We help busy professionals save time by providing quick and reliable home cleaning services.
            </p>
          </div>

          <div className="grid gap-3">
            <Label htmlFor="uniqueSolution">What makes your solution unique?</Label>
            <Textarea
              id="uniqueSolution"
              placeholder="Explain what sets your business apart from competitors..."
              value={data.uniqueSolution}
              onChange={(e) => updateData({ uniqueSolution: e.target.value })}
              rows={4}
              className="resize-none"
            />
            <p className="text-xs text-muted-foreground">
              Example: We use eco-friendly products and our trained staff follows a 50-point checklist for every cleaning.
            </p>
          </div>

          <div className="grid gap-3">
            <Label htmlFor="trustCredibility">Why should customers trust you?</Label>
            <Textarea
              id="trustCredibility"
              placeholder="Share your credentials, experience, achievements, or customer testimonials..."
              value={data.trustCredibility}
              onChange={(e) => updateData({ trustCredibility: e.target.value })}
              rows={4}
              className="resize-none"
            />
            <p className="text-xs text-muted-foreground">
              Example: With 10+ years of experience and 5000+ satisfied customers, we have built a reputation for excellence.
            </p>
          </div>
        </div>
      </div>
      
      <NavigationButtons />
    </StepWrapper>
  )
}