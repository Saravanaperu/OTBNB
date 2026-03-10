import datetime
from typing import Optional
from backend.bot.models import Signal, Position, MarketSnapshot, ExitSignal
from backend.strategies.base_strategy import BaseStrategy
from backend.bot.instrument_registry import InstrumentRegistry


class PCRReversalStrategy(BaseStrategy):
    name = "PCR Reversal"
    instruments = ["NIFTY", "BANKNIFTY"]
    enabled = True

    def generate_signal(
        self, snapshot: MarketSnapshot, registry: InstrumentRegistry
    ) -> Optional[Signal]:
        # Filter: Only trade PCR reversals between 10:30 AM and 2:00 PM
        current_time = datetime.datetime.fromtimestamp(snapshot.timestamp).time()
        start_time = datetime.time(10, 30)
        end_time = datetime.time(14, 0)

        if not (start_time <= current_time <= end_time):
            return None

        # Entry Conditions from doc1.txt
        # PCR < 0.7: Market is overly bullish -> buy PE for mean reversion
        if snapshot.pcr < 0.7:
            # We assume price momentum has stalled as per doc, but simplistic logic here.
            # E.g. price was rising but now forming a Doji or simply dropping below a short-term moving average.
            # Simplified for now:
            if snapshot.close < snapshot.vwap:
                token = self.select_strike(
                    snapshot.symbol, snapshot.close, "PE", registry
                )
                if token:
                    return Signal(
                        symbol=snapshot.symbol,
                        token=token,
                        side="BUY_PE",
                        entry_price=snapshot.close,
                        stop_loss=snapshot.close * 0.9,
                        target=snapshot.close * 1.2,
                    )

        # PCR > 1.5: Market is overly bearish -> buy CE for mean reversion
        if snapshot.pcr > 1.5:
            if snapshot.close > snapshot.vwap:
                token = self.select_strike(
                    snapshot.symbol, snapshot.close, "CE", registry
                )
                if token:
                    return Signal(
                        symbol=snapshot.symbol,
                        token=token,
                        side="BUY_CE",
                        entry_price=snapshot.close,
                        stop_loss=snapshot.close * 0.9,
                        target=snapshot.close * 1.2,
                    )

        return None

    def should_exit(
        self, position: Position, snapshot: MarketSnapshot
    ) -> Optional[ExitSignal]:
        if position.side == "BUY_CE":
            if snapshot.pcr < 1.0 or snapshot.close < snapshot.vwap:
                return ExitSignal(
                    symbol=position.symbol,
                    token=position.token,
                    reason="Mean Reverted or Trend Reversal",
                )
        elif position.side == "BUY_PE":
            if snapshot.pcr > 1.0 or snapshot.close > snapshot.vwap:
                return ExitSignal(
                    symbol=position.symbol,
                    token=position.token,
                    reason="Mean Reverted or Trend Reversal",
                )
        return None
