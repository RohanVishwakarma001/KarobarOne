from app.db.models.github.user import User
from app.repositories.github.base import BaseRepository


class UserRepository(
    BaseRepository[User]
):

    def __init__(self):
        super().__init__(User)


userRepository = UserRepository()