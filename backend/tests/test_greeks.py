import pytest
from backend.bot.greeks_engine import GreeksEngine


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
