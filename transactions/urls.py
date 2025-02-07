from django.urls import path
from .views import PaymentView

payment_list = PaymentView.as_view({'get': 'check_payment_status'})

urlpatterns = [
    path('payment/check_payment_status/<int:user_id>/<int:module_id>/', payment_list, name='payment-check-payment-status'),
]