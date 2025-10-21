import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const TopProducts = ({ topProducts }) => {
  if (!topProducts || !topProducts.products || topProducts.products.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Топ-5 товаров</h3>
        <div className="bg-gray-200 dark:bg-gray-700 rounded h-64 animate-pulse"></div>
      </div>
    );
  }

  const data = {
    labels: topProducts.products.map(p => p.product_name),
    datasets: [
      {
        label: 'Выручка',
        data: topProducts.products.map(p => p.total_amount),
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(249, 115, 22, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(168, 85, 247, 0.8)'
        ],
        borderColor: [
          'rgb(59, 130, 246)',
          'rgb(16, 185, 129)',
          'rgb(249, 115, 22)',
          'rgb(239, 68, 68)',
          'rgb(168, 85, 247)'
        ],
        borderWidth: 1
      }
    ]
  };

  const options = {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = '';
            if (context.parsed.x !== null) {
              label = new Intl.NumberFormat('ru-RU', {
                style: 'currency',
                currency: 'RUB',
                minimumFractionDigits: 0
              }).format(context.parsed.x);
            }
            const product = topProducts.products[context.dataIndex];
            label += ` (${product.sales_count} продаж)`;
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return new Intl.NumberFormat('ru-RU', {
              style: 'currency',
              currency: 'RUB',
              minimumFractionDigits: 0,
              notation: 'compact'
            }).format(value);
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      y: {
        grid: {
          display: false
        }
      }
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Топ-5 товаров</h3>
      <div style={{ height: '300px' }}>
        <Bar data={data} options={options} />
      </div>
      <div className="mt-4 space-y-2">
        {topProducts.products.map((product, index) => (
          <div key={index} className="flex justify-between text-sm">
            <span className="text-gray-600 dark:text-gray-400 truncate flex-1">
              {index + 1}. {product.product_name}
            </span>
            <span className="text-gray-900 dark:text-white font-medium ml-2">
              {new Intl.NumberFormat('ru-RU', {
                style: 'currency',
                currency: 'RUB',
                minimumFractionDigits: 0
              }).format(product.total_amount)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TopProducts;
