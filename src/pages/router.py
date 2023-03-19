from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from orders.router import get_specific_orders

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})