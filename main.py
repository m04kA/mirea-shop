from fastapi.middleware.cors import CORSMiddleware
#from orders.router import router as routerOrder
from src.pages.contactInfoPage import router as routerContact
from src.pages.shawarmaPage import router as routerShawarma
from src.pages.snacksPage import router as routerSnacks
from src.pages.router import router as routerMainPage
from src.pages.profilePage import router as routerProfilePage
from src.pages.checkoutPage import router as routerCheckoutPage
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Depends
from fastapi_users import fastapi_users, FastAPIUsers

from auth.auth import auth_backend
from auth.database import User
from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.userManager import get_user_manager

app = FastAPI(
    title='shawarma'
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(routerMainPage)
#app.include_router(routerOrder)
app.include_router(routerContact)
app.include_router(routerShawarma)
app.include_router(routerProfilePage)
app.include_router(routerCheckoutPage)
app.include_router(routerSnacks)

app.mount("/static", StaticFiles(directory="src/static"), name = "static")
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

@app.get("/")
async def root():
    return RedirectResponse("/pages/base")
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"

