from datetime import date
from typing import List, Optional
from sqlalchemy import select

from backend.storage.database import TradeModel, AsyncSessionLocal
from backend.api.schemas import Trade


class TradeRepository:
    async def add_trade(self, trade: Trade) -> TradeModel:
        async with AsyncSessionLocal() as session:
            trade_data = trade.dict()
            db_trade = TradeModel(**trade_data)
            session.add(db_trade)
            await session.commit()
            await session.refresh(db_trade)
            return db_trade

    async def get_trade(self, trade_id: str) -> Optional[TradeModel]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(TradeModel).where(TradeModel.id == trade_id)
            )
            return result.scalar_one_or_none()

    async def get_all_trades(
        self, limit: int = 100, skip: int = 0, target_date: Optional["date"] = None
    ) -> List[TradeModel]:

        async with AsyncSessionLocal() as session:
            query = select(TradeModel)
            if target_date:
                from sqlalchemy import cast, Date

                query = query.where(cast(TradeModel.entry_time, Date) == target_date)

            result = await session.execute(query.offset(skip).limit(limit))
            return result.scalars().all()

    async def update_trade(self, trade_id: str, updates: dict) -> Optional[TradeModel]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(TradeModel).where(TradeModel.id == trade_id)
            )
            trade_to_update = result.scalar_one_or_none()

            if not trade_to_update:
                return None

            for key, value in updates.items():
                setattr(trade_to_update, key, value)

            await session.commit()
            await session.refresh(trade_to_update)
            return trade_to_update
