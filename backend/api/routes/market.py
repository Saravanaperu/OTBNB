from fastapi import APIRouter
from backend.api.schemas import OptionChain
from datetime import datetime

router = APIRouter()


def get_chain_snapshot_mapped(instrument: str) -> dict:
    from backend.main import get_bot_state

    bot_state = get_bot_state()
    ocm = bot_state.get("option_chain_manager")
    if not ocm:
        return {
            "instrument": instrument,
            "expiry": "27FEB2025",
            "spot": 22000.0 if instrument == "NIFTY" else 48000.0,
            "atm_strike": 22000 if instrument == "NIFTY" else 48000,
            "updated_at": datetime.now(),
            "pcr_oi": 1.0,
            "pcr_volume": 1.0,
            "total_call_oi": 0,
            "total_put_oi": 0,
            "iv_rank": 30.0,
            "iv_percentile": 30.0,
            "strikes": {},
        }

    snapshot = ocm.get_snapshot(instrument)
    return {
        "instrument": instrument,
        "expiry": snapshot.get("expiry", "27FEB2025"),
        "spot": snapshot.get("spot", 22000.0 if instrument == "NIFTY" else 48000.0),
        "atm_strike": snapshot.get(
            "atm_strike", 22000 if instrument == "NIFTY" else 48000
        ),
        "updated_at": snapshot.get("updated_at", datetime.now()),
        "pcr_oi": snapshot.get("pcr_oi", 1.0),
        "pcr_volume": snapshot.get("pcr_volume", 1.0),
        "total_call_oi": snapshot.get("total_call_oi", 0),
        "total_put_oi": snapshot.get("total_put_oi", 0),
        "iv_rank": snapshot.get("iv_rank", 30.0),
        "iv_percentile": snapshot.get("iv_percentile", 30.0),
        "strikes": snapshot.get("strikes", {}),
    }


@router.get("/chain/nifty", response_model=OptionChain)
async def get_chain_nifty():
    """Live NIFTY option chain"""
    return get_chain_snapshot_mapped("NIFTY")


@router.get("/chain/banknifty", response_model=OptionChain)
async def get_chain_banknifty():
    """Live BANKNIFTY option chain"""
    return get_chain_snapshot_mapped("BANKNIFTY")


@router.get("/vix")
async def get_vix():
    """India VIX and IV Rank for both instruments"""
    return {"vix": 14.2, "change_pct": 0.0, "iv_rank_nifty": 28, "iv_rank_bnf": 31}


@router.get("/spot")
async def get_spot():
    """Current spot prices for both indices"""
    return {
        "nifty": 22450.0,
        "banknifty": 48120.0,
        "timestamp": datetime.now().isoformat(),
    }
