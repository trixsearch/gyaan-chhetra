from django.urls import path
from .views import BookSearchAPIView

urlpatterns = [
    path("search/", BookSearchAPIView.as_view()),
]
