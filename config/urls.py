"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Gyaan Chhetra API",
        default_version="v1",
        description="Library Management System APIs",
    ),
    public=False,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/accounts/",include("accounts.urls")),
    path("api/v1/admin/accounts/", include("accounts.admin_urls")),
    path("api/v1/admin/books/", include("books.admin_urls")),
    path("api/v1/borrower/", include("books.borrower_urls")),
    path("api/v1/borrower/issues/", include("issues.borrower_urls")),
    path("api/v1/borrower/", include("penalties.borrower_urls")),
    path("api/v1/admin/issues/", include("issues.admin_urls")),
    path("api/v1/books/", include("books.urls")),
    path("api/docs/",schema_view.with_ui("swagger", cache_timeout=0),name="swagger-docs",),
]
