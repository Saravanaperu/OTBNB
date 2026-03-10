import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Float, Integer, DateTime

from config.settings import settings

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

class TradeModel(Base):
    __tablename__ = "trades"

    id = Column(String, primary_key=True, index=True)
    instrument = Column(String, index=True)
    tradingsymbol = Column(String)
    direction = Column(String)
    strike = Column(Integer)
    expiry = Column(String)
    lots = Column(Integer)
    quantity = Column(Integer)
    entry_price = Column(Float)
    entry_time = Column(DateTime)
    exit_price = Column(Float, nullable=True)
    exit_time = Column(DateTime, nullable=True)
    exit_reason = Column(String, nullable=True)
    realised_pnl = Column(Float, nullable=True)
    entry_delta = Column(Float, nullable=True)
    entry_iv = Column(Float, nullable=True)
    entry_iv_rank = Column(Float, nullable=True)
    strategy_name = Column(String)
    order_id_entry = Column(String)
    order_id_exit = Column(String, nullable=True)
    status = Column(String)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
