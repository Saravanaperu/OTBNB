import structlog
from typing import Dict, Any

logger = structlog.get_logger()


class OptionChainManager:
    """Manages live option chain state."""

    def __init__(self, registry):
        self.registry = registry
        self.chain_state: Dict[str, Any] = {}

    def update(self, instrument: str, tick: Dict[str, Any]):
        """Updates the option chain with a new tick."""
        token = tick.get("token")
        if not token:
            return

        if instrument not in self.chain_state:
            self.chain_state[instrument] = {}

        if token not in self.chain_state[instrument]:
            self.chain_state[instrument][token] = {}

        # Update tick data
        self.chain_state[instrument][token].update(tick)

    def get_snapshot(self, instrument: str) -> Dict[str, Any]:
        """Returns the current state of the option chain."""
        return self.chain_state.get(instrument, {})
