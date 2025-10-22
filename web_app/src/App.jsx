import React, { useEffect, useState } from 'react';
import Dashboard from './components/Dashboard';
import HolidayDemand from './components/HolidayDemand';

function App() {
  const [telegramId, setTelegramId] = useState(null);
  const [isReady, setIsReady] = useState(false);
  const [view, setView] = useState('dashboard'); // 'dashboard' или 'holidays'

  useEffect(() => {
    // Инициализация Telegram Web App
    if (window.Telegram && window.Telegram.WebApp) {
      const tg = window.Telegram.WebApp;

      // Разворачиваем приложение на весь экран
      tg.expand();

      // Включаем закрывающую кнопку
      tg.enableClosingConfirmation();

      // Получаем данные пользователя
      if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        setTelegramId(tg.initDataUnsafe.user.id);
      } else {
        // Для разработки используем тестовый ID
        console.warn('Telegram WebApp не инициализирован, используется тестовый ID');
        setTelegramId(123456789);
      }

      // Проверяем URL параметры для переключения вида
      const urlParams = new URLSearchParams(window.location.search);
      const viewParam = urlParams.get('view');
      if (viewParam === 'holidays') {
        setView('holidays');
      }

      setIsReady(true);
    } else {
      // Для разработки вне Telegram
      console.warn('Запуск вне Telegram, используется тестовый ID');
      setTelegramId(123456789);

      // Проверяем URL параметры
      const urlParams = new URLSearchParams(window.location.search);
      const viewParam = urlParams.get('view');
      if (viewParam === 'holidays') {
        setView('holidays');
      }

      setIsReady(true);
    }
  }, []);

  if (!isReady) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Загрузка...</p>
        </div>
      </div>
    );
  }

  if (!telegramId) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-bold mb-2 text-gray-900 dark:text-white">
            Ошибка инициализации
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Не удалось получить данные пользователя
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {view === 'dashboard' ? (
        <Dashboard telegramId={telegramId} />
      ) : (
        <div className="container mx-auto px-4 py-6">
          <HolidayDemand />
        </div>
      )}
    </div>
  );
}

export default App;
