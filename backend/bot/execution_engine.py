import time
import structlog
from typing import Dict, Any, Optional
from backend.bot.session_manager import SessionManager
from backend.bot.models import Signal

logger = structlog.get_logger()


class ExecutionEngine:
    """Handles order placement, modification, and cancellation via SmartAPI."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.max_retries = 3

    def _execute_with_retry(self, func, *args, **kwargs) -> Any:
        """Executes a function with exponential backoff retry logic."""
        delay = 1.0
        for attempt in range(1, self.max_retries + 1):
            try:
                response = func(*args, **kwargs)
                # Check for API failure
                if isinstance(response, dict):
                    if response.get("status") is False:
                        error_msg = response.get("message", "Unknown error")
                        logger.warning(
                            "API request failed",
                            attempt=attempt,
                            error=error_msg,
                            func_name=func.__name__,
                        )
                        raise Exception(f"API error: {error_msg}")
                return response
            except Exception as e:
                logger.error(
                    "API call exception",
                    attempt=attempt,
                    error=str(e),
                    func_name=func.__name__,
                )
                if attempt == self.max_retries:
                    logger.error("Max retries reached. Operation failed.")
                    raise
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff

    def place_order(self, signal: Signal) -> Optional[str]:
        """
        Places an order based on the provided Signal.
        """
        sm = self.session_manager
        if not sm.is_connected or not sm.api:
            logger.error("Cannot place order: Session not connected")
            return None

        if not signal.quantity:
            logger.error("Cannot place order: Quantity is missing.")
            return None

        # Build order params based on the schema discovered
        orderparams: Dict[str, str] = {
            "variety": "NORMAL",
            "tradingsymbol": signal.symbol,
            "symboltoken": signal.token,
            "transactiontype": signal.side,
            "exchange": "NFO",  # Options trading
            "ordertype": "MARKET",  # Defaulting to MARKET
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": "0",  # Market order doesn't need a specific price
            "squareoff": "0",
            "stoploss": "0",
            "quantity": str(signal.quantity),
        }

        logger.info("Placing order", orderparams=orderparams)

        try:
            # Returns order ID if successful, or a dict response
            response = self._execute_with_retry(
                self.session_manager.api.placeOrder, orderparams
            )
            logger.info("Order placed successfully", response=response)

            if isinstance(response, dict):
                return response.get("data", {}).get("orderid", str(response))
            return str(response)

        except Exception as e:
            logger.error("Failed to place order", error=str(e))
            return None

    def cancel_order(self, order_id: str, variety: str = "NORMAL") -> bool:
        """
        Cancels an existing order.
        """
        sm = self.session_manager
        if not sm.is_connected or not sm.api:
            logger.error("Cannot cancel order: Session not connected")
            return False

        logger.info("Canceling order", order_id=order_id, variety=variety)

        try:
            response = self._execute_with_retry(
                self.session_manager.api.cancelOrder, order_id, variety
            )
            logger.info("Order canceled successfully", response=response)
            return True
        except Exception as e:
            logger.error("Cancel failed", error=str(e), order_id=order_id)
            return False

    def modify_order(self, orderparams: Dict[str, str]) -> bool:
        """
        Modifies an existing order.
        """
        sm = self.session_manager
        if not sm.is_connected or not sm.api:
            logger.error("Cannot modify order: Session not connected")
            return False

        logger.info("Modifying order", orderparams=orderparams)

        try:
            response = self._execute_with_retry(
                self.session_manager.api.modifyOrder, orderparams
            )
            logger.info("Order modified successfully", response=response)
            return True
        except Exception as e:
            logger.error("Failed to modify order", error=str(e))
            return False
