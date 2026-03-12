import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ToastContainer } from '../../../components/ui/Toast';
import { useToastStore } from '../../../store/toastStore';

describe('Toast Component', () => {
  beforeEach(() => {
    // Reset store before each test
    useToastStore.setState({ toasts: [] });
  });

  it('renders nothing when there are no toasts', () => {
    const { container } = render(<ToastContainer />);
    // The container element should be there but empty of toasts
    expect(container.querySelector('[role="alert"]')).toBeNull();
  });

  it('renders a toast message when one is added', () => {
    // Add a toast
    useToastStore.getState().addToast('Test Error Message', 'error');

    render(<ToastContainer />);

    // Toast should be visible
    expect(screen.getByText('Test Error Message')).toBeTruthy();
    expect(screen.getByRole('alert')).toBeTruthy();
  });

  it('renders multiple toasts', () => {
    // Add multiple toasts
    useToastStore.getState().addToast('Message 1', 'info');
    useToastStore.getState().addToast('Message 2', 'success');

    render(<ToastContainer />);

    // Both toasts should be visible
    expect(screen.getByText('Message 1')).toBeTruthy();
    expect(screen.getByText('Message 2')).toBeTruthy();
    expect(screen.getAllByRole('alert')).toHaveLength(2);
  });

  it('removes a toast when the close button is clicked', () => {
    // Mock the state and functions manually to prevent timing issues in the store
    const mockRemoveToast = vi.fn();

    // We mock the state to have exactly one toast
    useToastStore.setState({
      toasts: [{ id: 'toast-1', message: 'Dismissible Message', type: 'warning' }],
      removeToast: mockRemoveToast
    });

    render(<ToastContainer />);

    const closeButton = screen.getByLabelText('Close');
    expect(closeButton).toBeTruthy();

    fireEvent.click(closeButton);

    // Verify the remove function was called
    expect(mockRemoveToast).toHaveBeenCalledWith('toast-1');
  });

  it('applies correct styling based on toast type', () => {
    useToastStore.setState({
      toasts: [
        { id: '1', message: 'Success', type: 'success' },
        { id: '2', message: 'Error', type: 'error' },
      ],
    });

    const { container } = render(<ToastContainer />);

    // We can't easily test tailwind utility classes perfectly, but we can look for our custom ones
    const alerts = container.querySelectorAll('[role="alert"]');
    expect(alerts).toHaveLength(2);

    // First should be success
    expect(alerts[0].className).toContain('text-success');
    expect(alerts[0].className).toContain('border-success/30');

    // Second should be error
    expect(alerts[1].className).toContain('text-danger');
    expect(alerts[1].className).toContain('border-danger/30');
  });
});
