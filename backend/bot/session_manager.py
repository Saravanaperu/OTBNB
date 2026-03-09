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

        try:
            # Generate TOTP
            totp = pyotp.TOTP(self.totp_secret).now()

            # Authenticate
            data = self.api.generateSession(self.client_code, self.password, totp)

            if data['status'] == False:
                logger.error("Login failed", message=data['message'])
                raise Exception(f"Login failed: {data['message']}")

            self.jwt_token = data['data']['jwtToken']
            self.refresh_token = data['data']['refreshToken']
            self.feed_token = self.api.getfeedToken()

            self.is_connected = True
            logger.info("Successfully logged in to AngelOne.")

        except Exception as e:
            logger.exception("Exception occurred during login", error=str(e))
            self.is_connected = False

    def logout(self):
        """Logs out from AngelOne."""
        if self.is_connected:
            try:
                self.api.terminateSession(self.client_code)
                self.is_connected = False
                logger.info("Logged out from AngelOne.")
            except Exception as e:
                logger.error("Failed to logout", error=str(e))
