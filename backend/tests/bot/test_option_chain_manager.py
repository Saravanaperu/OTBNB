import pytest
from bot.option_chain_manager import OptionChainManager

class MockRegistry:
    pass

def test_option_chain_manager_update_and_get():
    registry = MockRegistry()
    manager = OptionChainManager(registry)

    tick = {
        'token': '12345',
        'ltp': 150.5,
        'volume': 1000
    }

    manager.update("NIFTY", tick)

    snapshot = manager.get_snapshot("NIFTY")
    assert "12345" in snapshot
    assert snapshot["12345"]["ltp"] == 150.5

    # Second tick updates the same token
    tick2 = {
        'token': '12345',
        'ltp': 152.0,
        'oi': 500
    }

    manager.update("NIFTY", tick2)
    snapshot = manager.get_snapshot("NIFTY")

    # Verify update merges data
    assert snapshot["12345"]["ltp"] == 152.0
    assert snapshot["12345"]["volume"] == 1000  # From previous tick
    assert snapshot["12345"]["oi"] == 500       # New field

def test_option_chain_manager_missing_token():
    registry = MockRegistry()
    manager = OptionChainManager(registry)

    tick = {
        'ltp': 150.5
    }

    manager.update("NIFTY", tick)

    snapshot = manager.get_snapshot("NIFTY")
    assert snapshot == {}  # No update should happen without a token

def test_option_chain_manager_empty_snapshot():
    registry = MockRegistry()
    manager = OptionChainManager(registry)

    snapshot = manager.get_snapshot("BANKNIFTY")
    assert snapshot == {}
