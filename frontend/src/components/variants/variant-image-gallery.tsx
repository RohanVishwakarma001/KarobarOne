"use client";

import { useState } from "react";
import { Reorder, motion } from "framer-motion";
import { GripVertical, Loader2, Star, Upload, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { springs, useReducedMotion } from "@/lib/motion";

export type GalleryImage = {
  id: string;
  url: string;
  isPrimary: boolean;
};

const ACCEPTED_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"];
const MAX_SIZE_BYTES = 5 * 1024 * 1024;

/**
 * Multi-image gallery with drag-to-reorder (framer-motion's Reorder
 * primitives — physically picks up and displaces neighbors, not just a
 * ghost-drag) plus a trailing drop target for adding more.
 *
 * Reorder is local-only right now: the backend's ProductImage.sortOrder
 * column is already aliased to store fileSize (see
 * app/productsPorted/models/models.py::ProductImage.fileSize — it's a
 * hybrid_property that writes through to sort_order), so there's nowhere to
 * durably persist a real display order without a schema change. `onReorder`
 * is still wired up (updates local order immediately, feels real) — persist
 * it once a dedicated column exists.
 */
export function VariantImageGallery({
  images,
  onReorder,
  onRemove,
  onSetPrimary,
  onFilesSelected,
  uploading,
}: {
  images: GalleryImage[];
  onReorder: (next: GalleryImage[]) => void;
  onRemove: (id: string) => void;
  onSetPrimary: (id: string) => void;
  onFilesSelected: (files: File[]) => void;
  uploading: boolean;
}) {
  const reducedMotion = useReducedMotion();
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateAndEmit = (fileList: FileList | null) => {
    if (!fileList || fileList.length === 0) return;
    const files = Array.from(fileList);
    const invalid = files.find((f) => !ACCEPTED_TYPES.includes(f.type) || f.size > MAX_SIZE_BYTES);
    if (invalid) {
      setError(!ACCEPTED_TYPES.includes(invalid.type) ? "PNG, JPG, WEBP or GIF only" : "Max 5MB per image");
      return;
    }
    setError(null);
    onFilesSelected(files);
  };

  return (
    <div className="flex flex-wrap items-center gap-2">
      <Reorder.Group
        as="div"
        axis="x"
        values={images}
        onReorder={onReorder}
        className="flex flex-wrap items-center gap-2"
      >
        {images.map((img) => (
          <Reorder.Item
            key={img.id}
            value={img}
            as="div"
            whileDrag={reducedMotion ? undefined : { scale: 1.08, zIndex: 10, boxShadow: "0 12px 28px -8px rgba(15,23,42,0.35)" }}
            transition={springs.snappy}
            className="group relative h-16 w-16 shrink-0 cursor-grab overflow-hidden rounded-xl border border-slate-200 bg-slate-50 active:cursor-grabbing"
          >
            <img src={img.url} alt="" className="pointer-events-none h-full w-full object-cover" draggable={false} />

            <div className="pointer-events-none absolute inset-0 flex items-start justify-between p-1 opacity-0 transition-opacity group-hover:opacity-100">
              <GripVertical className="pointer-events-none h-3.5 w-3.5 rounded bg-white/80 text-slate-500" />
              <button
                type="button"
                onPointerDown={(e) => e.stopPropagation()}
                onClick={() => onRemove(img.id)}
                className="pointer-events-auto rounded-full bg-white/90 p-0.5 text-slate-500 hover:text-red-500"
              >
                <X className="h-3 w-3" />
                <span className="sr-only">Remove image</span>
              </button>
            </div>

            <button
              type="button"
              onPointerDown={(e) => e.stopPropagation()}
              onClick={() => onSetPrimary(img.id)}
              className={cn(
                "pointer-events-auto absolute bottom-1 left-1 rounded-full p-0.5 transition-colors",
                img.isPrimary ? "bg-amber-400 text-white" : "bg-white/80 text-slate-400 opacity-0 group-hover:opacity-100",
              )}
            >
              <Star className={cn("h-3 w-3", img.isPrimary && "fill-current")} />
              <span className="sr-only">Set as primary image</span>
            </button>
          </Reorder.Item>
        ))}
      </Reorder.Group>

      <motion.button
        type="button"
        onClick={() => document.getElementById("gallery-file-input")?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setIsDragOver(false);
          validateAndEmit(e.dataTransfer.files);
        }}
        whileHover={reducedMotion ? undefined : { scale: 1.04 }}
        whileTap={reducedMotion ? undefined : { scale: 0.97 }}
        className={cn(
          "flex h-16 w-16 shrink-0 items-center justify-center rounded-xl border-2 border-dashed transition-colors",
          isDragOver ? "border-[#5b4ef9] bg-[#5b4ef9]/5" : "border-slate-200 bg-white hover:border-slate-300",
        )}
      >
        {uploading ? <Loader2 className="h-5 w-5 animate-spin text-slate-400" /> : <Upload className="h-5 w-5 text-slate-400" />}
      </motion.button>
      <input
        id="gallery-file-input"
        type="file"
        accept={ACCEPTED_TYPES.join(",")}
        multiple
        className="hidden"
        onChange={(e) => {
          validateAndEmit(e.target.files);
          e.target.value = "";
        }}
      />
      {error && <p className="w-full text-xs text-red-500">{error}</p>}
    </div>
  );
}
