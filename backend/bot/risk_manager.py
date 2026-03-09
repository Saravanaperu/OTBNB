import structlog
from typing import Dict, Any

logger = structlog.get_logger()

class RiskApproval:
    def __init__(self, ok: bool, reason: str = ""):
        self.ok = ok
        self.reason = reason

class RiskManager:
    """Evaluates trades against risk constraints."""
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.max_loss = self.config.get('daily_loss_limit', 5000)
        self.max_trades = self.config.get('max_open_positions', 5)
        self.risk_per_trade = self.config.get('risk_per_trade', 1000)

    def approve(self, signal: Any, portfolio: Any) -> RiskApproval:
        """Approves or rejects a signal."""
        if portfolio.get_total_mtm() < -self.max_loss:
            return RiskApproval(ok=False, reason="Daily loss limit breached")

        if portfolio.get_open_trades_count() >= self.max_trades:
            return RiskApproval(ok=False, reason="Max open positions reached")

        return RiskApproval(ok=True)

    def size(self, signal: Any, lot_size: int) -> int:
        """Calculates position size (number of lots)."""
        if signal.entry_price == signal.stop_loss:
            return lot_size

        risk_per_unit = abs(signal.entry_price - signal.stop_loss)
        max_units = self.risk_per_trade / risk_per_unit

        # Calculate number of lots, ensuring at least 1 lot
        lots = int(max_units / lot_size)
        lots = max(1, lots)

        return lots * lot_size
