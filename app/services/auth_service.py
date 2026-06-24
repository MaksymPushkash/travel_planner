from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)

    async def register(self, data: UserCreate) -> User:
        existing_user = await self.users.get_by_email(data.email)

        if existing_user:
            raise UserAlreadyExistsError()

        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
        )

        user = await self.users.create(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user


    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.users.get_by_email(data.email)

        if not user or not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError()

        access_token = create_access_token(subject=str(user.id))

        return TokenResponse(access_token=access_token)


