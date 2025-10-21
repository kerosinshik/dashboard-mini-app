import os
import aiohttp
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import WebAppInfo
from bot.keyboards import get_main_menu, get_report_menu, get_period_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я бот для визуализации данных и создания отчетов.\n\n"
        "🎯 Попробуйте демо-режим, чтобы увидеть все возможности!\n\n"
        "Выберите действие:"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu())


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "📖 Справка по командам:\n\n"
        "/start - Главное меню\n"
        "/dashboard - Открыть дашборд\n"
        "/report - Меню генерации отчетов\n"
        "/demo - Запустить демо-режим\n"
        "/help - Показать эту справку\n\n"
        "💡 Используйте кнопки меню для быстрой навигации!"
    )
    await message.answer(help_text, reply_markup=get_main_menu())


@router.message(Command("dashboard"))
async def cmd_dashboard(message: Message):
    """Обработчик команды /dashboard"""
    webapp_url = os.getenv("WEBAPP_URL", "https://example.com")
    await message.answer(
        "📊 Открываю дашборд...\n"
        "(Пока в разработке, будет доступно после создания Mini App)"
    )


@router.message(Command("report"))
async def cmd_report(message: Message):
    """Обработчик команды /report"""
    await message.answer(
        "📈 Выберите тип отчета:",
        reply_markup=get_report_menu()
    )


@router.message(Command("demo"))
async def cmd_demo(message: Message):
    """Обработчик команды /demo"""
    await message.answer(
        "🎯 Демо-режим активирован!\n\n"
        "Генерирую тестовые данные для вашего аккаунта...\n"
        "(Функционал будет доступен после создания API и БД)"
    )


# Обработчики callback-кнопок
@router.callback_query(F.data == "open_dashboard")
async def callback_open_dashboard(callback: CallbackQuery):
    """Открытие дашборда"""
    await callback.message.answer(
        "📊 Дашборд будет доступен после создания Mini App!"
    )
    await callback.answer()


@router.callback_query(F.data == "report_today")
async def callback_report_today(callback: CallbackQuery):
    """Отчет за сегодня"""
    await callback.message.answer(
        "📈 Генерирую отчет за сегодня...\n"
        "(Функционал будет доступен после создания генератора отчетов)"
    )
    await callback.answer()


@router.callback_query(F.data == "report_month")
async def callback_report_month(callback: CallbackQuery):
    """Отчет за месяц"""
    await callback.message.answer(
        "📅 Генерирую отчет за месяц...\n"
        "(Функционал будет доступен после создания генератора отчетов)"
    )
    await callback.answer()


@router.callback_query(F.data == "demo_mode")
async def callback_demo_mode(callback: CallbackQuery):
    """Активация демо-режима"""
    telegram_id = callback.from_user.id
    username = callback.from_user.username
    first_name = callback.from_user.first_name

    api_url = os.getenv("API_URL", "http://localhost:8000")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{api_url}/api/demo/{telegram_id}",
                params={"username": username, "first_name": first_name}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    await callback.message.answer(
                        f"🎯 Демо-режим активирован!\n\n"
                        f"✅ Создано {data['count']} тестовых продаж за последние 30 дней\n"
                        f"✅ Сгенерированы случайные товары и суммы\n"
                        f"✅ Добавлены различные статусы\n\n"
                        f"Теперь вы можете открыть дашборд или создать отчет!"
                    )
                    await callback.answer("Демо-данные созданы!")
                else:
                    await callback.message.answer("❌ Ошибка создания демо-данных")
                    await callback.answer()
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {str(e)}")
        await callback.answer()


@router.callback_query(F.data == "report_pdf")
async def callback_report_pdf(callback: CallbackQuery):
    """Генерация PDF отчета"""
    telegram_id = callback.from_user.id
    api_url = os.getenv("API_URL", "http://localhost:8000")

    await callback.message.answer("📄 Генерирую PDF отчет, подождите...")
    await callback.answer()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{api_url}/api/reports/{telegram_id}/pdf") as response:
                if response.status == 200:
                    # Сохраняем файл
                    content = await response.read()
                    file_path = f"/tmp/report_{telegram_id}.pdf"
                    with open(file_path, 'wb') as f:
                        f.write(content)

                    # Отправляем файл пользователю
                    document = FSInputFile(file_path)
                    await callback.message.answer_document(
                        document,
                        caption="📄 Ваш PDF отчет готов!"
                    )

                    # Удаляем временный файл
                    os.remove(file_path)
                else:
                    await callback.message.answer("❌ Ошибка генерации отчета. Убедитесь, что у вас есть данные.")
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {str(e)}")


@router.callback_query(F.data == "report_excel")
async def callback_report_excel(callback: CallbackQuery):
    """Генерация Excel отчета"""
    telegram_id = callback.from_user.id
    api_url = os.getenv("API_URL", "http://localhost:8000")

    await callback.message.answer("📊 Генерирую Excel отчет, подождите...")
    await callback.answer()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{api_url}/api/reports/{telegram_id}/excel") as response:
                if response.status == 200:
                    # Сохраняем файл
                    content = await response.read()
                    file_path = f"/tmp/report_{telegram_id}.xlsx"
                    with open(file_path, 'wb') as f:
                        f.write(content)

                    # Отправляем файл пользователю
                    document = FSInputFile(file_path)
                    await callback.message.answer_document(
                        document,
                        caption="📊 Ваш Excel отчет готов!"
                    )

                    # Удаляем временный файл
                    os.remove(file_path)
                else:
                    await callback.message.answer("❌ Ошибка генерации отчета. Убедитесь, что у вас есть данные.")
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {str(e)}")


@router.callback_query(F.data == "back_main")
async def callback_back_main(callback: CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_menu()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("period_"))
async def callback_period(callback: CallbackQuery):
    """Обработка выбора периода"""
    period = callback.data.split("_")[1]
    period_names = {
        "today": "сегодня",
        "yesterday": "вчера",
        "week": "неделю",
        "month": "месяц"
    }
    await callback.message.answer(
        f"Выбран период: {period_names.get(period, period)}\n"
        "Генерирую отчет..."
    )
    await callback.answer()
