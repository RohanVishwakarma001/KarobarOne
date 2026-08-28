# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for permission.
Defines the database schema, table columns, constraints, and relationships for permission.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated as BaseModel


# --------------------------------------------------------------------------------
# Permission Model
# Represents a granular access control unit (e.g. 'CAN_EDIT_PRODUCTS').
# Uses 'BaseModel' to automatically include a 'createdAt' timestamp.
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class Permission(BaseModel):
    __tablename__ = "permissions"

    # permissionName: User-friendly display name (e.g. 'Edit Products')
    permissionName: Mapped[str] = mapped_column(
        "permission_name",
        String(150),
        unique=True,
        nullable=False,
    )

    # permissionCode: Unique code used to check authorization programmatically
    permissionCode: Mapped[str] = mapped_column(
        "permission_code",
        String(100),
        unique=True,
        nullable=False,
    )

    # description: Optional explanation of what this permission allows
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # roleMappings: Roles that have been granted this permission
    roleMappings = relationship(
        "RolePermissionMapping",
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    # storeStaffMappings: Store staff overrides that have been granted this permission
    storeStaffMappings = relationship(
        "StoreStaffPermission",
        back_populates="permission",
        cascade="all, delete-orphan",
    )
