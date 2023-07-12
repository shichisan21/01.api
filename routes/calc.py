from fastapi import APIRouter

router = APIRouter()


@router.get("/calc")
def Calc():
    return "a"+"3"
