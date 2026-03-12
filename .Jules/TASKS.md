# Open Tasks

| ID | Status | Priority | Description | Assignee | Dependencies |
|---|---|---|---|---|---|
| QA-002 | Pending | High | Run bot with simulated ticks to verify system stability and order logic without money. | QA Engineer | QA-001, DEV-005 |
| QA-003 | Pending | Medium | Increase test coverage for frontend (currently only `App.test.tsx` exists). | QA Engineer | None |
| DOC-001 | Pending | Low | Document final setup instructions. | Tech Writer | QA-002 |
| QA-006 | Pending | High | Increase backend test coverage for `bot_engine.py` and `execution_engine.py` modules. | QA Engineer | None |

# Archive

| ID | Status | Priority | Description | Assignee | Dependencies |
|---|---|---|---|---|---|
| UI-010 | Done (2026-03-12) | Medium | Implement Toast notifications and Skeleton loaders | UIMaster | None |

| ID | Status | Priority | Description | Assignee | Dependencies |
|---|---|---|---|---|---|
| DEV-012 | Done (2026-03-12) | High | Integrate refresh_session logic into the bot lifecycle (e.g., scheduled token refresh). | Developer | INT-005 |
| ARCH-011 | Done (2026-03-12) | Medium | Implement automated error recovery and notification for backend exceptions. | Architect | ARCH-010 |

| ID | Status | Priority | Description | Assignee | Dependencies |
|---|---|---|---|---|---|
| DEV-013 | Closed (Duplicate of ARCH-011) | Medium | Implement automated error recovery and notification for backend exceptions. | Developer | ARCH-010 |

| ID | Status | Priority | Description | Assignee | Dependencies |
|---|---|---|---|---|---|
| INT-005 | Done (2024-05-18) | High | Implement automatic token refresh and retry logic for SmartAPI SessionManager. | Integrator | None |
| DOC-002 | Done (2026-03-11) | High | Generate OpenAPI specification and setup Swagger UI. | Tech Writer | None |
| QA-004 | Done (2026-03-11) | High | Increase test coverage for backend core components. | QA Engineer | None |
| OPS-003 | Done (2025-03-11) | Medium | Create runbooks for common operational tasks (Makefile) and database disaster recovery scripts. | Ops | None |
| UI-009 | Done (2026-03-11) | Medium | Replace placeholder Positions page with a dedicated component. | UIMaster | None |
| DEV-011 | Done (2026-03-11) | High | Implement real trade stats in `/api/v1/trades/stats`. | Developer | None |
| QA-005 | Done (2026-03-10) | Medium | Fix unhandled WebSocket error in frontend tests (`App.test.tsx`). | Developer | None |
| ARCH-010 | Done (2026-03-10) | High | Refactor global bot state access and implement global exception handler. | Architect | None |
| DEV-010 | Done (2025-03-05) | High | Integrate `ExecutionEngine` into main application logic and endpoints. | Developer | INT-003 |
| OPS-002 | Done (2026-03-10) | High | Enhance CI/CD pipeline with black, flake8, mypy, and test coverage | Ops | None |
| UI-008 | Done (2026-03-10) | Low | Add ARIA labels to buttons for accessibility. | UIMaster | None |
| INT-004 | Done (2026-03-11) | High | Implement WebSocket dynamic token subscription in FeedManager | Integrator | None |
| INT-003 | Done (2026-03-10) | High | Implement ExecutionEngine for AngelOne SmartAPI integration | Integrator | None |
| OPS-001 | Done (2026-03-10) | Medium | Containerize the application (Dockerfiles and docker-compose). | Ops | None |
| ARCH-009 | Done (2026-03-10) | High | Set up centralized logging configuration with structlog. | Architect | None |
| DEV-001 | Completed | Medium | Build the Base Strategy class (`backend/strategies/base_strategy.py`). | Architect | ARCH-004, ARCH-007 |
| DEV-002 | Completed | Medium | Implement Momentum Breakout Strategy (`backend/strategies/momentum_breakout.py`). | Developer | DEV-001 |
| DEV-003 | Completed | Medium | Implement OI Buildup Strategy (`backend/strategies/oi_buildup.py`). | Developer | DEV-001 |
| DEV-004 | Completed | Medium | Implement PCR Reversal Strategy (`backend/strategies/pcr_reversal.py`). | Developer | DEV-001 |
| DEV-005 | Completed | Medium | Implement Signal Aggregator (`backend/strategies/signal_aggregator.py`). | Developer | DEV-002, DEV-003, DEV-004 |
| INT-001 | Completed | Low | Set up Email Service with HTML templating (`backend/alerts/email_service.py`). | Integrator | None |
| DEV-009 | Completed | Medium | Use SQLite to persist trades history (`backend/storage/database.py`). | Developer | None |
| INT-002 | Completed | High | Link frontend to backend endpoints (completed 2024-05-18). | Integrator | DEV-007, UX-001 |
| TSK-001 | Completed | High | Implement CI/CD pipeline with GitHub Actions | Jules | None |
| TSK-002 | Completed | High | Add Automerge step to CI/CD | Jules | TSK-001 |
| TSK-003 | Completed | High | Add relevant tests to be run in CI/CD | Jules | TSK-001 |
| ARCH-001 | Completed | High | Implement SmartAPI login & TOTP generation (`backend/bot/session_manager.py`). | Integrator | None |
| ARCH-002 | Completed | High | Set up the WebSocket ticker for live market data (`backend/bot/feed_manager.py`). | Architect | ARCH-001 |
| ARCH-003 | Completed | High | Implement Instrument Registry to pull active strike details (`backend/bot/instrument_registry.py`). | Architect | ARCH-001 |
| ARCH-004 | Completed | High | Implement Option Chain tracking (`backend/bot/option_chain_manager.py`). | Developer | ARCH-002, ARCH-003 |
| ARCH-005 | Completed | High | Implement Greeks engine (`backend/bot/greeks_engine.py`) with `py_vollib`. | Developer | None |
| ARCH-006 | Completed | High | Implement the `RiskManager` module (`backend/bot/risk_manager.py`). | Architect | None |
| ARCH-007 | Completed | High | Implement the `PositionManager` and `PortfolioManager` to keep track of P&L. | Developer | ARCH-006 |
| ARCH-008 | Completed | High | Implement `settings.yaml` and `.env` parsing with `pydantic-settings` (`backend/config/settings.py`). | Architect | None |
| DEV-006 | Completed | Medium | Setup FastAPI main application and routing (`backend/main.py`). | Architect | None |
| DEV-007 | Completed | Medium | Build REST API endpoints for `/status`, `/positions`, `/pnl`, `/trades`, etc. | Developer | DEV-006 |
| DEV-008 | Completed | Medium | Build WebSocket server to emit events (`backend/api/websocket.py`). | Architect | DEV-006 |
| UX-001 | Completed | Low | Set up Vite + React + TypeScript with Tailwind CSS (`frontend/`). | UIMaster | None |
| UX-002 | Completed | Low | Implement layout components (TopBar, SideNav, SignalTicker). | UIMaster | UX-001 |
| UX-003 | Completed | Low | Configure `zustand` stores for bot status and market data. | Developer | UX-001 |
| UX-004 | Completed | Low | Implement WebSocket custom hook to ingest live ticks and position updates. | Developer | UX-003, DEV-008 |
| UX-005 | Completed | Low | Build the live monitoring UI: `PositionsTable`, `RiskGauge`, `PnLCurve` components. | UIMaster | UX-002, UX-004 |
| UX-006 | Completed | Low | Build the `TradeHistory` view pulling from the backend. | UIMaster | UX-002, DEV-007 |
| UX-007 | Completed | Low | Finalize configuration panels to adjust bot settings from UI. | UIMaster | UX-002, DEV-007 |
| QA-001 | Done (2026-03-10) | High | Write basic unit tests for the core logic (Greeks, Risk, Option Chain). | QA Engineer | ARCH-004, ARCH-005, ARCH-006 |
