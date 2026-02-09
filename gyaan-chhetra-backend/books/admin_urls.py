from django.urls import path
from .admin_views import AdminBookAPIView, AdminBookDetailAPIView

urlpatterns = [
    path("", AdminBookAPIView.as_view()),
    path("<str:book_uuid>/", AdminBookDetailAPIView.as_view()),
]
