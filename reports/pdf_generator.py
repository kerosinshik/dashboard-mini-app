from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime
from io import BytesIO
import tempfile


def generate_pdf_report(stats, sales, top_products, user_name="Пользователь"):
    """Генерация PDF отчета"""

    # Создаем временный файл для PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf_path = temp_file.name
    temp_file.close()

    # Создаем документ
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    # Стили
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#374151'),
        spaceAfter=12,
        spaceBefore=20
    )

    # Элементы документа
    elements = []

    # Заголовок
    title = Paragraph("Отчет о продажах", title_style)
    elements.append(title)

    # Дата и пользователь
    date_text = f"<para align=center>Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}<br/>Пользователь: {user_name}</para>"
    elements.append(Paragraph(date_text, styles['Normal']))
    elements.append(Spacer(1, 20))

    # Сводные показатели
    elements.append(Paragraph("Сводные показатели", heading_style))

    kpi_data = [
        ['Показатель', 'Значение'],
        ['Общая выручка', f"{stats['total_amount']:,.2f} ₽"],
        ['Всего продаж', str(stats['total_sales'])],
        ['Средний чек', f"{stats['average_check']:,.2f} ₽"],
        ['Завершено', str(stats['completed_sales'])],
        ['В ожидании', str(stats['pending_sales'])],
        ['Отменено', str(stats['cancelled_sales'])],
        ['Конверсия', f"{stats['conversion_rate']:.2f}%"]
    ]

    kpi_table = Table(kpi_data, colWidths=[100*mm, 60*mm])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(kpi_table)
    elements.append(Spacer(1, 30))

    # Топ товаров
    if top_products and len(top_products) > 0:
        elements.append(Paragraph("Топ-5 товаров", heading_style))

        top_data = [['№', 'Товар', 'Выручка', 'Продаж']]
        for idx, product in enumerate(top_products[:5], 1):
            top_data.append([
                str(idx),
                product['product_name'],
                f"{product['total_amount']:,.2f} ₽",
                str(product['sales_count'])
            ])

        top_table = Table(top_data, colWidths=[15*mm, 90*mm, 35*mm, 20*mm])
        top_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(top_table)
        elements.append(Spacer(1, 30))

    # Детализация продаж (последние 10)
    if sales and len(sales) > 0:
        elements.append(Paragraph("Последние продажи", heading_style))

        sales_data = [['Дата', 'Товар', 'Сумма', 'Кол-во', 'Статус']]
        for sale in sales[:10]:
            date_str = datetime.fromisoformat(sale['date'].replace('Z', '+00:00')).strftime('%d.%m.%Y')
            status_map = {
                'completed': 'Завершено',
                'pending': 'Ожидание',
                'cancelled': 'Отменено'
            }
            sales_data.append([
                date_str,
                sale['product_name'][:30],
                f"{sale['amount']:,.0f} ₽",
                str(sale['quantity']),
                status_map.get(sale['status'], sale['status'])
            ])

        sales_table = Table(sales_data, colWidths=[25*mm, 75*mm, 25*mm, 18*mm, 27*mm])
        sales_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(sales_table)

    # Генерируем PDF
    doc.build(elements)

    return pdf_path
