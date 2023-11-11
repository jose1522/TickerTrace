from typing import List, Annotated

from fastapi import APIRouter, Depends, Header

from clients.alpha_vantage import AlphaVantage
from models import get_session
from schemas.price import APIPrices, PriceCreate, PriceRecord
from stores.price import PriceDBTransaction

router = APIRouter(prefix="/price", tags=["Price"])


@router.post("/", status_code=201)
async def pull_ticker_prices(
    data: PriceCreate,
    api_key: Annotated[str | None, Header(description="Alpha Vantage API key")] = None,
    session=Depends(get_session),
):
    api = AlphaVantage(api_key=api_key)
    response = await api.get_daily_prices(symbol=data.symbol)
    response = APIPrices(records=response).model_dump()
    with PriceDBTransaction(session=session) as storage:
        storage.bulk_insert(response["records"], symbol=data.symbol)


@router.get("/", status_code=200, response_model=List[PriceRecord])
async def get_ticker_prices(
    symbol: str, page: int = None, page_size: int = None, session=Depends(get_session)
):
    with PriceDBTransaction(session=session) as storage:
        response = storage.get_by_symbol(symbol=symbol, page=page, page_size=page_size)
    return response
