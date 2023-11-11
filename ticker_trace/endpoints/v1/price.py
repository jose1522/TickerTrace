import datetime
from typing import List, Annotated

from fastapi import APIRouter, Depends, Header, BackgroundTasks

from models import get_session
from schemas.price import PriceCreate, PriceRecord
from stores.price import PriceDBTransaction
from tasks.price import update_price

router = APIRouter(prefix="/price", tags=["Price"])


@router.post("/refresh", status_code=201)
async def pull_ticker_prices(
    data: PriceCreate,
    background_tasks: BackgroundTasks,
    api_key: Annotated[str | None, Header(description="Alpha Vantage API key")] = None,
    background: Annotated[bool, Header(description="Run in background")] = False,
    session=Depends(get_session),
):
    if background:
        background_tasks.add_task(
            update_price, api_key=api_key, symbol=data.symbol, session=session
        )
        return {"message": "Task added to the queue"}
    else:
        await update_price(api_key=api_key, symbol=data.symbol, session=session)
        return {"message": "Task completed"}


@router.get("/", status_code=200, response_model=List[PriceRecord])
async def get_ticker_prices(
    symbol: str,
    start_date: datetime.date = None,
    end_date: datetime.date = None,
    page: int = None,
    page_size: int = None,
    session=Depends(get_session),
):
    with PriceDBTransaction(session=session) as storage:
        response = storage.get_by_symbol(
            symbol=symbol,
            page=page,
            page_size=page_size,
            start_date=start_date,
            end_date=end_date,
        )
    return response
