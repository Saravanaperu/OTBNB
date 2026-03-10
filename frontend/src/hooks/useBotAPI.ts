import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../services/apiClient';
import { Trade, RiskConfig, StrategyConfig, Position } from '../types';

export const useGetHealth = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const { data } = await apiClient.get('/status/health');
      return data;
    },
    refetchInterval: 5000,
  });
};

export const useGetStatus = () => {
  return useQuery({
    queryKey: ['status'],
    queryFn: async () => {
      const { data } = await apiClient.get('/status/');
      return data;
    },
    refetchInterval: 5000,
  });
};

export const usePauseBot = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post('/status/bot/pause');
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['status'] });
      queryClient.invalidateQueries({ queryKey: ['health'] });
    },
  });
};

export const useResumeBot = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post('/status/bot/resume');
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['status'] });
      queryClient.invalidateQueries({ queryKey: ['health'] });
    },
  });
};

export const useGetTrades = () => {
  return useQuery<Trade[]>({
    queryKey: ['trades'],
    queryFn: async () => {
      const { data } = await apiClient.get('/trades');
      return data;
    },
  });
};

export const useGetRiskConfig = () => {
  return useQuery<RiskConfig>({
    queryKey: ['riskConfig'],
    queryFn: async () => {
      const { data } = await apiClient.get('/config/risk');
      return data;
    },
  });
};

export const useUpdateRiskConfig = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (config: RiskConfig) => {
      const { data } = await apiClient.put('/config/risk', config);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['riskConfig'] });
    },
  });
};

export const useGetStrategies = () => {
  return useQuery<StrategyConfig[]>({
    queryKey: ['strategies'],
    queryFn: async () => {
      const { data } = await apiClient.get('/config/strategies');
      return data;
    },
  });
};

export const useUpdateStrategy = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ name, config }: { name: string; config: StrategyConfig }) => {
      const { data } = await apiClient.put(`/config/strategies/${name}`, config);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['strategies'] });
    },
  });
};

export const useGetPositions = () => {
  return useQuery<Position[]>({
    queryKey: ['positions'],
    queryFn: async () => {
      const { data } = await apiClient.get('/positions/');
      return data;
    },
  });
};
