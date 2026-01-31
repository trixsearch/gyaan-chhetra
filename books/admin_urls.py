from django.urls import path
from .admin_views import AdminBookAPIView, AdminBookDetailAPIView

urlpatterns = [
    path("books/", AdminBookAPIView.as_view()),
    path("books/<str:book_uuid>/", AdminBookDetailAPIView.as_view()),
]
