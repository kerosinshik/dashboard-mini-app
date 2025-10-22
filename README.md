# Dashboard Mini App для Telegram

Telegram бот с встроенным Mini App для визуализации данных продаж и генерации отчетов.

## 🚀 Технологии

### Backend
- **Python 3.12** - основной язык
- **aiogram 3.x** - Telegram Bot framework
- **FastAPI** - REST API
- **SQLAlchemy + SQLite** - база данных
- **ReportLab & openpyxl** - генерация PDF/Excel отчетов

### Frontend
- **React + Vite** - современный фронтенд
- **Tailwind CSS** - стилизация
- **Chart.js** - графики и визуализация
- **Telegram WebApp SDK** - интеграция с Telegram

## 📦 Что делают сервисы

### Vercel (для фронтенда)
- **Бесплатный хостинг** React приложения
- **Автоматический HTTPS** - готовый SSL сертификат
- **Глобальный CDN** - быстрая загрузка из любой точки мира
- **Автодеплой** - при каждом push в GitHub автоматически обновляется сайт
- **Бесплатный домен** - получаете URL типа `https://ваш-проект.vercel.app`

### Railway (для API и базы данных)
- **Бесплатный хостинг** FastAPI приложения (500 часов/месяц бесплатно)
- **Автоматический HTTPS** - готовый SSL сертификат
- **База данных SQLite** - хранится вместе с приложением
- **Автодеплой** - при каждом push автоматически обновляется
- **Бесплатный домен** - получаете URL типа `https://ваш-проект.up.railway.app`

## 🎯 Функционал бота

- **📊 Дашборд** - интерактивные графики продаж
- **📄 PDF отчеты** - красивые отчеты с таблицами и графиками
- **📊 Excel отчеты** - детальная аналитика в 4 листах
- **🎯 Демо-режим** - автоматическая генерация тестовых данных

## 🛠 Локальная разработка

### Установка зависимостей

```bash
# Python зависимости
pip install -r requirements.txt

# Frontend зависимости
cd web_app
npm install
```

### Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните:

```bash
cp .env.example .env
```

### Запуск в режиме разработки

**Терминал 1: API**
```bash
python -m uvicorn api.main:app --reload --port 8000
```

**Терминал 2: Frontend**
```bash
cd web_app
npm run dev
```

**Терминал 3: Bot**
```bash
python -m bot.main
```

## 📊 Структура проекта

```
dashboard_app/
├── bot/                    # Telegram бот
│   ├── main.py            # Точка входа
│   ├── handlers.py        # Обработчики команд
│   └── keyboards.py       # Клавиатуры
├── api/                   # FastAPI приложение
│   ├── main.py           # REST API
│   ├── routes.py         # Endpoints
│   └── models.py         # Pydantic модели
├── database/             # База данных
│   ├── models.py        # SQLAlchemy модели
│   └── seed.py          # Генератор демо-данных
├── reports/             # Генераторы отчетов
│   ├── pdf_generator.py
│   └── excel_generator.py
├── web_app/            # React Mini App
│   ├── src/
│   │   ├── components/ # React компоненты
│   │   └── api/       # API клиент
│   └── index.html
└── requirements.txt    # Python зависимости
```

## 🌐 Деплой на продакшн

### Vercel (Frontend)
1. Создайте репозиторий на GitHub
2. Залейте код
3. Подключите репозиторий к Vercel
4. Vercel автоматически задеплоит `web_app/`

### Railway (Backend)
1. Подключите тот же репозиторий к Railway
2. Railway автоматически обнаружит Python и задеплоит API
3. Скопируйте URL API и обновите `.env` фронтенда

## 📝 Переменные окружения

### Backend (.env)
```
BOT_TOKEN=ваш_токен_от_BotFather
WEBAPP_URL=https://ваш-проект.vercel.app
API_URL=https://ваш-проект.up.railway.app
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

### Frontend (web_app/.env)
```
VITE_API_URL=https://ваш-проект.up.railway.app/api
```

## 🎨 Демо-сценарий

1. Пользователь запускает бота `/start`
2. Нажимает "🎯 Демо-режим" - создаются тестовые данные
3. Нажимает "📊 Открыть дашборд" - открывается Mini App с графиками
4. Может сгенерировать PDF или Excel отчет одной кнопкой

## 🔄 Обновление проекта после изменений

### Изменения в коде

```bash
# 1. Внесите изменения в файлы
# 2. Добавьте изменения в git
git add .

# 3. Создайте коммит с описанием
git commit -m "Описание изменений"

# 4. Загрузите на GitHub
git push
```

**Автоматические деплои:**
- ✅ **Railway** (API и Бот) - автоматически передеплоится через 2-3 минуты
- ✅ **Vercel** (Frontend) - автоматически пересоберется через 1-2 минуты

### Изменения переменных окружения

**Railway (API и Бот):**
1. Откройте нужный сервис в Railway
2. Перейдите на вкладку **Variables**
3. Измените переменную
4. Railway автоматически перезапустит сервис

**Vercel (Frontend):**
1. Откройте проект на Vercel
2. **Settings** → **Environment Variables**
3. Измените переменную
4. **Deployments** → последний деплой → **⋮** → **Redeploy**

### Изменения в структуре БД

Если изменили `database/models.py`:
```bash
git add database/models.py
git commit -m "Update database schema"
git push
```

Railway автоматически применит изменения при следующем деплое.

**⚠️ Важно:** При изменении структуры БД существующие данные могут быть потеряны. Для продакшена используйте миграции (Alembic).

## 🐛 Решение проблем

### Бот не отвечает
- Проверьте логи в Railway (вкладка Deployments → View Logs)
- Убедитесь что `BOT_TOKEN` правильный
- Проверьте что только один экземпляр бота запущен (не локально и не в Railway одновременно)

### Дашборд не загружает данные
- Проверьте что `VITE_API_URL` на Vercel указывает на Railway API
- Откройте `https://ваш-api.up.railway.app/api/stats/ваш_telegram_id` в браузере
- Проверьте консоль браузера (F12 → Console) на ошибки

### Отчеты не генерируются
- Убедитесь что создали демо-данные через "🎯 Демо-режим"
- Проверьте логи API сервиса в Railway

### Railway показывает "Build failed"
- Проверьте что `requirements.txt` содержит все зависимости
- Проверьте логи сборки в Railway
- Убедитесь что Python версия 3.12 (файл `runtime.txt`)

## 📚 Полезные ссылки

- [Документация aiogram](https://docs.aiogram.dev/)
- [Документация FastAPI](https://fastapi.tiangolo.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram WebApp документация](https://core.telegram.org/bots/webapps)
- [Railway документация](https://docs.railway.app/)
- [Vercel документация](https://vercel.com/docs)

## 🎯 Что можно улучшить

- [ ] Добавить авторизацию пользователей
- [ ] Интеграция с реальными CRM (Битрикс24, amoCRM)
- [ ] Система прав доступа (админ, менеджер, просмотр)
- [ ] Экспорт графиков как изображений
- [ ] Мультиязычность (RU/EN)
- [ ] Кастомизация дашборда (выбор виджетов)
- [ ] Push-уведомления о важных метриках
- [ ] Использование PostgreSQL вместо SQLite для продакшена
- [ ] Добавить миграции БД (Alembic)
- [ ] Unit и integration тесты
- [ ] CI/CD pipeline с автоматическим тестированием
- [ ] Monitoring и логирование (Sentry)
- [ ] Rate limiting для API
- [ ] Кэширование данных (Redis)

## 👨‍💻 Автор

Создано с использованием Claude Code

## 📄 Лицензия

MIT
