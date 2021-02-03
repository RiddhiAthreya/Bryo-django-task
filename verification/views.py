from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
import base64
from .models import phoneModel
from django_otp.oath import TOTP
import time


# This class returns the string needed to generate the key
class KeyGeneration:
    @staticmethod
    def keyValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Secret Key"

  # create a TOTP object
class TOTPObject:
    @staticmethod
    def totp_obj(key):
        totp = TOTP(key=key,
                    step=100,
                    digits=6)
        totp.time = time.time()
        return totp    

class PhoneNumberRegistration(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists, take this , else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.save()  # Save the data
        keygen = KeyGeneration()
        #use base64 encoding to generate secret key
        key=base64.b32encode(keygen.keyValue(phone).encode())
        
        #make topt object and generate token
        totp = TOTPObject.totp_obj(key)
        totp.time = time.time()
        token = str(totp.token()).zfill(6)

        return Response({"OTP": token}, status=200) #This data can be sent to User's mobile through sms services

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = KeyGeneration()
        key = base64.b32encode(keygen.keyValue(phone).encode())

        totp = TOTPObject.totp_obj(key)
        totp.time = time.time()
        token=int(request.data["otp"])   
 
     
        if totp.verify(token):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)

    


