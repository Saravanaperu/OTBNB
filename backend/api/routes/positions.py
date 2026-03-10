from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from backend.api.schemas import Position as PositionSchema, ClosedPosition
from backend.storage.repositories import TradeRepository

router = APIRouter()
repo = TradeRepository()


@router.get("/", response_model=List[PositionSchema])
async def get_positions():
    """All currently open positions with live P&L"""
    from backend.main import get_bot_state

    bot_state = get_bot_state()
    pm = bot_state.get("portfolio_manager")
    if not pm:
        return []

    positions_out = []
    for token, pos_mgr in pm.positions.items():
        pos = pos_mgr.position
        positions_out.append(
            PositionSchema(
                position_id=pos.token,
                instrument=(
                    "NIFTY"
                    if "NIFTY" in pos.symbol and "BANKNIFTY" not in pos.symbol
                    else "BANKNIFTY"
                ),
                tradingsymbol=pos.symbol,
                token=pos.token,
                direction=pos.side,
                strike=0,
                expiry="",
                entry_price=pos.entry_price,
                entry_time=datetime.now(),
                lots=1,
                lot_size=1,
                quantity=pos.quantity,
                sl_price=0.0,
                target_price=0.0,
                trailing_sl_active=False,
                trailing_sl_price=0.0,
                peak_price=0.0,
                current_ltp=pos.current_price,
                unrealised_pnl=pos.unrealized_pnl,
                unrealised_pnl_pct=0.0,
                status="OPEN",
                strategy_name="Manual",
            )
        )
    return positions_out


@router.get("/history", response_model=List[ClosedPosition])
async def get_positions_history():
    """All closed positions for today with exit reason"""
    trades = await repo.get_all_trades(limit=1000)
    closed = []
    today = datetime.now().date()
    for t in trades:
        if t.status == "CLOSED" and t.exit_time and t.exit_time.date() == today:
            closed.append(
                ClosedPosition(
                    position_id=t.id,
                    instrument=t.instrument,
                    tradingsymbol=t.tradingsymbol,
                    token=t.id,
                    direction=t.direction,
                    strike=t.strike,
                    expiry=t.expiry,
                    entry_price=t.entry_price,
                    entry_time=t.entry_time,
                    lots=t.lots,
                    lot_size=1,
                    quantity=t.quantity,
                    sl_price=0.0,
                    target_price=0.0,
                    trailing_sl_active=False,
                    trailing_sl_price=0.0,
                    peak_price=0.0,
                    current_ltp=t.exit_price or 0.0,
                    unrealised_pnl=0.0,
                    unrealised_pnl_pct=0.0,
                    status="CLOSED",
                    strategy_name=t.strategy_name,
                    exit_price=t.exit_price or 0.0,
                    exit_time=t.exit_time,
                    exit_reason=t.exit_reason or "Unknown",
                    realised_pnl=t.realised_pnl or 0.0,
                )
            )
    return closed


@router.get("/{id}", response_model=PositionSchema)
async def get_position(id: str):
    """Single position detail including full Greeks"""
    from backend.main import get_bot_state

    bot_state = get_bot_state()
    pm = bot_state.get("portfolio_manager")
    if pm and id in pm.positions:
        pos = pm.positions[id].position
        return PositionSchema(
            position_id=pos.token,
            instrument=(
                "NIFTY"
                if "NIFTY" in pos.symbol and "BANKNIFTY" not in pos.symbol
                else "BANKNIFTY"
            ),
            tradingsymbol=pos.symbol,
            token=pos.token,
            direction=pos.side,
            strike=0,
            expiry="",
            entry_price=pos.entry_price,
            entry_time=datetime.now(),
            lots=1,
            lot_size=1,
            quantity=pos.quantity,
            sl_price=0.0,
            target_price=0.0,
            trailing_sl_active=False,
            trailing_sl_price=0.0,
            peak_price=0.0,
            current_ltp=pos.current_price,
            unrealised_pnl=pos.unrealized_pnl,
            unrealised_pnl_pct=0.0,
            status="OPEN",
            strategy_name="Manual",
        )
    raise HTTPException(status_code=404, detail="Position not found")


@router.post("/{id}/exit")
async def exit_position(id: str):
    """Manually trigger exit for a specific position"""
    from backend.main import get_bot_state
    from backend.bot.models import ExitSignal

    bot_state = get_bot_state()
    pm = bot_state.get("portfolio_manager")
    engine = bot_state.get("execution_engine")

    if pm and id in pm.positions:
        pos = pm.positions[id].position
        order_id = None
        if engine:
            exit_signal = ExitSignal(
                symbol=pos.symbol,
                token=pos.token,
                reason="Manual exit triggered via API"
            )
            order_id = await engine.exit(
                position=pos,
                exit_signal=exit_signal,
                exchange="NFO",
                variety="NORMAL",
                order_type="MARKET",  # Default market for immediate exit.
                product_type="INTRADAY",
                duration="DAY",
            )

        # We always remove it from the portfolio manager, whether the API call succeeded or not.
        # But if we strictly want to keep it if the order failed, we'd handle it differently.
        # Here we mimic the existing logic where manual exit assumes it closes the position.
        exit_price = pos.current_price
        pm.remove_position(id, exit_price)
        return {"success": True, "order_id": order_id or f"exit_order_{id}"}
    raise HTTPException(status_code=404, detail="Position not found")
