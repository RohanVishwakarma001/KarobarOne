from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.models.github.user import User
from app.schemas.github.userSchema import UserCreate, UserLogin

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class AuthService:

    def hashPassword(self, password: str):
        return pwd_context.hash(password)

    def verifyPassword(self, plain: str, hashed: str):
        return pwd_context.verify(plain, hashed)

    def register(
        self,
        db: Session,
        user: UserCreate
    ):

        existing = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing:
            return None

        dbUser = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            mobile=user.mobile,
            whatsapp_mobile=user.whatsapp_mobile,
            password_hash=self.hashPassword(
                user.password
            ),
            is_active=True,
            is_email_verified=False,
            is_mobile_verified=False,
        )

        db.add(dbUser)
        db.commit()
        db.refresh(dbUser)

        return dbUser

    def login(
        self,
        db: Session,
        user: UserLogin
    ):

        dbUser = db.query(User).filter(
            User.email == user.email
        ).first()

        if dbUser is None:
            return None

        if not self.verifyPassword(
            user.password,
            dbUser.password_hash
        ):
            return False

        return dbUser


authService = AuthService()