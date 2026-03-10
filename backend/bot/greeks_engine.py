import structlog
from typing import Dict, Any
import py_vollib.black_scholes.implied_volatility as iv
import py_vollib.black_scholes.greeks.analytical as greeks
from py_vollib.black_scholes.implied_volatility import (
    PriceIsBelowIntrinsic,
    PriceIsAboveMaximum,
)

logger = structlog.get_logger()


class GreeksEngine:
    """Computes options Greeks dynamically."""

    def __init__(self):
        pass

    def refresh(
        self,
        snapshot: Dict[str, Any],
        spot_price: float,
        time_to_expiry: float,
        risk_free_rate: float = 0.1,
    ):
        """Refreshes Greeks based on new option chain snapshot."""
        if time_to_expiry <= 0 or spot_price <= 0:
            return

        for token, option_data in snapshot.items():
            ltp = option_data.get("ltp")
            strike = option_data.get("strike")
            option_type = option_data.get("option_type")  # 'c' or 'p'

            if ltp is None or strike is None or not option_type:
                continue

            flag = option_type.lower()
            if flag not in ["c", "p"]:
                continue

            try:
                # Calculate Implied Volatility
                implied_vol = iv.implied_volatility(
                    price=ltp,
                    S=spot_price,
                    K=strike,
                    t=time_to_expiry,
                    r=risk_free_rate,
                    flag=flag,
                )

                # Calculate Greeks
                delta = greeks.delta(
                    flag,
                    spot_price,
                    strike,
                    time_to_expiry,
                    risk_free_rate,
                    implied_vol,
                )
                gamma = greeks.gamma(
                    flag,
                    spot_price,
                    strike,
                    time_to_expiry,
                    risk_free_rate,
                    implied_vol,
                )
                theta = greeks.theta(
                    flag,
                    spot_price,
                    strike,
                    time_to_expiry,
                    risk_free_rate,
                    implied_vol,
                )
                vega = greeks.vega(
                    flag,
                    spot_price,
                    strike,
                    time_to_expiry,
                    risk_free_rate,
                    implied_vol,
                )

                option_data["iv"] = implied_vol
                option_data["delta"] = delta
                option_data["gamma"] = gamma
                option_data["theta"] = theta
                option_data["vega"] = vega

            except (PriceIsBelowIntrinsic, PriceIsAboveMaximum) as e:
                # Typically means the option is deep ITM or there's bad data/liquidity
                option_data["iv"] = None
                option_data["delta"] = None
                option_data["gamma"] = None
                option_data["theta"] = None
                option_data["vega"] = None
                logger.debug(
                    f"Volatility calc error for strike {strike} {flag}: {str(e)}"
                )
            except Exception as e:
                option_data["iv"] = None
                option_data["delta"] = None
                option_data["gamma"] = None
                option_data["theta"] = None
                option_data["vega"] = None
                logger.error(f"Error calculating greeks for {token}: {str(e)}")
