"use client"

import { cn } from "@/lib/utils"
import { Check } from "lucide-react"
import { ReactNode } from "react"

interface SelectableCardProps {
  title: string
  description?: string
  icon?: ReactNode
  selected: boolean
  onClick: () => void
  disabled?: boolean
}

export function SelectableCard({
  title,
  description,
  icon,
  selected,
  onClick,
  disabled = false,
}: SelectableCardProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "relative w-full p-4 rounded-xl border-2 text-left transition-all duration-200",
        "hover:shadow-md focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
        selected
          ? "border-accent bg-accent/10 shadow-sm"
          : "border-border bg-card hover:border-muted-foreground/30",
        disabled && "opacity-50 cursor-not-allowed"
      )}
    >
      {selected && (
        <span className="absolute top-3 right-3 w-5 h-5 bg-accent rounded-full flex items-center justify-center">
          <Check className="w-3 h-3 text-accent-foreground" />
        </span>
      )}
      <div className="flex items-start gap-3">
        {icon && (
          <span className={cn(
            "w-10 h-10 rounded-lg flex items-center justify-center shrink-0",
            selected ? "bg-accent text-accent-foreground" : "bg-muted text-muted-foreground"
          )}>
            {icon}
          </span>
        )}
        <div className="min-w-0">
          <h4 className={cn(
            "font-medium",
            selected ? "text-foreground" : "text-foreground"
          )}>
            {title}
          </h4>
          {description && (
            <p className="text-sm text-muted-foreground mt-1">{description}</p>
          )}
        </div>
      </div>
    </button>
  )
}
