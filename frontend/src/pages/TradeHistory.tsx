import { useQuery } from '@tanstack/react-query';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getPaginationRowModel,
} from '@tanstack/react-table';
import { Trade } from '../types';
import { clsx } from 'clsx';
import { format } from 'date-fns';

const fetchTrades = async (): Promise<Trade[]> => {
  // In a real app, this would fetch from the backend:
  // const res = await fetch('http://localhost:8000/api/v1/trades');
  // return res.json();

  // For now, return mock data
  return Array.from({ length: 50 }).map((_, i) => ({
    id: `TRD-${i}`,
    instrument: 'NIFTY',
    tradingsymbol: `NIFTY24APR22000CE`,
    direction: i % 2 === 0 ? 'BUY' : 'SELL',
    strike: 22000,
    expiry: '2024-04-25',
    lots: 1,
    quantity: 50,
    entry_price: 100 + Math.random() * 50,
    entry_time: new Date(Date.now() - (i * 3600000)).toISOString(),
    exit_price: i % 3 === 0 ? undefined : (100 + Math.random() * 100),
    exit_time: i % 3 === 0 ? undefined : new Date(Date.now() - (i * 3600000) + 1800000).toISOString(),
    realised_pnl: i % 3 === 0 ? undefined : (Math.random() > 0.5 ? Math.random() * 1000 : -Math.random() * 500),
    strategy_name: 'MomentumBreakout',
    order_id_entry: `ORD-E-${i}`,
    status: i % 3 === 0 ? 'OPEN' : 'CLOSED',
  }));
};

const columnHelper = createColumnHelper<Trade>();

const columns = [
  columnHelper.accessor('entry_time', {
    header: 'Entry Time',
    cell: info => <span className="text-slate-300">{format(new Date(info.getValue()), 'MMM dd, HH:mm')}</span>,
  }),
  columnHelper.accessor('tradingsymbol', {
    header: 'Symbol',
    cell: info => <span className="font-medium text-slate-200">{info.getValue()}</span>,
  }),
  columnHelper.accessor('direction', {
    header: 'Side',
    cell: info => {
      const val = info.getValue();
      return (
        <span className={clsx("px-2 py-0.5 rounded text-xs font-semibold", val === 'BUY' ? 'bg-success/20 text-success' : 'bg-danger/20 text-danger')}>
          {val}
        </span>
      );
    },
  }),
  columnHelper.accessor('quantity', {
    header: 'Qty',
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('entry_price', {
    header: 'Entry',
    cell: info => info.getValue().toFixed(2),
  }),
  columnHelper.accessor('exit_price', {
    header: 'Exit',
    cell: info => {
      const val = info.getValue();
      return val ? val.toFixed(2) : '-';
    },
  }),
  columnHelper.accessor('realised_pnl', {
    header: 'Realised PnL',
    cell: info => {
      const val = info.getValue();
      if (val === undefined) return '-';
      return (
        <span className={clsx("font-medium", val >= 0 ? 'text-success' : 'text-danger')}>
          {val > 0 ? '+' : ''}{val.toFixed(2)}
        </span>
      );
    },
  }),
  columnHelper.accessor('status', {
    header: 'Status',
    cell: info => {
      const val = info.getValue();
      return (
        <span className={clsx("px-2 py-0.5 rounded text-xs font-medium border",
          val === 'CLOSED' ? 'border-slate-600 text-slate-400' : 'border-primary/50 text-primary'
        )}>
          {val}
        </span>
      );
    },
  }),
];

export function TradeHistory() {
  const { data: trades, isLoading } = useQuery({
    queryKey: ['trades'],
    queryFn: fetchTrades,
  });

  const table = useReactTable({
    data: trades || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: {
      pagination: {
        pageSize: 10,
      },
    },
  });

  return (
    <div className="p-6 h-full w-full flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Trade History</h1>
        <p className="text-slate-400 text-sm">Review past trades and performance</p>
      </div>

      <div className="card flex-1 flex flex-col overflow-hidden">
        {isLoading ? (
          <div className="flex-1 flex items-center justify-center text-slate-400">
            Loading trades...
          </div>
        ) : (
          <>
            <div className="flex-1 overflow-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-slate-400 uppercase bg-surface/50 border-b border-border sticky top-0 z-10">
                  {table.getHeaderGroups().map(headerGroup => (
                    <tr key={headerGroup.id}>
                      {headerGroup.headers.map(header => (
                        <th key={header.id} className="px-6 py-3 font-medium bg-surface">
                          {header.isPlaceholder
                            ? null
                            : flexRender(
                                header.column.columnDef.header,
                                header.getContext()
                              )}
                        </th>
                      ))}
                    </tr>
                  ))}
                </thead>
                <tbody className="divide-y divide-border">
                  {table.getRowModel().rows.map(row => (
                    <tr key={row.id} className="hover:bg-slate-800/50 transition-colors">
                      {row.getVisibleCells().map(cell => (
                        <td key={cell.id} className="px-6 py-4 whitespace-nowrap">
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </td>
                      ))}
                    </tr>
                  ))}
                  {table.getRowModel().rows.length === 0 && (
                    <tr>
                      <td colSpan={columns.length} className="px-6 py-8 text-center text-slate-400">
                        No trades found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <div className="flex items-center justify-between px-6 py-3 border-t border-border bg-surface/50 text-sm">
              <div className="flex items-center gap-2 text-slate-400">
                <span>
                  Page <span className="font-medium text-slate-200">{table.getState().pagination.pageIndex + 1}</span> of{' '}
                  <span className="font-medium text-slate-200">{table.getPageCount()}</span>
                </span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => table.previousPage()}
                  disabled={!table.getCanPreviousPage()}
                  className="btn btn-outline py-1 px-3 text-xs"
                >
                  Previous
                </button>
                <button
                  onClick={() => table.nextPage()}
                  disabled={!table.getCanNextPage()}
                  className="btn btn-outline py-1 px-3 text-xs"
                >
                  Next
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}