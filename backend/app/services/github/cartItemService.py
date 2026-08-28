from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.cartItemRepository import cartItemRepository
from app.repositories.github.cartRepository import cartRepository
from app.schemas.github.schemas import CartItemCreate, CartItemUpdate


class CartItemService:

    def calculateLineTotal(
        self,
        quantity: int,
        unitPrice: float,
        discountAmount: float,
        taxAmount: float,
    ):
        return round(
            (quantity * unitPrice) - discountAmount + taxAmount,
            2,
        )

    def recalculateCartTotals(
        self,
        db: Session,
        cartId: UUID,
    ):
        cart = cartRepository.get(
            db,
            cartId,
            cartRepository.model.id,
        )

        if cart is None:
            return

        items = cartItemRepository.getByCart(
            db,
            cartId,
        )

        subtotal = sum(
            float(i.quantity) * float(i.unit_price)
            for i in items
        )

        totalDiscount = sum(
            float(i.discount_amount or 0)
            for i in items
        )

        totalTax = sum(
            float(i.tax_amount or 0)
            for i in items
        )

        cart.subtotal_amount = round(subtotal, 2)
        cart.discount_amount = round(totalDiscount, 2)
        cart.tax_amount = round(totalTax, 2)

        cart.total_amount = round(
            subtotal
            - totalDiscount
            + totalTax
            + float(cart.shipping_amount or 0),
            2,
        )

        db.commit()

    def create(
        self,
        db: Session,
        cartItem: CartItemCreate,
    ):
        cart = cartRepository.get(
            db,
            cartItem.cart_id,
            cartRepository.model.id,
        )

        if cart is None:
            return None

        from app.db.models.github.models import CartItem

        data = cartItem.model_dump(mode="json")

        if not data.get("product_variant_id"):
            data["product_variant_id"] = data.get("product_id")

        data["line_total"] = self.calculateLineTotal(
            data["quantity"],
            data["unit_price"],
            data.get("discount_amount") or 0,
            data.get("tax_amount") or 0,
        )

        db_obj = CartItem(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        item = db_obj

        self.recalculateCartTotals(
            db,
            cartItem.cart_id,
        )

        return item

    def getAllByCart(
        self,
        db: Session,
        cartId: UUID,
    ):
        return cartItemRepository.getByCart(
            db,
            cartId,
        )

    def getById(
        self,
        db: Session,
        cartItemId: UUID,
    ):
        return cartItemRepository.get(
            db,
            cartItemId,
            cartItemRepository.model.id,
        )

    def update(
        self,
        db: Session,
        cartItemId: UUID,
        cartItem: CartItemUpdate,
    ):
        dbItem = self.getById(
            db,
            cartItemId,
        )

        if dbItem is None:
            return None

        updated = cartItemRepository.update(
            db,
            dbItem,
            cartItem,
        )

        updated.line_total = self.calculateLineTotal(
            updated.quantity,
            float(updated.unit_price),
            float(updated.discount_amount or 0),
            float(updated.tax_amount or 0),
        )

        db.commit()
        db.refresh(updated)

        self.recalculateCartTotals(
            db,
            updated.cart_id,
        )

        return updated

    def delete(
        self,
        db: Session,
        cartItemId: UUID,
    ):
        dbItem = self.getById(
            db,
            cartItemId,
        )

        if dbItem is None:
            return False

        cartId = dbItem.cart_id

        cartItemRepository.delete(
            db,
            dbItem,
        )

        self.recalculateCartTotals(
            db,
            cartId,
        )

        return True


cartItemService = CartItemService()