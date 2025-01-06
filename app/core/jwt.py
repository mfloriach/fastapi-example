
from functools import cache
from typing import Dict, List, Optional

import requests
from jose import jwk, jwt
from jose.utils import base64url_decode

from app.core.config import env_vars

JWK = Dict[str, str]
JWKS = Dict[str, List[JWK]]

@cache
def get_jwks() -> JWKS:
    return requests.get(env_vars.JWKS_URL).json()


def get_hmac_key(token: str, jwks: JWKS) -> Optional[JWK]:
    
    kid = jwt.get_unverified_header(token).get("kid")
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
        
def verify_jwt(token: str, jwks: JWKS) -> bool:
    hmac_key = get_hmac_key(token, jwks)

    if not hmac_key:
        raise ValueError("No pubic key found!")

    hmac_key = jwk.construct(get_hmac_key(token, jwks))

    message, encoded_signature = token.rsplit(".", 1)
    decoded_signature = base64url_decode(encoded_signature.encode())

    return hmac_key.verify(message.encode(), decoded_signature)
