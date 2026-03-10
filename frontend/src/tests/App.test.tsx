import { render } from '@testing-library/react';
import App from '../App';
import { describe, it, expect, beforeAll } from 'vitest';

describe('App Component', () => {
  beforeAll(() => {
    // Mock ResizeObserver for recharts
    (globalThis as any).ResizeObserver = class ResizeObserver {
      observe() {}
      unobserve() {}
      disconnect() {}
    };
  });

  it('renders without crashing', () => {
    // The App component has a BrowserRouter, which renders the initial route.
    render(<App />);
    expect(document.body).toBeTruthy();
  });
});
