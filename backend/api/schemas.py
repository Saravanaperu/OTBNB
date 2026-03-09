from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class Position(BaseModel):
    position_id: str
    instrument: str
    tradingsymbol: str
    token: str
    direction: str
    strike: int
    expiry: str
    entry_price: float
    entry_time: datetime
    lots: int
    lot_size: int
    quantity: int
    entry_greeks: Optional[Dict[str, float]] = None
    sl_price: float
    target_price: float
    trailing_sl_active: bool
    trailing_sl_price: float
    peak_price: float
    current_ltp: float
    unrealised_pnl: float
    unrealised_pnl_pct: float
    status: str
    strategy_name: str

class ClosedPosition(Position):
    exit_price: float
    exit_time: datetime
    exit_reason: str
    realised_pnl: float

class DailyPnL(BaseModel):
    date: str
    trade_count: int
    win_count: int
    gross_profit: float
    gross_loss: float
    net_pnl: float

class Trade(BaseModel):
    id: str
    instrument: str
    tradingsymbol: str
    direction: str
    strike: int
    expiry: str
    lots: int
    quantity: int
    entry_price: float
    entry_time: datetime
    exit_price: Optional[float]
    exit_time: Optional[datetime]
    exit_reason: Optional[str]
    realised_pnl: Optional[float]
    entry_delta: Optional[float]
    entry_iv: Optional[float]
    entry_iv_rank: Optional[float]
    strategy_name: str
    order_id_entry: str
    order_id_exit: Optional[str]
    status: str

class PerformanceStats(BaseModel):
    win_rate: float
    profit_factor: float
    avg_rr: float
    sharpe: float

class OptionData(BaseModel):
    ltp: float
    bid: float
    ask: float
    iv: float
    delta: float
    gamma: float
    theta: float
    vega: float
    oi: int
    oi_change: int
    volume: int

class StrikeData(BaseModel):
    CE: OptionData
    PE: OptionData

class OptionChain(BaseModel):
    instrument: str
    expiry: str
    spot: float
    atm_strike: int
    updated_at: datetime
    pcr_oi: float
    pcr_volume: float
    total_call_oi: int
    total_put_oi: int
    iv_rank: float
    iv_percentile: float
    strikes: Dict[int, StrikeData]

class RiskBudget(BaseModel):
    daily_loss_used: float
    remaining_budget: float
    open_position_count: int

class RiskConfig(BaseModel):
    daily_hard_limit: float
    daily_soft_limit: float
    per_trade_risk: float
    max_open_positions: int
    max_same_instrument: int
    max_lots_per_trade: int
    max_capital_pct: float
    iv_rank_buy_threshold: float
    min_delta: float
    max_delta: float
    max_theta_daily_pct: float
    min_strike_volume: int
    min_strike_oi: int
    max_bid_ask_spread_pct: float
    no_trade_after: str
    no_0dte_after: str

class StrategyConfig(BaseModel):
    name: str
    enabled: bool
    instruments: List[str]
    params: Dict[str, Any]
