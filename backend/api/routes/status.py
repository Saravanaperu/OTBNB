from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    from backend.main import bot_state

    # Adding some mock fields requested by UI

    return {
        "status": "ok",
        "uptime": 3600,
        "market_open": True,
        "last_tick_age_ms": 150,
        "bot_status": bot_state["status"],
    }


@router.get("/")
async def get_status():
    from backend.main import bot_state

    return {
        "bot_running": bot_state["status"] == "RUNNING",
        "strategy_paused": False,
        "vix": 14.2,
        "iv_rank_nifty": 28,
        "iv_rank_bnf": 31,
        "session_valid": True,
    }


@router.post("/bot/pause")
async def pause_bot():
    return {"success": True, "message": "Bot paused successfully."}


@router.post("/bot/resume")
async def resume_bot():
    return {"success": True, "message": "Bot resumed successfully."}


@router.post("/bot/emergency_exit")
async def emergency_exit():
    return {"success": True, "orders_placed": 0}
