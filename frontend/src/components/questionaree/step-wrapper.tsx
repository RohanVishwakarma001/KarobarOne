"use client"

import { ReactNode } from "react"

interface StepWrapperProps {
  title: string
  description?: string
  children: ReactNode
}

export function StepWrapper({ title, description, children }: StepWrapperProps) {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-semibold text-foreground">{title}</h2>
        {description && (
          <p className="text-muted-foreground">{description}</p>
        )}
      </div>
      {children}
    </div>
  )
}
