from django.urls import path
from .views import HealthCheckAPIView, MeAPIView, AdminStatsAPIView
from .dashboard_views import AdminDashboardAPIView
from .admin_stats import AdminStatsAPIView


urlpatterns = [
    path("health/", HealthCheckAPIView.as_view(), name="health"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("admin/stats/", AdminStatsAPIView.as_view(), name="admin-stats"),
    path("admin/dashboard/", AdminDashboardAPIView.as_view()),
    path("admin/stats/", AdminStatsAPIView.as_view()),
]