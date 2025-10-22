import { useState, useEffect } from 'react';
import { api } from '../api/client';

function HolidayDemand() {
  const [insights, setInsights] = useState([]);
  const [peaks, setPeaks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadHolidayData();
  }, []);

  const loadHolidayData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [insightsData, peaksData] = await Promise.all([
        api.getCategoryInsights(),
        api.getPeakSalesPeriods()
      ]);

      setInsights(insightsData.insights || []);
      setPeaks(peaksData.peaks || []);
    } catch (err) {
      console.error('Ошибка загрузки данных:', err);
      setError('Не удалось загрузить данные о праздниках');
    } finally {
      setLoading(false);
    }
  };

  const getAlertColor = (level) => {
    switch (level) {
      case 'high': return 'bg-red-100 text-red-800 border-red-300';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      default: return 'bg-blue-100 text-blue-800 border-blue-300';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-8">
        <div className="text-red-600 text-lg mb-4">{error}</div>
        <button
          onClick={loadHolidayData}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Попробовать снова
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-4">🎉 Праздники → Спрос</h2>
        <p className="text-gray-600 mb-6">
          Прогноз спроса на товары в период ближайших праздников
        </p>
      </div>

      {/* Пиковые периоды продаж */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">📊 Пиковые периоды продаж</h3>
        {peaks.length === 0 ? (
          <p className="text-gray-500">Нет ближайших праздников в следующие 30 дней</p>
        ) : (
          <div className="space-y-3">
            {peaks.map((peak, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border-2 ${getAlertColor(peak.alert_level)}`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <div className="font-semibold text-lg">{peak.holiday}</div>
                    <div className="text-sm opacity-80 mt-1">
                      {peak.days_until === 0 ? 'Сегодня' : `Через ${peak.days_until} ${peak.days_until === 1 ? 'день' : 'дней'}`}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs font-medium uppercase">
                      {peak.alert_level === 'high' ? '🔥 Срочно' : peak.alert_level === 'medium' ? '⚠️ Скоро' : '📅 Заранее'}
                    </div>
                  </div>
                </div>
                {peak.top_products && peak.top_products.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {peak.top_products.map((product, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-white rounded-full text-sm font-medium"
                      >
                        {product}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Инсайты по категориям */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">💡 Прогноз по категориям</h3>
        {insights.length === 0 ? (
          <p className="text-gray-500">Нет прогнозов на ближайшие 30 дней</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {insights.map((insight, index) => (
              <div
                key={index}
                className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-400 transition-colors"
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="font-semibold text-lg capitalize">{insight.category}</div>
                  <div className="text-2xl font-bold text-green-600">
                    +{insight.expected_growth}%
                  </div>
                </div>
                <div className="text-sm text-gray-600 mb-1">{insight.next_holiday}</div>
                <div className="text-xs text-gray-500">
                  {insight.days_until === 0 ? 'Сегодня' : `Через ${insight.days_until} ${insight.days_until === 1 ? 'день' : 'дней'}`}
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <div className="text-sm text-gray-700">{insight.recommendation}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Информация */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 border border-blue-200">
        <h4 className="font-semibold text-gray-800 mb-2">ℹ️ Как использовать прогноз</h4>
        <ul className="text-sm text-gray-700 space-y-1 list-disc list-inside">
          <li>🔥 <strong>Срочно</strong> - праздник через 7 дней или меньше, подготовьте товары</li>
          <li>⚠️ <strong>Скоро</strong> - праздник через 8-14 дней, начните подготовку</li>
          <li>📅 <strong>Заранее</strong> - праздник через 15-30 дней, спланируйте закупки</li>
          <li>💡 Процент показывает ожидаемый рост спроса относительно обычных дней</li>
        </ul>
      </div>
    </div>
  );
}

export default HolidayDemand;
