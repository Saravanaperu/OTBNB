import time
import pyotp
from SmartApi import SmartConnect
from backend.config.settings import settings
import structlog

logger = structlog.get_logger()


class SessionManager:
    """Manages connection and authentication with AngelOne SmartAPI."""

    def __init__(self):
        self.api_key = settings.angelone_api_key
        self.client_code = settings.angelone_client_code
        self.password = settings.angelone_password
        self.totp_secret = settings.angelone_totp_secret

        self.api = SmartConnect(api_key=self.api_key)
        self.feed_token = None
        self.jwt_token = None
        self.refresh_token = None
        self.is_connected = False

    def login(self):
        """Authenticates with AngelOne and retrieves tokens."""
        logger.info("Attempting login to AngelOne...", client_code=self.client_code)

        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                # Generate TOTP
                totp = pyotp.TOTP(self.totp_secret).now()

                # Authenticate
                data = self.api.generateSession(self.client_code, self.password, totp)

                if data.get("status") is False:
                    logger.error(
                        "Login failed", message=data["message"], attempt=attempt + 1
                    )
                    raise Exception(f"Login failed: {data['message']}")

                self.jwt_token = data["data"]["jwtToken"]
                self.refresh_token = data["data"]["refreshToken"]
                self.feed_token = self.api.getfeedToken()

                self.is_connected = True
                logger.info("Successfully logged in to AngelOne.")
                return

            except Exception as e:
                logger.error(
                    "Exception occurred during login", error=str(e), attempt=attempt + 1
                )

            if attempt < max_retries - 1:
                time.sleep(base_delay * (2**attempt))

        logger.error("Failed to login to AngelOne after all retries.")
        self.is_connected = False

    def refresh_session(self):
        """Refreshes the AngelOne session using the refresh token."""
        if not self.refresh_token:
            logger.error("No refresh token available. Cannot refresh session.")
            self.is_connected = False
            return False

        logger.info("Attempting to refresh AngelOne session...")

        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                data = self.api.generateToken(self.refresh_token)

                if data.get("status") is False:
                    logger.error(
                        "Session refresh failed",
                        message=data.get("message"),
                        attempt=attempt + 1,
                    )
                    raise Exception(f"Session refresh failed: {data.get('message')}")

                self.jwt_token = data["data"]["jwtToken"]
                self.refresh_token = data["data"]["refreshToken"]
                self.feed_token = data["data"]["feedToken"]

                # generateToken also updates the self.api internally using setAccessToken and setFeedToken

                self.is_connected = True
                logger.info("Successfully refreshed AngelOne session.")
                return True

            except Exception as e:
                logger.error(
                    "Exception occurred during session refresh",
                    error=str(e),
                    attempt=attempt + 1,
                )

            if attempt < max_retries - 1:
                time.sleep(base_delay * (2**attempt))

        logger.error(
            "Failed to refresh AngelOne session after all retries. Marking as disconnected."
        )
        self.is_connected = False
        return False

    def logout(self):
        """Logs out from AngelOne."""
        if self.is_connected:
            try:
                self.api.terminateSession(self.client_code)
                self.is_connected = False
                logger.info("Logged out from AngelOne.")
            except Exception as e:
                logger.error("Failed to logout", error=str(e))
