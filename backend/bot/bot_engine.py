import asyncio
import structlog
from typing import Dict, List, Optional

from backend.bot.feed_manager import FeedManager
from backend.bot.option_chain_manager import OptionChainManager
from backend.bot.greeks_engine import GreeksEngine
from backend.bot.portfolio_manager import PortfolioManager
from backend.bot.execution_engine import ExecutionEngine
from backend.bot.risk_manager import RiskManager
from backend.strategies.signal_aggregator import SignalAggregator
from backend.bot.models import Position
from backend.bot.session_manager import SessionManager

logger = structlog.get_logger()


class BotEngine:
    """
    The main execution loop for the Options Buying Bot.
    Consumes live ticks, updates state, checks exits, and evaluates strategies.
    """

    def __init__(
        self,
        feed_manager: FeedManager,
        option_chain_manager: OptionChainManager,
        greeks_engine: GreeksEngine,
        portfolio_manager: PortfolioManager,
        execution_engine: ExecutionEngine,
        risk_manager: RiskManager,
        aggregators: Dict[str, SignalAggregator],
        session_manager: Optional[SessionManager] = None,
        email_service=None,
    ):
        self.feed_manager = feed_manager
        self.option_chain_manager = option_chain_manager
        self.greeks_engine = greeks_engine
        self.portfolio_manager = portfolio_manager
        self.execution_engine = execution_engine
        self.risk_manager = risk_manager
        self.aggregators = aggregators
        self.session_manager = session_manager
        self.email_service = email_service
        self._running = False
        self._tasks: List[asyncio.Task] = []

    async def start(self):
        """Starts the bot engine tasks."""
        if self._running:
            return

        self._running = True
        logger.info("Starting BotEngine main loops...")

        for instrument, aggregator in self.aggregators.items():
            task = asyncio.create_task(self.process_instrument(instrument, aggregator))
            self._tasks.append(task)

        if self.session_manager:
            refresh_task = asyncio.create_task(self._token_refresh_loop())
            self._tasks.append(refresh_task)

    async def _token_refresh_loop(self):
        """Periodically refreshes the AngelOne session token."""
        if not self.session_manager:
            return

        # Refresh token every 50 minutes (3000 seconds) to ensure it does not expire
        refresh_interval = 3000
        while self._running:
            await asyncio.sleep(refresh_interval)
            if not self._running:
                break

            try:
                logger.info("Triggering scheduled session token refresh.")
                await asyncio.to_thread(self.session_manager.refresh_session)
            except Exception as e:
                logger.error(
                    "Error during scheduled session refresh",
                    error=str(e),
                    exc_info=True,
                )
                if self.email_service:
                    error_msg = f"BotEngine session refresh error: {str(e)}"
                    asyncio.create_task(self.email_service.send_error_alert(error_msg))

    async def stop(self):
        """Stops the bot engine tasks."""
        self._running = False
        logger.info("Stopping BotEngine main loops...")
        for task in self._tasks:
            task.cancel()

        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    async def process_instrument(self, instrument: str, aggregator: SignalAggregator):
        """Main loop for a specific instrument (NIFTY/BANKNIFTY)."""
        queue = self.feed_manager.get_queue(instrument)

        try:
            while self._running:
                # We use a timeout to allow graceful shutdown checking
                try:
                    tick = await asyncio.wait_for(queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue

                try:
                    # Update option chain
                    self.option_chain_manager.update(instrument, tick)
                    snapshot = self.option_chain_manager.get_snapshot(instrument)

                    # For simplicity, passing static spot/expiry for now as the manager doesn't track it inherently yet.
                    spot = snapshot.get("spot", 0.0)
                    if spot > 0:
                        self.greeks_engine.refresh(
                            snapshot=snapshot.get("strikes", {}),
                            spot_price=spot,
                            time_to_expiry=7.0 / 365.0,  # dummy 7 days
                        )

                    # Update portfolio prices
                    token = tick.get("token")
                    ltp = tick.get("ltp")
                    if token and ltp:
                        self.portfolio_manager.update_prices({token: float(ltp)})

                    # Check exits
                    # We iterate over a copy of items to avoid runtime errors if positions are removed
                    positions_to_check = list(self.portfolio_manager.positions.values())
                    for pos_mgr in positions_to_check:
                        pos = pos_mgr.position
                        if instrument in pos.symbol:  # Basic check
                            # Check trailing SL / Target logic here.
                            # Since we don't have a check_exit implemented in pos_mgr yet, we mock basic SL/TP:
                            # If we hit SL/TP, trigger exit
                            # Check target/SL logic from original signal
                            pass

                    # Note: tick-level exit checking is usually delegated to PositionManager or Strategy.

                    # 1. Gather comprehensive snapshot.
                    # Dummy mapping for now since get_snapshot returns a dict
                    from backend.bot.models import MarketSnapshot

                    market_snapshot = MarketSnapshot(
                        symbol=instrument, token="INDEX", close=spot
                    )

                    signal = aggregator.process_snapshot(market_snapshot)
                    if signal:
                        approval = self.risk_manager.approve(
                            signal, self.portfolio_manager
                        )
                        if approval.ok:
                            lots = self.risk_manager.size(signal, lot_size=15)
                            if lots > 0:
                                order_id = await self.execution_engine.buy(
                                    signal=signal,
                                    lots=lots,
                                    exchange="NFO",
                                    variety="NORMAL",
                                    order_type="MARKET",
                                    product_type="INTRADAY",
                                    duration="DAY",
                                )
                                if order_id:
                                    # Create position
                                    new_pos = Position(
                                        symbol=signal.symbol,
                                        token=signal.token,
                                        side=signal.side,
                                        quantity=lots * 15,  # assuming 15 is lot size
                                        entry_price=signal.entry_price,
                                        current_price=signal.entry_price,
                                    )
                                    self.portfolio_manager.add_position(new_pos)
                                    logger.info("Opened new pos", position=new_pos)

                except Exception as e:
                    logger.error(
                        f"Error in {instrument}",
                        error=str(e),
                        exc_info=True,
                    )
                    if self.email_service:
                        error_msg = f"BotEngine error for {instrument}: {str(e)}"
                        asyncio.create_task(
                            self.email_service.send_error_alert(error_msg)
                        )

                    # Prevent tight loop on repeated errors
                    await asyncio.sleep(1)

        except asyncio.CancelledError:
            logger.info(f"Processing loop cancelled for {instrument}")
