import pytest
from bot.risk_manager import RiskManager
from bot.models import Signal, Position
from bot.portfolio_manager import PortfolioManager

@pytest.fixture
def risk_manager():
    config = {
        'daily_loss_limit': 5000,
        'max_open_positions': 2,
        'risk_per_trade': 1000
    }
    return RiskManager(config)

@pytest.fixture
def portfolio():
    return PortfolioManager()

def test_approve_daily_loss_breached(risk_manager, portfolio):
    # Setup portfolio to have -5100 MTM
    pos = Position(
        symbol="NIFTY", token="123", side="BUY", quantity=50,
        entry_price=100, current_price=100
    )
    portfolio.add_position(pos)
    portfolio.update_prices({"123": -2}) # Drop price by 102 so unrealized is -5100

    signal = Signal(
        symbol="BANKNIFTY", token="456", side="BUY",
        entry_price=100, stop_loss=80, target=150
    )

    approval = risk_manager.approve(signal, portfolio)
    assert approval.ok is False
    assert approval.reason == "Daily loss limit breached"

def test_approve_max_positions_reached(risk_manager, portfolio):
    pos1 = Position(
        symbol="NIFTY1", token="123", side="BUY", quantity=50,
        entry_price=100, current_price=100
    )
    pos2 = Position(
        symbol="NIFTY2", token="456", side="BUY", quantity=50,
        entry_price=100, current_price=100
    )
    portfolio.add_position(pos1)
    portfolio.add_position(pos2)

    signal = Signal(
        symbol="BANKNIFTY", token="789", side="BUY",
        entry_price=100, stop_loss=80, target=150
    )

    approval = risk_manager.approve(signal, portfolio)
    assert approval.ok is False
    assert approval.reason == "Max open positions reached"

def test_approve_success(risk_manager, portfolio):
    signal = Signal(
        symbol="BANKNIFTY", token="789", side="BUY",
        entry_price=100, stop_loss=80, target=150
    )

    approval = risk_manager.approve(signal, portfolio)
    assert approval.ok is True

def test_size_normal_calculation(risk_manager):
    signal = Signal(
        symbol="BANKNIFTY", token="789", side="BUY",
        entry_price=100, stop_loss=80, target=150
    )

    # Risk per unit = 20
    # Max units = 1000 / 20 = 50
    # lot_size = 15
    # lots = int(50 / 15) = 3
    # final quantity = 3 * 15 = 45
    qty = risk_manager.size(signal, 15)
    assert qty == 45

def test_size_min_lots(risk_manager):
    signal = Signal(
        symbol="BANKNIFTY", token="789", side="BUY",
        entry_price=100, stop_loss=50, target=150
    )

    # Risk per unit = 50
    # Max units = 1000 / 50 = 20
    # lot_size = 25
    # lots = int(20 / 25) = 0 -> max(1, 0) = 1
    # final quantity = 1 * 25 = 25
    qty = risk_manager.size(signal, 25)
    assert qty == 25

def test_size_zero_risk_diff(risk_manager):
    signal = Signal(
        symbol="BANKNIFTY", token="789", side="BUY",
        entry_price=100, stop_loss=100, target=150
    )

    qty = risk_manager.size(signal, 15)
    assert qty == 15
