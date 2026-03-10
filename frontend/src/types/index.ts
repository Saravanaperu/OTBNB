export interface Position {
  position_id: string;
  instrument: string;
  tradingsymbol: string;
  token: string;
  direction: 'BUY' | 'SELL';
  strike: number;
  expiry: string;
  entry_price: number;
  entry_time: string;
  lots: number;
  lot_size: number;
  quantity: number;
  entry_greeks?: Record<string, number>;
  sl_price: number;
  target_price: number;
  trailing_sl_active: boolean;
  trailing_sl_price: number;
  peak_price: number;
  current_ltp: number;
  unrealised_pnl: number;
  unrealised_pnl_pct: number;
  status: 'OPEN' | 'CLOSED';
  strategy_name: string;
}

export interface ClosedPosition extends Position {
  exit_price: number;
  exit_time: string;
  exit_reason: string;
  realised_pnl: number;
}

export interface DailyPnL {
  date: string;
  trade_count: number;
  win_count: number;
  gross_profit: number;
  gross_loss: number;
  net_pnl: number;
}

export interface Trade {
  id: string;
  instrument: string;
  tradingsymbol: string;
  direction: 'BUY' | 'SELL';
  strike: number;
  expiry: string;
  lots: number;
  quantity: number;
  entry_price: number;
  entry_time: string;
  exit_price?: number;
  exit_time?: string;
  exit_reason?: string;
  realised_pnl?: number;
  entry_delta?: number;
  entry_iv?: number;
  entry_iv_rank?: number;
  strategy_name: string;
  order_id_entry: string;
  order_id_exit?: string;
  status: 'OPEN' | 'CLOSED' | 'CANCELLED';
}

export interface OptionData {
  ltp: number;
  bid: number;
  ask: number;
  iv: number;
  delta: number;
  gamma: number;
  theta: number;
  vega: number;
  oi: number;
  oi_change: number;
  volume: number;
}

export interface StrikeData {
  CE: OptionData;
  PE: OptionData;
}

export interface OptionChain {
  instrument: string;
  expiry: string;
  spot: number;
  atm_strike: number;
  updated_at: string;
  pcr_oi: number;
  pcr_volume: number;
  total_call_oi: number;
  total_put_oi: number;
  iv_rank: number;
  iv_percentile: number;
  strikes: Record<number, StrikeData>;
}

export interface RiskBudget {
  daily_loss_used: number;
  remaining_budget: number;
  open_position_count: number;
}

export interface RiskConfig {
  daily_hard_limit: number;
  daily_soft_limit: number;
  per_trade_risk: number;
  max_open_positions: number;
  max_same_instrument: number;
  max_lots_per_trade: number;
  max_capital_pct: number;
  iv_rank_buy_threshold: number;
  min_delta: number;
  max_delta: number;
  max_theta_daily_pct: number;
  min_strike_volume: number;
  min_strike_oi: number;
  max_bid_ask_spread_pct: number;
  no_trade_after: string;
  no_0dte_after: string;
}

export interface StrategyConfig {
  name: string;
  enabled: boolean;
  instruments: string[];
  params: Record<string, any>;
}