from payze.client import Payze
from payze.param import PayzeOPS
from payze.param import request as payze_req
from django.conf import settings

domain = settings.DOMAIN

payze = Payze(
    ops=PayzeOPS(
        url="https://payze.io",
        auth_token=f'{settings.PAYZE_KEY}:{settings.PAYZE_SECRET}',
        hooks=payze_req.Hooks(
            web_hook_gateway=f'https://{domain}/v1/webhook/payze/success',
            error_redirect_gateway=f'https://{domain}/v1/payment/payze/re-pay',
            success_redirect_gateway=f'https://{domain}/v1/payment/payze/thanks',
        )
    )
)

metadata = payze_req.Metadata(
    order=payze_req.Order(123),
)

req_params = payze_req.JustPay(
    amount=1,
    currency="USD",  # use currency=USD currency for VISA payments
    metadata=metadata,
)

# any kwarg fields are optional and can be extra attribute
resp = payze.just_pay(
    req_params=req_params,
    reason="for_trip",  # extra attribute example
)

print(resp.data.payment.payment_url)