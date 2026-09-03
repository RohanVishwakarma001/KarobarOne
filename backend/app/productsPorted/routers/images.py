# Owner - pradhansaikat123@gmail.com

# Product Images API endpoints. Supports CRUD, mock upload references,
# and direct file upload validation (file type, size, and plan limit checks).

# Import dropbox library (optional import for local execution)
try:
    import dropbox
    from dropbox.files import WriteMode
    from dropbox.exceptions import ApiError
    HAS_DROPBOX = True
except ImportError:
    dropbox = None
    WriteMode = None
    ApiError = Exception
    HAS_DROPBOX = False

# Import hashlib for checksum calculation of files
import hashlib

# Import uuid module for unique ID generation
import uuid
# Import List and Optional from typing for type hints
from typing import List, Optional
# Import UUID from uuid for database UUID mappings
from uuid import UUID
# Import datetime and timezone from datetime for datetime calculations
from datetime import datetime, timezone

# Import APIRouter, Depends, HTTPException, UploadFile, File, Form, and status from fastapi
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
# Import select and func from sqlalchemy for database queries
from sqlalchemy import select, func
# Import AsyncSession from sqlalchemy.ext.asyncio for async DB sessions
from sqlalchemy.ext.asyncio import AsyncSession

# Import settings instance from app core config
from app.productsPorted.core.config import settings
# Import get_db session dependency injection helper
from app.productsPorted.core.database import get_db
# Import ProductImage, Product, Variant, and MediaFile models
from app.productsPorted.models.models import ProductImage, Product, Variant, MediaFile
# Import schemas from app schemas
from app.productsPorted.schemas.schemas import ProductImageCreate, ProductImageResponse

router = APIRouter(prefix="/images", tags=["Products - Images"])
dbx = dropbox.Dropbox(settings.dropboxAccessToken) if (HAS_DROPBOX and getattr(settings, "dropboxAccessToken", None)) else None


def mapToMediaRole(isPrimary: bool, fileType: Optional[str] = None) -> str:
    allowedRoles = {"PRIMARY_IMAGE", "GALLERY_IMAGE", "LOGO", "HERO_IMAGE", "BANNER", "THUMBNAIL", "DOCUMENT_PREVIEW", "ICON", "OTHER"}
    if fileType in allowedRoles:
        return fileType
    return "PRIMARY_IMAGE" if isPrimary else "GALLERY_IMAGE"


async def uploadToDropbox(file: UploadFile, productId: UUID) -> str:
    if not HAS_DROPBOX or dbx is None:
        return f"https://storage.karobarone.com/products/{productId}/{file.filename or 'image.png'}"
    try:
        contents = await file.read()

        dropboxPath = f"/products/{productId}/{file.filename}"

        dbx.files_upload(
            contents,
            dropboxPath,
            mode=WriteMode.overwrite
        )

        try:
            sharedLink = dbx.sharing_create_shared_link_with_settings(
                dropboxPath
            )
            publicUrl = sharedLink.url

        except ApiError:
            links = dbx.sharing_list_shared_links(path=dropboxPath).links

            if not links:
                raise HTTPException(
                    status_code=500,
                    detail="Unable to create Dropbox shared link."
                )

            publicUrl = links[0].url

        await file.seek(0)

        return publicUrl.replace("?dl=0", "?raw=1")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Dropbox upload failed: {str(e)}"
        )


async def validateVariantBelongsToProduct(db: AsyncSession, productId: UUID, variantId: Optional[UUID]) -> None:
    if variantId is None:
        return
    res = await db.execute(select(Variant).where(Variant.id == variantId, Variant.productId == productId))
    if not res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="variantId does not belong to this product")


async def validateImageLimits(db: AsyncSession, productId: UUID, newFileSize: int, newContentType: str):
    """
    Validates plan limits (max images per product), file size, and file type.
    """
    # 1. Validate File Type
    if newContentType not in settings.allowedImageTypes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{newContentType}'. Allowed types: {settings.allowedImageTypes}"
        )

    # 2. Validate File Size
    if newFileSize > settings.maxImageSizeBytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed limit of {settings.maxImageSizeBytes // (1024 * 1024)}MB."
        )

    # 3. Validate Plan Limit: Max images per product
    res = await db.execute(
        select(func.count(ProductImage.id)).where(ProductImage.productId == productId)
    )
    count = res.scalar() or 0
    if count >= settings.maxImagesPerProduct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan limit exceeded: A product cannot have more than {settings.maxImagesPerProduct} images."
        )


# ── CREATE IMAGE REFERENCE (METADATA) ────────
@router.post("/", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
async def create_image_metadata(payload: ProductImageCreate, db: AsyncSession = Depends(get_db)):
    # Verify product exists
    prodRes = await db.execute(
        select(Product).where(Product.id == payload.productId, Product.deletedAt.is_(None))
    )
    product = prodRes.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Validate limits
    await validateImageLimits(db, payload.productId, payload.fileSize, payload.fileType)
    await validateVariantBelongsToProduct(db, payload.productId, payload.variantId)

    # If isPrimary is True, set all other images of this product to isPrimary=False
    if payload.isPrimary:
        await db.execute(
            ProductImage.__table__.update()
            .where(ProductImage.productId == payload.productId)
            .values(is_primary=False)
        )

    role = mapToMediaRole(payload.isPrimary, payload.fileType)
    if db.bind.dialect.name == "sqlite":
        img = ProductImage(
            productId=payload.productId,
            variantId=payload.variantId,
            url=payload.url,
            altText=payload.altText,
            isPrimary=payload.isPrimary,
            fileSize=payload.fileSize,
            fileType=role
        )
        db.add(img)
    else:
        # PostgreSQL
        mediaFile = MediaFile(
            tenantId=product.tenantId,
            publicUrl=payload.url,
            fileName=payload.url.split("/")[-1] or "image.png",
            originalFileName=payload.url.split("/")[-1] or "image.png",
            fileExtension=payload.fileType.split("/")[-1] if payload.fileType and "/" in payload.fileType else "png",
            mimeType=payload.fileType or "image/png",
            fileSizeBytes=payload.fileSize or 0,
            uploadedBy=uuid.uuid4(),
            isActive=True
        )
        db.add(mediaFile)
        await db.flush()

        img = ProductImage(
            productId=payload.productId,
            variantId=payload.variantId,
            url=str(mediaFile.id),
            altText=payload.altText,
            isPrimary=payload.isPrimary,
            fileSize=payload.fileSize,
            fileType=role,
            tenantId=product.tenantId,
            createdBy=uuid.uuid4(),
            entityType="PRODUCT"
        )
        db.add(img)

    await db.commit()
    await db.refresh(img)
    return img


def validateFileMagicBytes(contents: bytes, filename: Optional[str] = None):
    """
    Inspects raw file header bytes to verify it's a valid image and not an executable/script.
    """
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file content")

    # Reject executable headers
    if contents.startswith(b"MZ") or contents.startswith(b"\x7fELF") or contents.startswith(b"PK\x03\x04\x4d\x5a"):
        raise HTTPException(status_code=400, detail="Executable files are strictly forbidden")

    # Reject HTML/Script headers
    lower_head = contents[:256].lower()
    if b"<script" in lower_head or b"<?php" in lower_head or b"<!doctype" in lower_head or b"<html" in lower_head:
        raise HTTPException(status_code=400, detail="Script and HTML files are forbidden")

    # Allowed magic byte signatures
    is_png = contents.startswith(b"\x89PNG\r\n\x1a\n")
    is_jpeg = contents.startswith(b"\xff\xd8\xff")
    is_gif = contents.startswith(b"GIF87a") or contents.startswith(b"GIF89a")
    is_webp = contents.startswith(b"RIFF") and b"WEBP" in contents[8:16]

    if not (is_png or is_jpeg or is_gif or is_webp):
        raise HTTPException(status_code=400, detail="File content does not match a valid image format (PNG, JPEG, GIF, WEBP)")


# ── FILE UPLOAD API ──────────────────────────
@router.post("/upload", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_product_image(
    productId: UUID = Form(...),
    variantId: Optional[UUID] = Form(None),
    altText: Optional[str] = Form(None),
    isPrimary: bool = Form(False),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Verify product exists
    prodRes = await db.execute(
        select(Product).where(Product.id == productId, Product.deletedAt.is_(None))
    )
    product = prodRes.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await validateVariantBelongsToProduct(db, productId, variantId)

    # Calculate checksum hash and file size
    contents = await file.read()
    checksum = hashlib.md5(contents).hexdigest()
    fileSize = len(contents)
    await file.seek(0)

    # Validate file magic bytes & limits
    validateFileMagicBytes(contents, file.filename)
    await validateImageLimits(db, productId, fileSize, file.content_type)

    # If isPrimary is True, clear other primary flags
    if isPrimary:
        await db.execute(
            ProductImage.__table__.update()
            .where(ProductImage.productId == productId)
            .values(is_primary=False)
        )

    role = mapToMediaRole(isPrimary, file.content_type)
    if db.bind.dialect.name == "sqlite":
        mockSavedUrl = await uploadToDropbox(file, productId)
        img = ProductImage(
            productId=productId,
            variantId=variantId,
            url=mockSavedUrl,
            altText=altText,
            isPrimary=isPrimary,
            fileSize=fileSize,
            fileType=role
        )
        db.add(img)
    else:
        # PostgreSQL: Check if a MediaFile with this checksum already exists for the tenant
        stmtMedia = select(MediaFile).where(
            MediaFile.checksumHash == checksum,
            MediaFile.tenantId == product.tenantId,
            MediaFile.isActive == True
        )
        resMedia = await db.execute(stmtMedia)
        existingMedia = resMedia.scalar_one_or_none()

        if existingMedia:
            mediaFileId = existingMedia.id
        else:
            # Upload to Dropbox
            mockSavedUrl = await uploadToDropbox(file, productId)

            # Create new MediaFile
            mediaFile = MediaFile(
                tenantId=product.tenantId,
                publicUrl=mockSavedUrl,
                fileName=file.filename or "uploaded_image.png",
                originalFileName=file.filename or "uploaded_image.png",
                fileExtension=file.filename.split(".")[-1] if file.filename and "." in file.filename else "png",
                mimeType=file.content_type or "image/png",
                fileSizeBytes=fileSize,
                storageProvider="DROPBOX",
                storagePath=f"/products/{productId}/{file.filename or 'uploaded_image.png'}",
                checksumHash=checksum,
                uploadedBy=uuid.uuid4(),
                isActive=True
            )
            db.add(mediaFile)
            await db.flush()
            mediaFileId = mediaFile.id

        img = ProductImage(
            productId=productId,
            variantId=variantId,
            url=str(mediaFileId),
            altText=altText,
            isPrimary=isPrimary,
            fileSize=fileSize,
            fileType=role,
            tenantId=product.tenantId,
            createdBy=uuid.uuid4(),
            entityType="PRODUCT"
        )
        db.add(img)

    await db.commit()
    await db.refresh(img)
    return img


# ── LIST IMAGES FOR PRODUCT (optionally scoped to one variant) ──
@router.get("/", response_model=List[ProductImageResponse])
async def list_product_images(productId: UUID, variantId: Optional[UUID] = None, db: AsyncSession = Depends(get_db)):
    # Verify product exists
    prodRes = await db.execute(
        select(Product).where(Product.id == productId, Product.deletedAt.is_(None))
    )
    if not prodRes.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")

    stmt = select(ProductImage).where(ProductImage.productId == productId)
    if variantId is not None:
        stmt = stmt.where(ProductImage.variantId == variantId)
    res = await db.execute(stmt)
    return res.scalars().all()


# ── DELETE IMAGE ─────────────────────────────
@router.delete("/{imageId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(imageId: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProductImage).where(ProductImage.id == imageId)
    )
    img = result.scalar_one_or_none()
    if not img:
        raise HTTPException(status_code=404, detail="Image reference not found")

    await db.delete(img)
    await db.commit()
