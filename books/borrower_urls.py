from django.urls import path
from .borrower_views import BorrowerBookListAPIView

urlpatterns = [
    path("books/", BorrowerBookListAPIView.as_view()),
]
