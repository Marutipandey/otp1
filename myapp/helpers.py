import random
import requests
from django.conf import settings

# Use the api_key variable directly, not settings.api_key
api_key = getattr(settings, '293832-67745-11e5-88de-5600000c6b13', None)

def send_otp_to_phone(phone_number, user=None):
    try:
        otp = random.randint(1000, 9999)
        url = f'https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}'
        response = requests.get(url)
        
        # Log the response content for debugging
        print(response.content)

        # Save the OTP to the user model if a user is provided
        if user:
            user.otp = otp
            user.save()

        return otp
    except Exception as e:
        # Log the exception for debugging
        print(f"Error sending OTP: {e}")
        return None
