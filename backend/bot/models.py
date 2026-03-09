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
