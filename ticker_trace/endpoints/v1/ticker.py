from typing import List, Optional

from fastapi import APIRouter, Depends

from models import get_session
from schemas.ticker import TickerCreate, TickerUpdate
from stores.ticker import TickerDBTransaction

router = APIRouter(prefix="/ticker")


@router.post("/", status_code=201, response_model=TickerUpdate)
def add_new_ticker(data: TickerCreate, session=Depends(get_session)):
    with TickerDBTransaction(session) as ticker:
        obj = ticker.new_object(data)
        ticker.add(obj)
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
