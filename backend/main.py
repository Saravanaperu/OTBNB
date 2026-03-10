import asyncio
import datetime
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config.settings import settings
from bot.session_manager import SessionManager
from api.routes import api_router
from api.websocket import router as ws_router
from storage.database import init_db
from alerts.email_service import EmailService
from alerts.email_templates import get_template

logger = structlog.get_logger()

app = FastAPI(
    title="Options Buying Bot API",
    description="FastAPI backend for NIFTY/BANKNIFTY Options Trading Bot",
    version="2.0.0"
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
    "email_service": None
}

def get_bot_state():
    return bot_state

app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/ws")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application...")
    bot_state["session_manager"] = SessionManager()

    # Initialize DB
    await init_db()

    # Initialize Email Service
    email_service = EmailService()
    bot_state["email_service"] = email_service

    # Send bot start alert
    html_content = get_template("bot_start").render(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    asyncio.create_task(email_service.send_email("Bot Started Successfully", html_content))

    # In a real scenario, login should happen here or via API
    # bot_state["session_manager"].login()
    bot_state["status"] = "INITIALIZED"

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down FastAPI application...")
    if bot_state["session_manager"]:
        bot_state["session_manager"].logout()

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=settings.backend_host, port=settings.backend_port, reload=True)
