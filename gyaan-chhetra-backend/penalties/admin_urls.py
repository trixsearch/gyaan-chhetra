from django.urls import path
# ✅ I removed AdminCreateBorrowerAPIView from this list
from .admin_views import AdminPenaltyAPIView, AdminPayPenaltyAPIView

urlpatterns = [
    # ✅ I removed the "borrowers/" path because that view doesn't exist here
    path("", AdminPenaltyAPIView.as_view(), name="admin-penalties"),
    path("<uuid:uuid>/pay/", AdminPayPenaltyAPIView.as_view(), name="admin-pay-penalty"),
]