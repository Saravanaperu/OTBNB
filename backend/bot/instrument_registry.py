import structlog
import asyncio
import httpx
from typing import Dict, Any, List

logger = structlog.get_logger()


class InstrumentRegistry:
    """Manages available instruments and option strikes."""

    def __init__(self):
        self.master_data: List[Dict[str, Any]] = []
        self.token_to_symbol: Dict[str, str] = {}
        self.symbol_to_token: Dict[str, str] = {}
        self.strike_map: Dict[str, Any] = {}

    async def load_master(self):
        """Loads the instrument master from broker API."""
        logger.info("Loading instrument master data...")
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                # Filter for NIFTY and BANKNIFTY in NSE and NFO
                filtered_data = [
                    d
                    for d in data
                    if d.get("name") in ["NIFTY", "BANKNIFTY"]
                    and d.get("exch_seg") in ["NSE", "NFO"]
                ]

                self.master_data = filtered_data

                # Build lookup maps
                for inst in self.master_data:
                    token = inst.get("token")
                    symbol = inst.get("symbol")
                    if token and symbol:
                        self.token_to_symbol[token] = symbol
                        self.symbol_to_token[symbol] = token

                logger.info(f"Loaded {len(self.master_data)} relevant instruments.")
        except Exception as e:
            logger.error("Failed to load instrument master data", error=str(e))
            self.master_data = []

    def get_token(self, symbol: str) -> str:
        """Returns the token for a given symbol."""
        return self.symbol_to_token.get(symbol, "")

    def get_symbol_by_token(self, token: str) -> str:
        """Returns the symbol for a given token."""
        return self.token_to_symbol.get(token, "")
