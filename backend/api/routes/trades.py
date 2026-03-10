from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import date
from backend.api.schemas import Trade, PerformanceStats
from backend.storage.repositories import TradeRepository

router = APIRouter()
repo = TradeRepository()


@router.get("/", response_model=List[Trade])
async def get_trades(target_date: Optional[date] = Query(None, alias="date")):
    """Full trade log for a given date"""
    db_trades = await repo.get_all_trades(limit=10000, target_date=target_date)
    return [
        Trade(
            id=t.id,
            instrument=t.instrument,
            tradingsymbol=t.tradingsymbol,
            direction=t.direction,
            strike=t.strike,
            expiry=t.expiry,
            lots=t.lots,
            quantity=t.quantity,
            entry_price=t.entry_price,
            entry_time=t.entry_time,
            exit_price=t.exit_price,
            exit_time=t.exit_time,
            exit_reason=t.exit_reason,
            realised_pnl=t.realised_pnl,
            entry_delta=t.entry_delta,
            entry_iv=t.entry_iv,
            entry_iv_rank=t.entry_iv_rank,
            strategy_name=t.strategy_name,
            order_id_entry=t.order_id_entry,
            order_id_exit=t.order_id_exit,
            status=t.status,
        )
        for t in db_trades
    ]


@router.get("/stats", response_model=PerformanceStats)
async def get_trade_stats():
    """Win rate, profit factor, avg R:R, Sharpe (rolling 30d)"""
    return {"win_rate": 0.0, "profit_factor": 0.0, "avg_rr": 0.0, "sharpe": 0.0}
