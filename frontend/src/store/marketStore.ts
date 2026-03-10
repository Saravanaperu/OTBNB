import { create } from 'zustand';
import { Position, OptionChain, RiskBudget, DailyPnL } from '../types';

interface Signal {
  timestamp: string;
  direction: 'BUY' | 'SELL';
  instrument: string;
  strike: number;
  strategy: string;
}

interface MarketState {
  signals: Signal[];
  addSignal: (signal: Signal) => void;

  positions: Position[];
  setPositions: (positions: Position[]) => void;
  updatePosition: (position: Position) => void;
  removePosition: (positionId: string) => void;

  optionChains: Record<string, OptionChain>;
  setOptionChain: (instrument: string, chain: OptionChain) => void;

  riskBudget: RiskBudget | null;
  setRiskBudget: (budget: RiskBudget) => void;

  dailyPnL: DailyPnL | null;
  setDailyPnL: (pnl: DailyPnL) => void;
}

export const useMarketStore = create<MarketState>((set) => ({
  signals: [],
  addSignal: (signal) => set((state) => ({
    signals: [...state.signals, signal].slice(-50)
  })),

  positions: [],
  setPositions: (positions) => set({ positions }),
  updatePosition: (updatedPosition) => set((state) => {
    const exists = state.positions.find(p => p.position_id === updatedPosition.position_id);
    if (exists) {
      return {
        positions: state.positions.map(p =>
          p.position_id === updatedPosition.position_id ? updatedPosition : p
        )
      };
    }
    // If it doesn't exist, add it
    return { positions: [...state.positions, updatedPosition] };
  }),
  removePosition: (positionId) => set((state) => ({
    positions: state.positions.filter(p => p.position_id !== positionId)
  })),

  optionChains: {},
  setOptionChain: (instrument, chain) => set((state) => ({
    optionChains: {
      ...state.optionChains,
      [instrument]: chain
    }
  })),

  riskBudget: null,
  setRiskBudget: (budget) => set({ riskBudget: budget }),

  dailyPnL: null,
  setDailyPnL: (pnl) => set({ dailyPnL: pnl })
}));