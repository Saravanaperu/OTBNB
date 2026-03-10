import { useEffect, useRef } from 'react';
import { useBotStore } from '../store/botStore';
import { useMarketStore } from '../store/marketStore';

const WS_URL = (import.meta as any).env?.VITE_WS_URL || 'ws://localhost:8000/ws/live?token=dashboard_secret';

export function useWebSocket() {
  const ws = useRef<WebSocket | null>(null);
  const { setConnectionStatus } = useBotStore();
  const { addSignal, updatePosition, setOptionChain, setRiskBudget, setDailyPnL } = useMarketStore();
  const reconnectTimeoutRef = useRef<number | null>(null);
  const reconnectAttemptsRef = useRef<number>(0);
  const maxReconnectDelay = 30000;
  const initialReconnectDelay = 1000;

  useEffect(() => {
    connect();

    return () => {
      if (ws.current) {
        ws.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  const connect = () => {
    if (ws.current?.readyState === WebSocket.OPEN) return;

    ws.current = new WebSocket(WS_URL);

    ws.current.onopen = () => {
      setConnectionStatus(true);
      reconnectAttemptsRef.current = 0; // Reset attempts on successful connection
      console.log('WebSocket connected');
    };

    ws.current.onclose = () => {
      setConnectionStatus(false);

      const attempts = reconnectAttemptsRef.current;
      // Exponential backoff with a cap
      const delay = Math.min(initialReconnectDelay * Math.pow(2, attempts), maxReconnectDelay);

      console.log(`WebSocket disconnected. Reconnecting in ${delay}ms...`);

      reconnectTimeoutRef.current = window.setTimeout(() => {
        reconnectAttemptsRef.current += 1;
        connect();
      }, delay);
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      ws.current?.close();
    };

    ws.current.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        handleEvent(payload);
      } catch (err) {
        console.error('Error parsing WS message', err);
      }
    };
  };

  const handleEvent = (payload: any) => {
    const { event, data } = payload;

    switch (event) {
      case 'signal':
        addSignal(data);
        break;
      case 'position_update':
        if (data.status === 'CLOSED') {
           // We might want to remove it from active positions and perhaps add it to history
           // For now, we update it and it can be filtered out by views if needed.
           // Or explicitly remove it if views rely on positions being purely active
           updatePosition(data);
        } else {
           updatePosition(data);
        }
        break;
      case 'option_chain_update':
        setOptionChain(data.instrument, data);
        break;
      case 'risk_update':
        setRiskBudget(data);
        break;
      case 'pnl_update':
        setDailyPnL(data);
        break;
      default:
        console.warn('Unknown event received:', event);
    }
  };

  return {
    ws: ws.current,
  };
}