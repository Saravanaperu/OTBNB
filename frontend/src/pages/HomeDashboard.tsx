import { PositionsTable } from '../components/positions/PositionsTable';
import { RiskGauge } from '../components/charts/RiskGauge';
import { PnLCurve } from '../components/charts/PnLCurve';

export function HomeDashboard() {
  return (
    <div className="p-6 h-full w-full flex flex-col gap-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Overview Dashboard</h1>
          <p className="text-slate-400 text-sm">Real-time monitoring and analytics</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RiskGauge />
        <PnLCurve />
      </div>

      <div className="flex-1 mt-2">
        <h2 className="text-lg font-semibold text-slate-200 mb-4">Active Positions</h2>
        <PositionsTable />
      </div>
    </div>
  );
}