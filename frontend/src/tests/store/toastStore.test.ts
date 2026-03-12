import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { useToastStore } from '../../store/toastStore';

describe('toastStore', () => {
  beforeEach(() => {
    // Reset the store before each test
    useToastStore.setState({
      toasts: [],
    });
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should have an empty initial state', () => {
    const state = useToastStore.getState();
    expect(state.toasts).toEqual([]);
  });

  it('should add a toast with default values', () => {
    const store = useToastStore.getState();

    store.addToast('Test Message');

    const { toasts } = useToastStore.getState();
    expect(toasts).toHaveLength(1);
    expect(toasts[0].message).toBe('Test Message');
    expect(toasts[0].type).toBe('info');
    expect(toasts[0].id).toBeDefined();
  });

  it('should add a toast with custom type', () => {
    const store = useToastStore.getState();

    store.addToast('Error Occurred', 'error');

    const { toasts } = useToastStore.getState();
    expect(toasts).toHaveLength(1);
    expect(toasts[0].message).toBe('Error Occurred');
    expect(toasts[0].type).toBe('error');
  });

  it('should remove a toast by id', () => {
    const store = useToastStore.getState();

    store.addToast('Test Message');
    const { toasts } = useToastStore.getState();
    const id = toasts[0].id;

    useToastStore.getState().removeToast(id);

    expect(useToastStore.getState().toasts).toHaveLength(0);
  });

  it('should automatically remove toast after duration', () => {
    const store = useToastStore.getState();

    store.addToast('Timeout Message', 'info', 1000);

    let { toasts } = useToastStore.getState();
    expect(toasts).toHaveLength(1);

    vi.advanceTimersByTime(1000);

    toasts = useToastStore.getState().toasts;
    expect(toasts).toHaveLength(0);
  });

  it('should not automatically remove toast if duration is 0', () => {
    const store = useToastStore.getState();

    store.addToast('Persistent Message', 'info', 0);

    let { toasts } = useToastStore.getState();
    expect(toasts).toHaveLength(1);

    vi.advanceTimersByTime(5000);

    toasts = useToastStore.getState().toasts;
    expect(toasts).toHaveLength(1);
  });
});
