# Owner: shlokpallav@gmail.com
"""
===============================================================================
PRODUCT REPOSITORY
===============================================================================

Handles all database operations related to Products.

Responsibilities:
- CRUD operations
- Fetch active products
- Fetch product using SKU prefix

Business logic should NOT be written here.
Only database queries should exist in this file.
===============================================================================
"""

from sqlalchemy.orm import Session

from app.db.models.github.product import Product
from app.repositories.github.base import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def __init__(self):
        super().__init__(Product)

    # -------------------------------------------------------------------------
    # Returns product by SKU Prefix
    # -------------------------------------------------------------------------
    def getBySkuPrefix(
        self,
        db: Session,
        skuPrefix: str,
    ):
        return (
            db.query(Product)
            .filter(Product.sku_prefix == skuPrefix)
            .first()
        )

    # -------------------------------------------------------------------------
    # Returns all ACTIVE products
    # -------------------------------------------------------------------------
    def getActiveProducts(
        self,
        db: Session,
    ):
        return (
            db.query(Product)
            .filter(Product.status == "ACTIVE")
            .all()
        )


productRepository = ProductRepository()