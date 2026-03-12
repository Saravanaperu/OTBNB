import { X, CheckCircle2, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import { useToastStore, ToastType } from '../../store/toastStore';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

const icons: Record<ToastType, React.ElementType> = {
  success: CheckCircle2,
  error: AlertCircle,
  info: Info,
  warning: AlertTriangle,
};

const styles: Record<ToastType, string> = {
  success: 'bg-success/10 text-success border border-success/30',
  error: 'bg-danger/10 text-danger border border-danger/30',
  info: 'bg-primary/10 text-primary border border-primary/30',
  warning: 'bg-amber-500/10 text-amber-500 border border-amber-500/30',
};

export function ToastContainer() {
  const { toasts, removeToast } = useToastStore();

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
      {toasts.map((toast) => {
        const Icon = icons[toast.type];

        return (
          <div
            key={toast.id}
            className={twMerge(
              clsx(
                "flex items-center gap-3 px-4 py-3 rounded-md shadow-lg pointer-events-auto backdrop-blur-sm transition-all duration-300 transform translate-y-0 opacity-100",
                styles[toast.type]
              )
            )}
            role="alert"
          >
            <Icon className="h-5 w-5 shrink-0" />
            <p className="text-sm font-medium pr-4">{toast.message}</p>
            <button
              onClick={() => removeToast(toast.id)}
              className="ml-auto p-1 rounded hover:bg-black/10 transition-colors"
              aria-label="Close"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        );
      })}
    </div>
  );
}