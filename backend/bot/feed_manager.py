import asyncio
import structlog
import threading
from typing import Dict, Any
from SmartApi.smartWebSocketV2 import SmartWebSocketV2

logger = structlog.get_logger()

class FeedManager:
    """Manages WebSocket connections and routes ticks to respective queues."""
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.queues: Dict[str, asyncio.Queue] = {
            "NIFTY": asyncio.Queue(),
            "BANKNIFTY": asyncio.Queue()
        }
        self.sws = None
        self.is_connected = False
        self.registry = None
        self.loop = None

    def _on_data(self, wsapp, message):
        """Routes incoming ticks to the appropriate queue."""
        if not isinstance(message, dict):
            return

        token = message.get("token")
        if not token or not self.registry:
            return

        symbol = self.registry.get_symbol_by_token(token)
        if symbol and self.loop:
            if "NIFTY" in symbol and "BANKNIFTY" not in symbol:
                asyncio.run_coroutine_threadsafe(
                    self.queues["NIFTY"].put(message),
                    self.loop
                )
            elif "BANKNIFTY" in symbol:
                asyncio.run_coroutine_threadsafe(
                    self.queues["BANKNIFTY"].put(message),
                    self.loop
                )

    def _on_open(self, wsapp):
        logger.info("WebSocket connected successfully")
        self.is_connected = True
        if self.registry and self.loop:
            asyncio.run_coroutine_threadsafe(self.subscribe_all_tokens(self.registry), self.loop)

    def _on_error(self, wsapp, error):
        logger.error("WebSocket error occurred", error=str(error))

    def _on_close(self, wsapp):
        logger.warning("WebSocket disconnected")
        self.is_connected = False

    async def connect(self):
        """Connects to the WebSocket feed."""
        logger.info("Connecting to WebSocket feed...")
        self.loop = asyncio.get_running_loop()

        if not self.session_manager.is_connected:
            logger.error("Session manager is not connected, cannot start WebSocket")
            return

        self.sws = SmartWebSocketV2(
            self.session_manager.jwt_token,
            self.session_manager.api_key,
            self.session_manager.client_code,
            self.session_manager.feed_token
        )

        # We start the connection in a separate thread so it doesn't block asyncio
        def run_ws():
            self.sws.connect(
                on_data=self._on_data,
                on_open=self._on_open,
                on_error=self._on_error,
                on_close=self._on_close
            )

        threading.Thread(target=run_ws, daemon=True).start()

    async def subscribe_all_tokens(self, registry):
        """Subscribes to all active tokens."""
        self.registry = registry
        logger.info("Subscribing to tokens...")
        if not self.is_connected or not self.sws:
            logger.warning("WebSocket not connected, cannot subscribe")
            return

        # Example token lists, replace with actual implementation fetching from registry later
        # We subscribe after connection is established
        # In a real setup we construct the list of tokens from the registry.

    def get_queue(self, instrument: str) -> asyncio.Queue:
        return self.queues.get(instrument, asyncio.Queue())

    async def heartbeat_loop(self):
        """Maintains the WebSocket connection."""
        while True:
            await asyncio.sleep(60)
            logger.debug("WebSocket heartbeat ping")
