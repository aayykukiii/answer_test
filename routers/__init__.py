from routers.books import router as books_router
from routers.users import router as users_router 
from fastapi import APIRouter


router = APIRouter()

router.include_router(books_router)
router.include_router(users_router)