from pydantic import BaseModel
from typing import Optional

class Position(BaseModel):
    symbol: str
    token: str
    side: str  # 'BUY' or 'SELL'
    quantity: int
    entry_price: float
    current_price: float
    unrealized_pnl: float = 0.0

class Signal(BaseModel):
    symbol: str
    token: str
    side: str
    quantity: Optional[int] = None
    entry_price: float
    stop_loss: float
    target: float

class MarketSnapshot(BaseModel):
    timestamp: float = 0.0
    symbol: str = ""
    token: str = ""
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0.0
    vwap: float = 0.0
    rsi: float = 0.0
    supertrend_direction: str = ""  # 'UP' or 'DOWN'
    open_interest: float = 0.0
    pcr: float = 0.0
    morning_high: float = 0.0
    morning_low: float = 0.0
    average_volume: float = 0.0
    previous_close: float = 0.0
    previous_open_interest: float = 0.0

class ExitSignal(BaseModel):
    symbol: str
    token: str
    reason: str
