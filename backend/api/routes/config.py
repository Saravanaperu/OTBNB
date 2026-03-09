from fastapi import APIRouter
from typing import List
from backend.api.schemas import RiskConfig, StrategyConfig

router = APIRouter()

# Mock data
mock_risk_config = {
    "daily_hard_limit": 10000.0,
    "daily_soft_limit": 7000.0,
    "per_trade_risk": 2000.0,
    "max_open_positions": 4,
    "max_same_instrument": 2,
    "max_lots_per_trade": 3,
    "max_capital_pct": 0.15,
    "iv_rank_buy_threshold": 50.0,
    "min_delta": 0.20,
    "max_delta": 0.55,
    "max_theta_daily_pct": 3.0,
    "min_strike_volume": 500,
    "min_strike_oi": 10000,
    "max_bid_ask_spread_pct": 3.0,
    "no_trade_after": "15:20",
    "no_0dte_after": "13:00"
}

mock_strategies = [
    {
        "name": "momentum_breakout",
        "enabled": True,
        "instruments": ["NIFTY", "BANKNIFTY"],
        "params": {}
    }
]

@router.get("/risk", response_model=RiskConfig)
async def get_risk_config():
    """Current risk parameters"""
    return mock_risk_config

@router.put("/risk", response_model=RiskConfig)
async def update_risk_config(config: RiskConfig):
    """Update risk parameters at runtime (hot reload)"""
    global mock_risk_config
    mock_risk_config = config.dict()
    return mock_risk_config

@router.get("/strategies", response_model=List[StrategyConfig])
async def get_strategies():
    """Strategy list with enabled/disabled status"""
    return mock_strategies

@router.put("/strategies/{name}", response_model=StrategyConfig)
async def update_strategy(name: str, config: StrategyConfig):
    """Enable or disable a specific strategy at runtime"""
    for idx, strat in enumerate(mock_strategies):
        if strat["name"] == name:
            mock_strategies[idx] = config.dict()
            return config.dict()
    # Default if not found (ideally raise 404)
    return config.dict()
