# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: core/securityChat.py — Chat Module Security (Password Hashing & JWT)
# ================================================================================
# Why this file is used:
#   - It manages separate security helpers (JWT + hashing) for independent chat users.
#
# What components are inside:
#   - pwd_context        -> CryptContext instance using bcrypt algorithm rules.
#   - hash_password()    -> Generates password hashes.
#   - verify_password()  -> Verifies plaintext passwords against stored hashes.
#   - create_access_token() -> Creates signed access tokens.
#   - decode_token()     -> Extracts claims from tokens.
# ================================================================================
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import getSettings
# getSettings().jwtSecretKey, getSettings().jwtAlgorithm, getSettings().accessTokenExpireMinutes

# Passlib ka bcrypt context — password hash aur verify ke liye
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Plain password ko bcrypt hash mein convert karo
    # Database mein kabhi plain password store nahi hoga
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    # Login ke waqt user ka password entered vs stored hash compare karo
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    # JWT token banao — user_id aur role encode hoga andar
    payload = data.copy()

    # Token ki expiry time set karo
    expire = datetime.now(timezone.utc) + timedelta(minutes=getSettings().accessTokenExpireMinutes)
    payload.update({"exp": expire})

    # Secret key se sign karke token return karo
    return jwt.encode(payload, getSettings().jwtSecretKey, algorithm=getSettings().jwtAlgorithm)

def decode_token(token: str) -> dict:
    # Token verify karo aur andar ka data nikalo
    # Agar token invalid ya expired hai to JWTError raise hoga
    return jwt.decode(token, getSettings().jwtSecretKey, algorithms=[getSettings().jwtAlgorithm])