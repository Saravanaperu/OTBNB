# Options Buying Bot - Agent Instructions

Welcome to the Options Buying Bot project! As an AI agent contributing to this repository, please adhere to the following principles:

## Overall Context
This project implements an automated options trading system for NIFTY and BANKNIFTY on the Indian NSE stock exchange, specifically utilizing AngelOne SmartAPI.
It uses an intraday buying strategy. Key architectural decisions include:
- A FastAPI + asyncio backend in Python (the core bot engine).
- A standalone React dashboard for monitoring and manual intervention, built with Vite and TypeScript.
- Alerts are dispatched using an async email service.

## Directory Structure
- **backend/**: Contains the FastAPI application (`api/`), the core trading engine (`bot/`), trading strategies (`strategies/`), risk settings, and data storage logic.
- **frontend/**: Contains the React dashboard SPA, decoupled from the backend.
- **docs/**: Architectural design documents providing system details and logic flow.

## Guidelines
1. **Code Formatting & Typing:**
   - Backend: Use Pydantic models extensively for API schemas and internal types. Use type hinting across all Python code. Follow clean async/await patterns using `asyncio`.
   - Frontend: Use TypeScript for all React code. Use hooks properly, particularly Zustand for global state and React Query for REST calls. Use Tailwind CSS for styling.
2. **Secrets Management:** NEVER hardcode any keys, tokens, or passwords. All secrets must be loaded from `.env` files and appropriately typed via `pydantic-settings` (Backend) or `VITE_` prefixed environment variables (Frontend).
3. **Async Programming:** The Python trading core relies heavily on `asyncio` for executing simultaneous ticks on NIFTY and BANKNIFTY. Do not introduce blocking, synchronous calls in the async data paths.
4. **Testing:** Make sure changes in core logical components like `GreeksEngine`, `RiskManager`, or `OptionChainManager` are well tested before using them in the bot core event loops.
5. **No Actual Trading:** Since you do not have actual broker credentials to make real market orders, focus heavily on the structure, logic, routing, schemas, state management, and the scaffolding of the components.

When you finish setting up a new feature or implementing a module from the doc, remember to update or test your code. Good luck!
