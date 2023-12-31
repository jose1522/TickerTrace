from fastapi import APIRouter

from .healthcheck import router as healthcheck_router
from .price import router as price_router
from .ticker import router as ticker_router

router = APIRouter(prefix="/v1")
router.include_router(healthcheck_router)
router.include_router(ticker_router)
router.include_router(price_router)
