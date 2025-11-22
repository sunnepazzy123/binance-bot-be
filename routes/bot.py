import asyncio
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dto.trading_pairs import TradingPairCreate
from third_party.binance.bot import start_bot_dynamic
from utils.auth import get_current_user
from utils.index import raise_format_error
from third_party.binance.config import bot_status, bot_tasks


router = APIRouter(
    tags=["Bots"],
    prefix="/bots",
    dependencies=[Depends(get_current_user)]  # ensures auth
)


@router.post("/start")
async def start_bot(dto: TradingPairCreate, request: Request):
    try:
        symbol = dto.symbol.upper()
        dto.user = request.state.user
        
        # ------------------------------
        # 1️⃣ Prevent duplicate bot start
        # ------------------------------
        if symbol in bot_status and bot_status[symbol]["status"] == "running":
            return JSONResponse(
                {
                    "success": False,
                    "message": f"Bot for {symbol} is already running."
                },
                status_code=400
            )

        # Get loop safely
        loop = asyncio.get_running_loop()

        # Create async background task (safe)
        task = loop.create_task(start_bot_dynamic(dto))
        # Save task + status
        bot_tasks[symbol] = task
        bot_status[symbol] = {
            "status": "running",
            "last_trade": None,
            "user": dto.user
        }

        return {
            "status": "started",
            "message": f"Bot started for {symbol}",
            "symbol": symbol,
            "user": dto.user
        }

    except Exception as e:
        raise_format_error(e)
        
@router.get("/status/{symbol}")
async def get_recent_prices(symbol: str,):
    try:
        return bot_status[symbol]
    except Exception as e:
        raise_format_error(e)
