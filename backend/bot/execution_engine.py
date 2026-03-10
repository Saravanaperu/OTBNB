import asyncio
import structlog
from backend.bot.models import Signal, Position, ExitSignal
from backend.bot.session_manager import SessionManager

logger = structlog.get_logger()


class ExecutionEngine:
    """Handles order execution with AngelOne SmartAPI."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def buy(
        self,
        signal: Signal,
        lots: int,
        exchange: str,
        variety: str,
        order_type: str,
        product_type: str,
        duration: str,
    ) -> str | None:
        """
        Executes a buy order for the given signal and quantity.
        Returns the order ID if successful, else None.
        """
        if not self.session_manager.is_connected or not self.session_manager.api:
            logger.error("ExecutionEngine: Not connected to SmartAPI.")
            return None

        orderparams = {
            "variety": variety,
            "tradingsymbol": signal.symbol,
            "symboltoken": signal.token,
            "transactiontype": signal.side,
            "exchange": exchange,
            "ordertype": order_type,
            "producttype": product_type,
            "duration": duration,
            "quantity": str(lots),
        }

        # If it's a LIMIT order, we would need a price parameter, but we assume MARKET or the caller provides.
        # However, to be safe, if we get LIMIT we should have a price.
        # But for now, we map basic params.

        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                # Assuming session_manager.api is the SmartConnect instance
                logger.info(
                    "Placing buy order",
                    attempt=attempt + 1,
                    orderparams=orderparams,
                )

                # We need to run this blocking call in a thread
                # placeOrder is synchronous in smartapi-python
                response = await asyncio.to_thread(
                    self.session_manager.api.placeOrder, orderparams
                )

                if response:
                    logger.info("Buy order successful", order_id=response)
                    return response

                logger.warning(
                    "Buy order placeOrder returned None/False",
                    response=response,
                    attempt=attempt + 1,
                )

            except Exception as e:
                logger.error(
                    "Exception during buy order placement",
                    error=str(e),
                    attempt=attempt + 1,
                )

            if attempt < max_retries - 1:
                await asyncio.sleep(base_delay * (2**attempt))

        logger.error(
            "Failed to place buy order after all retries", orderparams=orderparams
        )
        return None

    async def exit(
        self,
        position: Position,
        exit_signal: ExitSignal,
        exchange: str,
        variety: str,
        order_type: str,
        product_type: str,
        duration: str,
    ) -> str | None:
        """
        Executes an exit order (opposite of current position) to close it.
        """
        if not self.session_manager.is_connected or not self.session_manager.api:
            logger.error("ExecutionEngine: Not connected to SmartAPI.")
            return None

        # Opposite transaction type to close
        transaction_type = "SELL" if position.side.upper() == "BUY" else "BUY"

        orderparams = {
            "variety": variety,
            "tradingsymbol": position.symbol,
            "symboltoken": position.token,
            "transactiontype": transaction_type,
            "exchange": exchange,
            "ordertype": order_type,
            "producttype": product_type,
            "duration": duration,
            "quantity": str(position.quantity),
        }

        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                logger.info(
                    "Placing exit order",
                    attempt=attempt + 1,
                    orderparams=orderparams,
                    reason=exit_signal.reason,
                )

                response = await asyncio.to_thread(
                    self.session_manager.api.placeOrder, orderparams
                )

                if response:
                    logger.info("Exit order successful", order_id=response)
                    return response

                logger.warning(
                    "Exit order placeOrder returned None/False",
                    response=response,
                    attempt=attempt + 1,
                )

            except Exception as e:
                logger.error(
                    "Exception during exit order placement",
                    error=str(e),
                    attempt=attempt + 1,
                )

            if attempt < max_retries - 1:
                await asyncio.sleep(base_delay * (2**attempt))

        logger.error(
            "Failed to place exit order after all retries", orderparams=orderparams
        )
        return None
