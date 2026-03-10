import { useMarketStore } from '../../store/marketStore';

export function RiskGauge() {
  const { riskBudget } = useMarketStore();

  if (!riskBudget) {
    return (
      <div className="card p-6 flex items-center justify-center text-slate-400 h-64">
        Loading risk metrics...
      </div>
    );
  }

  // Assuming daily_loss_used is negative when losing, and we want to show utilization of a budget.
  // For simplicity, let's treat it as an absolute value for the bar.
  const absLoss = Math.abs(riskBudget.daily_loss_used);
  const totalBudget = absLoss + riskBudget.remaining_budget;
  const utilizedPct = totalBudget === 0 ? 0 : (absLoss / totalBudget) * 100;

  let color = 'bg-success';
  if (utilizedPct > 50) color = 'bg-warning';
  if (utilizedPct > 80) color = 'bg-danger';

  return (
    <div className="card p-6 h-64 flex flex-col justify-between">
      <div>
        <h3 className="text-lg font-semibold text-slate-200 mb-1">Risk Budget</h3>
        <p className="text-xs text-slate-400">Daily utilized risk allocation</p>
      </div>

      <div className="flex flex-col items-center justify-center flex-1 py-4">
        <div className="text-3xl font-bold tracking-tight mb-2">
          {utilizedPct.toFixed(1)}%
        </div>

        <div className="w-full max-w-[200px] h-3 bg-slate-800 rounded-full overflow-hidden mt-2 relative">
           <div
             className={`h-full ${color} transition-all duration-500 ease-out`}
             style={{ width: `${Math.min(utilizedPct, 100)}%` }}
           />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mt-4 pt-4 border-t border-border">
         <div>
            <div className="text-xs text-slate-500 mb-1">Used</div>
            <div className="text-sm font-semibold text-danger">₹{absLoss.toFixed(2)}</div>
         </div>
         <div className="text-right">
            <div className="text-xs text-slate-500 mb-1">Remaining</div>
            <div className="text-sm font-semibold text-success">₹{riskBudget.remaining_budget.toFixed(2)}</div>
         </div>
      </div>
    </div>
  );
}