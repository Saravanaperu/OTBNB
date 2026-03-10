from fastapi import APIRouter
from typing import List
from backend.api.schemas import DailyPnL

router = APIRouter()


@router.get("/today", response_model=DailyPnL)
async def get_pnl_today():
    """Today's realised + unrealised P&L, win rate, trade count"""
    import datetime
    from backend.main import bot_state

    pm = bot_state.get("portfolio_manager")

    net_pnl = pm.get_total_mtm() if pm else 0.0
    trade_count = pm.get_open_trades_count() if pm else 0

    return {
        "date": datetime.date.today().isoformat(),
        "trade_count": trade_count,
        "win_count": 0,
        "gross_profit": 0.0,
        "gross_loss": 0.0,
        "net_pnl": net_pnl,
    }


@router.get("/history", response_model=List[DailyPnL])
async def get_pnl_history(days: int = 30):
    """Historical daily P&L for charting"""
    return []
