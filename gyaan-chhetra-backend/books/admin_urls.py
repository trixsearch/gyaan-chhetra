from django.urls import path
from .admin_views import AdminBookAPIView, AdminBookDetailAPIView,ExportBooksCSVAPIView

urlpatterns = [
    path("export/", ExportBooksCSVAPIView.as_view()),
    path("", AdminBookAPIView.as_view()),
    path("<str:book_uuid>/", AdminBookDetailAPIView.as_view()),
    
]
    