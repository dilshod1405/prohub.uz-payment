import requests
from django.conf import settings
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

AUTH_SERVICE_URL = f'{settings.AUTH_SERVICE_URL}/sendInfo/users/'
EDUCATION_SERVICE_URL = f'{settings.EDUCATION_SERVICE_URL}/edu/modules/'

class PaymentView(viewsets.ViewSet):
    def create_payment(self, user_id, module_id):
        try:
            # Fetch user details from the authentication service
            auth_response = requests.get(f'{AUTH_SERVICE_URL}{user_id}/')
            edu_response = requests.get(f'{EDUCATION_SERVICE_URL}{module_id}/')
            if auth_response.status_code == 200 and edu_response.status_code == 200:
                user_data = auth_response.json()
                edu_data = edu_response.json()
                user = User.objects.filter(email=user_data.get('email'), username=user_data.get('username')).first()
                # create the user if it does not exist
                if not user:
                    user, created = User.objects.get_or_create(
                        email=user_data.get('email'),
                        username=user_data.get('username'),
                        is_active=user_data.get('is_active'),
                        first_name=user_data.get('first_name'),
                        last_name=user_data.get('last_name')
                    )
                    # Store or update the payment in the local database
                    payment, created = Payment.objects.get_or_create(
                        user_id=user.id,
                        module_id=edu_data.get('id'),
                        amount=edu_data.get('price'),
                        status='pending'
                    )
                
                    return payment
                
                # update the user
                else:
                    if user:
                        payment, created = Payment.objects.get_or_create(
                            user_id=User.objects.get(username=user_data.get('username')).id,
                            module_id=edu_data.get('id'),
                            amount=edu_data.get('price'),
                            status='pending'
                        )
                        return payment
            else:
                return None
        except requests.exceptions.RequestException:
            return None

    @action(detail=False, methods=['get'])
    def check_status(self, request, user_id=None, module_id=None):
        # Get user details from the authentication service
        payment_data = self.create_payment(user_id, module_id)
        if not payment_data:
            return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)


        # Check if the user has paid for the module
        payment = Payment.objects.filter(user_id=user_id, module_id=module_id, status='paid').first()
        return Response({"status": "paid" if payment else "not_paid"})
