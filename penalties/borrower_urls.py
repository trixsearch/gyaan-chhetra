from django.urls import path
from .borrower_views import MyPenaltyAPIView

urlpatterns = [
    path("penalty/", MyPenaltyAPIView.as_view()),
]
