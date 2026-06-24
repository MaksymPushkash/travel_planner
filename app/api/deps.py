from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidCredentialsError
from app.core.security import decode_access_token
from app.database.session import AsyncSessionLocal
from app.models.user import User
from app.repositories.user_repo import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    
    user_id = decode_access_token(token)

    if user_id is None:
        raise InvalidCredentialsError()

    user = await UserRepository(db).get_by_id(int(user_id))

    if user is None:
        raise InvalidCredentialsError()

    return user

