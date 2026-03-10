import asyncio
import time
from datetime import datetime, timedelta
from backend.storage.repositories import TradeRepository
from backend.api.schemas import Trade
from backend.storage.database import init_db

async def benchmark_get_positions_history():
    repo = TradeRepository()
    await init_db()

    # 1. Setup: Inject dummy data
    print("Injecting dummy data...")
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    # Add 100 trades for yesterday
    for i in range(100):
        t = Trade(
            id=f"yest_{i}",
            instrument="NIFTY",
            tradingsymbol=f"NIFTY24OCT{19000+i}CE",
            direction="BUY",
            strike=19000+i,
            expiry="24OCT",
            lots=1,
            quantity=50,
            entry_price=100.0,
            entry_time=yesterday,
            exit_price=110.0,
            exit_time=yesterday,
            exit_reason="Target",
            realised_pnl=500.0,
            strategy_name="Test",
            order_id_entry=f"oid_e_{i}",
            status="CLOSED"
        )
        await repo.add_trade(t)

    # Add 10 trades for today
    for i in range(10):
        t = Trade(
            id=f"today_{i}",
            instrument="NIFTY",
            tradingsymbol=f"NIFTY24OCT{20000+i}CE",
            direction="BUY",
            strike=20000+i,
            expiry="24OCT",
            lots=1,
            quantity=50,
            entry_price=100.0,
            entry_time=today,
            exit_price=110.0,
            exit_time=today,
            exit_reason="Target",
            realised_pnl=500.0,
            strategy_name="Test",
            order_id_entry=f"oid_et_{i}",
            status="CLOSED"
        )
        await repo.add_trade(t)

    print("Data injected.")

    # Define the current (unoptimized) logic as a function to benchmark
    async def current_logic():
        trades = await repo.get_all_trades(limit=1000)
        closed = []
        today_date = datetime.now().date()
        for t in trades:
            if t.status == "CLOSED" and t.exit_time and t.exit_time.date() == today_date:
                closed.append(t)
        return closed

    # Define the optimized logic
    async def optimized_logic():
        today_date = datetime.now().date()
        trades = await repo.get_all_trades(limit=1000, target_date=today_date)
        closed = []
        for t in trades:
            if t.status == "CLOSED":
                closed.append(t)
        return closed

    # 2. Benchmark current logic
    print("Benchmarking current logic...")
    start_time = time.perf_counter()
    for _ in range(100):
        await current_logic()
    end_time = time.perf_counter()
    current_duration = end_time - start_time
    print(f"Current logic took: {current_duration:.4f} seconds for 100 calls")

    # 3. Benchmark optimized logic
    print("Benchmarking optimized logic...")
    start_time = time.perf_counter()
    for _ in range(100):
        await optimized_logic()
    end_time = time.perf_counter()
    optimized_duration = end_time - start_time
    print(f"Optimized logic took: {optimized_duration:.4f} seconds for 100 calls")

    improvement = (current_duration - optimized_duration) / current_duration * 100
    print(f"Improvement: {improvement:.2f}%")

if __name__ == "__main__":
    import os
    # Ensure we use a test database
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./benchmark.db"
    if os.path.exists("./benchmark.db"):
        os.remove("./benchmark.db")
    asyncio.run(benchmark_get_positions_history())
