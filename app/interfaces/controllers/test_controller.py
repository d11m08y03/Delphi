from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Root"])
async def hello_world():
    return {"message": "Hello, World!"}
