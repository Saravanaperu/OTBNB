import os
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, YamlConfigSettingsSource
from pydantic import Field
from typing import List, Tuple, Type

class MarketSettings(BaseSettings):
    open_time: str = '09:15'
    bot_start_time: str = '09:20'
    no_new_entry_after: str = '15:20'
    square_off_time: str = '15:20'
    eod_report_time: str = '15:35'
    timezone: str = 'Asia/Kolkata'

class InstrumentSettings(BaseSettings):
    lot_size: int
    strike_interval: int
    weekly_expiry_day: str
    atm_strikes_range: int
    min_premium: int
    max_premium: int

class InstrumentsConfig(BaseSettings):
    nifty: InstrumentSettings = InstrumentSettings(
        lot_size=50, strike_interval=50, weekly_expiry_day='Thursday',
        atm_strikes_range=5, min_premium=30, max_premium=300
    )
    banknifty: InstrumentSettings = InstrumentSettings(
        lot_size=15, strike_interval=100, weekly_expiry_day='Wednesday',
        atm_strikes_range=5, min_premium=50, max_premium=600
    )

class AppSettings(BaseSettings):
    # AngelOne Secrets
    angelone_api_key: str = Field(default="dummy_api_key")
    angelone_client_code: str = Field(default="dummy_client_code")
    angelone_password: str = Field(default="dummy_password")
    angelone_totp_secret: str = Field(default="dummy_totp_secret")

    # Dashboard Auth
    dashboard_token: str = Field(default="dummy_dashboard_token")

    # Email
    gmail_user: str = Field(default="dummy@gmail.com")
    gmail_app_pass: str = Field(default="dummy_pass")
    alert_email: str = Field(default="alert@gmail.com")

    # DB & Server
    database_url: str = Field(default="sqlite+aiosqlite:///./trades.db")
    backend_host: str = Field(default="0.0.0.0")
    backend_port: int = Field(default=8000)

    market: MarketSettings = MarketSettings()
    instruments: InstrumentsConfig = InstrumentsConfig()

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        yaml_file=os.path.join(os.path.dirname(__file__), 'settings.yaml'),
        yaml_file_encoding='utf-8',
        extra='ignore'
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )

settings = AppSettings()
