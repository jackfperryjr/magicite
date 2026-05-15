import jwt
import requests
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from functools import lru_cache
from jwt.algorithms import ECAlgorithm, OKPAlgorithm, RSAAlgorithm

from api.config import settings

_bearer = HTTPBearer()


@lru_cache(maxsize=1)
def _get_jwks() -> dict:
    res = requests.get(
        f"{settings.supabase_url}/auth/v1/.well-known/jwks.json",
        timeout=10,
    )
    res.raise_for_status()
    return res.json()


_EC_ALG = {"P-256": "ES256", "P-384": "ES384", "P-521": "ES512"}


def _public_key_for(kid: str) -> tuple:
    for key in _get_jwks().get("keys", []):
        if key.get("kid") == kid:
            kty = key.get("kty")
            if kty == "RSA":
                return RSAAlgorithm.from_jwk(key), "RS256"
            elif kty == "EC":
                alg = _EC_ALG.get(key.get("crv", "P-256"), "ES256")
                return ECAlgorithm.from_jwk(key), alg
            elif kty == "OKP":
                return OKPAlgorithm.from_jwk(key), "EdDSA"
            else:
                raise HTTPException(status_code=401, detail=f"Unsupported key type: {kty}")
    raise HTTPException(status_code=401, detail=f"Key '{kid}' not found in JWKS")


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(_bearer)) -> str:
    token = credentials.credentials
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")

        if kid:
            key, algorithm = _public_key_for(kid)
            payload = jwt.decode(token, key, algorithms=[algorithm], audience="authenticated")
        else:
            payload = jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=["HS256"],
                audience="authenticated",
            )

        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
