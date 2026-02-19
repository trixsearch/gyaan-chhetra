from django.urls import path
from .views import LoginAPIView,admin_add_borrower,admin_borrowers_list

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
     path("admin/borrowers/", admin_borrowers_list),
    path("admin/borrowers/add/", admin_add_borrower),
]