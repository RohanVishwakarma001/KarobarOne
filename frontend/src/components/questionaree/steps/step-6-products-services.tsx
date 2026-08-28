"use client"

import { useQuestionnaire, BusinessItem } from "@/context/questionnaire-context"
import { StepWrapper } from "../step-wrapper"
import { NavigationButtons } from "../navigation-buttons"
import { SelectableCard } from "../selectable-card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Plus, Trash2, Upload, X, Zap, Crown } from "lucide-react"
import { useRef } from "react"

export function Step6ProductsServices() {
  const { data, updateData } = useQuestionnaire()
  const isProduct = data.businessNature === "product"
  const label = isProduct ? "Product" : "Service"
  const maxImages = data.planType === "paid" ? 6 : 1

  const addItem = () => {
    const newItem: BusinessItem = {
      id: Date.now().toString(),
      name: "",
      images: [],
      shortDescription: "",
      longDescription: "",
      mrp: "",
      listPrice: "",
      discount: "",
      salePrice: "",
    }
    updateData({ items: [...data.items, newItem] })
  }

  const removeItem = (id: string) => {
    updateData({ items: data.items.filter((item) => item.id !== id) })
  }

  const updateItem = (id: string, updates: Partial<BusinessItem>) => {
    updateData({
      items: data.items.map((item) => (item.id === id ? { ...item, ...updates } : item)),
    })
  }

  const addImages = (id: string, files: FileList | null) => {
    if (!files) return
    const item = data.items.find((i) => i.id === id)
    if (!item) return
    const remaining = maxImages - item.images.length
    const newFiles = Array.from(files).slice(0, remaining)
    updateItem(id, { images: [...item.images, ...newFiles] })
  }

  const removeImage = (id: string, index: number) => {
    const item = data.items.find((i) => i.id === id)
    if (!item) return
    updateItem(id, { images: item.images.filter((_, i) => i !== index) })
  }

  return (
    <StepWrapper
      title={`Your ${label}s`}
      description={`Add the ${label.toLowerCase()}s you offer, along with details, pricing and images.`}
    >
      <div className="grid gap-6">
        {/* Plan selection */}
        <div className="grid gap-3">
          <Label>Choose Your Plan *</Label>
          <div className="grid md:grid-cols-2 gap-4">
            <SelectableCard
              title="Free"
              description="1 image per item"
              icon={<Zap className="w-5 h-5" />}
              selected={data.planType === "free"}
              onClick={() => updateData({ planType: "free" })}
            />
            <SelectableCard
              title="Paid"
              description="Up to 6 images per item"
              icon={<Crown className="w-5 h-5" />}
              selected={data.planType === "paid"}
              onClick={() => updateData({ planType: "paid" })}
            />
          </div>
        </div>

        {data.items.length === 0 && (
          <div className="text-center py-8 border-2 border-dashed border-border rounded-xl">
            <p className="text-muted-foreground">
              No {label.toLowerCase()}s added yet. Click below to add your first one.
            </p>
          </div>
        )}

        {data.items.map((item, index) => (
          <ItemCard
            key={item.id}
            item={item}
            index={index}
            label={label}
            maxImages={maxImages}
            onRemove={() => removeItem(item.id)}
            onUpdate={(updates) => updateItem(item.id, updates)}
            onAddImages={(files) => addImages(item.id, files)}
            onRemoveImage={(i) => removeImage(item.id, i)}
          />
        ))}

        <Button type="button" variant="outline" onClick={addItem} className="gap-2">
          <Plus className="w-4 h-4" />
          Add {label}
        </Button>
      </div>

      <NavigationButtons />
    </StepWrapper>
  )
}

function ItemCard({
  item,
  index,
  label,
  maxImages,
  onRemove,
  onUpdate,
  onAddImages,
  onRemoveImage,
}: {
  item: BusinessItem
  index: number
  label: string
  maxImages: number
  onRemove: () => void
  onUpdate: (updates: Partial<BusinessItem>) => void
  onAddImages: (files: FileList | null) => void
  onRemoveImage: (index: number) => void
}) {
  const inputRef = useRef<HTMLInputElement>(null)
  const canAddMore = item.images.length < maxImages

  return (
    <div className="rounded-xl border-2 border-border p-5 grid gap-4 relative">
      <div className="flex items-center justify-between">
        <h3 className="font-medium text-foreground">
          {label} #{index + 1}
        </h3>
        <button
          type="button"
          onClick={onRemove}
          className="p-2 hover:bg-destructive/10 rounded-md transition-colors"
        >
          <Trash2 className="w-4 h-4 text-destructive" />
        </button>
      </div>

      <div className="grid gap-2">
        <Label htmlFor={`name-${item.id}`}>{label} Name *</Label>
        <Input
          id={`name-${item.id}`}
          placeholder={`Enter ${label.toLowerCase()} name`}
          value={item.name}
          onChange={(e) => onUpdate({ name: e.target.value })}
        />
      </div>

      {/* Images */}
      <div className="grid gap-2">
        <Label>
          {label} Images ({item.images.length}/{maxImages})
        </Label>
        <div className="flex flex-wrap gap-3">
          {item.images.map((file, i) => (
            <div key={i} className="relative w-20 h-20 rounded-lg overflow-hidden border border-border">
              <img
                src={URL.createObjectURL(file)}
                alt={`${label} ${i + 1}`}
                className="w-full h-full object-cover"
              />
              <button
                type="button"
                onClick={() => onRemoveImage(i)}
                className="absolute top-0.5 right-0.5 bg-black/60 rounded-full p-0.5"
              >
                <X className="w-3 h-3 text-white" />
              </button>
            </div>
          ))}

          {canAddMore && (
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              className="w-20 h-20 rounded-lg border-2 border-dashed border-border flex flex-col items-center justify-center text-muted-foreground hover:border-muted-foreground/50 hover:bg-muted/30 transition-colors"
            >
              <Upload className="w-5 h-5 mb-1" />
              <span className="text-xs">Add</span>
            </button>
          )}
        </div>
        <input
          ref={inputRef}
          type="file"
          accept=".jpg,.jpeg,.png,.webp"
          multiple
          onChange={(e) => {
            onAddImages(e.target.files)
            e.target.value = ""
          }}
          className="hidden"
        />
      </div>

      <div className="grid gap-2">
        <Label htmlFor={`short-${item.id}`}>Short Description *</Label>
        <Input
          id={`short-${item.id}`}
          placeholder="One-line summary"
          value={item.shortDescription}
          onChange={(e) => onUpdate({ shortDescription: e.target.value })}
        />
      </div>

      <div className="grid gap-2">
        <Label htmlFor={`long-${item.id}`}>Detailed Description</Label>
        <Textarea
          id={`long-${item.id}`}
          placeholder={`Describe this ${label.toLowerCase()} in detail`}
          value={item.longDescription}
          onChange={(e) => onUpdate({ longDescription: e.target.value })}
          rows={4}
        />
      </div>

      {/* Pricing */}
      <div className="grid gap-4 pt-2 border-t border-border">
        <h4 className="text-sm font-medium text-foreground pt-3">Pricing (optional)</h4>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="grid gap-2">
            <Label htmlFor={`mrp-${item.id}`}>MRP</Label>
            <Input
              id={`mrp-${item.id}`}
              type="number"
              placeholder="₹ 0.00"
              value={item.mrp}
              onChange={(e) => onUpdate({ mrp: e.target.value })}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor={`listPrice-${item.id}`}>List Price</Label>
            <Input
              id={`listPrice-${item.id}`}
              type="number"
              placeholder="₹ 0.00"
              value={item.listPrice}
              onChange={(e) => onUpdate({ listPrice: e.target.value })}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor={`discount-${item.id}`}>Discount</Label>
            <Input
              id={`discount-${item.id}`}
              placeholder="e.g., 10% or ₹100"
              value={item.discount}
              onChange={(e) => onUpdate({ discount: e.target.value })}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor={`salePrice-${item.id}`}>Sale Price</Label>
            <Input
              id={`salePrice-${item.id}`}
              type="number"
              placeholder="₹ 0.00"
              value={item.salePrice}
              onChange={(e) => onUpdate({ salePrice: e.target.value })}
            />
          </div>
        </div>
      </div>
    </div>
  )
}