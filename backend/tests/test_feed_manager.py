import pytest
from unittest.mock import MagicMock
from backend.bot.feed_manager import FeedManager
from SmartApi.smartWebSocketV2 import SmartWebSocketV2


@pytest.fixture
def mock_session_manager():
    sm = MagicMock()
    sm.is_connected = True
    sm.jwt_token = "jwt"
    sm.api_key = "api_key"
    sm.client_code = "client_code"
    sm.feed_token = "feed_token"
    return sm


@pytest.fixture
def mock_registry():
    reg = MagicMock()
    reg.master_data = [
        {"token": "100", "exch_seg": "NSE"},
        {"token": "200", "exch_seg": "NFO"},
        {"token": "300", "exch_seg": "BSE"},
        {"token": "", "exch_seg": "NSE"},
        {"token": "400", "exch_seg": ""},
    ]
    return reg


@pytest.mark.asyncio
async def test_subscribe_all_tokens_success(mock_session_manager, mock_registry):
    fm = FeedManager(mock_session_manager)
    fm.is_connected = True
    fm.sws = MagicMock()

    await fm.subscribe_all_tokens(mock_registry)

    fm.sws.subscribe.assert_called_once()
    args, kwargs = fm.sws.subscribe.call_args
    assert kwargs["correlation_id"] == "init_sub"
    assert kwargs["mode"] == SmartWebSocketV2.SNAP_QUOTE

    expected_token_list = [
        {"exchangeType": 1, "tokens": ["100"]},
        {"exchangeType": 2, "tokens": ["200"]},
    ]
    assert kwargs["token_list"] == expected_token_list


@pytest.mark.asyncio
async def test_subscribe_all_tokens_not_connected(mock_session_manager, mock_registry):
    fm = FeedManager(mock_session_manager)
    fm.is_connected = False
    fm.sws = MagicMock()

    await fm.subscribe_all_tokens(mock_registry)
    fm.sws.subscribe.assert_not_called()


@pytest.mark.asyncio
async def test_subscribe_all_tokens_no_tokens(mock_session_manager):
    fm = FeedManager(mock_session_manager)
    fm.is_connected = True
    fm.sws = MagicMock()

    mock_registry = MagicMock()
    mock_registry.master_data = []

    await fm.subscribe_all_tokens(mock_registry)
    fm.sws.subscribe.assert_not_called()


@pytest.mark.asyncio
async def test_subscribe_all_tokens_exception(mock_session_manager, mock_registry):
    fm = FeedManager(mock_session_manager)
    fm.is_connected = True
    fm.sws = MagicMock()
    fm.sws.subscribe.side_effect = Exception("Test exception")

    # Should handle the exception gracefully without raising
    await fm.subscribe_all_tokens(mock_registry)
    fm.sws.subscribe.assert_called_once()
