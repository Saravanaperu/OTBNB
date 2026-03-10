import asyncio
import structlog
from backend.config.logging_config import setup_logging
from backend.bot.option_chain_manager import OptionChainManager
from backend.bot.risk_manager import RiskManager
from backend.bot.portfolio_manager import PortfolioManager
from backend.bot.models import Position, Signal

setup_logging()
logger = structlog.get_logger()


class MockRegistry:
    pass


async def run_simulation():
    logger.info("Starting simulation...")

    registry = MockRegistry()
    chain_manager = OptionChainManager(registry)
    risk_manager = RiskManager(
        {"daily_loss_limit": 5000, "max_open_positions": 5, "risk_per_trade": 1000}
    )
    portfolio_manager = PortfolioManager()

    # Simulate ticks
    ticks = [
        {"token": "100", "ltp": 50.0, "strike": 22000, "option_type": "c"},
        {"token": "200", "ltp": 45.0, "strike": 22000, "option_type": "p"},
        {"token": "100", "ltp": 55.0, "strike": 22000, "option_type": "c"},
        {"token": "200", "ltp": 40.0, "strike": 22000, "option_type": "p"},
    ]

    for tick in ticks:
        logger.info("Processing tick", tick=tick)
        chain_manager.update("NIFTY", tick)
        await asyncio.sleep(0.1)

    # Simulate a signal and risk check
    signal = Signal(
        symbol="NIFTY22000CE",
        token="100",
        side="BUY",
        entry_price=55.0,
        stop_loss=40.0,
        target=85.0,
        strategy_name="SimStrategy",
    )

    logger.info("Evaluating signal", signal=signal)
    approval = risk_manager.approve(signal, portfolio_manager)

    if approval.ok:
        logger.info("Signal approved")
        size = risk_manager.size(signal, lot_size=15)
        logger.info("Calculated position size", quantity=size)

        # Open position
        pos = Position(
            symbol=signal.symbol,
            token=signal.token,
            side=signal.side,
            entry_price=signal.entry_price,
            current_price=signal.entry_price,
            quantity=size,
        )
        portfolio_manager.add_position(pos)
    else:
        logger.warning("Signal rejected", reason=approval.reason)

    logger.info(
        "Portfolio state",
        open_trades=portfolio_manager.get_open_trades_count(),
        mtm=portfolio_manager.get_total_mtm(),
    )

    # Simulate price update
    logger.info("Updating prices")
    portfolio_manager.update_prices({"100": 60.0})
    logger.info(
        "Portfolio state after update",
        open_trades=portfolio_manager.get_open_trades_count(),
        mtm=portfolio_manager.get_total_mtm(),
    )

    # Simulate exit
    logger.info("Exiting position")
    portfolio_manager.remove_position("100", 65.0)
    logger.info(
        "Final portfolio state",
        open_trades=portfolio_manager.get_open_trades_count(),
        mtm=portfolio_manager.get_total_mtm(),
    )

    logger.info("Simulation completed successfully.")


if __name__ == "__main__":
    asyncio.run(run_simulation())
