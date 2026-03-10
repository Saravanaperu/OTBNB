from fastapi import APIRouter
from api.schemas import OptionChain
from datetime import datetime

router = APIRouter()

# Mock function for option chain, usually fetching from OptionChainManager
def get_mock_chain(instrument: str) -> dict:
    return {
        "instrument": instrument,
        "expiry": "27FEB2025",
        "spot": 22000.0,
        "atm_strike": 22000,
        "updated_at": datetime.now(),
        "pcr_oi": 1.0,
        "pcr_volume": 1.0,
        "total_call_oi": 0,
        "total_put_oi": 0,
        "iv_rank": 30.0,
        "iv_percentile": 30.0,
        "strikes": {}
    }

@router.get("/chain/nifty", response_model=OptionChain)
async def get_chain_nifty():
    """Live NIFTY option chain"""
    return get_mock_chain("NIFTY")

@router.get("/chain/banknifty", response_model=OptionChain)
async def get_chain_banknifty():
    """Live BANKNIFTY option chain"""
    return get_mock_chain("BANKNIFTY")

@router.get("/vix")
async def get_vix():
    """India VIX and IV Rank for both instruments"""
    return {
        "vix": 14.2,
        "change_pct": 0.0,
        "iv_rank_nifty": 28,
        "iv_rank_bnf": 31
    }

@router.get("/spot")
async def get_spot():
    """Current spot prices for both indices"""
    return {
        "nifty": 22450.0,
        "banknifty": 48120.0,
        "timestamp": datetime.now().isoformat()
    }
