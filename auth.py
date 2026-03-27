# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.ext.asyncio import AsyncSession
# from database.models import User
# from database.db import get_db
# from sqlalchemy.future import select

# # Настройка bcrypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # JWT настройки
# SECRET_KEY = "your_secret_key_here"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# # Хэширование пароля с обрезкой до 72 байт
# def hash_password(password: str) -> str:
#     truncated = password[:72]  # bcrypt ограничение
#     return pwd_context.hash(truncated)

# def verify_password(password: str, hashed: str) -> bool:
#     truncated = password[:72]
#     return pwd_context.verify(truncated, hashed)

# # Создание токена
# def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=expires_delta)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Получение текущего пользователя
# async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     result = await db.execute(select(User).where(User.username == username))
#     user = result.scalar_one_or_none()
#     if user is None:
#         raise credentials_exception
#     return user