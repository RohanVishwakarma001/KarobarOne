# Owner - pradhansaikat123@gmail.com

# Attributes API endpoints. Supports CRUD for attributes,
# and mapping attributes to products with uniqueness validation.

# Import uuid module for generating UUIDs
import uuid
# Import List and Optional from typing for type declarations
from typing import List, Optional
# Import UUID from uuid for unique identifier support
from uuid import UUID
# Import datetime and timezone from datetime for handling dates
from datetime import datetime, timezone

# Import APIRouter, Depends, HTTPException, and status from fastapi
from fastapi import APIRouter, Depends, HTTPException, status
# Import select from sqlalchemy for database queries
from sqlalchemy import select
# Import selectinload from sqlalchemy.orm to eager load relations
from sqlalchemy.orm import selectinload
# Import AsyncSession from sqlalchemy.ext.asyncio for asynchronous sessions
from sqlalchemy.ext.asyncio import AsyncSession

# Import get_db session dependency injection helper
from app.productsPorted.core.database import get_db
# Import Attribute, ProductAttributeMapping, Product, Category models
from app.productsPorted.models.models import Attribute, ProductAttributeMapping, Product, Category
# Import schemas from app schemas
from app.productsPorted.schemas.schemas import (
    AttributeCreate,
    AttributeResponse,
    AttributeUpdate,
    ProductAttributeMappingCreate,
    ProductAttributeMappingResponse
)

router = APIRouter(prefix="/attributes", tags=["Products - Attributes"])


# ── CREATE ATTRIBUTE MASTER ──────────────────
@router.post("/", response_model=AttributeResponse, status_code=status.HTTP_201_CREATED)
async def create_attribute(payload: AttributeCreate, db: AsyncSession = Depends(get_db)):
    # 1. Fetch productId to satisfy PostgreSQL foreign key constraint
    if db.bind.dialect.name == "sqlite":
        productId = payload.tenantId
    else:
        # Find an existing product for this tenant
        prodRes = await db.execute(select(Product).where(Product.tenantId == payload.tenantId).limit(1))
        product = prodRes.scalar_one_or_none()
        if not product:
            # Find or create default category
            catRes = await db.execute(select(Category).where(Category.tenantId == payload.tenantId).limit(1))
            category = catRes.scalar_one_or_none()
            if not category:
                category = Category(
                    tenantId=payload.tenantId,
                    name="Default Category",
                    slug="default-category",
                    categoryType="PRODUCT",
                    createdBy=uuid.uuid4()
                )
                db.add(category)
                await db.flush()

            # Create default product
            product = Product(
                tenantId=payload.tenantId,
                storeId=payload.tenantId,
                name="System Default Product",
                slug=f"system-default-{uuid.uuid4().hex[:8]}",
                sku=f"SYS-DEF-{uuid.uuid4().hex[:8].upper()}",
                productType="PHYSICAL",
                categoryId=category.id,
                status="DRAFT",
                createdBy=uuid.uuid4()
            )
            db.add(product)
            await db.flush()
        productId = product.id

    # 2. Duplicate check: tenantId + code
    if db.bind.dialect.name == "sqlite":
        dup = await db.execute(
            select(Attribute).where(
                Attribute.productId == payload.tenantId,
                Attribute.code == payload.code
            )
        )
    else:
        dup = await db.execute(
            select(Attribute)
            .join(Product, Attribute.productId == Product.id)
            .where(
                Product.tenantId == payload.tenantId,
                Attribute.code == payload.code
            )
        )
    if dup.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Attribute with this code already exists for this tenant")

    attribute = Attribute(
        id=uuid.uuid4(),
        productId=productId,
        name=payload.name,
        code=payload.code,
        type=payload.type,
        tenantId=payload.tenantId
    )
    db.add(attribute)
    await db.commit()
    await db.refresh(attribute)
    return attribute


# ── LIST ATTRIBUTES ──────────────────────────
@router.get("/", response_model=List[AttributeResponse])
async def list_attributes(tenantId: UUID, db: AsyncSession = Depends(get_db)):
    if db.bind.dialect.name == "sqlite":
        result = await db.execute(
            select(Attribute).where(
                Attribute.productId == tenantId
            )
        )
    else:
        result = await db.execute(
            select(Attribute)
            .join(Product, Attribute.productId == Product.id)
            .where(
                Product.tenantId == tenantId
            )
        )
    return result.scalars().all()


# ── GET ATTRIBUTE BY ID ──────────────────────
@router.get("/{attributeId}", response_model=AttributeResponse)
async def get_attribute(attributeId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Attribute).where(
            Attribute.id == attributeId
        )
    )
    attribute = result.scalar_one_or_none()
    if not attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return attribute


# ── UPDATE ATTRIBUTE ─────────────────────────
@router.patch("/{attributeId}", response_model=AttributeResponse)
async def update_attribute(
    attributeId: UUID, payload: AttributeUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Attribute).where(
            Attribute.id == attributeId
        )
    )
    attribute = result.scalar_one_or_none()
    if not attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")

    updateData = payload.model_dump(exclude_none=True)

    if "code" in updateData:
        if db.bind.dialect.name == "sqlite":
            dup = await db.execute(
                select(Attribute).where(
                    Attribute.productId == attribute.tenantId,
                    Attribute.code == updateData["code"],
                    Attribute.id != attributeId
                )
            )
        else:
            dup = await db.execute(
                select(Attribute)
                .join(Product, Attribute.productId == Product.id)
                .where(
                    Product.tenantId == attribute.tenantId,
                    Attribute.code == updateData["code"],
                    Attribute.id != attributeId
                )
            )
        if dup.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Attribute with this code already exists")

    for field, value in updateData.items():
        setattr(attribute, field, value)

    await db.commit()
    await db.refresh(attribute)
    return attribute


# ── DELETE ATTRIBUTE ─────────────────────────
@router.delete("/{attributeId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attribute(attributeId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Attribute).where(
            Attribute.id == attributeId
        )
    )
    attribute = result.scalar_one_or_none()
    if not attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")

    await db.delete(attribute)
    await db.commit()


# ── LINK ATTRIBUTE TO PRODUCT (Mapping) ──────
@router.post("/mappings", response_model=ProductAttributeMappingResponse, status_code=status.HTTP_201_CREATED)
async def create_product_attribute_mapping(
    productId: UUID,
    payload: ProductAttributeMappingCreate,
    db: AsyncSession = Depends(get_db)
):
    # Verify product exists
    prod = await db.execute(select(Product).where(Product.id == productId, Product.deletedAt.is_(None)))
    if not prod.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")

    # Verify attribute exists
    attr = await db.execute(select(Attribute).where(Attribute.id == payload.attributeId))
    if not attr.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Attribute not found")

    dup = await db.execute(
        select(ProductAttributeMapping)
        .where(
            ProductAttributeMapping.attributeId == payload.attributeId
        )
    )
    if dup.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="This attribute is already mapped to this product. Use PUT/PATCH to update the value.")

    mapping = ProductAttributeMapping(
        productId=productId,
        attributeId=payload.attributeId,
        value=payload.value
    )
    db.add(mapping)
    await db.commit()
    await db.refresh(mapping)
    return mapping


# ── GET PRODUCT ATTRIBUTE MAPPINGS ───────────
@router.get("/mappings/{productId}", response_model=List[ProductAttributeMappingResponse])
async def list_product_attribute_mappings(productId: UUID, db: AsyncSession = Depends(get_db)):
    # Verify product exists
    prodRes = await db.execute(select(Product).where(Product.id == productId, Product.deletedAt.is_(None)))
    productObj = prodRes.scalar_one_or_none()
    if not productObj:
        raise HTTPException(status_code=404, detail="Product not found")

    if db.bind.dialect.name == "sqlite":
        result = await db.execute(
            select(ProductAttributeMapping)
            .options(selectinload(ProductAttributeMapping.attribute))
            .join(Attribute)
            .where(Attribute.productId == productObj.tenantId)
        )
    else:
        result = await db.execute(
            select(ProductAttributeMapping)
            .options(selectinload(ProductAttributeMapping.attribute))
            .join(Attribute)
            .where(Attribute.productId == productId)
        )
    return result.scalars().all()


# ── REMOVE MAPPING ───────────────────────────
@router.delete("/mappings/{mappingId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_attribute_mapping(mappingId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProductAttributeMapping).where(ProductAttributeMapping.id == mappingId)
    )
    mapping = result.scalar_one_or_none()
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")

    await db.delete(mapping)
    await db.commit()
