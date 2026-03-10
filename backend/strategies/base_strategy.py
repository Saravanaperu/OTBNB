import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

from bot.models import Signal, Position, MarketSnapshot, ExitSignal
from bot.instrument_registry import InstrumentRegistry

class BaseStrategy(ABC):
    name: str
    instruments: List[str]    # ['NIFTY', 'BANKNIFTY']
    enabled: bool

    @abstractmethod
    def generate_signal(self, snapshot: MarketSnapshot, registry: InstrumentRegistry) -> Optional[Signal]:
        pass

    @abstractmethod
    def should_exit(self, position: Position, snapshot: MarketSnapshot) -> Optional[ExitSignal]:
        pass

    def select_strike(self, symbol: str, spot: float, direction: str, registry: InstrumentRegistry, moneyness: str = 'ATM') -> Optional[str]:
        """
        Selects a strike token based on instrument symbol, spot price, direction ('CE' or 'PE').
        Returns the instrument token for the nearest expiry.
        """
        if not registry.master_data:
            return None

        # Determine step size based on symbol
        step_size = 50.0 if symbol == 'NIFTY' else 100.0

        # Round spot to nearest strike
        atm_strike = round(spot / step_size) * step_size

        target_strike = atm_strike

        # Adjust for moneyness if needed
        # For 'OTM', 'ITM', we could shift by step_size
        if moneyness == 'OTM':
            if direction == 'CE':
                target_strike += step_size
            else:
                target_strike -= step_size
        elif moneyness == 'ITM':
            if direction == 'CE':
                target_strike -= step_size
            else:
                target_strike += step_size

        # Find all matching options in registry master_data for the target strike and direction
        # AngelOne 'strike' format: "1900000.000000" which means 19000.
        matching_options = []
        for inst in registry.master_data:
            if inst.get('name') == symbol and inst.get('exch_seg') == 'NFO' and inst.get('instrumenttype') == 'OPTIDX':
                inst_strike_str = inst.get('strike', '0')
                try:
                    inst_strike = float(inst_strike_str) / 100.0
                except ValueError:
                    continue

                inst_symbol = inst.get('symbol', '')
                if inst_symbol.endswith(direction):
                    if abs(inst_strike - target_strike) < 1.0:
                        expiry_str = inst.get('expiry')
                        if expiry_str:
                            try:
                                # Example expiry format: "29JUN2023"
                                expiry_date = datetime.datetime.strptime(expiry_str, '%d%b%Y').date()
                                # Only consider future or today's expiries
                                if expiry_date >= datetime.date.today():
                                    matching_options.append((expiry_date, inst.get('token')))
                            except ValueError:
                                pass

        if not matching_options:
            return None

        # Sort by expiry date (ascending) to get the nearest expiry
        matching_options.sort(key=lambda x: x[0])
        return matching_options[0][1]
