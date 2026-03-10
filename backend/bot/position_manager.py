import structlog
from bot.models import Position

logger = structlog.get_logger()

class PositionManager:
    """Manages individual open positions and calculates unrealized PnL."""
    def __init__(self, position: Position):
        self.position = position

    def update_price(self, new_price: float):
        """Updates the current price and recalculates unrealized PnL."""
        self.position.current_price = new_price

        if self.position.side == 'BUY':
            pnl_per_unit = new_price - self.position.entry_price
        else: # SELL
            pnl_per_unit = self.position.entry_price - new_price

        self.position.unrealized_pnl = pnl_per_unit * self.position.quantity

    def get_unrealized_pnl(self) -> float:
        """Returns the current unrealized PnL."""
        return self.position.unrealized_pnl

    def close_position(self, exit_price: float) -> float:
        """Closes the position and returns the realized PnL."""
        self.update_price(exit_price)
        realized_pnl = self.get_unrealized_pnl()
        logger.info(
            "Position closed",
            symbol=self.position.symbol,
            pnl=realized_pnl,
            exit_price=exit_price
        )
        return realized_pnl
