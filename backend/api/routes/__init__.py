from fastapi import APIRouter
from backend.api.routes import status, positions, pnl, trades, market, config

api_router = APIRouter()

api_router.include_router(status.router, prefix="/status", tags=["Status"])
api_router.include_router(positions.router, prefix="/positions", tags=["Positions"])
api_router.include_router(pnl.router, prefix="/pnl", tags=["PnL"])
api_router.include_router(trades.router, prefix="/trades", tags=["Trades"])
api_router.include_router(market.router, tags=["Market"])
api_router.include_router(config.router, prefix="/config", tags=["Config"])
