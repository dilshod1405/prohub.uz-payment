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

class PaymentView(viewsets.ViewSet):
    def get_user_details(self, user_id):
        try:
            # Fetch user details from the authentication service
            response = requests.get(f'{AUTH_SERVICE_URL}{user_id}/')
            if response.status_code == 200:
                user_data = response.json()
                # Store or update the user in the local database
                # check if the user exists
                user = User.objects.filter(email=user_data.get('email'), username=user_data.get('username')).first()
                # create the user if it does not exist
                if not user:
                    user, created = User.objects.get_or_create(
                        email=user_data.get('email'),
                        username=user_data.get('username'),
                        is_active=user_data.get('is_active')
                    )
                    return user
                # update the user
                else:
                    if user.username == user_data.get('username'):
                        user.delete()
                        user, created = User.objects.get_or_create(
                            email=user_data.get('email'),
                            username=user_data.get('username'),
                            is_active=user_data.get('is_active')
                        )
                        user.save()
                        return user
            else:
                print(f'Error: {response.status_code}')
                return None
        except requests.exceptions.RequestException:
            return None
    

    @action(detail=False, methods=['get'])
    def check_payment_status(self, request, user_id=None, module_id=None):
        # Get user details from the authentication service
        user_data = self.get_user_details(user_id)
        if not user_data:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has paid for the module
        payment = Payment.objects.filter(user_id=user_id, module_id=module_id, status='paid').first()
        return Response({"status": "paid" if payment else "not_paid"})
