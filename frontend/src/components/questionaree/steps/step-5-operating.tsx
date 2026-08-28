"use client"

import { useQuestionnaire } from "@/context/questionnaire-context"
import { StepWrapper } from "../step-wrapper"
import { NavigationButtons } from "../navigation-buttons"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

const daysOfWeek = [
  { id: "monday", title: "Monday" },
  { id: "tuesday", title: "Tuesday" },
  { id: "wednesday", title: "Wednesday" },
  { id: "thursday", title: "Thursday" },
  { id: "friday", title: "Friday" },
  { id: "saturday", title: "Saturday" },
  { id: "sunday", title: "Sunday" },
]

export function Step5Operating() {
  const { data, updateData } = useQuestionnaire()

  const toggleDay = (id: string) => {
    const current = data.daysOpen || []
    const isOpen = current.includes(id)

    if (isOpen) {
      const updatedTimings = { ...data.dayTimings }
      delete updatedTimings[id]
      updateData({
        daysOpen: current.filter((d) => d !== id),
        dayTimings: updatedTimings,
      })
    } else {
      updateData({
        daysOpen: [...current, id],
        dayTimings: {
          ...data.dayTimings,
          [id]: data.dayTimings[id] || { open: "", close: "" },
        },
      })
    }
  }

  const updateTiming = (id: string, field: "open" | "close", value: string) => {
    updateData({
      dayTimings: {
        ...data.dayTimings,
        [id]: {
          ...data.dayTimings[id],
          [field]: value,
        },
      },
    })
  }

  return (
    <StepWrapper
      title="Business Operating Details"
      description="Select the days your business operates and set timings for each."
    >
      <div className="grid gap-4">
        {daysOfWeek.map((day) => {
          const isOpen = data.daysOpen?.includes(day.id)
          const timing = data.dayTimings?.[day.id]

          return (
            <div
              key={day.id}
              className={`rounded-xl border-2 p-4 transition-all duration-200 ${
                isOpen ? "border-accent bg-accent/5" : "border-border bg-card"
              }`}
            >
              <div className="flex items-center justify-between gap-4">
                <button
                  type="button"
                  onClick={() => toggleDay(day.id)}
                  className="flex items-center gap-3 flex-1 text-left"
                >
                  <span
                    className={`w-5 h-5 rounded-md border-2 flex items-center justify-center shrink-0 ${
                      isOpen ? "bg-accent border-accent" : "border-border"
                    }`}
                  >
                    {isOpen && <span className="w-2 h-2 bg-accent-foreground rounded-sm" />}
                  </span>
                  <span className="font-medium text-foreground">{day.title}</span>
                </button>
              </div>

              {isOpen && (
                <div className="grid md:grid-cols-2 gap-4 mt-4 pl-8">
                  <div className="grid gap-2">
                    <Label htmlFor={`${day.id}-open`}>Opening Time</Label>
                    <Input
                      id={`${day.id}-open`}
                      type="time"
                      value={timing?.open || ""}
                      onChange={(e) => updateTiming(day.id, "open", e.target.value)}
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor={`${day.id}-close`}>Closing Time</Label>
                    <Input
                      id={`${day.id}-close`}
                      type="time"
                      value={timing?.close || ""}
                      onChange={(e) => updateTiming(day.id, "close", e.target.value)}
                    />
                  </div>
                </div>
              )}
            </div>
          )
        })}

        {data.daysOpen && data.daysOpen.length > 0 && (
          <div className="bg-muted/50 rounded-lg p-4 border border-border">
            <p className="text-sm text-muted-foreground">
              Operating: <span className="font-medium text-foreground">{data.daysOpen.length} days per week</span>
            </p>
          </div>
        )}
      </div>

      <NavigationButtons />
    </StepWrapper>
  )
}