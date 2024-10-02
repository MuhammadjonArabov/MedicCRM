from datetime import datetime
from rest_framework.exceptions import ValidationError


def filter_seller_dashboard(request, queryset):
    date_year_str = request.query_params.get("date_year")
    date_month_str = request.query_params.get("date_month")
    by_year_queryset = queryset
    if date_year_str:
        try:
            date_year = datetime.strptime(date_year_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError({"date_year": "Unsupported format data"})
        else:
            queryset = queryset.filter(created_at__year=date_year.year)
            by_year_queryset = by_year_queryset.filter(created_at__year=date_year.year)
    if date_year_str and date_month_str:
        try:
            date_year = datetime.strptime(date_year_str, "%Y-%m-%d")
            date_month = datetime.strptime(date_month_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError({"date_year": "Unsupported format data"})
        else:
            queryset = queryset.filter(created_at__year=date_year.year, created_at__month=date_month.month)
    return queryset, by_year_queryset

