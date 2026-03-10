import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { useMarketStore } from '../../store/marketStore';
import { Position } from '../../types';
import { clsx } from 'clsx';

const columnHelper = createColumnHelper<Position>();

const columns = [
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
  columnHelper.accessor('current_ltp', {
    header: 'LTP',
    cell: info => info.getValue().toFixed(2),
  }),
  columnHelper.accessor('unrealised_pnl', {
    header: 'PnL',
    cell: info => {
      const val = info.getValue();
      return (
        <span className={clsx("font-medium", val >= 0 ? 'text-success' : 'text-danger')}>
          {val > 0 ? '+' : ''}{val.toFixed(2)}
        </span>
      );
    },
  }),
  columnHelper.accessor('strategy_name', {
    header: 'Strategy',
    cell: info => <span className="text-slate-400 text-sm">{info.getValue()}</span>,
  }),
];

export function PositionsTable() {
  const { positions } = useMarketStore();
  const openPositions = positions.filter(p => p.status === 'OPEN');

  const table = useReactTable({
    data: openPositions,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (openPositions.length === 0) {
    return (
      <div className="card p-8 flex flex-col items-center justify-center text-slate-400">
        <p className="text-sm">No active positions</p>
      </div>
    );
  }

  return (
    <div className="card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-slate-400 uppercase bg-surface/50 border-b border-border">
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(header => (
                  <th key={header.id} className="px-6 py-3 font-medium">
                    {flexRender(
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
          </tbody>
        </table>
      </div>
    </div>
  );
}