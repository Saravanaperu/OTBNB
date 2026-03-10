import { useEffect, useRef } from 'react';
import { useMarketStore } from '../../store/marketStore';

export function SignalTicker() {
  const { signals } = useMarketStore();
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Scroll to right on new signal
    if (containerRef.current) {
      containerRef.current.scrollLeft = containerRef.current.scrollWidth;
    }
  }, [signals]);

  if (signals.length === 0) {
    return (
      <div className="h-8 bg-surface border-y border-border flex items-center px-4 text-xs text-slate-500 overflow-hidden whitespace-nowrap overflow-x-auto w-full">
        Waiting for signals...
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="h-8 bg-surface border-y border-border flex items-center px-4 overflow-x-auto whitespace-nowrap no-scrollbar w-full shadow-inner z-20"
    >
      <div className="flex gap-4">
        {signals.map((signal, idx) => (
          <div key={idx} className="flex items-center gap-2 text-xs">
            <span className="text-slate-400">
              {new Date(signal.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'})}
            </span>
            <span className={signal.direction === 'BUY' ? 'text-success font-medium' : 'text-danger font-medium'}>
              {signal.direction}
            </span>
            <span className="text-slate-200">{signal.instrument}</span>
            <span className="text-primary">{signal.strike}</span>
            <span className="text-slate-400">({signal.strategy})</span>
            {idx < signals.length - 1 && (
              <span className="text-border mx-2">|</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}