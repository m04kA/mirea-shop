from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/checkout")
def get_base_page(request: Request):
    return templates.TemplateResponse("pages/checkout.html", {"request": request})