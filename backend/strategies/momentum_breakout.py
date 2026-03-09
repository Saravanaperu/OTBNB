from typing import Optional
from backend.bot.models import Signal, Position, MarketSnapshot, ExitSignal
from backend.strategies.base_strategy import BaseStrategy

class MomentumBreakoutStrategy(BaseStrategy):
    name = "Momentum Breakout"
    instruments = ['NIFTY', 'BANKNIFTY']
    enabled = True

    def generate_signal(self, snapshot: MarketSnapshot) -> Optional[Signal]:
        # Entry Conditions from doc1.txt
        # Breakout Detection: 5-minute candle close above morning high (9:15-10:00 AM range) with body > 0.3% of open
        # Or close below morning low with body > 0.3% of open
        body = abs(snapshot.close - snapshot.open)
        body_percentage = body / snapshot.open if snapshot.open > 0 else 0

        # We need morning_high and morning_low from the snapshot.
        is_bullish_breakout = snapshot.close > snapshot.morning_high and body_percentage > 0.003
        is_bearish_breakout = snapshot.close < snapshot.morning_low and body_percentage > 0.003

        # Volume Confirmation: Breakout candle volume must be > 1.5x the 20-candle average volume
        has_volume = snapshot.volume > 1.5 * snapshot.average_volume

        if is_bullish_breakout and has_volume:
            # VWAP Alignment: CE signal -> price > VWAP
            if snapshot.close > snapshot.vwap:
                # Trend Filter: SuperTrend aligned with direction
                if snapshot.supertrend_direction == 'UP':
                    # RSI: Between 45 and 70 for CE entry
                    if 45 <= snapshot.rsi <= 70:
                        return Signal(
                            symbol=snapshot.symbol,
                            token=snapshot.token,
                            side='BUY_CE',
                            entry_price=snapshot.close,
                            stop_loss=snapshot.close * 0.9, # Placeholder stop loss
                            target=snapshot.close * 1.2 # Placeholder target
                        )

        elif is_bearish_breakout and has_volume:
            # VWAP Alignment: PE signal -> price < VWAP
            if snapshot.close < snapshot.vwap:
                # Trend Filter: SuperTrend aligned with direction
                if snapshot.supertrend_direction == 'DOWN':
                    # RSI: Between 30 and 55 for PE entry
                    if 30 <= snapshot.rsi <= 55:
                        return Signal(
                            symbol=snapshot.symbol,
                            token=snapshot.token,
                            side='BUY_PE',
                            entry_price=snapshot.close,
                            stop_loss=snapshot.close * 0.9, # Placeholder
                            target=snapshot.close * 1.2 # Placeholder
                        )

        return None

    def should_exit(self, position: Position, snapshot: MarketSnapshot) -> Optional[ExitSignal]:
        # Placeholder exit logic
        if position.side == 'BUY_CE':
            if snapshot.close < snapshot.vwap or snapshot.supertrend_direction == 'DOWN':
                return ExitSignal(symbol=position.symbol, token=position.token, reason="Trend Reversal")
        elif position.side == 'BUY_PE':
            if snapshot.close > snapshot.vwap or snapshot.supertrend_direction == 'UP':
                return ExitSignal(symbol=position.symbol, token=position.token, reason="Trend Reversal")

        return None
