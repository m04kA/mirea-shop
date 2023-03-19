from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/profile")
def get_base_page(request: Request):
    return templates.TemplateResponse("pages/profile.html", {"request": request})