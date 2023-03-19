from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from config import SECRET_KEY_TOKEN

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)

secret_key = SECRET_KEY_TOKEN


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=secret_key, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
