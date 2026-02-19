from django.urls import path
from .views import admin_issues_list, return_issue

urlpatterns = [
    path("admin/issues/", admin_issues_list),
    path("admin/issues/<uuid:id>/return/", return_issue),
]
