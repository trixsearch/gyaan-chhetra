from django.urls import path
from .admin_views import (
    BorrowerListCreateAPIView,
    BorrowerDetailAPIView,
)

urlpatterns = [
    path("borrowers/", BorrowerListCreateAPIView.as_view()),
    path("borrowers/<uuid:borrower_uuid>/", BorrowerDetailAPIView.as_view()),
]