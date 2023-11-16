


# views.py
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helpers import send_otp_to_phone
from .models import User

@api_view(['POST'])
def send_otp(request):
    data = request.data

    if data.get('phone_number') is None or data.get('password') is None:
        return Response({
            'status': 400,
            'message': 'Both phone_number and password are required.'
        })

    phone_number = data.get('phone_number')
    password = data.get('password')

    # Check if a user with the specified phone number already exists
    existing_user = User.objects.filter(phone_number=phone_number).first()
    if existing_user:
        return Response({
            'status': 400,
            'message': 'User with this phone number already exists.'
        })

    # If the user doesn't exist, create a new one
    user = User.objects.create(
        phone_number=phone_number,
        username=f"default_username_{phone_number}"  # Set a unique username based on phone_number
    )
    user.set_password(password)
    user.save()

    # Send OTP and save it to the user object
    otp = send_otp_to_phone(phone_number, user)

    if otp is not None:
        return Response({
            'status': 200,
            'message': 'Otp Sent'
        })
    else:
        return Response({
            'status': 500,
            'message': 'Failed to send OTP. Please try again.'
        })
   
def index(request):
    return render(request, 'myapp/index.html')

def home(request):
    return render(request, 'myapp/home.html')