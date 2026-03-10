import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SideNav } from './components/layout/SideNav';
import { TopBar } from './components/layout/TopBar';
import { SignalTicker } from './components/layout/SignalTicker';
import { useWebSocket } from './hooks/useWebSocket';

// Pages
import { HomeDashboard } from './pages/HomeDashboard';
import { TradeHistory } from './pages/TradeHistory';
import { Configuration } from './pages/Configuration';
import { OptionChain } from './pages/OptionChain';

// Placeholder Pages
const Positions = () => <div className="p-6 h-full w-full">Positions Content</div>;

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
const queryClient = new QueryClient();

function App() {
  // Initialize WebSocket connection on app mount
  useWebSocket();

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <div className="flex h-screen bg-background text-slate-100 overflow-hidden font-sans antialiased selection:bg-primary/30">
          <SideNav />
          <div className="flex-1 flex flex-col h-full min-w-0">
            <TopBar />
            <SignalTicker />
            <main className="flex-1 overflow-y-auto no-scrollbar relative w-full h-full bg-background/50">
              <Routes>
                <Route path="/" element={<HomeDashboard />} />
                <Route path="/positions" element={<Positions />} />
                <Route path="/option-chain" element={<OptionChain />} />
                <Route path="/history" element={<TradeHistory />} />
                <Route path="/config" element={<Configuration />} />
              </Routes>
            </main>
          </div>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;