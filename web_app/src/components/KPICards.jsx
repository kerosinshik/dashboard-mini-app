import React from 'react';

const KPICard = ({ title, value, subtitle, icon }) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-gray-500 dark:text-gray-400">{title}</span>
        {icon && <span className="text-xl">{icon}</span>}
      </div>
      <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
        {value}
      </div>
      {subtitle && (
        <div className="text-xs text-gray-500 dark:text-gray-400">
          {subtitle}
        </div>
      )}
    </div>
  );
};

const KPICards = ({ stats }) => {
  if (!stats) {
    return (
      <div className="grid grid-cols-2 gap-4 mb-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-gray-200 dark:bg-gray-700 rounded-lg h-24 animate-pulse"></div>
        ))}
      </div>
    );
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0
    }).format(value);
  };

  return (
    <div className="grid grid-cols-2 gap-4 mb-6">
      <KPICard
        title="Выручка"
        value={formatCurrency(stats.total_amount)}
        icon="💰"
      />
      <KPICard
        title="Продажи"
        value={stats.total_sales}
        subtitle={`${stats.completed_sales} завершено`}
        icon="📊"
      />
      <KPICard
        title="Средний чек"
        value={formatCurrency(stats.average_check)}
        icon="💳"
      />
      <KPICard
        title="Конверсия"
        value={`${stats.conversion_rate}%`}
        subtitle={`${stats.pending_sales} в ожидании`}
        icon="📈"
      />
    </div>
  );
};

export default KPICards;
