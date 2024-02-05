from fastapi import APIRouter

from src.models import create_test_data

router = APIRouter()

@router.post('/createdata')
async def create_data() -> None:
    await create_test_data()
