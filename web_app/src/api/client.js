import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

export const api = {
  // Получить статистику пользователя
  getStats: async (telegramId) => {
    const response = await apiClient.get(`/stats/${telegramId}`);
    return response.data;
  },

  // Получить список продаж
  getSales: async (telegramId, limit = 100) => {
    const response = await apiClient.get(`/sales/${telegramId}`, {
      params: { limit }
    });
    return response.data;
  },

  // Получить данные для графика продаж по дням
  getDailySalesChart: async (telegramId, days = 30) => {
    const response = await apiClient.get(`/charts/${telegramId}/daily`, {
      params: { days }
    });
    return response.data;
  },

  // Получить топ товаров
  getTopProducts: async (telegramId, limit = 5) => {
    const response = await apiClient.get(`/charts/${telegramId}/top-products`, {
      params: { limit }
    });
    return response.data;
  },

  // Создать демо-данные
  createDemo: async (telegramId, username, firstName) => {
    const response = await apiClient.post(`/demo/${telegramId}`, null, {
      params: { username, first_name: firstName }
    });
    return response.data;
  },

  // Получить информацию о пользователе
  getUser: async (telegramId) => {
    const response = await apiClient.get(`/user/${telegramId}`);
    return response.data;
  }
};

export default apiClient;
