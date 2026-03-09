from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import date
from backend.api.schemas import Trade, PerformanceStats

router = APIRouter()

@router.get("/", response_model=List[Trade])
async def get_trades(target_date: Optional[date] = Query(None, alias="date")):
    """Full trade log for a given date"""
    return []

@router.get("/stats", response_model=PerformanceStats)
async def get_trade_stats():
    """Win rate, profit factor, avg R:R, Sharpe (rolling 30d)"""
    return {
        "win_rate": 0.0,
        "profit_factor": 0.0,
        "avg_rr": 0.0,
        "sharpe": 0.0
    }
