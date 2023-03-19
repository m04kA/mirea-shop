from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orders.router import router as routerOrder
from src.pages.router import router as routerMainPage
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Shawarma"
)

app.include_router(routerMainPage)
app.include_router(routerOrder)

app.mount("/static", StaticFiles(directory="src/static"), name = "static")
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.get("/")
async def root():
    return RedirectResponse("/pages/base")


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
