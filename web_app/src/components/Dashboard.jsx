import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import KPICards from './KPICards';
import SalesChart from './SalesChart';
import TopProducts from './TopProducts';

const Dashboard = ({ telegramId }) => {
  const [stats, setStats] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [topProducts, setTopProducts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, [telegramId]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Загружаем все данные параллельно
      const [statsData, chartDataRes, topProductsData] = await Promise.all([
        api.getStats(telegramId),
        api.getDailySalesChart(telegramId, 30),
        api.getTopProducts(telegramId, 5)
      ]);

      setStats(statsData);
      setChartData(chartDataRes);
      setTopProducts(topProductsData);
    } catch (err) {
      console.error('Ошибка загрузки данных:', err);
      setError('Не удалось загрузить данные. Попробуйте позже.');
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="text-center">
          <div className="text-6xl mb-4">😕</div>
          <h2 className="text-xl font-bold mb-2 text-gray-900 dark:text-white">Ошибка</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
          <button
            onClick={loadData}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Попробовать снова
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Дашборд продаж
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Аналитика за последние 30 дней
          </p>
        </div>

        {/* KPI Cards */}
        <KPICards stats={stats} />

        {/* Sales Chart */}
        <SalesChart chartData={chartData} />

        {/* Top Products */}
        <TopProducts topProducts={topProducts} />

        {/* Refresh Button */}
        <div className="mt-6 text-center">
          <button
            onClick={loadData}
            disabled={loading}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Загрузка...' : 'Обновить данные'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
