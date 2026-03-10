import { useState } from 'react';
import { useMarketStore } from '../store/marketStore';
import { clsx } from 'clsx';
import { format } from 'date-fns';

export function OptionChain() {
  const { optionChains } = useMarketStore();
  const [selectedInstrument, setSelectedInstrument] = useState<string>('NIFTY');

  // Hardcode available instruments for now. Ideally this comes from the store.
  const instruments = ['NIFTY', 'BANKNIFTY'];

  const currentChain = optionChains[selectedInstrument];

  if (!currentChain) {
    return (
      <div className="p-6 h-full flex flex-col gap-6">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-2xl font-bold text-white mb-1">Option Chain</h1>
            <p className="text-slate-400 text-sm">Real-time option chain analysis</p>
          </div>

          <div className="flex gap-2">
            {instruments.map(inst => (
              <button
                key={inst}
                className={clsx(
                  "btn btn-outline text-sm",
                  selectedInstrument === inst && "bg-primary text-white border-primary"
                )}
                onClick={() => setSelectedInstrument(inst)}
              >
                {inst}
              </button>
            ))}
          </div>
        </div>

        <div className="card p-8 flex flex-col items-center justify-center text-slate-400 flex-1">
          <p className="text-sm">Waiting for live option chain data for {selectedInstrument}...</p>
        </div>
      </div>
    );
  }

  const strikes = Object.keys(currentChain.strikes).map(Number).sort((a, b) => a - b);
  const atmStrike = currentChain.atm_strike;

  return (
    <div className="p-6 h-full flex flex-col gap-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Option Chain</h1>
          <p className="text-slate-400 text-sm">
            Spot: <span className="font-semibold text-slate-200">{currentChain.spot.toFixed(2)}</span> |
            ATM: <span className="font-semibold text-slate-200">{atmStrike}</span> |
            Updated: {format(new Date(currentChain.updated_at), 'HH:mm:ss')}
          </p>
        </div>

        <div className="flex gap-2">
          {instruments.map(inst => (
            <button
              key={inst}
              className={clsx(
                "btn btn-outline text-sm",
                selectedInstrument === inst && "bg-primary text-white border-primary"
              )}
              onClick={() => setSelectedInstrument(inst)}
            >
              {inst}
            </button>
          ))}
        </div>
      </div>

      <div className="card overflow-hidden flex-1 flex flex-col">
        <div className="overflow-auto flex-1 h-0">
          <table className="w-full text-xs text-center border-collapse">
            <thead className="bg-surface/50 border-b-2 border-border sticky top-0 z-10 shadow-sm">
              <tr>
                <th colSpan={4} className="py-2 border-r border-border bg-danger/10 text-danger font-semibold uppercase tracking-wider">CALLS</th>
                <th className="py-2 px-4 bg-surface text-slate-300 font-semibold w-24">STRIKE</th>
                <th colSpan={4} className="py-2 border-l border-border bg-success/10 text-success font-semibold uppercase tracking-wider">PUTS</th>
              </tr>
              <tr className="text-slate-400 border-b border-border bg-background">
                <th className="py-2 px-2 font-medium border-r border-border/50">OI</th>
                <th className="py-2 px-2 font-medium border-r border-border/50">Delta</th>
                <th className="py-2 px-2 font-medium border-r border-border/50">IV</th>
                <th className="py-2 px-2 font-medium border-r border-border">LTP</th>

                <th className="py-2 px-2 font-semibold bg-surface">Price</th>

                <th className="py-2 px-2 font-medium border-l border-border">LTP</th>
                <th className="py-2 px-2 font-medium border-l border-border/50">IV</th>
                <th className="py-2 px-2 font-medium border-l border-border/50">Delta</th>
                <th className="py-2 px-2 font-medium border-l border-border/50">OI</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/50 bg-surface">
              {strikes.map(strike => {
                const ce = currentChain.strikes[strike].CE;
                const pe = currentChain.strikes[strike].PE;
                const isATM = strike === atmStrike;

                return (
                  <tr key={strike} className={clsx("hover:bg-slate-800 transition-colors", isATM && "bg-primary/10")}>
                    {/* Calls */}
                    <td className={clsx("py-2 px-2 border-r border-border/50 text-slate-300", strike < atmStrike && "bg-danger/5")}>
                      {(ce.oi / 1000).toFixed(1)}k
                    </td>
                    <td className={clsx("py-2 px-2 border-r border-border/50", strike < atmStrike && "bg-danger/5", ce.delta > 0.5 ? "text-slate-200" : "text-slate-500")}>
                      {ce.delta.toFixed(2)}
                    </td>
                    <td className={clsx("py-2 px-2 border-r border-border/50 text-slate-400", strike < atmStrike && "bg-danger/5")}>
                      {ce.iv.toFixed(1)}%
                    </td>
                    <td className={clsx("py-2 px-2 border-r border-border font-medium text-slate-200", strike < atmStrike && "bg-danger/5")}>
                      {ce.ltp.toFixed(2)}
                    </td>

                    {/* Strike */}
                    <td className={clsx("py-2 px-4 font-bold tracking-wide border-x border-border", isATM ? "text-primary bg-primary/20" : "text-slate-300 bg-background")}>
                      {strike}
                    </td>

                    {/* Puts */}
                    <td className={clsx("py-2 px-2 border-l border-border font-medium text-slate-200", strike > atmStrike && "bg-success/5")}>
                      {pe.ltp.toFixed(2)}
                    </td>
                    <td className={clsx("py-2 px-2 border-l border-border/50 text-slate-400", strike > atmStrike && "bg-success/5")}>
                      {pe.iv.toFixed(1)}%
                    </td>
                    <td className={clsx("py-2 px-2 border-l border-border/50", strike > atmStrike && "bg-success/5", pe.delta < -0.5 ? "text-slate-200" : "text-slate-500")}>
                      {pe.delta.toFixed(2)}
                    </td>
                    <td className={clsx("py-2 px-2 border-l border-border/50 text-slate-300", strike > atmStrike && "bg-success/5")}>
                      {(pe.oi / 1000).toFixed(1)}k
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Footer Metrics */}
        <div className="bg-background border-t border-border p-4 flex justify-between items-center text-sm">
          <div className="flex gap-6">
             <div>Total Call OI: <span className="font-semibold text-danger">{(currentChain.total_call_oi / 100000).toFixed(2)}Cr</span></div>
             <div>Total Put OI: <span className="font-semibold text-success">{(currentChain.total_put_oi / 100000).toFixed(2)}Cr</span></div>
          </div>
          <div className="flex gap-6">
             <div>PCR (OI): <span className={clsx("font-semibold", currentChain.pcr_oi > 1 ? "text-success" : "text-danger")}>{currentChain.pcr_oi.toFixed(2)}</span></div>
             <div>IV Rank: <span className="font-semibold text-slate-200">{currentChain.iv_rank.toFixed(1)}</span></div>
          </div>
        </div>
      </div>
    </div>
  );
}