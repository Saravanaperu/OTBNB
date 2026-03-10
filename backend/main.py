from typing import Dict, Any
from contextlib import asynccontextmanager
import asyncio
import datetime
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.config.settings import settings
from backend.config.logging_config import setup_logging
from backend.bot.session_manager import SessionManager
from backend.api.routes import api_router
from backend.api.websocket import router as ws_router
from backend.storage.database import init_db
from backend.alerts.email_service import EmailService
from backend.alerts.email_templates import get_template
from backend.bot.portfolio_manager import PortfolioManager
from backend.bot.instrument_registry import InstrumentRegistry
from backend.bot.option_chain_manager import OptionChainManager
from backend.bot.execution_engine import ExecutionEngine
from backend.bot.feed_manager import FeedManager
from backend.bot.greeks_engine import GreeksEngine
from backend.bot.risk_manager import RiskManager
from backend.strategies.signal_aggregator import SignalAggregator
from backend.strategies.momentum_breakout import MomentumBreakoutStrategy
from backend.strategies.oi_buildup import OIBuildupStrategy
from backend.strategies.pcr_reversal import PCRReversalStrategy
from backend.bot.bot_engine import BotEngine

# Setup centralized logging before other initializations
setup_logging()

logger = structlog.get_logger()

app = FastAPI(
    title="Options Buying Bot API",
    description="FastAPI backend for NIFTY/BANKNIFTY Options Trading Bot",
    version="2.0.0",
)

# CORS middleware for the React dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global bot state
bot_state: Dict[str, Any] = {
    "status": "STOPPED",
    "session_manager": None,
    "email_service": None,
    "portfolio_manager": None,
    "option_chain_manager": None,
    "execution_engine": None,
    "bot_engine": None,
}


def get_bot_state():
    return bot_state


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up FastAPI application...")
    bot_state["session_manager"] = SessionManager()

    # Initialize DB
    await init_db()

    # Initialize Email Service
    email_service = EmailService()
    bot_state["email_service"] = email_service

    bot_state["portfolio_manager"] = PortfolioManager()
    registry = InstrumentRegistry()
    bot_state["option_chain_manager"] = OptionChainManager(registry)
    bot_state["execution_engine"] = ExecutionEngine(bot_state["session_manager"])

    # Initialize strategies and bot engine
    strategies = [
        MomentumBreakoutStrategy(),
        OIBuildupStrategy(),
        PCRReversalStrategy(),
    ]

    nifty_agg = SignalAggregator(strategies, registry)
    bnf_agg = SignalAggregator(strategies, registry)

    feed_manager = FeedManager(bot_state["session_manager"])
    greeks_engine = GreeksEngine()
    risk_manager = RiskManager(
        {"daily_loss_limit": 5000, "max_open_positions": 5, "risk_per_trade": 1000}
    )

    bot_engine = BotEngine(
        feed_manager=feed_manager,
        option_chain_manager=bot_state["option_chain_manager"],
        greeks_engine=greeks_engine,
        portfolio_manager=bot_state["portfolio_manager"],
        execution_engine=bot_state["execution_engine"],
        risk_manager=risk_manager,
        aggregators={"NIFTY": nifty_agg, "BANKNIFTY": bnf_agg},
    )
    bot_state["bot_engine"] = bot_engine

    # Send bot start alert
    html_content = get_template("bot_start").render(
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    asyncio.create_task(
        email_service.send_email("Bot Started Successfully", html_content)
    )

    # In a real scenario, login should happen here or via API
    # In a real scenario, login should happen here or via API
    # bot_state["session_manager"].login()
    bot_state["status"] = "RUNNING"
    await bot_state["bot_engine"].start()

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application...")
    if bot_state.get("bot_engine"):
        await bot_state["bot_engine"].stop()

    if bot_state["session_manager"]:
        bot_state["session_manager"].logout()


app.router.lifespan_context = lifespan

app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/ws")

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,
    )
