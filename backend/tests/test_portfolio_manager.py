import pytest
from datetime import datetime
from unittest.mock import patch
from backend.bot.models import Position
from backend.bot.portfolio_manager import PortfolioManager


@pytest.fixture
def sample_position1():
    return Position(
        id="pos_1",
        token="12345",
        symbol="NIFTY24JUN20000CE",
        side="BUY",
        quantity=50,
        entry_price=100.0,
        current_price=100.0,
        unrealized_pnl=0.0,
        entry_time=datetime.now(),
    )


@pytest.fixture
def sample_position2():
    return Position(
        id="pos_2",
        token="67890",
        symbol="NIFTY24JUN20000PE",
        side="SELL",
        quantity=50,
        entry_price=100.0,
        current_price=100.0,
        unrealized_pnl=0.0,
        entry_time=datetime.now(),
    )


def test_initialization():
    pm = PortfolioManager()
    assert pm.positions == {}
    assert pm.realized_pnl == 0.0
    assert pm.get_open_trades_count() == 0
    assert pm.get_total_mtm() == 0.0


def test_add_position(sample_position1):
    pm = PortfolioManager()
    pm.add_position(sample_position1)

    assert "12345" in pm.positions
    assert pm.get_open_trades_count() == 1
    assert pm.positions["12345"].position == sample_position1


@patch("backend.bot.portfolio_manager.logger.warning")
def test_add_existing_position(mock_logger_warning, sample_position1):
    pm = PortfolioManager()
    pm.add_position(sample_position1)

    # Try adding the same token again
    pm.add_position(sample_position1)

    assert pm.get_open_trades_count() == 1
    mock_logger_warning.assert_called_once()
    assert "already exists" in mock_logger_warning.call_args[0][0]


def test_remove_position(sample_position1):
    pm = PortfolioManager()
    pm.add_position(sample_position1)

    # remove pos_1, it's a BUY at 100, we exit at 120 (profit of 20 * 50 = 1000)
    pm.remove_position("12345", 120.0)

    assert "12345" not in pm.positions
    assert pm.get_open_trades_count() == 0
    assert pm.realized_pnl == 1000.0


def test_remove_nonexistent_position():
    pm = PortfolioManager()
    pm.remove_position("99999", 100.0)

    # Should not crash, and realized PNL should remain 0
    assert pm.realized_pnl == 0.0


def test_update_prices(sample_position1, sample_position2):
    pm = PortfolioManager()
    pm.add_position(sample_position1)
    pm.add_position(sample_position2)

    # sample1 is BUY @ 100. We update to 110. Unrealized = +500.
    # sample2 is SELL @ 100. We update to 90. Unrealized = +500.
    updates = {
        "12345": 110.0,
        "67890": 90.0,
        "99999": 150.0,  # Non-existent, should be ignored
    }

    pm.update_prices(updates)

    assert pm.positions["12345"].position.current_price == 110.0
    assert pm.positions["12345"].get_unrealized_pnl() == 500.0

    assert pm.positions["67890"].position.current_price == 90.0
    assert pm.positions["67890"].get_unrealized_pnl() == 500.0

    assert pm.get_total_mtm() == 1000.0


def test_get_total_mtm_mixed(sample_position1, sample_position2):
    pm = PortfolioManager()
    pm.add_position(sample_position1)
    pm.add_position(sample_position2)

    # Initial MTM should be 0
    assert pm.get_total_mtm() == 0.0

    # Close position 1 with profit
    pm.remove_position("12345", 120.0)  # Realized = +1000

    # Update position 2 to a loss
    pm.update_prices({"67890": 110.0})  # Unrealized = -500

    # Total MTM = 1000 (realized) - 500 (unrealized) = 500
    assert pm.get_total_mtm() == 500.0

    # Open trades count should be 1
    assert pm.get_open_trades_count() == 1
