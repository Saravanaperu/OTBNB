import pytest
from unittest.mock import MagicMock, patch
from backend.bot.execution_engine import ExecutionEngine
from backend.bot.models import Signal, Position, ExitSignal


@pytest.fixture
def mock_session_manager():
    manager = MagicMock()
    manager.is_connected = True
    manager.api = MagicMock()
    return manager


@pytest.fixture
def signal():
    return Signal(
        symbol="NIFTY22000CE",
        token="100",
        side="BUY",
        entry_price=55.0,
        stop_loss=40.0,
        target=85.0,
    )


@pytest.fixture
def position():
    return Position(
        symbol="NIFTY22000CE",
        token="100",
        side="BUY",
        quantity=15,
        entry_price=55.0,
        current_price=55.0,
    )


@pytest.fixture
def exit_signal():
    return ExitSignal(symbol="NIFTY22000CE", token="100", reason="Target Reached")


@pytest.mark.asyncio
async def test_buy_successful(mock_session_manager, signal):
    mock_session_manager.api.placeOrder.return_value = "ORDER_123"
    engine = ExecutionEngine(mock_session_manager)

    order_id = await engine.buy(
        signal=signal,
        lots=1,
        exchange="NFO",
        variety="NORMAL",
        order_type="MARKET",
        product_type="INTRADAY",
        duration="DAY",
    )

    assert order_id == "ORDER_123"
    mock_session_manager.api.placeOrder.assert_called_once()
    args, kwargs = mock_session_manager.api.placeOrder.call_args
    assert args[0]["transactiontype"] == "BUY"
    assert args[0]["quantity"] == "1"


@pytest.mark.asyncio
async def test_buy_not_connected(mock_session_manager, signal):
    mock_session_manager.is_connected = False
    engine = ExecutionEngine(mock_session_manager)

    order_id = await engine.buy(
        signal=signal,
        lots=1,
        exchange="NFO",
        variety="NORMAL",
        order_type="MARKET",
        product_type="INTRADAY",
        duration="DAY",
    )

    assert order_id is None
    mock_session_manager.api.placeOrder.assert_not_called()


@pytest.mark.asyncio
async def test_buy_retry_success(mock_session_manager, signal):
    # Fails first time, succeeds second time
    mock_session_manager.api.placeOrder.side_effect = [None, "ORDER_123"]
    engine = ExecutionEngine(mock_session_manager)

    with patch("asyncio.sleep", return_value=None):
        order_id = await engine.buy(
            signal=signal,
            lots=1,
            exchange="NFO",
            variety="NORMAL",
            order_type="MARKET",
            product_type="INTRADAY",
            duration="DAY",
        )

    assert order_id == "ORDER_123"
    assert mock_session_manager.api.placeOrder.call_count == 2


@pytest.mark.asyncio
async def test_buy_all_retries_fail(mock_session_manager, signal):
    # Fails all times
    mock_session_manager.api.placeOrder.side_effect = Exception("API Error")
    engine = ExecutionEngine(mock_session_manager)

    with patch("asyncio.sleep", return_value=None):
        order_id = await engine.buy(
            signal=signal,
            lots=1,
            exchange="NFO",
            variety="NORMAL",
            order_type="MARKET",
            product_type="INTRADAY",
            duration="DAY",
        )

    assert order_id is None
    assert mock_session_manager.api.placeOrder.call_count == 3


@pytest.mark.asyncio
async def test_exit_successful(mock_session_manager, position, exit_signal):
    mock_session_manager.api.placeOrder.return_value = "ORDER_456"
    engine = ExecutionEngine(mock_session_manager)

    order_id = await engine.exit(
        position=position,
        exit_signal=exit_signal,
        exchange="NFO",
        variety="NORMAL",
        order_type="MARKET",
        product_type="INTRADAY",
        duration="DAY",
    )

    assert order_id == "ORDER_456"
    mock_session_manager.api.placeOrder.assert_called_once()
    args, kwargs = mock_session_manager.api.placeOrder.call_args
    # It was a BUY position, so exit should be SELL
    assert args[0]["transactiontype"] == "SELL"
    assert args[0]["quantity"] == "15"


@pytest.mark.asyncio
async def test_exit_not_connected(mock_session_manager, position, exit_signal):
    mock_session_manager.is_connected = False
    engine = ExecutionEngine(mock_session_manager)

    order_id = await engine.exit(
        position=position,
        exit_signal=exit_signal,
        exchange="NFO",
        variety="NORMAL",
        order_type="MARKET",
        product_type="INTRADAY",
        duration="DAY",
    )

    assert order_id is None
    mock_session_manager.api.placeOrder.assert_not_called()


@pytest.mark.asyncio
async def test_exit_retry_success(mock_session_manager, position, exit_signal):
    mock_session_manager.api.placeOrder.side_effect = [
        None,
        Exception("API Error"),
        "ORDER_456",
    ]
    engine = ExecutionEngine(mock_session_manager)

    with patch("asyncio.sleep", return_value=None):
        order_id = await engine.exit(
            position=position,
            exit_signal=exit_signal,
            exchange="NFO",
            variety="NORMAL",
            order_type="MARKET",
            product_type="INTRADAY",
            duration="DAY",
        )

    assert order_id == "ORDER_456"
    assert mock_session_manager.api.placeOrder.call_count == 3


@pytest.mark.asyncio
async def test_exit_all_retries_fail(mock_session_manager, position, exit_signal):
    mock_session_manager.api.placeOrder.side_effect = Exception("API Error")
    engine = ExecutionEngine(mock_session_manager)

    with patch("asyncio.sleep", return_value=None):
        order_id = await engine.exit(
            position=position,
            exit_signal=exit_signal,
            exchange="NFO",
            variety="NORMAL",
            order_type="MARKET",
            product_type="INTRADAY",
            duration="DAY",
        )

    assert order_id is None
    assert mock_session_manager.api.placeOrder.call_count == 3
