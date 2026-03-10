import { useMarketStore } from '../../store/marketStore';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function PnLCurve() {
  const { positions } = useMarketStore();

  // Create a mock curve based on currently open positions' PnL over time for visualization
  // Real implementation would track this history via WebSocket or REST.
  // For now, we'll just plot a simple sparkline based on current net PnL to visualize it.

  const currentNetPnL = positions.reduce((acc, p) => acc + (p.unrealised_pnl || 0), 0);

  const curveHistory = [
     { time: 'Now', pnl: currentNetPnL },
  ];

  return (
    <div className="card p-6 h-64 flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h3 className="text-lg font-semibold text-slate-200">Net PnL</h3>
          <p className="text-xs text-slate-400">Intraday Performance</p>
        </div>
        <div className={`text-2xl font-bold ${currentNetPnL >= 0 ? 'text-success' : 'text-danger'}`}>
          {currentNetPnL > 0 ? '+' : ''}{currentNetPnL.toFixed(2)}
        </div>
      </div>

      <div className="flex-1 w-full relative">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={curveHistory} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorPnL" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={currentNetPnL >= 0 ? '#22c55e' : '#ef4444'} stopOpacity={0.3}/>
                <stop offset="95%" stopColor={currentNetPnL >= 0 ? '#22c55e' : '#ef4444'} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
            <XAxis dataKey="time" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(val) => `₹${val}`} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '4px' }}
              itemStyle={{ color: '#f8fafc' }}
            />
            <Area
              type="monotone"
              dataKey="pnl"
              stroke={currentNetPnL >= 0 ? '#22c55e' : '#ef4444'}
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorPnL)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}