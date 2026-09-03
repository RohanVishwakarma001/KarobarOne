"use client";

import { AnimatePresence, motion } from "framer-motion";
import { Trash2 } from "lucide-react";
import type { Control, FieldArrayWithId, FieldErrors } from "react-hook-form";
import { Controller } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { VariantImageDropzone } from "./variant-image-dropzone";
import { SavedVariantImageCell } from "./variant-image-cell";
import type { VariantMatrixValues, VariantRowValues } from "@/lib/validation/variants";

export function VariantMatrixTable({
  control,
  fields,
  errors,
  productId,
  imagePreviews,
  uploadingClientIds,
  onImageSelected,
  onDeleteRow,
}: {
  control: Control<VariantMatrixValues>;
  fields: FieldArrayWithId<VariantMatrixValues, "rows", "id">[];
  errors: FieldErrors<VariantMatrixValues>;
  /** Only needed for persisted rows — their image gallery is live-wired to /catalog/images. */
  productId: string;
  imagePreviews: Record<string, string>;
  uploadingClientIds: Set<string>;
  onImageSelected: (clientId: string, file: File) => void;
  onDeleteRow: (index: number, row: VariantRowValues) => void;
}) {
  if (fields.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-200 py-12 text-center text-sm text-slate-400">
        No variants yet. Add option axes above and click &ldquo;Generate variants&rdquo;.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-100">
      <Table>
        <TableHeader>
          <TableRow className="bg-slate-50/80 hover:bg-slate-50/80">
            <TableHead className="w-44">Images</TableHead>
            <TableHead>Options</TableHead>
            <TableHead className="w-40">SKU</TableHead>
            <TableHead className="w-28">Price</TableHead>
            <TableHead className="w-24">Stock</TableHead>
            <TableHead className="w-12" />
          </TableRow>
        </TableHeader>
        <TableBody>
          <AnimatePresence mode="popLayout" initial={false}>
            {fields.map((field, index) => {
              const rowErrors = errors.rows?.[index];
              return (
                <motion.tr
                  key={field.id}
                  layout
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, x: -8 }}
                  transition={{ duration: 0.2 }}
                  className="border-b border-slate-100 align-top last:border-0"
                >
                  <TableCell>
                    {field.variantId ? (
                      <SavedVariantImageCell productId={productId} variantId={field.variantId} />
                    ) : (
                      <VariantImageDropzone
                        previewUrl={imagePreviews[field.clientId] ?? null}
                        uploading={uploadingClientIds.has(field.clientId)}
                        onFileSelected={(file) => onImageSelected(field.clientId, file)}
                      />
                    )}
                  </TableCell>
                  <TableCell>
                    <div className="flex flex-wrap gap-1.5 pt-2">
                      {Object.entries(field.attributes).map(([axis, value]) => (
                        <span
                          key={axis}
                          className="rounded-full bg-[#5b4ef9]/10 px-2.5 py-0.5 text-xs font-medium text-[#5b4ef9]"
                        >
                          {axis}: {value}
                        </span>
                      ))}
                      {field.variantId && (
                        <span className="rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-600">
                          Saved
                        </span>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Controller
                      control={control}
                      name={`rows.${index}.sku`}
                      render={({ field: f }) => <Input {...f} placeholder="SKU" aria-invalid={Boolean(rowErrors?.sku)} />}
                    />
                    {rowErrors?.sku && <p className="mt-1 text-xs text-red-500">{rowErrors.sku.message}</p>}
                  </TableCell>
                  <TableCell>
                    <Controller
                      control={control}
                      name={`rows.${index}.price`}
                      render={({ field: f }) => (
                        <Input
                          {...f}
                          type="number"
                          step="0.01"
                          min={0}
                          aria-invalid={Boolean(rowErrors?.price)}
                        />
                      )}
                    />
                    {rowErrors?.price && <p className="mt-1 text-xs text-red-500">{rowErrors.price.message}</p>}
                  </TableCell>
                  <TableCell>
                    <Controller
                      control={control}
                      name={`rows.${index}.inventory`}
                      render={({ field: f }) => <Input {...f} type="number" min={0} aria-invalid={Boolean(rowErrors?.inventory)} />}
                    />
                    {rowErrors?.inventory && <p className="mt-1 text-xs text-red-500">{rowErrors.inventory.message}</p>}
                  </TableCell>
                  <TableCell>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="text-slate-400 hover:text-red-500"
                      onClick={() => onDeleteRow(index, field)}
                    >
                      <Trash2 className="h-4 w-4" />
                      <span className="sr-only">Remove variant</span>
                    </Button>
                  </TableCell>
                </motion.tr>
              );
            })}
          </AnimatePresence>
        </TableBody>
      </Table>
    </div>
  );
}
