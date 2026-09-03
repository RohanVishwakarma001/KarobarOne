"use client";

import { useEffect, useState } from "react";
import { useVariantImages, useDeleteVariantImage, useUploadVariantImage } from "@/hooks/use-variants";
import { VariantImageGallery, type GalleryImage } from "./variant-image-gallery";
import type { ProductImageResponse } from "@/lib/api/variants";

function toGalleryImage(img: ProductImageResponse): GalleryImage {
  return { id: img.id, url: img.url, isPrimary: img.isPrimary };
}

/**
 * The full drag-reorder gallery, live-wired to the backend — only usable
 * once a variant has a real id (upload/list/delete all key off variantId).
 * Reorder and "set primary" stay local-only: there's no PATCH endpoint on
 * ProductImage to persist isPrimary after creation, and sort_order is
 * already aliased to fileSize server-side (see variant-image-gallery.tsx's
 * doc comment) — visually real, not yet durable.
 */
export function SavedVariantImageCell({ productId, variantId }: { productId: string; variantId: string }) {
  const imagesQuery = useVariantImages(productId, variantId);
  const uploadImage = useUploadVariantImage();
  const deleteImage = useDeleteVariantImage(productId, variantId);

  const [localImages, setLocalImages] = useState<GalleryImage[] | null>(null);

  useEffect(() => {
    if (imagesQuery.data) setLocalImages(imagesQuery.data.map(toGalleryImage));
  }, [imagesQuery.data]);

  const images = localImages ?? [];

  return (
    <VariantImageGallery
      images={images}
      uploading={uploadImage.isPending}
      onReorder={setLocalImages}
      onSetPrimary={(id) => setLocalImages(images.map((img) => ({ ...img, isPrimary: img.id === id })))}
      onRemove={(id) => {
        setLocalImages(images.filter((img) => img.id !== id));
        deleteImage.mutate(id);
      }}
      onFilesSelected={async (files) => {
        for (const file of files) {
          const created = await uploadImage.mutateAsync({ productId, variantId, file, isPrimary: images.length === 0 });
          setLocalImages((prev) => [...(prev ?? []), toGalleryImage(created)]);
        }
      }}
    />
  );
}
