from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.items.router import router as items_router
from src.items.ingredients.router import router as ingredients_router

app = FastAPI(
    title='shawarma'
)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

app.include_router(items_router)
app.include_router(ingredients_router)

