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

    def approve(self, signal: Any, portfolio: Any) -> RiskApproval:
        """Approves or rejects a signal."""
        return RiskApproval(ok=True)

    def size(self, signal: Any, portfolio: Any) -> int:
        """Calculates position size (number of lots)."""
        return 1
