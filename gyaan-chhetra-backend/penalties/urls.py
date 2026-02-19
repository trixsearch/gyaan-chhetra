from django.urls import path
from .views import admin_penalties_list, borrower_penalties

urlpatterns = [
    path("admin/penalties/", admin_penalties_list),
    path("borrower/penalties/", borrower_penalties),
]
