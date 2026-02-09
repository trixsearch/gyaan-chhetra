from django.urls import path
from .views import HealthCheckAPIView, MeAPIView, AdminStatsAPIView

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view(), name="health"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("admin/stats/", AdminStatsAPIView.as_view(), name="admin-stats"),
]