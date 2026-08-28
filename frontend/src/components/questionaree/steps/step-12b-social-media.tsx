"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"
import { StepWrapper } from "../step-wrapper"
import { NavigationButtons } from "../navigation-buttons"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { FaFacebook, FaInstagram, FaLinkedin } from "react-icons/fa"

export function Step12BSocialMedia() {
  const { data, updateData } = useQuestionnaire()

  return (
    <StepWrapper
      title="Social Media Links"
      description="If your business is active on social media, share your profile links. This step is optional."
    >
      <div className="grid gap-6">
        <div className="grid gap-2">
          <Label htmlFor="facebookUrl" className="flex items-center gap-2">
            <FaFacebook className="w-4 h-4 text-muted-foreground" />
            Facebook Page URL
          </Label>
          <Input
            id="facebookUrl"
            type="url"
            placeholder="https://facebook.com/yourbusiness"
            value={data.facebookUrl}
            onChange={(e) => updateData({ facebookUrl: e.target.value })}
          />
        </div>

        <div className="grid gap-2">
          <Label htmlFor="instagramUrl" className="flex items-center gap-2">
            <FaInstagram className="w-4 h-4 text-muted-foreground" />
            Instagram Profile URL
          </Label>
          <Input
            id="instagramUrl"
            type="url"
            placeholder="https://instagram.com/yourbusiness"
            value={data.instagramUrl}
            onChange={(e) => updateData({ instagramUrl: e.target.value })}
          />
        </div>

        <div className="grid gap-2">
          <Label htmlFor="linkedinUrl" className="flex items-center gap-2">
            <FaLinkedin className="w-4 h-4 text-muted-foreground" />
            LinkedIn Page URL
          </Label>
          <Input
            id="linkedinUrl"
            type="url"
            placeholder="https://linkedin.com/company/yourbusiness"
            value={data.linkedinUrl}
            onChange={(e) => updateData({ linkedinUrl: e.target.value })}
          />
        </div>

        <div className="bg-muted/50 rounded-lg p-4 border border-border">
          <p className="text-sm text-muted-foreground">
            Don&apos;t have these or don&apos;t use social media? No problem — just skip ahead.
          </p>
        </div>
      </div>

      <NavigationButtons />
    </StepWrapper>
  )
}