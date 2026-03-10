import { render } from '@testing-library/react';
import App from '../App';
import { describe, it, expect, beforeAll, afterAll } from 'vitest';

describe('App Component', () => {
  let originalConsoleWarn: typeof console.warn;
  let originalConsoleError: typeof console.error;

  beforeAll(() => {
    // Mock ResizeObserver for recharts
    (globalThis as any).ResizeObserver = class ResizeObserver {
      observe() {}
      unobserve() {}
      disconnect() {}
    };

    // Mute specific console.warn/error during tests
    originalConsoleWarn = console.warn;
    console.warn = (...args) => {
      if (typeof args[0] === 'string' && args[0].includes('The width(0) and height(0) of chart should be greater than 0')) {
        return;
      }
      originalConsoleWarn(...args);
    };
    originalConsoleError = console.error;
    console.error = (...args) => {
      if (typeof args[0] === 'string' && args[0].includes('WebSocket error')) {
        return;
      }
      if (typeof args[0] === 'string' && args[0].includes('API Error')) {
        return;
      }
      originalConsoleError(...args);
    };
  });

  afterAll(() => {
    console.warn = originalConsoleWarn;
    console.error = originalConsoleError;
  });

  it('renders without crashing', () => {
    // The App component has a BrowserRouter, which renders the initial route.
    render(<App />);
    expect(document.body).toBeTruthy();
  });
});
