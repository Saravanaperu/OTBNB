import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from backend.bot.bot_engine import BotEngine
from backend.bot.models import Signal


@pytest.fixture
def mock_dependencies():
    feed_manager = MagicMock()

    # We need an async queue mock
    queue = asyncio.Queue()
    queue.put_nowait(
        {"token": "100", "ltp": "50.5", "strike": "22000", "option_type": "ce"}
    )
    feed_manager.get_queue.return_value = queue

    option_chain_manager = MagicMock()
    option_chain_manager.get_snapshot.return_value = {"spot": 22000.0, "strikes": {}}

    greeks_engine = MagicMock()

    portfolio_manager = MagicMock()
    portfolio_manager.positions = {}

    execution_engine = AsyncMock()
    execution_engine.buy.return_value = "ORDER_123"

    risk_manager = MagicMock()
    risk_approval = MagicMock()
    risk_approval.ok = True
    risk_manager.approve.return_value = risk_approval
    risk_manager.size.return_value = 1

    aggregator = MagicMock()
    aggregator.process_snapshot.return_value = Signal(
        symbol="NIFTY22000CE",
        token="100",
        side="BUY",
        entry_price=50.5,
        stop_loss=40.0,
        target=60.0,
    )

    session_manager = MagicMock()

    email_service = AsyncMock()

    return {
        "feed_manager": feed_manager,
        "option_chain_manager": option_chain_manager,
        "greeks_engine": greeks_engine,
        "portfolio_manager": portfolio_manager,
        "execution_engine": execution_engine,
        "risk_manager": risk_manager,
        "aggregators": {"NIFTY": aggregator},
        "session_manager": session_manager,
        "email_service": email_service,
    }


@pytest.mark.asyncio
async def test_bot_engine_start_stop(mock_dependencies):
    engine = BotEngine(**mock_dependencies)

    assert engine._running is False
    assert len(engine._tasks) == 0

    await engine.start()

    assert engine._running is True
    # 1 aggregator task + 1 token refresh task
    assert len(engine._tasks) == 2

    # Let tasks run for a bit
    await asyncio.sleep(0.1)

    await engine.stop()

    assert engine._running is False
    assert len(engine._tasks) == 0


@pytest.mark.asyncio
async def test_bot_engine_process_instrument(mock_dependencies):
    # Setup the mock dependencies
    deps = mock_dependencies

    engine = BotEngine(**deps)

    async def side_effect(*args, **kwargs):
        engine._running = False
        return "ORDER_123"

    deps["execution_engine"].buy.side_effect = side_effect

    # We need to test the logic directly or run it briefly
    engine._running = True

    task = asyncio.create_task(
        engine.process_instrument("NIFTY", deps["aggregators"]["NIFTY"])
    )

    # Wait for completion or timeout
    try:
        await asyncio.wait_for(task, timeout=2.0)
    except asyncio.TimeoutError:
        engine._running = False
        await task

    deps["option_chain_manager"].update.assert_called_once()
    deps["greeks_engine"].refresh.assert_called_once()
    deps["portfolio_manager"].update_prices.assert_called_once_with({"100": 50.5})
    deps["aggregators"]["NIFTY"].process_snapshot.assert_called_once()
    deps["risk_manager"].approve.assert_called_once()
    deps["execution_engine"].buy.assert_called_once()
    deps["portfolio_manager"].add_position.assert_called_once()


@pytest.mark.asyncio
async def test_bot_engine_token_refresh_loop(mock_dependencies):
    deps = mock_dependencies
    engine = BotEngine(**deps)

    # Patch asyncio.sleep to break the loop after 1 iteration
    async def mock_sleep(interval):
        engine._running = False

    engine._running = True
    with patch("asyncio.sleep", new=mock_sleep):
        await engine._token_refresh_loop()

    # The session_manager.refresh_session should be called via to_thread
    # but since we exit immediately on sleep, we need a better mock strategy


@pytest.mark.asyncio
async def test_bot_engine_token_refresh_call(mock_dependencies):
    deps = mock_dependencies
    engine = BotEngine(**deps)
    engine._running = True

    calls = 0

    async def mock_sleep(interval):
        nonlocal calls
        calls += 1
        if calls > 0:
            pass  # allow it to proceed to to_thread then next iteration will stop it

    # We need to manually stop the loop after one execution of the body, which
    # happens after the try block, so we will use another side effect if needed,
    # or just let a side_effect on to_thread set running to False
    async def mock_to_thread(*args, **kwargs):
        engine._running = False
        return deps["session_manager"].refresh_session()

    with patch("asyncio.sleep", new=mock_sleep), patch(
        "asyncio.to_thread", side_effect=mock_to_thread
    ) as mock_thread:
        await engine._token_refresh_loop()

    mock_thread.assert_called_once_with(deps["session_manager"].refresh_session)


@pytest.mark.asyncio
async def test_process_instrument_timeout(mock_dependencies):
    deps = mock_dependencies

    # Replace queue with empty queue to trigger timeout
    empty_queue = asyncio.Queue()
    deps["feed_manager"].get_queue.return_value = empty_queue

    engine = BotEngine(**deps)
    engine._running = True

    async def cancel_later():
        await asyncio.sleep(1.5)
        engine._running = False

    asyncio.create_task(cancel_later())

    await engine.process_instrument("NIFTY", deps["aggregators"]["NIFTY"])

    # Should not process anything
    deps["option_chain_manager"].update.assert_not_called()


@pytest.mark.asyncio
async def test_process_instrument_exception(mock_dependencies):
    deps = mock_dependencies

    # Make option_chain_manager throw an error
    deps["option_chain_manager"].update.side_effect = Exception("Test Error")

    engine = BotEngine(**deps)
    engine._running = True

    async def cancel_later():
        await asyncio.sleep(0.5)
        engine._running = False

    asyncio.create_task(cancel_later())

    await engine.process_instrument("NIFTY", deps["aggregators"]["NIFTY"])

    # Assert email alert sent
    deps["email_service"].send_error_alert.assert_called_once()


@pytest.mark.asyncio
async def test_process_instrument_no_signal(mock_dependencies):
    deps = mock_dependencies
    deps["aggregators"]["NIFTY"].process_snapshot.return_value = None

    engine = BotEngine(**deps)
    engine._running = True

    async def cancel_later():
        await asyncio.sleep(0.5)
        engine._running = False

    asyncio.create_task(cancel_later())

    await engine.process_instrument("NIFTY", deps["aggregators"]["NIFTY"])

    deps["execution_engine"].buy.assert_not_called()


@pytest.mark.asyncio
async def test_process_instrument_risk_rejected(mock_dependencies):
    deps = mock_dependencies
    risk_approval = MagicMock()
    risk_approval.ok = False
    deps["risk_manager"].approve.return_value = risk_approval

    engine = BotEngine(**deps)
    engine._running = True

    async def cancel_later():
        await asyncio.sleep(0.5)
        engine._running = False

    asyncio.create_task(cancel_later())

    await engine.process_instrument("NIFTY", deps["aggregators"]["NIFTY"])

    deps["execution_engine"].buy.assert_not_called()


@pytest.mark.asyncio
async def test_token_refresh_exception(mock_dependencies):
    deps = mock_dependencies
    engine = BotEngine(**deps)
    engine._running = True

    async def mock_sleep(interval):
        pass  # allow it to proceed to to_thread

    def mock_to_thread(*args, **kwargs):
        engine._running = False
        raise Exception("Refresh Failed")

    with patch("asyncio.sleep", new=mock_sleep), patch(
        "asyncio.to_thread", side_effect=mock_to_thread
    ):
        await engine._token_refresh_loop()

    deps["email_service"].send_error_alert.assert_called_once()
