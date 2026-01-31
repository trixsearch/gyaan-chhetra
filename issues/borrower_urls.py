from django.urls import path
from .borrower_views import BorrowRequestAPIView, MyIssuedBooksAPIView

urlpatterns = [
    path("borrow/", BorrowRequestAPIView.as_view()),
    path("my-issues/", MyIssuedBooksAPIView.as_view()),
]
