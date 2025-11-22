from fastapi import APIRouter, Depends, Request
from dto.price import PriceCreate, PriceRead
from models.price import Price
from utils.auth import get_current_user
from utils.index import raise_format_error, run_sync


router = APIRouter(
    tags=["Prices"],
    prefix="/prices",
    dependencies=[Depends(get_current_user)]  # ensures auth
)


@router.get("/", response_model=list[PriceRead])
async def get_prices(request: Request):
    try:
        prices = await run_sync(lambda: Price.findAll())
        return [PriceRead.model_validate(u) for u in prices]
    except Exception as e:
        raise_format_error(e)
        
@router.get("/recent_prices/{symbol}")
async def get_recent_prices(symbol: str, request: Request):
    try:
        prices = await run_sync(lambda: Price.get_recent_prices(symbol))
        return prices
    except Exception as e:
        raise_format_error(e)


@router.post("/", response_model=PriceRead)
async def create_price(dto: PriceCreate,  request: Request):
    try:
        dto.user = request.state.user
        print(dto)
        new_price = await run_sync(lambda: Price.create_price(dto))
        return PriceRead.model_validate(new_price)
    except Exception as e:
        raise_format_error(e, "creating price")
        