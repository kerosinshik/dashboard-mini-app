from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os


def get_main_menu() -> InlineKeyboardMarkup:
    """Главное меню с основными функциями"""
    webapp_url = os.getenv("WEBAPP_URL", "https://localhost:3000")
    holidays_url = f"{webapp_url}?view=holidays"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Открыть дашборд", web_app=WebAppInfo(url=webapp_url))],
        [InlineKeyboardButton(text="🎉 Праздники → Спрос", web_app=WebAppInfo(url=holidays_url))],
        [InlineKeyboardButton(text="📄 PDF отчет", callback_data="report_pdf")],
        [InlineKeyboardButton(text="📊 Excel отчет", callback_data="report_excel")],
        [InlineKeyboardButton(text="🎯 Демо-режим", callback_data="demo_mode")]
    ])
    return keyboard


def get_report_menu() -> InlineKeyboardMarkup:
    """Меню выбора типа отчета"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 PDF отчет", callback_data="report_pdf")],
        [InlineKeyboardButton(text="📊 Excel отчет", callback_data="report_excel")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
    ])
    return keyboard


def get_period_menu() -> InlineKeyboardMarkup:
    """Меню выбора периода"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сегодня", callback_data="period_today")],
        [InlineKeyboardButton(text="Вчера", callback_data="period_yesterday")],
        [InlineKeyboardButton(text="Неделя", callback_data="period_week")],
        [InlineKeyboardButton(text="Месяц", callback_data="period_month")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
    ])
    return keyboard
