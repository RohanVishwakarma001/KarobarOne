"use client";

import { use, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { motion } from "framer-motion";
import { ArrowLeft, Save } from "lucide-react";

import { useRequireAuth } from "@/hooks/use-require-auth";
import { useProductVariants, useCreateVariant, useUpdateVariant, useDeleteVariant, useUploadVariantImage } from "@/hooks/use-variants";
import { AttributeAxisEditor, type AttributeAxis } from "@/components/variants/attribute-axis-editor";
import { VariantMatrixTable } from "@/components/variants/variant-matrix-table";
import { variantMatrixSchema, type VariantMatrixValues, type VariantRowValues } from "@/lib/validation/variants";
import { AnimatedButton, type AsyncButtonStatus } from "@/components/ui/animated-button";
import { Skeleton } from "@/components/ui/skeleton";
import type { VariantResponse } from "@/lib/api/variants";

function toRowValues(variant: VariantResponse): VariantRowValues {
  return {
    clientId: variant.id,
    variantId: variant.id,
    sku: variant.sku,
    price: variant.price,
    inventory: variant.inventory,
    attributes: variant.attributes ?? {},
  };
}

export default function ProductVariantsPage({ params }: { params: Promise<{ productId: string }> }) {
  const { productId } = use(params);
  const { session, ready } = useRequireAuth();
  const tenantId = session?.tenantId ?? "";

  const variantsQuery = useProductVariants(productId);
  const createVariant = useCreateVariant(productId, tenantId);
  const updateVariant = useUpdateVariant(productId);
  const deleteVariant = useDeleteVariant(productId);
  const uploadImage = useUploadVariantImage();

  const [axes, setAxes] = useState<AttributeAxis[]>([]);
  const [imagePreviews, setImagePreviews] = useState<Record<string, string>>({});
  const [uploadingClientIds, setUploadingClientIds] = useState<Set<string>>(new Set());
  const [saveStatus, setSaveStatus] = useState<AsyncButtonStatus>("idle");
  const pendingFiles = useRef<Map<string, File>>(new Map());
  const hasSeeded = useRef(false);

  const form = useForm<VariantMatrixValues>({
    resolver: zodResolver(variantMatrixSchema),
    defaultValues: { rows: [] },
  });
  const { fields, append, remove, replace } = useFieldArray({ control: form.control, name: "rows" });
  const { setValue } = form;

  // Seed the matrix from persisted variants exactly once, so in-progress local
  // edits (typing a price, generating new rows) never get clobbered by a
  // background refetch.
  useEffect(() => {
    if (hasSeeded.current || !variantsQuery.data) return;
    replace(variantsQuery.data.map(toRowValues));
    hasSeeded.current = true;
  }, [variantsQuery.data, replace]);

  const handleGenerate = (combinations: Record<string, string>[]) => {
    const existingCombos = new Set(fields.map((f) => JSON.stringify(f.attributes)));
    const newRows = combinations
      .filter((combo) => !existingCombos.has(JSON.stringify(combo)))
      .map<VariantRowValues>((combo) => ({
        clientId: crypto.randomUUID(),
        sku: Object.values(combo).join("-").toUpperCase().replace(/\s+/g, ""),
        price: 0,
        inventory: 0,
        attributes: combo,
      }));
    if (newRows.length === 0) {
      toast.info("Those combinations already exist in the table.");
      return;
    }
    append(newRows);
    toast.success(`${newRows.length} variant${newRows.length === 1 ? "" : "s"} added — set price/stock and save.`);
  };

  const handleImageSelected = async (clientId: string, file: File) => {
    const objectUrl = URL.createObjectURL(file);
    setImagePreviews((prev) => ({ ...prev, [clientId]: objectUrl }));

    const rowIndex = fields.findIndex((f) => f.clientId === clientId);
    const variantId = rowIndex >= 0 ? form.getValues(`rows.${rowIndex}.variantId`) : undefined;

    if (!variantId) {
      // Row hasn't been saved yet — hold the file and upload right after this
      // row gets its variantId back from the create call in onSubmit below.
      pendingFiles.current.set(clientId, file);
      return;
    }

    setUploadingClientIds((prev) => new Set(prev).add(clientId));
    try {
      await uploadImage.mutateAsync({ productId, variantId, file, isPrimary: true });
      toast.success("Image uploaded.");
    } finally {
      setUploadingClientIds((prev) => {
        const next = new Set(prev);
        next.delete(clientId);
        return next;
      });
    }
  };

  const handleDeleteRow = async (index: number, row: VariantRowValues) => {
    if (row.variantId) {
      await deleteVariant.mutateAsync(row.variantId);
    }
    remove(index);
  };

  const onSubmit = form.handleSubmit(async (values) => {
    setSaveStatus("pending");
    const results = await Promise.allSettled(
      values.rows.map(async (row, index) => {
        const payload = { sku: row.sku, price: row.price, inventory: row.inventory, attributes: row.attributes };

        if (row.variantId) {
          await updateVariant.mutateAsync({ variantId: row.variantId, input: payload });
          return;
        }

        const created = await createVariant.mutateAsync(payload);
        setValue(`rows.${index}.variantId`, created.id);

        const pending = pendingFiles.current.get(row.clientId);
        if (pending) {
          pendingFiles.current.delete(row.clientId);
          setUploadingClientIds((prev) => new Set(prev).add(row.clientId));
          try {
            await uploadImage.mutateAsync({ productId, variantId: created.id, file: pending, isPrimary: true });
          } finally {
            setUploadingClientIds((prev) => {
              const next = new Set(prev);
              next.delete(row.clientId);
              return next;
            });
          }
        }
      }),
    );

    const failed = results.filter((r) => r.status === "rejected").length;
    const succeeded = results.length - failed;
    if (failed === 0) {
      setSaveStatus("success");
      toast.success(`Saved ${succeeded} variant${succeeded === 1 ? "" : "s"}.`);
    } else {
      setSaveStatus("error");
      toast.error(`Saved ${succeeded}, ${failed} failed — check the highlighted rows and retry.`);
    }
  });

  if (!ready) return null;

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <Link
            href="/store-owner-dashboard"
            className="inline-flex items-center gap-1.5 text-xs font-medium uppercase tracking-[0.24em] text-slate-500 hover:text-[#5b4ef9]"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Store owner portal
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <h1 className="text-3xl font-semibold tracking-tight">Variants & options</h1>
        <p className="mt-1 text-sm text-slate-500">Build the size/color matrix, then fine-tune price and stock per variant.</p>

        <div className="mt-6">
          <AttributeAxisEditor axes={axes} onAxesChange={setAxes} onGenerate={handleGenerate} />
        </div>

        <motion.section
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.25 }}
          className="mt-6 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6"
        >
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Variants</h2>
            <AnimatedButton
              type="button"
              onClick={onSubmit}
              disabled={fields.length === 0}
              status={saveStatus}
              icon={<Save className="h-4 w-4" />}
              label="Save all variants"
              loadingLabel="Saving…"
              successLabel="All saved"
              errorLabel="Some failed"
              className="bg-[#5b4ef9] hover:bg-[#4a3ee0]"
            />
          </div>

          <div className="mt-4">
            {variantsQuery.isLoading ? (
              <div className="space-y-2">
                {Array.from({ length: 3 }).map((_, i) => (
                  <Skeleton key={i} className="h-16 w-full rounded-xl" />
                ))}
              </div>
            ) : (
              <VariantMatrixTable
                control={form.control}
                fields={fields}
                errors={form.formState.errors}
                productId={productId}
                imagePreviews={imagePreviews}
                uploadingClientIds={uploadingClientIds}
                onImageSelected={handleImageSelected}
                onDeleteRow={handleDeleteRow}
              />
            )}
          </div>
        </motion.section>
      </main>
    </div>
  );
}
