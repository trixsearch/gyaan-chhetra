from django.urls import path
from .admin_views import BorrowerPenaltyAPIView

urlpatterns = [
    path("borrower/<str:borrower_uuid>/", BorrowerPenaltyAPIView.as_view()),
]
