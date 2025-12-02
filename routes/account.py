from fastapi import APIRouter, Depends, Request
from third_party.binance.binance import connect_binance, get_account_balance
from utils.auth import get_current_user
from utils.index import raise_format_error
from config.env_config import configLoaded


router = APIRouter(
    tags=["Account"],
    prefix="/accounts",
    dependencies=[Depends(get_current_user)]  # ensures auth
)



        
@router.get("/{symbol}")
async def get_accounts(symbol: str, request: Request):
    try:
        client, _ = await connect_binance(
            api_key=configLoaded.TEST_API_KEY,
            api_secret=configLoaded.TEST_SECRET_KEY,
            environment=configLoaded.ENVIRONMENT
            )
        balance = await get_account_balance(client, symbol)
        return balance
    except Exception as e:
        raise_format_error(e)
