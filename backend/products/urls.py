from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_dashboard, name="product_dashboard"),
    path("export/csv/", views.export_csv, name="export_csv"),
    path("export/pdf/", views.export_pdf, name="export_pdf"),
]
