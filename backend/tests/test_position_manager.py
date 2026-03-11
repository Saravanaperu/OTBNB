import pytest
from datetime import datetime
from backend.bot.models import Position
from backend.bot.position_manager import PositionManager


@pytest.fixture
def long_position():
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
def short_position():
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


def test_initialization(long_position):
    pm = PositionManager(long_position)
    assert pm.position == long_position
    assert pm.get_unrealized_pnl() == 0.0


def test_update_price_long(long_position):
    pm = PositionManager(long_position)

    # Price increases, profit
    pm.update_price(110.0)
    assert pm.position.current_price == 110.0
    assert pm.get_unrealized_pnl() == 500.0  # (110 - 100) * 50

    # Price decreases, loss
    pm.update_price(90.0)
    assert pm.position.current_price == 90.0
    assert pm.get_unrealized_pnl() == -500.0  # (90 - 100) * 50


def test_update_price_short(short_position):
    pm = PositionManager(short_position)

    # Price increases, loss
    pm.update_price(110.0)
    assert pm.position.current_price == 110.0
    assert pm.get_unrealized_pnl() == -500.0  # (100 - 110) * 50

    # Price decreases, profit
    pm.update_price(90.0)
    assert pm.position.current_price == 90.0
    assert pm.get_unrealized_pnl() == 500.0  # (100 - 90) * 50


def test_close_position_long(long_position):
    pm = PositionManager(long_position)

    realized_pnl = pm.close_position(120.0)
    assert realized_pnl == 1000.0  # (120 - 100) * 50
    assert pm.position.current_price == 120.0
    assert pm.get_unrealized_pnl() == 1000.0


def test_close_position_short(short_position):
    pm = PositionManager(short_position)

    realized_pnl = pm.close_position(80.0)
    assert realized_pnl == 1000.0  # (100 - 80) * 50
    assert pm.position.current_price == 80.0
    assert pm.get_unrealized_pnl() == 1000.0
