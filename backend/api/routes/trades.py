from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import date, datetime, timedelta
import math
import statistics
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
    db_trades = await repo.get_all_trades(limit=10000)

    thirty_days_ago = datetime.now() - timedelta(days=30)

    closed_trades = [
        t
        for t in db_trades
        if t.status == "CLOSED" and t.exit_time and t.exit_time >= thirty_days_ago
    ]

    if not closed_trades:
        return {"win_rate": 0.0, "profit_factor": 0.0, "avg_rr": 0.0, "sharpe": 0.0}

    winning_trades = [t for t in closed_trades if t.realised_pnl > 0]
    losing_trades = [t for t in closed_trades if t.realised_pnl <= 0]

    win_rate = len(winning_trades) / len(closed_trades)

    gross_profit = sum(t.realised_pnl for t in winning_trades)
    gross_loss = abs(sum(t.realised_pnl for t in losing_trades))

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else float("inf") if gross_profit > 0 else 0.0
    )
    if profit_factor == float("inf"):
        profit_factor = 999.0  # Cap or keep reasonable for json response

    avg_profit = gross_profit / len(winning_trades) if winning_trades else 0.0
    avg_loss = gross_loss / len(losing_trades) if losing_trades else 0.0

    avg_rr = (
        avg_profit / avg_loss
        if avg_loss > 0
        else float("inf") if avg_profit > 0 else 0.0
    )
    if avg_rr == float("inf"):
        avg_rr = 999.0

    # Group PnL by date for Sharpe ratio (daily returns)
    daily_pnl = {}
    for t in closed_trades:
        if t.exit_time:
            d = t.exit_time.date()
            daily_pnl[d] = daily_pnl.get(d, 0.0) + t.realised_pnl

    daily_returns = list(daily_pnl.values())
    if len(daily_returns) > 1:
        mean_pnl = statistics.mean(daily_returns)
        std_pnl = statistics.stdev(daily_returns)
        sharpe = (mean_pnl / std_pnl) * math.sqrt(252) if std_pnl > 0 else 0.0
    else:
        sharpe = 0.0

    return {
        "win_rate": round(win_rate, 4),
        "profit_factor": round(profit_factor, 4),
        "avg_rr": round(avg_rr, 4),
        "sharpe": round(sharpe, 4),
    }
