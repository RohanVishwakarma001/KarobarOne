# Owner: mousamdas156@gmail.com
"""
SQLAlchemy database model for role.
Defines the database schema, table columns, constraints, and relationships for role.
"""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelWithUpdate


# --------------------------------------------------------------------------------
# Role Model
# Defines role records (global or optionally tenant-scoped via mapping table).
# Uses 'BaseModelWithUpdate' to automatically include 'createdAt' and 'updatedAt'.
# Python attribute names are camelCase; DB column names stay snake_case.
# --------------------------------------------------------------------------------
class Role(BaseModelWithUpdate):
    __tablename__ = "roles"

    # roleName: User-friendly display name (e.g. 'Store Manager')
    roleName: Mapped[str] = mapped_column(
        "role_name",
        String(100),
        nullable=False,
    )

    # roleCode: Unique system code for the role (e.g. 'STORE_MANAGER')
    roleCode: Mapped[str] = mapped_column(
        "role_code",
        String(50),
        unique=True,
        nullable=False,
    )

    # description: Optional explanation of the role's purpose/scope
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # isSystemRole: True for built-in roles that cannot be deleted/edited freely
    isSystemRole: Mapped[bool] = mapped_column(
        "is_system_role",
        Boolean,
        default=False,
        nullable=False,
    )

    # permissionMappings: Permissions granted to this role
    permissionMappings = relationship(
        "RolePermissionMapping",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    # userMappings: Users assigned to this role
    userMappings = relationship(
        "UserRoleMapping",
        back_populates="role",
        foreign_keys="UserRoleMapping.roleId",
        cascade="all, delete-orphan",
    )
