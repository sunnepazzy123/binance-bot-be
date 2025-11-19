import uuid
from fastapi import APIRouter, Depends, Request
from dto.trading_pairs import TradingPairCreate, TradingPairRead
from models.trading_pair import TradingPair
from utils.auth import get_current_user
from utils.index import raise_format_error, run_sync


router = APIRouter(
    tags=["Trading Pairs"],
    prefix="/trading_pairs",
    dependencies=[Depends(get_current_user)]  # ensures auth
)


@router.get("/", response_model=list[TradingPairRead])
async def get_trading_pairs(request: Request):
    try:
        trading_pairs = await run_sync(lambda: TradingPair.findAll())
        # Convert each dict to Pydantic TradingPairRead
        return [TradingPairRead.model_validate(u) for u in trading_pairs]
    except Exception as e:
        raise_format_error(e)

@router.get("/{id}", response_model=TradingPairRead)
async def get_trading_pair(id: uuid.UUID, request: Request):
    try:
        trading_pair = await run_sync(lambda: TradingPair.findOne(id))
        return TradingPairRead.model_validate(trading_pair)
    except Exception as e:
        raise_format_error(e)
        
@router.get("/symbol/{symbol}", response_model=TradingPairRead)
async def get_symbol_pair(symbol: str, request: Request):
    try:
        user_id = request.state.user
        trading_pair = await run_sync(lambda: TradingPair.findOneBySymbol(symbol, user_id))
        return TradingPairRead.model_validate(trading_pair)
    except Exception as e:
        raise_format_error(e, "Error fetching trading pair")
        

@router.post("/", response_model=TradingPairRead)
async def create_trading_pair(dto: TradingPairCreate):
    try:
        new_trade_pair = await run_sync(lambda: TradingPair.upsert_trading_pair(dto))
        return TradingPairRead.model_validate(new_trade_pair)
    except Exception as e:
        raise_format_error(e, "creating trading pair")
        