# Owner - pradhansaikat123@gmail.com

# SQLAlchemy database models mapped to the existing database schema in PostgreSQL.
# Aligns categories, brands, brand_approvals, products, product_variants, etc.

# Import uuid module for generating unique identifiers
import uuid
# Import json module for serializing/deserializing dictionary types in JSON fields
import json
# Import Column, String, Boolean, Integer, BigInteger, Float, Text, ForeignKey, CheckConstraint, UniqueConstraint, JSON, TypeDecorator from sqlalchemy
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    BigInteger,
    Float,
    Text,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    JSON,
    TypeDecorator
)
# Import UUID, TIMESTAMP types from sqlalchemy.types
from sqlalchemy.types import UUID, TIMESTAMP
# Import func to use sql function helpers from sqlalchemy.sql
from sqlalchemy.sql import func
# Import relationship and synonym helpers from sqlalchemy.orm
from sqlalchemy.orm import relationship, synonym
# Import hybrid_property from sqlalchemy.ext.hybrid for model-defined hybrid columns
from sqlalchemy.ext.hybrid import hybrid_property

# Import the Base declarative base class from our database configuration
from app.productsPorted.core.database import Base


# Custom TypeDecorator to store dict attributes inside a string column for product_variants
class JSONAsString(TypeDecorator):
    impl = String(1000)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return "{}"

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                return json.loads(value)
            except Exception:
                return {}
        return {}


class DialectUUIDOrString(TypeDecorator):
    impl = String(255)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(255))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            if isinstance(value, str):
                return uuid.UUID(value)
            return value
        else:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return value


# Custom TypeDecorator to translate between PHYSICAL/DIGITAL strings and database integer IDs
class ProductTypeInteger(TypeDecorator):
    impl = Integer
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value == "PHYSICAL":
            return 1
        elif value == "DIGITAL":
            return 2
        return value

    def process_result_value(self, value, dialect):
        if value == 1:
            return "PHYSICAL"
        elif value == 2:
            return "DIGITAL"
        return "PHYSICAL"



# ─────────────────────────────────────────────
# 1. Categories
# ─────────────────────────────────────────────
class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("tenant_id", "parent_category_id", "category_name", name="uq_category_tenant_parent_name_pg"),
        UniqueConstraint("tenant_id", "category_slug", name="uq_category_tenant_slug_pg"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    storeId = Column("store_id", UUID(as_uuid=True), nullable=True)
    name = Column("category_name", String(100), nullable=False)
    slug = Column("category_slug", String(100), nullable=False)
    parentId = Column("parent_category_id", UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    categoryType = Column("category_type", String(50), default="PRODUCT", nullable=False)
    createdBy = Column("created_by", UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deletedAt = Column("deleted_at", TIMESTAMP, nullable=True)

    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="category")


# ─────────────────────────────────────────────
# 2. Shipping Profiles
# ─────────────────────────────────────────────
class ShippingProfile(Base):
    __tablename__ = "shipping_profiles"
    __table_args__ = (
        UniqueConstraint("tenant_id", "profile_name", name="uq_shipping_profile_tenant_name_pg"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    name = Column("profile_name", String(100), nullable=False)
    deliveryEstimate = Column("description", String(100), nullable=False)
    charges = Column("free_shipping_threshold", Float, nullable=False, default=0.0)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())
    isActive = Column("is_active", Boolean, default=True, nullable=False)

    products = relationship("Product", back_populates="shippingProfile")


# ─────────────────────────────────────────────
# 3. Brands
# ─────────────────────────────────────────────
class Brand(Base):
    __tablename__ = "brands"
    __table_args__ = (
        UniqueConstraint("tenant_id", "brand_name", name="uq_brand_tenant_name_pg"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    name = Column("brand_name", String(100), nullable=False)
    ownerStoreId = Column("owner_store_id", UUID(as_uuid=True), nullable=True)
    logoUrl = Column("brand_slug", String(255), nullable=True)  # Mapped logoUrl to brand_slug string
    isApproved = Column("is_active", Boolean, default=False, nullable=False)  # Mapped isApproved to is_active
    createdBy = Column("created_by", UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    approvedBy = Column("approved_by", UUID(as_uuid=True), nullable=True)
    approvedAt = Column("approved_at", TIMESTAMP, nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deletedAt = Column("deleted_at", TIMESTAMP, nullable=True)

    products = relationship("Product", back_populates="brand")
    approvalRequests = relationship("BrandApprovalRequest", back_populates="brand", cascade="all, delete-orphan")


# ─────────────────────────────────────────────
# 4. Brand Approval Requests (Mapped to brand_approvals)
# ─────────────────────────────────────────────
class BrandApprovalRequest(Base):
    __tablename__ = "brand_approvals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brandId = Column("brand_id", UUID(as_uuid=True), ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    requestedBy = Column("requesting_store_id", UUID(as_uuid=True), nullable=False)
    brandOwnerStoreId = Column("brand_owner_store_id", UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    status = Column("request_status", String(20), default="PENDING", nullable=False)  # PENDING, APPROVED, REJECTED
    rejectionReason = Column("rejection_reason", Text, nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())

    brand = relationship("Brand", back_populates="approvalRequests")


# ─────────────────────────────────────────────
# 4b. Brand Approval Audit Logs
# ─────────────────────────────────────────────
class BrandApprovalAuditLog(Base):
    __tablename__ = "brand_approval_audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brandId = Column("brand_id", UUID(as_uuid=True), ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    requestId = Column("request_id", UUID(as_uuid=True), ForeignKey("brand_approvals.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(30), nullable=False)  # SUBMIT, APPROVE, REJECT
    performedBy = Column("performed_by", UUID(as_uuid=True), nullable=False)
    notes = Column(Text, nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())


# ─────────────────────────────────────────────
# 5. Products
# ─────────────────────────────────────────────
class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("tenant_id", "store_id", "sku_prefix", name="uq_product_tenant_store_sku_pg"),
        UniqueConstraint("tenant_id", "store_id", "product_slug", name="uq_product_tenant_store_slug_pg"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    storeId = Column("store_id", UUID(as_uuid=True), nullable=False)
    name = Column("product_name", String(255), nullable=False)
    slug = Column("product_slug", String(255), nullable=False)
    description = Column("long_description", Text, nullable=True)
    status = Column(String(20), default="DRAFT", nullable=False)
    productType = Column("product_type_id", ProductTypeInteger, default="PHYSICAL", nullable=False)  # Mapped productType to product_type_id (1=PHYSICAL, 2=DIGITAL)
    sku = Column("sku_prefix", String(100), nullable=False)  # Mapped sku to sku_prefix
    metaTitle = Column("short_description", String(255), nullable=True)  # Mapped metaTitle to short_description
    metaDescription = synonym("description")
    categoryId = Column("category_id", UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=False)
    brandId = Column("brand_id", UUID(as_uuid=True), ForeignKey("brands.id", ondelete="SET NULL"), nullable=True)
    shippingProfileId = Column("published_version_id", UUID(as_uuid=True), ForeignKey("shipping_profiles.id", ondelete="SET NULL"), nullable=True)  # Mapped shippingProfileId to published_version_id
    createdBy = Column("created_by", UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deletedAt = Column("deleted_at", TIMESTAMP, nullable=True)

    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    shippingProfile = relationship("ShippingProfile", back_populates="products")
    variants = relationship("Variant", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    attributeMappings = relationship(
        "ProductAttributeMapping",
        secondary="product_attributes",
        primaryjoin="Product.id == Attribute.productId",
        secondaryjoin="Attribute.id == ProductAttributeMapping.attributeId",
        viewonly=True
    )


# ─────────────────────────────────────────────
# 6. Variants (Mapped to product_variants)
# ─────────────────────────────────────────────
class Variant(Base):
    __tablename__ = "product_variants"
    __table_args__ = (
        UniqueConstraint("product_id", "variant_sku", name="uq_variant_product_sku_pg"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    productId = Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    sku = Column("variant_sku", String(100), nullable=False)
    price = Column(Float, nullable=False)
    inventory = Column("mrp", Integer, nullable=False, default=0)  # Map inventory to mrp column
    attributes = Column("variant_name", JSONAsString, nullable=True)  # Serialized JSON attributes stored in variant_name
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="variants")


# ─────────────────────────────────────────────
# 7. Attributes (Mapped to product_attributes)
# ─────────────────────────────────────────────
class Attribute(Base):
    __tablename__ = "product_attributes"
    __table_args__ = (
        UniqueConstraint("product_id", "attribute_code", name="uq_attribute_tenant_code_pg"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    productId = Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    name = Column("attribute_name", String(100), nullable=False)
    code = Column("attribute_code", String(100), nullable=False)
    type = Column("unit_type", String(50), nullable=False, default="text")  # Map type to unit_type
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())

    product = relationship("Product", foreign_keys=[productId], lazy="selectin")
    productMappings = relationship("ProductAttributeMapping", back_populates="attribute", cascade="all, delete-orphan")

    @property
    def tenantId(self):
        if self.product:
            return self.product.tenantId
        if hasattr(self, "_tenantId"):
            return self._tenantId
        return self.productId

    @tenantId.setter
    def tenantId(self, value):
        self._tenantId = value


# ─────────────────────────────────────────────
# 8. Product Attribute Mapping (Mapped to product_attribute_values)
# ─────────────────────────────────────────────
class ProductAttributeMapping(Base):
    __tablename__ = "product_attribute_values"
    __table_args__ = (
        UniqueConstraint("attribute_id", "value", name="uq_product_attribute_mapping_pg"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attributeId = Column("attribute_id", UUID(as_uuid=True), ForeignKey("product_attributes.id", ondelete="CASCADE"), nullable=False)
    value = Column(String(255), nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())

    attribute = relationship("Attribute", back_populates="productMappings", lazy="selectin")

    @property
    def productId(self):
        if hasattr(self, "_productId"):
            return self._productId
        return self.attribute.productId if self.attribute else None

    @productId.setter
    def productId(self, value):
        self._productId = value


# ─────────────────────────────────────────────
# 9. Product Images (Mapped to entity_media)
# ─────────────────────────────────────────────
class ProductImage(Base):
    __tablename__ = "entity_media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    productId = Column("entity_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    mediaFileId = Column("media_file_id", DialectUUIDOrString, nullable=False)
    altText = Column("alt_text_override", String(255), nullable=True)
    isPrimary = Column("is_primary", Boolean, default=False, nullable=False)
    sortOrder = Column("sort_order", Integer, nullable=False, default=0)

    @hybrid_property
    def fileSize(self):
        return self.sortOrder

    @fileSize.setter
    def fileSize(self, value):
        self.sortOrder = min(value, 32767) if value is not None else 0
    fileType = Column("media_role", String(100), nullable=False, default="image/png")  # Map fileType to media_role
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=True)
    createdBy = Column("created_by", UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    entityType = Column("entity_type", String(50), default="PRODUCT", nullable=True)
    mediaRole = synonym("fileType")
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="images")
    mediaFile = relationship("MediaFile", foreign_keys=[mediaFileId], primaryjoin="MediaFile.id == foreign(ProductImage.mediaFileId)", uselist=False, lazy="selectin")

    @property
    def url(self):
        if self.mediaFile:
            return self.mediaFile.publicUrl
        return self.mediaFileId

    @url.setter
    def url(self, value):
        self.mediaFileId = value


# ─────────────────────────────────────────────
# 10. Media Files
# ─────────────────────────────────────────────
class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    publicUrl = Column("public_url", String(255), nullable=False)
    fileName = Column("file_name", String(255), nullable=False)
    originalFileName = Column("original_file_name", String(255), nullable=False)
    fileExtension = Column("file_extension", String(50), nullable=False, default="png")
    mimeType = Column("mime_type", String(100), nullable=False, default="image/png")
    fileSizeBytes = Column("file_size_bytes", BigInteger, nullable=False, default=0)
    storageProvider = Column("storage_provider", String(100), nullable=False, default="LOCAL")
    storagePath = Column("storage_path", String(255), nullable=False, default="/uploads")
    checksumHash = Column("checksum_hash", String(255), nullable=False, default="d41d8cd98f00b204e9800998ecf8427e")
    approvalStatus = Column("approval_status", String(50), nullable=False, default="PENDING")
    uploadedBy = Column("uploaded_by", UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    isActive = Column("is_active", Boolean, default=True, nullable=False)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())
