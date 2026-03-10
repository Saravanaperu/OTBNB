from unittest.mock import MagicMock
from backend.bot.option_chain_manager import OptionChainManager


def test_option_chain_manager_update():
    mock_registry = MagicMock()
    manager = OptionChainManager(mock_registry)

    tick1 = {"token": "100", "ltp": 50.5}
    tick2 = {"token": "100", "volume": 1000}
    tick3 = {"token": "200", "ltp": 60.0}

    manager.update("NIFTY", tick1)
    manager.update("NIFTY", tick2)
    manager.update("NIFTY", tick3)

    snapshot = manager.get_snapshot("NIFTY")

    assert "100" in snapshot
    assert "200" in snapshot

    assert snapshot["100"]["ltp"] == 50.5
    assert snapshot["100"]["volume"] == 1000
    assert snapshot["200"]["ltp"] == 60.0


def test_option_chain_manager_update_no_token():
    mock_registry = MagicMock()
    manager = OptionChainManager(mock_registry)

    tick = {"ltp": 50.5}

    manager.update("NIFTY", tick)

    snapshot = manager.get_snapshot("NIFTY")

    assert len(snapshot) == 0


def test_option_chain_manager_get_snapshot_empty():
    mock_registry = MagicMock()
    manager = OptionChainManager(mock_registry)

    snapshot = manager.get_snapshot("NIFTY")

    assert snapshot == {}


def test_option_chain_manager_update_existing_token():
    mock_registry = MagicMock()
    manager = OptionChainManager(mock_registry)

    tick1 = {"token": "100", "ltp": 50.5}
    tick2 = {"token": "100", "ltp": 55.0, "volume": 2000}

    manager.update("NIFTY", tick1)
    manager.update("NIFTY", tick2)

    snapshot = manager.get_snapshot("NIFTY")

    assert "100" in snapshot
    assert snapshot["100"]["ltp"] == 55.0
    assert snapshot["100"]["volume"] == 2000
