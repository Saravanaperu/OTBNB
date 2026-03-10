import asyncio
import logging
from bot.feed_manager import FeedManager
from bot.session_manager import SessionManager
from bot.option_chain_manager import OptionChainManager
from bot.instrument_registry import InstrumentRegistry
from bot.greeks_engine import GreeksEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def simulate_bot():
    logger.info("Starting simulation...")

    # In a real environment, you'd load real credentials and start the real components.
    # Here, we can create mock instances or rely on the actual instances and feed them simulated data.
    registry = InstrumentRegistry()
    registry.instruments = {
        '12345': {'name': 'NIFTY', 'token': '12345', 'exch_seg': 'NFO', 'symbol': 'NIFTY24DEC20000CE', 'strike': '20000.0', 'instrumenttype': 'OPTIDX'},
        '67890': {'name': 'BANKNIFTY', 'token': '67890', 'exch_seg': 'NFO', 'symbol': 'BANKNIFTY24DEC45000CE', 'strike': '45000.0', 'instrumenttype': 'OPTIDX'}
    }

    chain_manager = OptionChainManager(registry)

    # Simulate a tick
    logger.info("Simulating incoming ticks...")
    tick1 = {
        'token': '12345',
        'last_traded_price': 150.50,
        'volume_trade_for_the_day': 10000,
        'open_interest': 5000
    }

    # Simulate feed manager processing tick
    chain_manager.update("NIFTY", tick1)

    snapshot = chain_manager.get_snapshot("NIFTY")
    logger.info(f"Snapshot after tick 1: {snapshot}")

    logger.info("Simulation completed successfully.")

if __name__ == "__main__":
    asyncio.run(simulate_bot())
