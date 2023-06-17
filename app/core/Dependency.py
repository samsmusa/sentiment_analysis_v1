from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from authlib.jose import jwt, JoseError
from passlib.context import CryptContext
from pydantic import BaseModel

import time

from authlib.jose import jwt
from authlib.jose.errors import ExpiredTokenError, InvalidTokenError, KeyMismatchError

from app.core.config import settings

auth_scheme = HTTPBearer()
pwd_context = CryptContext(schemes=[settings.CRYPTO_SCHEMA], deprecated="auto")


class Token(BaseModel):
    token: str


def auth_exception(details='', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY):
    return HTTPException(
        status_code=status_code,
        detail=details,
        headers={"WWW-Authenticate": settings.TOKEN_HEADER},
    )


async def get_current_user(token: Token = Depends(auth_scheme)):
    try:
        print(token.token)
        options = {'verify_aud': False, 'require_sub': True}
        payload = parse_token(
            token.token,
            settings.KEYCLOAK_PUBLIC.replace(b"\\n", b"\n"),
            options=options
        )
        yid: str = payload.get("sid", None)
        if yid is None:
            raise auth_exception(details='Yid not found!', status_code=status.HTTP_404_NOT_FOUND)
    except ExpiredTokenError as ex_token:
        raise auth_exception(ex_token.description, status_code=status.HTTP_403_FORBIDDEN)
    except InvalidTokenError as invalid_error:
        raise auth_exception(details=invalid_error.description, status_code=status.HTTP_403_FORBIDDEN)
    except JoseError as je:
        raise auth_exception(je.description, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return payload


def parse_token(token, public_key, **kwargs):
    claims = jwt.decode(token, public_key, **kwargs)
    claims.validate()
    return claims
