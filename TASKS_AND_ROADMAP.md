# Options Buying Bot - Tasks & Roadmap

## Phase 1: Project Initialization & Structure (Completed)
- [x] Read architecture documents
- [x] Extract file structure
- [x] Create backend file structure
- [x] Create frontend file structure
- [x] Create project documentation (README.md, AGENTS.md, TASKS_AND_ROADMAP.md)

## Phase 2: Backend Core Trading Engine Setup
- [x] Implement `settings.yaml` and `.env` parsing with `pydantic-settings` (`backend/config/settings.py`).
- [x] Implement SmartAPI login & TOTP generation (`backend/bot/session_manager.py`).
- [x] Set up the WebSocket ticker for live market data (`backend/bot/feed_manager.py`).
- [x] Implement Instrument Registry to pull active strike details (`backend/bot/instrument_registry.py`).
- [x] Implement Option Chain tracking (`backend/bot/option_chain_manager.py`).
- [x] Implement Greeks engine (`backend/bot/greeks_engine.py`) with `py_vollib`.
- [x] Implement the `RiskManager` module (`backend/bot/risk_manager.py`).
- [x] Implement the `PositionManager` and `PortfolioManager` to keep track of P&L (`backend/bot/position_manager.py`, `backend/bot/portfolio_manager.py`).

## Phase 3: Trading Strategies Implementation
- [x] Build the Base Strategy class (`backend/strategies/base_strategy.py`).
- [x] Implement Momentum Breakout Strategy (`backend/strategies/momentum_breakout.py`).
- [x] Implement OI Buildup Strategy (`backend/strategies/oi_buildup.py`).
- [x] Implement PCR Reversal Strategy (`backend/strategies/pcr_reversal.py`).
- [x] Implement Signal Aggregator (`backend/strategies/signal_aggregator.py`).

## Phase 4: API & Alerting (Completed)
- [x] Setup FastAPI main application and routing (`backend/main.py`).
- [x] Build REST API endpoints for `/status`, `/positions`, `/pnl`, `/trades`, etc. (`backend/api/routes/`).
- [x] Build WebSocket server to emit events (`backend/api/websocket.py`).
- [x] Set up Email Service with HTML templating (`backend/alerts/email_service.py`).
- [x] Use SQLite to persist trades history (`backend/storage/database.py`).

## Phase 5: Frontend Dashboard (Completed)
- [x] Set up Vite + React + TypeScript with Tailwind CSS (`frontend/`).
- [x] Implement layout components (TopBar, SideNav, SignalTicker).
- [x] Configure `zustand` stores for bot status and market data.
- [x] Implement WebSocket custom hook to ingest live ticks and position updates.
- [x] Build the live monitoring UI: `PositionsTable`, `RiskGauge`, `PnLCurve` components.
- [x] Build the `TradeHistory` view pulling from the backend.
- [x] Finalize configuration panels to adjust bot settings from UI.

## Phase 6: System Integration & Testing
- [x] Link frontend to backend endpoints.
- [x] Write basic unit tests for the core logic (Greeks, Risk, Option Chain).
- [ ] Run bot with simulated ticks to verify system stability and order logic without money.
- [ ] Document final setup instructions.
