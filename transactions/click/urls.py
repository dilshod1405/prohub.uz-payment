from django.urls import path
from django.urls import include

from .views import ClickWebhookAPIView


urlpatterns = [
    path("update/", ClickWebhookAPIView.as_view()),
]