from typing import Generic, Type, TypeVar, Optional, List

from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(
        self,
        db: Session,
        obj: BaseModel
    ) -> ModelType:

        db_obj = self.model(
    **obj.model_dump(mode="json")
)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get(
        self,
        db: Session,
        obj_id,
        id_field
    ) -> Optional[ModelType]:

        return (
            db.query(self.model)
            .filter(id_field == obj_id)
            .first()
        )

    def get_all(
        self,
        db: Session
    ) -> List[ModelType]:

        return db.query(self.model).all()

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj: BaseModel
    ) -> ModelType:

        update_data = obj.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    def delete(
        self,
        db: Session,
        db_obj: ModelType
    ) -> None:

        db.delete(db_obj)
        db.commit()