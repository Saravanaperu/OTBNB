import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { RiskConfig, StrategyConfig } from '../types';

// Mock API functions
const fetchConfig = async () => {
  // const riskRes = await fetch('/api/v1/config/risk');
  // const riskData = await riskRes.json();

  const mockRisk: RiskConfig = {
    daily_hard_limit: 5000,
    daily_soft_limit: 3000,
    per_trade_risk: 1000,
    max_open_positions: 3,
    max_same_instrument: 2,
    max_lots_per_trade: 5,
    max_capital_pct: 0.1,
    iv_rank_buy_threshold: 40,
    min_delta: 0.2,
    max_delta: 0.6,
    max_theta_daily_pct: 0.05,
    min_strike_volume: 50000,
    min_strike_oi: 10000,
    max_bid_ask_spread_pct: 0.05,
    no_trade_after: '14:30',
    no_0dte_after: '13:00'
  };

  const mockStrategies: StrategyConfig[] = [
    {
      name: 'MomentumBreakout',
      enabled: true,
      instruments: ['NIFTY', 'BANKNIFTY'],
      params: { rsi_period: 14, overbought: 70, oversold: 30 }
    },
    {
      name: 'OIBuildup',
      enabled: false,
      instruments: ['NIFTY'],
      params: { lookback_periods: 5, oi_change_threshold: 0.2 }
    }
  ];

  return { risk: mockRisk, strategies: mockStrategies };
};

export function Configuration() {
  const { data, isLoading, refetch } = useQuery({
    queryKey: ['config'],
    queryFn: fetchConfig,
  });

  const [riskConfig, setRiskConfig] = useState<RiskConfig | null>(null);

  useEffect(() => {
    if (data?.risk) {
      setRiskConfig(data.risk);
    }
  }, [data]);

  const saveConfig = async (newConfig: RiskConfig) => {
     // await fetch('/api/v1/config/risk', { method: 'POST', body: JSON.stringify(newConfig) })
     return newConfig;
  };

  const mutation = useMutation({
    mutationFn: saveConfig,
    onSuccess: () => {
       alert("Configuration saved successfully!");
       refetch();
    }
  });

  const handleRiskChange = (key: keyof RiskConfig, value: string | number) => {
    if (!riskConfig) return;
    setRiskConfig({
      ...riskConfig,
      [key]: typeof riskConfig[key] === 'number' ? Number(value) : value,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (riskConfig) {
      mutation.mutate(riskConfig);
    }
  };

  if (isLoading || !riskConfig || !data) {
    return <div className="p-6">Loading configuration...</div>;
  }

  return (
    <div className="p-6 h-full w-full flex flex-col gap-6 overflow-y-auto">
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Configuration</h1>
        <p className="text-slate-400 text-sm">Manage risk parameters and strategy settings</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pb-12">
        <form onSubmit={handleSubmit} className="card p-6 flex flex-col gap-4">
          <h2 className="text-lg font-semibold text-slate-200 border-b border-border pb-2 mb-2">Risk Budget & Limits</h2>

          <div className="grid grid-cols-2 gap-4">
             <div>
                <label className="block text-xs text-slate-400 mb-1">Daily Hard Limit (₹)</label>
                <input
                  type="number"
                  value={riskConfig.daily_hard_limit}
                  onChange={(e) => handleRiskChange('daily_hard_limit', e.target.value)}
                  className="input-field"
                />
             </div>
             <div>
                <label className="block text-xs text-slate-400 mb-1">Per Trade Risk (₹)</label>
                <input
                  type="number"
                  value={riskConfig.per_trade_risk}
                  onChange={(e) => handleRiskChange('per_trade_risk', e.target.value)}
                  className="input-field"
                />
             </div>
             <div>
                <label className="block text-xs text-slate-400 mb-1">Max Open Positions</label>
                <input
                  type="number"
                  value={riskConfig.max_open_positions}
                  onChange={(e) => handleRiskChange('max_open_positions', e.target.value)}
                  className="input-field"
                />
             </div>
             <div>
                <label className="block text-xs text-slate-400 mb-1">Max Lots Per Trade</label>
                <input
                  type="number"
                  value={riskConfig.max_lots_per_trade}
                  onChange={(e) => handleRiskChange('max_lots_per_trade', e.target.value)}
                  className="input-field"
                />
             </div>
          </div>

          <h2 className="text-lg font-semibold text-slate-200 border-b border-border pb-2 mt-4 mb-2">Option Entry Criteria</h2>

          <div className="grid grid-cols-2 gap-4">
             <div>
                <label className="block text-xs text-slate-400 mb-1">Min Delta</label>
                <input
                  type="number"
                  step="0.01"
                  value={riskConfig.min_delta}
                  onChange={(e) => handleRiskChange('min_delta', e.target.value)}
                  className="input-field"
                />
             </div>
             <div>
                <label className="block text-xs text-slate-400 mb-1">Max Delta</label>
                <input
                  type="number"
                  step="0.01"
                  value={riskConfig.max_delta}
                  onChange={(e) => handleRiskChange('max_delta', e.target.value)}
                  className="input-field"
                />
             </div>
             <div>
                <label className="block text-xs text-slate-400 mb-1">Min Strike Volume</label>
                <input
                  type="number"
                  value={riskConfig.min_strike_volume}
                  onChange={(e) => handleRiskChange('min_strike_volume', e.target.value)}
                  className="input-field"
                />
             </div>
             <div>
                <label className="block text-xs text-slate-400 mb-1">No Trade After (HH:mm)</label>
                <input
                  type="time"
                  value={riskConfig.no_trade_after}
                  onChange={(e) => handleRiskChange('no_trade_after', e.target.value)}
                  className="input-field"
                />
             </div>
          </div>

          <div className="mt-4 pt-4 border-t border-border flex justify-end">
            <button
              type="submit"
              disabled={mutation.isPending}
              className="btn btn-primary"
            >
              {mutation.isPending ? 'Saving...' : 'Save Risk Config'}
            </button>
          </div>
        </form>

        <div className="card p-6 flex flex-col gap-4">
          <h2 className="text-lg font-semibold text-slate-200 border-b border-border pb-2 mb-2">Active Strategies</h2>

          {data?.strategies.map((strat) => (
             <div key={strat.name} className="bg-background border border-border p-4 rounded flex justify-between items-center">
                <div>
                   <h3 className="font-medium text-slate-200">{strat.name}</h3>
                   <p className="text-xs text-slate-400">Instruments: {strat.instruments.join(', ')}</p>
                </div>
                <div className="flex items-center gap-2">
                   <span className={`text-xs font-semibold px-2 py-1 rounded ${strat.enabled ? 'bg-success/20 text-success' : 'bg-slate-800 text-slate-500'}`}>
                     {strat.enabled ? 'ENABLED' : 'DISABLED'}
                   </span>
                </div>
             </div>
          ))}

          <div className="mt-4 text-xs text-slate-500">
             Note: Strategy parameters and enablement must be updated in the backend config files or via API.
          </div>
        </div>
      </div>
    </div>
  );
}