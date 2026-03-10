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

### Prerequisites
- Python 3.12+
- Node.js 18+
- AngelOne SmartAPI account and credentials

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the `.env` file based on `config/settings.yaml` to include your AngelOne credentials:
   ```env
   ANGEL_API_KEY=your_api_key
   ANGEL_CLIENT_ID=your_client_id
   ANGEL_PASSWORD=your_password
   ANGEL_TOTP_SECRET=your_totp_secret
   ```
5. Run the FastAPI backend:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. The dashboard will be accessible at `http://localhost:5173`.
