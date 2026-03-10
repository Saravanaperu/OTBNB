import { create } from 'zustand';

interface BotState {
  isRunning: boolean;
  isConnected: boolean;
  toggleBot: () => void;
  setConnectionStatus: (status: boolean) => void;
  setBotStatus: (status: boolean) => void;
}

export const useBotStore = create<BotState>((set) => ({
  isRunning: false,
  isConnected: false,
  toggleBot: () => set((state) => ({ isRunning: !state.isRunning })),
  setConnectionStatus: (status) => set({ isConnected: status }),
  setBotStatus: (status) => set({ isRunning: status }),
}));