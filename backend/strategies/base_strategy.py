from abc import ABC, abstractmethod
from typing import List, Optional

from backend.bot.models import Signal, Position, MarketSnapshot, ExitSignal

class BaseStrategy(ABC):
    name: str
    instruments: List[str]    # ['NIFTY', 'BANKNIFTY']
    enabled: bool

    @abstractmethod
    def generate_signal(self, snapshot: MarketSnapshot) -> Optional[Signal]:
        pass

    @abstractmethod
    def should_exit(self, position: Position, snapshot: MarketSnapshot) -> Optional[ExitSignal]:
        pass

    def select_strike(self, spot: float, direction: str, moneyness: str = 'ATM') -> int:
        raise NotImplementedError("select_strike depends on InstrumentRegistry, which is not yet implemented.")
