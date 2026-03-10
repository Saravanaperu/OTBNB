import { useEffect } from 'react';
import { Play, Square, Wifi, WifiOff } from 'lucide-react';
import { clsx } from 'clsx';
import { useBotStore } from '../../store/botStore';
import { useGetStatus, usePauseBot, useResumeBot } from '../../hooks/useBotAPI';

export function TopBar() {
  const { isRunning, isConnected, setBotStatus } = useBotStore();
  const { data: statusData } = useGetStatus();
  const pauseMutation = usePauseBot();
  const resumeMutation = useResumeBot();

  useEffect(() => {
    if (statusData) {
      setBotStatus(statusData.bot_running);
    }
  }, [statusData, setBotStatus]);

  const toggleBot = () => {
    if (isRunning) {
      pauseMutation.mutate();
    } else {
      resumeMutation.mutate();
    }
  };

  return (
    <div className="h-16 bg-surface border-b border-border flex items-center justify-between px-6 shrink-0 w-full z-10 sticky top-0">
      <div className="flex items-center gap-4">
        <h2 className="text-lg font-semibold text-slate-200 hidden sm:block">
          Dashboard Control
        </h2>
      </div>

      <div className="flex items-center gap-6">
        {/* Connection Status */}
        <div className="flex items-center gap-2">
          {isConnected ? (
            <>
              <Wifi className="h-4 w-4 text-success" />
              <span className="text-xs font-medium text-success hidden sm:inline-block">Connected</span>
            </>
          ) : (
            <>
              <WifiOff className="h-4 w-4 text-danger" />
              <span className="text-xs font-medium text-danger hidden sm:inline-block">Disconnected</span>
            </>
          )}
        </div>

        {/* Bot Status Indicator */}
        <div className="flex items-center gap-3 bg-background border border-border px-3 py-1.5 rounded-full">
          <div className={clsx(
            "h-2.5 w-2.5 rounded-full animate-pulse",
            isRunning ? "bg-success" : "bg-danger"
          )} />
          <span className="text-sm font-medium text-slate-300">
            {isRunning ? 'Bot Active' : 'Bot Stopped'}
          </span>
        </div>

        {/* Master Control */}
        <button
          onClick={toggleBot}
          className={clsx(
            "flex items-center gap-2 px-4 py-2 rounded-md font-medium text-sm transition-all duration-200 shadow-sm",
            isRunning
              ? "bg-danger/10 text-danger border border-danger/30 hover:bg-danger/20"
              : "bg-success/10 text-success border border-success/30 hover:bg-success/20"
          )}
        >
          {isRunning ? (
            <>
              <Square className="h-4 w-4 fill-current" />
              Stop Bot
            </>
          ) : (
            <>
              <Play className="h-4 w-4 fill-current" />
              Start Bot
            </>
          )}
        </button>
      </div>
    </div>
  );
}