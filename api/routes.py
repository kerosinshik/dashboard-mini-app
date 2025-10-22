from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import List
from collections import defaultdict
import os

from database.models import get_session, User, Sale
from database.seed import create_demo_data
from reports.pdf_generator import generate_pdf_report
from reports.excel_generator import generate_excel_report
from api.models import (
    SaleResponse,
    UserResponse,
    StatsResponse,
    ChartResponse,
    TopProduct,
    TopProductsResponse
)
from api.holidays import (
    get_upcoming_holidays,
    get_demand_forecast,
    get_peak_sales_periods,
    get_category_insights
)

router = APIRouter()


@router.get("/sales/{telegram_id}", response_model=List[SaleResponse])
async def get_user_sales(
    telegram_id: int,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """Получить продажи пользователя"""
    # Находим пользователя
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем продажи
    result = await session.execute(
        select(Sale)
        .where(Sale.user_id == user.id)
        .order_by(Sale.date.desc())
        .limit(limit)
    )
    sales = result.scalars().all()

    return sales


@router.get("/stats/{telegram_id}", response_model=StatsResponse)
async def get_user_stats(
    telegram_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Получить статистику пользователя"""
    # Находим пользователя
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем все продажи
    result = await session.execute(
        select(Sale).where(Sale.user_id == user.id)
    )
    sales = result.scalars().all()

    if not sales:
        return StatsResponse(
            total_amount=0,
            total_sales=0,
            average_check=0,
            completed_sales=0,
            pending_sales=0,
            cancelled_sales=0,
            conversion_rate=0
        )

    # Вычисляем статистику
    total_amount = sum(sale.amount * sale.quantity for sale in sales)
    total_sales = len(sales)
    completed_sales = len([s for s in sales if s.status == "completed"])
    pending_sales = len([s for s in sales if s.status == "pending"])
    cancelled_sales = len([s for s in sales if s.status == "cancelled"])

    average_check = total_amount / total_sales if total_sales > 0 else 0
    conversion_rate = (completed_sales / total_sales * 100) if total_sales > 0 else 0

    return StatsResponse(
        total_amount=round(total_amount, 2),
        total_sales=total_sales,
        average_check=round(average_check, 2),
        completed_sales=completed_sales,
        pending_sales=pending_sales,
        cancelled_sales=cancelled_sales,
        conversion_rate=round(conversion_rate, 2)
    )


@router.get("/charts/{telegram_id}/daily", response_model=ChartResponse)
async def get_daily_sales_chart(
    telegram_id: int,
    days: int = 30,
    session: AsyncSession = Depends(get_session)
):
    """Получить данные для графика продаж по дням"""
    # Находим пользователя
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем продажи за указанный период
    start_date = datetime.utcnow() - timedelta(days=days)
    result = await session.execute(
        select(Sale)
        .where(Sale.user_id == user.id)
        .where(Sale.date >= start_date)
        .where(Sale.status == "completed")
    )
    sales = result.scalars().all()

    # Группируем по дням
    daily_sales = defaultdict(float)
    for sale in sales:
        date_key = sale.date.strftime("%Y-%m-%d")
        daily_sales[date_key] += sale.amount * sale.quantity

    # Заполняем пропущенные дни
    labels = []
    values = []
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=days - i - 1)).strftime("%Y-%m-%d")
        labels.append(date)
        values.append(round(daily_sales.get(date, 0), 2))

    return ChartResponse(labels=labels, values=values)


@router.get("/charts/{telegram_id}/top-products", response_model=TopProductsResponse)
async def get_top_products(
    telegram_id: int,
    limit: int = 5,
    session: AsyncSession = Depends(get_session)
):
    """Получить топ товаров"""
    # Находим пользователя
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем агрегированные данные по товарам
    result = await session.execute(
        select(
            Sale.product_name,
            func.sum(Sale.amount * Sale.quantity).label("total_amount"),
            func.sum(Sale.quantity).label("total_quantity"),
            func.count(Sale.id).label("sales_count")
        )
        .where(Sale.user_id == user.id)
        .where(Sale.status == "completed")
        .group_by(Sale.product_name)
        .order_by(func.sum(Sale.amount * Sale.quantity).desc())
        .limit(limit)
    )

    products = []
    for row in result:
        products.append(TopProduct(
            product_name=row.product_name,
            total_amount=round(row.total_amount, 2),
            total_quantity=row.total_quantity,
            sales_count=row.sales_count
        ))

    return TopProductsResponse(products=products)


@router.post("/demo/{telegram_id}")
async def create_demo(
    telegram_id: int,
    username: str = None,
    first_name: str = None,
    session: AsyncSession = Depends(get_session)
):
    """Создать демо-данные для пользователя"""
    try:
        count = await create_demo_data(telegram_id, username, first_name)
        return {
            "success": True,
            "message": f"Создано {count} демо-продаж",
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{telegram_id}", response_model=UserResponse)
async def get_user(
    telegram_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Получить информацию о пользователе"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user


@router.get("/reports/{telegram_id}/pdf")
async def generate_pdf(
    telegram_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Сгенерировать PDF отчет"""
    # Получаем данные
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем статистику
    result = await session.execute(
        select(Sale).where(Sale.user_id == user.id)
    )
    sales_list = result.scalars().all()

    if not sales_list:
        raise HTTPException(status_code=404, detail="Нет данных для отчета")

    # Вычисляем статистику
    total_amount = sum(sale.amount * sale.quantity for sale in sales_list)
    total_sales = len(sales_list)
    completed_sales = len([s for s in sales_list if s.status == "completed"])
    pending_sales = len([s for s in sales_list if s.status == "pending"])
    cancelled_sales = len([s for s in sales_list if s.status == "cancelled"])
    average_check = total_amount / total_sales if total_sales > 0 else 0
    conversion_rate = (completed_sales / total_sales * 100) if total_sales > 0 else 0

    stats = {
        'total_amount': round(total_amount, 2),
        'total_sales': total_sales,
        'average_check': round(average_check, 2),
        'completed_sales': completed_sales,
        'pending_sales': pending_sales,
        'cancelled_sales': cancelled_sales,
        'conversion_rate': round(conversion_rate, 2)
    }

    # Получаем топ товары
    result = await session.execute(
        select(
            Sale.product_name,
            func.sum(Sale.amount * Sale.quantity).label("total_amount"),
            func.sum(Sale.quantity).label("total_quantity"),
            func.count(Sale.id).label("sales_count")
        )
        .where(Sale.user_id == user.id)
        .where(Sale.status == "completed")
        .group_by(Sale.product_name)
        .order_by(func.sum(Sale.amount * Sale.quantity).desc())
        .limit(5)
    )

    top_products = []
    for row in result:
        top_products.append({
            'product_name': row.product_name,
            'total_amount': round(row.total_amount, 2),
            'total_quantity': row.total_quantity,
            'sales_count': row.sales_count
        })

    # Конвертируем продажи в dict
    sales = [
        {
            'date': sale.date.isoformat(),
            'product_name': sale.product_name,
            'amount': sale.amount,
            'quantity': sale.quantity,
            'status': sale.status
        }
        for sale in sales_list[:50]  # Ограничиваем 50 продажами
    ]

    # Генерируем PDF
    user_name = user.first_name or user.username or f"User {telegram_id}"
    pdf_path = generate_pdf_report(stats, sales, top_products, user_name)

    return FileResponse(
        pdf_path,
        media_type='application/pdf',
        filename=f'sales_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )


@router.get("/reports/{telegram_id}/excel")
async def generate_excel(
    telegram_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Сгенерировать Excel отчет"""
    # Получаем данные (аналогично PDF)
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем статистику
    result = await session.execute(
        select(Sale).where(Sale.user_id == user.id)
    )
    sales_list = result.scalars().all()

    if not sales_list:
        raise HTTPException(status_code=404, detail="Нет данных для отчета")

    # Вычисляем статистику
    total_amount = sum(sale.amount * sale.quantity for sale in sales_list)
    total_sales = len(sales_list)
    completed_sales = len([s for s in sales_list if s.status == "completed"])
    pending_sales = len([s for s in sales_list if s.status == "pending"])
    cancelled_sales = len([s for s in sales_list if s.status == "cancelled"])
    average_check = total_amount / total_sales if total_sales > 0 else 0
    conversion_rate = (completed_sales / total_sales * 100) if total_sales > 0 else 0

    stats = {
        'total_amount': round(total_amount, 2),
        'total_sales': total_sales,
        'average_check': round(average_check, 2),
        'completed_sales': completed_sales,
        'pending_sales': pending_sales,
        'cancelled_sales': cancelled_sales,
        'conversion_rate': round(conversion_rate, 2)
    }

    # Получаем топ товары
    result = await session.execute(
        select(
            Sale.product_name,
            func.sum(Sale.amount * Sale.quantity).label("total_amount"),
            func.sum(Sale.quantity).label("total_quantity"),
            func.count(Sale.id).label("sales_count")
        )
        .where(Sale.user_id == user.id)
        .where(Sale.status == "completed")
        .group_by(Sale.product_name)
        .order_by(func.sum(Sale.amount * Sale.quantity).desc())
    )

    top_products = []
    for row in result:
        top_products.append({
            'product_name': row.product_name,
            'total_amount': round(row.total_amount, 2),
            'total_quantity': row.total_quantity,
            'sales_count': row.sales_count
        })

    # Конвертируем продажи в dict
    sales = [
        {
            'date': sale.date.isoformat(),
            'product_name': sale.product_name,
            'amount': sale.amount,
            'quantity': sale.quantity,
            'status': sale.status
        }
        for sale in sales_list
    ]

    # Генерируем Excel
    user_name = user.first_name or user.username or f"User {telegram_id}"
    excel_path = generate_excel_report(stats, sales, top_products, user_name)

    return FileResponse(
        excel_path,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename=f'sales_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    )


# Праздники и спрос
@router.get("/holidays/upcoming")
async def api_get_upcoming_holidays(days_ahead: int = 30):
    """Получить ближайшие праздники"""
    return {"holidays": get_upcoming_holidays(days_ahead)}


@router.get("/holidays/demand/{category}")
async def api_get_demand_forecast(category: str, days_ahead: int = 30):
    """Получить прогноз спроса на категорию товаров"""
    forecast = get_demand_forecast(category, days_ahead)
    if not forecast:
        raise HTTPException(status_code=404, detail=f"Категория '{category}' не найдена")
    return {"category": category, "forecast": forecast}


@router.get("/holidays/peaks")
async def api_get_peak_sales_periods():
    """Получить пиковые периоды продаж"""
    return {"peaks": get_peak_sales_periods()}


@router.get("/holidays/insights")
async def api_get_category_insights():
    """Получить инсайты по всем категориям"""
    return {"insights": get_category_insights()}
