import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000;

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config;

    // Only retry on network errors or 5xx server errors
    if (!config || (error.response && error.response.status < 500)) {
      console.error('API Error:', error);
      return Promise.reject(error);
    }

    config.retryCount = config.retryCount || 0;

    if (config.retryCount >= MAX_RETRIES) {
      console.error(`API Error: Max retries (${MAX_RETRIES}) reached.`, error);
      return Promise.reject(error);
    }

    config.retryCount += 1;

    // Exponential backoff
    const delay = RETRY_DELAY * Math.pow(2, config.retryCount - 1);
    console.warn(`API Error: Retrying request (Attempt ${config.retryCount}) in ${delay}ms...`);

    await new Promise(resolve => setTimeout(resolve, delay));

    return apiClient(config);
  }
);
