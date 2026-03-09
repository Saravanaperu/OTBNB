from fastapi import APIRouter
from typing import List
from backend.api.schemas import DailyPnL

router = APIRouter()

@router.get("/today", response_model=DailyPnL)
async def get_pnl_today():
    """Today's realised + unrealised P&L, win rate, trade count"""
    import datetime
    return {
        "date": datetime.date.today().isoformat(),
        "trade_count": 0,
        "win_count": 0,
        "gross_profit": 0.0,
        "gross_loss": 0.0,
        "net_pnl": 0.0
    }

@router.get("/history", response_model=List[DailyPnL])
async def get_pnl_history(days: int = 30):
    """Historical daily P&L for charting"""
    return []
