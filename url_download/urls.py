from django.urls import path

from .views import UrlDownloadView

urlpatterns = [
    path('downloads/', UrlDownloadView.as_view()),
]
