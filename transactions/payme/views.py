from payme.views import PaymeWebHookAPIView


class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def handle_created_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        """
        Handle the cancelled payment. You can override this method
        """