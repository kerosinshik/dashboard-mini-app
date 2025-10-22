from datetime import datetime, timedelta
from typing import List, Dict

# Российские праздники 2025
RUSSIAN_HOLIDAYS = {
    "2025-01-01": {"name": "Новый год", "category": "major", "products": ["шампанское", "фейерверки", "подарки"]},
    "2025-01-07": {"name": "Рождество", "category": "major", "products": ["сладости", "подарки детям"]},
    "2025-02-14": {"name": "День святого Валентина", "category": "commercial", "products": ["цветы", "конфеты", "подарки"]},
    "2025-02-23": {"name": "День защитника Отечества", "category": "major", "products": ["алкоголь", "мужские подарки", "сувениры"]},
    "2025-03-08": {"name": "Международный женский день", "category": "major", "products": ["цветы", "духи", "украшения", "косметика"]},
    "2025-05-01": {"name": "Праздник Весны и Труда", "category": "major", "products": ["шашлык", "уголь", "пикник"]},
    "2025-05-09": {"name": "День Победы", "category": "major", "products": ["цветы", "георгиевская лента"]},
    "2025-06-12": {"name": "День России", "category": "major", "products": ["флаги", "сувениры"]},
    "2025-09-01": {"name": "День знаний", "category": "seasonal", "products": ["школьные принадлежности", "цветы", "рюкзаки"]},
    "2025-11-04": {"name": "День народного единства", "category": "major", "products": []},
    "2025-12-31": {"name": "Новый год (подготовка)", "category": "major", "products": ["елки", "украшения", "подарки", "шампанское"]}
}

# Средний рост спроса по категориям (в процентах)
DEMAND_PATTERNS = {
    "цветы": {
        "2025-02-14": 280,  # +280% к обычному спросу
        "2025-03-08": 350,
        "2025-09-01": 200
    },
    "алкоголь": {
        "2025-02-23": 180,
        "2025-12-31": 300,
        "2025-01-01": 150
    },
    "подарки": {
        "2025-12-31": 400,
        "2025-03-08": 250,
        "2025-02-14": 200,
        "2025-02-23": 150
    },
    "школьные принадлежности": {
        "2025-09-01": 500
    },
    "шампанское": {
        "2025-12-31": 450,
        "2025-01-01": 200
    },
    "сувениры": {
        "2025-02-23": 180,
        "2025-03-08": 150
    }
}


def get_upcoming_holidays(days_ahead: int = 30) -> List[Dict]:
    """Получить ближайшие праздники"""
    today = datetime.now()
    upcoming = []

    for date_str, info in RUSSIAN_HOLIDAYS.items():
        holiday_date = datetime.strptime(date_str, "%Y-%m-%d")
        days_until = (holiday_date - today).days

        if 0 <= days_until <= days_ahead:
            upcoming.append({
                "date": date_str,
                "name": info["name"],
                "category": info["category"],
                "days_until": days_until,
                "products": info["products"],
                "week_before": days_until <= 14,
                "urgent": days_until <= 7
            })

    return sorted(upcoming, key=lambda x: x["days_until"])


def get_demand_forecast(product_category: str, days_ahead: int = 30) -> List[Dict]:
    """Прогноз спроса на товарную категорию"""
    today = datetime.now()
    forecast = []

    if product_category not in DEMAND_PATTERNS:
        return []

    pattern = DEMAND_PATTERNS[product_category]

    for date_str, demand_increase in pattern.items():
        holiday_date = datetime.strptime(date_str, "%Y-%m-%d")
        days_until = (holiday_date - today).days

        if 0 <= days_until <= days_ahead:
            holiday_info = RUSSIAN_HOLIDAYS.get(date_str, {})
            forecast.append({
                "date": date_str,
                "holiday": holiday_info.get("name", ""),
                "days_until": days_until,
                "demand_increase": demand_increase,
                "peak_week": days_until <= 7
            })

    return sorted(forecast, key=lambda x: x["days_until"])


def get_peak_sales_periods() -> List[Dict]:
    """Пиковые периоды продаж на ближайший месяц"""
    holidays = get_upcoming_holidays(30)
    peaks = []

    for holiday in holidays:
        if holiday["products"]:
            peaks.append({
                "period": f"{holiday['days_until']} дней до {holiday['name']}",
                "date": holiday["date"],
                "days_until": holiday["days_until"],
                "holiday": holiday["name"],
                "top_products": holiday["products"][:3],
                "alert_level": "high" if holiday["urgent"] else "medium" if holiday["week_before"] else "low"
            })

    return peaks


def get_category_insights() -> List[Dict]:
    """Инсайты по всем категориям"""
    insights = []

    for category in DEMAND_PATTERNS.keys():
        forecast = get_demand_forecast(category, 30)
        if forecast:
            next_peak = forecast[0]
            insights.append({
                "category": category,
                "next_holiday": next_peak["holiday"],
                "days_until": next_peak["days_until"],
                "expected_growth": next_peak["demand_increase"],
                "recommendation": f"Пик через {next_peak['days_until']} дней. Прогноз: +{next_peak['demand_increase']}%"
            })

    return sorted(insights, key=lambda x: x["days_until"])
