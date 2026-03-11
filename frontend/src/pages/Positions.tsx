import { PositionsTable } from '../components/positions/PositionsTable';
import { useMarketStore } from '../store/marketStore';

export function Positions() {
  const { positions } = useMarketStore();
  const openPositions = positions.filter(p => p.status === 'OPEN');

  const totalInvested = openPositions.reduce((acc, p) => acc + (p.entry_price * p.quantity), 0);
  const netUnrealisedPnL = openPositions.reduce((acc, p) => acc + (p.unrealised_pnl || 0), 0);
  const openPositionsCount = openPositions.length;

  return (
    <div className="p-6 h-full w-full flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Positions</h1>
        <p className="text-slate-400 text-sm">Manage and monitor active trades</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6 flex flex-col justify-center">
          <div className="text-sm text-slate-400 mb-1">Open Positions</div>
          <div className="text-2xl font-bold text-slate-200">{openPositionsCount}</div>
        </div>
        <div className="card p-6 flex flex-col justify-center">
          <div className="text-sm text-slate-400 mb-1">Total Invested</div>
          <div className="text-2xl font-bold text-slate-200">₹{totalInvested.toFixed(2)}</div>
        </div>
        <div className="card p-6 flex flex-col justify-center">
          <div className="text-sm text-slate-400 mb-1">Net Unrealised PnL</div>
          <div className={`text-2xl font-bold ${netUnrealisedPnL >= 0 ? 'text-success' : 'text-danger'}`}>
            {netUnrealisedPnL > 0 ? '+' : ''}{netUnrealisedPnL.toFixed(2)}
          </div>
        </div>
      </div>

      <div className="flex-1 mt-2">
        <PositionsTable />
      </div>
    </div>
  );
}
