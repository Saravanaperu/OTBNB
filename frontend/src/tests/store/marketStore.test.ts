import { describe, it, expect, beforeEach } from 'vitest';
import { useMarketStore } from '../../store/marketStore';

describe('marketStore', () => {
  beforeEach(() => {
    // Reset the store before each test
    useMarketStore.setState({
      signals: [],
      positions: [],
      optionChains: {},
      riskBudget: null,
      dailyPnL: null,
    });
  });

  it('should have an empty initial state', () => {
    const state = useMarketStore.getState();
    expect(state.signals).toEqual([]);
    expect(state.positions).toEqual([]);
    expect(state.optionChains).toEqual({});
    expect(state.riskBudget).toBeNull();
    expect(state.dailyPnL).toBeNull();
  });

  it('should add a signal and keep only the latest 50', () => {
    const store = useMarketStore.getState();

    // Add one signal
    store.addSignal({
      timestamp: '2023-01-01T00:00:00Z',
      direction: 'BUY',
      instrument: 'NIFTY',
      strike: 22000,
      strategy: 'Strategy1'
    });

    expect(useMarketStore.getState().signals).toHaveLength(1);

    // Add 50 more signals
    for (let i = 0; i < 50; i++) {
      useMarketStore.getState().addSignal({
        timestamp: `2023-01-01T00:${i.toString().padStart(2, '0')}:00Z`,
        direction: 'SELL',
        instrument: 'BANKNIFTY',
        strike: 45000,
        strategy: 'Strategy2'
      });
    }

    // Should only have 50 signals
    expect(useMarketStore.getState().signals).toHaveLength(50);
    // The first signal should be gone
    expect(useMarketStore.getState().signals[0].instrument).toBe('BANKNIFTY');
  });

  it('should set positions', () => {
    const store = useMarketStore.getState();
    const positions: any[] = [{ position_id: '1', symbol: 'NIFTY22000CE', quantity: 50 }];

    store.setPositions(positions);

    expect(useMarketStore.getState().positions).toEqual(positions);
  });

  it('should update an existing position', () => {
    const store = useMarketStore.getState();
    const positions: any[] = [{ position_id: '1', symbol: 'NIFTY22000CE', quantity: 50, current_price: 100 }];
    store.setPositions(positions);

    const updatedPosition: any = { position_id: '1', symbol: 'NIFTY22000CE', quantity: 50, current_price: 120 };
    useMarketStore.getState().updatePosition(updatedPosition);

    expect(useMarketStore.getState().positions[0].current_price).toBe(120);
  });

  it('should add a position if it does not exist during update', () => {
    const store = useMarketStore.getState();
    const positions: any[] = [{ position_id: '1', symbol: 'NIFTY22000CE', quantity: 50, current_price: 100 }];
    store.setPositions(positions);

    const newPosition: any = { position_id: '2', symbol: 'BANKNIFTY45000PE', quantity: 15, current_price: 200 };
    useMarketStore.getState().updatePosition(newPosition);

    expect(useMarketStore.getState().positions).toHaveLength(2);
    expect(useMarketStore.getState().positions[1]).toEqual(newPosition);
  });

  it('should remove a position', () => {
    const store = useMarketStore.getState();
    const positions: any[] = [
      { position_id: '1', symbol: 'NIFTY22000CE', quantity: 50 },
      { position_id: '2', symbol: 'BANKNIFTY45000PE', quantity: 15 }
    ];
    store.setPositions(positions);

    useMarketStore.getState().removePosition('1');

    expect(useMarketStore.getState().positions).toHaveLength(1);
    expect(useMarketStore.getState().positions[0].position_id).toBe('2');
  });

  it('should set an option chain', () => {
    const store = useMarketStore.getState();
    const chain: any = { spot: 22000, timestamp: '123' };

    store.setOptionChain('NIFTY', chain);

    expect(useMarketStore.getState().optionChains['NIFTY']).toEqual(chain);
  });

  it('should set risk budget', () => {
    const store = useMarketStore.getState();
    const budget: any = { daily_limit: 5000, current_drawdown: 1000 };

    store.setRiskBudget(budget);

    expect(useMarketStore.getState().riskBudget).toEqual(budget);
  });

  it('should set daily PnL', () => {
    const store = useMarketStore.getState();
    const pnl: any = { date: '2023-01-01', total_mtm: 1000, realized_pnl: 500 };

    store.setDailyPnL(pnl);

    expect(useMarketStore.getState().dailyPnL).toEqual(pnl);
  });
});
