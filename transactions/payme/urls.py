from django.urls import path
from django.urls import include

from .views import PaymeCallBackAPIView

urlpatterns = [
    path("update/", PaymeCallBackAPIView.as_view()),
]