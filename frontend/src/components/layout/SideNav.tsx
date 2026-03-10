import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  List,
  ActivitySquare,
  History,
  Settings
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/positions', label: 'Positions', icon: List },
  { path: '/option-chain', label: 'Option Chain', icon: ActivitySquare },
  { path: '/history', label: 'Trade History', icon: History },
  { path: '/config', label: 'Configuration', icon: Settings },
];

export function SideNav() {
  const location = useLocation();

  return (
    <nav className="w-64 bg-surface border-r border-border h-full flex flex-col">
      <div className="p-4 border-b border-border">
        <h1 className="text-xl font-bold text-primary flex items-center gap-2">
          <ActivitySquare className="h-6 w-6" />
          Options Bot
        </h1>
      </div>

      <div className="flex-1 py-4 flex flex-col gap-1 px-3">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={twMerge(
                clsx(
                  "flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                )
              )}
            >
              <Icon className="h-5 w-5" />
              {item.label}
            </Link>
          );
        })}
      </div>

      <div className="p-4 border-t border-border text-xs text-slate-500">
        v1.0.0
      </div>
    </nav>
  );
}