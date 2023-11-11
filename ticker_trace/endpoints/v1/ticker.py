from typing import List, Optional, Annotated

from fastapi import APIRouter, Depends, BackgroundTasks, Header

from models import get_session
from schemas.ticker import TickerCreate, TickerUpdate
from stores.ticker import TickerDBTransaction
from tasks.price import update_price

router = APIRouter(prefix="/ticker", tags=["Ticker"])


@router.post("/", status_code=201, response_model=TickerUpdate)
def add_new_ticker(
    data: TickerCreate,
    background_tasks: BackgroundTasks,
    session=Depends(get_session),
    api_key: Annotated[str | None, Header(description="Alpha Vantage API key")] = None,
):
    with TickerDBTransaction(session) as ticker:
        obj = ticker.new_object(data)
        ticker.add(obj)
    background_tasks.add_task(
        update_price, api_key=api_key, symbol=data.symbol, session=session
    )
    return obj


@router.get("/{ticker_id}", response_model=TickerUpdate)
def get_ticker(ticker_id: int, session=Depends(get_session)):
    with TickerDBTransaction(session) as ticker:
        obj = ticker.get(ticker_id)
    return obj


@router.get("/", response_model=List[TickerUpdate])
def get_all_tickers(
    symbol: Optional[str] = None,
    name: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    session=Depends(get_session),
):
    query = {}
    if symbol:
        query["symbol"] = symbol
    if name:
        query["name"] = name
    with TickerDBTransaction(session) as ticker:
        if query:
            objs = ticker.query(page=page, page_size=page_size, **query)
        else:
            objs = ticker.get_all(page=page, page_size=page_size)
    return objs


@router.put("/{ticker_id}", response_model=TickerUpdate)
def update_ticker(ticker_id: int, data: TickerCreate, session=Depends(get_session)):
    with TickerDBTransaction(session) as ticker:
        return ticker.update(ticker_id, data)
