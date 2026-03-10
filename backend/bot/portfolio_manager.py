import structlog
from typing import Dict
from backend.bot.position_manager import PositionManager
from backend.bot.models import Position

logger = structlog.get_logger()


class PortfolioManager:
    """Manages the overall portfolio of positions and tracks MTM."""

    def __init__(self):
        self.positions: Dict[str, PositionManager] = {}  # token -> PositionManager
        self.realized_pnl: float = 0.0

    def add_position(self, position: Position):
        """Adds a new position to the portfolio."""
        if position.token in self.positions:
            logger.warning(
                f"Position for token {position.token} already exists, ignoring."
            )
            return

        self.positions[position.token] = PositionManager(position)
        logger.info(f"Added position for {position.symbol} to portfolio.")

    def remove_position(self, token: str, exit_price: float):
        """Removes a position, adding its PnL to the realized PnL."""
        pm = self.positions.get(token)
        if pm:
            pnl = pm.close_position(exit_price)
            self.realized_pnl += pnl
            del self.positions[token]
            logger.info(f"Removed position for token {token}. Realized PnL: {pnl}")

    def update_prices(self, updates: Dict[str, float]):
        """Updates prices for all active positions."""
        for token, new_price in updates.items():
            pm = self.positions.get(token)
            if pm:
                pm.update_price(new_price)

    def get_open_trades_count(self) -> int:
        """Returns the number of active open positions."""
        return len(self.positions)

    def get_total_mtm(self) -> float:
        """Calculates total mark-to-market (realized + unrealized)."""
        unrealized = sum(pm.get_unrealized_pnl() for pm in self.positions.values())
        return self.realized_pnl + unrealized
