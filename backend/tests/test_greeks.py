from unittest.mock import patch

from backend.bot.greeks_engine import GreeksEngine
from py_vollib.black_scholes.implied_volatility import PriceIsBelowIntrinsic


def test_greeks_engine_refresh():
    engine = GreeksEngine()

    snapshot = {
        "12345": {"token": "12345", "ltp": 150.0, "strike": 22000, "option_type": "c"},
        "67890": {"token": "67890", "ltp": 120.0, "strike": 22000, "option_type": "p"},
    }

    # Current spot 22000, 10 days to expiry (10/365 approx 0.0274)
    spot_price = 22000.0
    time_to_expiry = 10.0 / 365.0

    engine.refresh(snapshot, spot_price, time_to_expiry)

    ce_opt = snapshot["12345"]
    assert "iv" in ce_opt
    assert "delta" in ce_opt
    assert "gamma" in ce_opt
    assert "theta" in ce_opt
    assert "vega" in ce_opt

    assert ce_opt["iv"] is not None
    assert ce_opt["delta"] is not None
    assert ce_opt["gamma"] is not None
    assert ce_opt["theta"] is not None
    assert ce_opt["vega"] is not None

    pe_opt = snapshot["67890"]
    assert "iv" in pe_opt
    assert "delta" in pe_opt
    assert "gamma" in pe_opt
    assert "theta" in pe_opt
    assert "vega" in pe_opt

    assert pe_opt["iv"] is not None
    assert pe_opt["delta"] is not None
    assert pe_opt["gamma"] is not None
    assert pe_opt["theta"] is not None
    assert pe_opt["vega"] is not None


def test_greeks_engine_zero_dte():
    engine = GreeksEngine()
    snapshot = {
        "12345": {"token": "12345", "ltp": 150.0, "strike": 22000, "option_type": "c"}
    }

    engine.refresh(snapshot, 22000.0, 0.0)

    assert "iv" not in snapshot["12345"]


def test_greeks_engine_invalid_data():
    engine = GreeksEngine()
    snapshot = {
        "12345": {"token": "12345", "ltp": None, "strike": 22000, "option_type": "c"}
    }

    engine.refresh(snapshot, 22000.0, 0.05)

    assert "iv" not in snapshot["12345"]


def test_greeks_engine_invalid_flag():
    engine = GreeksEngine()
    snapshot = {
        "12345": {"token": "12345", "ltp": 150.0, "strike": 22000, "option_type": "x"}
    }

    engine.refresh(snapshot, 22000.0, 0.05)

    assert "iv" not in snapshot["12345"]


@patch("py_vollib.black_scholes.implied_volatility.implied_volatility")
def test_greeks_engine_price_below_intrinsic(mock_iv):
    mock_iv.side_effect = PriceIsBelowIntrinsic()

    engine = GreeksEngine()
    snapshot = {
        "12345": {"token": "12345", "ltp": 1.0, "strike": 20000, "option_type": "c"}
    }

    engine.refresh(snapshot, 22000.0, 0.05)

    assert snapshot["12345"]["iv"] is None
    assert snapshot["12345"]["delta"] is None
    assert snapshot["12345"]["gamma"] is None
    assert snapshot["12345"]["theta"] is None
    assert snapshot["12345"]["vega"] is None


@patch("py_vollib.black_scholes.implied_volatility.implied_volatility")
def test_greeks_engine_generic_exception(mock_iv):
    mock_iv.side_effect = Exception("Generic error")

    engine = GreeksEngine()
    snapshot = {
        "12345": {"token": "12345", "ltp": 150.0, "strike": 22000, "option_type": "c"}
    }

    engine.refresh(snapshot, 22000.0, 0.05)

    assert snapshot["12345"]["iv"] is None
    assert snapshot["12345"]["delta"] is None
    assert snapshot["12345"]["gamma"] is None
    assert snapshot["12345"]["theta"] is None
    assert snapshot["12345"]["vega"] is None
