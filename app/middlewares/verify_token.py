
from fastapi import HTTPException

from app.core.jwt import get_jwks, verify_jwt


def get_token(header: str) -> str:
    match header.split(" "):
        case ["Bearer", token]:
            return token

    raise ValueError("Invalid token")

async def verify_token(access_token: str):
    try:
        token = get_token(access_token)
        if not verify_jwt(token, get_jwks()):
            raise 
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )