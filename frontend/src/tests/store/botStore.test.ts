import { describe, it, expect, beforeEach } from 'vitest';
import { useBotStore } from '../../store/botStore';

describe('botStore', () => {
  beforeEach(() => {
    // Reset the store before each test
    useBotStore.setState({
      isRunning: false,
      isConnected: false,
    });
  });

  it('should have correct initial state', () => {
    const state = useBotStore.getState();
    expect(state.isRunning).toBe(false);
    expect(state.isConnected).toBe(false);
  });

  it('should toggle isRunning using toggleBot', () => {
    const store = useBotStore.getState();

    // Initial state is false
    expect(useBotStore.getState().isRunning).toBe(false);

    // Toggle to true
    store.toggleBot();
    expect(useBotStore.getState().isRunning).toBe(true);

    // Toggle back to false
    useBotStore.getState().toggleBot();
    expect(useBotStore.getState().isRunning).toBe(false);
  });

  it('should set connection status using setConnectionStatus', () => {
    const store = useBotStore.getState();

    store.setConnectionStatus(true);
    expect(useBotStore.getState().isConnected).toBe(true);

    store.setConnectionStatus(false);
    expect(useBotStore.getState().isConnected).toBe(false);
  });

  it('should set bot status using setBotStatus', () => {
    const store = useBotStore.getState();

    store.setBotStatus(true);
    expect(useBotStore.getState().isRunning).toBe(true);

    store.setBotStatus(false);
    expect(useBotStore.getState().isRunning).toBe(false);
  });
});
