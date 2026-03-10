# Options Buying Bot (NIFTY & BANKNIFTY)

This repository contains an options buying bot for trading NIFTY and BANKNIFTY on AngelOne SmartAPI.

## Features
- Intraday fully automated options buying bot
- NIFTY and BANKNIFTY trading
- Uses multiple strategies (Momentum Breakout, OI Buildup, PCR Reversal, etc.)
- Strict risk management
- FastAPI backend serving a REST and WebSocket API
- React dashboard (Vite + TypeScript) for real-time monitoring
- Email alerts for trades

## Structure
- `backend/`: FastAPI backend and the core python trading bot engine
- `frontend/`: React based user interface dashboard
- `docs/`: Relevant architecture documents

## Setup

### 1. Backend
To run the backend FastAPI server and the core Python trading bot engine:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend
To run the React based user interface dashboard:
```bash
cd frontend
npm install
npm run dev
```

### 3. Testing
To run the automated test suite for the backend:
```bash
cd backend
PYTHONPATH=. pytest tests/
```
