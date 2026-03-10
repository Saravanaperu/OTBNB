from unittest.mock import MagicMock
from backend.bot.risk_manager import RiskManager


def test_risk_manager_approve_success():
    rm = RiskManager(config={"daily_loss_limit": 5000, "max_open_positions": 5})

    mock_portfolio = MagicMock()
    mock_portfolio.get_total_mtm.return_value = 1000  # positive pnl
    mock_portfolio.get_open_trades_count.return_value = 2

    mock_signal = MagicMock()

    approval = rm.approve(mock_signal, mock_portfolio)
    assert approval.ok is True


def test_risk_manager_approve_loss_limit_breached():
    rm = RiskManager(config={"daily_loss_limit": 5000, "max_open_positions": 5})

    mock_portfolio = MagicMock()
    mock_portfolio.get_total_mtm.return_value = -6000  # breached
    mock_portfolio.get_open_trades_count.return_value = 2

    mock_signal = MagicMock()

    approval = rm.approve(mock_signal, mock_portfolio)
    assert approval.ok is False
    assert "loss limit breached" in approval.reason


def test_risk_manager_approve_max_trades_breached():
    rm = RiskManager(config={"daily_loss_limit": 5000, "max_open_positions": 5})

    mock_portfolio = MagicMock()
    mock_portfolio.get_total_mtm.return_value = -1000
    mock_portfolio.get_open_trades_count.return_value = 5  # reached max

    mock_signal = MagicMock()

    approval = rm.approve(mock_signal, mock_portfolio)
    assert approval.ok is False
    assert "Max open positions reached" in approval.reason


def test_risk_manager_size():
    rm = RiskManager(config={"risk_per_trade": 1000})

    mock_signal = MagicMock()
    mock_signal.entry_price = 100
    mock_signal.stop_loss = 80

    # risk per unit = 20
    # max units = 1000 / 20 = 50
    # lot size = 15
    # lots = int(50 / 15) = 3
    # return lots * lot_size = 3 * 15 = 45

    size = rm.size(mock_signal, 15)
    assert size == 45


def test_risk_manager_size_minimum():
    rm = RiskManager(config={"risk_per_trade": 1000})

    mock_signal = MagicMock()
    mock_signal.entry_price = 100
    mock_signal.stop_loss = 10

    # risk per unit = 90
    # max units = 1000 / 90 = 11.1
    # lot size = 15
    # lots = int(11.1 / 15) = 0 => forced to 1
    # return 1 * 15 = 15

    size = rm.size(mock_signal, 15)
    assert size == 15


def test_risk_manager_size_zero_risk():
    rm = RiskManager(config={"risk_per_trade": 1000})

    mock_signal = MagicMock()
    mock_signal.entry_price = 100
    mock_signal.stop_loss = 100

    size = rm.size(mock_signal, 15)
    assert size == 15
