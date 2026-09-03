# Owner - pradhansaikat123@gmail.com

# Products API endpoints. Supports CRUD, paginated searching & filtering, 
# brand approval restrictions, and status workflows (Draft, Pending, Published, Archived).

import uuid
import csv
import io
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, status
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.productsPorted.core.database import get_db
from app.productsPorted.models.models import Product, Brand, Category, ShippingProfile, ProductAttributeMapping
from app.productsPorted.schemas.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductPaginatedResponse,
    BulkImportResponse,
    BulkRowError
)

from app.db.models.approvals import AuditLog

router = APIRouter(prefix="/products", tags=["Products - Catalog"])


async def validate_brand_approval_for_publish(db: AsyncSession, brandId: Optional[UUID], statusValue: str):
    """
    Blocks publishing a product if it is linked to a brand that is not approved.
    """
    if statusValue == "PUBLISHED" and brandId is not None:
        brandRes = await db.execute(select(Brand).where(Brand.id == brandId, Brand.deletedAt.is_(None)))
        brand = brandRes.scalar_one_or_none()
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Associated brand does not exist."
            )
        if not brand.isApproved:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot publish product. Brand '{brand.name}' is not approved by owner."
            )


# ── CREATE PRODUCT ───────────────────────────
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    # 0. Check Plan Limits
    from app.core.planGuard import PlanGuard
    guard = PlanGuard(db)
    await guard.check_product_limit(payload.tenantId)

    # 1. Verify Category exists (if provided) or find/create default
    categoryId = payload.categoryId
    if not categoryId:
        # Find an existing category for this tenant
        catRes = await db.execute(select(Category).where(Category.tenantId == payload.tenantId, Category.deletedAt.is_(None)))
        existingCat = catRes.scalars().first()
        if not existingCat:
            # Create a default category
            defaultCat = Category(
                tenantId=payload.tenantId,
                name="Default Category",
                slug="default-category",
                categoryType="PRODUCT",
                createdBy=uuid.uuid4()
            )
            db.add(defaultCat)
            await db.flush()  # gets defaultCat.id
            categoryId = defaultCat.id
        else:
            categoryId = existingCat.id
    else:
        catRes = await db.execute(select(Category).where(Category.id == payload.categoryId, Category.deletedAt.is_(None)))
        if not catRes.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Category not found")

    # 2. Verify Brand exists (if provided)
    if payload.brandId:
        brandRes = await db.execute(select(Brand).where(Brand.id == payload.brandId, Brand.deletedAt.is_(None)))
        if not brandRes.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Brand not found")

    # 3. Verify Shipping Profile exists (if provided)
    if payload.shippingProfileId:
        shipRes = await db.execute(select(ShippingProfile).where(ShippingProfile.id == payload.shippingProfileId, ShippingProfile.isActive == True))
        if not shipRes.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Shipping Profile not found")

    # 4. Duplicate Check: SKU under same tenant & store
    dupSku = await db.execute(
        select(Product).where(
            Product.tenantId == payload.tenantId,
            Product.storeId == payload.storeId,
            Product.sku == payload.sku,
            Product.deletedAt.is_(None)
        )
    )
    if dupSku.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Product with this SKU already exists for this store")

    # 5. Duplicate Check: Slug under same tenant & store
    dupSlug = await db.execute(
        select(Product).where(
            Product.tenantId == payload.tenantId,
            Product.storeId == payload.storeId,
            Product.slug == payload.slug,
            Product.deletedAt.is_(None)
        )
    )
    if dupSlug.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Product with this slug already exists for this store")

    # 6. Validate Brand Approval before Publishing
    await validate_brand_approval_for_publish(db, payload.brandId, payload.status)

    data = payload.model_dump()
    data["categoryId"] = categoryId
    product = Product(**data)
    db.add(product)
    await db.commit()

    # Record Audit Log for Product Creation
    try:
        audit_entry = AuditLog(
            tenantId=product.tenantId,
            entityType="PRODUCT",
            entityId=product.id,
            actionType="CREATE",
            newValue={"name": product.name, "sku": product.sku, "status": product.status},
            performedBy=product.createdBy or product.tenantId,
        )
        db.add(audit_entry)
        await db.commit()
    except Exception:
        # Without this rollback the session is left in PendingRollbackError
        # state (a failed flush aborts the transaction), which then fails
        # every subsequent query on it — including the relation-load below.
        await db.rollback()

    # Load relations for response
    stmt = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.brand),
        selectinload(Product.shippingProfile),
        selectinload(Product.variants),
        selectinload(Product.images),
        selectinload(Product.attributeMappings).selectinload(ProductAttributeMapping.attribute)
    ).where(Product.id == product.id)
    res = await db.execute(stmt)
    return res.scalar_one()


# ── GET PRODUCT BY ID ────────────────────────
@router.get("/{productId}", response_model=ProductResponse)
async def get_product(productId: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.brand),
        selectinload(Product.shippingProfile),
        selectinload(Product.variants),
        selectinload(Product.images),
        selectinload(Product.attributeMappings).selectinload(ProductAttributeMapping.attribute)
    ).where(Product.id == productId, Product.deletedAt.is_(None))
    
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# ── UPDATE PRODUCT ───────────────────────────
@router.patch("/{productId}", response_model=ProductResponse)
async def update_product(
    productId: UUID, payload: ProductUpdate, db: AsyncSession = Depends(get_db)
):
    stmt = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.brand),
        selectinload(Product.shippingProfile),
        selectinload(Product.variants),
        selectinload(Product.images),
        selectinload(Product.attributeMappings).selectinload(ProductAttributeMapping.attribute)
    ).where(Product.id == productId, Product.deletedAt.is_(None))
    
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updateData = payload.model_dump(exclude_none=True)

    # Capture old values for audit log
    oldSnapshot = {
        col.key: (str(getattr(product, col.key)) if isinstance(getattr(product, col.key), UUID) else getattr(product, col.key))
        for col in product.__table__.columns if col.key in updateData
    }

    # Validate category, brand, and shipping profile if changed
    if "categoryId" in updateData and updateData["categoryId"]:
        catRes = await db.execute(select(Category).where(Category.id == updateData["categoryId"], Category.deletedAt.is_(None)))
        if not catRes.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Category not found")

    if "brandId" in updateData and updateData["brandId"]:
        brandRes = await db.execute(select(Brand).where(Brand.id == updateData["brandId"], Brand.deletedAt.is_(None)))
        if not brandRes.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Brand not found")

    if "shippingProfileId" in updateData and updateData["shippingProfileId"]:
        shipRes = await db.execute(select(ShippingProfile).where(ShippingProfile.id == updateData["shippingProfileId"], ShippingProfile.isActive == True))
        if not shipRes.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Shipping Profile not found")

    if "sku" in updateData:
        dupSku = await db.execute(
            select(Product).where(
                Product.tenantId == product.tenantId,
                Product.storeId == product.storeId,
                Product.sku == updateData["sku"],
                Product.id != productId,
                Product.deletedAt.is_(None)
            )
        )
        if dupSku.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Product with this SKU already exists")

    if "slug" in updateData:
        dupSlug = await db.execute(
            select(Product).where(
                Product.tenantId == product.tenantId,
                Product.storeId == product.storeId,
                Product.slug == updateData["slug"],
                Product.id != productId,
                Product.deletedAt.is_(None)
            )
        )
        if dupSlug.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Product with this slug already exists")

    # Validate Brand approval constraints when publishing
    targetStatus = updateData.get("status", product.status)
    targetBrandId = updateData.get("brandId", product.brandId)
    if "status" in updateData or "brandId" in updateData:
        await validate_brand_approval_for_publish(db, targetBrandId, targetStatus)

    for field, value in updateData.items():
        setattr(product, field, value)

    newSnapshot = {k: str(v) if isinstance(v, UUID) else v for k, v in updateData.items()}

    await db.commit()
    await db.refresh(product)

    # Audit log creation (best-effort: AuditLog is a main-app model — see the
    # matching note on create_product below — its table name doesn't match
    # what's actually provisioned in this database, so this must not be able
    # to break the update itself; failures are swallowed after rollback).
    try:
        audit_entry = AuditLog(
            tenantId=product.tenantId,
            entityType="PRODUCT",
            entityId=product.id,
            actionType="UPDATE",
            oldValue=oldSnapshot,
            newValue=newSnapshot,
            changedFields=list(updateData.keys()),
            performedBy=product.createdBy or product.tenantId,
        )
        db.add(audit_entry)
        await db.commit()
    except Exception:
        await db.rollback()
    return product


# ── DELETE PRODUCT (SOFT) ────────────────────
@router.delete("/{productId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(productId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).where(Product.id == productId, Product.deletedAt.is_(None))
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.deletedAt = datetime.now(timezone.utc).replace(tzinfo=None)
    await db.commit()

    # Audit log creation for delete (best-effort — see the note on
    # update_product above; must not be able to break the delete itself).
    try:
        audit_entry = AuditLog(
            tenantId=product.tenantId,
            entityType="PRODUCT",
            entityId=product.id,
            actionType="DELETE",
            oldValue={"name": product.name, "sku": product.sku},
            performedBy=product.createdBy or product.tenantId,
        )
        db.add(audit_entry)
        await db.commit()
    except Exception:
        await db.rollback()


# ── SEARCH / LIST PRODUCTS (PAGINATED & SORTED) ──────
@router.get("/", response_model=ProductPaginatedResponse)
async def search_products(
    tenantId: UUID,
    storeId: Optional[UUID] = Query(None),
    categoryId: Optional[UUID] = Query(None),
    brandId: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    productType: Optional[str] = Query(None),
    search: Optional[str] = Query(None, description="Search by product name or description"),
    sortBy: Optional[str] = Query("createdAt", description="Sort by field: e.g. name, sku, createdAt"),
    sortOrder: Optional[str] = Query("desc", description="asc or desc"),
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    # Construct base filters
    filters = [Product.tenantId == tenantId, Product.deletedAt.is_(None)]

    if storeId:
        filters.append(Product.storeId == storeId)
    if categoryId:
        filters.append(Product.categoryId == categoryId)
    if brandId:
        filters.append(Product.brandId == brandId)
    if status:
        filters.append(Product.status == status)
    if productType:
        filters.append(Product.productType == productType)
    if search:
        # Sanitize search query wildcards
        clean_search = search.replace("%", r"\%").replace("_", r"\_")
        filters.append(
            or_(
                Product.name.ilike(f"%{clean_search}%"),
                Product.description.ilike(f"%{clean_search}%")
            )
        )

    # 1. Count total matching
    countStmt = select(func.count(Product.id)).where(*filters)
    countRes = await db.execute(countStmt)
    total = countRes.scalar() or 0

    # 2. Query with eager loaded relationships
    stmt = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.brand),
        selectinload(Product.shippingProfile),
        selectinload(Product.variants),
        selectinload(Product.images),
        selectinload(Product.attributeMappings).selectinload(ProductAttributeMapping.attribute)
    ).where(*filters)

    # Apply sorting
    if sortBy == "name":
        orderCol = Product.name
    elif sortBy == "sku":
        orderCol = Product.sku
    else:
        orderCol = Product.createdAt

    if sortOrder.lower() == "desc":
        stmt = stmt.order_by(orderCol.desc())
    else:
        stmt = stmt.order_by(orderCol.asc())

    # Apply pagination
    stmt = stmt.offset((page - 1) * pageSize).limit(pageSize)
    
    result = await db.execute(stmt)
    products = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "pageSize": pageSize,
        "data": products
    }


# ── SUBMIT PRODUCT FOR APPROVAL ──────────────
@router.post("/{productId}/submit-approval", response_model=ProductResponse)
async def submit_product_approval(productId: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.brand),
        selectinload(Product.shippingProfile),
        selectinload(Product.variants),
        selectinload(Product.images),
        selectinload(Product.attributeMappings).selectinload(ProductAttributeMapping.attribute)
    ).where(Product.id == productId, Product.deletedAt.is_(None))
    
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Set status to PENDING
    product.status = "PENDING"
    await db.commit()
    await db.refresh(product)
    return product


# ── APPROVE PRODUCT (ADMIN WORKFLOW) ─────────
@router.post("/{productId}/approve", response_model=ProductResponse)
async def approve_product(productId: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.brand),
        selectinload(Product.shippingProfile),
        selectinload(Product.variants),
        selectinload(Product.images),
        selectinload(Product.attributeMappings).selectinload(ProductAttributeMapping.attribute)
    ).where(Product.id == productId, Product.deletedAt.is_(None))
    
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.status != "PENDING":
        raise HTTPException(status_code=400, detail="Only products in PENDING status can be approved")

    # Verify brand approval before setting to PUBLISHED
    await validate_brand_approval_for_publish(db, product.brandId, "PUBLISHED")

    product.status = "PUBLISHED"
    await db.commit()
    await db.refresh(product)
    return product


# ── BULK IMPORT PRODUCTS (CSV) ───────────────
@router.post("/bulk-import", response_model=BulkImportResponse, status_code=status.HTTP_201_CREATED)
async def bulk_import_products(
    tenantId: UUID = Form(...),
    storeId: UUID = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    TC-0134: Bulk product import via CSV.
    Validates required fields and reports row-level errors.
    Creates valid rows as PENDING/DRAFT products (pending approval).
    """
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files (.csv) are accepted for bulk product import."
        )

    content = await file.read()
    try:
        decoded = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            decoded = content.decode("latin-1")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid text encoding in CSV file")

    reader = csv.DictReader(io.StringIO(decoded))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV file is empty or missing headers")

    row_index = 0
    created_products: List[Product] = []
    row_errors: List[BulkRowError] = []

    # Get or create default category for tenant if needed
    catRes = await db.execute(select(Category).where(Category.tenantId == tenantId, Category.deletedAt.is_(None)))
    defaultCat = catRes.scalars().first()
    if not defaultCat:
        defaultCat = Category(
            tenantId=tenantId,
            name="Default Category",
            slug="default-category",
            categoryType="PRODUCT",
            createdBy=uuid.uuid4()
        )
        db.add(defaultCat)
        await db.flush()

    for row in reader:
        row_index += 1
        errors = []

        name = (row.get("name") or row.get("product_name") or "").strip()
        slug = (row.get("slug") or row.get("product_slug") or "").strip()
        productType = (row.get("productType") or row.get("product_type") or "PHYSICAL").strip().upper()
        sku = (row.get("sku") or "").strip() or None
        description = (row.get("description") or "").strip() or None
        status_val = (row.get("status") or "DRAFT").strip().upper()

        if not name:
            errors.append("Row missing required field 'name'")
        if not slug:
            errors.append("Row missing required field 'slug'")
        if productType not in {"PHYSICAL", "DIGITAL"}:
            errors.append(f"Invalid productType '{productType}'. Must be PHYSICAL or DIGITAL")
        if status_val not in {"DRAFT", "PENDING", "PUBLISHED", "ARCHIVED", "ACTIVE"}:
            errors.append(f"Invalid status '{status_val}'. Must be DRAFT, PENDING, PUBLISHED, or ARCHIVED")

        if errors:
            row_errors.append(BulkRowError(row=row_index, data=dict(row), errors=errors))
            continue

        # Check for slug uniqueness within tenant and store
        slug_check = await db.execute(
            select(Product).where(
                Product.tenantId == tenantId,
                Product.storeId == storeId,
                Product.slug == slug,
                Product.deletedAt.is_(None)
            )
        )
        if slug_check.scalar_one_or_none():
            row_errors.append(BulkRowError(row=row_index, data=dict(row), errors=[f"Duplicate slug '{slug}' within store"]))
            continue

        product = Product(
            tenantId=tenantId,
            storeId=storeId,
            name=name,
            slug=slug,
            description=description,
            status=status_val,
            productType=productType,
            sku=sku,
            categoryId=defaultCat.id,
            createdBy=uuid.uuid4()
        )
        db.add(product)
        created_products.append(product)

    await db.commit()
    for p in created_products:
        await db.refresh(p)

    return BulkImportResponse(
        totalRows=row_index,
        successfulCount=len(created_products),
        failedCount=len(row_errors),
        createdProducts=created_products,
        rowErrors=row_errors
    )
