from fastapi import APIRouter

router = APIRouter()

@router.get("/test", tags=["Root"])
async def hello_world():
    return {"message": "Hello, World!"}
