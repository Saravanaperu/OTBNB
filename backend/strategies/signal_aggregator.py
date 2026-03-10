from typing import List, Optional
from backend.bot.models import Signal, MarketSnapshot
from backend.strategies.base_strategy import BaseStrategy
from backend.bot.instrument_registry import InstrumentRegistry


class SignalAggregator:
    def __init__(self, strategies: List[BaseStrategy], registry: InstrumentRegistry):
        self.strategies = strategies
        self.registry = registry

    def process_snapshot(self, snapshot: MarketSnapshot) -> Optional[Signal]:
        """
        Process a market snapshot across all enabled strategies.
        Returns the first generated signal based on strategy priority (list order).
        """
        for strategy in self.strategies:
            if not strategy.enabled or snapshot.symbol not in strategy.instruments:
                continue

            signal = strategy.generate_signal(snapshot, self.registry)
            if signal:
                return signal

        return None
