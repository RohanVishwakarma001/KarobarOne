"use client";

import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { ImageOff, Loader2, Upload } from "lucide-react";
import { cn } from "@/lib/utils";

const ACCEPTED_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"];
const MAX_SIZE_BYTES = 5 * 1024 * 1024;

export function VariantImageDropzone({
  previewUrl,
  uploading,
  onFileSelected,
}: {
  previewUrl: string | null;
  uploading: boolean;
  onFileSelected: (file: File) => void;
}) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateAndEmit = (file: File | undefined) => {
    if (!file) return;
    if (!ACCEPTED_TYPES.includes(file.type)) {
      setError("PNG, JPG, WEBP or GIF only");
      return;
    }
    if (file.size > MAX_SIZE_BYTES) {
      setError("Max 5MB");
      return;
    }
    setError(null);
    onFileSelected(file);
  };

  return (
    <div className="w-20 shrink-0">
      <motion.button
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setIsDragging(false);
          validateAndEmit(e.dataTransfer.files?.[0]);
        }}
        whileHover={{ scale: 1.04 }}
        whileTap={{ scale: 0.97 }}
        className={cn(
          "relative flex h-16 w-16 items-center justify-center overflow-hidden rounded-xl border-2 border-dashed transition-colors",
          isDragging ? "border-[#5b4ef9] bg-[#5b4ef9]/5" : "border-slate-200 bg-slate-50 hover:border-slate-300",
        )}
      >
        {uploading ? (
          <Loader2 className="h-5 w-5 animate-spin text-slate-400" />
        ) : previewUrl ? (
          <img src={previewUrl} alt="" className="h-full w-full object-cover" />
        ) : (
          <Upload className="h-5 w-5 text-slate-400" />
        )}
      </motion.button>
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED_TYPES.join(",")}
        className="hidden"
        onChange={(e) => validateAndEmit(e.target.files?.[0])}
      />
      {error && (
        <p className="mt-1 flex items-center gap-1 text-[10px] leading-tight text-red-500">
          <ImageOff className="h-2.5 w-2.5 shrink-0" />
          {error}
        </p>
      )}
    </div>
  );
}
