from fastapi import APIRouter, Depends, Request
from dto.order import OrderRead
from models.order import Order
from utils.auth import get_current_user
from utils.index import raise_format_error, run_sync


router = APIRouter(
    tags=["Orders"],
    prefix="/orders",
    dependencies=[Depends(get_current_user)]  # ensures auth
)


@router.get("/", response_model=list[OrderRead])
async def get_orders(request: Request):
    try:
        userId = request.state.user
        orders = await run_sync(lambda: Order.findAllByUser(userId))
        return [OrderRead.model_validate(u) for u in orders]
    except Exception as e:
        raise_format_error(e)
        
