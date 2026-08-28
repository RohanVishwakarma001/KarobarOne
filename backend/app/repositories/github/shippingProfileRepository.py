from sqlalchemy.orm import Session

from app.db.models.github.shippingProfile import ShippingProfile
from app.repositories.github.base import BaseRepository


class ShippingProfileRepository(BaseRepository):

    def __init__(self):
        super().__init__(ShippingProfile)

    def getByProfileName(
        self,
        db: Session,
        profileName: str
    ):
        return (
            db.query(ShippingProfile)
            .filter(
                ShippingProfile.profile_name == profileName
            )
            .first()
        )


shippingProfileRepository = ShippingProfileRepository()