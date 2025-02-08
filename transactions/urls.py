from django.urls import path
from .views import PaymentView

payment_list = PaymentView.as_view({'get': 'check_status'})

urlpatterns = [
    path('check_status/<int:user_id>/<int:module_id>/', payment_list, name='payment-check-payment-status'),
]