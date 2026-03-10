import asyncio
import datetime
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.config.settings import settings
from backend.bot.session_manager import SessionManager
from backend.api.routes import api_router
from backend.api.websocket import router as ws_router
from backend.storage.database import init_db
from backend.alerts.email_service import EmailService
from backend.alerts.email_templates import get_template
from backend.bot.portfolio_manager import PortfolioManager
from backend.bot.instrument_registry import InstrumentRegistry
from backend.bot.option_chain_manager import OptionChainManager

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
bot_state = {
    "status": "STOPPED",
    "session_manager": None,
    "email_service": None,
    "portfolio_manager": None,
    "option_chain_manager": None,
}


def get_bot_state():
    return bot_state


from contextlib import asynccontextmanager


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

    # Send bot start alert
    html_content = get_template("bot_start").render(
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    asyncio.create_task(
        email_service.send_email("Bot Started Successfully", html_content)
    )

    # In a real scenario, login should happen here or via API
    # bot_state["session_manager"].login()
    bot_state["status"] = "INITIALIZED"

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application...")
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
