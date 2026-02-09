from django.urls import path
from .admin_views import IssueBooksAPIView, ReturnBooksAPIView,BorrowerPenaltyAPIView

urlpatterns = [
    path("issue/", IssueBooksAPIView.as_view()),
    path("return/", ReturnBooksAPIView.as_view()),
    path("borrower/<str:borrower_uuid>/penalty/",BorrowerPenaltyAPIView.as_view(),),
]