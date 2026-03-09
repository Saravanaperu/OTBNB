import { render } from '@testing-library/react';
import App from '../App';
import { describe, it, expect } from 'vitest';

describe('App Component', () => {
  it('renders without crashing', () => {
    // The App component has a BrowserRouter, which renders the initial route.
    render(<App />);
    expect(document.body).toBeTruthy();
  });
});
