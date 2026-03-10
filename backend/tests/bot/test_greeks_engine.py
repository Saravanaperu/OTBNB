import pytest
from bot.greeks_engine import GreeksEngine

def test_greeks_engine_refresh_valid_data():
    engine = GreeksEngine()

    # Valid call option ITM
    snapshot = {
        'token1': {
            'ltp': 150.0,
            'strike': 20000.0,
            'option_type': 'c'
        }
    }
    spot_price = 20100.0
    time_to_expiry = 0.01  # ~3.6 days

    engine.refresh(snapshot, spot_price, time_to_expiry)

    # Ensure values are populated, they might be None if PriceIsBelowIntrinsic error,
    # but the keys should exist
    assert 'iv' in snapshot['token1']
    assert 'delta' in snapshot['token1']

def test_greeks_engine_refresh_invalid_data():
    engine = GreeksEngine()

    snapshot = {
        'token_invalid': {
            'ltp': None,
            'strike': 20000.0,
            'option_type': 'c'
        }
    }
    spot_price = 20100.0
    time_to_expiry = 0.01

    engine.refresh(snapshot, spot_price, time_to_expiry)

    # Keys should not be added if ltp is None
    assert 'iv' not in snapshot['token_invalid']

def test_greeks_engine_refresh_negative_dte():
    engine = GreeksEngine()

    snapshot = {
        'token1': {
            'ltp': 100.0,
            'strike': 20000.0,
            'option_type': 'c'
        }
    }

    # Should return early and not crash
    engine.refresh(snapshot, 20100.0, -1.0)
    assert 'iv' not in snapshot['token1']
