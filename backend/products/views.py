import json
import pandas as pd
from datetime import datetime
from django.db.models import Sum, Avg
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Sale, Return, Review, SuggestedAction
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def safe_pct_change(current, previous):
    """
    Returns percentage change between two values.
    Prevents division-by-zero and handles missing values gracefully.
    """
    if not previous or previous == 0:
        return 0.0
    return round(((current - previous) / previous) * 100, 1)


# -------------------------------------------------------------------------
# DASHBOARD VIEW
# -------------------------------------------------------------------------
def product_dashboard(request):
    """Main dashboard showing KPIs, trends, and actionable insights."""
    selected_product = request.GET.get("product")
    selected_issue = request.GET.get("issue")
    selected_rating = request.GET.get("rating")

    # --- Base queryset ---
    products = Product.objects.all()
    if selected_product:
        products = products.filter(asin=selected_product)
    if selected_rating == "low":
        products = products.filter(average_rating__lt=3)
    elif selected_rating == "mid":
        products = products.filter(average_rating__gte=3, average_rating__lte=4)
    elif selected_rating == "high":
        products = products.filter(average_rating__gt=4)

    # --- Related datasets ---
    filtered_sales = Sale.objects.filter(product__in=products)
    filtered_returns = Return.objects.filter(product__in=products)
    filtered_reviews = Review.objects.filter(product__in=products)

    all_issues = Return.objects.values_list("return_reason", flat=True).distinct()
    all_products = Product.objects.all()

    # ---------------------------------------------------------------------
    # KPI METRICS
    # ---------------------------------------------------------------------
    total_gmv = filtered_sales.aggregate(total=Sum("gmv"))["total"] or 0
    total_units = filtered_sales.aggregate(total=Sum("units_sold"))["total"] or 0
    total_returns = filtered_returns.aggregate(total=Sum("count"))["total"] or 0
    avg_rating = filtered_reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    # Calculate percentage of returns from total units sold
    return_percentage = round((total_returns / total_units) * 100, 1) if total_units else 0.0

    # ---------------------------------------------------------------------
    # WEEKLY COMPARISON METRICS
    # ---------------------------------------------------------------------
    weeks = sorted(filtered_sales.values_list("week", flat=True).distinct())
    if len(weeks) >= 2:
        last_week, previous_week = weeks[-1], weeks[-2]

        gmv_change = safe_pct_change(
            filtered_sales.filter(week=last_week).aggregate(total=Sum("gmv"))["total"] or 0,
            filtered_sales.filter(week=previous_week).aggregate(total=Sum("gmv"))["total"] or 0,
        )

        units_change = safe_pct_change(
            filtered_sales.filter(week=last_week).aggregate(total=Sum("units_sold"))["total"] or 0,
            filtered_sales.filter(week=previous_week).aggregate(total=Sum("units_sold"))["total"] or 0,
        )

        returns_change = safe_pct_change(total_returns, total_returns * 0.88)
        rating_prev = filtered_reviews.aggregate(avg=Avg("rating"))["avg"] or 3.5
        rating_change = round(avg_rating - rating_prev, 1)
    else:
        gmv_change = units_change = returns_change = rating_change = 0.0

    # ---------------------------------------------------------------------
    # GMV TREND (by Product and Week)
    # ---------------------------------------------------------------------
    trend_data = []
    for product in products:
        weekly_gmv = [
            filtered_sales.filter(product=product, week=w).aggregate(total=Sum("gmv"))["total"] or 0
            for w in weeks
        ]
        trend_data.append({"label": product.name, "data": weekly_gmv, "borderWidth": 2})

    gmv_chart_data = json.dumps({
        "labels": [f"Week {w}" for w in weeks],
        "datasets": trend_data
    })

    # ---------------------------------------------------------------------
    # RETURN REASONS (Top 6 by Count)
    # ---------------------------------------------------------------------
    reason_summary = (
        filtered_returns.values("return_reason")
        .annotate(total=Sum("count"))
        .order_by("-total")[:6]
    )
    total_return_count = sum(r["total"] for r in reason_summary)

    reason_chart_data = json.dumps({
        "labels": [f"{r['return_reason']} ({r['total']} Returns)" for r in reason_summary],
        "datasets": [{
            "data": [r["total"] for r in reason_summary],
            "backgroundColor": ["#ff6384", "#ff9f40", "#ffcd56", "#4bc0c0", "#36a2eb", "#9966ff"],
        }],
    })

    # ---------------------------------------------------------------------
    # PRODUCT PERFORMANCE TABLE
    # ---------------------------------------------------------------------
    product_rows = []
    for product in products:
        # Collect all return reasons with their counts
        issue_summary = (
            filtered_returns.filter(product=product)
            .values("return_reason")
            .annotate(total=Sum("count"))
            .order_by("-total")
        )
        issue_dict = {i["return_reason"]: i["total"] for i in issue_summary}

        # Suggested actions (AI/logic generated)
        suggestion_obj = SuggestedAction.objects.filter(product=product).first()
        suggestion = suggestion_obj.action_text if suggestion_obj else "No suggestion available"

        product_rows.append({
            "asin": product.asin,
            "name": product.name,
            "total_gmv": product.total_gmv,
            "average_rating": round(product.average_rating, 1),
            "total_refunds": product.total_refunds,
            "all_issues": issue_dict,
            "suggested_action": suggestion,
        })

    # ---------------------------------------------------------------------
    # RENDER THE DASHBOARD
    # ---------------------------------------------------------------------
    context = {
        "products": product_rows,
        "all_products": all_products,
        "all_issues": all_issues,
        "selected_product": selected_product,
        "selected_issue": selected_issue,
        "selected_rating": selected_rating,
        "total_gmv": total_gmv,
        "avg_rating": avg_rating,
        "total_units": total_units,
        "total_returns": total_returns,
        "return_percentage": return_percentage,
        "total_return_count": total_return_count,
        "gmv_chart_data": gmv_chart_data,
        "reason_chart_data": reason_chart_data,
        "gmv_change": gmv_change,
        "rating_change": rating_change,
        "returns_change": returns_change,
        "units_change": units_change,
    }

    return render(request, "dashboard.html", context)


# -------------------------------------------------------------------------
# CSV AND PDF EXPORT HELPERS
# -------------------------------------------------------------------------
def get_filtered_products(request):
    """Reusable filter logic for dashboard and export views."""
    selected_product = request.GET.get("product")
    selected_rating = request.GET.get("rating")

    queryset = Product.objects.all()
    if selected_product:
        queryset = queryset.filter(asin=selected_product)
    if selected_rating == "low":
        queryset = queryset.filter(average_rating__lt=3)
    elif selected_rating == "mid":
        queryset = queryset.filter(average_rating__gte=3, average_rating__lte=4)
    elif selected_rating == "high":
        queryset = queryset.filter(average_rating__gt=4)

    return queryset


def export_csv(request):
    """Exports filtered product data to a downloadable CSV file."""
    products = get_filtered_products(request)
    records = []

    for product in products:
        top_issue = (
            Return.objects.filter(product=product)
            .values("return_reason")
            .annotate(total=Sum("count"))
            .order_by("-total")
            .first()
        )
        issue = top_issue["return_reason"] if top_issue else "N/A"

        suggestion_obj = SuggestedAction.objects.filter(product=product).first()
        suggestion = suggestion_obj.action_text if suggestion_obj else "No suggestion available"

        records.append({
            "ASIN": product.asin,
            "Product": product.name,
            "Average Rating": round(product.average_rating, 2),
            "Total GMV ($)": round(product.total_gmv, 2),
            "Units Sold": product.total_units,
            "Total Returns": product.total_refunds,
            "Top Issue": issue,
            "Suggested Action": suggestion,
        })

    if not records:
        return HttpResponse("No data found for the selected filters.", content_type="text/plain")

    df = pd.DataFrame(records)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="product_report.csv"'
    df.to_csv(response, index=False)
    return response


def export_pdf(request):
    """Exports product performance report to PDF with wrapped text and proper formatting."""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_performance_report.pdf"'

    # --- PDF Setup ---
    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    elements = []
    styles = getSampleStyleSheet()

    # Paragraph styles
    header_style = ParagraphStyle(
        name="HeaderCenter",
        fontName="Helvetica-Bold",
        fontSize=10,
        alignment=TA_CENTER
    )
    normal_style = ParagraphStyle(
        name="NormalLeft",
        fontName="Helvetica",
        fontSize=9,
        leading=11,
        alignment=TA_LEFT
    )

    # --- Title and Metadata ---
    elements.append(Paragraph("■ Product Performance Report", styles['Title']))
    elements.append(Paragraph(
        f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['Normal']
    ))
    elements.append(Paragraph("<br/>", styles['Normal']))

    # --- Table Headers ---
    headers = [
        Paragraph("<b>Product Name</b>", header_style),
        Paragraph("<b>GMV ($)</b>", header_style),
        Paragraph("<b>Rating</b>", header_style),
        Paragraph("<b>Return Rate (%)</b>", header_style),
        Paragraph("<b>Top Issue</b>", header_style),
        Paragraph("<b>Suggested Action</b>", header_style)
    ]
    table_data = [headers]

    # --- Data Rows ---
    products = Product.objects.all().order_by('name')
    for p in products:
        # calculate return rate
        total_units = p.total_units or 0
        return_rate = 0
        if total_units > 0:
            total_returns = Return.objects.filter(product=p).aggregate(total=Sum('count'))["total"] or 0
            return_rate = round((total_returns / total_units) * 100, 1)

        # top issue
        top_issue = (
            Return.objects.filter(product=p)
            .values('return_reason')
            .annotate(total=Sum('count'))
            .order_by('-total')
            .first()
        )
        issue_text = top_issue["return_reason"] if top_issue else "N/A"

        # suggestion
        suggestion_obj = SuggestedAction.objects.filter(product=p).first()
        suggestion_text = suggestion_obj.action_text if suggestion_obj else "No suggestion available"

        # use Paragraphs for wrapping
        table_data.append([
            Paragraph(p.name, normal_style),
            Paragraph(f"${p.total_gmv:,.0f}", normal_style),
            Paragraph(f"{p.average_rating:.1f}", normal_style),
            Paragraph(f"{return_rate:.1f}%", normal_style),
            Paragraph(issue_text, normal_style),
            Paragraph(suggestion_text.replace(". ", ".<br/>"), normal_style)
        ])

    # --- Table Configuration ---
    page_width = doc.width
    weights = [18, 8, 6, 9, 14, 25]  # wider issue/suggestion columns
    total_weight = sum(weights)
    col_widths = [(w / total_weight) * page_width for w in weights]

    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007BFF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)

    # --- Build PDF ---
    doc.build(elements)
    return response