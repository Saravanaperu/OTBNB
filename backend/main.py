import asyncio
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.config.settings import settings
from backend.bot.session_manager import SessionManager

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
    "session_manager": None
}

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application...")
    bot_state["session_manager"] = SessionManager()

    # In a real scenario, login should happen here or via API
    # bot_state["session_manager"].login()
    bot_state["status"] = "INITIALIZED"

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down FastAPI application...")
    if bot_state["session_manager"]:
        bot_state["session_manager"].logout()

@app.get("/health")
async def health_check():
    return {"status": "ok", "bot_status": bot_state["status"]}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=settings.backend_host, port=settings.backend_port, reload=True)
