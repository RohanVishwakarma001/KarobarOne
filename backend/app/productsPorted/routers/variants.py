# Owner - pradhansaikat123@gmail.com

# Variants API endpoints. Supports CRUD, tenant-wide SKU uniqueness, tenant
# mismatch rejection, and duplicate attribute combination validation.
#
# Two routers share the same helpers below:
#   - `router` (prefix "/variants", flat, body-driven — original shape)
#   - `productVariantsRouter` (prefix "/products", nested under
#     /catalog/products/{productId}/variants — REST-conventional shape)
# Both are mounted under /api/v1/catalog in app/api/router.py.

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tenantResolver import getTenantIdAsUUID
from app.productsPorted.core.database import get_db
from app.productsPorted.models.models import Variant, Product
from app.productsPorted.schemas.schemas import (
    VariantBase,
    VariantCreate,
    VariantCreateForProduct,
    VariantResponse,
    VariantUpdate,
)

router = APIRouter(prefix="/variants", tags=["Products - Variants"])
productVariantsRouter = APIRouter(prefix="/products", tags=["Products - Variants"])


# ── SHARED HELPERS ───────────────────────────
async def _getProductOrNotFound(db: AsyncSession, productId: UUID) -> Product:
    result = await db.execute(select(Product).where(Product.id == productId, Product.deletedAt.is_(None)))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def _assertTenantMatches(product: Product, tenantId: UUID) -> None:
    """Rejects cross-tenant writes — a store cannot add variants to another tenant's product."""
    if product.tenantId != tenantId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant mismatch: this product does not belong to the given tenant",
        )


def _attributeCombinationsEqual(dict1: Optional[dict], dict2: Optional[dict]) -> bool:
    """Checks if two attribute dictionaries are equal, ignoring ordering."""
    if not dict1 and not dict2:
        return True
    if not dict1 or not dict2:
        return False
    return dict1 == dict2


async def _assertNoDuplicateAttributeCombo(
    db: AsyncSession, productId: UUID, attributes: Optional[dict], excludeVariantId: Optional[UUID] = None
) -> None:
    stmt = select(Variant).where(Variant.productId == productId)
    if excludeVariantId:
        stmt = stmt.where(Variant.id != excludeVariantId)
    existing = (await db.execute(stmt)).scalars().all()
    for var in existing:
        if _attributeCombinationsEqual(var.attributes, attributes):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A variant with this exact combination of attributes already exists for this product.",
            )


async def _assertSkuAvailable(
    db: AsyncSession, tenantId: UUID, sku: str, excludeVariantId: Optional[UUID] = None
) -> None:
    """SKUs must be unique across the whole tenant's catalog, not just within one product."""
    stmt = select(Variant).join(Product, Variant.productId == Product.id).where(
        Product.tenantId == tenantId,
        Variant.sku == sku,
    )
    if excludeVariantId:
        stmt = stmt.where(Variant.id != excludeVariantId)
    if (await db.execute(stmt)).scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"SKU '{sku}' is already used by another variant in this tenant's catalog",
        )


async def _createVariantForProduct(db: AsyncSession, product: Product, tenantId: UUID, data: VariantBase) -> Variant:
    _assertTenantMatches(product, tenantId)
    await _assertSkuAvailable(db, tenantId, data.sku)
    await _assertNoDuplicateAttributeCombo(db, product.id, data.attributes)

    variant = Variant(
        productId=product.id,
        sku=data.sku,
        price=data.price,
        inventory=data.inventory,
        attributes=data.attributes,
    )
    db.add(variant)
    await db.commit()
    await db.refresh(variant)
    return variant


async def _listVariantsForProduct(db: AsyncSession, productId: UUID) -> List[Variant]:
    result = await db.execute(select(Variant).where(Variant.productId == productId))
    return list(result.scalars().all())


async def _getVariantOrNotFound(db: AsyncSession, variantId: UUID) -> Variant:
    result = await db.execute(select(Variant).where(Variant.id == variantId))
    variant = result.scalar_one_or_none()
    if not variant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant not found")
    return variant


async def _updateVariantRecord(db: AsyncSession, variant: Variant, payload: VariantUpdate) -> Variant:
    updateData = payload.model_dump(exclude_none=True)
    tenantId = variant.tenantId

    if "sku" in updateData:
        await _assertSkuAvailable(db, tenantId, updateData["sku"], excludeVariantId=variant.id)
    if "attributes" in updateData:
        await _assertNoDuplicateAttributeCombo(db, variant.productId, updateData["attributes"], excludeVariantId=variant.id)

    for field, value in updateData.items():
        setattr(variant, field, value)

    await db.commit()
    await db.refresh(variant)
    return variant


async def _deleteVariantRecord(db: AsyncSession, variant: Variant) -> None:
    await db.delete(variant)
    await db.commit()


# ── FLAT ROUTER: /api/v1/catalog/variants ────
@router.post("/", response_model=VariantResponse, status_code=status.HTTP_201_CREATED)
async def create_variant(payload: VariantCreate, db: AsyncSession = Depends(get_db)):
    product = await _getProductOrNotFound(db, payload.productId)
    return await _createVariantForProduct(db, product, payload.tenantId, payload)


@router.get("/", response_model=List[VariantResponse])
async def list_variants(productId: UUID, db: AsyncSession = Depends(get_db)):
    await _getProductOrNotFound(db, productId)
    return await _listVariantsForProduct(db, productId)


@router.get("/{variantId}", response_model=VariantResponse)
async def get_variant(variantId: UUID, db: AsyncSession = Depends(get_db)):
    return await _getVariantOrNotFound(db, variantId)


@router.patch("/{variantId}", response_model=VariantResponse)
async def update_variant(variantId: UUID, payload: VariantUpdate, db: AsyncSession = Depends(get_db)):
    variant = await _getVariantOrNotFound(db, variantId)
    return await _updateVariantRecord(db, variant, payload)


@router.delete("/{variantId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(variantId: UUID, db: AsyncSession = Depends(get_db)):
    variant = await _getVariantOrNotFound(db, variantId)
    await _deleteVariantRecord(db, variant)


# ── NESTED ROUTER: /api/v1/catalog/products/{productId}/variants ────
@productVariantsRouter.get("/{productId}/variants", response_model=List[VariantResponse])
async def list_variants_for_product(productId: UUID, db: AsyncSession = Depends(get_db)):
    await _getProductOrNotFound(db, productId)
    return await _listVariantsForProduct(db, productId)


@productVariantsRouter.post(
    "/{productId}/variants", response_model=VariantResponse, status_code=status.HTTP_201_CREATED
)
async def create_variant_for_product(
    productId: UUID,
    payload: VariantCreateForProduct,
    tenantId: UUID = Depends(getTenantIdAsUUID),
    db: AsyncSession = Depends(get_db),
):
    product = await _getProductOrNotFound(db, productId)
    return await _createVariantForProduct(db, product, tenantId, payload)


@productVariantsRouter.put("/{productId}/variants/{variantId}", response_model=VariantResponse)
async def replace_variant_for_product(
    productId: UUID, variantId: UUID, payload: VariantCreateForProduct, db: AsyncSession = Depends(get_db)
):
    """PUT replaces sku/price/inventory/attributes wholesale (all VariantBase fields are required on this schema)."""
    variant = await _getVariantOrNotFound(db, variantId)
    if variant.productId != productId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant not found for this product")
    return await _updateVariantRecord(db, variant, VariantUpdate(**payload.model_dump()))


@productVariantsRouter.delete("/{productId}/variants/{variantId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant_for_product(productId: UUID, variantId: UUID, db: AsyncSession = Depends(get_db)):
    variant = await _getVariantOrNotFound(db, variantId)
    if variant.productId != productId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant not found for this product")
    await _deleteVariantRecord(db, variant)
