from typing import Optional
from backend.bot.models import Signal, Position, MarketSnapshot, ExitSignal
from backend.strategies.base_strategy import BaseStrategy
from backend.bot.instrument_registry import InstrumentRegistry


class OIBuildupStrategy(BaseStrategy):
    name = "OI Buildup"
    instruments = ["NIFTY", "BANKNIFTY"]
    enabled = True

    def generate_signal(
        self, snapshot: MarketSnapshot, registry: InstrumentRegistry
    ) -> Optional[Signal]:
        # Entry Conditions from doc1.txt for Strategy 2: OI Buildup
        # Long Buildup: Price Rising, OI Rising -> Buy CE
        # Short Covering: Price Rising, OI Falling -> Buy CE
        # Short Buildup: Price Falling, OI Rising -> Buy PE
        # Long Unwinding: Price Falling, OI Falling -> Buy PE

        # We need historical comparison, using snapshot vs some previous state
        # In this implementation, we assume snapshot has 'previous_close' and 'previous_open_interest'

        if not snapshot.previous_close or not snapshot.previous_open_interest:
            return None  # Need previous data to compare

        price_rising = snapshot.close > snapshot.previous_close
        price_falling = snapshot.close < snapshot.previous_close

        oi_rising = snapshot.open_interest > snapshot.previous_open_interest
        oi_falling = snapshot.open_interest < snapshot.previous_open_interest

        signal_side = None
        direction = None

        if price_rising and oi_rising:
            # Long Buildup
            signal_side = "BUY_CE"
            direction = "CE"
        elif price_rising and oi_falling:
            # Short Covering
            signal_side = "BUY_CE"
            direction = "CE"
        elif price_falling and oi_rising:
            # Short Buildup
            signal_side = "BUY_PE"
            direction = "PE"
        elif price_falling and oi_falling:
            # Long Unwinding
            signal_side = "BUY_PE"
            direction = "PE"

        if signal_side:
            # VWAP check as confirmation
            if signal_side == "BUY_CE" and snapshot.close > snapshot.vwap:
                token = self.select_strike(
                    snapshot.symbol, snapshot.close, direction, registry
                )
                if token:
                    return Signal(
                        symbol=snapshot.symbol,
                        token=token,
                        side=signal_side,
                        entry_price=snapshot.close,
                        stop_loss=snapshot.close * 0.9,  # Placeholder stop loss
                        target=snapshot.close * 1.2,  # Placeholder target
                    )
            elif signal_side == "BUY_PE" and snapshot.close < snapshot.vwap:
                token = self.select_strike(
                    snapshot.symbol, snapshot.close, direction, registry
                )
                if token:
                    return Signal(
                        symbol=snapshot.symbol,
                        token=token,
                        side=signal_side,
                        entry_price=snapshot.close,
                        stop_loss=snapshot.close * 0.9,  # Placeholder stop loss
                        target=snapshot.close * 1.2,  # Placeholder target
                    )

        return None

    def should_exit(
        self, position: Position, snapshot: MarketSnapshot
    ) -> Optional[ExitSignal]:
        # Placeholder exit logic
        if position.side == "BUY_CE":
            if snapshot.close < snapshot.vwap:
                return ExitSignal(
                    symbol=position.symbol,
                    token=position.token,
                    reason="Price below VWAP",
                )
        elif position.side == "BUY_PE":
            if snapshot.close > snapshot.vwap:
                return ExitSignal(
                    symbol=position.symbol,
                    token=position.token,
                    reason="Price above VWAP",
                )

        return None
